# JTL-Wawi API Registrierungsablauf

## Übersicht

Die App-Registrierung bei der JTL-Wawi API ist ein dreistufiger Prozess, der eine manuelle Bestätigung in JTL-Wawi erfordert. Dies gewährleistet die Sicherheit, da nur autorisierte Apps Zugriff erhalten.

## Voraussetzungen

### OnPrem (Lokal installierte JTL-Wawi)

1. **JTL-Wawi Version 1.9 oder höher** mit neuer Oberfläche
2. **REST-Server gestartet**:
   ```bash
   JTL.Wawi.Rest.exe -w "Mandantenname" -l 127.0.0.1 --port 5883 -d datenbankname
   ```
3. **Firewall-Regeln** (falls Netzwerkzugriff benötigt)

### Cloud

1. **JTL-Cloud-Konto** mit aktivierter API
2. **Client-ID und Client-Secret** für OAuth2

## Detaillierter Ablauf

### Phase 1: Registrierungsanfrage senden

```
┌──────────────────────────────────────────────────────────────────┐
│                     PHASE 1: REGISTRIERUNG                        │
├──────────────────────────────────────────────────────────────────┤
│                                                                    │
│   Ihre App                           JTL-Wawi REST-Server         │
│      │                                      │                      │
│      │  POST /authentication               │                      │
│      │  Headers:                            │                      │
│      │    - Content-Type: application/json  │                      │
│      │    - api-version: 1.0                │                      │
│      │    - X-ChallengeCode: <ihr-code>     │                      │
│      │  Body: { AppId, DisplayName, ... }   │                      │
│      │────────────────────────────────────→│                      │
│      │                                      │                      │
│      │  Response 202 Accepted              │                      │
│      │  {                                   │                      │
│      │    "RequestStatusInfo": {            │                      │
│      │      "RegistrationRequestId": "..."  │                      │
│      │      "Status": 0                     │                      │
│      │    }                                 │                      │
│      │  }                                   │                      │
│      │←────────────────────────────────────│                      │
│      │                                      │                      │
└──────────────────────────────────────────────────────────────────┘
```

**Status-Werte**:
- `0` = Ausstehend (Pending)
- `1` = Genehmigt (Approved)
- `2` = Abgelehnt (Rejected)

### Phase 2: Manuelle Genehmigung in JTL-Wawi

**⚠️ WICHTIG: Korrekte Reihenfolge beachten!**

```
┌──────────────────────────────────────────────────────────────────┐
│           PHASE 2: MANUELLE GENEHMIGUNG (SCHRITT FÜR SCHRITT)     │
├──────────────────────────────────────────────────────────────────┤
│                                                                    │
│   VORHER (bevor POST /authentication gesendet wird!):             │
│   ─────────────────────────────────────────────────               │
│   1. JTL-Wawi öffnen (NEUE Oberfläche: JTL-SharpWawi.exe)        │
│                                                                    │
│   2. Navigation: Admin → App-Registrierung                        │
│                                                                    │
│   3. Klick auf "Hinzufügen"                                       │
│                                                                    │
│   4. Einführungsseite → "Weiter" klicken                         │
│                                                                    │
│   5. Seite "Registrierung beginnen" wird angezeigt               │
│      ┌─────────────────────────────────────────────────┐          │
│      │  JTL-Wawi wartet jetzt auf API-Anfrage...      │          │
│      │  (Der "Weiter"-Button ist ausgegraut)           │          │
│      └─────────────────────────────────────────────────┘          │
│                                                                    │
│   JETZT: POST /authentication von Ihrer App senden                │
│   ────────────────────────────────────────────────                │
│                                                                    │
│   NACHHER (nach erfolgreicher API-Anfrage):                       │
│   ─────────────────────────────────────────                       │
│   6. JTL-Wawi springt AUTOMATISCH auf "Anwendungsinformationen"  │
│      - App-ID wird angezeigt                                      │
│      - Angeforderte Berechtigungen (Scopes) werden angezeigt     │
│                                                                    │
│   7. Optionale Berechtigungen aktivieren/deaktivieren            │
│                                                                    │
│   8. "Weiter" klicken                                             │
│                                                                    │
│   9. Übersichtsseite → "Fertigstellen" klicken                   │
│                                                                    │
│   10. API-Key wird angezeigt (NUR JETZT, EINMALIG!)              │
│       ┌─────────────────────────────────────────────────┐         │
│       │  API Token: FB622234-98A7-46FA-A01B-06C9D0971AAF│         │
│       │                                                  │         │
│       │  ⚠️ Dieser Schlüssel wird NICHT erneut angezeigt!│         │
│       │     Kopieren Sie ihn JETZT und speichern Sie    │         │
│       │     ihn an einem sicheren Ort!                  │         │
│       └─────────────────────────────────────────────────┘         │
│                                                                    │
└──────────────────────────────────────────────────────────────────┘
```

### Hinweis zur "Neuen Oberfläche"

Das App-Registrierungsfenster ist **NUR** in der neuen JTL-Wawi Oberfläche verfügbar:

```
RICHTIG:  C:\Program Files (x86)\JTL-Software\JTL-SharpWawi.exe
FALSCH:   C:\Program Files (x86)\JTL-Software\JTL-Wawi.exe (alte Oberfläche)
```

Falls der Menüpunkt `Admin → App-Registrierung` nicht sichtbar ist:
- Prüfen Sie, ob Sie die richtige Wawi-Version gestartet haben
- Prüfen Sie, ob Sie Admin-Rechte haben
- Prüfen Sie, ob die API-Lizenz im JTL-Kundencenter gebucht wurde

### Phase 3: API-Key abrufen (Polling)

```
┌──────────────────────────────────────────────────────────────────┐
│                      PHASE 3: API-KEY ABRUFEN                     │
├──────────────────────────────────────────────────────────────────┤
│                                                                    │
│   Ihre App                           JTL-Wawi REST-Server         │
│      │                                      │                      │
│      │  GET /authentication/{id}            │                      │
│      │  Headers:                            │                      │
│      │    - api-version: 1.0                │                      │
│      │    - X-ChallengeCode: <ihr-code>     │                      │
│      │────────────────────────────────────→│                      │
│      │                                      │                      │
│      │  Response 200 OK (nach Genehmigung) │                      │
│      │  {                                   │                      │
│      │    "RequestStatusInfo": {            │                      │
│      │      "Status": 1                     │                      │
│      │    },                                │                      │
│      │    "Token": {                        │                      │
│      │      "ApiKey": "FB622234-..."        │   ← EINMALIG!       │
│      │    },                                │                      │
│      │    "GrantedScopes": "all.read,..."   │                      │
│      │  }                                   │                      │
│      │←────────────────────────────────────│                      │
│      │                                      │                      │
└──────────────────────────────────────────────────────────────────┘
```

## Polling-Implementierung

### Empfohlene Strategie

```python
import time

MAX_ATTEMPTS = 120  # 10 Minuten bei 5s Intervall
POLL_INTERVAL = 5   # Sekunden

def poll_for_api_key(registration_id, headers):
    for attempt in range(MAX_ATTEMPTS):
        response = requests.get(
            f"{BASE_URL}/authentication/{registration_id}",
            headers=headers
        )

        data = response.json()
        status = data.get("RequestStatusInfo", {}).get("Status")

        if status == 1:  # Genehmigt
            api_key = data.get("Token", {}).get("ApiKey")
            if api_key:
                return api_key

        elif status == 2:  # Abgelehnt
            raise Exception("App-Registrierung wurde abgelehnt")

        print(f"Warte auf Genehmigung... (Versuch {attempt + 1}/{MAX_ATTEMPTS})")
        time.sleep(POLL_INTERVAL)

    raise TimeoutError("Timeout: Keine Genehmigung innerhalb der Zeit")
```

### Wichtige Hinweise zum Polling

1. **Intervall**: 5 Sekunden ist ein guter Kompromiss
2. **Timeout**: 10-15 Minuten empfohlen (Benutzer braucht Zeit)
3. **X-ChallengeCode**: MUSS bei allen Anfragen identisch sein
4. **Fehlerbehandlung**: Status 2 = Ablehnung, nicht weiter pollen

## X-ChallengeCode

Der X-ChallengeCode ist ein Sicherheitsmechanismus:

```
┌─────────────────────────────────────────────────────────────────┐
│                       X-CHALLENGECODE                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  • Beliebiger String (max. 30 Zeichen)                           │
│  • Muss bei ALLEN Registrierungsanfragen identisch sein          │
│  • Verhindert Man-in-the-Middle-Angriffe                         │
│  • Empfehlung: Zufällig generierter, sicherer String             │
│                                                                   │
│  Beispiele:                                                       │
│    ✓ "abc123xyz789"                                              │
│    ✓ "meineFirma-2024-geheim"                                    │
│    ✓ "a1b2c3d4e5f6g7h8i9j0"                                      │
│    ✗ "zu-langer-challenge-code-der-mehr-als-dreissig-zeichen"    │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

## Request Body Felder

### Pflichtfelder

| Feld | Typ | Beschreibung | Beispiel |
|------|-----|--------------|----------|
| `AppId` | string | Eindeutige App-ID | `"meineFirma/meinApp/v1"` |
| `DisplayName` | string | Anzeigename in JTL-Wawi | `"Meine App"` |
| `Description` | string | Beschreibung | `"Synchronisiert Daten..."` |
| `Version` | string | App-Version | `"1.0.0"` |
| `ProviderName` | string | Anbieter-Name | `"Meine Firma GmbH"` |
| `ProviderWebsite` | string | Anbieter-Website | `"https://meine-firma.de"` |
| `MandatoryApiScopes` | string[] | Erforderliche Berechtigungen | `["all.read"]` |

### Optionale Felder

| Feld | Typ | Beschreibung | Standard |
|------|-----|--------------|----------|
| `OptionalApiScopes` | string[] | Optionale Berechtigungen | `[]` |
| `RegistrationType` | int | Instanz-Typ (0-3) | `0` |
| `AppIcon` | string | Base64-kodiertes Icon | `""` |
| `LocalizedDisplayNames` | object[] | Übersetzte Namen | `[]` |
| `LocalizedDescriptions` | object[] | Übersetzte Beschreibungen | `[]` |
| `Signature` | string | Signatur (für verifizierte Apps) | `""` |
| `SignatureData` | string | Signatur-Daten | `""` |

## Fehlerbehandlung

### HTTP Status Codes

| Code | Bedeutung | Aktion |
|------|-----------|--------|
| 202 | Registrierung akzeptiert | Polling starten |
| 200 | Status abgerufen | Token prüfen |
| 400 | Ungültige Anfrage | Request Body prüfen |
| 401 | Nicht autorisiert | X-ChallengeCode prüfen |
| 404 | ID nicht gefunden | Registration ID prüfen |
| 500 | Serverfehler | Später erneut versuchen |

### Häufige Probleme

| Problem | Ursache | Lösung |
|---------|---------|--------|
| Keine Response | REST-Server nicht gestartet | Server starten |
| Status bleibt 0 | Keine Genehmigung | In JTL-Wawi genehmigen |
| X-ChallengeCode Fehler | Code geändert | Gleichen Code verwenden |
| Scopes nicht gewährt | In JTL-Wawi abgelehnt | Erneut registrieren |

## Sicherheitshinweise

1. **API-Key sicher speichern**: Umgebungsvariable oder verschlüsselte Konfiguration
2. **X-ChallengeCode**: Nicht im Code hardcoden, Konfiguration nutzen
3. **HTTPS verwenden**: Bei Netzwerkzugriff immer verschlüsselt
4. **Minimale Scopes**: Nur benötigte Berechtigungen anfordern
5. **Key-Rotation**: Bei Verdacht auf Kompromittierung neu registrieren
