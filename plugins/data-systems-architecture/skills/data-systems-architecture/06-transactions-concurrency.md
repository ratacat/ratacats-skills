# Transactions and Concurrency

## Overview

Transactions are the fundamental mechanism for handling concurrent access to shared data. They provide guarantees about what happens when multiple operations execute simultaneously and when things go wrong.

**Core insight:** Concurrency bugs are among the hardest to detect because they're non-deterministic. Transactions provide a safety net, but only if you understand what guarantees your isolation level actually provides.

---

## ACID Properties

The classic transaction guarantees:

| Property | Meaning | What It Prevents |
|----------|---------|------------------|
| **Atomicity** | All or nothing | Partial failures |
| **Consistency** | Valid state to valid state | Constraint violations |
| **Isolation** | Transactions don't interfere | Concurrency anomalies |
| **Durability** | Committed data persists | Data loss |

### Atomicity

If a transaction fails partway through, all changes are rolled back. You never see partial results.

**Example:**
```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
-- If this fails, the debit from account 1 is also rolled back
COMMIT;
```

### Consistency

The database moves from one valid state to another. Constraints are enforced.

**Note:** Consistency depends on both database constraints AND application logic. The database can only enforce what you tell it to enforce.

### Isolation

Concurrent transactions don't affect each other's execution. The isolation level determines exactly what guarantees are provided.

### Durability

Once a transaction commits, its changes persist even if the system crashes immediately after.

**Implementation:** Write-ahead log (WAL) — changes written to durable log before commit confirmed.

---

## Isolation Levels

Isolation levels trade off safety for performance. Weaker isolation allows more concurrency but permits more anomalies.

### Read Uncommitted

**Guarantee:** Almost none.
**Allows:** Dirty reads (seeing uncommitted changes).
**Use case:** Rarely used; only for specific read-heavy scenarios where stale data is acceptable.

### Read Committed

**Guarantee:** You only see committed data.
**Prevents:** Dirty reads.
**Allows:** Non-repeatable reads, phantom reads.

**Implementation:** Locks held only during read/write, not entire transaction.

**PostgreSQL default:** Yes, this is the default level.

### Repeatable Read (Snapshot Isolation)

**Guarantee:** You see a consistent snapshot from transaction start.
**Prevents:** Dirty reads, non-repeatable reads.
**Allows:** Phantoms (in standard definition); PostgreSQL prevents most phantoms.

**Implementation:** MVCC — each transaction sees data as it existed at transaction start.

**Naming confusion:** PostgreSQL and MySQL call their snapshot isolation "repeatable read." Oracle calls it "serializable." The SQL standard definition is different. **Nobody agrees on what repeatable read means.**

### Serializable

**Guarantee:** Transactions execute as if run one at a time.
**Prevents:** All anomalies.
**Cost:** Highest overhead; may abort more transactions.

---

## Concurrency Anomalies

### Dirty Read

Reading data written by an uncommitted transaction.

```
T1: UPDATE balance = 500  (not committed)
T2: SELECT balance → 500  (dirty read!)
T1: ROLLBACK
T2: Now has wrong data
```

**Prevented by:** Read Committed and above.

### Non-Repeatable Read

Reading the same row twice yields different results because another transaction modified it.

```
T1: SELECT balance → 1000
T2: UPDATE balance = 500; COMMIT
T1: SELECT balance → 500  (different!)
```

**Prevented by:** Repeatable Read and above.

### Phantom Read

A query returns different rows because another transaction inserted/deleted.

```
T1: SELECT count(*) WHERE dept = 'A' → 5
T2: INSERT INTO employees (dept = 'A'); COMMIT
T1: SELECT count(*) WHERE dept = 'A' → 6  (phantom!)
```

**Prevented by:** Serializable (fully); Repeatable Read (partially in PostgreSQL).

### Lost Update

Two transactions read-modify-write, and one overwrites the other.

```
T1: SELECT balance → 100
T2: SELECT balance → 100
T1: UPDATE balance = 100 + 10 → 110
T2: UPDATE balance = 100 + 20 → 120
-- T1's update is lost!
```

**Result:** Balance should be 130, but it's 120.

### Write Skew

Two transactions read overlapping data, then make decisions based on stale reads.

**Example:** Two doctors checking if they can go off-call:
```
-- Both check: 2 doctors on call
Alice: SELECT count(*) WHERE on_call = true → 2
Bob:   SELECT count(*) WHERE on_call = true → 2

-- Both decide it's safe
Alice: UPDATE SET on_call = false WHERE name = 'Alice'
Bob:   UPDATE SET on_call = false WHERE name = 'Bob'

-- Result: 0 doctors on call!
```

**Prevented by:** Serializable isolation only.

---

## Multi-Version Concurrency Control (MVCC)

PostgreSQL uses MVCC to implement snapshot isolation.

### How It Works

1. Each row has creation and deletion transaction IDs
2. Updates create new row versions (not in-place modification)
3. Transactions see rows based on visibility rules
4. Old versions garbage collected by VACUUM

### Visibility Rules

A row is visible to a transaction if:
1. The creating transaction committed before the reader's snapshot
2. The row is not deleted, OR the deleting transaction hadn't committed when reader's snapshot was taken

### Consequences

**Dead tuples:** Updated/deleted rows remain until VACUUM removes them.

**Table bloat:** Without regular VACUUM, tables grow with dead tuples.

**Long transactions:** Hold back VACUUM, increase bloat.

```sql
-- Check for long-running transactions
SELECT pid, age(clock_timestamp(), xact_start), query
FROM pg_stat_activity
WHERE state = 'active'
ORDER BY xact_start;
```

---

## Preventing Lost Updates

Several strategies to prevent the read-modify-write problem:

### 1. Atomic Operations (Best)

Let the database do the modification atomically.

```sql
-- Instead of: SELECT → modify in app → UPDATE
UPDATE counters SET value = value + 1 WHERE id = 1;

UPDATE accounts SET balance = balance - 100 WHERE id = 1;

UPDATE products SET stock = stock - 1
WHERE id = 42 AND stock > 0;  -- With check
```

### 2. Explicit Locking (SELECT FOR UPDATE)

Lock the rows before modifying.

```sql
BEGIN;
SELECT * FROM accounts WHERE id = 1 FOR UPDATE;
-- Row is now locked; other transactions must wait
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
COMMIT;
```

**Lock modes:**
- `FOR UPDATE`: Exclusive lock (blocks other FOR UPDATE)
- `FOR SHARE`: Shared lock (allows other FOR SHARE)
- `FOR NO KEY UPDATE`: Like FOR UPDATE, but allows foreign key checks
- `NOWAIT`: Error immediately if can't acquire lock
- `SKIP LOCKED`: Skip locked rows (for queue-like patterns)

### 3. Compare-and-Set

Check that value hasn't changed before updating.

```sql
UPDATE wiki_pages
SET content = 'new content', version = version + 1
WHERE id = 1 AND version = 5;  -- Expected version

-- Check rows affected
-- If 0, someone else modified it
```

### 4. Automatic Detection

PostgreSQL's Repeatable Read detects some lost updates and aborts the conflicting transaction.

```sql
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
-- If another transaction modified the same row,
-- this transaction will be aborted
```

**Note:** MySQL's Repeatable Read does NOT detect lost updates.

---

## Preventing Write Skew

Write skew is harder to prevent because it involves multiple rows.

### Use Serializable Isolation

```sql
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
BEGIN;
SELECT count(*) FROM doctors WHERE on_call = true;
-- Decision made based on this count
UPDATE doctors SET on_call = false WHERE name = 'Alice';
COMMIT;
```

PostgreSQL's Serializable Snapshot Isolation (SSI) will abort one transaction if write skew would occur.

### Use FOR UPDATE on Read Rows

Lock the rows your decision depends on:

```sql
BEGIN;
SELECT * FROM doctors WHERE on_call = true FOR UPDATE;
-- Now locked; can safely check count and update
UPDATE doctors SET on_call = false WHERE name = 'Alice';
COMMIT;
```

### Use Constraints

Where possible, use database constraints:

```sql
-- Unique constraint prevents double-booking usernames
CREATE UNIQUE INDEX ON users (username);

-- Exclusion constraint prevents overlapping bookings
CREATE TABLE reservations (
    room_id INT,
    during TSTZRANGE,
    EXCLUDE USING GIST (room_id WITH =, during WITH &&)
);
```

---

## Locking Strategies

### Row-Level Locking

PostgreSQL uses row-level locking, not table-level.

```sql
-- Only locks the specific rows
SELECT * FROM accounts WHERE id = 1 FOR UPDATE;
```

### Advisory Locks

Application-level locks for custom scenarios:

```sql
-- Obtain lock (blocks if already held)
SELECT pg_advisory_lock(12345);

-- Do work...

-- Release lock
SELECT pg_advisory_unlock(12345);
```

Useful for:
- Coordinating between multiple processes
- Preventing duplicate cron job execution
- Custom locking schemes

### Deadlock Detection

PostgreSQL automatically detects deadlocks and aborts one transaction.

```
T1: Lock row A
T2: Lock row B
T1: Try to lock row B → waits for T2
T2: Try to lock row A → waits for T1
-- Deadlock detected! One transaction aborted.
```

**Prevention:**
- Always lock rows in consistent order
- Use short transactions
- Use `NOWAIT` to fail fast

---

## PostgreSQL Isolation Levels

### Read Committed (Default)

```sql
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
-- or just BEGIN; (default)
```

**Behavior:**
- Each statement sees a new snapshot
- No dirty reads
- Non-repeatable reads possible
- Lost updates NOT automatically detected

### Repeatable Read (Snapshot Isolation)

```sql
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
```

**Behavior:**
- Transaction sees snapshot from its start
- No dirty or non-repeatable reads
- Some lost updates detected and aborted
- Write skew NOT prevented

### Serializable (SSI)

```sql
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
```

**Behavior:**
- Full serializability
- Write skew detected and prevented
- May abort more transactions (must retry)
- Best for correctness

---

## Transaction Patterns

### Short Transactions

Keep transactions as short as possible:

```sql
-- BAD: Long transaction
BEGIN;
SELECT * FROM orders WHERE status = 'pending';
-- ... application processing for 30 seconds ...
UPDATE orders SET status = 'processed' WHERE id = 123;
COMMIT;

-- GOOD: Short transaction
-- Do processing outside transaction
BEGIN;
UPDATE orders SET status = 'processed' WHERE id = 123;
COMMIT;
```

### Savepoints

Partial rollback within a transaction:

```sql
BEGIN;
INSERT INTO orders (id, amount) VALUES (1, 100);

SAVEPOINT before_items;
INSERT INTO order_items (order_id, product_id) VALUES (1, 999);
-- Oops, product 999 doesn't exist
ROLLBACK TO before_items;

-- Continue with valid data
INSERT INTO order_items (order_id, product_id) VALUES (1, 123);
COMMIT;
```

### Retry Logic

Handle serialization failures:

```python
def execute_with_retry(conn, fn, max_retries=3):
    for attempt in range(max_retries):
        try:
            with conn.cursor() as cur:
                result = fn(cur)
                conn.commit()
                return result
        except psycopg2.errors.SerializationFailure:
            conn.rollback()
            if attempt == max_retries - 1:
                raise
            time.sleep(random.uniform(0.01, 0.1))
```

---

## Queue Pattern with SELECT FOR UPDATE SKIP LOCKED

Process items from a queue without conflicts:

```sql
-- Worker gets next unprocessed item
BEGIN;
SELECT id, data FROM tasks
WHERE status = 'pending'
ORDER BY created_at
LIMIT 1
FOR UPDATE SKIP LOCKED;

-- Process the task...

UPDATE tasks SET status = 'complete' WHERE id = :id;
COMMIT;
```

Multiple workers can process different items concurrently without blocking.

---

## Common Mistakes

| Mistake | Why It's Wrong | Better Approach |
|---------|----------------|-----------------|
| Assuming Read Committed prevents all issues | Non-repeatable reads and lost updates still possible | Use appropriate isolation level or locking |
| Long transactions | Hold locks, block VACUUM, cause contention | Keep transactions short |
| Missing retry logic | Serialization failures are expected | Always handle and retry |
| Using ORM without understanding SQL | May generate unsafe patterns | Understand the SQL being executed |
| Ignoring deadlocks | Application hangs | Lock in consistent order, handle errors |
| Not using FOR UPDATE | Lost updates in read-modify-write | Lock rows before modification |

---

## Performance Considerations

### Isolation Level Trade-offs

| Level | Correctness | Throughput | Abort Rate |
|-------|-------------|------------|------------|
| Read Committed | Lowest | Highest | Lowest |
| Repeatable Read | Medium | Medium | Low |
| Serializable | Highest | Lower | Higher |

### When to Use Each Level

**Read Committed:**
- High-throughput scenarios
- When application handles consistency
- Read-only analytics

**Repeatable Read:**
- Reports that need consistent snapshots
- When you need to read same data multiple times

**Serializable:**
- Financial transactions
- Inventory management
- Any place write skew would be catastrophic

---

## Key Takeaways

1. **ACID provides guarantees**, but isolation levels trade off safety for performance.

2. **Read Committed is the default** but allows non-repeatable reads and lost updates.

3. **Repeatable Read provides snapshot isolation** but doesn't prevent write skew.

4. **Serializable is safest** but has higher abort rates; must retry.

5. **Use atomic operations** for read-modify-write when possible.

6. **Use FOR UPDATE** to lock rows when you need to read-then-write.

7. **Keep transactions short** to reduce contention and bloat.

8. **Handle retries** for serialization failures.

9. **Understand what your isolation level actually guarantees** — names are inconsistent across databases.

---

## References

- Kleppmann, M. *Designing Data-Intensive Applications*, Chapter 7
- PostgreSQL Documentation: Transaction Isolation
- PostgreSQL Documentation: Explicit Locking
