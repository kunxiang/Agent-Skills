{**
 * List View Product Item
 * Copy to: templates/YourTheme/productlist/item_list.tpl
 *}
<div class="product-list-item">
    <div class="product-image">
        <a href="{$Artikel->cURL}">
            <img src="{$Artikel->Bilder[0]->cPfadKlein}" alt="{$Artikel->cName|escape}" loading="lazy">
        </a>
    </div>
    <div class="product-info">
        <h3><a href="{$Artikel->cURL}">{$Artikel->cName}</a></h3>
        {if $Artikel->cHersteller}<small class="text-muted">{$Artikel->cHersteller}</small>{/if}
        <div class="text-muted">Art.-Nr.: {$Artikel->cArtNr}</div>
        {if $Artikel->oMerkmale_arr|@count > 0}
        <div class="product-params">
            {foreach $Artikel->oMerkmale_arr as $m name=params}
                {if $smarty.foreach.params.index < 6}
                <span class="badge badge-light mr-1">{$m->cName}: {$m->cWert}</span>
                {/if}
            {/foreach}
            {if $Artikel->oMerkmale_arr|@count > 6}
            <a href="{$Artikel->cURL}" class="badge badge-secondary">+{$Artikel->oMerkmale_arr|@count - 6} mehr</a>
            {/if}
        </div>
        {/if}
    </div>
    <div class="product-buy text-right">
        <div class="product-price">{$Artikel->Preise->cVKLocalized[0]}</div>
        <div class="product-stock my-2">
            {if $Artikel->fLagerbestand > 0}
            <span class="text-success"><i class="fa fa-check-circle"></i> {$Artikel->fLagerbestand|number_format:0:",":"."} auf Lager</span>
            {else}
            <span class="text-danger"><i class="fa fa-times-circle"></i> Nicht verfügbar</span>
            {/if}
        </div>
        {if $Artikel->nIstVater == 0 && $Artikel->fLagerbestand > 0}
        <button class="btn btn-primary btn-sm"><i class="fa fa-cart-plus"></i> In den Warenkorb</button>
        {else}
        <a href="{$Artikel->cURL}" class="btn btn-outline-primary btn-sm">Details ansehen</a>
        {/if}
    </div>
</div>
