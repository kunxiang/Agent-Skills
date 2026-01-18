---
name: creating-odoo-18-apps
description: "Creates Odoo 18 modules/addons with proper structure, models, views, and security. Use when: (1) building new Odoo 18 applications, (2) creating custom modules for Odoo ERP, (3) developing Odoo addons with models and views, (4) user mentions Odoo, ERP module, or addon development."
---

# Creating Odoo 18 Apps

## Quick Reference

| Task | Approach | Reference |
|------|----------|-----------|
| Module structure | Create standard addon layout | See Directory Structure |
| Manifest file | Define `__manifest__.py` | [references/manifest.md](references/manifest.md) |
| Models & Fields | Python ORM classes | [references/models.md](references/models.md) |
| Views & Menus | XML view definitions | [references/views.md](references/views.md) |
| Security | Access control lists | [references/security.md](references/security.md) |

## Directory Structure

```
my_module/
├── __init__.py              # Python package init
├── __manifest__.py          # Module manifest (required)
├── models/
│   ├── __init__.py
│   └── my_model.py          # Business logic
├── views/
│   └── my_model_views.xml   # UI definitions
├── security/
│   ├── ir.model.access.csv  # Access control list
│   └── security.xml         # Record rules (optional)
├── data/
│   └── data.xml             # Default data
├── demo/
│   └── demo.xml             # Demo data
├── controllers/
│   ├── __init__.py
│   └── main.py              # Web controllers
├── static/
│   ├── description/
│   │   └── icon.png         # Module icon (128x128)
│   └── src/
│       ├── js/
│       ├── css/
│       └── xml/             # QWeb templates
├── wizard/                  # Transient models
├── report/                  # Report definitions
└── i18n/                    # Translations
```

## Core Workflow

### Phase 1: Create Module Structure

1. Create module directory in `addons/` or custom addons path
2. Create `__manifest__.py` with required metadata
3. Create `__init__.py` files for Python packages
4. Add module icon at `static/description/icon.png`

### Phase 2: Define Models

1. Create model class extending `models.Model`
2. Define `_name` attribute (technical name)
3. Add fields with appropriate types
4. Implement business logic methods

### Phase 3: Create Views

1. Define tree (list) view
2. Define form view
3. Create action window
4. Add menu items

### Phase 4: Configure Security

1. Create `security/ir.model.access.csv`
2. Grant CRUD permissions per group
3. Add record rules if needed

### Phase 5: Install & Test

```bash
# Restart Odoo with module update
./odoo-bin -u my_module -d mydb

# Or install via Apps menu (enable developer mode)
```

## Quick Start Example

### Minimal Module

**`__manifest__.py`**:
```python
{
    'name': 'My Module',
    'version': '18.0.1.0.0',
    'category': 'Services',
    'summary': 'Short description',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/my_model_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
```

**`models/__init__.py`**:
```python
from . import my_model
```

**`models/my_model.py`**:
```python
from odoo import models, fields, api

class MyModel(models.Model):
    _name = 'my.model'
    _description = 'My Model'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
    ], default='draft')
    date = fields.Date(string='Date')
    partner_id = fields.Many2one('res.partner', string='Partner')
```

**`security/ir.model.access.csv`**:
```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_my_model_user,my.model.user,model_my_model,base.group_user,1,1,1,1
```

**`views/my_model_views.xml`**:
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Tree View -->
    <record id="my_model_view_tree" model="ir.ui.view">
        <field name="name">my.model.tree</field>
        <field name="model">my.model</field>
        <field name="arch" type="xml">
            <tree>
                <field name="name"/>
                <field name="partner_id"/>
                <field name="state"/>
                <field name="date"/>
            </tree>
        </field>
    </record>

    <!-- Form View -->
    <record id="my_model_view_form" model="ir.ui.view">
        <field name="name">my.model.form</field>
        <field name="model">my.model</field>
        <field name="arch" type="xml">
            <form>
                <header>
                    <field name="state" widget="statusbar"/>
                </header>
                <sheet>
                    <group>
                        <group>
                            <field name="name"/>
                            <field name="partner_id"/>
                        </group>
                        <group>
                            <field name="date"/>
                            <field name="active"/>
                        </group>
                    </group>
                    <notebook>
                        <page string="Description">
                            <field name="description"/>
                        </page>
                    </notebook>
                </sheet>
            </form>
        </field>
    </record>

    <!-- Action -->
    <record id="my_model_action" model="ir.actions.act_window">
        <field name="name">My Records</field>
        <field name="res_model">my.model</field>
        <field name="view_mode">tree,form</field>
    </record>

    <!-- Menu -->
    <menuitem id="my_module_menu_root" name="My Module" sequence="10"/>
    <menuitem id="my_model_menu" name="My Records"
              parent="my_module_menu_root"
              action="my_model_action" sequence="10"/>
</odoo>
```

## Key Concepts

### Version Numbering

Format: `ODOO_VERSION.MODULE_VERSION` (e.g., `18.0.1.0.0`)

### Common Dependencies

| Module | Use Case |
|--------|----------|
| `base` | Core models (res.partner, res.users) |
| `mail` | Chatter, messaging, activity |
| `web` | Web client features |
| `sale` | Sales functionality |
| `purchase` | Purchase management |
| `stock` | Inventory management |
| `account` | Accounting features |

### Reserved Field Names

| Field | Purpose |
|-------|---------|
| `name` | Default display name (`_rec_name`) |
| `active` | Archive/unarchive records |
| `sequence` | Ordering in lists |
| `state` | Workflow status |
| `company_id` | Multi-company support |
| `create_uid`, `create_date` | Audit: who/when created |
| `write_uid`, `write_date` | Audit: who/when modified |

## Guidelines

1. **Naming conventions**
   - Model names: lowercase with dots (`my.model`)
   - Module names: lowercase with underscores (`my_module`)
   - XML IDs: lowercase with underscores

2. **Best practices**
   - Always set `_description` on models
   - Use `_order` for default sorting
   - Add `_sql_constraints` for data integrity
   - Use `_inherit` for extending existing models

3. **Performance**
   - Use `@api.depends` for computed fields
   - Prefer `sudo()` sparingly
   - Use `env.ref()` for XML ID references

## Common Issues

| Issue | Solution |
|-------|----------|
| Model not found | Check `__init__.py` imports |
| View not loading | Verify XML syntax and file in manifest `data` |
| Access denied | Check `ir.model.access.csv` permissions |
| Field not visible | Ensure field defined in view XML |
| Module not in Apps | Set `application: True` in manifest |

## Resources

- **Official Documentation**: https://www.odoo.com/documentation/18.0/developer.html
- **Tutorials**: https://www.odoo.com/documentation/18.0/developer/tutorials.html
- **ORM Reference**: https://www.odoo.com/documentation/18.0/developer/reference/backend/orm.html
- **Module Reference**: https://www.odoo.com/documentation/18.0/developer/reference/backend/module.html

## Detailed References

- **Manifest fields**: [references/manifest.md](references/manifest.md)
- **Models & ORM**: [references/models.md](references/models.md)
- **Views & XML**: [references/views.md](references/views.md)
- **Security rules**: [references/security.md](references/security.md)

## Templates

Module templates available in `assets/templates/`:
- `basic_module/` - Minimal module structure
- `full_module/` - Complete module with all components
