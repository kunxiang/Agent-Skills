---
name: creating-jtl-shop-nova-template
description: "JTL-Shop 5 NOVA Template-Entwicklung und Child-Template Anpassungen. Erstellt Child-Templates, passt SCSS/CSS-Stile an, modifiziert Smarty-Blöcke, baut parametrische Produktkataloge (DigiKey-Stil). Verwenden bei: (1) JTL-Shop Child-Template erstellen, (2) SCSS/CSS Themes anpassen, (3) Smarty Templates modifizieren, (4) Umschaltbare Produktansichten (Galerie/Liste/Tabelle), (5) Parametrische Filter und Produktvergleich, (6) CSV/Excel Export. Keywords: JTL-Wawi, NOVA, Bootstrap.php, template.xml, Smarty Blöcke, SCSS Variablen, NOVAChild."
---

# JTL-Shop 5 NOVA Template-Entwicklung

## Quick Start

```bash
# 1. NOVAChild-Vorlage herunterladen
wget https://build.jtl-shop.de/get/template/NOVAChild-master.zip

# 2. Entpacken in templates/
unzip NOVAChild-master.zip -d /shop/templates/

# 3. Im Backend aktivieren: Darstellung → Templates → NOVAChild
```

## Offizielle Ressourcen

| Ressource | Link |
|-----------|------|
| NOVAChild Download | https://build.jtl-shop.de/get/template/NOVAChild-master.zip |
| GitLab NOVAChild | https://gitlab.com/jtl-software/jtl-shop/child-templates/novachild |
| Entwickler-Docs | https://jtl-devguide.readthedocs.io/projects/jtl-shop/de/latest/shop_templates/ |
| JTL-Guide | https://guide.jtl-software.com/jtl-shop/darstellung/nova-template/ |
| JTL-Forum | https://forum.jtl-software.de/ |

## Quick Reference

| Aufgabe | Lösung |
|---------|--------|
| Farben/Schriften ändern | `themes/my-nova/sass/_variables.scss` |
| Layout anpassen | Smarty-Block `{extends}` + `{block}` |
| JavaScript hinzufügen | `footer.tpl` Block mit `async` Attribut |
| Parametrischer Katalog | Templates aus `assets/templates/` kopieren |

## Child-Template Struktur

```
templates/MeinTheme/
├── Bootstrap.php          # PHP-Klasse (Namespace = Ordnername)
├── template.xml           # Konfiguration (<Name> = Ordnername)
├── themes/meintheme/sass/
│   ├── _variables.scss    # Variable Überschreibungen
│   └── meintheme.scss     # Haupt-SCSS (importiert NOVA + eigenes)
└── productlist/           # Template-Überschreibungen
```

**Wichtig**: Ab JTL-Shop 5.0 muss der Ordnername dem `<Name>` in template.xml entsprechen.

### template.xml

```xml
<?xml version="1.0" encoding="utf-8"?>
<Template isFullResponsive="true">
    <Name>MeinTheme</Name>
    <Parent>NOVA</Parent>
    <Author>Ihr Name</Author>
    <Version>1.0.0</Version>
    <ShopVersion>5.0.0</ShopVersion>
</Template>
```

### Bootstrap.php

```php
<?php
declare(strict_types=1);
namespace Template\MeinTheme;  // Muss dem Ordnernamen entsprechen

class Bootstrap extends \Template\NOVA\Bootstrap
{
    public function boot(): void
    {
        parent::boot();  // Immer zuerst Parent aufrufen
        // Eigene Smarty-Funktionen hier registrieren
    }
}
```

### SCSS-Struktur

```scss
// meintheme.scss - WICHTIG: Reihenfolge beachten!
@import "~bootstrap/scss/functions";
@import "variables";  // ZUERST eigene Variablen überschreiben
@import "~templates/NOVA/themes/base/sass/allstyles";  // DANN NOVA laden
// Eigene Stile UNTEN hinzufügen
```

**Kompilieren**: Backend → Plugins → JTL Theme-Editor → Theme auswählen → "Theme kompilieren"

**Wichtig**: Nach Änderungen immer Template-Cache leeren (Backend → Einstellungen → Template Cache)

## Smarty-Block-Vererbung

```smarty
{extends file="{$parent_template_path}/productlist/index.tpl"}

{block name="productlist"}
    {* Block-Inhalt ersetzen *}
{/block}

{block name="head-resources" append}
    {* An Block anhängen *}
{/block}

{block name="footer" prepend}
    {* Vor Block einfügen *}
{/block}
```

### Wichtige Variablen

| Variable | Beschreibung |
|----------|--------------|
| `$Artikel` | Produkt-Objekt |
| `$Kategorie` | Kategorie-Objekt |
| `$Suchergebnisse` | Such-/Listenergebnisse |
| `$ShopURL` | Shop-Basis-URL |
| `$Einstellungen` | Shop-Einstellungen |

## Parametrischer Produktkatalog

DigiKey-Stil mit umschaltbaren Ansichten (Galerie/Liste/Tabelle):

1. Templates aus `assets/templates/productlist/` kopieren
2. `assets/js/parametric-catalog.js` kopieren
3. `assets/themes/_parametric-catalog.scss` kopieren
4. IO-Handler in Bootstrap.php für View-Persistenz hinzufügen

### Ansichten-Wechsel (Kern)

```javascript
switchView(view) {
    document.querySelectorAll('.catalog-view').forEach(v => v.style.display = 'none');
    document.querySelector(`.view-${view}`).style.display = '';
    fetch('/io.php', {
        method: 'POST',
        body: `io={"name":"setCatalogView","params":["${view}"]}`
    });
}
```

### Hauptfunktionen

- **Galerie**: Karten-Grid, große Bilder
- **Liste**: Horizontales Layout mit 6 Parametern
- **Tabelle**: Alle Parameter, sortierbare Spalten, CSV/Excel-Export
- **Filter**: Multi-Select Dropdowns mit Suche
- **Vergleich**: Bis zu 4 Produkte auswählen
- **Tastatur**: Alt+1/2/3 für Ansichtswechsel

## Referenzen

- **SCSS-Variablen**: [references/scss-variables.md](references/scss-variables.md) - Bootstrap/NOVA Variablen
- **Smarty-Blöcke**: [references/smarty-blocks.md](references/smarty-blocks.md) - Verfügbare Blöcke
- **Katalog-Templates**: [references/parametric-catalog.md](references/parametric-catalog.md) - Smarty-Templates
- **Katalog-JavaScript**: [references/parametric-catalog-js.md](references/parametric-catalog-js.md) - JS-Klasse
- **Katalog-Stile**: [references/parametric-catalog-styles.md](references/parametric-catalog-styles.md) - SCSS

## Assets

| Datei | Zweck |
|-------|-------|
| `assets/templates/productlist/` | Fertige Template-Dateien |
| `assets/js/parametric-catalog.js` | JavaScript-Funktionalität |
| `assets/themes/_parametric-catalog.scss` | Katalog-Stile |
| `assets/Bootstrap.php` | PHP mit IO-Handler und Export |

## JavaScript einbinden

Scripts in `footer.tpl` laden mit `async` Attribut:

```smarty
{extends file="{$parent_template_path}/layout/footer.tpl"}

{block name='layout-footer-js' append}
    <script src="{$ShopURL}/templates/MeinTheme/js/custom.js" async></script>
{/block}
```

## Plugin-basierte Block-Überschreibung

Templates können auch per Plugin überschrieben werden:

```
<pluginverzeichnis>/frontend/templates/productdetails/variation.tpl
```

Der Block wird im Plugin-Template erweitert (gleiche Struktur wie Child-Template).

## Häufige Probleme

| Problem | Lösung |
|---------|--------|
| Template nicht sichtbar | `<Name>` in template.xml = Ordnername |
| Namespace-Fehler | `Template\<Ordnername>` in Bootstrap.php |
| SCSS kompiliert nicht | Cache leeren + Theme-Editor neu laden |
| Smarty-Block ignoriert | `{extends}` Pfad prüfen, `{$parent_template_path}` verwenden |
| Variablen wirken nicht | Import-Reihenfolge: variables VOR allstyles |
| Änderungen nicht sichtbar | Template-Cache im Backend leeren |
