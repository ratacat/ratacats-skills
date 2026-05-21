# Indexing Strategies

## Overview

Indexes are the primary tool for accelerating database queries. A well-designed indexing strategy can transform a query from minutes to milliseconds. A poorly designed one wastes disk space and slows writes with no benefit.

**Core insight:** Indexes trade write performance for read performance. Every index you add must be justified by the queries it accelerates.

---

## What Is an Index?

An index is:
1. **A redundant data structure** — Can be dropped without data loss, rebuilt from table data
2. **Invisible to the application** — Same query results with or without index
3. **Designed to speed up data selection** — Based on specific filtering criteria

> "An index provides additional data access paths; it allows us to determine what values are stored in the rows of a table without actually reading the table."

### The Fundamental Trade-off

| Operation | Without Index | With Index |
|-----------|---------------|------------|
| **Full table scan** | O(n) — read all rows | Still O(n) if no filter uses index |
| **Point lookup** | O(n) — scan to find | O(log n) — tree traversal |
| **INSERT** | Fast — just append | Slower — update index too |
| **UPDATE** | Fast (on indexed column) | Slower — update index too |
| **DELETE** | Fast | Slower — update index too |

---

## PostgreSQL Index Types

### B-tree (Default)

The most common index structure, suitable for most queries.

**Supports:**
- Equality: `=`
- Range: `<`, `<=`, `>`, `>=`, `BETWEEN`
- Pattern: `LIKE 'prefix%'` (prefix only)
- Ordering: `ORDER BY`
- NULL handling: `IS NULL`, `IS NOT NULL`

**Structure:**
- Balanced tree with O(log n) depth
- Typical branching factor: hundreds of pointers per page
- 4-level tree can store billions of rows

```sql
CREATE INDEX idx_users_email ON users (email);
CREATE INDEX idx_orders_date ON orders (order_date);
```

**When to use:** Default choice for most columns. Use unless you have specific reason for another type.

### Hash

Uses hash function to compute index block address.

**Supports:**
- Equality only: `=`

**Does NOT support:**
- Range queries
- Ordering
- Pattern matching

```sql
CREATE INDEX idx_users_id_hash ON users USING HASH (id);
```

**When to use:** Only for exact-match lookups where you'll never need range queries. B-tree is almost always a better choice.

### GiST (Generalized Search Tree)

Framework for building custom index types.

**Built-in support for:**
- Geometric data (points, boxes, polygons)
- Range types
- Full-text search
- Nearest-neighbor queries

```sql
-- Geometric containment
CREATE INDEX idx_locations ON stores USING GIST (location);
SELECT * FROM stores WHERE location <@ box '((0,0),(10,10))';

-- Range exclusion constraint
CREATE TABLE reservations (
    room_id INT,
    during TSTZRANGE,
    EXCLUDE USING GIST (room_id WITH =, during WITH &&)
);
```

**When to use:** Spatial data, range types, or any data where you need overlap/containment queries.

### GIN (Generalized Inverted Index)

Maps values to lists of row locations. Excellent for multi-valued columns.

**Ideal for:**
- Arrays: `@>`, `&&`, `<@`
- JSONB: `@>`, `?`, `?|`, `?&`
- Full-text search: `@@`
- Trigram similarity

```sql
-- Array containment
CREATE INDEX idx_tags ON articles USING GIN (tags);
SELECT * FROM articles WHERE tags @> ARRAY['postgresql'];

-- JSONB containment
CREATE INDEX idx_data ON events USING GIN (data);
SELECT * FROM events WHERE data @> '{"type": "click"}';

-- Full-text search
CREATE INDEX idx_content ON documents USING GIN (to_tsvector('english', content));
```

**When to use:** Columns containing multiple values that need to be individually searchable.

### BRIN (Block Range Index)

Stores summary info about ranges of physical table blocks.

**Characteristics:**
- Very small (orders of magnitude smaller than B-tree)
- Best for naturally ordered data (timestamps, sequences)
- Less precise — may read extra blocks

```sql
-- Time-series data with natural ordering
CREATE INDEX idx_events_time ON events USING BRIN (created_at);
```

**When to use:** Very large tables where data is physically ordered by the indexed column (e.g., append-only time-series).

---

## Index Type Decision Matrix

| Query Pattern | Best Index Type |
|---------------|-----------------|
| Equality (`=`) | B-tree (or Hash) |
| Range (`<`, `>`, `BETWEEN`) | B-tree |
| Pattern prefix (`LIKE 'abc%'`) | B-tree |
| Pattern anywhere (`LIKE '%abc%'`) | GIN with pg_trgm |
| Array containment (`@>`) | GIN |
| JSONB containment (`@>`) | GIN |
| Full-text search (`@@`) | GIN |
| Geometric (contains, overlaps) | GiST |
| Range overlaps | GiST |
| Nearest neighbor | GiST |
| Very large table, ordered data | BRIN |

---

## How Indexes Are Used

### Selectivity: The Key Factor

**Selectivity** = (rows matching filter) / (total rows)

The choice between index scan and sequential scan depends on selectivity:

| Selectivity | Best Access Method |
|-------------|-------------------|
| < 5-10% | Index scan |
| > 5-10% | Sequential scan |

**Why?** Random I/O (index scan) is expensive. When you're reading most of the table anyway, sequential I/O (full scan) is faster.

### Data Access Algorithms

PostgreSQL chooses between several access methods:

**Sequential Scan:**
```
Read all blocks → Filter rows → Return matches
```
Cost: O(n) I/O + O(n) CPU

**Index Scan:**
```
Read index → For each match, fetch table row → Return
```
Cost: O(log n + k) where k = matching rows
Problem: May read same table block multiple times

**Bitmap Index Scan:**
```
Read index → Build bitmap of matching blocks → Read blocks → Filter rows
```
Benefits:
- Reads each block at most once
- Can combine multiple indexes with AND/OR
- Better for medium selectivity

**Index-Only Scan:**
```
Read index → Return data directly from index
```
Best case: Index contains all needed columns (covering index)

### When Indexes Cannot Be Used

Indexes won't help when:

1. **Expression applied to column:**
```sql
-- BAD: Cannot use index on created_at
WHERE EXTRACT(YEAR FROM created_at) = 2023

-- GOOD: Use range instead
WHERE created_at >= '2023-01-01' AND created_at < '2024-01-01'
```

2. **Type mismatch:**
```sql
-- If column is INTEGER
WHERE user_id = '123'  -- String comparison, may not use index
```

3. **Leading wildcard:**
```sql
WHERE name LIKE '%smith'  -- Cannot use B-tree index
```

4. **OR conditions on different columns:**
```sql
WHERE email = 'x' OR phone = 'y'  -- May not use either index efficiently
```

5. **Low selectivity:**
```sql
WHERE active = true  -- If 95% of rows are active, index scan is slower
```

---

## Composite Indexes

Index on multiple columns in specific order.

```sql
CREATE INDEX idx_orders_customer_date ON orders (customer_id, order_date);
```

### Column Order Matters

The index above supports:
- `WHERE customer_id = ?` — Uses index
- `WHERE customer_id = ? AND order_date = ?` — Uses index fully
- `WHERE customer_id = ? AND order_date > ?` — Uses index fully
- `WHERE order_date = ?` — **Cannot use this index** (wrong prefix)

**Rule:** Put equality columns first, then range columns.

### Covering Indexes (INCLUDE)

Include additional columns in index for index-only scans:

```sql
CREATE INDEX idx_orders_covering ON orders (customer_id, order_date)
    INCLUDE (total, status);
```

Now this query uses index-only scan:
```sql
SELECT order_date, total, status
FROM orders
WHERE customer_id = 123;
```

---

## Partial Indexes

Index only a subset of rows.

```sql
-- Only index active users
CREATE INDEX idx_active_users ON users (email)
    WHERE active = true;

-- Only index recent orders
CREATE INDEX idx_recent_orders ON orders (customer_id)
    WHERE order_date > '2023-01-01';
```

**Benefits:**
- Smaller index size
- Faster to maintain
- Better cache utilization

**Use when:**
- Query always includes the filter condition
- Most rows don't match the condition

---

## Expression Indexes

Index on computed expression.

```sql
-- Index on lowercase email
CREATE INDEX idx_users_email_lower ON users (LOWER(email));

-- Query uses the index
SELECT * FROM users WHERE LOWER(email) = 'user@example.com';

-- Index on JSON field
CREATE INDEX idx_events_user ON events ((data->>'user_id'));
```

**Important:** Query must use exact same expression.

---

## Index Strategies by Query Pattern

### Single-Column Equality

```sql
SELECT * FROM users WHERE id = 123;
```
**Strategy:** B-tree index on `id`

### Single-Column Range

```sql
SELECT * FROM orders WHERE created_at > '2023-01-01';
```
**Strategy:** B-tree index on `created_at`

### Multiple Equality Conditions

```sql
SELECT * FROM orders WHERE customer_id = 123 AND status = 'pending';
```
**Strategy:** Composite index `(customer_id, status)` or separate indexes (PostgreSQL can combine with bitmap)

### Equality + Range

```sql
SELECT * FROM orders
WHERE customer_id = 123
AND order_date BETWEEN '2023-01-01' AND '2023-12-31';
```
**Strategy:** Composite index `(customer_id, order_date)` — equality column first

### Sorting

```sql
SELECT * FROM orders WHERE customer_id = 123 ORDER BY order_date DESC;
```
**Strategy:** Composite index `(customer_id, order_date DESC)`

### Pattern Matching

```sql
-- Prefix match
SELECT * FROM users WHERE name LIKE 'John%';
-- Strategy: B-tree index (works for prefix)

-- Anywhere match
SELECT * FROM users WHERE name LIKE '%john%';
-- Strategy: GIN with pg_trgm extension
CREATE EXTENSION pg_trgm;
CREATE INDEX idx_users_name_trgm ON users USING GIN (name gin_trgm_ops);
```

### JSONB Queries

```sql
SELECT * FROM events WHERE data @> '{"type": "click"}';
```
**Strategy:** GIN index on JSONB column
```sql
CREATE INDEX idx_events_data ON events USING GIN (data);
```

### Full-Text Search

```sql
SELECT * FROM articles WHERE to_tsvector('english', body) @@ to_tsquery('postgresql');
```
**Strategy:** GIN index on tsvector
```sql
CREATE INDEX idx_articles_fts ON articles USING GIN (to_tsvector('english', body));
```

---

## Query Planner Behavior

### Viewing Execution Plans

```sql
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';

-- With actual timing
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';
```

### Reading EXPLAIN Output

Key things to look for:

| Node Type | Meaning |
|-----------|---------|
| `Seq Scan` | Full table scan (no index) |
| `Index Scan` | Using index, fetching from table |
| `Index Only Scan` | Using index alone (covering) |
| `Bitmap Heap Scan` | Index → bitmap → fetch blocks |
| `Nested Loop` | For each row in outer, scan inner |
| `Hash Join` | Build hash table, probe |
| `Merge Join` | Sorted merge of two inputs |

### Statistics and Cost Estimation

PostgreSQL relies on table statistics to choose execution plans:

```sql
-- Update statistics
ANALYZE users;

-- View statistics
SELECT * FROM pg_stats WHERE tablename = 'users';
```

**Critical statistics:**
- Row count
- Column cardinality (distinct values)
- Most common values
- Histogram of value distribution

---

## Common Indexing Mistakes

### 1. Over-Indexing

**Problem:** Creating indexes for every possible query.

**Cost:**
- Each index slows INSERT/UPDATE/DELETE
- Disk space usage
- Maintenance overhead

**Solution:** Index only what you query. Monitor and drop unused indexes.

```sql
-- Find unused indexes
SELECT schemaname, relname, indexrelname, idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0;
```

### 2. Indexing Low-Cardinality Columns

**Problem:** Index on boolean or status column with few values.

```sql
-- BAD: Most queries select 95% of rows
CREATE INDEX idx_users_active ON users (active);
SELECT * FROM users WHERE active = true;  -- Will use seq scan anyway
```

**Solution:** Use partial index if one value is rare:
```sql
CREATE INDEX idx_users_inactive ON users (id) WHERE active = false;
```

### 3. Wrong Column Order in Composite Index

**Problem:** Range column before equality column.

```sql
-- BAD: Can only use index partially
CREATE INDEX idx_orders ON orders (order_date, customer_id);
SELECT * FROM orders WHERE customer_id = 123 AND order_date > '2023-01-01';

-- GOOD: Equality first, then range
CREATE INDEX idx_orders ON orders (customer_id, order_date);
```

### 4. Function Wrapping Indexed Column

**Problem:** Applying function to column in WHERE clause.

```sql
-- BAD: Cannot use index
WHERE UPPER(email) = 'TEST@EXAMPLE.COM';

-- GOOD: Expression index or fix at write time
CREATE INDEX idx_email_upper ON users (UPPER(email));
```

### 5. Neglecting Index Maintenance

**Problem:** Bloated indexes after many updates/deletes.

**Solution:**
```sql
-- Rebuild index
REINDEX INDEX idx_users_email;

-- Rebuild concurrently (no lock)
REINDEX INDEX CONCURRENTLY idx_users_email;
```

---

## Index Maintenance

### Creating Indexes Without Locking

```sql
-- Blocks writes during creation (default)
CREATE INDEX idx_users_email ON users (email);

-- Does not block writes (takes longer)
CREATE INDEX CONCURRENTLY idx_users_email ON users (email);
```

### Monitoring Index Usage

```sql
-- Index usage statistics
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;
```

### Index Size

```sql
SELECT
    indexname,
    pg_size_pretty(pg_relation_size(indexname::regclass)) AS size
FROM pg_indexes
WHERE tablename = 'users';
```

### Bloat Detection

After many updates, indexes can become bloated:

```sql
-- Install pgstattuple extension
CREATE EXTENSION pgstattuple;

-- Check bloat
SELECT * FROM pgstattuple('idx_users_email');
```

---

## Indexing Strategy Process

### Step 1: Identify Critical Queries

List your most important queries:
- Most frequently executed
- Slowest response times
- Business-critical paths

### Step 2: Analyze Without Indexes

```sql
EXPLAIN ANALYZE SELECT ...;
```

Look for:
- Seq Scans on large tables
- High row estimates
- Long execution times

### Step 3: Design Indexes

For each query:
1. Identify filter columns (WHERE)
2. Identify join columns
3. Identify sort columns (ORDER BY)
4. Consider covering columns (SELECT list)

### Step 4: Test and Measure

```sql
-- Create index
CREATE INDEX CONCURRENTLY ...;

-- Update statistics
ANALYZE tablename;

-- Verify usage
EXPLAIN ANALYZE SELECT ...;
```

### Step 5: Monitor Over Time

- Track query performance
- Monitor index usage
- Remove unused indexes
- Adjust as data and queries change

---

## Key Takeaways

1. **Indexes trade write for read performance.** Only create indexes that accelerate queries you actually run.

2. **B-tree is the default.** Use other types only for specific needs (GIN for arrays/JSONB, GiST for geometry).

3. **Selectivity determines usefulness.** Low-selectivity indexes may never be used.

4. **Column order matters.** Put equality columns before range columns in composite indexes.

5. **Use EXPLAIN ANALYZE.** Don't guess—verify that indexes are being used.

6. **Create concurrently.** Use `CREATE INDEX CONCURRENTLY` in production.

7. **Monitor and maintain.** Track usage, remove unused indexes, rebuild bloated ones.

8. **Expression indexes match expressions.** Query must use exact same expression.

---

## References

- Dombrovskaya, H. et al. *PostgreSQL Query Optimization*, Chapters 3, 5, 14
- Fontaine, D. *The Art of PostgreSQL*, Indexing chapters
- PostgreSQL Documentation: Indexes
