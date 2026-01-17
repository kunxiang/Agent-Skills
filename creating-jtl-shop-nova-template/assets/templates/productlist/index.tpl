{**
 * Parametric Product Catalog - Main Template
 * Copy to: templates/YourTheme/productlist/index.tpl
 *}
{extends file="{$parent_template_path}/productlist/index.tpl"}

{block name="productlist"}
<div class="parametric-catalog" data-view="{$smarty.session.catalogView|default:'gallery'}">
    
    {include file='snippets/breadcrumb.tpl'}
    
    <div class="catalog-header">
        <div>
            <h1>{$Kategorie->cName}</h1>
            {if $Kategorie->cBeschreibung}<p class="text-muted">{$Kategorie->cBeschreibung|truncate:150}</p>{/if}
        </div>
        <span class="result-count"><strong>{$Suchergebnisse->Artikel->nAnzahl|number_format:0:",":"."}</strong> Produkte</span>
    </div>
    
    {include file="productlist/filter_parametric.tpl"}
    
    <div class="catalog-toolbar">
        <div class="view-switcher btn-group">
            <button class="btn btn-outline-secondary view-btn" data-view="gallery" title="Galerie"><i class="fa fa-th-large"></i></button>
            <button class="btn btn-outline-secondary view-btn" data-view="list" title="Liste"><i class="fa fa-th-list"></i></button>
            <button class="btn btn-outline-secondary view-btn" data-view="table" title="Tabelle"><i class="fa fa-table"></i></button>
        </div>
        <div class="table-tools">
            <button class="btn btn-outline-secondary btn-sm" id="exportBtn"><i class="fa fa-download"></i> Export</button>
            <button class="btn btn-primary btn-sm" id="compareBtn" disabled><i class="fa fa-balance-scale"></i> Vergleichen (<span id="compareCount">0</span>)</button>
        </div>
        <select id="sortSelect" class="form-control form-control-sm ml-auto" style="width:auto" onchange="location.href=this.value">
            {foreach $Suchergebnisse->SortierungSelection as $sort}
            <option value="{$sort->cURL}" {if $sort->nAktiv}selected{/if}>{$sort->cName}</option>
            {/foreach}
        </select>
    </div>
    
    <div class="catalog-content">
        <div class="view-gallery catalog-view">
            <div class="row">
                {foreach $Suchergebnisse->Artikel->elemente as $Artikel}
                <div class="col-6 col-md-4 col-lg-3 col-xl-2 mb-4">{include file='productlist/item_box.tpl'}</div>
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
    
    {if $Suchergebnisse->Artikel->nAnzahl == 0}
    <div class="text-center py-5">
        <i class="fa fa-search fa-4x text-muted mb-3"></i>
        <h4>Keine Produkte gefunden</h4>
        <p class="text-muted">Bitte passen Sie Ihre Filterkriterien an.</p>
        <a href="{$Suchergebnisse->cURLFilterReset}" class="btn btn-outline-primary">Filter zurücksetzen</a>
    </div>
    {/if}
    
    {include file='snippets/pagination.tpl' oPagination=$Suchergebnisse->Seitenzahlen}
</div>

{inline_script}<script src="{$ShopURL}/templates/{$template->getName()}/js/parametric-catalog.js"></script>{/inline_script}
{/block}
