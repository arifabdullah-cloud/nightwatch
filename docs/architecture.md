# Nightwatch Architecture

## Purpose

This document defines the initial architecture of Nightwatch and its supporting e-commerce workload.

Nightwatch is a cloud reliability and operations project. The e-commerce workload exists to generate realistic traffic, application behaviour, dependency usage, metrics, logs, traces, deployment events, and controlled failures.

The architecture should remain simple enough for one developer to build and operate, while still supporting meaningful reliability and failure scenarios.

---

## Architectural Approach

The initial workload will use a modular monolith.

All business endpoints will run within one FastAPI application, with internal modules separating product, cart, order, payment, and fault-injection logic.

This approach is intentionally chosen over microservices for the first version.

### Reasons

* Lower development and operational overhead
* Easier local execution
* Easier Docker deployment
* Simpler debugging
* Lower Azure cost
* Faster delivery of observability and reliability features
* Enough complexity to demonstrate application, database, cache, and dependency failures

The architecture may evolve into multiple services later when a failure scenario or scaling requirement provides a clear reason.

---

## System Context

```text
                    Synthetic Users
                       k6 / Locust
                            |
                            v
                  E-Commerce Workload
                      FastAPI API
                            |
             +--------------+--------------+
             |              |              |
             v              v              v
        PostgreSQL        Redis      Mock Payment
         Database         Cache         Provider
             |
             v
      Order and Product Data


                            |
                            v
                    Observability Layer
             Logs, Metrics, Traces and Events
                            |
                            v
                        Nightwatch
              Detection, Analysis and Response
```

---

## Initial Runtime Architecture

```text
+------------------------------------------------------+
| Synthetic Traffic Generator                          |
|                                                      |
| - Browses products                                   |
| - Adds products to carts                             |
| - Creates orders                                     |
| - Generates normal and peak traffic                  |
+---------------------------+--------------------------+
                            |
                            | HTTP
                            v
+------------------------------------------------------+
| FastAPI Workload Application                         |
|                                                      |
| Modules:                                             |
| - Product catalogue                                  |
| - Shopping cart                                      |
| - Order processing                                   |
| - Mock payment integration                           |
| - Health and readiness checks                        |
| - Fault injection                                    |
| - Structured logging                                 |
| - Metrics and tracing                                |
+-------------+----------------------+-----------------+
              |                      |
              | SQL                  | Cache operations
              v                      v
+-------------------------+   +-------------------------+
| PostgreSQL              |   | Redis                   |
|                         |   |                         |
| - Products              |   | - Product cache         |
| - Carts                 |   | - Cart state            |
| - Orders                |   | - Temporary data        |
+-------------------------+   +-------------------------+

              |
              | HTTP
              v
+------------------------------------------------------+
| Mock Payment Provider                                |
|                                                      |
| - Successful payments                                |
| - Delayed responses                                  |
| - Timeouts                                           |
| - Failed responses                                   |
+------------------------------------------------------+

              |
              v
+------------------------------------------------------+
| Observability                                        |
|                                                      |
| - Application logs                                   |
| - Request metrics                                    |
| - Dependency metrics                                 |
| - Distributed traces                                 |
| - Container health                                   |
| - Deployment events                                  |
| - Azure platform metrics                             |
+------------------------------------------------------+

              |
              v
+------------------------------------------------------+
| Nightwatch Reliability Capabilities                  |
|                                                      |
| - Health overview                                    |
| - Incident detection                                 |
| - Signal correlation                                 |
| - Operational recommendations                        |
| - Runbooks                                           |
| - Automated remediation                              |
+------------------------------------------------------+
```

---

## Initial Technology Choices

### Application

* Python
* FastAPI
* Uvicorn

### Database

* PostgreSQL

PostgreSQL will store persistent workload data, including products, carts, and orders.

### Cache

* Redis

Redis will support cache-related scenarios and reduce repeated database reads.

### Traffic Generation

* k6 or Locust

The final selection will be made when load testing is implemented.

### Containers

* Docker
* Docker Compose for local development

### Cloud Platform

* Microsoft Azure
* Azure Container Apps
* Azure Database for PostgreSQL or a lower-cost development alternative
* Azure Cache for Redis or a container-based alternative during early development
* Azure Monitor
* Log Analytics
* Application Insights

### Infrastructure as Code

* Bicep

### Continuous Integration and Deployment

* GitHub Actions

### Observability

* Structured application logging
* OpenTelemetry
* Azure Monitor
* Application Insights

Grafana may be added later if it provides value beyond Azure-native dashboards.

---

## Application Structure

The workload application should evolve toward the following structure:

```text
app/
├── main.py
├── api/
│   ├── health.py
│   ├── products.py
│   ├── carts.py
│   ├── orders.py
│   ├── payments.py
│   └── faults.py
├── core/
│   ├── config.py
│   ├── logging.py
│   └── telemetry.py
├── models/
│   ├── product.py
│   ├── cart.py
│   └── order.py
├── services/
│   ├── product_service.py
│   ├── cart_service.py
│   ├── order_service.py
│   └── payment_service.py
├── repositories/
│   ├── product_repository.py
│   ├── cart_repository.py
│   └── order_repository.py
├── faults/
│   ├── cpu.py
│   ├── memory.py
│   ├── latency.py
│   ├── errors.py
│   └── dependencies.py
└── tests/
```

This structure is a target, not a requirement to create every file immediately.

Files and modules should be introduced only when they are needed.

---

## Core Business Entities

## Product

Represents an item available for purchase.

Minimum fields:

* `id`
* `name`
* `description`
* `price`
* `stock_quantity`
* `is_active`

---

## Cart

Represents a temporary customer shopping cart.

Minimum fields:

* `id`
* `items`
* `created_at`
* `updated_at`

No permanent user account is required.

A cart ID is sufficient for synthetic users.

---

## Cart Item

Represents a product placed in a cart.

Minimum fields:

* `product_id`
* `quantity`
* `unit_price`

---

## Order

Represents a completed checkout attempt.

Minimum fields:

* `id`
* `cart_id`
* `status`
* `total_amount`
* `payment_status`
* `created_at`

Possible order statuses:

* `pending`
* `confirmed`
* `failed`

---

## Payment Result

Represents the result returned by the mock payment provider.

Minimum fields:

* `payment_id`
* `order_id`
* `status`
* `failure_reason`
* `processing_time_ms`

Possible payment statuses:

* `approved`
* `declined`
* `timeout`
* `error`

---

## Minimum Business Endpoints

The first version should implement only the endpoints required to create realistic read, write, cache, database, and dependency behaviour.

---

## Product Catalogue

### `GET /products`

Returns a list of active products.

Operational value:

* Generates database reads
* Supports Redis caching
* Produces cache hit and miss metrics
* Supports high-traffic browsing scenarios

Example response:

```json
{
  "items": [
    {
      "id": 1,
      "name": "Wireless Keyboard",
      "price": 49.90,
      "stock_quantity": 20
    }
  ],
  "count": 1
}
```

---

### `GET /products/{product_id}`

Returns one product by ID.

Operational value:

* Generates targeted database or cache reads
* Supports product-level latency analysis
* Produces HTTP 404 behaviour for invalid IDs

---

## Shopping Cart

### `POST /carts`

Creates a new anonymous cart.

Operational value:

* Generates database writes
* Gives each synthetic user an isolated session
* Avoids unnecessary authentication complexity

Example response:

```json
{
  "cart_id": "0b6ad99d-7324-49ce-8f74-1cf835ac1744",
  "status": "active"
}
```

---

### `POST /carts/{cart_id}/items`

Adds an item to a cart.

Example request:

```json
{
  "product_id": 1,
  "quantity": 2
}
```

Operational value:

* Generates reads and writes
* Requires product validation
* Can use Redis for temporary cart state
* Supports cache and database dependency failures

---

### `GET /carts/{cart_id}`

Returns the current cart.

Operational value:

* Produces repeated cache reads
* Supports cache hit-rate measurement
* Allows synthetic users to validate cart state

---

## Order Processing

### `POST /orders`

Submits a cart for checkout.

Example request:

```json
{
  "cart_id": "0b6ad99d-7324-49ce-8f74-1cf835ac1744"
}
```

Expected workflow:

1. Retrieve the cart.
2. Validate cart contents.
3. Validate available product stock.
4. Create a pending order.
5. Call the mock payment provider.
6. Update order and payment status.
7. Return the result.

Operational value:

* Exercises PostgreSQL
* Exercises Redis
* Calls an external dependency
* Creates latency, timeout, retry, and failure signals
* Supports distributed tracing
* Produces meaningful business transaction metrics

---

### `GET /orders/{order_id}`

Returns the order status.

Operational value:

* Supports polling behaviour
* Generates additional database reads
* Allows delayed or asynchronous workflows later

---

## Operational Endpoints

### `GET /health`

Indicates whether the application process is running.

The health endpoint should not depend on PostgreSQL, Redis, or the payment provider.

Example response:

```json
{
  "status": "healthy"
}
```

A successful health check means the process is alive. It does not mean the application can serve production traffic correctly.

---

### `GET /ready`

Indicates whether the application is ready to receive production traffic.

The readiness check should eventually validate required dependencies.

Initial dependencies:

* PostgreSQL connectivity

Redis may be treated as optional if the application supports database fallback.

Example healthy response:

```json
{
  "status": "ready",
  "dependencies": {
    "postgresql": "available",
    "redis": "available"
  }
}
```

Example degraded response:

```json
{
  "status": "not_ready",
  "dependencies": {
    "postgresql": "unavailable",
    "redis": "available"
  }
}
```

---

## Mock Payment Provider Endpoints

The mock payment provider may initially run inside the same application, but it should use a separate API route to simulate an external dependency.

### `POST /mock-payment/charge`

Example request:

```json
{
  "order_id": "order-123",
  "amount": 99.80
}
```

Supported behaviours:

* Successful payment
* Payment declined
* Delayed response
* HTTP 500 response
* Timeout

This endpoint should eventually be separated into its own container when dependency-level observability is introduced.

---

## Fault Injection Endpoints

Fault injection endpoints should not be publicly usable in a production environment.

They must be:

* Disabled by default
* Controlled through configuration
* Protected using an administrative token or private network
* Clearly identified as development and testing functionality

Potential endpoints:

### `POST /admin/faults/error-rate`

Introduces controlled HTTP errors for a percentage of requests.

Example request:

```json
{
  "enabled": true,
  "percentage": 25
}
```

---

### `POST /admin/faults/latency`

Adds artificial latency.

Example request:

```json
{
  "enabled": true,
  "delay_ms": 1000,
  "target": "database"
}
```

---

### `POST /admin/faults/cpu`

Starts or stops CPU pressure.

---

### `POST /admin/faults/memory`

Starts or stops controlled memory growth.

---

### `POST /admin/faults/payment`

Controls mock payment behaviour.

Example request:

```json
{
  "mode": "timeout"
}
```

Possible modes:

* `normal`
* `slow`
* `timeout`
* `error`
* `decline`

---

### `GET /admin/faults`

Returns the currently active fault configuration.

---

### `DELETE /admin/faults`

Disables active faults and restores the normal state.

---

## Initial Endpoint Scope

The first implementation should include:

```text
GET  /
GET  /health
GET  /ready
GET  /products
GET  /products/{product_id}
POST /carts
POST /carts/{cart_id}/items
GET  /carts/{cart_id}
POST /orders
GET  /orders/{order_id}
POST /mock-payment/charge
```

Fault injection endpoints should be added only after normal workload behaviour is stable and observable.

---

## Synthetic User Flow

The initial synthetic user journey will be:

```text
Create cart
    |
    v
Browse products
    |
    v
View random product
    |
    v
Add product to cart
    |
    v
Optional pause
    |
    v
Submit order
    |
    v
Check order status
```

Suggested behavioural distribution:

* 100% request the product list
* 70% view at least one product
* 35% create or update a cart
* 10% submit an order
* 5% poll order status

These percentages are initial assumptions and should be adjusted after observing system behaviour.

---

## Data Strategy

The application should use seeded product data.

No product administration interface is required.

Initial product records may be inserted through:

* Database migration
* Seed script
* Application startup script for local development

The project does not need:

* User registration
* User authentication
* Product administration
* Real payment processing
* Shipping
* Refund processing
* Promotional codes
* Full inventory management
* Customer profiles

These features do not materially improve the reliability scenarios at the current stage.

---

## Deployment Evolution

### Stage 1 — Local Development

```text
FastAPI
PostgreSQL
Redis
Mock payment route
Docker Compose
```

### Stage 2 — Initial Azure Deployment

```text
Azure Container Apps
PostgreSQL
Redis
Azure Monitor
Application Insights
```

### Stage 3 — Dependency Separation

The mock payment provider may move into a separate container.

```text
Workload API
    |
    v
Payment API
```

### Stage 4 — Nightwatch Capabilities

Nightwatch begins consuming and correlating:

* Application metrics
* Logs
* Traces
* Azure resource metrics
* Deployment events
* Fault injection state

---

## Architecture Principles

The project should follow these principles:

1. Build only what is needed to support a reliability scenario.
2. Prefer a modular monolith before introducing microservices.
3. Keep failure injection controlled and reversible.
4. Separate application health from readiness.
5. Instrument important operations from the beginning.
6. Use structured logs rather than unstructured text.
7. Use Infrastructure as Code for Azure resources.
8. Keep local development inexpensive and reproducible.
9. Avoid real customer, payment, or personal data.
10. Document major architecture changes and their rationale.

---

## Current Status

The current implementation contains:

* FastAPI application
* Root endpoint
* Health endpoint
* Readiness endpoint
* Docker configuration

The business endpoints, PostgreSQL integration, Redis integration, synthetic users, observability, and fault injection have not yet been implemented.
