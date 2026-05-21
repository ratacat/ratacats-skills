# Foundational Principles of Data Systems Architecture

## Overview

This chapter establishes the core concepts that underpin all data system architecture decisions. Before diving into specific technologies or optimization techniques, you must understand the fundamental trade-offs that shape every data-intensive application.

**Key insight:** There is no "best" database design, only trade-offs. Every architectural choice involves sacrificing something to gain something else. Understanding these trade-offs is the foundation of good data systems thinking.

---

## The Three Pillars: Reliability, Scalability, Maintainability

Every data system must balance three fundamental concerns. These are not features to add later—they are architectural properties that must be designed in from the start.

### Reliability

**Definition:** The system continues to work correctly (performing the correct function at the desired level of performance) even in the face of adversity—hardware faults, software errors, and human mistakes.

Reliability means more than just "it works." A reliable system:

- Performs the function the user expected
- Tolerates the user making mistakes or using the software in unexpected ways
- Maintains good performance under expected load and data volume
- Prevents unauthorized access and abuse

**The distinction between faults and failures is critical:**

| Term | Definition | Example |
|------|------------|---------|
| **Fault** | One component deviating from its spec | A disk sector becomes unreadable |
| **Failure** | The system as a whole stops providing service | Users cannot access the application |

The goal is not to prevent all faults (impossible), but to design fault-tolerance mechanisms that prevent faults from causing failures. You build reliable systems from unreliable parts.

#### Types of Faults

**Hardware Faults**
- Hard disk crash (MTTF: 10-50 years; with 10,000 disks, expect one failure per day)
- RAM errors
- Power grid blackouts
- Network cable disconnections

Traditional response: Add redundancy (RAID, dual power supplies, diesel generators). Modern approach: Design software to tolerate entire machine loss through redundancy at the system level.

**Software Errors**
Unlike hardware faults (which are random and independent), software bugs are systematic and correlated—they can take down many nodes simultaneously.

Common patterns:
- Bugs triggered by unusual inputs (leap second bugs, etc.)
- Runaway processes consuming shared resources
- Cascading failures where one component's failure triggers others
- Services slowing down and becoming unresponsive

Software faults often lie dormant until triggered by unusual circumstances. They exploit assumptions about the environment that stop being true.

**Human Errors**
Configuration errors by operators are the leading cause of outages—hardware plays a role in only 10-25% of failures.

Mitigation strategies:
1. Design interfaces that make "the right thing" easy and "the wrong thing" hard
2. Provide sandbox environments for safe experimentation with real data
3. Test thoroughly at all levels (unit, integration, manual)
4. Enable quick rollback of configuration changes
5. Implement detailed monitoring and alerting
6. Roll out changes gradually (canary deployments)

### Scalability

**Definition:** The ability to cope with increased load gracefully. Scalability is not a binary property—you cannot say "X is scalable" without context. Instead, ask: "If load grows in a particular way, what are our options for coping?"

#### Describing Load

Before discussing scalability, you must describe current load using **load parameters**. The best choice of parameters depends on your system architecture:

- Requests per second to a web server
- Ratio of reads to writes in a database
- Number of simultaneously active users
- Hit rate on a cache
- Size of working data set relative to memory

**Example: Twitter's Load Parameters (2012)**

| Operation | Volume |
|-----------|--------|
| Post tweet | 4.6k requests/sec average, 12k peak |
| Home timeline reads | 300k requests/sec |

The scaling challenge wasn't tweet volume—it was **fan-out**. Each user follows many people and is followed by many. Some users have 30 million followers. A single tweet can require 30 million writes to home timeline caches.

**Load distribution matters:** The average follower count hides that some users have orders of magnitude more followers than others. Your architecture must handle the outliers, not just the average.

#### Describing Performance

Once you've described load, investigate what happens when it increases:

1. If load increases with fixed resources, how does performance degrade?
2. To maintain performance under increased load, how many resources must you add?

**Key metrics differ by system type:**

| System Type | Primary Metric | Why |
|-------------|----------------|-----|
| Batch processing | Throughput | Records/second or total job time |
| Online systems | Response time | Time between request and response |

**Response Time vs. Latency:**
- **Response time:** What the client sees (service time + network delays + queueing delays)
- **Latency:** Duration a request waits before being handled (the "waiting" portion)

**Use percentiles, not averages:**

Averages hide the distribution of actual user experience. A service with 200ms average response time might have 5% of users waiting 1.5+ seconds.

| Percentile | Meaning | Use Case |
|------------|---------|----------|
| p50 (median) | Half of requests are faster | Typical user experience |
| p95 | 95% of requests are faster | Outlier threshold |
| p99 | 99% of requests are faster | Worst-case monitoring |
| p999 | 99.9% of requests are faster | SLA compliance |

**Why high percentiles matter:** Your slowest customers are often your most valuable—they have the most data because they're power users. Amazon observed that 100ms latency increase reduces sales by 1%.

**Tail latency amplification:** If a request requires multiple backend calls, the probability of experiencing slow response increases. With 5 parallel calls each having 1% chance of being slow, you have ~5% chance of the overall request being slow.

#### Approaches for Coping with Load

| Approach | Description | Trade-offs |
|----------|-------------|------------|
| **Scaling up (vertical)** | Move to more powerful machine | Simpler; limited by available hardware |
| **Scaling out (horizontal)** | Distribute across multiple machines | Complex; enables massive scale |
| **Elastic scaling** | Automatically add resources on load increase | Requires sophisticated automation |
| **Manual scaling** | Human decides when to add resources | Simpler; fewer surprises |

**Stateless vs. stateful scaling:**
- Stateless services: Straightforward to distribute
- Stateful data systems: Introduces significant complexity; traditionally kept on single node until forced to distribute

**There is no generic scalable architecture.** The architecture for 100,000 requests/second of 1KB each looks completely different from 3 requests/minute of 2GB each—even though throughput is identical.

### Maintainability

**Definition:** The ease with which the system can be operated, understood, and modified over time.

Most software cost is in ongoing maintenance, not initial development. Maintainability has three components:

**Operability (Making Life Easy for Operations)**

Operations teams must:
- Monitor system health and restore service quickly
- Track down causes of problems
- Keep software and platforms up to date
- Anticipate and prevent future problems
- Maintain security as configuration changes

Good operability means:
- Visibility into runtime behavior with good monitoring
- Support for automation and integration with standard tools
- No dependency on individual machines (allow maintenance without downtime)
- Good documentation and predictable behavior
- Sensible defaults with override capability

**Simplicity (Managing Complexity)**

Complexity symptoms:
- Explosion of state space
- Tight coupling between modules
- Tangled dependencies
- Inconsistent naming and terminology
- Hacks for performance problems
- Special-casing to work around issues

Complexity increases bug risk—hidden assumptions and unexpected interactions are easily overlooked in complex systems.

**The antidote is abstraction.** Good abstractions hide implementation details behind clean facades. SQL is an abstraction over disk structures, memory management, and concurrent access. High-level languages abstract over machine code.

**Evolvability (Making Change Easy)**

Requirements constantly change: new use cases, business priorities, user requests, regulatory requirements, and growth patterns.

Design for change through:
- Agile practices (TDD, refactoring)
- Good abstractions that isolate change
- Clear module boundaries
- Test coverage that enables confident modification

---

## Think Like a Database

*This concept from PostgreSQL Query Optimization is essential for writing performant queries.*

**Core insight:** To optimize effectively, you must understand how the database engine processes your query. Imagine you have to execute the query yourself, manually, against the data on disk. What would you have to do?

### Declarative vs. Imperative Thinking

SQL is a **declarative** language: you describe what result you want, not how to obtain it. This is fundamentally different from imperative languages where you specify the sequence of steps.

**The trap:** Developers naturally think imperatively. When approaching a query, they think about steps:
1. First, find all frequent flyers with level 4
2. Then, get their account numbers
3. Then, find their bookings
4. Then, filter by date and departure...

This thinking produces nested subqueries and CTEs that **lock in a specific execution order**, preventing the optimizer from choosing better approaches.

**Example: Imperative Style (Anti-pattern)**

```sql
WITH bk AS (
  WITH level4 AS (
    SELECT * FROM account WHERE frequent_flyer_id IN (
      SELECT frequent_flyer_id FROM frequent_flyer WHERE level = 4
    )
  )
  SELECT * FROM booking WHERE account_id IN
    (SELECT account_id FROM level4)
)
SELECT * FROM bk WHERE bk.booking_id IN (
  SELECT booking_id FROM booking_leg WHERE leg_num = 1
    AND is_returning IS false
    AND flight_id IN (
      SELECT flight_id FROM flight
      WHERE departure_airport IN ('ORD', 'MDW')
        AND scheduled_departure::DATE = '2020-07-04'
    )
)
```

This forces the database to follow your specified order, even if it's suboptimal.

**Example: Declarative Style (Correct)**

```sql
SELECT count(*) FROM
  booking bk
  JOIN booking_leg bl ON bk.booking_id = bl.booking_id
  JOIN flight f ON f.flight_id = bl.flight_id
  JOIN account a ON a.account_id = bk.account_id
  JOIN frequent_flyer ff ON ff.frequent_flyer_id = a.frequent_flyer_id
  JOIN passenger ps ON ps.booking_id = bk.booking_id
WHERE level = 4
  AND leg_num = 1
  AND is_returning IS false
  AND departure_airport IN ('ORD', 'MDW')
  AND scheduled_departure BETWEEN '2020-07-04' AND '2020-07-05'
```

This tells the database what you need, allowing the optimizer to choose the best execution order based on statistics and indexes.

### Why Two Equivalent Queries Can Have Different Performance

Consider these two queries that return identical results:

```sql
-- Query A: BETWEEN operator
SELECT flight_id, departure_airport, arrival_airport
FROM flight
WHERE scheduled_arrival BETWEEN '2020-10-14' AND '2020-10-15';

-- Query B: Cast to date
SELECT flight_id, departure_airport, arrival_airport
FROM flight
WHERE scheduled_arrival::date = '2020-10-14';
```

Query A can use an index on `scheduled_arrival`. Query B cannot—the cast transforms every value, preventing index usage. Same result, vastly different performance.

**The lesson:** Understanding how the database engine works is not optional. It determines whether your application performs well or collapses under load.

---

## OLTP vs. OLAP: Different Optimization Strategies

Understanding whether you're optimizing for OLTP or OLAP fundamentally changes your approach.

### Characteristics

| Aspect | OLTP (Online Transaction Processing) | OLAP (Online Analytical Processing) |
|--------|--------------------------------------|-------------------------------------|
| **Primary users** | Application, end users | Analysts, data scientists |
| **Operations** | INSERT, UPDATE, DELETE, point queries | Complex aggregations, scans |
| **Data scope** | Single record or small set | Large portions or entire tables |
| **Access pattern** | Random access by key | Sequential scans, aggregations |
| **Latency requirement** | Milliseconds | Seconds to hours acceptable |
| **Query complexity** | Simple, known patterns | Complex, ad-hoc |
| **Concurrency** | Many concurrent users | Few concurrent queries |

### Query Classification: Short vs. Long

**Short queries** (typical in OLTP):
- Access small number of rows (ideally single digits to hundreds)
- Should complete in milliseconds
- Must be highly concurrent
- Index-driven

**Long queries** (typical in OLAP):
- Access large portions of data
- Completion in seconds or minutes is acceptable
- Full table scans may be optimal
- Aggregate-focused

**Critical insight:** The length of the SQL statement text has nothing to do with whether a query is "short" or "long." A one-line query that scans millions of rows is a long query. A multi-page query that retrieves one row by primary key is a short query.

### Optimization Differences

| Strategy | OLTP | OLAP |
|----------|------|------|
| **Indexes** | Many, targeted indexes | Fewer indexes; scans often better |
| **Normalization** | Highly normalized | Often denormalized |
| **Query patterns** | Fixed, known queries | Ad-hoc, varied queries |
| **Response time goal** | < 100ms typical | Minutes acceptable |
| **Full scans** | Almost always bad | Often optimal |

---

## Setting SMART Optimization Goals

Optimization without defined goals leads to wasted effort. Use the SMART framework:

| Characteristic | Bad Example | Good Example |
|----------------|-------------|--------------|
| **Specific** | "All pages should respond fast" | "Each function execution completes before system timeout" |
| **Measurable** | "Customers shouldn't wait too long" | "Registration page response time < 4 seconds" |
| **Achievable** | "Daily refresh time should never increase" | "Refresh time grows logarithmically with data volume" |
| **Result-based** | "Each report should run as fast as possible" | "Report refresh avoids lock waits" |
| **Time-bound** | "We will optimize as many reports as we can" | "By month end, all financial reports run in < 30 seconds" |

### Response Time Varies by Context

What is "good enough" depends entirely on context:

| Context | Acceptable Response Time |
|---------|-------------------------|
| Web application function | < 100ms |
| Page load | 1-3 seconds |
| Executive dashboard | < 10 seconds |
| Daily marketing analysis | Minutes |
| Monthly general ledger | Under 1 hour |

### Beyond Response Time

Other optimization goals may include:
- **Throughput:** Maximize transactions per second (important for service providers)
- **Resource utilization:** Minimize hardware costs while maintaining performance
- **Consistency:** Ensure data correctness under concurrent access
- **Availability:** Minimize downtime

---

## Data Systems Thinking

Modern applications rarely use a single tool for all data needs. Instead, they compose multiple specialized components:

- **Databases** for persistent storage
- **Caches** for accelerating reads
- **Search indexes** for text queries
- **Message queues** for async processing
- **Stream processors** for real-time events
- **Batch processors** for periodic analysis

When you combine tools, you become a data system designer, not just an application developer. Your composite system must provide guarantees:
- Cache correctly invalidated on writes
- Indexes kept in sync with source data
- Consistent results across components

### Data-Intensive vs. Compute-Intensive

**Data-intensive applications:** Data is the primary challenge—quantity, complexity, or speed of change. Most modern applications fall here.

**Compute-intensive applications:** CPU cycles are the bottleneck.

This book focuses on data-intensive applications, where the limiting factor is data management, not computation.

---

## Principles for Data System Design

### 1. Start with Load Parameters

Before designing anything, identify your load parameters:
- What are your read/write ratios?
- How much data are you storing?
- What are your latency requirements?
- What are your access patterns?
- What's your 10x growth scenario?

### 2. Design for the Outliers, Not the Average

The Twitter example teaches this: average follower count doesn't predict system behavior. Celebrity accounts with millions of followers drive the architecture.

Identify your outliers:
- What are your largest records?
- Who are your most active users?
- What are your most complex queries?

### 3. Make Trade-offs Explicit

Every decision has consequences. Document them:
- "We're choosing eventual consistency for higher availability"
- "We're denormalizing this table for read performance at the cost of write complexity"
- "We're partitioning by customer_id, which makes cross-customer queries expensive"

### 4. Measure, Don't Guess

Before optimizing, measure:
- Use percentiles, not averages
- Monitor in production, not just test environments
- Track trends over time

### 5. Question Requirements

Before optimizing a slow report, ask: "Is this report still needed?" One organization cut 40% of reporting server traffic by questioning report purposes.

---

## Common Mistakes

| Mistake | Why It's Wrong | Better Approach |
|---------|---------------|-----------------|
| Optimizing for average case | Outliers dominate real-world behavior | Design for percentiles |
| Premature optimization | You don't know what will matter | Measure first, then optimize |
| Ignoring operations | Development is 10% of lifetime cost | Design for operability from day one |
| Designing for current load only | Growth will invalidate assumptions | Plan for 10x growth scenarios |
| Treating SQL as "just queries" | SQL is code with engineering standards | Apply version control, testing, review |
| "Make it work, then optimize" | Bad structure is hard to fix later | Think about performance while designing |

---

## Key Takeaways

1. **Reliability, Scalability, Maintainability** are not features—they are properties that must be designed in from the start.

2. **Faults are inevitable; failures are preventable.** Build systems that tolerate component faults without failing as a whole.

3. **Scalability requires understanding your load.** Define your load parameters before discussing how to scale.

4. **Use percentiles, not averages** to understand real user experience.

5. **Think like a database.** Understand how the engine processes queries to write performant SQL.

6. **Declarative thinking enables optimization.** Let the query planner do its job by describing what you want, not how to get it.

7. **OLTP and OLAP require different strategies.** Know which you're optimizing for.

8. **Set SMART optimization goals.** Vague goals lead to wasted effort.

9. **You are a data system designer.** When combining multiple tools, you're responsible for the guarantees of the whole system.

---

## References

- Kleppmann, M. *Designing Data-Intensive Applications*, Chapter 1
- Dombrovskaya, H. et al. *PostgreSQL Query Optimization*, Chapter 1
- Fontaine, D. *The Art of PostgreSQL*, Introduction
