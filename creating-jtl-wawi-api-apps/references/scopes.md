# JTL-Wawi API Scopes

## Übersicht

Scopes definieren die Berechtigungen einer App. Sie werden bei der Registrierung in `MandatoryApiScopes` (Pflicht) oder `OptionalApiScopes` (Optional) angegeben.

## ⚠️ KRITISCHE HINWEISE (aus Community-Erfahrungen)

### 1. Wo findet man die Scopes?

> Forum-Zitat: "Bei jedem Endpoint in der Dokumentation kommt direkt oben nach der Beschreibung ein Punkt 'AUTHORIZATIONS:', den man aufklappen muss."

**Swagger UI**: `http://localhost:5883/swagger` → Endpoint auswählen → "AUTHORIZATIONS" aufklappen

### 2. Kein `all.write` oder `all.create`!

```
✓ all.read          → Existiert (Lesezugriff auf alles)
✗ all.write         → Existiert NICHT!
✗ all.create        → Existiert NICHT!
```

> Forum: "Für die Leseberechtigung existiert ein 'all.read' - ein 'all.write' oder 'all.create' ist jedoch aktuell nicht vorhanden."

**Konsequenz**: Für jede Schreiboperation muss der spezifische Scope angegeben werden!

### 3. Zu viele Scopes können Registrierung blockieren!

> Forum-Erfahrung: "Bei manchen Nutzern hatte die Registrierung wegen zu vieler Scopes nicht funktioniert."

**Empfehlung**:
1. Mit `["all.read"]` starten
2. Schreibscopes nach Bedarf hinzufügen
3. Bei Problemen: Scopes reduzieren, neu registrieren

### 4. Groß-/Kleinschreibung beachten!

Scopes sind **case-sensitive**:
```
✗ Customer.CreateCustomer    ❌
✗ CUSTOMER.CREATECUSTOMER    ❌
✓ customer.createcustomer    ✓
```

### 5. Scopes aus swagger.json extrahieren

Für eine vollständige Liste aller Scopes:
```bash
# 1. Swagger JSON herunterladen
curl http://localhost:5883/swagger/v1/swagger.json -o swagger.json

# 2. Scopes extrahieren (mit jq)
jq '.components.securitySchemes.oauth2.flows.clientCredentials.scopes | keys' swagger.json
```

## Scope-Format

```
<bereich>.<aktion>
```

Beispiel: `customer.createcustomer` = Kunden anlegen

### Aktions-Suffixe

| Suffix | HTTP-Methode | Bedeutung |
|--------|--------------|-----------|
| `get...` | GET | Einzelnen Datensatz abrufen |
| `query...` | POST | Mehrere Datensätze suchen/filtern |
| `create...` | POST | Neuen Datensatz anlegen |
| `update...` | PUT | Datensatz aktualisieren |
| `delete...` | DELETE | Datensatz löschen |

## Globale Scopes

| Scope | Beschreibung |
|-------|--------------|
| `all.read` | Lesezugriff auf alle Ressourcen |

## Kunden (customer)

| Scope | Beschreibung |
|-------|--------------|
| `customer.getcustomer` | Kunde abrufen |
| `customer.createcustomer` | Kunde anlegen |
| `customer.updatecustomer` | Kunde aktualisieren |
| `customer.deletecustomer` | Kunde löschen |
| `customer.querycustomers` | Kunden suchen |
| `customer.getcustomercontact` | Kontaktdaten abrufen |
| `customer.createcustomercontact` | Kontaktdaten anlegen |
| `customer.deletecustomercontact` | Kontaktdaten löschen |
| `customer.getcustomerbankaccount` | Bankdaten abrufen |
| `customer.createcustomerbankaccount` | Bankdaten anlegen |
| `customer.deletecustomerbankaccount` | Bankdaten löschen |
| `customer.getcustomernote` | Notizen abrufen |
| `customer.createcustomernote` | Notizen anlegen |
| `customer.deletecustomernote` | Notizen löschen |
| `customer.querycustomerbankaccounts` | Bankdaten suchen |
| `customer.deletecustomercustomfield` | Eigene Felder löschen |

## Aufträge (salesorder)

| Scope | Beschreibung |
|-------|--------------|
| `salesorder.getsalesorder` | Auftrag abrufen |
| `salesorder.createsalesorder` | Auftrag anlegen |
| `salesorder.updatesalesorder` | Auftrag aktualisieren |
| `salesorder.deletesalesorder` | Auftrag löschen |
| `salesorder.querysalesorders` | Aufträge suchen |

## Artikel (article)

| Scope | Beschreibung |
|-------|--------------|
| `article.getarticle` | Artikel abrufen |
| `article.createarticle` | Artikel anlegen |
| `article.updatearticle` | Artikel aktualisieren |
| `article.deletearticle` | Artikel löschen |
| `article.queryarticles` | Artikel suchen |

## Lagerbestand (stock)

| Scope | Beschreibung |
|-------|--------------|
| `stock.querystock` | Bestand abfragen |
| `stock.stockadjustment` | Bestand anpassen |

## Rechnungen (invoice)

| Scope | Beschreibung |
|-------|--------------|
| `invoice.getinvoice` | Rechnung abrufen |
| `invoice.createinvoice` | Rechnung erstellen |
| `invoice.queryinvoices` | Rechnungen suchen |

## Lieferscheine (deliverynote)

| Scope | Beschreibung |
|-------|--------------|
| `deliverynote.getdeliverynote` | Lieferschein abrufen |
| `deliverynote.createdeliverynote` | Lieferschein erstellen |
| `deliverynote.querydeliverynotes` | Lieferscheine suchen |

## Kategorien (category)

| Scope | Beschreibung |
|-------|--------------|
| `category.getcategory` | Kategorie abrufen |
| `category.createcategory` | Kategorie anlegen |
| `category.updatecategory` | Kategorie aktualisieren |
| `category.querycategories` | Kategorien suchen |
| `category.addcategoryitems` | Artikel zu Kategorie hinzufügen |
| `category.createcategorydescription` | Beschreibung anlegen |
| `category.updatecategorydescription` | Beschreibung aktualisieren |
| `category.deletecategorydescription` | Beschreibung löschen |
| `category.querycategorydescriptions` | Beschreibungen suchen |

## Firmen (company)

| Scope | Beschreibung |
|-------|--------------|
| `company.querycompanies` | Firmen abfragen |

## Kundengruppen (customergroup)

| Scope | Beschreibung |
|-------|--------------|
| `customergroup.querycustomergroups` | Kundengruppen abfragen |

## Kundenkategorien (customercategory)

| Scope | Beschreibung |
|-------|--------------|
| `customercategory.querycustomercategories` | Kundenkategorien abfragen |

## Buchhaltungsdaten (accountingdata)

| Scope | Beschreibung |
|-------|--------------|
| `accountingdata.queryaccountingdata` | Buchhaltungsdaten abfragen |

## Verfügbarkeit (availability)

| Scope | Beschreibung |
|-------|--------------|
| `availability.queryavailabilities` | Verfügbarkeiten abfragen |

## Stornogründe (cancellationreason)

| Scope | Beschreibung |
|-------|--------------|
| `cancellationreason.querycancellationreasons` | Stornogründe abfragen |

## Farbcodes (colorcode)

| Scope | Beschreibung |
|-------|--------------|
| `colorcode.querycolorcodes` | Farbcodes abfragen |

## Bedingungen (condition)

| Scope | Beschreibung |
|-------|--------------|
| `condition.queryconditions` | Bedingungen abfragen |

## Gutschriften (creditnote)

| Scope | Beschreibung |
|-------|--------------|
| `creditnote.getcreditnote` | Gutschrift abrufen |
| `creditnote.createcreditnote` | Gutschrift erstellen |
| `creditnote.querycreditnotes` | Gutschriften suchen |

## Angebote (offer)

| Scope | Beschreibung |
|-------|--------------|
| `offer.getoffer` | Angebot abrufen |
| `offer.createoffer` | Angebot erstellen |
| `offer.queryoffers` | Angebote suchen |

## Halt-Gründe (onholdreason)

| Scope | Beschreibung |
|-------|--------------|
| `onholdreason.queryonholdreasons` | Halt-Gründe abfragen |

## Zahlungsarten (paymentmethod)

| Scope | Beschreibung |
|-------|--------------|
| `paymentmethod.querypaymentmethods` | Zahlungsarten abfragen |

## Drucker (printer)

| Scope | Beschreibung |
|-------|--------------|
| `printer.queryprinters` | Drucker abfragen |

## Eigenschaften (property)

| Scope | Beschreibung |
|-------|--------------|
| `property.queryproperties` | Eigenschaften abfragen |

## Retouren (return)

| Scope | Beschreibung |
|-------|--------------|
| `return.getreturn` | Retoure abrufen |
| `return.createreturn` | Retoure erstellen |
| `return.queryreturns` | Retouren suchen |

## Retourengrund (returnreason)

| Scope | Beschreibung |
|-------|--------------|
| `returnreason.queryreturnreasons` | Retourengründe abfragen |

## Retourenstatus (returnstate)

| Scope | Beschreibung |
|-------|--------------|
| `returnstate.queryreturnstates` | Retourenstatus abfragen |

## Verkaufskanal (saleschannel)

| Scope | Beschreibung |
|-------|--------------|
| `saleschannel.querysaleschannels` | Verkaufskanäle abfragen |

## Stornorechnung (salesinvoicecorrection)

| Scope | Beschreibung |
|-------|--------------|
| `salesinvoicecorrection.getsalesinvoicecorrection` | Stornorechnung abrufen |
| `salesinvoicecorrection.querysalesinvoicecorrections` | Stornorechnungen suchen |

## Versandarten (shippingmethod)

| Scope | Beschreibung |
|-------|--------------|
| `shippingmethod.queryshippingmethods` | Versandarten abfragen |

## Lager (warehouse)

| Scope | Beschreibung |
|-------|--------------|
| `warehouse.querywarehouses` | Lager abfragen |

## Worker (Synchronisation)

| Scope | Beschreibung |
|-------|--------------|
| `worker.configuresync` | Synchronisation konfigurieren |

## Beispiel: Minimale Scopes

Für eine Lese-App:
```json
{
  "MandatoryApiScopes": ["all.read"]
}
```

## Beispiel: Kunden-Management

```json
{
  "MandatoryApiScopes": [
    "customer.getcustomer",
    "customer.createcustomer",
    "customer.updatecustomer",
    "customer.querycustomers"
  ]
}
```

## Beispiel: Auftragsverarbeitung

```json
{
  "MandatoryApiScopes": [
    "all.read",
    "salesorder.createsalesorder",
    "salesorder.updatesalesorder",
    "invoice.createinvoice",
    "deliverynote.createdeliverynote"
  ]
}
```

## Beispiel: Lagerverwaltung

```json
{
  "MandatoryApiScopes": [
    "stock.querystock",
    "stock.stockadjustment",
    "article.getarticle",
    "warehouse.querywarehouses"
  ]
}
```

## Best Practices

1. **Minimale Berechtigungen**: Nur benötigte Scopes anfordern
2. **all.read nutzen**: Für reine Lese-Apps ausreichend
3. **Optionale Scopes**: Für Funktionen, die nicht immer benötigt werden
4. **Dokumentation prüfen**: Scope-Anforderungen je Endpoint in Swagger
5. **Nachträgliche Änderung**: Erfordert neue App-Registrierung

## ⚠️ Häufige Fehler bei Scopes

| Fehler | Ursache | Lösung |
|--------|---------|--------|
| **403 Forbidden** | Scope fehlt | Benötigten Scope bei Registrierung hinzufügen |
| **403 Forbidden** | Falsche Schreibweise | Kleinschreibung verwenden: `customer.createcustomer` |
| **Registrierung schlägt fehl** | Zu viele Scopes | Mit `["all.read"]` starten, schrittweise erweitern |
| **GET funktioniert, POST nicht** | Nur `all.read` registriert | Spezifischen Schreib-Scope hinzufügen |
| **Scope nicht erkannt** | Scope existiert nicht | In Swagger "AUTHORIZATIONS" prüfen |

## MandatoryApiScopes vs. OptionalApiScopes

| Typ | Wann verwenden? | Verhalten |
|-----|-----------------|-----------|
| **MandatoryApiScopes** | Für Kernfunktionen | App startet nur mit diesen Scopes |
| **OptionalApiScopes** | Für optionale Features | Benutzer kann in JTL-Wawi ablehnen |

**Beispiel**:
```json
{
  "MandatoryApiScopes": ["all.read", "customer.createcustomer"],
  "OptionalApiScopes": ["customer.deletecustomer"]
}
```

→ Benutzer **muss** Lesen und Kunden-Anlegen erlauben
→ Benutzer **kann** Kunden-Löschen verweigern

## Spezielle Scopes

### Application.RunAs

Für Aktionen im Namen eines anderen Benutzers:
```json
{
  "MandatoryApiScopes": ["all.read", "Application.RunAs"]
}
```

Header bei Anfrage:
```
X-RunAs: BenutzerName
```

## Vollständige Scope-Liste abrufen

### Option 1: Swagger UI
1. REST-Server starten
2. Browser: `http://localhost:5883/swagger`
3. Bei jedem Endpoint "AUTHORIZATIONS" aufklappen

### Option 2: swagger.json parsen
```python
import requests
import json

# Swagger JSON abrufen
resp = requests.get("http://localhost:5883/swagger/v1/swagger.json")
data = resp.json()

# Scopes extrahieren
scopes = data.get("components", {}).get("securitySchemes", {}).get("oauth2", {}).get("flows", {}).get("clientCredentials", {}).get("scopes", {})

for scope, description in scopes.items():
    print(f"{scope}: {description}")
```

### Option 3: Postman Import
1. Swagger JSON herunterladen
2. In Postman importieren
3. Collection zeigt alle Endpoints mit Scopes
