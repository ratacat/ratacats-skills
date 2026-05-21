# Scaling Patterns

## Overview

When a single machine cannot handle your data volume, read load, or write load, you must distribute data across multiple machines. This chapter covers the two fundamental techniques for distributed data: **replication** (keeping copies on multiple nodes) and **partitioning** (splitting data across nodes).

**Core insight:** Scaling a stateful data system is fundamentally harder than scaling stateless services. There are no magic solutions—only trade-offs between consistency, availability, and complexity.

---

## Why Distribute Data?

Three primary reasons to distribute a database:

| Reason | Goal | Technique |
|--------|------|-----------|
| **Scalability** | Handle more data or load than one machine can | Partitioning |
| **Fault tolerance** | Keep running despite failures | Replication |
| **Latency** | Serve users from nearby locations | Geo-distributed replication |

---

## Scaling Approaches

### Vertical Scaling (Scale Up)

Move to a more powerful machine: more CPUs, RAM, disk.

**Advantages:**
- Simple — no distributed systems complexity
- Strong consistency by default
- All data in one place

**Disadvantages:**
- Cost grows faster than linearly
- Single point of failure
- Limited by available hardware

### Horizontal Scaling (Scale Out)

Distribute across multiple machines (shared-nothing architecture).

**Advantages:**
- Can scale beyond single-machine limits
- Fault tolerance through redundancy
- Geographic distribution possible

**Disadvantages:**
- Significant added complexity
- Network latency and partitions
- Weaker consistency guarantees

### Practical Guidance

**Start vertical, go horizontal when necessary:**

1. Optimize queries and indexes first
2. Scale up until cost/capability limits
3. Add read replicas if read-heavy
4. Partition only when unavoidable

> "In some cases, a simple single-threaded program can perform significantly better than a cluster with over 100 CPU cores."

---

## Replication

Replication keeps copies of the same data on multiple machines.

### Purposes of Replication

- **High availability:** Keep running if nodes fail
- **Latency reduction:** Serve from nearby replicas
- **Read scalability:** Distribute read load

### Replication Topologies

#### Single-Leader (Master-Slave)

**How it works:**
1. One node is designated **leader** (master, primary)
2. All writes go to the leader
3. Leader streams changes to **followers** (slaves, replicas)
4. Reads can go to leader or followers

```
         Writes
           │
           ▼
        ┌──────┐
        │Leader│
        └──┬───┘
           │ Replication stream
     ┌─────┼─────┐
     ▼     ▼     ▼
┌────────┐ ┌────────┐ ┌────────┐
│Follower│ │Follower│ │Follower│
└────────┘ └────────┘ └────────┘
     ▲         ▲         ▲
     └─────────┴─────────┘
           Reads
```

**Advantages:**
- No write conflicts (single writer)
- Easy to understand
- Well-supported in PostgreSQL, MySQL, etc.

**Disadvantages:**
- Leader is single point of failure
- All writes go through one node
- Failover can be complex

**Used by:** PostgreSQL, MySQL, MongoDB, RabbitMQ

#### Multi-Leader

Multiple nodes accept writes; replicate changes to each other.

**Use cases:**
- Multi-datacenter deployment
- Offline-capable clients
- Collaborative editing

**Challenge:** Write conflicts when same data modified on different leaders.

**Conflict resolution strategies:**
- Last write wins (risk of data loss)
- Merge (application-specific logic)
- Keep all versions (let user resolve)

#### Leaderless

No designated leader; clients write to multiple nodes.

**How it works:**
- Write to W nodes
- Read from R nodes
- If W + R > N, reads overlap with writes

**Example:** With N=3, W=2, R=2:
- Write succeeds if 2 nodes confirm
- Read queries 2 nodes, takes most recent
- At least 1 node seen both read and write

**Used by:** Cassandra, Riak, Voldemort (Dynamo-style)

### Synchronous vs Asynchronous Replication

| Aspect | Synchronous | Asynchronous |
|--------|-------------|--------------|
| **Durability** | Guaranteed on replica | May lose recent writes |
| **Latency** | Higher (wait for replica) | Lower (don't wait) |
| **Availability** | Blocked if replica down | Continues if replica down |

**Practical approach:** Semi-synchronous — one synchronous replica, others async.

### Replication Lag

Asynchronous replication means followers may be behind.

**Problems:**
- Read your writes: Write, then read from follower that hasn't caught up
- Monotonic reads: Read from one replica, then older replica
- Consistent prefix: See effect before cause

**Mitigation:**
- Read from leader for recently written data
- Session stickiness to same replica
- Include version/timestamp in reads

### Failover

When leader fails, a follower must become the new leader.

**Failover steps:**
1. Detect leader failure (timeout-based)
2. Choose new leader (most up-to-date replica)
3. Reconfigure clients to use new leader
4. Handle old leader if it comes back

**Risks:**
- Split brain: Two nodes think they're leader
- Data loss: Async replica may be behind
- Coordination: External systems need updating

---

## Partitioning (Sharding)

Partitioning splits data across nodes so each node holds a subset.

### Why Partition?

- Dataset too large for one machine
- Query throughput exceeds one machine's capacity
- Write throughput exceeds one machine's capacity

### Partitioning Strategies

#### By Key Range

Assign continuous ranges of keys to each partition.

```
Partition 0: A-F
Partition 1: G-L
Partition 2: M-R
Partition 3: S-Z
```

**Advantages:**
- Efficient range queries
- Keys sorted within partition
- Easy to understand

**Disadvantages:**
- Risk of hot spots (sequential keys)
- Timestamp-based keys → one hot partition

**Example problem:** If key is timestamp, all writes go to "today" partition.

**Solution:** Prefix key with something distributed (sensor_id, user_id).

#### By Hash of Key

Hash the key and assign hash ranges to partitions.

**Advantages:**
- Even distribution of keys
- No hot spots from sequential keys

**Disadvantages:**
- Lose range query efficiency
- Keys scattered across partitions

**Cassandra's compromise:** Hash first column, sort by remaining columns.
```sql
PRIMARY KEY ((user_id), timestamp)
-- Partitioned by hash(user_id)
-- Sorted by timestamp within partition
```

### Partitioning and Secondary Indexes

Secondary indexes complicate partitioning.

#### Local Index (Document-Partitioned)

Each partition maintains its own index for its data.

```
Partition 0: Index of its own red cars
Partition 1: Index of its own red cars
...
```

**Query:** Must scatter to all partitions, gather results.

**Used by:** MongoDB, Cassandra, Elasticsearch

#### Global Index (Term-Partitioned)

Index entries distributed across partitions by term.

```
Index Partition 0: color:a-m (all cars with colors a-m)
Index Partition 1: color:n-z (all cars with colors n-z)
```

**Query:** Single partition for point queries.
**Write:** May update multiple index partitions.

**Trade-off:** Faster reads, slower writes.

### Hot Spots

Even with hash partitioning, hot spots can occur.

**Example:** Celebrity user — all writes to one partition.

**Application-level solutions:**
- Add random prefix to hot keys (e.g., user_123_01, user_123_02)
- Trade-off: Reads must combine results from all prefixed keys

### Rebalancing

Moving data between partitions when nodes added/removed.

**Goals:**
- Even load distribution after rebalancing
- Minimize data movement
- Keep system available during rebalancing

**Approaches:**

| Approach | Description | Trade-off |
|----------|-------------|-----------|
| Fixed partitions | Pre-create many partitions (e.g., 1000), assign to nodes | Simple, but partition size fixed |
| Dynamic partitions | Split when too large, merge when too small | Adapts to data, more complex |
| Per-node partitions | Fixed partitions per node | Scales with cluster |

**Anti-pattern:** `hash(key) mod N` — adding one node moves almost all data.

---

## Combining Replication and Partitioning

Real systems use both:

- Data partitioned across nodes
- Each partition replicated for fault tolerance

```
                    ┌─────────────────────┐
                    │   Partition 1       │
           ┌───────►│ Leader: Node A      │
           │        │ Follower: Node B, C │
           │        └─────────────────────┘
   Data────┤
           │        ┌─────────────────────┐
           │        │   Partition 2       │
           └───────►│ Leader: Node B      │
                    │ Follower: Node A, C │
                    └─────────────────────┘
```

Each node is leader for some partitions, follower for others.

---

## PostgreSQL Scaling Options

### Built-in Replication

**Streaming replication:**
- Async or sync
- Read replicas for query scaling
- Automatic failover with tools like Patroni

**Logical replication:**
- Replicate selected tables
- Cross-version replication
- Replicate to different schemas

### Partitioning (Native)

Declarative partitioning since PostgreSQL 10:

```sql
CREATE TABLE events (
    id SERIAL,
    created_at TIMESTAMP,
    data JSONB
) PARTITION BY RANGE (created_at);

CREATE TABLE events_2023 PARTITION OF events
    FOR VALUES FROM ('2023-01-01') TO ('2024-01-01');
```

**Benefits:**
- Prune partitions in queries
- Faster VACUUM (per-partition)
- Easier archival (drop old partitions)

### Extensions

**Citus:** Distributed PostgreSQL for horizontal scaling.
- Transparent sharding
- Distributed queries
- Reference tables (replicated everywhere)

**TimescaleDB:** Time-series optimizations.
- Automatic partitioning by time
- Compression
- Continuous aggregates

---

## Consistency Trade-offs (CAP Theorem)

The CAP theorem states you can have at most 2 of 3:
- **Consistency:** All nodes see the same data
- **Availability:** Every request gets a response
- **Partition tolerance:** System works despite network partitions

**Reality:** Network partitions happen. You must choose between:
- **CP:** Sacrifice availability for consistency (wait for partition to heal)
- **AP:** Sacrifice consistency for availability (serve stale data)

### Consistency Models

| Model | Guarantee | Performance |
|-------|-----------|-------------|
| **Strong (linearizable)** | Reads see latest write | Slowest |
| **Sequential** | Operations in some order | Fast |
| **Causal** | Cause before effect | Fast |
| **Eventual** | Eventually converge | Fastest |

**PostgreSQL:** Strong consistency on single node; configurable on replicas.

---

## Read Replicas Pattern

Common pattern for read-heavy workloads:

1. All writes to primary
2. Reads distributed across replicas
3. Application routes read-only queries to replicas

**Implementation:**
```python
# Simple connection routing
def get_connection(read_only=False):
    if read_only:
        return replica_pool.get()
    return primary_pool.get()
```

**Considerations:**
- Replication lag: May read stale data
- Session consistency: Route user's reads to same replica
- Query routing: Which queries are safe on replicas?

---

## Scaling Decision Framework

### When to Add Read Replicas

- Read queries dominating CPU
- Read latency requirements in multiple regions
- Need redundancy for disaster recovery

### When to Partition

- Data volume exceeds single-machine capacity
- Write throughput exceeds single-machine capacity
- Hot partitions after optimization

### When to Stay Single-Node

- Data fits comfortably in memory
- Writes are not bottleneck
- Strong consistency required
- Team lacks distributed systems expertise

---

## Common Mistakes

| Mistake | Why It's Wrong | Better Approach |
|---------|----------------|-----------------|
| Premature sharding | Massive complexity for unclear benefit | Optimize and scale up first |
| Ignoring replication lag | Stale reads cause user confusion | Design for eventual consistency or route appropriately |
| Wrong partition key | Hot spots, cross-partition queries | Analyze access patterns before partitioning |
| hash(key) mod N | Most data moves on rebalance | Use consistent hashing or fixed partitions |
| No failover testing | Discover problems in production | Practice failovers regularly |
| Assuming linearizability | Replicas may be behind | Understand your consistency model |

---

## Key Takeaways

1. **Replication and partitioning serve different purposes.** Replication for fault tolerance and read scaling; partitioning for data volume and write scaling.

2. **Single-leader replication is simplest.** Use it unless you have specific needs for multi-leader or leaderless.

3. **Replication lag is unavoidable** in asynchronous systems. Design applications to handle it.

4. **Partition key choice is critical.** Wrong choice leads to hot spots or inefficient queries.

5. **Range partitioning enables range queries;** hash partitioning distributes evenly.

6. **Combining partitioning + replication** is normal and necessary.

7. **CAP means real trade-offs.** Know what your system sacrifices during partitions.

8. **Start simple.** Single-node PostgreSQL handles more than most people think.

---

## References

- Kleppmann, M. *Designing Data-Intensive Applications*, Chapters 5-6
- PostgreSQL Documentation: High Availability, Load Balancing, Replication
- PostgreSQL Documentation: Table Partitioning
