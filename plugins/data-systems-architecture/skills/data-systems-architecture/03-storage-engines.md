# Storage Engines and Data Structures

## Overview

Understanding how databases store and retrieve data is essential for making good architectural decisions. The choice of storage engine fundamentally shapes your system's performance characteristics—what operations are fast, what are slow, and where the trade-offs lie.

**Core insight:** There is a fundamental trade-off between write performance and read performance. Different storage engines make different trade-offs, and choosing the right one requires understanding your workload.

---

## The Fundamental Trade-off

Every database must do two things:
1. **Store data** when you give it data
2. **Retrieve data** when you ask for it later

The simplest possible storage is an append-only log file:

```bash
# Write: append to file (O(1))
echo "$key,$value" >> database

# Read: scan entire file (O(n))
grep "^$key," database | tail -n 1
```

This has excellent write performance (just append) but terrible read performance (scan entire file).

**Indexes** exist to solve this problem. They're additional data structures that speed up reads at the cost of slowing down writes.

> "This is an important trade-off in storage systems: well-chosen indexes speed up read queries, but every index slows down writes."

---

## Storage Engine Families

There are two major families of storage engines:

| Family | Examples | Optimized For | Structure |
|--------|----------|---------------|-----------|
| **Log-structured** | LSM-trees, Bitcask, LevelDB, RocksDB, Cassandra | Writes | Append-only logs, compaction |
| **Page-oriented** | B-trees, PostgreSQL, MySQL InnoDB | Reads | Fixed-size pages, in-place updates |

---

## Hash Indexes

The simplest indexing strategy for key-value data:

1. Store data in an append-only file
2. Keep an in-memory hash map: key → byte offset in file

**How it works:**
- Write: Append to file, update hash map with new offset
- Read: Look up offset in hash map, seek to that position

**Strengths:**
- Very fast reads (O(1) lookup + one disk seek)
- Very fast writes (append-only)
- Simple to implement

**Limitations:**
- Hash map must fit in memory
- Range queries are not efficient
- Cannot scan keys in order

**Compaction:**
To prevent the file from growing forever, segments are periodically compacted (removing duplicate keys, keeping only most recent value) and merged.

**Use case:** High write throughput with limited key space (e.g., URL to view count).

---

## SSTables and LSM-Trees

**SSTable (Sorted String Table):** Like the append-only log, but with key-value pairs sorted by key within each segment.

### Advantages of Sorted Segments

1. **Efficient merging:** Merge-sort algorithm, simple and efficient even for large files
2. **Sparse index:** No need to index every key—know offset of surrounding keys and scan
3. **Compression:** Group and compress blocks of records

### LSM-Tree Structure

**LSM (Log-Structured Merge) Tree** algorithm:

1. **Memtable:** Writes go to in-memory balanced tree (red-black, AVL)
2. **Flush:** When memtable exceeds threshold (~MB), write to disk as SSTable
3. **Compaction:** Background process merges SSTables, discards old values
4. **Read path:** Check memtable → recent segments → older segments

**Durability:** Separate write-ahead log captures writes before memtable (restored on crash).

### Compaction Strategies

| Strategy | How It Works | Trade-offs |
|----------|--------------|------------|
| **Size-tiered** | Merge smaller SSTables into larger ones | Higher space amplification |
| **Leveled** | Key ranges split into levels, incremental merging | Lower space usage, more I/O |

### LSM-Tree Characteristics

**Strengths:**
- High write throughput (sequential writes)
- Efficient use of disk bandwidth
- Better compression (no fragmentation)
- Works well even when dataset >> memory

**Weaknesses:**
- Compaction can interfere with reads/writes
- Higher read latency (check multiple SSTables)
- Space amplification during compaction
- Key may exist in multiple places (complicates locking)

**Used by:** LevelDB, RocksDB, Cassandra, HBase, Lucene

---

## B-Trees

The most widely used indexing structure, standard in almost all relational databases.

### Structure

- Database broken into fixed-size **pages** (typically 4KB)
- Pages reference other pages (tree structure)
- **Leaf pages** contain values or references to values
- **Internal pages** contain keys and child page references

### Key Properties

- **Balanced:** All leaf pages at same depth
- **Branching factor:** Number of child references per page (typically hundreds)
- **Depth:** O(log n) — a 4-level tree with branching factor 500 can store 256TB

### Operations

**Lookup:**
1. Start at root page
2. Binary search for key range containing target
3. Follow reference to child page
4. Repeat until leaf page

**Insert:**
1. Find leaf page that should contain key
2. If space available, add key to page
3. If full, split page into two, update parent

**Update:**
1. Find leaf page containing key
2. Modify value in place
3. Write page back to disk

### Reliability Mechanisms

**Write-Ahead Log (WAL):**
- Every modification written to append-only log first
- WAL replayed on crash to restore consistent state

**Latches:**
- Lightweight locks protecting tree during concurrent access
- Necessary because in-place updates could leave tree inconsistent

### B-Tree Optimizations

| Optimization | Description |
|--------------|-------------|
| Copy-on-write | Write modified pages to new location (LMDB) |
| Key abbreviation | Internal pages only need boundary info |
| Sequential leaf layout | Keep adjacent keys physically close |
| Sibling pointers | Leaf pages point to neighbors for range scans |
| Fractal trees | Borrow LSM ideas to reduce seeks |

---

## B-Trees vs LSM-Trees

### Write Performance

| Aspect | B-tree | LSM-tree |
|--------|--------|----------|
| **Write pattern** | Random (in-place update) | Sequential (append) |
| **Write amplification** | ~2x (WAL + page) | Varies (compaction) |
| **Throughput** | Lower | Higher |

LSM-trees typically have higher write throughput due to sequential writes.

### Read Performance

| Aspect | B-tree | LSM-tree |
|--------|--------|----------|
| **Read pattern** | Predictable path | Multiple SSTables to check |
| **Latency variance** | Low | Higher (compaction interference) |
| **Point lookups** | Faster | Slower |

B-trees have more predictable read latency; LSM-trees can spike during compaction.

### Space Efficiency

| Aspect | B-tree | LSM-tree |
|--------|--------|----------|
| **Fragmentation** | Higher (page splits) | Lower (compaction removes) |
| **Compression** | Harder | Easier |
| **Disk usage** | More | Less |

LSM-trees generally use disk more efficiently.

### When to Choose Each

**Choose B-trees when:**
- Read-heavy workload
- Need predictable latency
- Strong transactional semantics (locks on key ranges)
- Proven, mature implementation needed

**Choose LSM-trees when:**
- Write-heavy workload
- High write throughput needed
- Disk space is constrained
- Range queries over sorted data are common

---

## In-Memory Databases

With RAM prices falling, many datasets fit entirely in memory.

### Examples
- **Caching only:** Memcached (data loss acceptable on restart)
- **Durable:** VoltDB, MemSQL (WAL + periodic snapshots)
- **Hybrid:** Redis (async persistence)

### Performance Characteristics

Counterintuitively, the main performance benefit is **not** avoiding disk reads:
- OS filesystem cache means disk-based DBs often serve from memory too
- Real benefit: avoiding overhead of encoding data for disk format

### In-Memory Advantages

- Simpler data structures possible
- Can implement types hard on disk (Redis: queues, sets)
- Lower latency for complex operations

### In-Memory Limitations

- Dataset limited by RAM (or cluster RAM)
- Durability requires careful design
- More expensive per GB than disk

---

## OLTP vs OLAP Storage

### Access Pattern Differences

| Aspect | OLTP | OLAP |
|--------|------|------|
| **Read pattern** | Small number of records by key | Aggregate over many records |
| **Write pattern** | Random, low-latency | Bulk load (ETL) |
| **Data focus** | Current state | Historical trends |
| **Dataset size** | GB to TB | TB to PB |
| **Users** | End users, applications | Analysts |

### Why Separate Systems?

Running analytics on OLTP databases:
- Expensive queries harm transactional performance
- Different indexes needed
- Different storage formats optimal

**Data warehouses** solve this: separate read-only copy optimized for analytics.

---

## Column-Oriented Storage

Traditional row-oriented storage: all values from one row stored together.

**Column-oriented storage:** All values from each column stored together.

### Why Columns?

Analytic queries typically:
- Scan millions/billions of rows
- Use only a few columns per query
- Aggregate values

Row storage wastes bandwidth loading unused columns.

### Example Query

```sql
SELECT date.weekday, product.category, SUM(quantity)
FROM fact_sales
JOIN dim_date ON ...
JOIN dim_product ON ...
WHERE date.year = 2023
  AND product.category IN ('Fruit', 'Candy')
GROUP BY date.weekday, product.category;
```

This only needs 3 columns from fact_sales, but row storage loads all 100+.

### Column Compression

Columns often have repeated values → excellent compression:

**Bitmap encoding:**
- N distinct values → N bitmaps
- Each bitmap: 1 bit per row (is this value present?)
- Sparse bitmaps: run-length encoding

**Bitwise operations:**
```sql
WHERE product_sk IN (30, 68, 69)
-- OR the three bitmaps

WHERE product_sk = 31 AND store_sk = 3
-- AND two bitmaps
```

### Vectorized Processing

Column data enables CPU-efficient processing:
- Load column chunk into L1 cache
- Tight loops with no function calls
- SIMD instructions for parallel processing

### Column Storage in Practice

| System | Column-Oriented? |
|--------|------------------|
| PostgreSQL | Row-oriented (but has columnar extensions) |
| Vertica, Redshift | Column-oriented |
| Cassandra, HBase | Row-oriented (despite "column families" name) |
| Parquet, ORC | Column-oriented file formats |

---

## Star and Snowflake Schemas

Common data warehouse schema patterns:

### Star Schema

- **Fact table:** Central table with events (sales, clicks, etc.)
- **Dimension tables:** Who, what, where, when, why, how

```
           dim_date
              |
dim_store -- fact_sales -- dim_product
              |
          dim_customer
```

Fact tables can have 100+ columns, billions of rows.

### Snowflake Schema

Dimensions further normalized into sub-dimensions:
- dim_product → dim_brand, dim_category
- More normalized, but harder for analysts to query

Star schemas generally preferred for simplicity.

---

## PostgreSQL Storage Internals

PostgreSQL uses a page-oriented storage engine with these characteristics:

### Heap Tables

- Data stored in 8KB pages
- Rows stored in insertion order (no clustering by default)
- Dead tuples from updates/deletes remain until VACUUM

### TOAST (The Oversized-Attribute Storage Technique)

Large values (>2KB) stored separately:
- Compressed
- Stored in separate TOAST table
- Transparently fetched when needed

**Implication:** Large columns are expensive to fetch; avoid SELECT *.

### MVCC Storage

Multi-Version Concurrency Control means:
- Updates create new row versions
- Old versions kept for concurrent transactions
- VACUUM reclaims dead tuples

**Bloat:** Without regular VACUUM, tables grow with dead tuples.

### Index Types in PostgreSQL

| Type | Structure | Use Case |
|------|-----------|----------|
| **B-tree** | Balanced tree | Default, most queries |
| **Hash** | Hash table | Equality only |
| **GiST** | Generalized search tree | Geometric, full-text |
| **GIN** | Generalized inverted | Arrays, JSONB, full-text |
| **BRIN** | Block range | Large tables, sorted data |

---

## Choosing Storage Strategy

### Questions to Ask

1. **Read/write ratio?**
   - Read-heavy → B-tree, traditional RDBMS
   - Write-heavy → LSM-tree, consider NoSQL

2. **Data size vs memory?**
   - Fits in memory → Many options
   - Much larger than memory → Need efficient disk access

3. **Query patterns?**
   - Point lookups → Hash index, B-tree
   - Range scans → B-tree, LSM-tree
   - Aggregations → Column store

4. **Consistency requirements?**
   - Strong ACID → Traditional RDBMS
   - Eventual consistency OK → More options

5. **OLTP or OLAP?**
   - OLTP → Row-oriented
   - OLAP → Column-oriented

### PostgreSQL Defaults

For most applications, PostgreSQL's defaults work well:
- B-tree indexes for most queries
- Row-oriented heap storage
- MVCC for concurrency

Consider extensions (TimescaleDB, Citus) for specialized needs.

---

## Common Mistakes

| Mistake | Why It's Wrong | Better Approach |
|---------|----------------|-----------------|
| Ignoring storage engine choice | Wrong engine = wrong trade-offs | Understand your workload |
| Over-indexing | Every index slows writes | Index only what you query |
| Running analytics on OLTP | Harms transactional performance | Use read replica or warehouse |
| SELECT * on TOAST columns | Fetches large external values | Select only needed columns |
| Ignoring VACUUM | Table bloat, degraded performance | Monitor and tune autovacuum |

---

## Key Takeaways

1. **Two families:** Log-structured (LSM) vs page-oriented (B-tree) with different trade-offs.

2. **Indexes trade write for read performance.** Every index slows writes.

3. **LSM-trees excel at writes;** sequential I/O, good compression.

4. **B-trees excel at reads;** predictable latency, mature implementations.

5. **Column storage enables analytics** by reading only needed columns.

6. **OLTP and OLAP need different storage** optimizations.

7. **PostgreSQL uses B-trees and row storage** by default, well-suited for OLTP.

8. **Understand your workload** before choosing storage strategy.

---

## References

- Kleppmann, M. *Designing Data-Intensive Applications*, Chapter 3
- Dombrovskaya, H. et al. *PostgreSQL Query Optimization*, Chapters 2-3
- PostgreSQL Documentation: Storage and TOAST
