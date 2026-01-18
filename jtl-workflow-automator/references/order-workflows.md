# Order Processing Workflows

## Table of Contents
1. [Order Import](#order-import)
2. [Order Validation](#order-validation)
3. [Fulfillment Pipeline](#fulfillment-pipeline)
4. [Multi-Channel Sync](#multi-channel-sync)
5. [Return Processing](#return-processing)

## Order Import

### From JTL-Shop
```python
from scripts.wawi_connector import WawiConnector, WawiConfig
from scripts.workflow_engine import Workflow, FunctionStep, WorkflowContext

def fetch_shop_orders(ctx: WorkflowContext):
    """Fetch new orders from JTL-Shop."""
    connector = ctx.get("connector")
    last_sync = ctx.get("last_sync_time")
    
    response = connector.get_orders(status="new", since=last_sync)
    if response["success"]:
        ctx.set("orders", response["data"])
        return {"count": len(response["data"])}
    raise Exception(response["error"])
```

### From External Channels (eBay, Conrad)
```python
def import_marketplace_orders(ctx: WorkflowContext):
    """Import orders from marketplace APIs."""
    orders = []
    
    # eBay orders
    ebay_orders = fetch_ebay_orders(ctx.get("ebay_config"))
    orders.extend(transform_ebay_orders(ebay_orders))
    
    # Conrad orders
    conrad_orders = fetch_conrad_orders(ctx.get("conrad_config"))
    orders.extend(transform_conrad_orders(conrad_orders))
    
    ctx.set("imported_orders", orders)
    return {"total": len(orders)}
```

## Order Validation

### Validation Rules
Apply these checks before processing:

1. **Customer validation**: Verify customer exists or create new
2. **Address validation**: Check shipping address completeness
3. **Stock validation**: Ensure items are available
4. **Price validation**: Verify prices match current catalog
5. **Payment validation**: Confirm payment status

```python
def validate_order(order: dict) -> dict:
    """Validate single order, return issues."""
    issues = []
    
    if not order.get("shipping_address", {}).get("postal_code"):
        issues.append("Missing postal code")
    
    if order.get("total", 0) <= 0:
        issues.append("Invalid order total")
    
    for item in order.get("items", []):
        if item.get("quantity", 0) <= 0:
            issues.append(f"Invalid quantity for {item.get('sku')}")
    
    return {"valid": len(issues) == 0, "issues": issues}
```

## Fulfillment Pipeline

### Standard Flow
```
New Order → Validate → Reserve Stock → Pick → Pack → Ship → Complete
```

### Workflow Implementation
```python
workflow = Workflow("order-fulfillment", fail_fast=False)

workflow.add_step(FunctionStep("fetch-orders", fetch_pending_orders))
workflow.add_step(FunctionStep("validate", validate_orders_batch))
workflow.add_step(FunctionStep("reserve-stock", reserve_inventory))
workflow.add_step(FunctionStep("generate-picklist", create_picklist))
workflow.add_step(FunctionStep("update-status", mark_orders_processing))
workflow.add_step(FunctionStep("notify", send_fulfillment_notifications))

result = workflow.run({"date": "today"})
```

### Status Transitions
| From | To | Trigger |
|------|-----|---------|
| new | validated | Validation pass |
| validated | processing | Stock reserved |
| processing | shipped | Tracking uploaded |
| shipped | completed | Delivery confirmed |

## Multi-Channel Sync

### Sync Order Status Back to Channels
```python
def sync_order_status_to_channels(ctx: WorkflowContext):
    """Push order status updates to sales channels."""
    orders = ctx.get("updated_orders", [])
    
    for order in orders:
        channel = order.get("source_channel")
        
        if channel == "ebay":
            update_ebay_order_status(order)
        elif channel == "conrad":
            update_conrad_order_status(order)
        elif channel == "shop":
            # JTL-Shop syncs automatically
            pass
    
    return {"synced": len(orders)}
```

## Return Processing

### RMA Workflow
```
Return Request → Validate → Approve → Receive → Inspect → Restock/Dispose → Refund
```

```python
def process_return(ctx: WorkflowContext):
    """Handle return merchandise authorization."""
    return_request = ctx.get("return_request")
    original_order = ctx.get("original_order")
    
    # Validate return eligibility
    if not is_returnable(original_order):
        return {"approved": False, "reason": "Return period expired"}
    
    # Create RMA
    rma = create_rma(return_request, original_order)
    ctx.set("rma", rma)
    
    return {"approved": True, "rma_number": rma["number"]}
```

## Error Handling Patterns

### Retry Logic for Order Operations
```python
from scripts.batch_processor import BatchProcessor

processor = BatchProcessor(
    process_func=process_single_order,
    batch_size=50,
    max_workers=4,
    max_retries=3,
    retry_delay=2.0,
)

result = processor.process(orders)
if result.failed > 0:
    # Queue failed orders for manual review
    queue_for_review([i.item for i in result.items if i.status == "failed"])
```

### Notification on Failure
```python
from scripts.notification_sender import NotificationSender, NotificationMessage

if result.failed > 0:
    sender.send(NotificationMessage(
        title="Order Processing Errors",
        body=f"{result.failed} orders failed to process",
        level="error",
        metadata={"failed_orders": [o["id"] for o in failed_orders][:20]},
    ))
```
