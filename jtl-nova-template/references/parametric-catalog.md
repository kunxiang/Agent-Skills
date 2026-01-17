# Parametric Product Catalog Implementation

## Overview

DigiKey-style catalog with three switchable views and user preference persistence.

## File Structure

```
templates/MyTheme/
├── Bootstrap.php                    # IO handlers + export
├── productlist/
│   ├── index.tpl                   # Main (copy from assets)
│   ├── filter_parametric.tpl       # Filters
│   ├── product_table.tpl           # Table view
│   └── item_list.tpl               # List view item
├── js/
│   └── parametric-catalog.js       # JS class
└── themes/mytheme/sass/
    └── _parametric-catalog.scss    # Styles
```

## Main Template (index.tpl)

```smarty
{extends file="{$parent_template_path}/productlist/index.tpl"}

{block name="productlist"}
<div class="parametric-catalog" data-view="{$smarty.session.catalogView|default:'gallery'}">
    
    {* Header *}
    <div class="catalog-header">
        <h1>{$Kategorie->cName}</h1>
        <span class="result-count"><strong>{$Suchergebnisse->Artikel->nAnzahl}</strong> Produkte</span>
    </div>
    
    {* Filters *}
    {include file="productlist/filter_parametric.tpl"}
    
    {* Toolbar *}
    <div class="catalog-toolbar">
        <div class="view-switcher btn-group">
            <button class="btn view-btn" data-view="gallery"><i class="fa fa-th-large"></i></button>
            <button class="btn view-btn" data-view="list"><i class="fa fa-th-list"></i></button>
            <button class="btn view-btn" data-view="table"><i class="fa fa-table"></i></button>
        </div>
        <div class="table-tools">
            <button id="exportBtn"><i class="fa fa-download"></i> Export</button>
            <button id="compareBtn" disabled>Vergleichen (<span id="compareCount">0</span>)</button>
        </div>
        <select id="sortSelect" class="form-control">
            <option value="0">Standard</option>
            <option value="3">Preis aufsteigend</option>
            <option value="4">Preis absteigend</option>
        </select>
    </div>
    
    {* Views *}
    <div class="catalog-content">
        <div class="view-gallery catalog-view">
            <div class="row">
                {foreach $Suchergebnisse->Artikel->elemente as $Artikel}
                    <div class="col-6 col-md-4 col-lg-3">
                        {include file='productlist/item_box.tpl'}
                    </div>
                {/foreach}
            </div>
        </div>
        
        <div class="view-list catalog-view" style="display:none">
            {foreach $Suchergebnisse->Artikel->elemente as $Artikel}
                {include file='productlist/item_list.tpl'}
            {/foreach}
        </div>
        
        <div class="view-table catalog-view" style="display:none">
            {include file='productlist/product_table.tpl'}
        </div>
    </div>
    
    {include file='snippets/pagination.tpl' oPagination=$Suchergebnisse->Seitenzahlen}
</div>

{inline_script}<script src="{$ShopURL}/templates/{$template->getName()}/js/parametric-catalog.js"></script>{/inline_script}
{/block}
```

## Filter Component (filter_parametric.tpl)

```smarty
<div class="parametric-filter">
    <div class="filter-row">
        {* Stock filter *}
        <div class="filter-dropdown">
            <button class="filter-btn" data-toggle="dropdown">Verfügbarkeit <i class="fa fa-chevron-down"></i></button>
            <div class="filter-dropdown-content">
                <label><input type="checkbox" name="lf" value="1" {if $Suchergebnisse->nLagerbestandFilter == 1}checked{/if}> Nur auf Lager</label>
            </div>
        </div>
        
        {* Merkmal filters *}
        {foreach $Suchergebnisse->MerkmalFilter as $filter}
        <div class="filter-dropdown">
            <button class="filter-btn" data-toggle="dropdown">
                {$filter->cName}
                {assign var="active" value=0}
                {foreach $filter->oMerkmalWert_arr as $v}{if $v->nAktiv}{assign var="active" value=$active+1}{/if}{/foreach}
                {if $active > 0}<span class="badge">{$active}</span>{/if}
                <i class="fa fa-chevron-down"></i>
            </button>
            <div class="filter-dropdown-content">
                {if $filter->oMerkmalWert_arr|@count > 10}
                    <input type="text" class="filter-search" placeholder="Suchen...">
                {/if}
                <div class="filter-options">
                    {foreach $filter->oMerkmalWert_arr as $value}
                    <label class="filter-option">
                        <input type="checkbox" name="mf[{$filter->kMerkmal}][]" value="{$value->kMerkmalWert}" {if $value->nAktiv}checked{/if}>
                        <span>{$value->cWert}</span> <small>({$value->nAnzahl})</small>
                    </label>
                    {/foreach}
                </div>
            </div>
        </div>
        {/foreach}
    </div>
    
    {* Active filter tags *}
    <div class="active-filters">
        {foreach $Suchergebnisse->MerkmalFilter as $filter}
            {foreach $filter->oMerkmalWert_arr as $value}
                {if $value->nAktiv}
                <span class="filter-tag">
                    {$filter->cName}: {$value->cWert}
                    <a href="{$value->cURLPfad}">×</a>
                </span>
                {/if}
            {/foreach}
        {/foreach}
        <a href="{$Suchergebnisse->cURLFilterReset}">Alle zurücksetzen</a>
    </div>
</div>
```

## Table View (product_table.tpl)

```smarty
<div class="product-table-wrapper">
    <table class="product-table table table-hover table-sm">
        <thead>
            <tr>
                <th><input type="checkbox" id="selectAll"></th>
                <th>Bild</th>
                <th class="sortable" data-sort="name">Produkt</th>
                <th>Art.-Nr.</th>
                {foreach $Suchergebnisse->MerkmalFilter as $m}
                <th class="sortable" data-sort="param_{$m->kMerkmal}">{$m->cName}</th>
                {/foreach}
                <th class="sortable" data-sort="stock">Lager</th>
                <th class="sortable" data-sort="price">Preis</th>
                <th>Aktion</th>
            </tr>
        </thead>
        <tbody>
            {foreach $Suchergebnisse->Artikel->elemente as $Artikel}
            <tr data-id="{$Artikel->kArtikel}" data-price="{$Artikel->Preise->fVKNetto}" data-stock="{$Artikel->fLagerbestand}">
                <td><input type="checkbox" class="compare-cb" value="{$Artikel->kArtikel}"></td>
                <td><img src="{$Artikel->Bilder[0]->cPfadMini}" width="50"></td>
                <td><a href="{$Artikel->cURL}">{$Artikel->cName}</a></td>
                <td>{$Artikel->cArtNr}</td>
                {foreach $Suchergebnisse->MerkmalFilter as $m}
                <td data-merkmal="{$m->kMerkmal}">
                    {foreach $Artikel->oMerkmale_arr as $am}
                        {if $am->kMerkmal == $m->kMerkmal}{$am->cWert}{/if}
                    {/foreach}
                </td>
                {/foreach}
                <td>{$Artikel->fLagerbestand|number_format:0:",":"."}</td>
                <td>{$Artikel->Preise->cVKLocalized[0]}</td>
                <td><button class="btn btn-sm btn-primary add-cart" data-id="{$Artikel->kArtikel}"><i class="fa fa-cart-plus"></i></button></td>
            </tr>
            {/foreach}
        </tbody>
    </table>
</div>
```

## JavaScript (parametric-catalog.js)

```javascript
class ParametricCatalog {
    constructor() {
        this.container = document.querySelector('.parametric-catalog');
        if (!this.container) return;
        this.view = this.container.dataset.view || 'gallery';
        this.compareList = [];
        this.init();
    }
    
    init() {
        this.initViewSwitcher();
        this.initFilters();
        this.initTableSort();
        this.initCompare();
        this.initExport();
        this.switchView(this.view, false);
    }
    
    // View switching
    initViewSwitcher() {
        this.container.querySelectorAll('.view-btn').forEach(btn => {
            btn.addEventListener('click', () => this.switchView(btn.dataset.view));
        });
    }
    
    switchView(view, save = true) {
        // Update buttons
        this.container.querySelectorAll('.view-btn').forEach(b => 
            b.classList.toggle('active', b.dataset.view === view));
        
        // Switch views
        this.container.querySelectorAll('.catalog-view').forEach(v => v.style.display = 'none');
        this.container.querySelector(`.view-${view}`).style.display = '';
        
        // Show/hide table tools
        const tools = this.container.querySelector('.table-tools');
        if (tools) tools.style.display = view === 'table' ? '' : 'none';
        
        this.view = view;
        
        // Save preference
        if (save) {
            fetch('/io.php', {
                method: 'POST',
                headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                body: `io={"name":"setCatalogView","params":["${view}"]}`
            });
            localStorage.setItem('catalogView', view);
        }
    }
    
    // Filter dropdowns
    initFilters() {
        this.container.querySelectorAll('[data-toggle="dropdown"]').forEach(btn => {
            btn.addEventListener('click', e => {
                e.stopPropagation();
                const content = btn.nextElementSibling;
                this.container.querySelectorAll('.filter-dropdown-content.show').forEach(c => {
                    if (c !== content) c.classList.remove('show');
                });
                content.classList.toggle('show');
            });
        });
        
        document.addEventListener('click', () => {
            this.container.querySelectorAll('.filter-dropdown-content.show').forEach(c => c.classList.remove('show'));
        });
        
        // Filter search
        this.container.querySelectorAll('.filter-search').forEach(input => {
            input.addEventListener('input', e => {
                const term = e.target.value.toLowerCase();
                e.target.parentElement.querySelectorAll('.filter-option').forEach(opt => {
                    opt.style.display = opt.textContent.toLowerCase().includes(term) ? '' : 'none';
                });
            });
        });
        
        // Auto-apply filters with debounce
        let timeout;
        this.container.querySelectorAll('.filter-options input').forEach(cb => {
            cb.addEventListener('change', () => {
                clearTimeout(timeout);
                timeout = setTimeout(() => this.applyFilters(), 500);
            });
        });
    }
    
    applyFilters() {
        const form = document.createElement('form');
        form.method = 'GET';
        form.action = location.pathname;
        this.container.querySelectorAll('.filter-options input:checked').forEach(cb => {
            const input = document.createElement('input');
            input.type = 'hidden';
            input.name = cb.name;
            input.value = cb.value;
            form.appendChild(input);
        });
        document.body.appendChild(form);
        form.submit();
    }
    
    // Table sorting
    initTableSort() {
        this.container.querySelectorAll('th.sortable').forEach(th => {
            th.addEventListener('click', () => {
                const key = th.dataset.sort;
                const order = th.dataset.order === 'asc' ? 'desc' : 'asc';
                this.container.querySelectorAll('th.sortable').forEach(h => h.dataset.order = '');
                th.dataset.order = order;
                this.sortTable(key, order);
            });
        });
    }
    
    sortTable(key, order) {
        const tbody = this.container.querySelector('.product-table tbody');
        const rows = Array.from(tbody.querySelectorAll('tr'));
        
        rows.sort((a, b) => {
            let av, bv;
            if (key === 'price') {
                av = parseFloat(a.dataset.price) || 0;
                bv = parseFloat(b.dataset.price) || 0;
            } else if (key === 'stock') {
                av = parseInt(a.dataset.stock) || 0;
                bv = parseInt(b.dataset.stock) || 0;
            } else if (key === 'name') {
                av = a.querySelector('td:nth-child(3)').textContent.trim();
                bv = b.querySelector('td:nth-child(3)').textContent.trim();
            } else if (key.startsWith('param_')) {
                const id = key.replace('param_', '');
                av = this.extractNum(a.querySelector(`[data-merkmal="${id}"]`)?.textContent);
                bv = this.extractNum(b.querySelector(`[data-merkmal="${id}"]`)?.textContent);
            }
            if (typeof av === 'string') return order === 'asc' ? av.localeCompare(bv) : bv.localeCompare(av);
            return order === 'asc' ? av - bv : bv - av;
        });
        
        rows.forEach(r => tbody.appendChild(r));
    }
    
    extractNum(str) {
        if (!str) return 0;
        const m = str.match(/[\d.,]+/);
        return m ? parseFloat(m[0].replace(',', '.')) : 0;
    }
    
    // Product comparison
    initCompare() {
        const btn = this.container.querySelector('#compareBtn');
        const count = this.container.querySelector('#compareCount');
        
        this.container.querySelectorAll('.compare-cb').forEach(cb => {
            cb.addEventListener('change', e => {
                if (e.target.checked && this.compareList.length < 4) {
                    this.compareList.push(e.target.value);
                } else if (e.target.checked) {
                    e.target.checked = false;
                    alert('Max 4 Produkte');
                } else {
                    this.compareList = this.compareList.filter(id => id !== e.target.value);
                }
                count.textContent = this.compareList.length;
                btn.disabled = this.compareList.length < 2;
            });
        });
        
        btn.addEventListener('click', () => {
            if (this.compareList.length >= 2) {
                location.href = `/vergleichsliste.php?a=${this.compareList.join('_')}`;
            }
        });
    }
    
    // Export
    initExport() {
        this.container.querySelector('#exportBtn')?.addEventListener('click', () => {
            const params = new URLSearchParams(location.search);
            params.set('export', '1');
            params.set('format', 'csv');
            location.href = `${location.pathname}?${params}`;
        });
    }
}

document.addEventListener('DOMContentLoaded', () => new ParametricCatalog());
```

## Bootstrap.php Additions

```php
public function boot(): void
{
    parent::boot();
    $this->handleIO();
    $this->handleExport();
}

protected function handleIO(): void
{
    if (!isset($_POST['io'])) return;
    $io = json_decode($_POST['io'], true);
    if ($io && $io['name'] === 'setCatalogView') {
        $_SESSION['catalogView'] = $io['params'][0] ?? 'gallery';
        header('Content-Type: application/json');
        echo json_encode(['success' => true]);
        exit;
    }
}

protected function handleExport(): void
{
    if (($_GET['export'] ?? '') !== '1') return;
    
    $filename = 'produkte_' . date('Y-m-d') . '.csv';
    header('Content-Type: text/csv; charset=utf-8');
    header('Content-Disposition: attachment; filename="' . $filename . '"');
    
    $out = fopen('php://output', 'w');
    fprintf($out, chr(0xEF) . chr(0xBB) . chr(0xBF)); // UTF-8 BOM
    
    // Headers
    fputcsv($out, ['Art.-Nr.', 'Name', 'Preis', 'Lager'], ';');
    
    // Data from current filter results
    // Implementation depends on how you access filtered products
    
    fclose($out);
    exit;
}
```

## SCSS (_parametric-catalog.scss)

```scss
.parametric-catalog {
    .catalog-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 3px solid $primary;
    }
    
    .catalog-toolbar {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1rem;
        
        .table-tools { display: none; }
    }
    
    .view-btn.active {
        background: $primary;
        color: white;
    }
}

// Filters
.parametric-filter {
    background: $gray-100;
    padding: 1rem;
    border-radius: $border-radius;
    margin-bottom: 1rem;
    
    .filter-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
    }
    
    .filter-dropdown {
        position: relative;
    }
    
    .filter-btn {
        padding: 0.5rem 1rem;
        background: white;
        border: 1px solid $border-color;
        border-radius: $border-radius;
        cursor: pointer;
        
        .badge { margin-left: 0.5rem; }
    }
    
    .filter-dropdown-content {
        display: none;
        position: absolute;
        top: 100%;
        left: 0;
        z-index: 1000;
        min-width: 250px;
        background: white;
        border: 1px solid $border-color;
        border-radius: $border-radius;
        box-shadow: $box-shadow;
        padding: 0.5rem;
        
        &.show { display: block; }
    }
    
    .filter-option {
        display: block;
        padding: 0.375rem 0.5rem;
        cursor: pointer;
        
        &:hover { background: $gray-100; }
    }
    
    .filter-tag {
        display: inline-flex;
        align-items: center;
        background: $primary;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 50px;
        font-size: 0.8rem;
        margin: 0.25rem;
        
        a { color: white; margin-left: 0.5rem; }
    }
}

// Table
.product-table {
    font-size: 0.85rem;
    
    th.sortable {
        cursor: pointer;
        &:hover { background: $gray-200; }
        &[data-order="asc"]::after { content: " ↑"; }
        &[data-order="desc"]::after { content: " ↓"; }
    }
}

// Responsive
@media (max-width: 767px) {
    .product-table thead { display: none; }
    .product-table tr {
        display: block;
        margin-bottom: 1rem;
        border: 1px solid $border-color;
        padding: 0.75rem;
    }
    .product-table td {
        display: flex;
        justify-content: space-between;
        &::before { content: attr(data-label); font-weight: bold; }
    }
}
```

## JTL-Wawi Configuration

Create Merkmale (attributes) for your products:

| Name | German | Examples |
|------|--------|----------|
| Resistance | Widerstand | 10kΩ, 4.7kΩ |
| Package | Bauform | 0402, 0805 |
| Tolerance | Toleranz | ±1%, ±5% |
| Power | Leistung | 1/8W, 1/4W |
| Voltage | Spannung | 50V, 100V |
