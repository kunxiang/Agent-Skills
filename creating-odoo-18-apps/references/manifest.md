# Odoo 18 Module Manifest Reference

The `__manifest__.py` file declares a Python package as an Odoo module and specifies module metadata.

## Required Fields

```python
{
    'name': 'Module Name',      # Human-readable name (required)
    'version': '18.0.1.0.0',    # Version string
    'depends': ['base'],        # List of dependencies
}
```

## All Manifest Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | str | **Required**. Human-readable module name |
| `version` | str | Module version (format: `ODOO.MAJOR.MINOR.PATCH`) |
| `depends` | list | Required module dependencies |
| `category` | str | Module category for Apps menu |
| `summary` | str | Short one-line description |
| `description` | str | Long description (reStructuredText) |
| `author` | str | Author name or company |
| `website` | str | Author's website URL |
| `license` | str | License identifier (LGPL-3, AGPL-3, etc.) |
| `data` | list | Data files to load on install/update |
| `demo` | list | Demo data files (only in demo mode) |
| `assets` | dict | Static asset bundles |
| `installable` | bool | Whether module can be installed (default: True) |
| `application` | bool | Show as App in Apps menu |
| `auto_install` | bool | Auto-install when all dependencies met |
| `external_dependencies` | dict | Python/binary dependencies |
| `maintainer` | str | Maintainer (defaults to author) |
| `pre_init_hook` | str | Function to call before install |
| `post_init_hook` | str | Function to call after install |
| `uninstall_hook` | str | Function to call on uninstall |
| `post_load` | str | Function to call when server loads module |

## Complete Example

```python
{
    'name': 'Real Estate',
    'version': '18.0.1.0.0',
    'category': 'Real Estate/Brokerage',
    'summary': 'Manage real estate properties',
    'description': """
Real Estate Management
======================

This module allows you to manage:
* Properties (houses, apartments)
* Property offers
* Property types and tags
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mail',
    ],
    'data': [
        # Security first
        'security/estate_security.xml',
        'security/ir.model.access.csv',
        # Views
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        # Data
        'data/estate_data.xml',
        # Reports
        'report/estate_report.xml',
    ],
    'demo': [
        'demo/estate_demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'estate/static/src/js/**/*',
            'estate/static/src/css/**/*',
            'estate/static/src/xml/**/*',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'external_dependencies': {
        'python': ['xlrd', 'xlwt'],
        'bin': ['wkhtmltopdf'],
    },
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
}
```

## Category Examples

Common categories (can use `/` for hierarchy):

```python
'category': 'Accounting'
'category': 'Sales/CRM'
'category': 'Inventory/Warehouse'
'category': 'Human Resources'
'category': 'Manufacturing'
'category': 'Project'
'category': 'Website'
'category': 'Services'
'category': 'Technical'
```

## License Options

| License | Description |
|---------|-------------|
| `LGPL-3` | Lesser GPL v3 (recommended for commercial) |
| `AGPL-3` | Affero GPL v3 (community standard) |
| `GPL-3` | GNU GPL v3 |
| `Other proprietary` | Proprietary license |
| `OEEL-1` | Odoo Enterprise Edition License |

## Data File Loading Order

Files in `data` list are loaded in order. Recommended sequence:

1. **Security groups** (`security/security.xml`)
2. **Access control** (`security/ir.model.access.csv`)
3. **Record rules** (`security/rules.xml`)
4. **Views** (`views/*.xml`)
5. **Actions and menus** (`views/menus.xml`)
6. **Data records** (`data/*.xml`)
7. **Reports** (`report/*.xml`)
8. **Wizards** (`wizard/*.xml`)

## Assets Bundle

```python
'assets': {
    'web.assets_backend': [
        'module_name/static/src/js/my_widget.js',
        'module_name/static/src/css/my_styles.css',
        'module_name/static/src/xml/my_templates.xml',
    ],
    'web.assets_frontend': [
        'module_name/static/src/js/portal.js',
    ],
    'web.report_assets_common': [
        'module_name/static/src/css/report.css',
    ],
}
```

## External Dependencies

```python
'external_dependencies': {
    'python': [
        'xlrd',           # Excel reading
        'xlwt',           # Excel writing
        'phonenumbers',   # Phone validation
    ],
    'bin': [
        'wkhtmltopdf',    # PDF generation
        'lessc',          # LESS compilation
    ],
}
```

## Hooks

**`__init__.py`** (at module root):

```python
from . import models
from . import controllers
from . import wizard

def post_init_hook(env):
    """Called after module installation."""
    env['res.partner'].search([]).write({'active': True})

def uninstall_hook(env):
    """Called before module uninstallation."""
    env['my.model'].search([]).unlink()
```

## Version Convention

Format: `ODOO_VERSION.MODULE_VERSION`

```
18.0.1.0.0
│   │ │ │
│   │ │ └── Patch (bug fixes)
│   │ └──── Minor (new features, backward compatible)
│   └────── Major (breaking changes)
└────────── Odoo version
```

## Depends Best Practices

1. Always include `base` (even if implicit)
2. Only include direct dependencies
3. Order alphabetically for readability

```python
'depends': [
    'base',
    'mail',
    'sale',
    'stock',
],
```

## Common Patterns

### Technical Module (Hidden)

```python
{
    'name': 'Technical Helper',
    'application': False,
    'installable': True,
    'auto_install': False,
}
```

### Glue Module (Auto-Install)

```python
{
    'name': 'Sale Stock Integration',
    'depends': ['sale', 'stock'],
    'auto_install': True,  # Installs when both sale and stock are installed
    'application': False,
}
```

### Localization Module

```python
{
    'name': 'Germany - Accounting',
    'category': 'Accounting/Localizations',
    'depends': ['account'],
    'application': False,
}
```
