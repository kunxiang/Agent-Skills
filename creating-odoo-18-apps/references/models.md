# Odoo 18 Models & ORM Reference

## Model Types

| Type | Base Class | Database | Use Case |
|------|------------|----------|----------|
| Regular | `models.Model` | Persistent | Business data |
| Transient | `models.TransientModel` | Auto-cleaned | Wizards |
| Abstract | `models.AbstractModel` | None | Mixins, shared logic |

## Model Definition

```python
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'
    _order = 'name'
    _rec_name = 'name'

    # Fields defined here
    name = fields.Char(string='Title', required=True)
```

## Model Attributes

| Attribute | Description |
|-----------|-------------|
| `_name` | Technical name (required for new models) |
| `_description` | Human-readable description |
| `_order` | Default sort order |
| `_rec_name` | Field used for display name (default: `name`) |
| `_inherit` | Model(s) to inherit from |
| `_inherits` | Delegation inheritance |
| `_table` | Custom table name |
| `_log_access` | Track create/write dates (default: True) |
| `_auto` | Create database table (default: True) |

## Field Types

### Simple Fields

```python
# String fields
name = fields.Char(string='Name', size=64, required=True)
description = fields.Text(string='Description')
html_content = fields.Html(string='Content', sanitize=True)

# Numeric fields
sequence = fields.Integer(string='Sequence', default=10)
price = fields.Float(string='Price', digits=(10, 2))
amount = fields.Monetary(string='Amount', currency_field='currency_id')

# Boolean
active = fields.Boolean(string='Active', default=True)

# Date/Time
date = fields.Date(string='Date', default=fields.Date.today)
datetime = fields.Datetime(string='DateTime', default=fields.Datetime.now)

# Selection
state = fields.Selection([
    ('draft', 'Draft'),
    ('confirmed', 'Confirmed'),
    ('done', 'Done'),
    ('cancelled', 'Cancelled'),
], string='Status', default='draft', required=True)

# Binary
image = fields.Binary(string='Image', attachment=True)
document = fields.Binary(string='Document')
```

### Relational Fields

```python
# Many2one (foreign key)
partner_id = fields.Many2one(
    comodel_name='res.partner',
    string='Customer',
    ondelete='restrict',  # 'cascade', 'set null', 'restrict'
    domain=[('is_company', '=', True)],
    context={'show_email': True},
    required=False,
)

# One2many (reverse of Many2one)
line_ids = fields.One2many(
    comodel_name='sale.order.line',
    inverse_name='order_id',
    string='Order Lines',
    copy=True,
)

# Many2many
tag_ids = fields.Many2many(
    comodel_name='product.tag',
    relation='product_tag_rel',      # Optional: custom table name
    column1='product_id',            # Optional: this model's column
    column2='tag_id',                # Optional: related model's column
    string='Tags',
)
```

### Computed Fields

```python
# Computed field (read-only by default)
total = fields.Float(
    string='Total',
    compute='_compute_total',
    store=True,  # Store in database
)

# Computed with inverse (read-write)
display_name = fields.Char(
    string='Display Name',
    compute='_compute_display_name',
    inverse='_inverse_display_name',
    store=True,
)

@api.depends('line_ids.subtotal')
def _compute_total(self):
    for record in self:
        record.total = sum(record.line_ids.mapped('subtotal'))

def _inverse_display_name(self):
    for record in self:
        # Parse display_name and set name
        record.name = record.display_name.split(' ')[0]
```

### Related Fields

```python
# Related field (shortcut to related model field)
partner_email = fields.Char(
    string='Partner Email',
    related='partner_id.email',
    readonly=True,
    store=False,
)
```

## Field Attributes

| Attribute | Description |
|-----------|-------------|
| `string` | Label displayed in UI |
| `required` | Field must have value |
| `readonly` | Cannot be modified in UI |
| `index` | Create database index |
| `default` | Default value (value or callable) |
| `help` | Tooltip text |
| `copy` | Copy on duplicate (default: True) |
| `groups` | Access groups |
| `company_dependent` | Different value per company |
| `translate` | Enable translation |
| `tracking` | Track changes (requires mail.thread) |

## API Decorators

### @api.depends

Triggers compute when dependencies change:

```python
@api.depends('price', 'quantity')
def _compute_total(self):
    for record in self:
        record.total = record.price * record.quantity
```

### @api.onchange

Triggers on form field change (UI only):

```python
@api.onchange('partner_id')
def _onchange_partner_id(self):
    if self.partner_id:
        self.delivery_address = self.partner_id.street
```

### @api.constrains

Validation on save:

```python
@api.constrains('price')
def _check_price(self):
    for record in self:
        if record.price < 0:
            raise ValidationError("Price cannot be negative!")
```

### @api.model

Method operates on model (no recordset):

```python
@api.model
def get_default_values(self):
    return {'state': 'draft'}
```

### @api.model_create_multi

Optimized create for multiple records:

```python
@api.model_create_multi
def create(self, vals_list):
    for vals in vals_list:
        vals['reference'] = self.env['ir.sequence'].next_by_code('my.model')
    return super().create(vals_list)
```

## CRUD Methods

### Create

```python
# Single record
record = self.env['res.partner'].create({
    'name': 'John Doe',
    'email': 'john@example.com',
})

# Multiple records
records = self.env['res.partner'].create([
    {'name': 'John'},
    {'name': 'Jane'},
])
```

### Read/Search

```python
# Search
partners = self.env['res.partner'].search([
    ('is_company', '=', True),
    ('country_id.code', '=', 'US'),
], limit=10, order='name')

# Search count
count = self.env['res.partner'].search_count([('active', '=', True)])

# Browse by ID
partner = self.env['res.partner'].browse(1)

# Read specific fields
data = partner.read(['name', 'email'])

# Search and read
data = self.env['res.partner'].search_read(
    domain=[('is_company', '=', True)],
    fields=['name', 'email'],
    limit=10,
)
```

### Update

```python
# Single field
record.name = 'New Name'

# Multiple fields
record.write({
    'name': 'New Name',
    'email': 'new@example.com',
})

# Update multiple records
records.write({'active': False})
```

### Delete

```python
record.unlink()
```

## Search Domains

```python
# Basic operators
[('name', '=', 'John')]
[('age', '>', 18)]
[('name', 'like', 'John%')]      # SQL LIKE
[('name', 'ilike', '%john%')]    # Case-insensitive
[('id', 'in', [1, 2, 3])]
[('partner_id', '!=', False)]    # Not null

# Logical operators
['&', ('age', '>', 18), ('country', '=', 'US')]  # AND (default)
['|', ('age', '<', 18), ('age', '>', 65)]        # OR
['!', ('active', '=', True)]                      # NOT

# Complex example
[
    '|',
    ('state', '=', 'done'),
    '&',
    ('state', '=', 'confirmed'),
    ('date', '>=', '2024-01-01'),
]
```

## Inheritance

### Extension Inheritance

Modify existing model in-place:

```python
class ResPartner(models.Model):
    _inherit = 'res.partner'

    loyalty_points = fields.Integer(string='Loyalty Points')

    def action_add_points(self):
        self.loyalty_points += 10
```

### Prototype Inheritance

Copy features to new model:

```python
class CustomPartner(models.Model):
    _name = 'custom.partner'
    _inherit = 'res.partner'  # Copies all fields/methods
    _description = 'Custom Partner'
```

### Delegation Inheritance

Embed another model:

```python
class Employee(models.Model):
    _name = 'hr.employee'
    _inherits = {'res.partner': 'partner_id'}

    partner_id = fields.Many2one('res.partner', required=True, ondelete='cascade')
    department_id = fields.Many2one('hr.department')
```

## Mixins

### mail.thread (Chatter)

```python
class MyModel(models.Model):
    _name = 'my.model'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(tracking=True)
    state = fields.Selection(..., tracking=True)
```

### Common Mixins

| Mixin | Purpose |
|-------|---------|
| `mail.thread` | Chatter, followers |
| `mail.activity.mixin` | Activities, tasks |
| `portal.mixin` | Portal access |
| `image.mixin` | Image handling |
| `avatar.mixin` | User avatars |

## SQL Constraints

```python
class MyModel(models.Model):
    _name = 'my.model'

    code = fields.Char(required=True)
    sequence = fields.Integer()

    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'Code must be unique!'),
        ('sequence_positive', 'CHECK(sequence > 0)', 'Sequence must be positive!'),
    ]
```

## Recordset Operations

```python
# Iteration
for record in records:
    print(record.name)

# Mapping
names = records.mapped('name')
partner_names = records.mapped('partner_id.name')

# Filtering
active = records.filtered(lambda r: r.active)
active = records.filtered('active')

# Sorting
sorted_records = records.sorted(key=lambda r: r.name)
sorted_records = records.sorted('name', reverse=True)

# Set operations
combined = records1 | records2  # Union
common = records1 & records2    # Intersection
diff = records1 - records2      # Difference

# Check membership
if record in records:
    pass
```

## Environment (env)

```python
# Access models
partners = self.env['res.partner'].search([])

# Current user
user = self.env.user
company = self.env.company

# Context
lang = self.env.context.get('lang')

# Change context
records = self.with_context(lang='fr_FR').search([])

# Sudo (bypass access rights)
records = self.sudo().search([])

# Run as different user
records = self.with_user(user_id).search([])

# Reference by XML ID
group = self.env.ref('base.group_user')
```
