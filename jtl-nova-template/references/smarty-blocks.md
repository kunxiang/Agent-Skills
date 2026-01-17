# Smarty Blocks Reference

## Block Inheritance

```smarty
{extends file="{$parent_template_path}/layout/index.tpl"}

{block name="blockname"}...{/block}           {* Replace *}
{block name="blockname" append}...{/block}    {* Append *}
{block name="blockname" prepend}...{/block}   {* Prepend *}
```

## Layout Blocks

### Header (`layout/header.tpl`)
| Block | Content |
|-------|---------|
| `head-meta` | Meta tags |
| `head-title` | Page title |
| `head-resources` | CSS/JS links |
| `header` | Full header |
| `header-top-bar` | Top bar (contact, language) |
| `header-branding` | Logo area |
| `header-search` | Search form |
| `header-nav` | Main navigation |

### Footer (`layout/footer.tpl`)
| Block | Content |
|-------|---------|
| `footer` | Full footer |
| `footer-content` | Footer columns |
| `footer-newsletter` | Newsletter signup |
| `footer-payment` | Payment icons |
| `footer-copyright` | Copyright |

### Sidebar (`snippets/sidebar.tpl`)
| Block | Content |
|-------|---------|
| `sidebar` | Full sidebar |
| `sidebar-categories` | Category tree |
| `sidebar-filter` | Product filters |

## Product List Blocks (`productlist/index.tpl`)

| Block | Content |
|-------|---------|
| `productlist` | Full product listing |
| `productlist-header` | Category title, description |
| `productlist-sorting` | Sort dropdown |
| `productlist-filters` | Filter options |
| `productlist-products` | Product grid/list |
| `productlist-pagination` | Page navigation |
| `productlist-item` | Single product card |

## Product Detail Blocks (`productdetails/index.tpl`)

| Block | Content |
|-------|---------|
| `product-detail` | Full detail page |
| `product-image` | Main image + gallery |
| `product-info` | Name, price, buy form |
| `product-buy-form` | Add to cart form |
| `product-variations` | Variant selectors |
| `product-price` | Price display |
| `product-stock` | Availability |
| `product-attributes` | Specifications table |
| `product-description` | Long description |
| `product-reviews` | Customer reviews |
| `product-related` | Related products |

## Checkout Blocks (`checkout/index.tpl`)

| Block | Content |
|-------|---------|
| `checkout-steps` | Step indicators |
| `checkout-address` | Address forms |
| `checkout-shipping` | Shipping options |
| `checkout-payment` | Payment methods |
| `checkout-summary` | Order summary |
| `checkout-confirm` | Confirm button |

## Account Blocks (`account/index.tpl`)

| Block | Content |
|-------|---------|
| `account-dashboard` | Account overview |
| `account-orders` | Order history |
| `account-addresses` | Saved addresses |
| `account-wishlist` | Wishlist |

## Basket Blocks (`basket/index.tpl`)

| Block | Content |
|-------|---------|
| `basket-items` | Cart items table |
| `basket-item` | Single cart item |
| `basket-totals` | Subtotals, shipping, total |
| `basket-coupon` | Coupon input |
| `basket-actions` | Update/checkout buttons |

## Common Variables

| Variable | Description |
|----------|-------------|
| `$Artikel` | Product object |
| `$Kategorie` | Category object |
| `$Suchergebnisse` | Search/listing results |
| `$ShopURL` | Shop base URL |
| `$Einstellungen` | Shop settings |
| `$smarty.session` | Session data |

## Usage Examples

### Replace block
```smarty
{block name="header-branding"}
    <a href="{$ShopURL}" class="custom-logo">
        <img src="{$ShopURL}/templates/{$template->getName()}/img/logo.svg" alt="Logo">
    </a>
{/block}
```

### Append to block
```smarty
{block name="head-resources" append}
    <link rel="stylesheet" href="{$ShopURL}/templates/{$template->getName()}/custom.css">
    <script src="{$ShopURL}/templates/{$template->getName()}/js/custom.js" defer></script>
{/block}
```

### Conditional override
```smarty
{block name="product-price"}
    {if $Artikel->Preise->rabatt > 0}
        <span class="price-sale">{$Artikel->Preise->cVKLocalized[0]}</span>
        <span class="price-old">{$Artikel->Preise->cAufpreisLocalized[0]}</span>
    {else}
        {$smarty.block.parent}
    {/if}
{/block}
```

### JavaScript in templates
```smarty
{inline_script}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Your code
    });
</script>
{/inline_script}
```

### JavaScript in footer (empfohlen)
```smarty
{extends file="{$parent_template_path}/layout/footer.tpl"}

{block name='layout-footer-js' append}
    <script src="{$ShopURL}/templates/{$template->getName()}/js/custom.js" async></script>
{/block}
```

## Plugin-basierte Block-Überschreibung

Blöcke können auch über Plugins überschrieben werden (ohne Child-Template):

```
<plugin-verzeichnis>/
└── frontend/
    └── templates/
        └── productdetails/
            └── variation.tpl
```

**variation.tpl**:
```smarty
{block name="product-variations" append}
    {* Plugin-spezifische Erweiterung *}
{/block}
```

**Vorteile**:
- Änderungen bleiben bei Template-Updates erhalten
- Mehrere Plugins können denselben Block erweitern
- Keine Konflikte mit Child-Templates

**Hinweis**: Plugin-Erweiterungen werden nach Child-Template-Erweiterungen geladen.
