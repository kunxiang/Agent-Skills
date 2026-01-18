---
name: creating-jtl-wawi-api-apps
description: "JTL-Wawi REST API App-Registrierung und Integration. Führt den kompletten App-Registrierungsprozess durch, konfiguriert API-Authentifizierung und erstellt API-Client-Implementierungen. Verwenden bei: (1) JTL-Wawi API App registrieren, (2) API-Authentifizierung mit X-ChallengeCode einrichten, (3) API-Key durch Polling-Mechanismus abrufen, (4) REST-Client für JTL-Wawi implementieren. Keywords: JTL-Wawi, REST API, App-Registrierung, RegisterApp, ConfirmRegistration, API-Key, OAuth, X-ChallengeCode, OnPrem, Cloud."
---

# JTL-Wawi API App-Registrierung

## Offizielle Ressourcen

| Ressource | Link |
|-----------|------|
| API-Dokumentation | https://developer.jtl-software.com/products/erpapi |
| OnPrem API (Swagger) | https://developer.jtl-software.com/products/erpapi/openapi |
| Cloud API (Swagger) | https://developer.jtl-software.com/products/erpapi/1.1-cloud/openapi |
| App-Registrierung Swagger | https://wawi-api.jtl-software.com/#tag/appRegistration |
| JTL-Guide (Deutsch) | https://guide.jtl-software.com/jtl-wawi/jtl-wawi-api/ |

## Quick Reference

| Aufgabe | Lösung |
|---------|--------|
| App registrieren | POST `/authentication` mit App-Daten |
| Status prüfen | GET `/authentication/{registrationId}` (Polling) |
| API nutzen | Header `Authorization: Wawi {API-KEY}` |
| X-ChallengeCode | Beliebiger Wert, max. 30 Zeichen, bei allen Anfragen identisch |
| API-Version | Header `api-version: 1.0` |

## Voraussetzungen

1. **JTL-Wawi 1.9+** installiert (neue Oberfläche)
2. **REST-Server gestartet** (OnPrem) oder Cloud-Zugang
3. **Registrierung initiiert**: In JTL-Wawi unter `Admin → App-Registrierung` starten

## Registrierungsablauf (3 Schritte)

```
┌─────────────┐      POST /authentication       ┌─────────────┐
│  Ihre App   │ ──────────────────────────────→ │  JTL-Wawi   │
│             │ ←─────────────────────────────  │    API      │
│             │    RegistrationRequestId         │             │
└─────────────┘                                  └─────────────┘
       │                                                │
       │  Benutzer bestätigt in JTL-Wawi              │
       │  (Admin → App-Registrierung → Akzeptieren)    │
       │                                                │
       ▼                                                │
┌─────────────┐   GET /authentication/{id}       ┌─────────────┐
│  Ihre App   │ ──────────────────────────────→ │  JTL-Wawi   │
│  (Polling)  │ ←─────────────────────────────  │    API      │
│             │         API-Key (einmalig!)      │             │
└─────────────┘                                  └─────────────┘
```

**WICHTIG**: Der API-Key wird nur EINMAL angezeigt! Sofort sicher speichern!

## OnPrem: REST-Server starten

```bash
# Beispiel: Server auf localhost:5883 starten
JTL.Wawi.Rest.exe -w "Standard" -l 127.0.0.1 --port 5883 -d eazybusiness

# Oder für Netzwerkzugriff
JTL.Wawi.Rest.exe -w "Standard" -l 0.0.0.0 --port 5883 -d eazybusiness
```

| Parameter | Beschreibung |
|-----------|--------------|
| `-w` | Mandantenname (z.B. "Standard") |
| `-l` | IP-Adresse (127.0.0.1, 0.0.0.0, oder LAN-IP) |
| `--port` | Port-Nummer (Standard: 5883) |
| `-d` | Datenbankname |

## Schritt 1: App registrieren (POST)

**Endpoint**: `POST /authentication`

**Headers**:
```
Content-Type: application/json
api-version: 1.0
X-ChallengeCode: mein-geheimer-code-123
```

**Request Body**:
```json
{
  "AppId": "meine-firma/mein-app/v1",
  "DisplayName": "Meine App",
  "Description": "Beschreibung der App-Funktionen",
  "Version": "1.0.0",
  "ProviderName": "Meine Firma GmbH",
  "ProviderWebsite": "https://www.meine-firma.de",
  "MandatoryApiScopes": [
    "all.read",
    "customer.createcustomer",
    "salesorder.createsalesorder"
  ],
  "OptionalApiScopes": [],
  "RegistrationType": 0,
  "AppIcon": ""
}
```

**Response** (202 Accepted):
```json
{
  "RequestStatusInfo": {
    "AppId": "meine-firma/mein-app/v1",
    "RegistrationRequestId": "295C196B-CBB0-4E76-9050-ECEC3356DDA6",
    "Status": 0
  }
}
```

## Schritt 2: In JTL-Wawi bestätigen

1. Öffnen Sie JTL-Wawi (neue Oberfläche)
2. Navigieren zu: `Admin → App-Registrierung`
3. Ihre App erscheint in der Liste
4. Klicken Sie auf **Akzeptieren/Genehmigen**

## Schritt 3: Status abfragen (Polling)

**Endpoint**: `GET /authentication/{RegistrationRequestId}`

**Headers**:
```
api-version: 1.0
X-ChallengeCode: mein-geheimer-code-123
```

**Response** (nach Bestätigung):
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
  "GrantedScopes": "all.read,customer.createcustomer,salesorder.createsalesorder"
}
```

**Polling-Strategie**: Alle 5 Sekunden abfragen, bis `Token.ApiKey` vorhanden.

## API nutzen (nach Registrierung)

**Standard-Headers für alle Anfragen**:
```
Authorization: Wawi FB622234-98A7-46FA-A01B-06C9D0971AAF
api-version: 1.0
X-AppID: meine-firma/mein-app/v1
X-AppVersion: 1.0.0
```

## RegistrationType

| Wert | Typ | Beschreibung |
|------|-----|--------------|
| 0 | OneInstance | Eine Instanz pro JTL-Wawi |
| 1 | MultiInstance | Mehrere Instanzen erlaubt |
| 2 | PerUserInstance | Eine Instanz pro Benutzer |
| 3 | PerUserLoginInstance | Eine Instanz pro Login |

## Häufige API-Scopes

| Scope | Beschreibung |
|-------|--------------|
| `all.read` | Alle Lesezugriffe |
| `customer.createcustomer` | Kunden anlegen |
| `customer.getcustomer` | Kunden abrufen |
| `salesorder.createsalesorder` | Aufträge anlegen |
| `salesorder.getsalesorder` | Aufträge abrufen |
| `stock.stockadjustment` | Bestand anpassen |
| `article.getarticle` | Artikel abrufen |

Vollständige Liste: [references/scopes.md](references/scopes.md)

## Python Beispiel

```python
import requests
import time

BASE_URL = "http://localhost:5883"
CHALLENGE_CODE = "mein-geheimer-code"
HEADERS = {
    "Content-Type": "application/json",
    "api-version": "1.0",
    "X-ChallengeCode": CHALLENGE_CODE
}

# Schritt 1: Registrieren
app_data = {
    "AppId": "meine-firma/mein-app/v1",
    "DisplayName": "Meine App",
    "Description": "Meine App Beschreibung",
    "Version": "1.0.0",
    "ProviderName": "Meine Firma",
    "ProviderWebsite": "https://meine-firma.de",
    "MandatoryApiScopes": ["all.read"],
    "RegistrationType": 0
}

response = requests.post(
    f"{BASE_URL}/authentication",
    json=app_data,
    headers=HEADERS
)
registration_id = response.json()["RequestStatusInfo"]["RegistrationRequestId"]
print(f"Bitte App in JTL-Wawi genehmigen. ID: {registration_id}")

# Schritt 2: Polling
api_key = None
while not api_key:
    time.sleep(5)
    status = requests.get(
        f"{BASE_URL}/authentication/{registration_id}",
        headers=HEADERS
    ).json()

    if "Token" in status and status["Token"].get("ApiKey"):
        api_key = status["Token"]["ApiKey"]
        print(f"API-Key erhalten: {api_key}")
        print("WICHTIG: Sicher speichern - wird nicht erneut angezeigt!")
```

## cURL Beispiele

**Registrierung**:
```bash
curl -X POST "http://localhost:5883/authentication" \
  -H "Content-Type: application/json" \
  -H "api-version: 1.0" \
  -H "X-ChallengeCode: mein-code" \
  -d '{
    "AppId": "test/app/v1",
    "DisplayName": "Test App",
    "Description": "Test",
    "Version": "1.0.0",
    "ProviderName": "Test",
    "ProviderWebsite": "https://test.de",
    "MandatoryApiScopes": ["all.read"],
    "RegistrationType": 0
  }'
```

**Status prüfen**:
```bash
curl -X GET "http://localhost:5883/authentication/{REGISTRATION_ID}" \
  -H "api-version: 1.0" \
  -H "X-ChallengeCode: mein-code"
```

## ⚠️ KRITISCHE HINWEISE (aus Community-Erfahrungen)

### 1. Authorization Header Format - HÄUFIGSTER FEHLER!

**FALSCH** ❌:
```
Authorization: FB622234-98A7-46FA-A01B-06C9D0971AAF
Authorization: Bearer FB622234-98A7-46FA-A01B-06C9D0971AAF
```

**RICHTIG** ✓:
```
Authorization: Wawi FB622234-98A7-46FA-A01B-06C9D0971AAF
```

> Forum-Zitat: "Es fehlt das 'Wawi' vor dem API Key. Man sollte besser die Doku anschauen."

### 2. JTL-Wawi UI: "Neue Oberfläche" erforderlich!

Das Dialogfenster `Admin → App-Registrierung` ist **NUR** in der neuen Oberfläche verfügbar:
- Starten über: `C:\Program Files (x86)\JTL-Software\JTL-SharpWawi.exe`
- NICHT über die alte WaWi-Oberfläche!

### 3. Registrierung muss ZUERST in JTL-Wawi gestartet werden

```
REIHENFOLGE:
1. JTL-Wawi öffnen → Admin → App-Registrierung → Hinzufügen → Weiter
2. JTL-Wawi wartet jetzt auf API-Anfrage ("Registrierung beginnen")
3. DANN erst POST /authentication senden
4. JTL-Wawi springt automatisch weiter
5. Berechtigungen bestätigen → Fertigstellen
6. API-Key wird angezeigt (NUR EINMAL!)
```

### 4. Datenbank-Feld bei OnPrem (nicht "eazybusiness"!)

Wenn Ihr Mandant NICHT "eazybusiness" heißt, muss der **exakte Tabellenname** angegeben werden:
```bash
# FALSCH (wenn Mandant anders heißt):
JTL.Wawi.Rest.exe -d eazybusiness

# RICHTIG:
JTL.Wawi.Rest.exe -d IhrMandantenName
```

### 5. Scopes minimal halten!

> Forum-Erfahrung: "Bei manchen Nutzern hatte die Registrierung wegen zu vieler Scopes nicht funktioniert."

**Empfehlung**: Mit `["all.read"]` starten, dann erweitern.

### 6. NICHT als Windows-Dienst bei Ersteinrichtung!

Die erste Registrierung sollte **nicht** mit der Start-Art "als Windows-Dienst" durchgeführt werden.

## Häufige Fehler

| Problem | Ursache | Lösung |
|---------|---------|--------|
| **401 Unauthorized** | "Wawi" Prefix fehlt | `Authorization: Wawi {KEY}` verwenden |
| **401 Unauthorized** | Falsche X-AppID/X-AppVersion | Muss mit Registrierung übereinstimmen |
| **401 Unauthorized** | App nicht genehmigt | In JTL-Wawi "Fertigstellen" klicken |
| **403 Forbidden** | Fehlende Scopes | Scope bei Registrierung hinzufügen |
| **Keine Reaktion** | Reihenfolge falsch | Erst in JTL-Wawi starten, dann API |
| **Menüpunkt fehlt** | Falsche WaWi-Version | Neue Oberfläche (SharpWawi.exe) nutzen |
| **Connection refused** | Server nicht gestartet | `JTL.Wawi.Rest.exe` starten |
| **Registrierung hängt** | Falscher Mandant/DB | Datenbank-Parameter prüfen |
| **API-Key verloren** | Nur einmal angezeigt | Neue App registrieren (keine Wiederherstellung!) |
| **Lizenzfehler** | Keine API-Lizenz | JTL-Kundencenter: API-Lizenz buchen |

## Referenzen

- **Registrierungsablauf**: [references/registration-flow.md](references/registration-flow.md) - Detaillierter Ablauf
- **API-Endpoints**: [references/api-endpoints.md](references/api-endpoints.md) - Alle Endpoints
- **Scopes**: [references/scopes.md](references/scopes.md) - Vollständige Scope-Liste

## Assets (Vorlagen)

| Datei | Zweck |
|-------|-------|
| `assets/templates/register_app.py` | Python-Registrierungsskript |
| `assets/templates/api_client.py` | Python API-Client Vorlage |
| `assets/templates/register_app.sh` | Bash-Registrierungsskript |

## Cloud vs. OnPrem

| Aspekt | OnPrem | Cloud |
|--------|--------|-------|
| Base URL | `http://localhost:5883` | `https://api.jtl-software.com/...` |
| REST-Server | Manuell starten | Automatisch |
| OAuth | Nicht erforderlich | Client Credentials Flow |
| Verfügbarkeit | Abhängig von Server | 24/7 |
