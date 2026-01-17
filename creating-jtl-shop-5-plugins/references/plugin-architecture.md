# Plugin-Architektur

Dieses Dokument beschreibt die vollständige Verzeichnisstruktur und Architektur eines JTL-Shop 5 Plugins.

## Verzeichnisstruktur

### Minimal-Plugin

```
plugins/MeineFirma_MeinPlugin/
├── info.xml                  # Pflicht: Plugin-Manifest
└── Bootstrap.php             # Pflicht: Hauptklasse
```

### Standard-Plugin

```
plugins/MeineFirma_MeinPlugin/
├── info.xml                  # Plugin-Manifest
├── Bootstrap.php             # Hauptklasse
├── adminmenu/                # Backend-Seiten
│   ├── templates/            # Admin-Templates (Smarty)
│   │   └── config.tpl
│   └── config.php            # Admin-Seite Logik
├── frontend/                 # Frontend
│   └── template/             # Frontend-Templates
│       └── widget.tpl
├── css/                      # Stylesheets
│   └── styles.css
└── js/                       # JavaScript
    └── main.js
```

### Vollständiges Plugin

```
plugins/MeineFirma_MeinPlugin/
├── info.xml                  # Plugin-Manifest
├── Bootstrap.php             # Hauptklasse mit Hooks
│
├── src/                      # PSR-4 Klassen
│   ├── Services/             # Service-Klassen
│   │   ├── ApiService.php
│   │   └── DataService.php
│   ├── Models/               # Datenmodelle
│   │   └── CustomEntity.php
│   ├── Controllers/          # Controller
│   │   └── AdminController.php
│   └── Helpers/              # Hilfsfunktionen
│       └── Formatter.php
│
├── adminmenu/                # Backend-Bereich
│   ├── templates/            # Admin-Templates
│   │   ├── config.tpl
│   │   ├── stats.tpl
│   │   └── logs.tpl
│   ├── config.php            # Konfigurationsseite
│   ├── stats.php             # Statistik-Seite
│   └── logs.php              # Log-Viewer
│
├── frontend/                 # Frontend-Bereich
│   ├── template/             # Frontend-Templates
│   │   ├── widget.tpl
│   │   └── page.tpl
│   └── page.php              # Frontend-Seite (wenn FrontendLink definiert)
│
├── Migrations/               # Datenbank-Migrationen
│   ├── Migration20240101120000.php
│   └── Migration20240115140000.php
│
├── Crons/                    # Cron-Job Klassen
│   └── SyncJob.php
│
├── Widgets/                  # Dashboard-Widgets
│   └── StatsWidget.php
│
├── Portlets/                 # OPC Portlets
│   └── CustomPortlet.php
│
├── PaymentMethods/           # Zahlungsarten
│   └── CustomPayment.php
│
├── locale/                   # Übersetzungen
│   ├── de-DE/
│   │   └── base.mo
│   └── en-GB/
│       └── base.mo
│
├── css/                      # Stylesheets
│   ├── frontend.css
│   └── admin.css
│
├── js/                       # JavaScript
│   ├── frontend.js
│   └── admin.js
│
├── vendor/                   # Composer Dependencies (optional)
│   └── autoload.php
│
└── composer.json             # Composer Config (optional)
```

## Namespaces

Ab JTL-Shop 5.0 erhält jedes Plugin automatisch einen PSR-4 Namespace:

```
Plugin\<PluginID>
```

### Beispiele

| PluginID | Namespace |
|----------|-----------|
| `MeineFirma_MeinPlugin` | `Plugin\MeineFirma_MeinPlugin` |
| `Beispiel_DemoPlugin` | `Plugin\Beispiel_DemoPlugin` |

### Verwendung

```php
<?php
// Bootstrap.php
namespace Plugin\MeineFirma_MeinPlugin;

// src/Services/ApiService.php
namespace Plugin\MeineFirma_MeinPlugin\Services;

// src/Models/CustomEntity.php
namespace Plugin\MeineFirma_MeinPlugin\Models;
```

## Admin-Seiten

### PHP-Datei (adminmenu/config.php)

```php
<?php
declare(strict_types=1);

use JTL\Shop;
use JTL\Smarty\JTLSmarty;

/** @var \JTL\Plugin\PluginInterface $plugin */
/** @var JTLSmarty $smarty */
/** @var \JTL\DB\DbInterface $db */

// Plugin-Konfiguration
$config = $plugin->getConfig();
$apiKey = $config->getValue('api_key');

// POST-Verarbeitung
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (isset($_POST['saveSettings'])) {
        // Einstellungen speichern
        $config->setValue('api_key', $_POST['api_key'] ?? '');
        Shop::Container()->getAlertService()->addSuccess('Einstellungen gespeichert');
    }
}

// Daten für Template
$smarty->assign('apiKey', $apiKey);
$smarty->assign('pluginUrl', $plugin->getPaths()->getBaseURL());
```

### Smarty-Template (adminmenu/templates/config.tpl)

```smarty
{include file='tpl_inc/header.tpl'}

<div class="card">
    <div class="card-header">
        <h3>Plugin-Konfiguration</h3>
    </div>
    <div class="card-body">
        <form method="post">
            {$jtl_token}

            <div class="form-group">
                <label for="api_key">API-Schlüssel</label>
                <input type="text" class="form-control" id="api_key"
                       name="api_key" value="{$apiKey|escape:'html'}">
            </div>

            <button type="submit" name="saveSettings" class="btn btn-primary">
                Speichern
            </button>
        </form>
    </div>
</div>

{include file='tpl_inc/footer.tpl'}
```

## Frontend-Seiten

### Definition in info.xml

```xml
<Install>
    <FrontendLink>
        <Filename>meine_seite.php</Filename>
        <Name>Meine Seite</Name>
        <VisibleName>Öffentlicher Titel</VisibleName>
        <TemplateFile>meine_seite.tpl</TemplateFile>
        <NoFollow>0</NoFollow>
        <LinkGroup>hidden</LinkGroup>
    </FrontendLink>
</Install>
```

### PHP-Datei (frontend/meine_seite.php)

```php
<?php
declare(strict_types=1);

use JTL\Shop;

/** @var \JTL\Plugin\PluginInterface $plugin */
/** @var \JTL\Smarty\JTLSmarty $smarty */

// Daten laden
$data = Shop::Container()->getDB()->getObjects(
    'SELECT * FROM tartikel LIMIT 10'
);

// An Template übergeben
$smarty->assign('produkte', $data);
$smarty->assign('pluginConfig', $plugin->getConfig()->getAll());
```

### Template (frontend/template/meine_seite.tpl)

```smarty
{extends file="layout/index.tpl"}

{block name="content"}
    <div class="container mein-plugin-seite">
        <h1>{$cTitel}</h1>

        {foreach $produkte as $produkt}
            <div class="produkt-item">
                <h3>{$produkt->cName}</h3>
                <p>{$produkt->cBeschreibung}</p>
            </div>
        {/foreach}
    </div>
{/block}
```

## Migrations

### Dateiname-Konvention

```
Migration[YYYYMMDDHHMMSS].php
```

Beispiel: `Migration20240115120000.php`

### Migration-Klasse

```php
<?php
declare(strict_types=1);

namespace Plugin\MeineFirma_MeinPlugin\Migrations;

use JTL\Plugin\Migration;
use JTL\Update\IMigration;

class Migration20240115120000 extends Migration implements IMigration
{
    public function getAuthor(): string
    {
        return 'Meine Firma';
    }

    public function getDescription(): string
    {
        return 'Erstellt die Haupt-Datentabelle';
    }

    public function up(): void
    {
        $this->execute("
            CREATE TABLE IF NOT EXISTS plugin_meinplugin_entries (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                content TEXT,
                status ENUM('draft', 'published') DEFAULT 'draft',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_status (status)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ");
    }

    public function down(): void
    {
        $this->execute("DROP TABLE IF EXISTS plugin_meinplugin_entries");
    }
}
```

## Cron-Jobs

### Klassen-Definition

```php
<?php
// Crons/SyncJob.php
declare(strict_types=1);

namespace Plugin\MeineFirma_MeinPlugin\Crons;

use JTL\Cron\Job;
use JTL\Cron\JobInterface;
use JTL\Shop;

class SyncJob extends Job implements JobInterface
{
    public function start(): void
    {
        // Job-Logik
        $this->log('Sync gestartet');

        try {
            $this->processSync();
            $this->setFinished(true);
        } catch (\Exception $e) {
            $this->log('Fehler: ' . $e->getMessage(), 'error');
            $this->setFinished(false);
        }
    }

    private function processSync(): void
    {
        // Synchronisationslogik
    }

    private function log(string $message, string $level = 'info'): void
    {
        Shop::Container()->getLogService()->{$level}(
            '[MeinPlugin Sync] ' . $message
        );
    }
}
```

## Dashboard-Widgets

```php
<?php
// Widgets/StatsWidget.php
declare(strict_types=1);

namespace Plugin\MeineFirma_MeinPlugin\Widgets;

use JTL\Backend\AdminWidget\Widget;
use JTL\DB\DbInterface;
use JTL\Smarty\JTLSmarty;

class StatsWidget extends Widget
{
    public function getContent(JTLSmarty $smarty, DbInterface $db): string
    {
        $stats = $db->getSingleObject(
            'SELECT COUNT(*) as total FROM plugin_meinplugin_entries'
        );

        $smarty->assign('widgetStats', $stats);

        return $smarty->fetch('widgets/stats_widget.tpl');
    }
}
```

## Composer-Integration

### composer.json

```json
{
    "name": "meinefirma/mein-plugin",
    "description": "Mein JTL-Shop 5 Plugin",
    "type": "jtl-shop-plugin",
    "autoload": {
        "psr-4": {
            "Plugin\\MeineFirma_MeinPlugin\\": "src/"
        }
    },
    "require": {
        "php": ">=7.4"
    }
}
```

### Bootstrap mit Composer-Autoloader

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

        // Composer Autoloader laden
        $autoloader = $this->getPlugin()->getPaths()->getBasePath() . '/vendor/autoload.php';
        if (file_exists($autoloader)) {
            require_once $autoloader;
        }

        // Hooks registrieren...
    }
}
```

## Best Practices

1. **Trennung von Logik**: Business-Logik in `src/` Klassen auslagern
2. **Dependency Injection**: Shop-Container nutzen statt globale Variablen
3. **Namespaces**: Konsistent PSR-4 Namespaces verwenden
4. **Migrations**: Datenbank-Änderungen immer über Migrations
5. **Caching**: Cache für aufwändige Operationen nutzen
6. **Logging**: Aussagekräftige Log-Nachrichten für Debugging
7. **Übersetzungen**: Texte in locale/ für Mehrsprachigkeit
