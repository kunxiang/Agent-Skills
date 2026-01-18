#!/bin/bash
#
# JTL-Wawi API App-Registrierung (Bash)
#
# Dieses Skript führt Schritt 1 der Registrierung durch
# und gibt Anweisungen für die weiteren Schritte.
#
# Verwendung:
#   chmod +x register_app.sh
#   ./register_app.sh
#
# Voraussetzungen:
#   - curl
#   - jq (für JSON-Parsing)
#

# ===== KONFIGURATION (ANPASSEN!) =====

BASE_URL="${JTL_API_BASE_URL:-http://localhost:5883}"
CHALLENGE_CODE="${JTL_CHALLENGE_CODE:-mein-geheimer-code}"

# App-Konfiguration
APP_ID="meine-firma/meine-app/v1"
DISPLAY_NAME="Meine App"
DESCRIPTION="Beschreibung meiner App-Funktionen"
VERSION="1.0.0"
PROVIDER_NAME="Meine Firma GmbH"
PROVIDER_WEBSITE="https://www.meine-firma.de"
SCOPES='["all.read", "customer.createcustomer", "salesorder.createsalesorder"]'
REGISTRATION_TYPE=0

# ===== ENDE KONFIGURATION =====

set -e

echo ""
echo "=============================================="
echo "JTL-Wawi API App-Registrierung"
echo "=============================================="
echo ""
echo "Base URL: $BASE_URL"
echo "App-ID: $APP_ID"
echo ""

# Prüfe ob jq installiert ist
if ! command -v jq &> /dev/null; then
    echo "WARNUNG: jq ist nicht installiert."
    echo "         JSON-Ausgabe wird nicht formatiert."
    USE_JQ=false
else
    USE_JQ=true
fi

# Erstelle Request Body
REQUEST_BODY=$(cat <<EOF
{
  "AppId": "$APP_ID",
  "DisplayName": "$DISPLAY_NAME",
  "Description": "$DESCRIPTION",
  "Version": "$VERSION",
  "ProviderName": "$PROVIDER_NAME",
  "ProviderWebsite": "$PROVIDER_WEBSITE",
  "MandatoryApiScopes": $SCOPES,
  "OptionalApiScopes": [],
  "RegistrationType": $REGISTRATION_TYPE,
  "AppIcon": ""
}
EOF
)

echo "Sende Registrierungsanfrage..."
echo ""

# Schritt 1: Registrierung
RESPONSE=$(curl -s -w "\n%{http_code}" \
    -X POST "$BASE_URL/authentication" \
    -H "Content-Type: application/json" \
    -H "api-version: 1.0" \
    -H "X-ChallengeCode: $CHALLENGE_CODE" \
    -d "$REQUEST_BODY")

# Extrahiere HTTP-Status und Body
HTTP_STATUS=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_STATUS" = "202" ]; then
    echo "✓ Registrierung erfolgreich eingereicht!"
    echo ""

    if $USE_JQ; then
        REGISTRATION_ID=$(echo "$BODY" | jq -r '.RequestStatusInfo.RegistrationRequestId')
        echo "Registration-ID: $REGISTRATION_ID"
    else
        echo "Response:"
        echo "$BODY"
        echo ""
        echo "Bitte extrahieren Sie die RegistrationRequestId aus der Response."
    fi

    echo ""
    echo "=============================================="
    echo "NÄCHSTE SCHRITTE:"
    echo "=============================================="
    echo ""
    echo "1. Öffnen Sie JTL-Wawi (neue Oberfläche)"
    echo "2. Navigieren Sie zu: Admin → App-Registrierung"
    echo "3. Genehmigen Sie die App '$DISPLAY_NAME'"
    echo ""
    echo "4. Führen Sie dann folgenden Befehl aus, um den API-Key abzurufen:"
    echo ""

    if $USE_JQ; then
        echo "   curl -s '$BASE_URL/authentication/$REGISTRATION_ID' \\"
        echo "        -H 'api-version: 1.0' \\"
        echo "        -H 'X-ChallengeCode: $CHALLENGE_CODE' | jq"
    else
        echo "   curl -s '$BASE_URL/authentication/{REGISTRATION_ID}' \\"
        echo "        -H 'api-version: 1.0' \\"
        echo "        -H 'X-ChallengeCode: $CHALLENGE_CODE'"
    fi

    echo ""
    echo "=============================================="
    echo "WICHTIG: Der API-Key wird nur EINMAL angezeigt!"
    echo "         Bitte sicher speichern!"
    echo "=============================================="

else
    echo "✗ Fehler bei der Registrierung"
    echo "  HTTP-Status: $HTTP_STATUS"
    echo ""

    if $USE_JQ && [ -n "$BODY" ]; then
        echo "  Response:"
        echo "$BODY" | jq .
    else
        echo "  Response: $BODY"
    fi

    echo ""
    echo "Mögliche Ursachen:"
    echo "  - REST-Server nicht gestartet"
    echo "  - Falsche Base-URL"
    echo "  - Ungültige App-Konfiguration"

    exit 1
fi

echo ""

# Optionales Polling-Skript erstellen
if $USE_JQ && [ -n "$REGISTRATION_ID" ]; then
    cat > poll_status.sh <<POLL_SCRIPT
#!/bin/bash
# Auto-generiertes Polling-Skript
# Führt Polling durch bis API-Key verfügbar

REGISTRATION_ID="$REGISTRATION_ID"
BASE_URL="$BASE_URL"
CHALLENGE_CODE="$CHALLENGE_CODE"

echo "Warte auf Genehmigung..."
echo "(Drücken Sie Ctrl+C zum Abbrechen)"
echo ""

while true; do
    RESPONSE=\$(curl -s "\$BASE_URL/authentication/\$REGISTRATION_ID" \\
        -H "api-version: 1.0" \\
        -H "X-ChallengeCode: \$CHALLENGE_CODE")

    STATUS=\$(echo "\$RESPONSE" | jq -r '.RequestStatusInfo.Status')

    if [ "\$STATUS" = "1" ]; then
        API_KEY=\$(echo "\$RESPONSE" | jq -r '.Token.ApiKey')
        SCOPES=\$(echo "\$RESPONSE" | jq -r '.GrantedScopes')

        echo ""
        echo "=============================================="
        echo "✓ REGISTRIERUNG ERFOLGREICH!"
        echo "=============================================="
        echo ""
        echo "API-Key: \$API_KEY"
        echo "Scopes:  \$SCOPES"
        echo ""
        echo "WICHTIG: Dieser Key wird NUR EINMAL angezeigt!"
        echo ""

        # In Datei speichern
        echo "# JTL-Wawi API Credentials" > .env.jtl
        echo "JTL_API_KEY=\$API_KEY" >> .env.jtl
        echo "JTL_API_BASE_URL=\$BASE_URL" >> .env.jtl
        echo ""
        echo "Gespeichert in: .env.jtl"

        exit 0
    elif [ "\$STATUS" = "2" ]; then
        echo ""
        echo "✗ App wurde in JTL-Wawi abgelehnt."
        exit 1
    else
        echo -n "."
        sleep 5
    fi
done
POLL_SCRIPT

    chmod +x poll_status.sh
    echo "Polling-Skript erstellt: poll_status.sh"
    echo "Führen Sie './poll_status.sh' aus, um automatisch auf den API-Key zu warten."
fi
