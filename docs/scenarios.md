# Nightwatch Scenarios

## Purpose

This document defines the workload and failure scenarios used to develop and demonstrate Nightwatch.

Nightwatch is a cloud reliability and operations platform. It requires a realistic application workload so that monitoring, alerting, diagnostics, incident response, and remediation capabilities can be tested against observable system behaviour.

The initial workload will be a simplified e-commerce platform.

The e-commerce application is not the main product. It exists primarily to generate realistic application traffic, infrastructure utilisation, logs, metrics, dependencies, and operational failures for Nightwatch to observe.

---

## Workload Overview

The workload represents a small online store where synthetic customers can:

* Browse products
* View product details
* Add products to a cart
* Submit an order
* Check order status

The business functionality will remain intentionally limited. Development effort should focus on reliability engineering, observability, automation, and cloud operations rather than building a complete commercial e-commerce platform.

---

## Planned Workload Components

The initial system may include the following components:

* Product catalogue API
* Shopping cart service
* Order service
* PostgreSQL database
* Redis cache
* Mock payment service
* Background notification worker
* Synthetic traffic generator

The exact architecture may evolve as the project develops.

---

## User Journey

A typical synthetic customer journey will follow this sequence:

1. Request the product catalogue.
2. View one or more products.
3. Add a product to the cart.
4. Pause for a short, random period.
5. Submit an order.
6. Receive either a successful response or a controlled failure.
7. Repeat the journey based on the active traffic profile.

Not every synthetic user will complete checkout.

The workload generator should create a realistic distribution of behaviour, with product browsing occurring more frequently than cart updates or order submissions.

---

## Traffic Profiles

### Normal Traffic

Represents ordinary system usage.

Expected characteristics:

* Low to moderate request rate
* Stable response times
* Low error rate
* Normal database utilisation
* High cache availability
* No active fault injection

Purpose:

* Establish a healthy baseline
* Validate monitoring and dashboards
* Measure normal latency and resource usage
* Confirm that alerts remain inactive

---

### Peak Traffic

Represents a short period of increased customer activity.

Expected characteristics:

* Rapid increase in concurrent users
* Increased CPU and memory usage
* Higher database connection usage
* Increased cache activity
* Possible increase in response latency

Purpose:

* Test autoscaling behaviour
* Validate capacity thresholds
* Identify system bottlenecks
* Confirm that alerts distinguish high utilisation from actual failure

---

### Sustained High Traffic

Represents prolonged elevated demand.

Expected characteristics:

* High request rate over an extended period
* Sustained database and cache pressure
* Increased operational cost
* Possible queue or connection backlog
* Potential performance degradation

Purpose:

* Evaluate long-running capacity limits
* Detect resource saturation
* Observe scaling stability
* Identify cost and efficiency concerns

---

## Failure Scenarios

## Scenario 1 — Application Error Spike

### Description

The application begins returning an increased number of HTTP 500 responses.

### Possible Cause

A controlled application fault is enabled for a percentage of incoming requests.

### Expected Signals

* Increased server error rate
* Failed request logs
* Reduced successful transaction rate
* Possible retry activity
* Alert triggered when the configured error threshold is exceeded

### Nightwatch Objectives

Nightwatch should eventually be able to:

* Detect the increase in server errors
* Identify the affected service or endpoint
* Show the approximate incident start time
* Correlate errors with recent changes or fault activation
* Recommend investigation of application logs and deployments

---

## Scenario 2 — High CPU Utilisation

### Description

One or more application instances experience sustained high CPU utilisation.

### Possible Cause

A controlled CPU-intensive operation is triggered while synthetic traffic is active.

### Expected Signals

* CPU usage exceeds the normal baseline
* Request latency increases
* Throughput may decline
* Autoscaling may add application replicas
* Health checks may remain successful initially

### Nightwatch Objectives

Nightwatch should eventually be able to:

* Detect sustained CPU pressure
* Distinguish a brief spike from an ongoing issue
* Correlate CPU usage with increased latency
* Show scaling activity
* Recommend scaling or investigating CPU-intensive operations

---

## Scenario 3 — Memory Pressure

### Description

Application memory usage increases continuously until the container or process is restarted.

### Possible Cause

A controlled memory leak is introduced.

### Expected Signals

* Gradual increase in memory usage
* Reduced available memory
* Container restart or termination
* Temporary reduction in service availability
* Possible increase in failed requests

### Nightwatch Objectives

Nightwatch should eventually be able to:

* Detect abnormal memory growth
* Identify container or process restarts
* Correlate restarts with availability loss
* Recommend investigating memory allocation and leak behaviour
* Record the recovery timeline

---

## Scenario 4 — Slow Database

### Description

Database operations become significantly slower than normal.

### Possible Cause

Artificial latency is added to database queries, or inefficient queries are introduced.

### Expected Signals

* Increased API response time
* Increased database query duration
* Higher connection usage
* Request timeouts
* Reduced checkout success rate

### Nightwatch Objectives

Nightwatch should eventually be able to:

* Detect increased database latency
* Correlate database slowdown with API performance
* Identify the most affected endpoints
* Detect connection pool pressure
* Recommend investigating slow queries or database capacity

---

## Scenario 5 — Database Unavailable

### Description

The application cannot connect to PostgreSQL.

### Possible Cause

The database is stopped, blocked, misconfigured, or made temporarily unreachable.

### Expected Signals

* Database connection errors
* Failed readiness checks
* Increased HTTP 500 or HTTP 503 responses
* Failed order operations
* Possible retry storms

### Nightwatch Objectives

Nightwatch should eventually be able to:

* Detect database connectivity failure
* Mark the application as not ready
* Identify PostgreSQL as the failing dependency
* Distinguish infrastructure failure from application failure
* Recommend restoring connectivity or database availability

---

## Scenario 6 — Redis Cache Unavailable

### Description

The Redis cache becomes unavailable while the application remains operational.

### Possible Cause

Redis is stopped or network access is interrupted.

### Expected Signals

* Cache connection failures
* Reduced cache hit rate
* Increased database query volume
* Increased response latency
* Possible application errors if cache fallback is not implemented correctly

### Nightwatch Objectives

Nightwatch should eventually be able to:

* Detect cache availability problems
* Show the reduction in cache effectiveness
* Correlate cache failure with increased database load
* Determine whether the application degraded gracefully
* Recommend restoring Redis or reviewing fallback behaviour

---

## Scenario 7 — Payment Service Timeout

### Description

The mock payment service responds slowly or stops responding.

### Possible Cause

Artificial network latency or timeout behaviour is introduced.

### Expected Signals

* Increased checkout latency
* Payment request timeouts
* Retry attempts
* Reduced order completion rate
* Possible duplicate requests if retry handling is incorrect

### Nightwatch Objectives

Nightwatch should eventually be able to:

* Detect dependency latency
* Identify the payment service as the affected dependency
* Show timeout and retry behaviour
* Detect possible retry amplification
* Recommend circuit breaking, backoff, or dependency investigation

---

## Scenario 8 — Payment Service Error

### Description

The payment service returns failed responses.

### Possible Cause

The mock payment service returns HTTP 500 or transaction rejection responses.

### Expected Signals

* Increased checkout failure rate
* Payment-related application logs
* Failed orders
* Normal infrastructure health despite business transaction failures

### Nightwatch Objectives

Nightwatch should eventually be able to:

* Detect business transaction degradation
* Distinguish dependency errors from infrastructure outages
* Identify the affected checkout workflow
* Show failure rate and incident duration
* Recommend reviewing dependency health and fallback behaviour

---

## Scenario 9 — Traffic Surge

### Description

The workload receives a sudden and substantial increase in requests.

### Possible Cause

The synthetic traffic generator rapidly increases the number of concurrent users.

### Expected Signals

* Sudden request-rate increase
* CPU and memory growth
* Increased database connections
* Increased latency
* Autoscaling activity
* Possible request throttling or failures

### Nightwatch Objectives

Nightwatch should eventually be able to:

* Detect the traffic surge
* Show the relationship between traffic and resource utilisation
* Observe autoscaling response
* Identify whether the system remained within service objectives
* Recommend capacity or scaling changes when required

---

## Scenario 10 — Container Crash

### Description

An application container exits unexpectedly.

### Possible Cause

A controlled crash endpoint, fatal exception, or forced process termination is triggered.

### Expected Signals

* Container termination
* Failed requests during restart
* New container instance created
* Health and readiness state changes
* Application restart event

### Nightwatch Objectives

Nightwatch should eventually be able to:

* Detect the crash and restart
* Record service interruption duration
* Correlate the crash with logs or fault activation
* Confirm whether the platform recovered automatically
* Recommend investigation when crashes repeat

---

## Scenario 11 — Deployment Regression

### Description

A newly deployed application version causes increased errors or latency.

### Possible Cause

A deliberately faulty application release is deployed.

### Expected Signals

* Error or latency increase following deployment
* Healthy infrastructure but degraded application behaviour
* Change in service version
* Alert activation shortly after release

### Nightwatch Objectives

Nightwatch should eventually be able to:

* Correlate degradation with deployment time
* Identify the affected application version
* Compare current behaviour with the previous baseline
* Recommend rollback when appropriate
* Record the deployment as a probable incident trigger

---

## Scenario 12 — Readiness Failure

### Description

The application process is running but is unable to serve production traffic safely.

### Possible Cause

A required dependency is unavailable, or the application has not completed initialisation.

### Expected Signals

* Health endpoint remains successful
* Readiness endpoint fails
* Traffic should be removed from the affected instance
* Reduced available capacity

### Nightwatch Objectives

Nightwatch should eventually be able to:

* Distinguish health from readiness
* Detect reduced serving capacity
* Identify the failing readiness dependency
* Confirm whether traffic routing behaved correctly
* Recommend remediation for the failed dependency

---

## Scenario 13 — Notification Queue Backlog

### Description

Background notification jobs accumulate faster than they are processed.

### Possible Cause

The notification worker is slowed, stopped, or receives an increased job volume.

### Expected Signals

* Increasing queue depth
* Increased message age
* Delayed notifications
* Worker utilisation increase
* Possible failed or retried jobs

### Nightwatch Objectives

Nightwatch should eventually be able to:

* Detect queue backlog growth
* Measure processing delay
* Identify worker capacity problems
* Correlate order activity with queued notifications
* Recommend scaling or restoring the worker

---

## Scenario 14 — Misconfiguration

### Description

The application is deployed with an incorrect environment variable or dependency configuration.

### Possible Cause

A deployment introduces an invalid connection string, missing secret, or incorrect service address.

### Expected Signals

* Startup failure or readiness failure
* Repeated application restarts
* Configuration-related logs
* Dependency connection errors
* Deployment-associated incident

### Nightwatch Objectives

Nightwatch should eventually be able to:

* Detect the failed deployment
* Correlate the issue with the configuration change
* Identify the affected dependency or variable where possible
* Recommend rollback or configuration correction
* Preserve an audit trail of the incident

---

## Scenario 15 — Combined Failure

### Description

Two or more failures occur at the same time.

Example:

* Peak traffic begins
* Redis becomes unavailable
* Database load increases
* API latency rises
* Checkout errors increase

### Purpose

This scenario tests whether Nightwatch can avoid treating every symptom as an independent incident.

### Nightwatch Objectives

Nightwatch should eventually be able to:

* Correlate related signals
* Identify the likely initiating event
* Separate the probable cause from secondary symptoms
* Produce a coherent incident timeline
* Avoid generating excessive duplicate alerts

---

## Success Criteria

A scenario will be considered successfully implemented when:

* It can be triggered in a controlled and repeatable way.
* It produces observable logs, metrics, traces, or platform events.
* The system can return to a healthy state after the scenario.
* The expected behaviour is documented.
* Nightwatch can detect or display at least one relevant signal.
* The incident and recovery process can be demonstrated.

Later project phases may introduce stricter criteria, including:

* Alert activation
* Root-cause suggestions
* Service-level objective impact
* Automated remediation
* Incident timeline generation
* Audit logging

---

## Scenario Implementation Principles

Failure injection must be:

* Explicitly enabled
* Disabled by default
* Safe to run in a development environment
* Repeatable
* Observable
* Reversible
* Protected from accidental public use where necessary

Fault injection should not depend on manually damaging cloud resources unless the scenario specifically requires infrastructure failure.

Where possible, application-level fault controls should be used first because they are safer, cheaper, and easier to reproduce.

---

## Initial Implementation Priority

The first scenarios to implement should be:

1. Normal traffic baseline
2. Application error spike
3. High CPU utilisation
4. Slow database
5. Redis unavailable
6. Traffic surge
7. Container crash
8. Deployment regression

These scenarios provide enough variety to demonstrate:

* Application monitoring
* Infrastructure monitoring
* Dependency monitoring
* Load testing
* Autoscaling
* Incident detection
* Deployment correlation
* Recovery behaviour

The remaining scenarios can be introduced incrementally as Nightwatch develops.

---

## Current Status

The scenarios in this document are design targets.

At the current stage, only the initial FastAPI application, health endpoint, readiness endpoint, and Docker setup have been completed.

No failure scenarios have been implemented yet.
