# Data Modeling for Data-Intensive Applications

## Overview

Data modeling is arguably the most important skill for building data-intensive applications. A good data model makes every query easy to write, keeps data clean, and enables the system to evolve gracefully. A poor model creates endless workarounds, performance problems, and maintenance headaches.

**Core insight:** Your data model determines what operations are easy and what are hard. The model should reflect how your application actually uses data, not how you initially imagine it might.

---

## Data Model Fundamentals

### The Layered Nature of Data

Every application works through layers of data abstraction:

1. **Real world:** People, organizations, events, transactions
2. **Application model:** Objects, data structures, APIs
3. **Database model:** Tables, documents, graphs, columns
4. **Storage model:** Bytes on disk, memory structures, indexes
5. **Hardware:** Electrical signals, magnetic fields, light pulses

Each layer hides complexity from the layer above. Your job is to choose the right database model for your application layer's needs.

### Why Data Model Choice Matters

Every data model embodies assumptions about how data will be used:

| Aspect | Impact |
|--------|--------|
| **Query patterns** | Some operations are easy, others impossible |
| **Performance** | Some access patterns are fast, others slow |
| **Evolvability** | Some changes are simple, others require rewrites |
| **Correctness** | Some invariants are enforced, others rely on application code |

**Key question:** What operations does your application need to perform frequently? Model for those operations.

---

## Relational Model

The relational model (SQL) organizes data into **relations** (tables), where each relation is an unordered collection of **tuples** (rows).

### Strengths of Relational Model

| Strength | Explanation |
|----------|-------------|
| **Join support** | Efficiently combine data from multiple tables |
| **Many-to-many relationships** | Natural representation of complex relationships |
| **Data integrity** | Foreign keys, constraints, transactions |
| **Query flexibility** | Ad-hoc queries without changing schema |
| **Optimizer** | Automatic query optimization |

### When to Use Relational Model

- Data has complex relationships (many-to-many)
- Need for strong consistency guarantees
- Query patterns are varied or unknown in advance
- Multiple applications access the same data
- Need for ACID transactions

### The Query Optimizer Advantage

In relational databases, the query optimizer automatically decides:
- Which parts of the query to execute first
- Which indexes to use
- How to join tables

**This is a fundamental advantage:** You don't need to manually specify access paths. Declare what you want, and the database figures out how to get it efficiently.

If you want to query data in new ways, just declare a new index. Queries automatically use the most appropriate indexes without code changes.

---

## Document Model

Document databases store data as self-contained documents (typically JSON or similar).

### Strengths of Document Model

| Strength | Explanation |
|----------|-------------|
| **Schema flexibility** | No predefined schema required |
| **Locality** | Entire document loaded in one query |
| **Natural mapping** | Matches application object structures |
| **One-to-many** | Nested data within parent record |

### When to Use Document Model

- Data is naturally hierarchical (tree structure)
- Documents are self-contained (rarely need joins)
- Schema changes frequently
- One-to-many relationships dominate
- Application objects map naturally to documents

### The Locality Advantage

When you need to display all information about an entity at once (like a user profile), document models win:

```json
{
  "user_id": 251,
  "name": "Jane Smith",
  "positions": [
    {"title": "CTO", "company": "Acme Inc"},
    {"title": "Engineer", "company": "StartupCo"}
  ],
  "education": [
    {"school": "MIT", "degree": "PhD"}
  ]
}
```

One query retrieves everything. In a relational model, this requires joins across multiple tables.

### Document Model Limitations

**Poor join support:** If you need many-to-many relationships, document databases become awkward. You either:
- Denormalize data (creating update complexity)
- Emulate joins in application code (slower, more complex)

**Data interconnection tendency:** Even if your initial model fits documents well, data often becomes more interconnected as features are added.

---

## Graph Model

Graph databases use nodes (entities) and edges (relationships) as their fundamental structures.

### When to Use Graph Model

- Highly connected data
- Relationship traversal is the primary query pattern
- Variable or recursive relationship depth
- Finding paths, shortest routes, patterns

### Examples

- Social networks (who knows whom)
- Fraud detection (connected suspicious transactions)
- Recommendation engines (similar items/users)
- Knowledge graphs

---

## Schema Design: Schema-on-Write vs Schema-on-Read

### Schema-on-Write (Traditional Relational)

The schema is explicit and enforced at write time. All data must conform to the schema.

**Advantages:**
- Data is always consistent with schema
- Errors caught at write time
- Clear documentation of structure
- Optimizer can use schema knowledge

**Disadvantages:**
- Schema changes can be expensive
- Less flexible for heterogeneous data

### Schema-on-Read (Document/NoSQL)

No schema enforcement at write time. Structure is interpreted when data is read.

**Advantages:**
- Flexibility for varied data structures
- Easy to store heterogeneous data
- No migration needed for new fields

**Disadvantages:**
- Application must handle missing/unexpected fields
- No database-level integrity guarantees
- Schema still exists (implicitly in code)

### Practical Guidance

| Situation | Approach |
|-----------|----------|
| All records have similar structure | Schema-on-write |
| Structure varies by record type | Schema-on-read may help |
| Need data integrity guarantees | Schema-on-write |
| Rapid prototyping | Schema-on-read initially |
| Production system | Usually schema-on-write |

---

## Normalization: The Foundation

### What is Normalization?

Normalization means structuring data to eliminate redundancy. The key idea: store each piece of information in exactly one place, and reference it by ID elsewhere.

### Why Normalize?

| Problem | Caused By | Solution |
|---------|-----------|----------|
| **Update anomalies** | Duplicate data updated inconsistently | Store once, reference by ID |
| **Insert anomalies** | Can't add data without related data | Separate independent entities |
| **Delete anomalies** | Deleting one thing removes unrelated data | Separate independent entities |

### Example: Phone Numbers

**Single-table design (denormalized):**
```
account(id, name, home_phone, work_phone, cell_phone)
```

**Two-table design (normalized):**
```
account(id, name)
phone(id, account_id, phone_type, number, is_primary)
```

**Which is better?** It depends on usage:

| Use Case | Better Design |
|----------|---------------|
| Display all phones with fixed labels | Single table |
| Search by any phone number | Two tables |
| Support variable number of phones | Two tables |
| Allow primary phone designation | Two tables |
| Simple CRUD on account | Single table may be simpler |

### The Normalization Debate

Many developers argue endlessly about normalization vs. denormalization. Here's the practical approach:

1. **Start normalized** (typically 3NF)
2. **Measure actual performance**
3. **Denormalize only with measured justification**
4. **Document the trade-off explicitly**

Premature denormalization is a common mistake. Normalize first, then optimize based on real data.

---

## Practical Schema Design Patterns

### IDs vs. Plain Text

**Always use IDs for:**
- Values that might change (city names, company names)
- Values that need consistency (avoid typos)
- Values that need localization
- Values used for joins

```sql
-- BAD: Plain text that might change
SELECT * FROM users WHERE city = 'Greater Seattle Area';

-- GOOD: ID that references canonical value
SELECT * FROM users WHERE region_id = 91;
```

**The advantage:** IDs never need to change. If "Greater Seattle Area" is renamed, you update one row in the regions table, not thousands of user rows.

### One-to-Many Relationships

**Pattern:** Parent table with child table referencing parent ID.

```sql
CREATE TABLE booking (
    booking_id SERIAL PRIMARY KEY,
    account_id INT REFERENCES account(id),
    booking_date DATE
);

CREATE TABLE booking_leg (
    leg_id SERIAL PRIMARY KEY,
    booking_id INT REFERENCES booking(booking_id),
    flight_id INT REFERENCES flight(id),
    leg_num INT
);
```

### Many-to-Many Relationships

**Pattern:** Junction/bridge table connecting two entities.

```sql
CREATE TABLE user_role (
    user_id INT REFERENCES users(id),
    role_id INT REFERENCES roles(id),
    PRIMARY KEY (user_id, role_id)
);
```

### Surrogate Keys vs. Natural Keys

**Surrogate key:** Artificial identifier (auto-increment, UUID)
**Natural key:** Meaningful business identifier (email, SSN, ISBN)

| Aspect | Surrogate | Natural |
|--------|-----------|---------|
| **Stability** | Never changes | May need to change |
| **Size** | Typically small (INT) | Often larger (VARCHAR) |
| **Meaningfulness** | None | Documents business rule |
| **Performance** | Consistent | Varies by key size |

**Recommendation:** Use surrogate keys as primary keys, but add unique constraints on natural keys:

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    -- ...
);
```

---

## Anti-Patterns to Avoid

### Entity-Attribute-Value (EAV)

**The pattern:**
```sql
CREATE TABLE attributes (
    entity_id INT,
    attribute_name VARCHAR(100),
    attribute_value TEXT
);
```

**Why it's problematic:**
- No type safety
- Can't use constraints
- Queries become complex and slow
- Schema is hidden in data

**When it's acceptable:** True arbitrary key-value metadata. Even then, consider PostgreSQL's `jsonb` type instead.

### Multiple Values in One Column

**Bad:**
```sql
-- Comma-separated values in one column
INSERT INTO users (name, skills) VALUES ('Jane', 'python,sql,java');
```

**Problems:**
- Can't index individual values efficiently
- Complex queries to search for single value
- Difficult to maintain data integrity

**Better:** Use a junction table or PostgreSQL arrays with proper indexing.

### Storing Calculated Values Without Strategy

Storing calculated values (denormalization) is fine with a clear strategy for keeping them updated:

- Triggers that update on source change
- Materialized views with refresh schedule
- Documented manual update process

Without a strategy, calculated values become stale and unreliable.

---

## PostgreSQL-Specific Data Modeling

### JSON/JSONB for Semi-Structured Data

PostgreSQL's `jsonb` type offers the best of both worlds:

```sql
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    event_type VARCHAR(50),
    created_at TIMESTAMP,
    metadata JSONB  -- Flexible, queryable, indexable
);

-- Query into JSON
SELECT * FROM events
WHERE metadata->>'user_id' = '123';

-- Index JSON paths
CREATE INDEX idx_events_user ON events ((metadata->>'user_id'));
```

**Use JSONB when:**
- Part of your data varies by record
- You need flexibility but still want to query
- You're integrating with JSON APIs

**Avoid JSONB when:**
- Data structure is well-known and consistent
- You need foreign key constraints on JSON fields
- Heavy analytical queries across JSON fields

### Arrays for Multi-Valued Attributes

```sql
CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    title TEXT,
    tags TEXT[]  -- Array of tags
);

-- Query for articles with specific tag
SELECT * FROM articles WHERE 'postgresql' = ANY(tags);

-- GIN index for array containment
CREATE INDEX idx_articles_tags ON articles USING GIN(tags);
```

### Range Types for Temporal Data

```sql
CREATE TABLE room_bookings (
    room_id INT,
    during TSTZRANGE,  -- Timestamp range with timezone
    EXCLUDE USING GIST (room_id WITH =, during WITH &&)  -- Prevent overlaps
);

-- Query for active bookings
SELECT * FROM room_bookings
WHERE during @> NOW();
```

---

## Design for Performance

### Query-Driven Design

**Critical principle:** Design your schema based on how you'll query it.

Before finalizing any table structure, write out the most important queries your application will execute. Then design the schema to make those queries efficient.

**Example process:**

1. List top 10 most frequent queries
2. List queries with strictest latency requirements
3. Design schema to support those queries
4. Verify with EXPLAIN ANALYZE
5. Adjust based on actual execution plans

### The Phone Number Example Revisited

From PostgreSQL Query Optimization:

> "Which of the two designs is the right one? It depends on the intended usage of the data."

| Query Pattern | Optimal Design |
|---------------|----------------|
| Display phones as labeled fields | Single table |
| Search by any phone number | Multi-table |
| Support variable phone count | Multi-table |
| Designate primary phone | Multi-table |

**The lesson:** There is no universally correct design. Design follows use case.

### Indexing Considerations at Design Time

While full indexing strategy is covered elsewhere, consider at design time:

- Which columns will be in WHERE clauses?
- What are your JOIN columns?
- Will you search within text fields?
- Are there range queries (dates, numbers)?

Design your types accordingly (e.g., use `TIMESTAMP WITH TIME ZONE` if you'll do range queries on time).

---

## When to Denormalize

### Valid Reasons to Denormalize

1. **Measured performance problem** with normalized design
2. **Read-heavy workload** where join cost matters
3. **Reporting/analytics** that aggregate across tables
4. **Caching** calculated values for expensive computations

### Denormalization Strategies

**Materialized Views:**
```sql
CREATE MATERIALIZED VIEW order_summary AS
SELECT
    customer_id,
    COUNT(*) as order_count,
    SUM(total) as total_spent
FROM orders
GROUP BY customer_id;

-- Refresh periodically
REFRESH MATERIALIZED VIEW order_summary;
```

**Pre-aggregated columns with triggers:**
```sql
-- Add to parent table
ALTER TABLE customers ADD COLUMN order_count INT DEFAULT 0;

-- Trigger to maintain count
CREATE TRIGGER update_order_count
AFTER INSERT OR DELETE ON orders
FOR EACH ROW EXECUTE FUNCTION maintain_order_count();
```

**Caching tables for analytics:**
Separate denormalized tables optimized for reporting, updated on schedule.

### The Denormalization Contract

When you denormalize, you must:

1. Document what invariant you're maintaining
2. Implement mechanism to keep it consistent
3. Handle failure scenarios (what if update fails?)
4. Monitor for drift between source and cache

---

## Evolving Your Schema

### Schema Changes in Production

Database schemas must evolve. Plan for it:

**Safe changes:**
- Adding nullable columns
- Adding tables
- Adding indexes (with `CONCURRENTLY`)
- Adding constraints with validation

**Risky changes:**
- Dropping columns (break queries)
- Changing column types
- Renaming columns/tables
- Adding NOT NULL to existing columns

### Migration Strategy

1. **Expand:** Add new structure alongside old
2. **Migrate:** Copy/transform data to new structure
3. **Verify:** Confirm new structure works
4. **Contract:** Remove old structure

This allows rollback at each step.

---

## Common Mistakes

| Mistake | Why It's Wrong | Better Approach |
|---------|----------------|-----------------|
| Modeling for flexibility over clarity | Vague models create query complexity | Model actual use cases |
| Denormalizing without measurement | May not improve performance, increases complexity | Measure first |
| Using EAV for "flexibility" | Hides schema, prevents optimization | Use proper types or JSONB |
| Ignoring query patterns | Schema doesn't support actual queries | Write queries first |
| Over-normalizing for purity | Excessive joins hurt performance | Pragmatic normalization |
| Storing derived data without update strategy | Data becomes inconsistent | Document update mechanism |

---

## Key Takeaways

1. **Data model choice is fundamental.** It determines what operations are easy and what are hard.

2. **Match model to access patterns.** Relational for joins and complex relationships, document for hierarchical data, graph for connected data.

3. **Start normalized.** Denormalize only with measured justification.

4. **Design for your queries.** Write the important queries first, then design the schema.

5. **Use IDs for references.** Store human-readable values once, reference by ID elsewhere.

6. **PostgreSQL offers flexibility.** JSONB, arrays, and range types let you mix paradigms.

7. **Plan for evolution.** Schemas change; design for safe migration.

8. **There is no perfect design.** Only trade-offs appropriate to your use case.

---

## References

- Kleppmann, M. *Designing Data-Intensive Applications*, Chapter 2
- Dombrovskaya, H. et al. *PostgreSQL Query Optimization*, Chapter 1, 9
- Fontaine, D. *The Art of PostgreSQL*, Part VI: Data Modeling
