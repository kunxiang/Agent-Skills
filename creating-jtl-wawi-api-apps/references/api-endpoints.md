# JTL-Wawi API Endpoints

## ⚠️ KRITISCH: URL-Format (häufigster Fehler!)

### Vollständige URL-Struktur für OnPrem

```
http://<HOST>:<PORT>/api/<MANDANT>/v1/<ENDPOINT>
```

**Beispiel**:
```
http://192.168.1.24:5883/api/eazybusiness/v1/customers
                   │        │           │   │
                   │        │           │   └── Endpoint
                   │        │           └────── API-Version (v1)
                   │        └────────────────── Mandantenname (Datenbank)
                   └─────────────────────────── Port (Standard: 5883)
```

### ❌ FALSCHE URL-Formate (häufige Fehler)

```bash
# FALSCH: Fehlendes /api/
http://localhost:5883/eazybusiness/v1/customers ❌

# FALSCH: Fehlendes /v1/
http://localhost:5883/api/eazybusiness/customers ❌

# FALSCH: Falscher Mandantenname
http://localhost:5883/api/eazyBusiness/v1/customers ❌  # Groß-/Kleinschreibung!

# FALSCH: Altes /rest/ Format (veraltet)
http://localhost:5883/rest/eazybusiness/v1/Customer ❌

# FALSCH: Fehlender Mandant
http://localhost:5883/api/v1/customers ❌
```

### ✓ RICHTIGE URL-Formate

```bash
# Korrekt: Standard OnPrem
http://localhost:5883/api/eazybusiness/v1/customers ✓

# Korrekt: Mit IP-Adresse
http://192.168.1.24:5883/api/eazybusiness/v1/customers ✓

# Korrekt: Anderer Mandantenname
http://localhost:5883/api/MeinMandant/v1/customers ✓
```

### Mandantenname herausfinden

Der Mandantenname entspricht dem **Datenbanknamen** in SQL Server:

```bash
# Beim Starten des REST-Servers wird der Mandant angezeigt:
JTL.Wawi.Rest.exe -w "Standard" -d MeinMandant --port 5883

# Ausgabe zeigt:
# Starting REST API for tenant 'MeinMandant' on 'http://0.0.0.0:5883/api/MeinMandant'...
```

**Standard-Mandantenname**: `eazybusiness` (bei Standardinstallation)

## Base URLs

| Umgebung | URL | Bemerkung |
|----------|-----|-----------|
| OnPrem (lokal) | `http://localhost:5883/api/eazybusiness` | Standard-Port, Standard-Mandant |
| OnPrem (Netzwerk) | `http://<IP>:5883/api/<MANDANT>` | Firewall beachten |
| Cloud | `https://api.jtl-software.com/erp/v1.1` | OAuth erforderlich |

## App-Registrierung Endpoints

### POST /authentication

**Zweck**: Neue App registrieren

**Request**:
```http
POST /authentication HTTP/1.1
Host: localhost:5883
Content-Type: application/json
api-version: 1.0
X-ChallengeCode: mein-geheimer-code

{
  "AppId": "meine-firma/mein-app/v1",
  "DisplayName": "Meine App",
  "Description": "Beschreibung der App-Funktionen",
  "Version": "1.0.0",
  "ProviderName": "Meine Firma GmbH",
  "ProviderWebsite": "https://www.meine-firma.de",
  "MandatoryApiScopes": ["all.read", "customer.createcustomer"],
  "OptionalApiScopes": [],
  "RegistrationType": 0,
  "AppIcon": ""
}
```

**Response (202 Accepted)**:
```json
{
  "RequestStatusInfo": {
    "AppId": "meine-firma/mein-app/v1",
    "RegistrationRequestId": "295C196B-CBB0-4E76-9050-ECEC3356DDA6",
    "Status": 0
  }
}
```

### GET /authentication/{registrationId}

**Zweck**: Registrierungsstatus und API-Key abrufen

**Request**:
```http
GET /authentication/295C196B-CBB0-4E76-9050-ECEC3356DDA6 HTTP/1.1
Host: localhost:5883
api-version: 1.0
X-ChallengeCode: mein-geheimer-code
```

**Response (200 OK - nach Genehmigung)**:
```json
{
  "RequestStatusInfo": {
    "AppId": "meine-firma/mein-app/v1",
    "RegistrationRequestId": "295C196B-CBB0-4E76-9050-ECEC3356DDA6",
    "Status": 1
  },
  "Token": {
    "ApiKey": "FB622234-98A7-46FA-A01B-06C9D0971AAF"
  },
  "GrantedScopes": "all.read,customer.createcustomer"
}
```

## Standard API Headers (nach Registrierung)

Alle API-Anfragen nach erfolgreicher Registrierung benötigen:

```http
Authorization: Wawi FB622234-98A7-46FA-A01B-06C9D0971AAF
api-version: 1.0
X-AppID: meine-firma/mein-app/v1
X-AppVersion: 1.0.0
Content-Type: application/json
```

## Wichtige Business-Endpoints

### Kunden (customer)

| Methode | Endpoint | Beschreibung | Scope |
|---------|----------|--------------|-------|
| GET | `/customer/{id}` | Kunde abrufen | `customer.getcustomer` |
| POST | `/customer` | Kunde anlegen | `customer.createcustomer` |
| PUT | `/customer/{id}` | Kunde aktualisieren | `customer.updatecustomer` |
| DELETE | `/customer/{id}` | Kunde löschen | `customer.deletecustomer` |
| POST | `/customer/query` | Kunden suchen | `customer.querycustomers` |

**Beispiel: Kunden suchen**:
```http
POST /customer/query HTTP/1.1
Authorization: Wawi {API-KEY}
api-version: 1.0
Content-Type: application/json

{
  "SearchKeyWord": "Mustermann",
  "PageSize": 100,
  "PageIndex": 0
}
```

### Aufträge (salesorder)

| Methode | Endpoint | Beschreibung | Scope |
|---------|----------|--------------|-------|
| GET | `/salesorder/{id}` | Auftrag abrufen | `salesorder.getsalesorder` |
| POST | `/salesorder` | Auftrag anlegen | `salesorder.createsalesorder` |
| POST | `/salesorder/query` | Aufträge suchen | `salesorder.querysalesorders` |

### Artikel (article)

| Methode | Endpoint | Beschreibung | Scope |
|---------|----------|--------------|-------|
| GET | `/article/{id}` | Artikel abrufen | `article.getarticle` |
| POST | `/article/query` | Artikel suchen | `article.queryarticles` |

### Lagerbestand (stock)

| Methode | Endpoint | Beschreibung | Scope |
|---------|----------|--------------|-------|
| POST | `/stock/adjustment` | Bestand anpassen | `stock.stockadjustment` |
| POST | `/stock/query` | Bestand abfragen | `stock.querystock` |

### Rechnungen (invoice)

| Methode | Endpoint | Beschreibung | Scope |
|---------|----------|--------------|-------|
| GET | `/invoice/{id}` | Rechnung abrufen | `invoice.getinvoice` |
| POST | `/invoice/query` | Rechnungen suchen | `invoice.queryinvoices` |

### Firmen (company)

| Methode | Endpoint | Beschreibung | Scope |
|---------|----------|--------------|-------|
| POST | `/company/query` | Firmen abfragen | `company.querycompanies` |

### Kategorien (category)

| Methode | Endpoint | Beschreibung | Scope |
|---------|----------|--------------|-------|
| GET | `/category/{id}` | Kategorie abrufen | `category.getcategory` |
| POST | `/category` | Kategorie anlegen | `category.createcategory` |
| POST | `/category/query` | Kategorien suchen | `category.querycategories` |

## Query-Request Format

Die meisten Query-Endpoints verwenden ein einheitliches Format:

```json
{
  "SearchKeyWord": "Suchbegriff",
  "PageSize": 100,
  "PageIndex": 0,
  "Filter": {
    "FieldName": "Wert"
  },
  "SortBy": "CreatedDate",
  "SortDirection": "Descending"
}
```

## Pagination

Alle Query-Endpoints unterstützen Pagination:

| Parameter | Typ | Beschreibung | Standard |
|-----------|-----|--------------|----------|
| `PageSize` | int | Einträge pro Seite | 100 |
| `PageIndex` | int | Seitennummer (0-basiert) | 0 |

**Response-Format**:
```json
{
  "TotalCount": 1500,
  "PageSize": 100,
  "PageIndex": 0,
  "Items": [...]
}
```

## Fehler-Responses

### 400 Bad Request
```json
{
  "type": "https://tools.ietf.org/html/rfc7231#section-6.5.1",
  "title": "Bad Request",
  "status": 400,
  "detail": "The request was invalid.",
  "errors": {
    "AppId": ["The AppId field is required."]
  }
}
```

### 401 Unauthorized
```json
{
  "type": "https://tools.ietf.org/html/rfc7235#section-3.1",
  "title": "Unauthorized",
  "status": 401,
  "detail": "Invalid or missing API key."
}
```

### 403 Forbidden
```json
{
  "type": "https://tools.ietf.org/html/rfc7231#section-6.5.3",
  "title": "Forbidden",
  "status": 403,
  "detail": "Insufficient permissions. Required scope: customer.createcustomer"
}
```

### 404 Not Found
```json
{
  "type": "https://tools.ietf.org/html/rfc7231#section-6.5.4",
  "title": "Not Found",
  "status": 404,
  "detail": "Customer with ID 12345 not found."
}
```

## API-Versionen

| Version | Status | Bemerkung |
|---------|--------|-----------|
| 1.0 | Stabil | OnPrem Standard |
| 1.1 | Stabil | Cloud Standard |
| 1.2 | Beta | Neue Features |

**Version im Header angeben**:
```http
api-version: 1.0
```

## Rate Limiting

| Umgebung | Limit | Zeitraum |
|----------|-------|----------|
| OnPrem | Kein Limit | - |
| Cloud | 1000 Anfragen | pro Minute |

Bei Überschreitung: `429 Too Many Requests`

## Swagger/OpenAPI

Interaktive API-Dokumentation:

- **OnPrem**: `http://localhost:5883/swagger`
- **Online**: https://developer.jtl-software.com/products/erpapi/openapi

## ⚠️ Häufige Endpoint-Fehler und Lösungen

### 1. URL-Pfad-Fehler

| Fehler | Problem | Richtig |
|--------|---------|---------|
| `404 Not Found` | `/customers` statt `/v1/customers` | `/api/eazybusiness/v1/customers` |
| `404 Not Found` | `/rest/...` statt `/api/...` | `/api/...` (aktuelles Format) |
| `404 Not Found` | Mandant fehlt | `/api/eazybusiness/...` nicht `/api/...` |
| `404 Not Found` | Falsche Groß-/Kleinschreibung | Mandantenname exakt wie in DB |

### 2. HTTP-Methoden-Fehler

| Fehler | Problem | Richtig |
|--------|---------|---------|
| `405 Method Not Allowed` | GET für Suche verwendet | POST `/customer/query` für Suche |
| `405 Method Not Allowed` | POST für Abruf verwendet | GET `/customer/{id}` für Einzelabruf |

**Wichtig: PUT vs POST bei JTL-Wawi API**

- **PUT**: Zum **Validieren/Berechnen** von Werten (gibt berechnete Werte zurück)
- **POST**: Zum **tatsächlichen Speichern** von Daten

### 3. Endpoint-Namenskonventionen

| Falsch ❌ | Richtig ✓ | Hinweis |
|-----------|-----------|---------|
| `/customers` | `/customer` | Singular für Einzeloperationen |
| `/customer/search` | `/customer/query` | "query" nicht "search" |
| `/articles` | `/article` | Singular |
| `/orders` | `/salesorder` | "salesorder" nicht "order" |
| `/invoices` | `/invoice` | Singular |

### 4. Vollständige Endpoint-Übersicht

```
/api/{mandant}/v1/
├── authentication                  # App-Registrierung (kein Auth)
│   ├── POST /authentication        # Registrierung starten
│   └── GET /authentication/{id}    # Status/API-Key abrufen
│
├── customer                        # Kunden
│   ├── GET /{id}                   # Kunde abrufen
│   ├── POST /                      # Kunde anlegen
│   ├── PUT /{id}                   # Kunde aktualisieren
│   ├── DELETE /{id}                # Kunde löschen
│   └── POST /query                 # Kunden suchen
│
├── salesorder                      # Aufträge
│   ├── GET /{id}                   # Auftrag abrufen
│   ├── POST /                      # Auftrag anlegen
│   └── POST /query                 # Aufträge suchen
│
├── article                         # Artikel
│   ├── GET /{id}                   # Artikel abrufen
│   └── POST /query                 # Artikel suchen
│
├── stock                           # Lagerbestand
│   ├── POST /query                 # Bestand abfragen
│   └── POST /adjustment            # Bestand anpassen
│
├── invoice                         # Rechnungen
│   ├── GET /{id}                   # Rechnung abrufen
│   └── POST /query                 # Rechnungen suchen
│
├── deliverynote                    # Lieferscheine
│   ├── GET /{id}                   # Lieferschein abrufen
│   └── POST /query                 # Lieferscheine suchen
│
├── category                        # Kategorien
│   ├── GET /{id}                   # Kategorie abrufen
│   ├── POST /                      # Kategorie anlegen
│   └── POST /query                 # Kategorien suchen
│
├── company                         # Firmen
│   └── POST /query                 # Firmen abfragen
│
├── offer                           # Angebote
│   ├── GET /{id}                   # Angebot abrufen
│   ├── POST /                      # Angebot anlegen
│   └── POST /query                 # Angebote suchen
│
├── creditnote                      # Gutschriften
│   ├── GET /{id}                   # Gutschrift abrufen
│   └── POST /query                 # Gutschriften suchen
│
├── return                          # Retouren
│   ├── GET /{id}                   # Retoure abrufen
│   ├── POST /                      # Retoure anlegen
│   └── POST /query                 # Retouren suchen
│
├── warehouse                       # Lager
│   └── POST /query                 # Lager abfragen
│
├── workers                         # Synchronisation
│   ├── GET /status                 # Worker-Status
│   └── POST /configuresync         # Sync konfigurieren
│
└── info                            # System-Info
    └── GET /status                 # API-Status
```

### 5. cURL-Beispiele für Fehlerbehebung

**Prüfen ob Server erreichbar ist**:
```bash
curl -v http://localhost:5883/api/eazybusiness/v1/info/status \
  -H "Authorization: Wawi {API-KEY}" \
  -H "api-version: 1.0"
```

**Kunden suchen (POST, nicht GET!)**:
```bash
curl -X POST http://localhost:5883/api/eazybusiness/v1/customer/query \
  -H "Authorization: Wawi {API-KEY}" \
  -H "api-version: 1.0" \
  -H "Content-Type: application/json" \
  -d '{"SearchKeyWord": "Mustermann", "PageSize": 10}'
```

**Einzelnen Kunden abrufen (GET)**:
```bash
curl http://localhost:5883/api/eazybusiness/v1/customer/12345 \
  -H "Authorization: Wawi {API-KEY}" \
  -H "api-version: 1.0"
```

### 6. Debugging-Tipps

1. **Swagger UI nutzen**: `http://localhost:5883/swagger` zeigt alle verfügbaren Endpoints
2. **Postman verwenden**: API-Spezifikationen können importiert werden
3. **Server-Logs prüfen**: JTL.Wawi.Rest.exe Konsole zeigt Fehlerdetails
4. **api-version Header**: Immer angeben (`1.0` für OnPrem)
5. **Content-Type**: Bei POST/PUT immer `application/json` setzen
