<?php
/**
 * JTL-Shop 5 Plugin Bootstrap Template
 * =====================================
 *
 * Anleitung:
 * 1. Ersetze {{COMPANY}}_{{PLUGIN_ID}} mit deiner PluginID
 * 2. Passe die Hooks nach Bedarf an
 * 3. Lösche nicht benötigte Methoden
 *
 * Namespace-Format: Plugin\<PluginID>
 */

declare(strict_types=1);

namespace Plugin\{{COMPANY}}_{{PLUGIN_ID}};

use JTL\Events\Dispatcher;
use JTL\Plugin\Bootstrapper;
use JTL\Shop;

class Bootstrap extends Bootstrapper
{
    /**
     * Wird bei jedem Request aufgerufen (wenn Plugin aktiv)
     *
     * @param Dispatcher $dispatcher Event-Dispatcher für Hook-Registrierung
     */
    public function boot(Dispatcher $dispatcher): void
    {
        parent::boot($dispatcher);

        // =====================================================
        // HOOKS REGISTRIEREN
        // =====================================================

        // Hook: Vor HTML-Ausgabe (universell einsetzbar)
        $dispatcher->listen(
            'shop.hook.' . \HOOK_SMARTY_OUTPUTFILTER,
            [$this, 'onOutputFilter']
        );

        // Hook: Smarty initialisiert (Variablen setzen)
        $dispatcher->listen(
            'shop.hook.' . \HOOK_SMARTY_INC,
            [$this, 'onSmartyInit']
        );

        // Hook: Artikel geladen
        // $dispatcher->listen(
        //     'shop.hook.' . \HOOK_ARTIKEL_CLASS_FUELLEARTIKEL,
        //     [$this, 'onArticleLoad']
        // );

        // Hook: Artikel in Warenkorb
        // $dispatcher->listen(
        //     'shop.hook.' . \HOOK_WARENKORB_CLASS_FUEGEEIN,
        //     [$this, 'onCartAdd']
        // );

        // Hook: Bestellung abgeschlossen
        // $dispatcher->listen(
        //     'shop.hook.' . \HOOK_BESTELLABSCHLUSS_INC_BESTELLUNGABGESCHLOSSEN,
        //     [$this, 'onOrderComplete']
        // );

        // =====================================================
        // EVENTS (Alternative zu Hooks, ab Shop 5.x)
        // =====================================================

        // Backend-Benachrichtigung anzeigen
        // $dispatcher->listen('backend.notification', function(array &$args) {
        //     $args['notifications'][] = [
        //         'type' => 'info',  // info, warning, error, success
        //         'message' => 'Plugin-Hinweis für Admins'
        //     ];
        // });
    }

    // =========================================================
    // HOOK-CALLBACK-METHODEN
    // =========================================================

    /**
     * Hook: HOOK_SMARTY_OUTPUTFILTER (140)
     * Wird vor der HTML-Ausgabe aufgerufen
     *
     * @param array $args ['smarty' => JTLSmarty]
     */
    public function onOutputFilter(array $args): void
    {
        $smarty = $args['smarty'];
        $config = $this->getPlugin()->getConfig();

        // Beispiel: Prüfen ob Plugin aktiv
        if (!$config->getValue('is_active')) {
            return;
        }

        // Beispiel: CSS einbinden
        $pluginUrl = $this->getPlugin()->getPaths()->getBaseURL();
        $smarty->_tpl_vars['cPluginCss'] .=
            '<link rel="stylesheet" href="' . $pluginUrl . '/css/styles.css">';

        // Beispiel: JavaScript einbinden
        $smarty->_tpl_vars['cPluginJsBody'] .=
            '<script src="' . $pluginUrl . '/js/main.js" defer></script>';

        // Beispiel: Widget HTML einfügen
        // $widgetHtml = '<div id="mein-widget" data-config=\'' . json_encode([
        //     'apiKey' => $config->getValue('api_key'),
        //     'mode' => $config->getValue('display_mode'),
        // ]) . '\'></div>';
        // $smarty->_tpl_vars['cPluginJsBody'] .= $widgetHtml;
    }

    /**
     * Hook: HOOK_SMARTY_INC (131)
     * Wird bei Smarty-Initialisierung aufgerufen
     *
     * @param array $args ['smarty' => JTLSmarty]
     */
    public function onSmartyInit(array $args): void
    {
        $smarty = $args['smarty'];
        $config = $this->getPlugin()->getConfig();

        // Variablen für Templates verfügbar machen
        $smarty->assign('meinPlugin', [
            'enabled' => (bool)$config->getValue('is_active'),
            'mode' => $config->getValue('display_mode'),
            'color' => $config->getValue('accent_color'),
        ]);

        // Plugin-Objekt für Templates
        // $smarty->assign('oMeinPlugin', $this->getPlugin());
    }

    /**
     * Hook: HOOK_ARTIKEL_CLASS_FUELLEARTIKEL (47)
     * Wird beim Laden eines Artikels aufgerufen
     *
     * @param array $args ['oArtikel' => Artikel]
     */
    public function onArticleLoad(array $args): void
    {
        $artikel = $args['oArtikel'];

        // Beispiel: Zusätzliche Daten zum Artikel hinzufügen
        // $artikel->customData = $this->loadCustomData($artikel->kArtikel);

        $this->log('Artikel geladen: ' . $artikel->kArtikel);
    }

    /**
     * Hook: HOOK_WARENKORB_CLASS_FUEGEEIN (93)
     * Wird beim Hinzufügen zum Warenkorb aufgerufen
     *
     * @param array $args ['kArtikel', 'oArtikel', 'nAnzahl']
     */
    public function onCartAdd(array $args): void
    {
        $artikelId = $args['kArtikel'];
        $anzahl = $args['nAnzahl'];

        $this->log("Artikel $artikelId mit Anzahl $anzahl in Warenkorb");

        // Beispiel: Tracking-Event senden
        // $this->trackEvent('add_to_cart', [
        //     'product_id' => $artikelId,
        //     'quantity' => $anzahl
        // ]);
    }

    /**
     * Hook: HOOK_BESTELLABSCHLUSS_INC_BESTELLUNGABGESCHLOSSEN (142)
     * Wird nach Bestellabschluss aufgerufen
     *
     * @param array $args ['oBestellung' => Bestellung]
     */
    public function onOrderComplete(array $args): void
    {
        $bestellung = $args['oBestellung'];

        $this->log('Bestellung abgeschlossen: ' . $bestellung->cBestellNr);

        // Beispiel: An externes System senden
        // $this->sendToExternalApi($bestellung);
    }

    // =========================================================
    // LIFECYCLE-METHODEN
    // =========================================================

    /**
     * Wird nach Plugin-Installation aufgerufen
     */
    public function installed(): void
    {
        parent::installed();

        $this->log('Plugin installiert');

        // Beispiel: Datenbank-Tabelle erstellen (alternativ: Migrations verwenden)
        // $db = Shop::Container()->getDB();
        // $db->query("
        //     CREATE TABLE IF NOT EXISTS plugin_meinplugin_data (
        //         id INT AUTO_INCREMENT PRIMARY KEY,
        //         data TEXT,
        //         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        //     ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        // ");
    }

    /**
     * Wird nach Plugin-Deinstallation aufgerufen
     *
     * @param bool $deleteData true wenn Daten gelöscht werden sollen
     */
    public function uninstalled(bool $deleteData = true): void
    {
        parent::uninstalled($deleteData);

        $this->log('Plugin deinstalliert, Daten löschen: ' . ($deleteData ? 'ja' : 'nein'));

        if ($deleteData) {
            // Datenbank-Tabellen löschen
            // $db = Shop::Container()->getDB();
            // $db->query("DROP TABLE IF EXISTS plugin_meinplugin_data");
        }
    }

    /**
     * Wird nach Plugin-Aktivierung aufgerufen
     */
    public function enabled(): void
    {
        parent::enabled();
        $this->log('Plugin aktiviert');
    }

    /**
     * Wird nach Plugin-Deaktivierung aufgerufen
     */
    public function disabled(): void
    {
        parent::disabled();
        $this->log('Plugin deaktiviert');
    }

    /**
     * Wird nach Plugin-Update aufgerufen
     *
     * @param string $oldVersion Alte Version
     * @param string $newVersion Neue Version
     */
    public function updated($oldVersion, $newVersion): void
    {
        parent::updated($oldVersion, $newVersion);
        $this->log("Plugin aktualisiert: $oldVersion → $newVersion");

        // Beispiel: Migrations für bestimmte Versionen
        // if (version_compare($oldVersion, '1.1.0', '<')) {
        //     $this->migrateToVersion110();
        // }
    }

    // =========================================================
    // HILFSMETHODEN
    // =========================================================

    /**
     * Schreibt eine Log-Nachricht
     *
     * @param string $message Log-Nachricht
     * @param string $level Log-Level (debug, info, notice, warning, error)
     */
    private function log(string $message, string $level = 'debug'): void
    {
        $pluginName = $this->getPlugin()->getMeta()->getName();
        Shop::Container()->getLogService()->{$level}(
            "[$pluginName] $message"
        );
    }

    /**
     * Gibt den Plugin-Konfigurationswert zurück
     *
     * @param string $key Konfigurationsschlüssel
     * @param mixed $default Standardwert
     * @return mixed
     */
    private function getConfigValue(string $key, $default = null)
    {
        $value = $this->getPlugin()->getConfig()->getValue($key);
        return $value ?? $default;
    }

    /**
     * Führt eine Datenbankabfrage aus
     *
     * @param string $sql SQL-Query
     * @return array
     */
    private function query(string $sql): array
    {
        return Shop::Container()->getDB()->getObjects($sql);
    }

    /**
     * Holt einen Wert aus dem Cache oder führt den Callback aus
     *
     * @param string $key Cache-Schlüssel
     * @param callable $callback Callback zum Generieren des Wertes
     * @param int $ttl Time-to-live in Sekunden
     * @return mixed
     */
    private function cached(string $key, callable $callback, int $ttl = 3600)
    {
        $cache = Shop::Container()->getCache();
        $cacheKey = 'plugin_meinplugin_' . $key;

        $value = $cache->get($cacheKey);

        if ($value === false) {
            $value = $callback();
            $cache->set($cacheKey, $value, [\CACHING_GROUP_PLUGIN], $ttl);
        }

        return $value;
    }
}
