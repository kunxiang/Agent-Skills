# Parametric Product Catalog - Smarty Templates

## Übersicht

DigiKey-Stil Katalog mit drei umschaltbaren Ansichten und Benutzereinstellungs-Persistenz.

## Dateistruktur

```
templates/MeinTheme/
├── Bootstrap.php                    # IO-Handler + Export
├── productlist/
│   ├── index.tpl                   # Haupt-Template
│   ├── filter_parametric.tpl       # Filter
│   ├── product_table.tpl           # Tabellenansicht
│   └── item_list.tpl               # Listenansicht-Item
├── js/
│   └── parametric-catalog.js       # JS-Klasse
└── themes/meintheme/sass/
    └── _parametric-catalog.scss    # Stile
```

## Haupt-Template (index.tpl)

```smarty
{extends file="{$parent_template_path}/productlist/index.tpl"}

{block name="productlist"}
<div class="parametric-catalog" data-view="{$smarty.session.catalogView|default:'gallery'}">

    {* Header *}
    <div class="catalog-header">
        <h1>{$Kategorie->cName}</h1>
        <span class="result-count"><strong>{$Suchergebnisse->Artikel->nAnzahl}</strong> Produkte</span>
    </div>

    {* Filter *}
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

    {* Ansichten *}
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

## Filter-Komponente (filter_parametric.tpl)

```smarty
<div class="parametric-filter">
    <div class="filter-row">
        {* Lagerfilter *}
        <div class="filter-dropdown">
            <button class="filter-btn" data-toggle="dropdown">Verfügbarkeit <i class="fa fa-chevron-down"></i></button>
            <div class="filter-dropdown-content">
                <label><input type="checkbox" name="lf" value="1" {if $Suchergebnisse->nLagerbestandFilter == 1}checked{/if}> Nur auf Lager</label>
            </div>
        </div>

        {* Merkmal-Filter *}
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

    {* Aktive Filter-Tags *}
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

## Tabellenansicht (product_table.tpl)

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

## Listenansicht-Item (item_list.tpl)

```smarty
<div class="product-list-item" data-id="{$Artikel->kArtikel}">
    <div class="row align-items-center">
        <div class="col-2">
            <input type="checkbox" class="compare-cb" value="{$Artikel->kArtikel}">
            <img src="{$Artikel->Bilder[0]->cPfadKlein}" class="img-fluid" alt="{$Artikel->cName}">
        </div>
        <div class="col-4">
            <h5><a href="{$Artikel->cURL}">{$Artikel->cName}</a></h5>
            <small class="text-muted">Art.-Nr.: {$Artikel->cArtNr}</small>
        </div>
        <div class="col-4">
            <div class="row small">
                {assign var="count" value=0}
                {foreach $Artikel->oMerkmale_arr as $m}
                    {if $count < 6}
                    <div class="col-6">
                        <strong>{$m->cName}:</strong> {$m->cWert}
                    </div>
                    {assign var="count" value=$count+1}
                    {/if}
                {/foreach}
            </div>
        </div>
        <div class="col-2 text-right">
            <div class="price h5">{$Artikel->Preise->cVKLocalized[0]}</div>
            <button class="btn btn-sm btn-primary add-cart" data-id="{$Artikel->kArtikel}">
                <i class="fa fa-cart-plus"></i> Kaufen
            </button>
        </div>
    </div>
</div>
```

## Bootstrap.php Erweiterungen

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

    fputcsv($out, ['Art.-Nr.', 'Name', 'Preis', 'Lager'], ';');
    // Daten-Implementierung hier

    fclose($out);
    exit;
}
```

## JTL-Wawi Konfiguration

Merkmale für Produkte anlegen:

| Name | Deutsch | Beispiele |
|------|---------|-----------|
| Resistance | Widerstand | 10kΩ, 4.7kΩ |
| Package | Bauform | 0402, 0805 |
| Tolerance | Toleranz | ±1%, ±5% |
| Power | Leistung | 1/8W, 1/4W |
| Voltage | Spannung | 50V, 100V |
