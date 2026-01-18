# Inventory Management Workflows

## Table of Contents
1. [Stock Synchronization](#stock-synchronization)
2. [Reorder Automation](#reorder-automation)
3. [Supplier Integration](#supplier-integration)
4. [Multi-Warehouse Management](#multi-warehouse-management)
5. [Stock Alerts](#stock-alerts)

## Stock Synchronization

### Wawi ↔ Shop Sync
```python
from scripts.wawi_connector import WawiConnector, WawiConfig
from scripts.batch_processor import BatchProcessor

def sync_stock_to_shop(ctx):
    """Sync JTL-Wawi stock levels to JTL-Shop."""
    connector = ctx.get("connector")
    
    # Fetch current Wawi stock
    articles = connector.get_articles(limit=1000)["data"]
    
    # Transform to shop format
    stock_updates = [
        {"sku": a["sku"], "stock": a["available_stock"]}
        for a in articles
        if a.get("sync_to_shop", True)
    ]
    
    # Batch update shop
    processor = BatchProcessor(
        process_func=lambda item: update_shop_stock(item),
        batch_size=100,
    )
    
    return processor.process(stock_updates).to_dict()
```

### Multi-Channel Stock Sync
```python
def calculate_channel_allocation(total_stock: int, channels: dict) -> dict:
    """Allocate stock across sales channels."""
    allocations = {}
    remaining = total_stock
    
    # Priority allocation: Shop > eBay > Conrad
    for channel, config in sorted(channels.items(), key=lambda x: x[1]["priority"]):
        min_stock = config.get("min_stock", 0)
        max_pct = config.get("max_percentage", 100)
        
        allocation = min(remaining, int(total_stock * max_pct / 100))
        allocation = max(allocation, min_stock) if remaining >= min_stock else 0
        
        allocations[channel] = allocation
        remaining -= allocation
    
    return allocations
```

## Reorder Automation

### Reorder Point Calculation
```python
def calculate_reorder_point(article: dict) -> dict:
    """Calculate when to reorder based on sales velocity."""
    avg_daily_sales = article.get("avg_daily_sales", 0)
    lead_time_days = article.get("supplier_lead_time", 14)
    safety_stock_days = article.get("safety_stock_days", 7)
    
    reorder_point = avg_daily_sales * (lead_time_days + safety_stock_days)
    reorder_quantity = avg_daily_sales * article.get("reorder_cover_days", 30)
    
    return {
        "sku": article["sku"],
        "reorder_point": int(reorder_point),
        "reorder_quantity": int(reorder_quantity),
        "current_stock": article["available_stock"],
        "needs_reorder": article["available_stock"] <= reorder_point,
    }
```

### Automated Reorder Workflow
```python
workflow = Workflow("auto-reorder")

workflow.add_step(FunctionStep("fetch-articles", fetch_all_articles))
workflow.add_step(FunctionStep("calculate-reorder", calculate_reorder_needs))
workflow.add_step(FunctionStep("filter-reorder", filter_needs_reorder))
workflow.add_step(FunctionStep("group-by-supplier", group_by_supplier))
workflow.add_step(FunctionStep("generate-pos", generate_purchase_orders))
workflow.add_step(FunctionStep("send-to-suppliers", send_purchase_orders))
workflow.add_step(FunctionStep("notify", send_reorder_summary))

# Run daily at 6 AM
result = workflow.run()
```

## Supplier Integration

### Supplier Stock Import
```python
def import_supplier_stock(ctx):
    """Import stock levels from supplier feeds."""
    suppliers = ctx.get("active_suppliers", [])
    updates = []
    
    for supplier in suppliers:
        if supplier["feed_type"] == "csv":
            data = fetch_csv_feed(supplier["feed_url"])
        elif supplier["feed_type"] == "api":
            data = fetch_api_feed(supplier["api_config"])
        elif supplier["feed_type"] == "ftp":
            data = fetch_ftp_feed(supplier["ftp_config"])
        
        # Map supplier SKUs to internal SKUs
        mapped = map_supplier_skus(data, supplier["sku_mapping"])
        updates.extend(mapped)
    
    ctx.set("supplier_stock_updates", updates)
    return {"suppliers": len(suppliers), "updates": len(updates)}
```

### Purchase Order Creation
```python
def create_purchase_order(supplier_id: str, items: list) -> dict:
    """Create PO in JTL-Wawi."""
    connector = get_wawi_connector()
    
    po_data = {
        "supplier_id": supplier_id,
        "items": [
            {
                "article_id": item["article_id"],
                "quantity": item["order_quantity"],
                "unit_price": item["last_purchase_price"],
            }
            for item in items
        ],
        "expected_delivery": calculate_expected_delivery(supplier_id),
    }
    
    return connector.post("/v1/purchase-orders", data=po_data)
```

## Multi-Warehouse Management

### Warehouse Configuration
```python
WAREHOUSES = {
    "main": {"id": 1, "name": "Hauptlager", "priority": 1},
    "external": {"id": 2, "name": "Außenlager", "priority": 2},
    "dropship": {"id": 3, "name": "Dropship", "priority": 3, "virtual": True},
}
```

### Cross-Warehouse Stock Check
```python
def check_availability_all_warehouses(sku: str, quantity: int) -> dict:
    """Check if quantity is available across all warehouses."""
    connector = get_wawi_connector()
    
    response = connector.get(f"/v1/articles/sku/{sku}/stock")
    if not response["success"]:
        return {"available": False, "error": response["error"]}
    
    warehouse_stocks = response["data"].get("warehouse_stocks", [])
    
    total_available = sum(w["available"] for w in warehouse_stocks)
    
    if total_available >= quantity:
        # Determine fulfillment sources
        sources = []
        remaining = quantity
        
        for wh in sorted(warehouse_stocks, key=lambda x: WAREHOUSES.get(x["id"], {}).get("priority", 99)):
            if remaining <= 0:
                break
            take = min(remaining, wh["available"])
            if take > 0:
                sources.append({"warehouse": wh["id"], "quantity": take})
                remaining -= take
        
        return {"available": True, "sources": sources}
    
    return {"available": False, "shortage": quantity - total_available}
```

## Stock Alerts

### Alert Thresholds
```python
ALERT_THRESHOLDS = {
    "critical": 0,      # Out of stock
    "low": 0.25,        # 25% of reorder point
    "warning": 0.5,     # 50% of reorder point
    "overstock": 3.0,   # 300% of target stock
}
```

### Alert Generation
```python
def generate_stock_alerts(ctx):
    """Generate alerts for stock issues."""
    articles = ctx.get("articles", [])
    alerts = []
    
    for article in articles:
        stock = article["available_stock"]
        reorder_point = article.get("reorder_point", 10)
        target_stock = article.get("target_stock", reorder_point * 2)
        
        if stock == 0:
            alerts.append({
                "sku": article["sku"],
                "level": "critical",
                "message": "Out of stock",
                "stock": stock,
            })
        elif stock < reorder_point * 0.25:
            alerts.append({
                "sku": article["sku"],
                "level": "low",
                "message": "Critically low stock",
                "stock": stock,
            })
        elif stock < reorder_point:
            alerts.append({
                "sku": article["sku"],
                "level": "warning",
                "message": "Below reorder point",
                "stock": stock,
            })
        elif stock > target_stock * 3:
            alerts.append({
                "sku": article["sku"],
                "level": "overstock",
                "message": "Excess inventory",
                "stock": stock,
            })
    
    ctx.set("stock_alerts", alerts)
    return {"alerts": len(alerts), "critical": sum(1 for a in alerts if a["level"] == "critical")}
```

### Alert Notification
```python
def send_stock_alerts(ctx):
    """Send stock alerts via configured channels."""
    alerts = ctx.get("stock_alerts", [])
    sender = ctx.get("notification_sender")
    
    # Group by severity
    critical = [a for a in alerts if a["level"] == "critical"]
    
    if critical:
        sender.send(NotificationMessage(
            title=f"🚨 {len(critical)} Products Out of Stock",
            body="Immediate attention required for stock replenishment.",
            level="error",
            metadata={"products": [a["sku"] for a in critical][:20]},
        ))
    
    # Daily summary for other alerts
    if alerts:
        sender.send(NotificationMessage(
            title="Daily Stock Alert Summary",
            body=f"{len(alerts)} stock alerts generated.",
            level="warning" if any(a["level"] in ["critical", "low"] for a in alerts) else "info",
            metadata={
                "critical": len([a for a in alerts if a["level"] == "critical"]),
                "low": len([a for a in alerts if a["level"] == "low"]),
                "warning": len([a for a in alerts if a["level"] == "warning"]),
                "overstock": len([a for a in alerts if a["level"] == "overstock"]),
            },
        ))
```
