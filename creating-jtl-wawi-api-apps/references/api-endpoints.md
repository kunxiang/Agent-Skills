# JTL-Wawi API Endpoints

## Base URLs

| Umgebung | URL | Bemerkung |
|----------|-----|-----------|
| OnPrem (lokal) | `http://localhost:5883` | Standard-Port |
| OnPrem (Netzwerk) | `http://<IP>:5883` | Firewall beachten |
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
