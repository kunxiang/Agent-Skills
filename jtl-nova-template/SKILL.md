---
name: jtl-nova-template
description: "JTL-Shop 5 NOVA template customization for creating Child-Templates, SCSS theming, Smarty modifications, and professional parametric product catalogs (DigiKey-style). Use when: (1) Creating JTL-Shop Child-Templates, (2) Customizing SCSS/CSS styles, (3) Modifying Smarty templates, (4) Building switchable product views (gallery/list/table), (5) Implementing parametric filters and product comparison, (6) Exporting product lists to CSV/Excel"
---

# JTL-Shop 5 NOVA Template Development

## Quick Reference

| Task | Approach |
|------|----------|
| Change colors/fonts | Override variables in `_variables.scss` |
| Modify layout | Smarty block inheritance in `.tpl` files |
| Parametric catalog | Copy templates from `assets/templates/` |
| View switching | JavaScript class + Session storage |

## Child-Template Setup

```
templates/MyTheme/
├── Bootstrap.php          # PHP class (namespace must match folder)
├── template.xml           # Config (<Name> must match folder)
├── themes/mytheme/sass/
│   ├── _variables.scss    # Variable overrides
│   └── mytheme.scss       # Main SCSS (imports NOVA + custom)
└── productlist/           # Template overrides
```

### template.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<Template isFullResponsive="true">
    <Name>MyTheme</Name>
    <Parent>NOVA</Parent>
    <Author>Your Name</Author>
    <Version>1.0.0</Version>
    <ShopVersion>5.0.0</ShopVersion>
</Template>
```

### Bootstrap.php
```php
<?php
declare(strict_types=1);
namespace Template\MyTheme;  // Must match folder name

class Bootstrap extends \Template\NOVA\Bootstrap
{
    public function boot(): void
    {
        parent::boot();  // Always call parent first
        // Register custom Smarty functions here
    }
}
```

### SCSS Structure
```scss
// mytheme.scss
@import "~bootstrap/scss/functions";
@import "variables";  // Your overrides
@import "~templates/NOVA/themes/base/sass/allstyles";
// Custom styles below
```

Compile via: Backend → Plugins → Theme Editor → Select theme → Compile

## Smarty Block Inheritance

```smarty
{extends file="{$parent_template_path}/productlist/index.tpl"}

{block name="productlist"}
    {* Replace block content *}
{/block}

{block name="head-resources" append}
    {* Append to block *}
{/block}
```

## Parametric Product Catalog

For DigiKey-style catalog with switchable views (gallery/list/table):

1. Copy templates from `assets/templates/productlist/`
2. Copy `assets/js/parametric-catalog.js`
3. Copy `assets/themes/_parametric-catalog.scss`
4. Add IO handler to Bootstrap.php for view persistence

### View Switching Core

```javascript
// Switch view (gallery | list | table)
switchView(view) {
    document.querySelectorAll('.catalog-view').forEach(v => v.style.display = 'none');
    document.querySelector(`.view-${view}`).style.display = '';
    fetch('/io.php', { method: 'POST', body: `io={"name":"setCatalogView","params":["${view}"]}` });
}
```

```php
// Bootstrap.php - Save view to session
if ($_POST['io'] ?? false) {
    $io = json_decode($_POST['io'], true);
    if ($io['name'] === 'setCatalogView') {
        $_SESSION['catalogView'] = $io['params'][0];
        echo json_encode(['success' => true]);
        exit;
    }
}
```

### Key Features

- **Gallery**: Card grid, large images
- **List**: Horizontal layout with 6 parameters
- **Table**: Full parameters, sortable columns, export to CSV/Excel
- **Filters**: Multi-select dropdowns with search
- **Compare**: Select up to 4 products
- **Keyboard**: Alt+1/2/3 to switch views

## References

- **SCSS Variables**: See `references/scss-variables.md` for Bootstrap/NOVA variable reference
- **Smarty Blocks**: See `references/smarty-blocks.md` for available blocks
- **Catalog Implementation**: See `references/parametric-catalog.md` for complete code

## Assets

- `assets/templates/productlist/` - Ready-to-use template files
- `assets/js/parametric-catalog.js` - JavaScript functionality
- `assets/themes/_parametric-catalog.scss` - Catalog styles
- `assets/Bootstrap.php` - PHP with IO handlers and export
