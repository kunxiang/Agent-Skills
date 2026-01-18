# JTL-Wawi API Scopes

## Übersicht

Scopes definieren die Berechtigungen einer App. Sie werden bei der Registrierung in `MandatoryApiScopes` (Pflicht) oder `OptionalApiScopes` (Optional) angegeben.

## Wichtiger Hinweis

Der Scope `all.read` gewährt Lesezugriff auf alle Ressourcen. Für Schreiboperationen sind spezifische Scopes erforderlich.

## Scope-Format

```
<bereich>.<aktion>
```

Beispiel: `customer.createcustomer` = Kunden anlegen

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
