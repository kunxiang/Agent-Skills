#!/usr/bin/env python3
"""
JTL-Wawi API App-Registrierung

Dieses Skript führt die vollständige App-Registrierung durch:
1. Registrierungsanfrage senden
2. Auf Genehmigung in JTL-Wawi warten (Polling)
3. API-Key speichern

Verwendung:
    python register_app.py

Konfiguration:
    Umgebungsvariablen oder .env-Datei:
    - JTL_API_BASE_URL: z.B. http://localhost:5883
    - JTL_CHALLENGE_CODE: Beliebiger String (max. 30 Zeichen)
"""

import os
import sys
import time
import json
import requests
from dataclasses import dataclass
from typing import Optional

# Konfiguration
BASE_URL = os.getenv("JTL_API_BASE_URL", "http://localhost:5883")
CHALLENGE_CODE = os.getenv("JTL_CHALLENGE_CODE", "mein-geheimer-code")
POLL_INTERVAL = 5  # Sekunden
MAX_POLL_ATTEMPTS = 120  # 10 Minuten

# App-Konfiguration (ANPASSEN!)
APP_CONFIG = {
    "AppId": "meine-firma/meine-app/v1",
    "DisplayName": "Meine App",
    "Description": "Beschreibung meiner App-Funktionen",
    "Version": "1.0.0",
    "ProviderName": "Meine Firma GmbH",
    "ProviderWebsite": "https://www.meine-firma.de",
    "MandatoryApiScopes": [
        "all.read",
        "customer.createcustomer",
        "salesorder.createsalesorder"
    ],
    "OptionalApiScopes": [],
    "RegistrationType": 0,  # 0=OneInstance, 1=MultiInstance, 2=PerUserInstance, 3=PerUserLoginInstance
    "AppIcon": ""
}


@dataclass
class RegistrationResult:
    """Ergebnis der Registrierung"""
    success: bool
    api_key: Optional[str] = None
    granted_scopes: Optional[str] = None
    error: Optional[str] = None


def get_headers(include_content_type: bool = False) -> dict:
    """Erstellt die Standard-Headers für die API"""
    headers = {
        "api-version": "1.0",
        "X-ChallengeCode": CHALLENGE_CODE
    }
    if include_content_type:
        headers["Content-Type"] = "application/json"
    return headers


def register_app() -> Optional[str]:
    """
    Schritt 1: App bei der API registrieren

    Returns:
        RegistrationRequestId oder None bei Fehler
    """
    print(f"Registriere App bei {BASE_URL}...")
    print(f"App-ID: {APP_CONFIG['AppId']}")
    print(f"Angeforderte Scopes: {', '.join(APP_CONFIG['MandatoryApiScopes'])}")
    print()

    try:
        response = requests.post(
            f"{BASE_URL}/authentication",
            json=APP_CONFIG,
            headers=get_headers(include_content_type=True),
            timeout=30
        )

        if response.status_code == 202:
            data = response.json()
            registration_id = data.get("RequestStatusInfo", {}).get("RegistrationRequestId")
            print(f"✓ Registrierung eingereicht!")
            print(f"  Registration-ID: {registration_id}")
            return registration_id
        else:
            print(f"✗ Fehler: HTTP {response.status_code}")
            print(f"  Response: {response.text}")
            return None

    except requests.exceptions.ConnectionError:
        print(f"✗ Verbindungsfehler: Kann {BASE_URL} nicht erreichen")
        print("  Ist der JTL-Wawi REST-Server gestartet?")
        return None
    except requests.exceptions.Timeout:
        print("✗ Timeout: Server antwortet nicht")
        return None
    except Exception as e:
        print(f"✗ Unerwarteter Fehler: {e}")
        return None


def poll_for_approval(registration_id: str) -> RegistrationResult:
    """
    Schritt 2 & 3: Auf Genehmigung warten und API-Key abrufen

    Args:
        registration_id: Die RegistrationRequestId aus Schritt 1

    Returns:
        RegistrationResult mit API-Key oder Fehler
    """
    print()
    print("=" * 60)
    print("WICHTIG: Bitte App in JTL-Wawi genehmigen!")
    print("  Navigation: Admin → App-Registrierung → Genehmigen")
    print("=" * 60)
    print()

    for attempt in range(1, MAX_POLL_ATTEMPTS + 1):
        try:
            response = requests.get(
                f"{BASE_URL}/authentication/{registration_id}",
                headers=get_headers(),
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                status = data.get("RequestStatusInfo", {}).get("Status")

                # Status 1 = Genehmigt
                if status == 1:
                    token_data = data.get("Token", {})
                    api_key = token_data.get("ApiKey")
                    granted_scopes = data.get("GrantedScopes", "")

                    if api_key:
                        return RegistrationResult(
                            success=True,
                            api_key=api_key,
                            granted_scopes=granted_scopes
                        )

                # Status 2 = Abgelehnt
                elif status == 2:
                    return RegistrationResult(
                        success=False,
                        error="App-Registrierung wurde in JTL-Wawi abgelehnt"
                    )

                # Status 0 = Ausstehend
                else:
                    print(f"  Warte auf Genehmigung... ({attempt}/{MAX_POLL_ATTEMPTS})", end="\r")

            else:
                print(f"  Warnung: HTTP {response.status_code} - Versuche erneut...")

        except requests.exceptions.RequestException as e:
            print(f"  Warnung: {e} - Versuche erneut...")

        time.sleep(POLL_INTERVAL)

    return RegistrationResult(
        success=False,
        error=f"Timeout: Keine Genehmigung nach {MAX_POLL_ATTEMPTS * POLL_INTERVAL} Sekunden"
    )


def save_api_key(api_key: str, granted_scopes: str):
    """Speichert den API-Key in einer Datei"""
    env_file = ".env.jtl"

    with open(env_file, "w") as f:
        f.write(f"# JTL-Wawi API Credentials\n")
        f.write(f"# Generiert am: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"# WICHTIG: Diese Datei sicher aufbewahren!\n\n")
        f.write(f"JTL_API_BASE_URL={BASE_URL}\n")
        f.write(f"JTL_API_KEY={api_key}\n")
        f.write(f"JTL_APP_ID={APP_CONFIG['AppId']}\n")
        f.write(f"JTL_APP_VERSION={APP_CONFIG['Version']}\n")
        f.write(f"JTL_GRANTED_SCOPES={granted_scopes}\n")

    print(f"\n✓ API-Key gespeichert in: {env_file}")
    print("  WICHTIG: Diese Datei sicher aufbewahren und NICHT committen!")


def main():
    """Hauptfunktion: Führt die komplette Registrierung durch"""
    print()
    print("=" * 60)
    print("JTL-Wawi API App-Registrierung")
    print("=" * 60)
    print()

    # Schritt 1: Registrieren
    registration_id = register_app()
    if not registration_id:
        sys.exit(1)

    # Schritt 2 & 3: Polling
    result = poll_for_approval(registration_id)

    print()  # Neue Zeile nach Polling-Status

    if result.success:
        print()
        print("=" * 60)
        print("✓ REGISTRIERUNG ERFOLGREICH!")
        print("=" * 60)
        print()
        print(f"API-Key: {result.api_key}")
        print()
        print("WICHTIG: Dieser Key wird NUR EINMAL angezeigt!")
        print("         Bitte sicher speichern!")
        print()
        print(f"Gewährte Scopes: {result.granted_scopes}")
        print()

        # API-Key speichern
        save_api_key(result.api_key, result.granted_scopes)

        # Beispiel für Verwendung ausgeben
        print()
        print("Verwendung in Ihrem Code:")
        print("-" * 40)
        print(f'headers = {{')
        print(f'    "Authorization": "Wawi {result.api_key}",')
        print(f'    "api-version": "1.0",')
        print(f'    "X-AppID": "{APP_CONFIG["AppId"]}",')
        print(f'    "X-AppVersion": "{APP_CONFIG["Version"]}"')
        print(f'}}')
        print()

    else:
        print()
        print("=" * 60)
        print("✗ REGISTRIERUNG FEHLGESCHLAGEN")
        print("=" * 60)
        print()
        print(f"Fehler: {result.error}")
        print()
        sys.exit(1)


if __name__ == "__main__":
    main()
