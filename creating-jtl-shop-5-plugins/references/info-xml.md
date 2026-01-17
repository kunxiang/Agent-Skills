# info.xml Vollständige Referenz

Die info.xml ist das Herzstück jedes JTL-Shop 5 Plugins. Sie beschreibt das Plugin und seine Funktionalitäten.

## Grundstruktur

```xml
<?xml version="1.0" encoding="UTF-8"?>
<jtlshopplugin>
    <!-- Globale Informationen -->
    <Name>Plugin-Name</Name>
    <Description>Ausführliche Beschreibung</Description>
    <Author>Firmenname</Author>
    <URL>https://ihre-website.de</URL>
    <PluginID>Firma_PluginName</PluginID>
    <XMLVersion>100</XMLVersion>
    <MinShopVersion>5.0.0</MinShopVersion>
    <CreateDate>2024-01-15</CreateDate>
    <Version>1.0.0</Version>

    <!-- Optional für JTL-Store -->
    <ExsID>xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx</ExsID>

    <!-- Installationsblock -->
    <Install>
        <!-- Inhalte siehe unten -->
    </Install>
</jtlshopplugin>
```

**Hinweis**: Ab JTL-Shop 5.x heißt das Root-Element `<jtlshopplugin>` (nicht mehr `<jtlshop3plugin>`).

## Pflichtfelder

| Element | Beschreibung | Beispiel |
|---------|--------------|----------|
| `<Name>` | Anzeigename im Backend | `Mein Plugin` |
| `<Description>` | Beschreibung | `Fügt Funktionalität X hinzu` |
| `<Author>` | Entwickler/Firma | `Meine Firma GmbH` |
| `<URL>` | Support/Info-URL | `https://meine-firma.de` |
| `<PluginID>` | Eindeutige ID (= Ordnername) | `MeineFirma_PluginName` |
| `<XMLVersion>` | Plugin-XML Schema Version | `100` (für Shop 5.0+) |
| `<MinShopVersion>` | Mindest-Shopversion | `5.0.0` |
| `<CreateDate>` | Erstellungsdatum (YYYY-MM-DD) | `2024-01-15` |
| `<Version>` | Plugin-Version | `1.0.0` |

## PluginID Regeln

- Nur erlaubt: `a-z`, `A-Z`, `0-9`, `_` (Unterstrich)
- **Nicht erlaubt**: `.` (Punkt), `-` (Bindestrich), Leerzeichen
- Empfohlenes Format: `Firma_PluginName`
- Entspricht ab Shop 5.0 dem PSR-4 Namespace: `Plugin\<PluginID>`

## XMLVersion Werte

| Version | Shop-Version | Beschreibung |
|---------|--------------|--------------|
| 100 | 5.0.0+ | Basis für JTL-Shop 5 |
| 101 | 5.0.0+ | Erweiterte Features |
| 102 | 5.0.0+ | Lizenzklasse Support |

## Install-Block

### Cache-Tags leeren

```xml
<Install>
    <FlushTags>CACHING_GROUP_CORE, CACHING_GROUP_ARTICLE, CACHING_GROUP_CATEGORY</FlushTags>
</Install>
```

Verfügbare Tags:
- `CACHING_GROUP_CORE`
- `CACHING_GROUP_ARTICLE`
- `CACHING_GROUP_CATEGORY`
- `CACHING_GROUP_LANGUAGE`
- `CACHING_GROUP_TEMPLATE`
- `CACHING_GROUP_OPTION`

### Plugin-Einstellungen

```xml
<Install>
    <PluginSettings>
        <Setting type="text" sort="1" name="config_key">
            <Name>Einstellungsname</Name>
            <Description>Hilfetext zur Einstellung</Description>
            <DefaultValue>Standardwert</DefaultValue>
        </Setting>

        <Setting type="checkbox" sort="2" name="is_enabled">
            <Name>Aktiviert</Name>
            <DefaultValue>1</DefaultValue>
        </Setting>

        <Setting type="selectbox" sort="3" name="mode">
            <Name>Modus</Name>
            <DefaultValue>standard</DefaultValue>
            <SelectboxOptions>
                <Option value="standard" sort="1">Standard</Option>
                <Option value="extended" sort="2">Erweitert</Option>
                <Option value="debug" sort="3">Debug</Option>
            </SelectboxOptions>
        </Setting>

        <Setting type="radio" sort="4" name="position">
            <Name>Position</Name>
            <DefaultValue>left</DefaultValue>
            <RadioOptions>
                <Option value="left" sort="1">Links</Option>
                <Option value="right" sort="2">Rechts</Option>
            </RadioOptions>
        </Setting>

        <Setting type="textarea" sort="5" name="custom_css">
            <Name>Eigenes CSS</Name>
            <DefaultValue></DefaultValue>
        </Setting>

        <Setting type="password" sort="6" name="api_secret">
            <Name>API Secret</Name>
            <DefaultValue></DefaultValue>
        </Setting>

        <Setting type="color" sort="7" name="accent_color">
            <Name>Akzentfarbe</Name>
            <DefaultValue>#007bff</DefaultValue>
        </Setting>
    </PluginSettings>
</Install>
```

### Setting-Typen

| Typ | Beschreibung |
|-----|--------------|
| `text` | Einzeiliges Textfeld |
| `textarea` | Mehrzeiliges Textfeld |
| `checkbox` | Checkbox (0/1) |
| `selectbox` | Dropdown mit Optionen |
| `radio` | Radio-Buttons |
| `password` | Passwortfeld (maskiert) |
| `color` | Farbwähler |

### Admin-Menü

```xml
<Install>
    <PluginAdminMenu>
        <Customlink sort="1">
            <Name>Einstellungen</Name>
            <Filename>settings.php</Filename>
        </Customlink>
        <Customlink sort="2">
            <Name>Statistiken</Name>
            <Filename>stats.php</Filename>
        </Customlink>
        <Customlink sort="3">
            <Name>Import/Export</Name>
            <Filename>import.php</Filename>
        </Customlink>
    </PluginAdminMenu>
</Install>
```

Die PHP-Dateien müssen in `adminmenu/` liegen.

### Frontend-Links

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

### Hooks

```xml
<Install>
    <Hooks>
        <Hook id="140" priority="5">hook_output.php</Hook>
        <Hook id="131">hook_smarty.php</Hook>
        <Hook id="47" priority="10">hook_artikel.php</Hook>
    </Hooks>
</Install>
```

**Hinweis**: In JTL-Shop 5 werden Hooks bevorzugt in Bootstrap.php registriert.

### Payment-Methoden

```xml
<Install>
    <PaymentMethods>
        <PaymentMethod>
            <Name>Meine Zahlart</Name>
            <ClassName>MeinZahlungsProvider</ClassName>
            <ClassFile>MeinZahlungsProvider.php</ClassFile>
            <TemplateFile>payment.tpl</TemplateFile>
            <Sort>1</Sort>
        </PaymentMethod>
    </PaymentMethods>
</Install>
```

### Portlets (für OPC)

```xml
<Install>
    <Portlets>
        <Portlet>
            <Name>Mein Portlet</Name>
            <Class>MeinPortlet</Class>
        </Portlet>
    </Portlets>
</Install>
```

### Widgets (Dashboard)

```xml
<Install>
    <AdminWidgets>
        <Widget sort="1">
            <Name>Mein Widget</Name>
            <Description>Dashboard-Widget für XYZ</Description>
            <Container>center</Container>
            <Class>MeinWidget</Class>
        </Widget>
    </AdminWidgets>
</Install>
```

### Cron-Jobs

```xml
<Install>
    <Crons>
        <Cron>
            <Name>Tägliche Synchronisation</Name>
            <Description>Synchronisiert Daten täglich</Description>
            <Filename>sync_cron.php</Filename>
            <Interval>24</Interval>
            <IntervalType>H</IntervalType>
        </Cron>
    </Crons>
</Install>
```

Intervall-Typen: `M` (Minuten), `H` (Stunden), `D` (Tage)

### Mail-Templates

```xml
<Install>
    <Mails>
        <Mail>
            <Name>Mein Mail Template</Name>
            <Type>text/html</Type>
            <Module>mein_mail_modul</Module>
            <Active>1</Active>
            <Subject>Betreff: {$Variable}</Subject>
            <BodyHtml>mail_body.tpl</BodyHtml>
        </Mail>
    </Mails>
</Install>
```

### Consent Manager

```xml
<Install>
    <ConsentManager>
        <Vendor>
            <ID>mein_tracking</ID>
            <Name>Mein Tracking Service</Name>
            <Description>Beschreibung des Tracking-Dienstes</Description>
            <Purpose>Analyse</Purpose>
            <Company>Tracking GmbH</Company>
            <PrivacyPolicy>https://tracking.example.com/privacy</PrivacyPolicy>
        </Vendor>
    </ConsentManager>
</Install>
```

## Lizenzierung (Optional)

```xml
<jtlshopplugin>
    ...
    <LicenceClass>MeineLizenzPruefung</LicenceClass>
    <LicenceClassFile>MeineLizenzPruefung.php</LicenceClassFile>
    ...
</jtlshopplugin>
```

## Vollständiges Beispiel

```xml
<?xml version="1.0" encoding="UTF-8"?>
<jtlshopplugin>
    <Name>Beispiel Plugin</Name>
    <Description>Ein vollständiges Beispiel-Plugin für JTL-Shop 5</Description>
    <Author>Beispiel GmbH</Author>
    <URL>https://beispiel.de</URL>
    <PluginID>Beispiel_DemoPlugin</PluginID>
    <XMLVersion>102</XMLVersion>
    <MinShopVersion>5.0.0</MinShopVersion>
    <CreateDate>2024-01-15</CreateDate>
    <Version>1.0.0</Version>

    <Install>
        <FlushTags>CACHING_GROUP_CORE</FlushTags>

        <PluginSettings>
            <Setting type="text" sort="1" name="api_key">
                <Name>API-Schlüssel</Name>
                <Description>Ihr API-Schlüssel</Description>
                <DefaultValue></DefaultValue>
            </Setting>
            <Setting type="checkbox" sort="2" name="debug_mode">
                <Name>Debug-Modus</Name>
                <DefaultValue>0</DefaultValue>
            </Setting>
        </PluginSettings>

        <PluginAdminMenu>
            <Customlink sort="1">
                <Name>Konfiguration</Name>
                <Filename>config.php</Filename>
            </Customlink>
        </PluginAdminMenu>

        <Crons>
            <Cron>
                <Name>Sync Job</Name>
                <Description>Stündliche Synchronisation</Description>
                <Filename>sync.php</Filename>
                <Interval>1</Interval>
                <IntervalType>H</IntervalType>
            </Cron>
        </Crons>
    </Install>
</jtlshopplugin>
```

## Validierung

- XML muss wohlgeformt sein (UTF-8 Encoding)
- PluginID muss mit Ordnername übereinstimmen
- Alle referenzierten Dateien müssen existieren
- CreateDate im Format YYYY-MM-DD
