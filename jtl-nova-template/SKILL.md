---
name: jtl-nova-template
description: "JTL-Shop 5 NOVA Template-Entwicklung und Child-Template Anpassungen. Erstellt Child-Templates, passt SCSS/CSS-Stile an, modifiziert Smarty-Blöcke, baut parametrische Produktkataloge (DigiKey-Stil). Verwenden bei: (1) JTL-Shop Child-Template erstellen, (2) SCSS/CSS Themes anpassen, (3) Smarty Templates modifizieren, (4) Umschaltbare Produktansichten (Galerie/Liste/Tabelle), (5) Parametrische Filter und Produktvergleich, (6) CSV/Excel Export. Keywords: JTL-Wawi, NOVA, Bootstrap.php, template.xml, Smarty Blöcke, SCSS Variablen."
---

# JTL-Shop 5 NOVA Template-Entwicklung

## Quick Reference

| Aufgabe | Lösung |
|---------|--------|
| Farben/Schriften ändern | `_variables.scss` überschreiben |
| Layout anpassen | Smarty-Block-Vererbung in `.tpl` |
| Parametrischer Katalog | Templates aus `assets/templates/` kopieren |
| Ansicht wechseln | JavaScript + Session Storage |

## Offizielle Ressourcen

| Ressource | Link |
|-----------|------|
| Child-Template Download | https://build.jtl-shop.de/get/template/NOVAChild-master.zip |
| Entwickler-Dokumentation | https://jtl-shop-mkdocs.readthedocs.io/de/latest/shop_templates/ |
| GitLab Repository | https://gitlab.com/jtl-software/jtl-shop/child-templates/novachild |
| SCC Komponenten | https://gitlab.com/jtl-software/jtl-shop/tools/scc |

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
// meintheme.scss
@import "~bootstrap/scss/functions";
@import "variables";  // Eigene Überschreibungen
@import "~templates/NOVA/themes/base/sass/allstyles";
// Eigene Stile unten
```

Kompilieren: Backend → Plugins → Template-Editor → Theme auswählen → Kompilieren

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

## Häufige Probleme

| Problem | Lösung |
|---------|--------|
| Template nicht sichtbar | `<Name>` in template.xml muss Ordnernamen entsprechen |
| Namespace-Fehler | Namespace in Bootstrap.php = `Template\<Ordnername>` |
| SCSS kompiliert nicht | Cache leeren, Theme-Editor neu laden |
| Smarty-Block wird ignoriert | Pfad in `{extends}` prüfen |
