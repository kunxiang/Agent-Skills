# Product Data Workflows

## Table of Contents
1. [Product Enrichment](#product-enrichment)
2. [Channel Sync](#channel-sync)
3. [Categorization](#categorization)
4. [Pricing Automation](#pricing-automation)
5. [Image Processing](#image-processing)

## Product Enrichment

### AI-Powered Description Generation
```python
def enrich_product_descriptions(ctx):
    """Generate/enhance product descriptions using AI."""
    products = ctx.get("products_needing_enrichment", [])
    ai_client = ctx.get("ai_client")
    
    enriched = []
    for product in products:
        # Build prompt from existing data
        prompt = f"""
        Generate a professional German product description for:
        Name: {product['name']}
        Category: {product.get('category', 'Electronics')}
        Technical specs: {product.get('specs', {})}
        
        Requirements:
        - SEO optimized
        - Professional tone
        - Highlight key features
        - Max 200 words
        """
        
        description = ai_client.generate(prompt)
        
        enriched.append({
            "article_id": product["id"],
            "description_de": description,
            "enriched_at": datetime.now().isoformat(),
        })
    
    ctx.set("enriched_products", enriched)
    return {"enriched": len(enriched)}
```

### Attribute Extraction from Supplier Data
```python
def extract_product_attributes(product: dict, category_schema: dict) -> dict:
    """Extract structured attributes from unstructured product data."""
    extracted = {}
    
    # Parse technical specs from name/description
    text = f"{product.get('name', '')} {product.get('description', '')}"
    
    for attr_name, patterns in category_schema.get("patterns", {}).items():
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                extracted[attr_name] = match.group(1)
                break
    
    return extracted


# Example patterns for electronics
ELECTRONICS_PATTERNS = {
    "voltage": [r"(\d+(?:\.\d+)?)\s*V(?:olt)?", r"Spannung[:\s]+(\d+(?:\.\d+)?)\s*V"],
    "current": [r"(\d+(?:\.\d+)?)\s*(?:m)?A(?:mp)?", r"Strom[:\s]+(\d+(?:\.\d+)?)\s*(?:m)?A"],
    "power": [r"(\d+(?:\.\d+)?)\s*W(?:att)?", r"Leistung[:\s]+(\d+(?:\.\d+)?)\s*W"],
    "dimensions": [r"(\d+(?:\.\d+)?\s*x\s*\d+(?:\.\d+)?\s*x\s*\d+(?:\.\d+)?)\s*mm"],
}
```

## Channel Sync

### Product Data Mapping
```python
CHANNEL_MAPPINGS = {
    "ebay": {
        "title": lambda p: p["name"][:80],  # eBay title limit
        "description": lambda p: format_ebay_description(p),
        "price": lambda p: p["gross_price"],
        "quantity": lambda p: p["available_stock"],
        "ean": lambda p: p.get("ean", ""),
        "category_id": lambda p: map_to_ebay_category(p["category"]),
    },
    "conrad": {
        "article_name": lambda p: p["name"],
        "long_description": lambda p: p["description_de"],
        "price_net": lambda p: p["net_price"],
        "stock": lambda p: p["available_stock"],
        "gtin": lambda p: p.get("ean", ""),
    },
}


def transform_for_channel(product: dict, channel: str) -> dict:
    """Transform product data for specific sales channel."""
    mapping = CHANNEL_MAPPINGS.get(channel, {})
    
    return {
        target_field: transformer(product)
        for target_field, transformer in mapping.items()
    }
```

### Sync Workflow
```python
def sync_products_to_channel(ctx):
    """Sync product updates to sales channel."""
    products = ctx.get("modified_products", [])
    channel = ctx.get("target_channel")
    
    transformed = [transform_for_channel(p, channel) for p in products]
    
    processor = BatchProcessor(
        process_func=lambda p: push_to_channel(p, channel),
        batch_size=50,
        max_retries=3,
    )
    
    result = processor.process(transformed)
    
    return {
        "channel": channel,
        "synced": result.succeeded,
        "failed": result.failed,
    }
```

## Categorization

### Auto-Categorization Rules
```python
CATEGORY_RULES = [
    {
        "pattern": r"(?:raspberry|rpi)\s*(?:pi)?\s*(?:hat|shield)",
        "category": "Raspberry Pi > HATs & Add-ons",
        "priority": 10,
    },
    {
        "pattern": r"sensor.*breakout|breakout.*sensor",
        "category": "Sensors > Breakout Boards",
        "priority": 10,
    },
    {
        "pattern": r"motor.*driver|treiber.*motor",
        "category": "Motors > Drivers",
        "priority": 10,
    },
    {
        "pattern": r"arduino.*(?:shield|board)",
        "category": "Arduino > Shields",
        "priority": 5,
    },
]


def auto_categorize(product: dict) -> str:
    """Determine product category based on rules."""
    text = f"{product.get('name', '')} {product.get('description', '')}".lower()
    
    matches = []
    for rule in CATEGORY_RULES:
        if re.search(rule["pattern"], text, re.IGNORECASE):
            matches.append((rule["priority"], rule["category"]))
    
    if matches:
        # Return highest priority match
        return sorted(matches, reverse=True)[0][1]
    
    return "Uncategorized"
```

### Category Hierarchy Management
```python
def ensure_category_path(connector, category_path: str) -> int:
    """Create category hierarchy if needed, return leaf category ID."""
    parts = [p.strip() for p in category_path.split(">")]
    parent_id = None
    
    for part in parts:
        # Check if exists
        existing = connector.get("/v1/categories", params={
            "name": part,
            "parent_id": parent_id or "null",
        })
        
        if existing["data"]:
            parent_id = existing["data"][0]["id"]
        else:
            # Create new category
            new_cat = connector.post("/v1/categories", data={
                "name": part,
                "parent_id": parent_id,
            })
            parent_id = new_cat["data"]["id"]
    
    return parent_id
```

## Pricing Automation

### Dynamic Pricing Rules
```python
PRICING_RULES = {
    "margin_floor": 0.15,  # Minimum 15% margin
    "market_adjustment": True,
    "competitor_tracking": True,
    "bulk_discounts": [
        {"min_qty": 10, "discount": 0.05},
        {"min_qty": 50, "discount": 0.10},
        {"min_qty": 100, "discount": 0.15},
    ],
}


def calculate_selling_price(product: dict, rules: dict = PRICING_RULES) -> dict:
    """Calculate optimal selling price."""
    cost = product["purchase_price"]
    min_margin = rules["margin_floor"]
    
    # Base price with minimum margin
    base_price = cost / (1 - min_margin)
    
    # Round to .99 pricing
    base_price = round(base_price) - 0.01
    
    # Calculate bulk prices
    bulk_prices = {}
    for tier in rules.get("bulk_discounts", []):
        bulk_prices[f"qty_{tier['min_qty']}"] = round(base_price * (1 - tier["discount"]), 2)
    
    return {
        "base_price": base_price,
        "bulk_prices": bulk_prices,
        "margin_at_base": (base_price - cost) / base_price,
    }
```

### Price Update Workflow
```python
workflow = Workflow("price-update")

workflow.add_step(FunctionStep("fetch-cost-updates", fetch_updated_costs))
workflow.add_step(FunctionStep("calculate-prices", calculate_new_prices))
workflow.add_step(FunctionStep("validate-margins", validate_margin_requirements))
workflow.add_step(FunctionStep("apply-to-wawi", update_wawi_prices))
workflow.add_step(FunctionStep("sync-channels", sync_prices_to_channels))
workflow.add_step(FunctionStep("notify-changes", send_price_change_report))

result = workflow.run()
```

## Image Processing

### Image Optimization Pipeline
```python
def process_product_images(ctx):
    """Optimize and resize product images for different channels."""
    products = ctx.get("products_with_new_images", [])
    
    IMAGE_SIZES = {
        "thumbnail": (150, 150),
        "listing": (500, 500),
        "detail": (1200, 1200),
        "zoom": (2000, 2000),
    }
    
    processed = []
    for product in products:
        for image_url in product.get("raw_images", []):
            image = download_image(image_url)
            
            variants = {}
            for size_name, dimensions in IMAGE_SIZES.items():
                resized = resize_image(image, dimensions)
                optimized = optimize_image(resized, quality=85)
                
                # Upload to CDN
                cdn_url = upload_to_cdn(optimized, f"{product['sku']}_{size_name}.jpg")
                variants[size_name] = cdn_url
            
            processed.append({
                "sku": product["sku"],
                "original": image_url,
                "variants": variants,
            })
    
    ctx.set("processed_images", processed)
    return {"processed": len(processed)}
```

### Image Validation
```python
def validate_product_images(product: dict) -> list:
    """Validate product images meet requirements."""
    issues = []
    
    images = product.get("images", [])
    
    if not images:
        issues.append("No product images")
        return issues
    
    main_image = images[0]
    
    # Check main image requirements
    if main_image.get("width", 0) < 1000:
        issues.append("Main image width < 1000px")
    
    if main_image.get("height", 0) < 1000:
        issues.append("Main image height < 1000px")
    
    # Check for white background (for eBay)
    if not main_image.get("has_white_background", False):
        issues.append("Main image should have white background")
    
    return issues
```
