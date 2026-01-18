---
name: jtl-workflow-automator
description: "Automates JTL-Wawi and JTL-Shop business workflows through intelligent orchestration. Use when: (1) Building automated order processing pipelines, (2) Creating inventory sync workflows between Wawi and Shop, (3) Generating business reports from JTL data, (4) Implementing supplier/procurement automation, (5) Creating customer notification workflows, (6) Building product data enrichment pipelines, (7) Automating price updates across channels, (8) Any request mentioning JTL workflow, automation, or batch processing. Keywords: JTL-Wawi, JTL-Shop, automation, workflow, batch, sync, inventory, orders, ERP."
---

# JTL Workflow Automator

Orchestrates automated business workflows for JTL-Wawi and JTL-Shop e-commerce operations.

## Quick Start

1. Identify the workflow type (see Workflow Categories below)
2. Load the relevant reference file for detailed patterns
3. Use provided scripts for common operations
4. Customize workflow logic as needed

## Workflow Categories

### Order Processing
Automate order lifecycle: import → validate → fulfill → notify → archive.
**Reference:** `references/order-workflows.md`

### Inventory Management  
Sync stock levels, reorder alerts, supplier integration, multi-warehouse.
**Reference:** `references/inventory-workflows.md`

### Product Data
Enrich products, sync across channels, automate categorization, update pricing.
**Reference:** `references/product-workflows.md`

### Reporting & Analytics
Generate scheduled reports, KPI dashboards, export automation.
**Reference:** `references/reporting-workflows.md`

## Core Scripts

| Script | Purpose |
|--------|---------|
| `scripts/wawi_connector.py` | JTL-Wawi REST API client with auth handling |
| `scripts/workflow_engine.py` | Base workflow orchestration framework |
| `scripts/batch_processor.py` | Parallel batch processing for large datasets |
| `scripts/notification_sender.py` | Multi-channel notifications (email, webhook) |

## Workflow Design Pattern

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   TRIGGER   │────▶│   PROCESS   │────▶│   OUTPUT    │
│ (Schedule/  │     │ (Transform/ │     │ (API/File/  │
│  Event/API) │     │  Validate)  │     │  Notify)    │
└─────────────┘     └─────────────┘     └─────────────┘
        │                   │                   │
        └───────────────────┴───────────────────┘
                    Error Handler
```

## Implementation Steps

1. **Define trigger**: Schedule (cron), event (webhook), or manual
2. **Configure data source**: Wawi API, Shop DB, or external
3. **Build processing logic**: Transform, validate, enrich
4. **Set output targets**: API calls, file exports, notifications
5. **Add error handling**: Retry logic, alerts, logging

## Best Practices

- Use `workflow_engine.py` for consistent state management
- Implement idempotency for retry-safe operations
- Log all API calls with correlation IDs
- Use batch processing for >100 items
- Store sensitive config in environment variables

## Error Handling

All workflows implement three-tier error handling:

1. **Retry**: Transient failures (network, rate limits) → exponential backoff
2. **Skip**: Item-level failures → log and continue batch
3. **Abort**: Critical failures (auth, schema) → alert and stop
