# Reporting & Analytics Workflows

## Table of Contents
1. [Scheduled Reports](#scheduled-reports)
2. [KPI Dashboards](#kpi-dashboards)
3. [Export Automation](#export-automation)
4. [Data Aggregation](#data-aggregation)

## Scheduled Reports

### Report Configuration
```python
REPORT_SCHEDULES = {
    "daily_sales": {
        "cron": "0 7 * * *",  # 7 AM daily
        "recipients": ["sales@eckstein.de"],
        "format": "xlsx",
    },
    "weekly_inventory": {
        "cron": "0 8 * * 1",  # 8 AM Monday
        "recipients": ["warehouse@eckstein.de"],
        "format": "xlsx",
    },
    "monthly_performance": {
        "cron": "0 9 1 * *",  # 9 AM first of month
        "recipients": ["management@eckstein.de"],
        "format": "pdf",
    },
}
```

### Daily Sales Report
```python
def generate_daily_sales_report(ctx):
    """Generate daily sales summary."""
    connector = ctx.get("connector")
    date = ctx.get("report_date", datetime.now().date())
    
    orders = connector.get_orders(
        created_after=f"{date}T00:00:00",
        created_before=f"{date}T23:59:59",
    )["data"]
    
    total_revenue = sum(o["total_gross"] for o in orders)
    total_orders = len(orders)
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
    
    # Channel breakdown
    by_channel = {}
    for order in orders:
        channel = order.get("source_channel", "unknown")
        if channel not in by_channel:
            by_channel[channel] = {"count": 0, "revenue": 0}
        by_channel[channel]["count"] += 1
        by_channel[channel]["revenue"] += order["total_gross"]
    
    return {
        "date": str(date),
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "avg_order_value": avg_order_value,
        "by_channel": by_channel,
    }
```

## KPI Dashboards

### Core KPIs
```python
def calculate_kpis(ctx):
    """Calculate key performance indicators."""
    connector = ctx.get("connector")
    start_date, end_date = ctx.get("period_dates")
    
    orders = fetch_orders_in_period(connector, start_date, end_date)
    prev_start, prev_end = get_previous_period(start_date, end_date)
    previous_orders = fetch_orders_in_period(connector, prev_start, prev_end)
    
    kpis = {
        "revenue": {
            "current": sum(o["total_gross"] for o in orders),
            "previous": sum(o["total_gross"] for o in previous_orders),
        },
        "orders": {
            "current": len(orders),
            "previous": len(previous_orders),
        },
        "aov": {
            "current": sum(o["total_gross"] for o in orders) / max(len(orders), 1),
            "previous": sum(o["total_gross"] for o in previous_orders) / max(len(previous_orders), 1),
        },
    }
    
    # Calculate changes
    for kpi_name, values in kpis.items():
        prev = values["previous"] or 1
        values["change_pct"] = ((values["current"] - values["previous"]) / prev) * 100
    
    return kpis
```

## Export Automation

### Excel Export
```python
def export_to_excel(data: list, columns: list, filename: str) -> str:
    """Export data to Excel file."""
    import openpyxl
    from openpyxl.styles import Font, PatternFill
    
    wb = openpyxl.Workbook()
    ws = wb.active
    
    header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
    header_font = Font(color="FFFFFF", bold=True)
    
    for col_idx, col_name in enumerate(columns, 1):
        cell = ws.cell(row=1, column=col_idx, value=col_name)
        cell.fill = header_fill
        cell.font = header_font
    
    for row_idx, record in enumerate(data, 2):
        for col_idx, col_name in enumerate(columns, 1):
            ws.cell(row=row_idx, column=col_idx, value=record.get(col_name, ""))
    
    filepath = f"/tmp/{filename}"
    wb.save(filepath)
    return filepath
```

### CSV Export
```python
def export_to_csv(data: list, columns: list, filename: str) -> str:
    """Export data to CSV for external systems."""
    import csv
    
    filepath = f"/tmp/{filename}"
    with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=columns, delimiter=";")
        writer.writeheader()
        writer.writerows(data)
    return filepath
```

## Data Aggregation

### Time-Series Aggregation
```python
def aggregate_by_period(data: list, date_field: str, value_field: str, period: str = "day") -> list:
    """Aggregate data by time period."""
    from collections import defaultdict
    
    aggregated = defaultdict(lambda: {"count": 0, "sum": 0})
    
    for record in data:
        date = parse_date(record[date_field])
        if period == "day":
            key = date.strftime("%Y-%m-%d")
        elif period == "week":
            key = date.strftime("%Y-W%W")
        elif period == "month":
            key = date.strftime("%Y-%m")
        
        aggregated[key]["count"] += 1
        aggregated[key]["sum"] += record.get(value_field, 0)
    
    return [
        {"period": k, "count": v["count"], "sum": v["sum"], "avg": v["sum"] / v["count"]}
        for k, v in sorted(aggregated.items())
    ]
```

### Period Comparison
```python
def calculate_period_comparison(current: dict, previous: dict) -> dict:
    """Calculate period-over-period comparison."""
    comparison = {}
    for key in current:
        if key in previous and isinstance(current[key], (int, float)):
            change = current[key] - previous[key]
            change_pct = (change / previous[key] * 100) if previous[key] != 0 else 0
            comparison[key] = {
                "current": current[key],
                "previous": previous[key],
                "change": change,
                "change_pct": round(change_pct, 2),
            }
    return comparison
```
