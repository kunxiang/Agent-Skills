# Troubleshooting

Häufige Probleme bei der JTL-Shop 5 Plugin-Entwicklung und deren Lösungen.

## Installation & Aktivierung

### Plugin nicht in der Pluginverwaltung sichtbar

**Ursache**: Ordnername stimmt nicht mit PluginID überein.

**Lösung**:
```
# Falsch
plugins/mein-plugin/        # Bindestrich nicht erlaubt
plugins/MeinPlugin/         # Stimmt nicht mit PluginID überein

# Richtig
plugins/MeineFirma_MeinPlugin/  # Genau wie <PluginID> in info.xml
```

**Prüfen**:
```bash
# info.xml öffnen und PluginID prüfen
grep "<PluginID>" plugins/*/info.xml
```

### "Fehler beim Installieren" ohne Details

**Ursachen**:
1. XML-Syntaxfehler in info.xml
2. Fehlende Pflichtfelder
3. Ungültiges Datumsformat

**Lösung**:
```bash
# XML validieren
xmllint --noout plugins/MeineFirma_MeinPlugin/info.xml

# Pflichtfelder prüfen
# - Name, Description, Author, URL
# - PluginID, XMLVersion, MinShopVersion
# - CreateDate (Format: YYYY-MM-DD), Version
```

### Plugin installiert, aber Bootstrap wird nicht geladen

**Ursache**: Namespace-Fehler in Bootstrap.php

**Lösung**:
```php
// Falsch
namespace MeinPlugin;                          // Namespace fehlt Plugin\
namespace Plugin\MeinPlugin;                   // Muss PluginID entsprechen
namespace Template\MeineFirma_MeinPlugin;      // Template\ statt Plugin\

// Richtig
namespace Plugin\MeineFirma_MeinPlugin;        // Genau: Plugin\<PluginID>
```

## Hooks & Events

### Hook wird nicht aufgerufen

**Mögliche Ursachen**:

1. **Falsches Event-Format**:
```php
// Falsch
$dispatcher->listen(HOOK_SMARTY_OUTPUTFILTER, ...);
$dispatcher->listen(140, ...);

// Richtig
$dispatcher->listen('shop.hook.' . \HOOK_SMARTY_OUTPUTFILTER, ...);
$dispatcher->listen('shop.hook.140', ...);
```

2. **Hook-ID existiert nicht in dieser Shop-Version**:
```php
// Hook-Liste prüfen: https://jtl-shop-mkdocs.readthedocs.io/de/latest/shop_plugins/hook_list.html
```

3. **Callback-Methode fehlt oder ist private**:
```php
// Falsch
private function onOutput(array $args): void { }

// Richtig - Methode muss public sein
public function onOutput(array $args): void { }
```

4. **Plugin nicht aktiv**:
```
Backend → Plugins → Pluginverwaltung → Plugin aktivieren
```

### Hook-Variablen nicht verfügbar

**Lösung**: Alle Hooks haben unterschiedliche Variablen in `$args`

```php
public function onHook(array $args): void
{
    // Verfügbare Variablen debuggen
    error_log(print_r(array_keys($args), true));

    // Dann gezielt verwenden
    if (isset($args['smarty'])) {
        $smarty = $args['smarty'];
    }
}
```

## Admin-Bereich

### Admin-Tab erscheint nicht

**Checkliste**:

1. **info.xml korrekt**:
```xml
<Install>
    <PluginAdminMenu>
        <Customlink sort="1">
            <Name>Einstellungen</Name>
            <Filename>config.php</Filename>  <!-- Ohne Pfad -->
        </Customlink>
    </PluginAdminMenu>
</Install>
```

2. **PHP-Datei vorhanden**:
```
plugins/MeineFirma_MeinPlugin/adminmenu/config.php  ← Muss existieren
```

3. **Nach info.xml-Änderung**: Plugin neu installieren oder Dev-Modus

### Variables $plugin, $smarty nicht verfügbar in Admin

**Lösung**: Diese Variablen werden automatisch injiziert

```php
<?php
// adminmenu/config.php

// Diese sind automatisch verfügbar:
/** @var \JTL\Plugin\PluginInterface $plugin */
/** @var \JTL\Smarty\JTLSmarty $smarty */
/** @var \JTL\DB\DbInterface $db */

// Nicht manuell laden
// $plugin = ... ← Falsch
```

### Einstellungen werden nicht gespeichert

**Ursache**: Falscher Einstellungsname oder fehlender CSRF-Token

**Lösung**:
```smarty
{* Template: CSRF-Token einbinden *}
<form method="post">
    {$jtl_token}  {* Wichtig! *}
    ...
</form>
```

```php
// PHP: Richtiger Config-Name
$value = $plugin->getConfig()->getValue('api_key');  // Muss mit name= in info.xml übereinstimmen
```

## Frontend

### Frontend-Template wird nicht geladen

**Checkliste**:

1. Template-Pfad korrekt: `frontend/template/`
2. FrontendLink in info.xml definiert
3. Template-Name in info.xml = Dateiname

```xml
<FrontendLink>
    <TemplateFile>meine_seite.tpl</TemplateFile>
    <!-- Template liegt in: frontend/template/meine_seite.tpl -->
</FrontendLink>
```

### CSS/JS wird nicht geladen

**Lösung 1**: In Bootstrap.php einbinden

```php
$dispatcher->listen('shop.hook.' . \HOOK_SMARTY_OUTPUTFILTER, function($args) {
    $pluginUrl = $this->getPlugin()->getPaths()->getBaseURL();

    $args['smarty']->_tpl_vars['cPluginCss'] .=
        '<link rel="stylesheet" href="' . $pluginUrl . '/css/styles.css">';

    $args['smarty']->_tpl_vars['cPluginJsBody'] .=
        '<script src="' . $pluginUrl . '/js/main.js" defer></script>';
});
```

**Lösung 2**: Im Template direkt

```smarty
{extends file="layout/index.tpl"}

{block name="head-custom-css" append}
    <link rel="stylesheet" href="{$oPlugin->cFrontendPfadURLSSL}/css/styles.css">
{/block}
```

## Datenbank

### Migration wird nicht ausgeführt

**Checkliste**:

1. **Dateiname-Format**: `Migration[YYYYMMDDHHMMSS].php`
2. **Namespace korrekt**: `Plugin\<PluginID>\Migrations`
3. **Klasse implementiert Interface**: `implements IMigration`
4. **Klassenname = Dateiname**

```php
// Datei: Migrations/Migration20240115120000.php
namespace Plugin\MeineFirma_MeinPlugin\Migrations;

class Migration20240115120000 extends Migration implements IMigration
{
    // ...
}
```

### SQL-Fehler in Migration

**Debugging**:

```php
public function up(): void
{
    try {
        $this->execute("CREATE TABLE ...");
    } catch (\Exception $e) {
        // Log schreiben
        \JTL\Shop::Container()->getLogService()->error(
            'Migration Error: ' . $e->getMessage()
        );
        throw $e;
    }
}
```

## Caching-Probleme

### Änderungen werden nicht sichtbar

**Lösung**:

1. **Template-Cache leeren**:
   ```
   Backend → System → Cache → Template-Cache → Leeren
   ```

2. **Object-Cache leeren**:
   ```
   Backend → System → Cache → Object-Cache → Leeren
   ```

3. **Browser-Cache**:
   - Strg+F5 (Hard Refresh)
   - Inkognito-Modus testen

4. **Opcache** (bei PHP):
   ```php
   opcache_reset();
   // Oder: PHP-FPM neustarten
   ```

## Dev-Modus

### info.xml-Änderungen erfordern Neuinstallation

**Lösung**: Dev-Modus aktivieren

```php
// In includes/config.JTL-Shop.ini.php hinzufügen:
define('PLUGIN_DEV_MODE', true);
```

**Achtung**: Nur in Entwicklungsumgebung verwenden!

## Logging & Debugging

### Debug-Informationen ausgeben

```php
// In Logdatei schreiben
\JTL\Shop::Container()->getLogService()->debug('Mein Debug: ' . $variable);
\JTL\Shop::Container()->getLogService()->info('Info: ' . json_encode($array));

// Temporär in Frontend (nur Entwicklung!)
echo '<pre>' . print_r($variable, true) . '</pre>';

// In Browser-Konsole
echo '<script>console.log(' . json_encode($data) . ');</script>';
```

### Logs finden

```
Backend → System → Log → Plugin-Logs
```

Oder Datei:
```
<shop>/includes/logs/shop*.log
```

## Häufige Fehlermeldungen

| Fehlermeldung | Ursache | Lösung |
|---------------|---------|--------|
| "Class not found" | Namespace falsch | `Plugin\<PluginID>` prüfen |
| "Cannot use object of type..." | Falscher Variablentyp | Typen prüfen, Casting |
| "Fatal error: Uncaught Error" | PHP-Syntaxfehler | `php -l datei.php` |
| "XML Parse Error" | Ungültige info.xml | `xmllint --noout info.xml` |
| "SQLSTATE[42S02]" | Tabelle existiert nicht | Migration ausführen |
| "Access denied" | Berechtigungen | Dateiberechtigungen prüfen |

## Nützliche Befehle

```bash
# XML validieren
xmllint --noout plugins/*/info.xml

# PHP Syntax prüfen
php -l plugins/MeineFirma_MeinPlugin/Bootstrap.php

# Alle PHP-Dateien prüfen
find plugins/MeineFirma_MeinPlugin -name "*.php" -exec php -l {} \;

# Logs live verfolgen
tail -f includes/logs/shop*.log

# Cache-Verzeichnisse leeren
rm -rf templates_c/*
```

## Support-Ressourcen

- **JTL-Forum**: https://forum.jtl-software.de/
- **Entwickler-Dokumentation**: https://jtl-devguide.readthedocs.io/
- **GitLab Issues**: https://gitlab.com/jtl-software/jtl-shop/core/-/issues
- **Test-Plugin Referenz**: https://gitlab.com/jtl-software/jtl-shop/plugins/jtl_test
