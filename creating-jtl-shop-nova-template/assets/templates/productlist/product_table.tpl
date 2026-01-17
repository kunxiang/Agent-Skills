{**
 * Parametric Table View
 * Copy to: templates/YourTheme/productlist/product_table.tpl
 *}
<div class="product-table-wrapper">
    <table class="product-table table table-hover table-sm">
        <thead>
            <tr>
                <th style="width:40px"><input type="checkbox" id="selectAll" title="Alle auswählen"></th>
                <th style="width:60px">Bild</th>
                <th class="sortable" data-sort="name">Produkt</th>
                <th style="width:100px">Art.-Nr.</th>
                {foreach $Suchergebnisse->MerkmalFilter as $m}
                <th class="sortable" data-sort="param_{$m->kMerkmal}">{$m->cName}</th>
                {/foreach}
                <th class="sortable text-right" data-sort="stock" style="width:80px">Lager</th>
                <th class="sortable text-right" data-sort="price" style="width:100px">Preis</th>
                <th style="width:80px">Aktion</th>
            </tr>
        </thead>
        <tbody>
            {foreach $Suchergebnisse->Artikel->elemente as $Artikel}
            <tr data-id="{$Artikel->kArtikel}" data-price="{$Artikel->Preise->fVKNetto}" data-stock="{$Artikel->fLagerbestand}">
                <td><input type="checkbox" class="compare-cb" value="{$Artikel->kArtikel}"></td>
                <td>
                    <a href="{$Artikel->cURL}">
                        <img src="{$Artikel->Bilder[0]->cPfadMini}" alt="{$Artikel->cName|escape}" loading="lazy">
                    </a>
                </td>
                <td data-label="Produkt">
                    <a href="{$Artikel->cURL}" class="font-weight-bold">{$Artikel->cName}</a>
                    {if $Artikel->cHersteller}<br><small class="text-muted">{$Artikel->cHersteller}</small>{/if}
                </td>
                <td data-label="Art.-Nr."><code>{$Artikel->cArtNr}</code></td>
                {foreach $Suchergebnisse->MerkmalFilter as $m}
                <td data-label="{$m->cName}" data-merkmal="{$m->kMerkmal}">
                    {foreach $Artikel->oMerkmale_arr as $am}
                        {if $am->kMerkmal == $m->kMerkmal}{$am->cWert}{/if}
                    {/foreach}
                </td>
                {/foreach}
                <td data-label="Lager" class="text-right">
                    {if $Artikel->fLagerbestand > 0}
                    <span class="text-success"><i class="fa fa-check-circle"></i> {$Artikel->fLagerbestand|number_format:0:",":"."}</span>
                    {else}
                    <span class="text-danger"><i class="fa fa-times-circle"></i> 0</span>
                    {/if}
                </td>
                <td data-label="Preis" class="text-right font-weight-bold text-primary">{$Artikel->Preise->cVKLocalized[0]}</td>
                <td class="text-center">
                    {if $Artikel->nIstVater == 0 && $Artikel->fLagerbestand > 0}
                    <button class="btn btn-sm btn-primary" title="In den Warenkorb"><i class="fa fa-cart-plus"></i></button>
                    {else}
                    <a href="{$Artikel->cURL}" class="btn btn-sm btn-outline-secondary" title="Details"><i class="fa fa-eye"></i></a>
                    {/if}
                </td>
            </tr>
            {/foreach}
        </tbody>
    </table>
</div>
