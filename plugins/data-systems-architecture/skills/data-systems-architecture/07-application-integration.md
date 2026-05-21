# Application Integration

## Overview

The interface between your application and database is where architecture decisions become reality. Poor integration patterns can negate all the benefits of good schema design and indexing. This chapter covers practical patterns for connecting applications to PostgreSQL effectively.

**Core insight:** Network round-trips are often the dominant factor in database performance. Reducing round-trips matters more than micro-optimizing individual queries.

---

## The N+1 Query Problem

The most common performance anti-pattern in database-backed applications.

### What Is N+1?

```python
# BAD: N+1 queries
artists = db.query("SELECT * FROM artist LIMIT 10")  # 1 query
for artist in artists:
    # N additional queries (one per artist)
    albums = db.query(f"SELECT * FROM album WHERE artistid = {artist.id}")
    for album in albums:
        print(f"{artist.name}: {album.title}")
```

This executes 1 + N queries. With 100 artists, that's 101 queries.

### Why It's Expensive

| Factor | Impact |
|--------|--------|
| **Network latency** | 1-2ms per round-trip, multiplied by N |
| **Connection overhead** | Each query has setup/teardown |
| **Query parsing** | Database parses each query separately |
| **Lock contention** | More queries = more lock operations |

**Example calculation:**
- 100 artists, 2ms round-trip each
- N+1 approach: 101 * 2ms = 202ms
- Single query: 1 * 2ms = 2ms (100x faster)

### The Solution: JOIN

```sql
-- GOOD: Single query with JOIN
SELECT artist.name, album.title
FROM artist
JOIN album USING (artistid)
ORDER BY artist.name, album.title;
```

Or with aggregation:

```sql
SELECT artist.name,
       array_agg(album.title ORDER BY album.title) as albums
FROM artist
JOIN album USING (artistid)
GROUP BY artist.artistid
ORDER BY artist.name;
```

### Detecting N+1 in ORMs

Most ORMs default to lazy loading, which causes N+1:

```python
# Django (lazy loading - N+1)
artists = Artist.objects.all()[:10]
for artist in artists:
    for album in artist.album_set.all():  # Triggers query per artist
        print(album.title)

# Django (eager loading - single query)
artists = Artist.objects.prefetch_related('album_set').all()[:10]
```

```ruby
# Rails (lazy loading - N+1)
Artist.limit(10).each do |artist|
  artist.albums.each { |album| puts album.title }
end

# Rails (eager loading - single query)
Artist.includes(:albums).limit(10).each do |artist|
  artist.albums.each { |album| puts album.title }
end
```

### Query Logging

Enable query logging to detect N+1:

```python
# Django settings.py
LOGGING = {
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
        },
    },
}
```

Look for patterns of repeated similar queries.

---

## ORM Pitfalls

ORMs are convenient but can hide performance problems.

### Common ORM Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| **SELECT *** | Fetches unused columns | Select only needed columns |
| **Lazy loading** | N+1 queries | Use eager loading |
| **In-memory filtering** | Fetches all rows, filters in app | Use WHERE clause |
| **In-memory sorting** | Fetches all rows, sorts in app | Use ORDER BY |
| **Object hydration** | Creates objects for aggregate queries | Use raw queries for reports |

### SELECT * Is Expensive

```python
# BAD: Fetches all columns including large text fields
user = User.objects.get(id=1)
print(user.name)  # Only needed name, but fetched bio, avatar, etc.

# GOOD: Fetch only what you need
user = User.objects.only('name').get(id=1)

# Or with values:
name = User.objects.filter(id=1).values_list('name', flat=True).first()
```

With TOAST columns (large values stored separately), SELECT * triggers extra I/O even for columns you don't use.

### In-Memory vs Database Operations

```python
# BAD: Filter in Python
active_users = [u for u in User.objects.all() if u.is_active]

# GOOD: Filter in database
active_users = User.objects.filter(is_active=True)
```

```python
# BAD: Sort in Python
users = sorted(User.objects.all(), key=lambda u: u.created_at)

# GOOD: Sort in database
users = User.objects.order_by('created_at')
```

```python
# BAD: Count in Python
count = len(User.objects.all())

# GOOD: Count in database
count = User.objects.count()
```

### When to Use Raw SQL

ORMs struggle with:
- Complex aggregations
- Window functions
- Recursive queries
- Bulk operations
- Performance-critical queries

```python
# Complex query - use raw SQL
from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("""
        WITH monthly_sales AS (
            SELECT date_trunc('month', created_at) as month,
                   SUM(amount) as total
            FROM orders
            GROUP BY 1
        )
        SELECT month,
               total,
               total - LAG(total) OVER (ORDER BY month) as change
        FROM monthly_sales
        ORDER BY month
    """)
    results = cursor.fetchall()
```

---

## Where to Put Business Logic

Three options, each with trade-offs.

### Option 1: Application Code Only

```python
def transfer_money(from_id, to_id, amount):
    with transaction.atomic():
        from_account = Account.objects.select_for_update().get(id=from_id)
        to_account = Account.objects.select_for_update().get(id=to_id)

        if from_account.balance < amount:
            raise InsufficientFunds()

        from_account.balance -= amount
        to_account.balance += amount
        from_account.save()
        to_account.save()
```

**Pros:**
- Logic in familiar language
- Easy to test
- Version controlled with application

**Cons:**
- More network round-trips
- Logic scattered across codebase
- Concurrency handled in application

### Option 2: Stored Procedures

```sql
CREATE OR REPLACE FUNCTION transfer_money(
    from_id INT,
    to_id INT,
    amount NUMERIC
) RETURNS void AS $$
DECLARE
    from_balance NUMERIC;
BEGIN
    -- Lock accounts
    SELECT balance INTO from_balance
    FROM accounts WHERE id = from_id FOR UPDATE;

    IF from_balance < amount THEN
        RAISE EXCEPTION 'Insufficient funds';
    END IF;

    UPDATE accounts SET balance = balance - amount WHERE id = from_id;
    UPDATE accounts SET balance = balance + amount WHERE id = to_id;
END;
$$ LANGUAGE plpgsql;
```

**Pros:**
- Single network round-trip
- Logic close to data
- Consistent enforcement across all clients

**Cons:**
- Different language (PL/pgSQL)
- Harder to test
- Deployment coupled with schema

### Option 3: Hybrid Approach (Recommended)

- **Application code:** Complex business rules, validation, orchestration
- **Database:** Data integrity constraints, simple transformations, aggregations

```python
# Application handles orchestration
def process_order(order_data):
    validate_order(order_data)  # Application logic

    with transaction.atomic():
        # Database handles atomicity and constraints
        order = Order.objects.create(**order_data)

        # Use database for efficient bulk operations
        connection.cursor().execute("""
            INSERT INTO order_items (order_id, product_id, quantity, price)
            SELECT %s, product_id, quantity,
                   quantity * price_per_unit
            FROM unnest(%s::int[], %s::int[]) AS t(product_id, quantity)
            JOIN products USING (product_id)
        """, [order.id, product_ids, quantities])
```

---

## Connection Management

### Connection Pooling

Database connections are expensive to create. Use a pool.

**Without pooling:**
```
Request → Create connection → Execute query → Close connection
Request → Create connection → Execute query → Close connection
...
```

**With pooling:**
```
Request → Get connection from pool → Execute query → Return to pool
Request → Get connection from pool → Execute query → Return to pool
...
```

### PgBouncer (External Pooler)

Most common PostgreSQL connection pooler.

```ini
# pgbouncer.ini
[databases]
mydb = host=localhost dbname=mydb

[pgbouncer]
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 20
```

**Pool modes:**

| Mode | Description | Use Case |
|------|-------------|----------|
| **session** | Connection held for entire session | Prepared statements, temp tables |
| **transaction** | Connection held for transaction | Most applications |
| **statement** | Connection per statement | Simple queries only |

### Application-Level Pooling

Most ORMs and drivers support pooling:

```python
# Django
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'CONN_MAX_AGE': 600,  # Reuse connections for 10 minutes
    }
}

# SQLAlchemy
engine = create_engine(
    'postgresql://...',
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
)
```

### Connection Sizing

**Rule of thumb:** `connections = (cores * 2) + spindles`

For SSD systems: `connections ≈ cores * 2`

More connections ≠ better performance. Too many connections:
- Increase memory usage
- Cause lock contention
- Reduce throughput

---

## Prepared Statements

Parse query once, execute many times.

### Benefits

| Benefit | Description |
|---------|-------------|
| **Parse once** | Query plan computed once |
| **Binary protocol** | More efficient than text |
| **SQL injection prevention** | Parameters separated from query |

### PostgreSQL Prepared Statements

```sql
-- Prepare once
PREPARE get_user(int) AS
SELECT * FROM users WHERE id = $1;

-- Execute many times
EXECUTE get_user(1);
EXECUTE get_user(2);
EXECUTE get_user(3);
```

### Driver-Level Preparation

Most drivers handle this automatically:

```python
# psycopg2 - server-side prepared statements
cursor.execute("SELECT * FROM users WHERE id = %s", [user_id])

# With explicit preparation
cursor.execute("PREPARE get_user AS SELECT * FROM users WHERE id = $1")
cursor.execute("EXECUTE get_user(%s)", [user_id])
```

### Prepared Statement Gotchas

1. **Plan caching:** First few executions use generic plan, then specialized
2. **Parameter sniffing:** Plan optimized for first parameter values
3. **Session scope:** Prepared statements live in session; lost on disconnect
4. **PgBouncer transaction mode:** Doesn't support server-side prepared statements

---

## Batch Operations

### Bulk Inserts

```python
# BAD: One insert at a time
for item in items:
    cursor.execute("INSERT INTO items (name) VALUES (%s)", [item.name])

# GOOD: Batch insert
cursor.executemany(
    "INSERT INTO items (name) VALUES (%s)",
    [(item.name,) for item in items]
)

# BETTER: COPY (fastest for large datasets)
from io import StringIO
buffer = StringIO()
for item in items:
    buffer.write(f"{item.name}\n")
buffer.seek(0)
cursor.copy_from(buffer, 'items', columns=['name'])
```

### Bulk Updates

```sql
-- Using UPDATE FROM VALUES
UPDATE items
SET price = v.price
FROM (VALUES
    (1, 10.00),
    (2, 20.00),
    (3, 30.00)
) AS v(id, price)
WHERE items.id = v.id;

-- Using unnest for arrays
UPDATE items
SET price = data.price
FROM unnest(
    ARRAY[1, 2, 3]::int[],
    ARRAY[10.00, 20.00, 30.00]::numeric[]
) AS data(id, price)
WHERE items.id = data.id;
```

### UPSERT (INSERT ... ON CONFLICT)

```sql
INSERT INTO items (id, name, quantity)
VALUES (1, 'Widget', 10)
ON CONFLICT (id) DO UPDATE
SET quantity = items.quantity + EXCLUDED.quantity;
```

---

## Query Patterns

### Pagination

```sql
-- Offset pagination (simple, but slow for large offsets)
SELECT * FROM items ORDER BY id LIMIT 20 OFFSET 1000;

-- Keyset pagination (fast, consistent)
SELECT * FROM items
WHERE id > :last_seen_id
ORDER BY id
LIMIT 20;
```

Keyset pagination is O(1); offset pagination is O(offset).

### Counting with Estimates

```sql
-- Exact count (slow for large tables)
SELECT count(*) FROM items WHERE active = true;

-- Estimate from statistics (fast, approximate)
SELECT reltuples::bigint FROM pg_class WHERE relname = 'items';

-- Hybrid: exact for small, estimate for large
SELECT CASE
    WHEN c.reltuples < 10000 THEN
        (SELECT count(*) FROM items WHERE active = true)
    ELSE
        c.reltuples::bigint
END
FROM pg_class c WHERE c.relname = 'items';
```

### EXISTS vs COUNT

```sql
-- BAD: Count when you only need existence
SELECT CASE WHEN count(*) > 0 THEN true ELSE false END
FROM orders WHERE user_id = 1;

-- GOOD: EXISTS stops at first match
SELECT EXISTS(SELECT 1 FROM orders WHERE user_id = 1);
```

### Returning Data After Insert

```sql
-- Instead of INSERT then SELECT
INSERT INTO users (name, email)
VALUES ('Jane', 'jane@example.com')
RETURNING id, created_at;
```

---

## SQL File Management

Keep SQL in version-controlled files:

```
app/
  sql/
    users/
      get_by_id.sql
      search.sql
    orders/
      create.sql
      list_by_user.sql
```

**Benefits:**
- Version controlled
- Syntax highlighting
- Easy to test in psql
- Can be reviewed by DBAs

### Loading SQL in Application

```python
# Load SQL from files
def load_sql(name):
    with open(f'sql/{name}.sql') as f:
        return f.read()

GET_USER = load_sql('users/get_by_id')

# Use in queries
cursor.execute(GET_USER, {'id': user_id})
```

---

## Monitoring Application Queries

### pg_stat_statements

Track query performance across all sessions:

```sql
-- Enable extension
CREATE EXTENSION pg_stat_statements;

-- Find slowest queries
SELECT query,
       calls,
       mean_time,
       total_time / 1000 as total_seconds
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;

-- Find most called queries
SELECT query, calls
FROM pg_stat_statements
ORDER BY calls DESC
LIMIT 10;
```

### Application-Level Logging

Log slow queries in your application:

```python
import time
import logging

def timed_query(cursor, sql, params=None):
    start = time.time()
    cursor.execute(sql, params)
    duration = time.time() - start

    if duration > 0.1:  # Log queries over 100ms
        logging.warning(f"Slow query ({duration:.3f}s): {sql}")

    return cursor
```

---

## Common Mistakes

| Mistake | Why It's Wrong | Better Approach |
|---------|----------------|-----------------|
| N+1 queries | Network latency dominates | Use JOINs or eager loading |
| SELECT * | Fetches unused data | Select only needed columns |
| Not using connection pooling | Connection creation is expensive | Use PgBouncer or driver pooling |
| Large transactions | Hold locks, block VACUUM | Keep transactions short |
| Offset pagination | O(offset) performance | Use keyset pagination |
| COUNT for existence | Scans all matches | Use EXISTS |
| ORM for everything | Misses database features | Raw SQL for complex queries |

---

## Key Takeaways

1. **Network round-trips are expensive.** Minimize them with JOINs, batch operations, and proper query design.

2. **N+1 is the most common performance bug.** Use eager loading or explicit JOINs.

3. **ORMs hide important details.** Understand the SQL they generate.

4. **Use connection pooling.** PgBouncer or driver-level pooling.

5. **Put logic where it makes sense.** Database for integrity, application for business rules.

6. **Batch operations are faster.** Use COPY, multi-value INSERT, bulk UPDATE.

7. **Monitor your queries.** pg_stat_statements and application-level logging.

8. **SQL files are code.** Version control them like any other code.

---

## References

- Fontaine, D. *The Art of PostgreSQL*, Parts III-V
- Dombrovskaya, H. et al. *PostgreSQL Query Optimization*, Chapters 7-8
- PostgreSQL Documentation: libpq, psycopg2
