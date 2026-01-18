# Odoo 18 Views & XML Reference

## View Types

| Type | Purpose | Primary Tag |
|------|---------|-------------|
| Form | Single record editing | `<form>` |
| Tree/List | Multiple records display | `<tree>` |
| Kanban | Card-based view | `<kanban>` |
| Search | Search filters | `<search>` |
| Calendar | Date-based view | `<calendar>` |
| Gantt | Timeline view | `<gantt>` |
| Graph | Charts | `<graph>` |
| Pivot | Pivot tables | `<pivot>` |

## View Definition Structure

```xml
<record id="view_xml_id" model="ir.ui.view">
    <field name="name">model.view.type</field>
    <field name="model">model.name</field>
    <field name="priority">16</field>
    <field name="arch" type="xml">
        <!-- View definition here -->
    </field>
</record>
```

## Form View

### Basic Structure

```xml
<form string="Form Title">
    <header>
        <!-- Buttons and status bar -->
        <button name="action_confirm" type="object" string="Confirm"
                class="btn-primary" invisible="state != 'draft'"/>
        <field name="state" widget="statusbar"
               statusbar_visible="draft,confirmed,done"/>
    </header>
    <sheet>
        <!-- Main content -->
        <div class="oe_button_box" name="button_box">
            <!-- Smart buttons -->
            <button name="action_view_orders" type="object"
                    class="oe_stat_button" icon="fa-shopping-cart">
                <field name="order_count" widget="statinfo" string="Orders"/>
            </button>
        </div>
        <widget name="web_ribbon" title="Archived" bg_color="bg-danger"
                invisible="active"/>
        <field name="image" widget="image" class="oe_avatar"/>
        <div class="oe_title">
            <h1>
                <field name="name" placeholder="Name"/>
            </h1>
        </div>
        <group>
            <group string="General">
                <field name="partner_id"/>
                <field name="date"/>
            </group>
            <group string="Details">
                <field name="amount"/>
                <field name="currency_id"/>
            </group>
        </group>
        <notebook>
            <page string="Lines" name="lines">
                <field name="line_ids">
                    <tree editable="bottom">
                        <field name="product_id"/>
                        <field name="quantity"/>
                        <field name="price"/>
                    </tree>
                </field>
            </page>
            <page string="Notes" name="notes">
                <field name="notes" placeholder="Add notes..."/>
            </page>
        </notebook>
    </sheet>
    <div class="oe_chatter">
        <field name="message_follower_ids"/>
        <field name="activity_ids"/>
        <field name="message_ids"/>
    </div>
</form>
```

### Form Elements

| Element | Purpose |
|---------|---------|
| `<header>` | Top buttons and status bar |
| `<sheet>` | Main content area |
| `<group>` | Field grouping (2 columns default) |
| `<notebook>` | Tabbed sections |
| `<page>` | Tab within notebook |
| `<div class="oe_chatter">` | Mail thread |
| `<separator>` | Visual divider |
| `<label>` | Custom label |

## Tree View

```xml
<tree string="Records"
      decoration-danger="state == 'cancelled'"
      decoration-success="state == 'done'"
      default_order="date desc">
    <field name="name"/>
    <field name="partner_id"/>
    <field name="date"/>
    <field name="amount" sum="Total"/>
    <field name="state"
           decoration-info="state == 'draft'"
           decoration-warning="state == 'confirmed'"
           widget="badge"/>
    <button name="action_confirm" type="object" icon="fa-check"
            invisible="state != 'draft'"/>
</tree>
```

### Tree Attributes

| Attribute | Description |
|-----------|-------------|
| `editable="bottom"` | Inline editing (add at bottom) |
| `editable="top"` | Inline editing (add at top) |
| `default_order` | Default sort |
| `decoration-*` | Conditional styling |
| `multi_edit="1"` | Enable multi-record editing |
| `sample="1"` | Show sample data |

### Decoration Colors

```xml
decoration-bf      <!-- Bold -->
decoration-it      <!-- Italic -->
decoration-danger  <!-- Red -->
decoration-warning <!-- Yellow/Orange -->
decoration-success <!-- Green -->
decoration-info    <!-- Blue -->
decoration-muted   <!-- Gray -->
```

## Search View

```xml
<search string="Search Records">
    <!-- Search fields -->
    <field name="name"/>
    <field name="partner_id"/>
    <field name="date"/>

    <!-- Filters -->
    <filter name="filter_draft" string="Draft"
            domain="[('state', '=', 'draft')]"/>
    <filter name="filter_confirmed" string="Confirmed"
            domain="[('state', '=', 'confirmed')]"/>
    <separator/>
    <filter name="filter_today" string="Today"
            domain="[('date', '=', context_today().strftime('%Y-%m-%d'))]"/>
    <filter name="filter_this_month" string="This Month"
            domain="[('date', '>=', (context_today() + relativedelta(day=1)).strftime('%Y-%m-%d')),
                     ('date', '&lt;', (context_today() + relativedelta(months=1, day=1)).strftime('%Y-%m-%d'))]"/>

    <!-- Group by -->
    <group expand="1" string="Group By">
        <filter name="group_state" string="Status"
                context="{'group_by': 'state'}"/>
        <filter name="group_partner" string="Partner"
                context="{'group_by': 'partner_id'}"/>
        <filter name="group_date" string="Date"
                context="{'group_by': 'date:month'}"/>
    </group>
</search>
```

## Kanban View

```xml
<kanban default_group_by="state" class="o_kanban_small_column"
        quick_create="true" on_create="quick_create">
    <field name="name"/>
    <field name="partner_id"/>
    <field name="state"/>
    <field name="color"/>
    <templates>
        <t t-name="kanban-box">
            <div t-attf-class="oe_kanban_card oe_kanban_global_click
                               o_kanban_record_has_image_fill">
                <div class="oe_kanban_content">
                    <div class="o_kanban_record_top">
                        <div class="o_kanban_record_headings">
                            <strong class="o_kanban_record_title">
                                <field name="name"/>
                            </strong>
                        </div>
                        <div class="o_dropdown_kanban dropdown">
                            <a role="button" class="dropdown-toggle o-no-caret btn"
                               data-bs-toggle="dropdown" href="#">
                                <span class="fa fa-ellipsis-v"/>
                            </a>
                            <div class="dropdown-menu" role="menu">
                                <a t-if="widget.editable" role="menuitem"
                                   type="edit" class="dropdown-item">Edit</a>
                                <a t-if="widget.deletable" role="menuitem"
                                   type="delete" class="dropdown-item">Delete</a>
                            </div>
                        </div>
                    </div>
                    <div class="o_kanban_record_body">
                        <field name="partner_id"/>
                    </div>
                    <div class="o_kanban_record_bottom">
                        <div class="oe_kanban_bottom_left">
                            <field name="priority" widget="priority"/>
                        </div>
                        <div class="oe_kanban_bottom_right">
                            <field name="user_id" widget="many2one_avatar_user"/>
                        </div>
                    </div>
                </div>
            </div>
        </t>
    </templates>
</kanban>
```

## Calendar View

```xml
<calendar string="Calendar" date_start="date_start" date_stop="date_end"
          color="partner_id" mode="month" quick_add="false"
          event_open_popup="true" event_limit="5">
    <field name="name"/>
    <field name="partner_id" filters="1"/>
    <field name="state"/>
</calendar>
```

## Graph View

```xml
<graph string="Analysis" type="bar" stacked="True">
    <field name="date" interval="month" type="row"/>
    <field name="partner_id" type="row"/>
    <field name="amount" type="measure"/>
</graph>
```

| Type | Description |
|------|-------------|
| `bar` | Bar chart |
| `line` | Line chart |
| `pie` | Pie chart |

## Pivot View

```xml
<pivot string="Analysis" sample="1">
    <field name="date" interval="month" type="row"/>
    <field name="state" type="col"/>
    <field name="amount" type="measure"/>
</pivot>
```

## Actions

### Window Action

```xml
<record id="action_my_model" model="ir.actions.act_window">
    <field name="name">My Records</field>
    <field name="res_model">my.model</field>
    <field name="view_mode">tree,form,kanban</field>
    <field name="domain">[('active', '=', True)]</field>
    <field name="context">{'default_state': 'draft'}</field>
    <field name="search_view_id" ref="view_my_model_search"/>
    <field name="help" type="html">
        <p class="o_view_nocontent_smiling_face">
            Create your first record!
        </p>
        <p>
            Click the button to get started.
        </p>
    </field>
</record>
```

### Server Action

```xml
<record id="action_confirm_selected" model="ir.actions.server">
    <field name="name">Confirm Selected</field>
    <field name="model_id" ref="model_my_model"/>
    <field name="binding_model_id" ref="model_my_model"/>
    <field name="binding_view_types">list,form</field>
    <field name="state">code</field>
    <field name="code">
        records.action_confirm()
    </field>
</record>
```

## Menus

```xml
<!-- Root menu -->
<menuitem id="menu_my_module_root"
          name="My Module"
          sequence="10"
          web_icon="my_module,static/description/icon.png"/>

<!-- Sub menu -->
<menuitem id="menu_my_model"
          name="My Records"
          parent="menu_my_module_root"
          action="action_my_model"
          sequence="10"/>

<!-- Nested menu -->
<menuitem id="menu_configuration"
          name="Configuration"
          parent="menu_my_module_root"
          sequence="100"/>

<menuitem id="menu_settings"
          name="Settings"
          parent="menu_configuration"
          action="action_settings"
          sequence="10"/>
```

## Common Widgets

| Widget | Field Type | Description |
|--------|------------|-------------|
| `badge` | Selection | Colored badge |
| `statusbar` | Selection | Status workflow |
| `priority` | Selection | Star rating |
| `many2one_avatar_user` | Many2one | User avatar |
| `image` | Binary | Image display |
| `url` | Char | Clickable URL |
| `email` | Char | Clickable email |
| `phone` | Char | Clickable phone |
| `monetary` | Float | Currency formatted |
| `progressbar` | Float/Integer | Progress bar |
| `handle` | Integer | Drag handle (sequence) |
| `html` | Html | Rich text editor |
| `color` | Integer | Color picker |
| `daterange` | Date | Date range picker |

## Conditional Visibility

```xml
<!-- Hide if condition true -->
<field name="partner_id" invisible="state == 'done'"/>

<!-- Multiple conditions -->
<button name="action" invisible="state != 'draft' or not partner_id"/>

<!-- Column invisibility in tree -->
<field name="amount" column_invisible="parent.hide_amounts"/>
```

## View Inheritance

```xml
<record id="view_partner_form_inherit" model="ir.ui.view">
    <field name="name">res.partner.form.inherit</field>
    <field name="model">res.partner</field>
    <field name="inherit_id" ref="base.view_partner_form"/>
    <field name="arch" type="xml">
        <!-- Add after -->
        <field name="email" position="after">
            <field name="loyalty_points"/>
        </field>

        <!-- Add before -->
        <field name="phone" position="before">
            <field name="mobile"/>
        </field>

        <!-- Replace -->
        <field name="website" position="replace">
            <field name="website" widget="url"/>
        </field>

        <!-- Add attributes -->
        <field name="name" position="attributes">
            <attribute name="required">True</attribute>
        </field>

        <!-- Inside (at end) -->
        <xpath expr="//group[@name='sale']" position="inside">
            <field name="custom_field"/>
        </xpath>

        <!-- Remove -->
        <field name="obsolete_field" position="replace"/>
    </field>
</record>
```

### XPath Expressions

```xml
<xpath expr="//form//group[1]" position="after">
<xpath expr="//field[@name='name']" position="before">
<xpath expr="//page[@name='notes']" position="replace">
<xpath expr="//button[@name='action']" position="attributes">
<xpath expr="//sheet" position="inside">
<xpath expr="//div[hasclass('oe_title')]" position="after">
```
