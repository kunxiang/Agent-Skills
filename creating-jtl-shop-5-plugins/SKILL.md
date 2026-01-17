---
name: creating-jtl-shop-5-plugins
description: "JTL-Shop 5 Plugin-Entwicklung und Erstellung. Erstellt vollständige Plugins mit info.xml, Bootstrap.php, Hooks, Adminmenü und Frontend-Integration. Verwenden bei: (1) JTL-Shop 5 Plugin von Grund auf erstellen, (2) Plugin-Struktur und info.xml anlegen, (3) Bootstrap.php mit Hooks und Events implementieren, (4) Backend-Einstellungen und Adminmenü hinzufügen, (5) Frontend-Templates und JavaScript einbinden. Keywords: JTL-Shop 5, Plugin, info.xml, Bootstrap.php, Hooks, Events, Adminmenu, PSR-4 Namespace."
---

# JTL-Shop 5 Plugin-Entwicklung

## Offizielle Ressourcen

| Ressource | Link |
|-----------|------|
| Entwickler-Docs | https://jtl-devguide.readthedocs.io/projects/jtl-shop/de/latest/shop_plugins/ |
| info.xml Referenz | https://jtl-devguide.readthedocs.io/projects/jtl-shop/de/latest/shop_plugins/infoxml.html |
| Hook-Liste | https://jtl-shop-mkdocs.readthedocs.io/de/latest/shop_plugins/hook_list.html |
| Test-Plugin (Vorlage) | https://gitlab.com/jtl-software/jtl-shop/plugins/jtl_test |
| JTL-Forum | https://forum.jtl-software.de/ |

## Quick Start

```bash
# 1. Plugin-Verzeichnis erstellen
mkdir -p <SHOP-ROOT>/plugins/MeineFirma_MeinPlugin

# 2. Minimale Dateien erstellen: info.xml + Bootstrap.php

# 3. Im Backend installieren: Plugins → Pluginverwaltung → Verfügbar
```

## Plugin-Struktur (JTL-Shop 5)

```
plugins/MeineFirma_MeinPlugin/
├── info.xml                 # Pflicht: Plugin-Manifest
├── Bootstrap.php            # Pflicht: Hauptklasse mit Hooks
├── adminmenu/               # Optional: Backend-Seiten
│   ├── templates/           # Smarty-Templates für Admin
│   └── settings.php         # Einstellungsseite
├── frontend/                # Optional: Frontend-Ausgabe
│   └── template/            # Smarty-Templates
├── src/                     # Optional: PSR-4 Klassen
│   └── Services/
├── css/                     # Optional: Stylesheets
├── js/                      # Optional: JavaScript
└── Migrations/              # Optional: Datenbank-Migrationen
```

**Wichtig**: Ordnername = PluginID in info.xml (z.B. `MeineFirma_MeinPlugin`)

## Quick Reference

| Aufgabe | Lösung |
|---------|--------|
| Plugin-ID festlegen | Nur a-z, A-Z, 0-9, Unterstrich. Kein Punkt/Bindestrich |
| Namespace | `Plugin\<PluginID>` (automatisch ab Shop 5.0) |
| Hook registrieren | `$dispatcher->listen(HOOK_ID, [$this, 'method'])` |
| Admin-Einstellungen | `<PluginAdminMenu>` in info.xml + PHP-Datei |
| Frontend-Template | `frontend/template/` Ordner, extends mit Smarty |
| Dev-Modus | `define('PLUGIN_DEV_MODE', true);` in config.JTL-Shop.ini |

## Minimale info.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<jtlshopplugin>
    <Name>Mein Plugin</Name>
    <Description>Beschreibung des Plugins</Description>
    <Author>Ihre Firma</Author>
    <URL>https://ihre-website.de</URL>
    <PluginID>MeineFirma_MeinPlugin</PluginID>
    <XMLVersion>100</XMLVersion>
    <MinShopVersion>5.0.0</MinShopVersion>
    <CreateDate>2024-01-15</CreateDate>
    <Version>1.0.0</Version>
    <Install>
        <FlushTags>CACHING_GROUP_CORE</FlushTags>
    </Install>
</jtlshopplugin>
```

## Minimale Bootstrap.php

```php
<?php
declare(strict_types=1);

namespace Plugin\MeineFirma_MeinPlugin;

use JTL\Events\Dispatcher;
use JTL\Plugin\Bootstrapper;

class Bootstrap extends Bootstrapper
{
    public function boot(Dispatcher $dispatcher): void
    {
        parent::boot($dispatcher);

        // Hook registrieren
        $dispatcher->listen('shop.hook.' . \HOOK_SMARTY_OUTPUTFILTER, [$this, 'onOutput']);
    }

    public function onOutput(array $args): void
    {
        // Hook-Logik hier
    }

    public function installed(): void
    {
        parent::installed();
        // Nach Installation ausführen
    }

    public function enabled(): void
    {
        parent::enabled();
        // Nach Aktivierung ausführen
    }
}
```

## Häufig verwendete Hooks

| Hook-ID | Konstante | Beschreibung |
|---------|-----------|--------------|
| 140 | `HOOK_SMARTY_OUTPUTFILTER` | Vor HTML-Ausgabe (universell) |
| 131 | `HOOK_SMARTY_INC` | Smarty-Variablen modifizieren |
| 47 | `HOOK_ARTIKEL_CLASS_FUELLEARTIKEL` | Artikel-Objekt erweitern |
| 181 | `HOOK_BESTELLVORGANG_PAGE` | Checkout-Seite |
| 93 | `HOOK_WARENKORB_CLASS_FUEGEEIN` | Artikel in Warenkorb |
| 50 | `HOOK_KATEGORIE_CLASS_LOADFROMDB` | Kategorie laden |

**Hinweis**: Hook-IDs können je nach Shop-Version variieren. Immer offizielle Hook-Liste prüfen.

## Admin-Einstellungen hinzufügen

In info.xml:

```xml
<Install>
    <PluginAdminMenu>
        <Customlink sort="1">
            <Name>Einstellungen</Name>
            <Filename>settings.php</Filename>
        </Customlink>
    </PluginAdminMenu>
    <PluginSettings>
        <Setting type="text" sort="1" name="api_key">
            <Name>API-Schlüssel</Name>
            <Description>Ihr API-Schlüssel für den Service</Description>
            <DefaultValue></DefaultValue>
        </Setting>
        <Setting type="checkbox" sort="2" name="active">
            <Name>Aktiv</Name>
            <DefaultValue>0</DefaultValue>
        </Setting>
    </PluginSettings>
</Install>
```

Setting-Typen: `text`, `textarea`, `checkbox`, `selectbox`, `radio`, `color`, `password`

Einstellungen in PHP lesen:

```php
$value = $this->getPlugin()->getConfig()->getValue('api_key');
```

## Frontend-Hook Beispiel

Smarty-Variable injizieren:

```php
public function boot(Dispatcher $dispatcher): void
{
    parent::boot($dispatcher);

    $dispatcher->listen('shop.hook.' . \HOOK_SMARTY_INC, function(array $args) {
        $smarty = $args['smarty'];
        $smarty->assign('meineDaten', $this->loadMyData());
    });
}
```

Im Template verwenden:

```smarty
{if isset($meineDaten)}
    <div class="mein-plugin">{$meineDaten}</div>
{/if}
```

## EventDispatcher (Alternative zu Hooks)

Ab JTL-Shop 5.x bevorzugt:

```php
use JTL\Events\Event;

$dispatcher->listen(Event::MAP_CRONJOB_TYPE, function(array &$args) {
    $args['jobs']['mein_job'] = MeinCronJob::class;
});

$dispatcher->listen('backend.notification', function(array &$args) {
    $args['notifications'][] = [
        'type' => 'warning',
        'message' => 'Plugin-Warnung!'
    ];
});
```

## Datenbank-Migration

```
Migrations/Migration20240115120000.php
```

```php
<?php
namespace Plugin\MeineFirma_MeinPlugin\Migrations;

use JTL\Plugin\Migration;
use JTL\Update\IMigration;

class Migration20240115120000 extends Migration implements IMigration
{
    public function up(): void
    {
        $this->execute("CREATE TABLE IF NOT EXISTS plugin_meinplugin_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            value TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )");
    }

    public function down(): void
    {
        $this->execute("DROP TABLE IF EXISTS plugin_meinplugin_data");
    }
}
```

## Referenzen

- **info.xml Vollständig**: [references/info-xml.md](references/info-xml.md) - Alle XML-Elemente
- **Bootstrap & Hooks**: [references/bootstrap-hooks.md](references/bootstrap-hooks.md) - Lifecycle und Events
- **Plugin-Architektur**: [references/plugin-architecture.md](references/plugin-architecture.md) - Verzeichnisse und Klassen
- **Troubleshooting**: [references/troubleshooting.md](references/troubleshooting.md) - Häufige Fehler

## Assets (Vorlagen)

| Datei | Zweck |
|-------|-------|
| `assets/templates/info.xml` | Vollständige info.xml Vorlage |
| `assets/templates/Bootstrap.php` | Erweiterte Bootstrap.php Vorlage |

## Häufige Fehler

| Problem | Lösung |
|---------|--------|
| Plugin nicht sichtbar | Ordnername ≠ PluginID → Muss identisch sein |
| Namespace-Fehler | `Plugin\<PluginID>` verwenden, nicht Template\ |
| Hook wird nicht aufgerufen | Hook-ID prüfen, Event-Format: `shop.hook.` + ID |
| info.xml Änderungen ignoriert | Dev-Modus aktivieren oder Plugin neu installieren |
| Klasse nicht gefunden | PSR-4 Namespace prüfen, Autoloader in composer.json |
| Admin-Tab fehlt | `<Customlink>` + passende PHP-Datei in adminmenu/ |

## Entwickler-Tipps

1. **Dev-Modus aktivieren**: `define('PLUGIN_DEV_MODE', true);` in `includes/config.JTL-Shop.ini`
2. **Cache leeren**: Backend → System → Cache → Alle Caches leeren
3. **Logging nutzen**: `Shop::Container()->getLogService()->notice('Debug: ' . $var);`
4. **Test-Plugin als Vorlage**: https://gitlab.com/jtl-software/jtl-shop/plugins/jtl_test
