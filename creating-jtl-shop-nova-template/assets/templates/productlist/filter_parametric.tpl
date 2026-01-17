{**
 * Parametric Filter Component
 * Copy to: templates/YourTheme/productlist/filter_parametric.tpl
 *}
{if $Suchergebnisse->MerkmalFilter|@count > 0 || $Suchergebnisse->Herstellerauswahl|@count > 0}
<div class="parametric-filter">
    <div class="filter-row">
        {* Stock filter *}
        <div class="filter-dropdown">
            <button class="filter-btn" data-toggle="dropdown">
                <i class="fa fa-cube"></i> Verfügbarkeit
                {if $Suchergebnisse->nLagerbestandFilter > 0}<span class="badge badge-primary">1</span>{/if}
                <i class="fa fa-chevron-down ml-1"></i>
            </button>
            <div class="filter-dropdown-content">
                <label class="filter-option">
                    <input type="checkbox" name="lf" value="1" {if $Suchergebnisse->nLagerbestandFilter == 1}checked{/if}>
                    <span>Nur auf Lager</span>
                </label>
            </div>
        </div>
        
        {* Manufacturer filter *}
        {if $Suchergebnisse->Herstellerauswahl|@count > 0}
        <div class="filter-dropdown">
            <button class="filter-btn" data-toggle="dropdown">
                Hersteller
                {assign var="hActive" value=0}
                {foreach $Suchergebnisse->Herstellerauswahl as $h}{if $h->nAktiv}{assign var="hActive" value=$hActive+1}{/if}{/foreach}
                {if $hActive > 0}<span class="badge badge-primary">{$hActive}</span>{/if}
                <i class="fa fa-chevron-down ml-1"></i>
            </button>
            <div class="filter-dropdown-content">
                {if $Suchergebnisse->Herstellerauswahl|@count > 10}
                <input type="text" class="form-control form-control-sm filter-search" placeholder="Suchen...">
                {/if}
                <div class="filter-options">
                    {foreach $Suchergebnisse->Herstellerauswahl as $h}
                    <label class="filter-option">
                        <input type="checkbox" name="hf[]" value="{$h->kHersteller}" {if $h->nAktiv}checked{/if}>
                        <span>{$h->cName}</span><small>({$h->nAnzahl})</small>
                    </label>
                    {/foreach}
                </div>
            </div>
        </div>
        {/if}
        
        {* Merkmal filters *}
        {foreach $Suchergebnisse->MerkmalFilter as $filter}
        <div class="filter-dropdown">
            <button class="filter-btn" data-toggle="dropdown">
                {$filter->cName}
                {assign var="fActive" value=0}
                {foreach $filter->oMerkmalWert_arr as $v}{if $v->nAktiv}{assign var="fActive" value=$fActive+1}{/if}{/foreach}
                {if $fActive > 0}<span class="badge badge-primary">{$fActive}</span>{/if}
                <i class="fa fa-chevron-down ml-1"></i>
            </button>
            <div class="filter-dropdown-content">
                {if $filter->oMerkmalWert_arr|@count > 10}
                <input type="text" class="form-control form-control-sm filter-search" placeholder="Suchen...">
                {/if}
                <div class="filter-options">
                    {foreach $filter->oMerkmalWert_arr as $value}
                    <label class="filter-option">
                        <input type="checkbox" name="mf[{$filter->kMerkmal}][]" value="{$value->kMerkmalWert}" {if $value->nAktiv}checked{/if}>
                        <span>{$value->cWert}</span><small>({$value->nAnzahl})</small>
                    </label>
                    {/foreach}
                </div>
            </div>
        </div>
        {/foreach}
    </div>
    
    {* Active filter tags *}
    {assign var="hasActive" value=false}
    {foreach $Suchergebnisse->MerkmalFilter as $f}{foreach $f->oMerkmalWert_arr as $v}{if $v->nAktiv}{assign var="hasActive" value=true}{/if}{/foreach}{/foreach}
    {foreach $Suchergebnisse->Herstellerauswahl as $h}{if $h->nAktiv}{assign var="hasActive" value=true}{/if}{/foreach}
    
    {if $hasActive || $Suchergebnisse->nLagerbestandFilter > 0}
    <div class="active-filters">
        <span class="text-muted mr-2"><i class="fa fa-filter"></i> Aktive Filter:</span>
        {if $Suchergebnisse->nLagerbestandFilter > 0}
        <span class="filter-tag">Auf Lager<a href="?lf=0">×</a></span>
        {/if}
        {foreach $Suchergebnisse->Herstellerauswahl as $h}
            {if $h->nAktiv}<span class="filter-tag">{$h->cName}<a href="{$h->cURLPfad}">×</a></span>{/if}
        {/foreach}
        {foreach $Suchergebnisse->MerkmalFilter as $f}
            {foreach $f->oMerkmalWert_arr as $v}
                {if $v->nAktiv}<span class="filter-tag">{$f->cName}: {$v->cWert}<a href="{$v->cURLPfad}">×</a></span>{/if}
            {/foreach}
        {/foreach}
        <a href="{$Suchergebnisse->cURLFilterReset}" class="ml-2 text-danger">Alle zurücksetzen</a>
    </div>
    {/if}
</div>
{/if}
