# Odoo 18 Security Reference

## Security Layers

1. **Access Control Lists (ACL)** - Model-level CRUD permissions
2. **Record Rules** - Row-level access filtering
3. **Field-level Security** - Individual field access
4. **Menu/Action Security** - UI element visibility

## Access Control Lists (ir.model.access.csv)

### File Format

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
```

| Column | Description |
|--------|-------------|
| `id` | Unique XML ID |
| `name` | Human-readable name |
| `model_id:id` | Model reference (`model_<model_name>`) |
| `group_id:id` | Group reference (empty = all users) |
| `perm_read` | Read permission (0 or 1) |
| `perm_write` | Update permission (0 or 1) |
| `perm_create` | Create permission (0 or 1) |
| `perm_unlink` | Delete permission (0 or 1) |

### Examples

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
# All users can read
access_my_model_all,my.model.all,model_my_model,,1,0,0,0
# Base users have full access
access_my_model_user,my.model.user,model_my_model,base.group_user,1,1,1,1
# Custom group with limited access
access_my_model_readonly,my.model.readonly,model_my_model,my_module.group_readonly,1,0,0,0
```

### Model ID Convention

Replace dots with underscores, prefix with `model_`:

| Model | Model ID |
|-------|----------|
| `res.partner` | `model_res_partner` |
| `sale.order` | `model_sale_order` |
| `my.custom.model` | `model_my_custom_model` |

## Security Groups

### Defining Groups

**`security/security.xml`**:

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Category -->
    <record id="module_category_my_module" model="ir.module.category">
        <field name="name">My Module</field>
        <field name="sequence">10</field>
    </record>

    <!-- User Group -->
    <record id="group_my_module_user" model="res.groups">
        <field name="name">User</field>
        <field name="category_id" ref="module_category_my_module"/>
        <field name="implied_ids" eval="[(4, ref('base.group_user'))]"/>
    </record>

    <!-- Manager Group (inherits User) -->
    <record id="group_my_module_manager" model="res.groups">
        <field name="name">Manager</field>
        <field name="category_id" ref="module_category_my_module"/>
        <field name="implied_ids" eval="[(4, ref('group_my_module_user'))]"/>
        <field name="users" eval="[(4, ref('base.user_root')), (4, ref('base.user_admin'))]"/>
    </record>
</odoo>
```

### Common Base Groups

| Group | XML ID | Description |
|-------|--------|-------------|
| Internal User | `base.group_user` | Standard employees |
| Portal User | `base.group_portal` | External users |
| Public User | `base.group_public` | Anonymous users |
| Administrator | `base.group_system` | Full admin access |
| Multi-company | `base.group_multi_company` | See multiple companies |
| Technical Features | `base.group_no_one` | Developer mode |

### Group Relationships

```xml
<!-- implied_ids: This group inherits permissions from listed groups -->
<field name="implied_ids" eval="[(4, ref('base.group_user'))]"/>

<!-- users: Default users added to this group -->
<field name="users" eval="[(4, ref('base.user_admin'))]"/>
```

## Record Rules (ir.rule)

Row-level security based on domain expressions.

### Global Rules (Apply to All Users)

```xml
<record id="rule_my_model_global" model="ir.rule">
    <field name="name">My Model: Active Only</field>
    <field name="model_id" ref="model_my_model"/>
    <field name="global" eval="True"/>
    <field name="domain_force">[('active', '=', True)]</field>
</record>
```

### Group-based Rules

```xml
<!-- Users see own records -->
<record id="rule_my_model_user" model="ir.rule">
    <field name="name">My Model: Own Records</field>
    <field name="model_id" ref="model_my_model"/>
    <field name="groups" eval="[(4, ref('my_module.group_my_module_user'))]"/>
    <field name="domain_force">[('user_id', '=', user.id)]</field>
    <field name="perm_read" eval="True"/>
    <field name="perm_write" eval="True"/>
    <field name="perm_create" eval="True"/>
    <field name="perm_unlink" eval="True"/>
</record>

<!-- Managers see all records -->
<record id="rule_my_model_manager" model="ir.rule">
    <field name="name">My Model: Manager Full Access</field>
    <field name="model_id" ref="model_my_model"/>
    <field name="groups" eval="[(4, ref('my_module.group_my_module_manager'))]"/>
    <field name="domain_force">[(1, '=', 1)]</field>
</record>
```

### Multi-company Rule

```xml
<record id="rule_my_model_company" model="ir.rule">
    <field name="name">My Model: Company</field>
    <field name="model_id" ref="model_my_model"/>
    <field name="global" eval="True"/>
    <field name="domain_force">[
        '|',
        ('company_id', '=', False),
        ('company_id', 'in', company_ids)
    ]</field>
</record>
```

### Domain Variables

| Variable | Description |
|----------|-------------|
| `user` | Current user record |
| `user.id` | Current user ID |
| `user.company_id` | Current company |
| `company_id` | Active company ID |
| `company_ids` | All accessible company IDs |
| `time` | Python time module |

## Field-level Security

### In Model Definition

```python
class MyModel(models.Model):
    _name = 'my.model'

    # Only managers can see/edit
    secret_field = fields.Char(groups='my_module.group_my_module_manager')

    # Read-only for users, editable by managers
    approved_amount = fields.Float(groups='my_module.group_my_module_manager')
```

### In Views

```xml
<field name="secret_field" groups="my_module.group_my_module_manager"/>

<button name="action_approve" groups="my_module.group_my_module_manager"
        string="Approve"/>
```

## Menu/Action Security

### Menu Item

```xml
<menuitem id="menu_config"
          name="Configuration"
          parent="menu_root"
          groups="my_module.group_my_module_manager"
          sequence="100"/>
```

### Actions

```xml
<record id="action_admin_settings" model="ir.actions.act_window">
    <field name="name">Admin Settings</field>
    <field name="res_model">my.settings</field>
    <field name="groups_id" eval="[(4, ref('my_module.group_my_module_manager'))]"/>
</record>
```

## Sudo Operations

Bypass security for specific operations:

```python
# Execute with full admin rights
self.sudo().create({'name': 'System Record'})

# Check permission explicitly
if self.env.user.has_group('my_module.group_my_module_manager'):
    self.action_approve()

# Run as specific user
self.with_user(user_id).action_check()
```

## Complete Example

### File Structure

```
my_module/
├── __manifest__.py
├── security/
│   ├── security.xml      # Groups
│   └── ir.model.access.csv   # ACL
```

### `__manifest__.py`

```python
{
    'name': 'My Module',
    'depends': ['base'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
    ],
}
```

### `security/security.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="module_category_my_module" model="ir.module.category">
        <field name="name">My Module</field>
    </record>

    <record id="group_my_module_user" model="res.groups">
        <field name="name">User</field>
        <field name="category_id" ref="module_category_my_module"/>
        <field name="implied_ids" eval="[(4, ref('base.group_user'))]"/>
    </record>

    <record id="group_my_module_manager" model="res.groups">
        <field name="name">Manager</field>
        <field name="category_id" ref="module_category_my_module"/>
        <field name="implied_ids" eval="[(4, ref('group_my_module_user'))]"/>
    </record>

    <!-- Record rule: Users see own records -->
    <record id="rule_my_model_user" model="ir.rule">
        <field name="name">Own Records</field>
        <field name="model_id" ref="model_my_model"/>
        <field name="groups" eval="[(4, ref('group_my_module_user'))]"/>
        <field name="domain_force">[('create_uid', '=', user.id)]</field>
    </record>

    <!-- Record rule: Managers see all -->
    <record id="rule_my_model_manager" model="ir.rule">
        <field name="name">All Records</field>
        <field name="model_id" ref="model_my_model"/>
        <field name="groups" eval="[(4, ref('group_my_module_manager'))]"/>
        <field name="domain_force">[(1, '=', 1)]</field>
    </record>
</odoo>
```

### `security/ir.model.access.csv`

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_my_model_user,my.model.user,model_my_model,group_my_module_user,1,1,1,0
access_my_model_manager,my.model.manager,model_my_model,group_my_module_manager,1,1,1,1
```

## Debugging Security

```python
# Check current user's groups
self.env.user.groups_id.mapped('full_name')

# Check if user has specific group
self.env.user.has_group('my_module.group_my_module_manager')

# View effective rules
self.env['ir.rule']._compute_domain(self._name, 'read')

# Bypass for debugging (don't use in production)
records = self.sudo().search([])
```

## Common Patterns

### Draft/Confirmed Workflow

```csv
# Users can only delete drafts (handled via Python code)
access_my_model_user,my.model.user,model_my_model,group_user,1,1,1,1
```

```python
def unlink(self):
    if any(record.state != 'draft' for record in self):
        raise UserError("Can only delete draft records!")
    return super().unlink()
```

### Portal Access

```xml
<record id="rule_my_model_portal" model="ir.rule">
    <field name="name">Portal: Own Records</field>
    <field name="model_id" ref="model_my_model"/>
    <field name="groups" eval="[(4, ref('base.group_portal'))]"/>
    <field name="domain_force">[('partner_id', '=', user.partner_id.id)]</field>
</record>
```
