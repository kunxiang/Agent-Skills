# Bootstrap.php und Hooks Referenz

Die Bootstrap.php ist die Hauptklasse eines JTL-Shop 5 Plugins. Sie steuert den gesamten Lebenszyklus und registriert Hooks und Events.

## Grundstruktur

```php
<?php
declare(strict_types=1);

namespace Plugin\MeineFirma_MeinPlugin;

use JTL\Events\Dispatcher;
use JTL\Plugin\Bootstrapper;

class Bootstrap extends Bootstrapper
{
    /**
     * Wird bei jedem Request aufgerufen (wenn Plugin aktiv)
     */
    public function boot(Dispatcher $dispatcher): void
    {
        parent::boot($dispatcher);

        // Hooks und Events hier registrieren
    }
}
```

## Lifecycle-Methoden

```php
class Bootstrap extends Bootstrapper
{
    /**
     * Nach Installation des Plugins
     */
    public function installed(): void
    {
        parent::installed();
        // Einmalige Setup-Aufgaben
        // z.B. Datenbank-Tabellen erstellen
    }

    /**
     * Nach Deinstallation des Plugins
     */
    public function uninstalled(bool $deleteData = true): void
    {
        parent::uninstalled($deleteData);
        // Aufräumarbeiten
        // $deleteData: true wenn Daten gelöscht werden sollen
    }

    /**
     * Nach Aktivierung des Plugins
     */
    public function enabled(): void
    {
        parent::enabled();
        // Bei jeder Aktivierung ausführen
    }

    /**
     * Nach Deaktivierung des Plugins
     */
    public function disabled(): void
    {
        parent::disabled();
        // Bei jeder Deaktivierung ausführen
    }

    /**
     * Nach Update des Plugins
     */
    public function updated($oldVersion, $newVersion): void
    {
        parent::updated($oldVersion, $newVersion);
        // Migrations-Logik
    }
}
```

## Hooks registrieren

### Über den Dispatcher

```php
public function boot(Dispatcher $dispatcher): void
{
    parent::boot($dispatcher);

    // Variante 1: Callback-Methode
    $dispatcher->listen('shop.hook.' . \HOOK_SMARTY_OUTPUTFILTER, [$this, 'onOutput']);

    // Variante 2: Closure
    $dispatcher->listen('shop.hook.' . \HOOK_ARTIKEL_CLASS_FUELLEARTIKEL, function(array $args) {
        $artikel = $args['oArtikel'];
        // Artikel modifizieren
    });

    // Variante 3: Mit Priorität (höher = früher)
    $dispatcher->listen('shop.hook.' . \HOOK_WARENKORB_CLASS_FUEGEEIN, [$this, 'onCartAdd'], 100);
}

public function onOutput(array $args): void
{
    // $args enthält Hook-spezifische Variablen
    $smarty = $args['smarty'];
    // HTML modifizieren
}
```

### Wichtige Hook-Konstanten

| Konstante | ID | Beschreibung | Verfügbare Variablen |
|-----------|----|--------------|-----------------------|
| `HOOK_SMARTY_OUTPUTFILTER` | 140 | Vor HTML-Ausgabe | `smarty` |
| `HOOK_SMARTY_INC` | 131 | Smarty initialisiert | `smarty` |
| `HOOK_ARTIKEL_CLASS_FUELLEARTIKEL` | 47 | Artikel geladen | `oArtikel` |
| `HOOK_WARENKORB_CLASS_FUEGEEIN` | 93 | Artikel in Warenkorb | `kArtikel`, `oArtikel`, `nAnzahl` |
| `HOOK_WARENKORB_CLASS_LOESCHEPOS` | 95 | Artikel aus Warenkorb | `kWarenkorbPos` |
| `HOOK_BESTELLVORGANG_PAGE` | 181 | Checkout-Seite | `step`, `smarty` |
| `HOOK_BESTELLABSCHLUSS_INC_BESTELLUNGABGESCHLOSSEN` | 142 | Bestellung abgeschlossen | `oBestellung` |
| `HOOK_KATEGORIE_CLASS_LOADFROMDB` | 50 | Kategorie geladen | `oKategorie` |
| `HOOK_LINKCONTAINER_CLASS_BUILDNAVIGATION` | 9 | Navigation gebaut | `oLinkGruppe` |
| `HOOK_SITEMAP_EXPORT_ITEM` | 162 | Sitemap-Eintrag | `item`, `type` |
| `HOOK_PLUGIN_PAGE_SAVE` | 161 | Plugin-Seite gespeichert | `pluginID`, `settings` |

## EventDispatcher (Moderne Alternative)

```php
use JTL\Events\Event;

public function boot(Dispatcher $dispatcher): void
{
    parent::boot($dispatcher);

    // Backend-Benachrichtigung
    $dispatcher->listen('backend.notification', function(array &$args) {
        $args['notifications'][] = [
            'type' => 'info',
            'message' => 'Plugin-Hinweis anzeigen'
        ];
    });

    // Cron-Job registrieren
    $dispatcher->listen(Event::MAP_CRONJOB_TYPE, function(array &$args) {
        $args['jobs']['mein_cron'] = MeinCronJob::class;
    });

    // Payment-Methode registrieren
    $dispatcher->listen(Event::MAP_PAYMENT_METHOD_CLASS, function(array &$args) {
        $args['methods']['meine_zahlung'] = MeineZahlung::class;
    });
}
```

## Plugin-Konfiguration lesen

```php
public function boot(Dispatcher $dispatcher): void
{
    parent::boot($dispatcher);

    // Einzelne Einstellung
    $apiKey = $this->getPlugin()->getConfig()->getValue('api_key');

    // Alle Einstellungen
    $config = $this->getPlugin()->getConfig()->getAll();

    // Mit Standardwert
    $debug = $this->getPlugin()->getConfig()->getValue('debug_mode') ?? false;
}
```

## Plugin-Pfade

```php
// Plugin-Verzeichnis
$pluginPath = $this->getPlugin()->getPaths()->getBasePath();

// Admin-Verzeichnis
$adminPath = $this->getPlugin()->getPaths()->getAdminPath();

// Frontend-Verzeichnis
$frontendPath = $this->getPlugin()->getPaths()->getFrontendPath();

// URL zum Plugin
$pluginUrl = $this->getPlugin()->getPaths()->getBaseURL();
```

## Smarty-Variablen setzen

```php
$dispatcher->listen('shop.hook.' . \HOOK_SMARTY_INC, function(array $args) {
    $smarty = $args['smarty'];

    // Einfache Variable
    $smarty->assign('meineDaten', $this->loadData());

    // Array
    $smarty->assign('meineProdukte', [
        ['name' => 'Produkt 1', 'preis' => 19.99],
        ['name' => 'Produkt 2', 'preis' => 29.99],
    ]);

    // Objekt
    $smarty->assign('meinObjekt', new \stdClass());
});
```

## HTML modifizieren

```php
$dispatcher->listen('shop.hook.' . \HOOK_SMARTY_OUTPUTFILTER, function(array $args) {
    $smarty = $args['smarty'];

    // HTML vor </body> einfügen
    $customHtml = '<div id="mein-widget">Widget Content</div>';
    $smarty->_tpl_vars['cPluginJsBody'] .= $customHtml;

    // Oder direkter Output-Filter
    if (isset($args['output'])) {
        $args['output'] = str_replace(
            '</body>',
            $customHtml . '</body>',
            $args['output']
        );
    }
});
```

## Dependency Injection

```php
use JTL\Shop;
use Psr\Log\LoggerInterface;

public function boot(Dispatcher $dispatcher): void
{
    parent::boot($dispatcher);

    // Container-Zugriff
    $container = Shop::Container();

    // Logger
    $logger = $container->getLogService();
    $logger->notice('Plugin gestartet');

    // Datenbank
    $db = $container->getDB();
    $results = $db->getObjects('SELECT * FROM tartikel LIMIT 10');

    // Cache
    $cache = $container->getCache();
    $cached = $cache->get('mein_cache_key');

    // Session
    $session = $container->getFrontend()->getCustomer();
}
```

## Logging

```php
use JTL\Shop;

// Verschiedene Log-Level
Shop::Container()->getLogService()->debug('Debug-Info');
Shop::Container()->getLogService()->info('Info-Nachricht');
Shop::Container()->getLogService()->notice('Hinweis');
Shop::Container()->getLogService()->warning('Warnung');
Shop::Container()->getLogService()->error('Fehler');
Shop::Container()->getLogService()->critical('Kritischer Fehler');
```

## AJAX-Endpunkt registrieren

```php
$dispatcher->listen('shop.hook.' . \HOOK_IO_HANDLE_REQUEST, function(array $args) {
    $io = $args['io'];
    $request = $args['request'];

    if (isset($request['meinPlugin_action'])) {
        $response = $this->handleAjax($request);
        echo json_encode($response);
        exit;
    }
});
```

## Vollständiges Beispiel

```php
<?php
declare(strict_types=1);

namespace Plugin\MeineFirma_MeinPlugin;

use JTL\Events\Dispatcher;
use JTL\Plugin\Bootstrapper;
use JTL\Shop;

class Bootstrap extends Bootstrapper
{
    private bool $debugMode = false;

    public function boot(Dispatcher $dispatcher): void
    {
        parent::boot($dispatcher);

        $this->debugMode = (bool)$this->getPlugin()->getConfig()->getValue('debug_mode');

        // Hooks registrieren
        $dispatcher->listen('shop.hook.' . \HOOK_SMARTY_INC, [$this, 'onSmartyInit']);
        $dispatcher->listen('shop.hook.' . \HOOK_ARTIKEL_CLASS_FUELLEARTIKEL, [$this, 'onArticleLoad']);
        $dispatcher->listen('shop.hook.' . \HOOK_BESTELLABSCHLUSS_INC_BESTELLUNGABGESCHLOSSEN, [$this, 'onOrderComplete']);
    }

    public function onSmartyInit(array $args): void
    {
        $args['smarty']->assign('meinPlugin_enabled', true);
        $args['smarty']->assign('meinPlugin_data', $this->loadData());
    }

    public function onArticleLoad(array $args): void
    {
        $artikel = $args['oArtikel'];
        // Artikel erweitern
        $artikel->customField = 'Mein Wert';

        if ($this->debugMode) {
            Shop::Container()->getLogService()->debug(
                'Artikel geladen: ' . $artikel->kArtikel
            );
        }
    }

    public function onOrderComplete(array $args): void
    {
        $bestellung = $args['oBestellung'];

        // Bestellung an externes System senden
        $this->sendToExternalApi($bestellung);
    }

    public function installed(): void
    {
        parent::installed();

        // Datenbank-Tabelle erstellen
        $db = Shop::Container()->getDB();
        $db->query(
            'CREATE TABLE IF NOT EXISTS plugin_meinplugin_log (
                id INT AUTO_INCREMENT PRIMARY KEY,
                message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )'
        );
    }

    public function uninstalled(bool $deleteData = true): void
    {
        parent::uninstalled($deleteData);

        if ($deleteData) {
            $db = Shop::Container()->getDB();
            $db->query('DROP TABLE IF EXISTS plugin_meinplugin_log');
        }
    }

    private function loadData(): array
    {
        // Daten laden
        return [];
    }

    private function sendToExternalApi($bestellung): void
    {
        // API-Aufruf
    }
}
```
