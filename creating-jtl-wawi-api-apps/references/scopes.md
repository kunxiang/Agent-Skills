# JTL-Wawi API Scopes

## Übersicht

Scopes definieren die Berechtigungen einer App. Sie werden bei der Registrierung in `MandatoryApiScopes` (Pflicht) oder `OptionalApiScopes` (Optional) angegeben.

**Quelle**: Diese Liste wurde aus der offiziellen OpenAPI-Spezifikation (v1.2, JTL-Wawi 1.12.0) extrahiert.

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
| `mail...` | POST | Per E-Mail versenden |
| `pdf...` | GET | Als PDF abrufen |
| `print...` | POST | Drucken |
| `trigger...workflow` | POST | Workflow auslösen |

---

## Vollständige Scope-Liste (aus OpenAPI v1.2)

### Globale Scopes

| Scope | Beschreibung |
|-------|--------------|
| `all.read` | **Universeller Lesezugriff** auf alle Ressourcen |

### Buchhaltung (accountingdata)

| Scope | Beschreibung |
|-------|--------------|
| `accountingdata.queryaccountingdata` | Buchhaltungsdaten abfragen |
| `accountings.read` | Buchhaltung lesen |

### Verfügbarkeit (availability)

| Scope | Beschreibung |
|-------|--------------|
| `availability.queryavailabilities` | Verfügbarkeiten abfragen |

### Stornogründe (cancellationreason)

| Scope | Beschreibung |
|-------|--------------|
| `cancellationreason.querycancellationreasons` | Stornogründe abfragen |

### Kategorien (category)

| Scope | Beschreibung |
|-------|--------------|
| `category.addcategoryitems` | Artikel zu Kategorie hinzufügen |
| `category.createcategory` | Kategorie anlegen |
| `category.createcategorydescription` | Kategorie-Beschreibung anlegen |
| `category.deletecategorydescription` | Kategorie-Beschreibung löschen |
| `category.getcategory` | Kategorie abrufen |
| `category.querycategories` | Kategorien suchen |
| `category.querycategorydescriptions` | Kategorie-Beschreibungen suchen |
| `category.updatecategory` | Kategorie aktualisieren |
| `category.updatecategorydescription` | Kategorie-Beschreibung aktualisieren |

### Farbcodes (colorcode)

| Scope | Beschreibung |
|-------|--------------|
| `colorcode.querycolorcodes` | Farbcodes abfragen |

### Firmen (company)

| Scope | Beschreibung |
|-------|--------------|
| `company.querycompanies` | Firmen abfragen |

### Bedingungen (condition)

| Scope | Beschreibung |
|-------|--------------|
| `condition.queryconditions` | Bedingungen abfragen |

### Gutschriften (creditnote)

| Scope | Beschreibung |
|-------|--------------|
| `creditnote.mailcreditnote` | Gutschrift per E-Mail senden |
| `creditnote.pdfcreditnote` | Gutschrift als PDF |
| `creditnote.printcreditnote` | Gutschrift drucken |

### Kunden (customer) - 32 Scopes

| Scope | Beschreibung |
|-------|--------------|
| `customer.createcustomer` | Kunde anlegen |
| `customer.createcustomerbankaccount` | Bankdaten anlegen |
| `customer.createcustomercontact` | Kontakt anlegen |
| `customer.createcustomernote` | Notiz anlegen |
| `customer.deletecustomer` | Kunde löschen |
| `customer.deletecustomerbankaccount` | Bankdaten löschen |
| `customer.deletecustomercontact` | Kontakt löschen |
| `customer.deletecustomercustomfield` | Eigenes Feld löschen |
| `customer.deletecustomernote` | Notiz löschen |
| `customer.getcustomer` | Kunde abrufen |
| `customer.getcustomerbankaccount` | Bankdaten abrufen |
| `customer.getcustomercontact` | Kontakt abrufen |
| `customer.getcustomerlastchange` | Letzte Änderung abrufen |
| `customer.getcustomernote` | Notiz abrufen |
| `customer.querycustomerbankaccounts` | Bankdaten suchen |
| `customer.querycustomercontacts` | Kontakte suchen |
| `customer.querycustomercustomfields` | Eigene Felder suchen |
| `customer.querycustomercustomfieldvalues` | Eigene Feldwerte suchen |
| `customer.querycustomernotes` | Notizen suchen |
| `customer.querycustomers` | Kunden suchen |
| `customer.querycustomerworkflowevents` | Workflow-Events suchen |
| `customer.triggercustomerworkflow` | Workflow auslösen |
| `customer.triggercustomerworkflowevent` | Workflow-Event auslösen |
| `customer.updatecustomer` | Kunde aktualisieren |
| `customer.updatecustomerbankaccount` | Bankdaten aktualisieren |
| `customer.updatecustomercontact` | Kontakt aktualisieren |
| `customer.updatecustomercustomfield` | Eigenes Feld aktualisieren |
| `customer.updatecustomernote` | Notiz aktualisieren |
| `customers.read` | Kunden lesen (global) |
| `customers.write` | Kunden schreiben (global) |
| `cusomters.read` | Kunden lesen (Tippfehler in API!) |

### Kundenkategorien (customercategory)

| Scope | Beschreibung |
|-------|--------------|
| `customercategory.createcustomercategory` | Kundenkategorie anlegen |
| `customercategory.deletecustomercategory` | Kundenkategorie löschen |
| `customercategory.getcustomercategory` | Kundenkategorie abrufen |
| `customercategory.querycustomercategories` | Kundenkategorien suchen |
| `customercategory.updatecustomercategory` | Kundenkategorie aktualisieren |

### Kundengruppen (customergroup)

| Scope | Beschreibung |
|-------|--------------|
| `customergroup.createcustomergroup` | Kundengruppe anlegen |
| `customergroup.deletecustomergroup` | Kundengruppe löschen |
| `customergroup.getcustomergroup` | Kundengruppe abrufen |
| `customergroup.querycustomergroups` | Kundengruppen suchen |
| `customergroup.updatecustomergroup` | Kundengruppe aktualisieren |

### Lieferungen (deliveries)

| Scope | Beschreibung |
|-------|--------------|
| `deliveries.read` | Lieferungen lesen |
| `deliveries.write` | Lieferungen schreiben |

### Liefer-API (deliveryapi)

| Scope | Beschreibung |
|-------|--------------|
| `deliveryapi.cancelreservation` | Reservierung stornieren |
| `deliveryapi.deliversalesorder` | Auftrag liefern |
| `deliveryapi.queryreservations` | Reservierungen abfragen |
| `deliveryapi.reassignstock` | Bestand neu zuweisen |
| `deliveryapi.reservesalesorders` | Aufträge reservieren |

### Lieferscheine (deliverynote) - 13 Scopes

| Scope | Beschreibung |
|-------|--------------|
| `deliverynote.getdeliverynote` | Lieferschein abrufen |
| `deliverynote.getdeliverynotepackages` | Pakete abrufen |
| `deliverynote.maildeliverynote` | Per E-Mail senden |
| `deliverynote.package` | Paket erstellen |
| `deliverynote.patchpackagedata` | Paketdaten ändern |
| `deliverynote.pdfdeliverynote` | Als PDF abrufen |
| `deliverynote.postpackagedatafordeliverynote` | Paketdaten hinzufügen |
| `deliverynote.printdeliverynote` | Drucken |
| `deliverynote.querydeliverynotes` | Lieferscheine suchen |
| `deliverynote.triggerdeliverynoteworkflow` | Workflow auslösen |
| `deliverynotes.print` | Lieferscheine drucken (global) |
| `deliverynotes.read` | Lieferscheine lesen (global) |
| `deliverynotes.write` | Lieferscheine schreiben (global) |

### Erweiterbarkeit (extensibility)

| Scope | Beschreibung |
|-------|--------------|
| `extensibility.createextension` | Erweiterung anlegen |
| `extensibility.deleteextension` | Erweiterung löschen |
| `extensibility.getextension` | Erweiterung abrufen |
| `extensibility.getextensions` | Erweiterungen abrufen |
| `extensibility.integration` | Integration |
| `extensibility.putextensionmanifest` | Manifest aktualisieren |
| `extensibility.updateextension` | Erweiterung aktualisieren |

### Inventuren (inventories)

| Scope | Beschreibung |
|-------|--------------|
| `inventories.read` | Inventuren lesen |
| `inventories.write` | Inventuren schreiben |

### Rechnungen (invoice) - 14 Scopes

| Scope | Beschreibung |
|-------|--------------|
| `invoice.cancelinvoice` | Rechnung stornieren |
| `invoice.finalizeinvoice` | Rechnung abschließen |
| `invoice.getinvoice` | Rechnung abrufen |
| `invoice.mailinvoice` | Per E-Mail senden |
| `invoice.pdfinvoice` | Als PDF abrufen |
| `invoice.printinvoice` | Drucken |
| `invoice.queryinvoicecancellationreasons` | Stornogründe abfragen |
| `invoice.queryinvoicelineitems` | Positionen abfragen |
| `invoice.queryinvoices` | Rechnungen suchen |
| `invoice.queryinvoiceworkflowevents` | Workflow-Events abfragen |
| `invoice.triggerinvoiceworkflow` | Workflow auslösen |
| `invoice.triggerinvoiceworkflowevent` | Workflow-Event auslösen |
| `invoices.print` | Rechnungen drucken (global) |
| `invoices.read` | Rechnungen lesen (global) |
| `invoices.write` | Rechnungen schreiben (global) |

### Artikel (item) - 43 Scopes

| Scope | Beschreibung |
|-------|--------------|
| `item.assignchilditemtoparent` | Kind-Artikel zuweisen |
| `item.createitem` | Artikel anlegen |
| `item.createitemcustomerprice` | Kundenpreis anlegen |
| `item.createitemdescription` | Beschreibung anlegen |
| `item.createitemimage` | Bild anlegen |
| `item.createitemproperty` | Eigenschaft anlegen |
| `item.createitemsaleschannelprice` | Kanalpreis anlegen |
| `item.createitemsupplier` | Lieferant anlegen |
| `item.createitemvariation` | Variation anlegen |
| `item.createitemvariationvalue` | Variationswert anlegen |
| `item.deleteitemcustomerprice` | Kundenpreis löschen |
| `item.deleteitemcustomfield` | Eigenes Feld löschen |
| `item.deleteitemdescription` | Beschreibung löschen |
| `item.deleteitemimage` | Bild löschen |
| `item.deleteitemproperty` | Eigenschaft löschen |
| `item.deleteitemsaleschannelprice` | Kanalpreis löschen |
| `item.deleteitemsupplier` | Lieferant löschen |
| `item.deleteitemvariation` | Variation löschen |
| `item.deleteitemvariationvalue` | Variationswert löschen |
| `item.getitem` | Artikel abrufen |
| `item.queryitemcustomerprices` | Kundenpreise suchen |
| `item.queryitemcustomfields` | Eigene Felder suchen |
| `item.queryitemcustomfieldvalues` | Eigene Feldwerte suchen |
| `item.queryitemdescriptions` | Beschreibungen suchen |
| `item.queryitemimagedata` | Bilddaten abrufen |
| `item.queryitemimages` | Bilder suchen |
| `item.queryitemproperties` | Eigenschaften suchen |
| `item.queryitems` | Artikel suchen |
| `item.queryitemsaleschannelprice` | Kanalpreise suchen |
| `item.queryitemspecialprice` | Sonderpreise suchen |
| `item.queryitemsuppliers` | Lieferanten suchen |
| `item.queryitemvariations` | Variationen suchen |
| `item.queryitemvariationvalues` | Variationswerte suchen |
| `item.queryitemworkflowevents` | Workflow-Events suchen |
| `item.triggeritemworkflow` | Workflow auslösen |
| `item.triggeritemworkflowevent` | Workflow-Event auslösen |
| `item.updateitem` | Artikel aktualisieren |
| `item.updateitemcustomerprice` | Kundenpreis aktualisieren |
| `item.updateitemcustomfield` | Eigenes Feld aktualisieren |
| `item.updateitemdescription` | Beschreibung aktualisieren |
| `item.updateitemimage` | Bild aktualisieren |
| `item.updateitemsaleschannelprice` | Kanalpreis aktualisieren |
| `item.updateitemsaleschannels` | Kanäle aktualisieren |
| `item.updateitemspecialprice` | Sonderpreis aktualisieren |
| `item.updateitemsupplier` | Lieferant aktualisieren |
| `item.updateitemvariation` | Variation aktualisieren |
| `item.updateitemvariationvalue` | Variationswert aktualisieren |
| `items.read` | Artikel lesen (global) |
| `items.write` | Artikel schreiben (global) |

### Hersteller (manufacturer)

| Scope | Beschreibung |
|-------|--------------|
| `manufacturer.querymanufacturers` | Hersteller abfragen |

### Nummernkreise (numberranges)

| Scope | Beschreibung |
|-------|--------------|
| `numberranges.createnumberrange` | Nummernkreis anlegen |
| `numberranges.deletenumberrange` | Nummernkreis löschen |
| `numberranges.getnumberrange` | Nummernkreis abrufen |
| `numberranges.getnumberranges` | Nummernkreise abrufen |
| `numberranges.numberrangeincrement` | Nummernkreis erhöhen |
| `numberranges.numberrangepreview` | Vorschau |
| `numberranges.updatenumberrange` | Nummernkreis aktualisieren |

### Angebote (offer)

| Scope | Beschreibung |
|-------|--------------|
| `offer.mailoffer` | Per E-Mail senden |
| `offer.pdfoffer` | Als PDF abrufen |
| `offer.printoffer` | Drucken |
| `offers.print` | Angebote drucken (global) |
| `offers.read` | Angebote lesen (global) |

### Halt-Gründe (onholdreason)

| Scope | Beschreibung |
|-------|--------------|
| `onholdreason.queryonholdreasons` | Halt-Gründe abfragen |

### Bestellungen (orders)

| Scope | Beschreibung |
|-------|--------------|
| `orders.read` | Bestellungen lesen |

### Zahlungsarten (paymentmethod)

| Scope | Beschreibung |
|-------|--------------|
| `paymentmethod.querypaymentmethods` | Zahlungsarten abfragen |

### Picklisten (picklists)

| Scope | Beschreibung |
|-------|--------------|
| `picklists.read` | Picklisten lesen |
| `picklists.write` | Picklisten schreiben |

### Drucker (printers)

| Scope | Beschreibung |
|-------|--------------|
| `printers.installedprinters` | Installierte Drucker abfragen |

### Warengruppen (productgroup)

| Scope | Beschreibung |
|-------|--------------|
| `productgroup.queryproductgroups` | Warengruppen abfragen |

### Eigenschaften (property)

| Scope | Beschreibung |
|-------|--------------|
| `property.createproperty` | Eigenschaft anlegen |
| `property.createpropertygroup` | Eigenschaftsgruppe anlegen |
| `property.createpropertyvalue` | Eigenschaftswert anlegen |
| `property.createpropertyvaluedescription` | Wert-Beschreibung anlegen |
| `property.deletepropertyvalue` | Eigenschaftswert löschen |
| `property.deletepropertyvaluedescription` | Wert-Beschreibung löschen |
| `property.queryproperties` | Eigenschaften suchen |
| `property.querypropertygroups` | Eigenschaftsgruppen suchen |
| `property.querypropertyvaluedescriptions` | Wert-Beschreibungen suchen |
| `property.querypropertyvalues` | Eigenschaftswerte suchen |
| `property.updatepropertyvalue` | Eigenschaftswert aktualisieren |
| `property.updatepropertyvaluedescription` | Wert-Beschreibung aktualisieren |

### Erstattung (refund)

| Scope | Beschreibung |
|-------|--------------|
| `refund.queryrefundcancellationreasons` | Stornogründe abfragen |

### Verantwortliche Person (responsibleperson)

| Scope | Beschreibung |
|-------|--------------|
| `responsibleperson.queryresponsiblepersons` | Verantwortliche Personen abfragen |

### Retouren (return)

| Scope | Beschreibung |
|-------|--------------|
| `return.createreturn` | Retoure anlegen |
| `return.getreturn` | Retoure abrufen |
| `return.queryreturnlineitems` | Positionen abfragen |
| `return.queryreturnpackages` | Pakete abfragen |
| `return.queryreturns` | Retouren suchen |
| `returns.read` | Retouren lesen (global) |
| `returns.write` | Retouren schreiben (global) |

### Retourengründe (returnreason)

| Scope | Beschreibung |
|-------|--------------|
| `returnreason.queryreturnreasons` | Retourengründe abfragen |

### Retourenstatus (returnstate)

| Scope | Beschreibung |
|-------|--------------|
| `returnstate.queryreturnstates` | Retourenstatus abfragen |

### Verkaufskanal (saleschannel)

| Scope | Beschreibung |
|-------|--------------|
| `saleschannel.getsaleschannels` | Verkaufskanäle abrufen |
| `saleschannels.read` | Verkaufskanäle lesen (global) |

### Rechnungskorrekturen (salesinvoicecorrection)

| Scope | Beschreibung |
|-------|--------------|
| `salesinvoicecorrection.finalizesalesinvoicecorrection` | Korrektur abschließen |
| `salesinvoicecorrection.querysalesinvoicecorrectioncancellationreasons` | Stornogründe abfragen |
| `salesinvoicecorrections.print` | Korrekturen drucken (global) |
| `salesinvoicecorrections.read` | Korrekturen lesen (global) |
| `salesinvoicecorrections.write` | Korrekturen schreiben (global) |

### Aufträge (salesorder) - 34 Scopes

| Scope | Beschreibung |
|-------|--------------|
| `salesorder.cancelsalesorder` | Auftrag stornieren |
| `salesorder.createsalesorder` | Auftrag anlegen |
| `salesorder.createsalesorderfile` | Datei anlegen |
| `salesorder.createsalesorderlineitem` | Position anlegen |
| `salesorder.createsalesorderlineitemfile` | Positionsdatei anlegen |
| `salesorder.createsalesordernote` | Notiz anlegen |
| `salesorder.deletesalesordercustomfield` | Eigenes Feld löschen |
| `salesorder.deletesalesorderfile` | Datei löschen |
| `salesorder.deletesalesorderlineitem` | Position löschen |
| `salesorder.deletesalesorderlineitemfile` | Positionsdatei löschen |
| `salesorder.deletesalesordernote` | Notiz löschen |
| `salesorder.getsalesorder` | Auftrag abrufen |
| `salesorder.mailsalesorder` | Per E-Mail senden |
| `salesorder.newinvoice` | Neue Rechnung erstellen |
| `salesorder.pdfsalesorder` | Als PDF abrufen |
| `salesorder.printsalesorder` | Drucken |
| `salesorder.querysalesordercancellationreasons` | Stornogründe abfragen |
| `salesorder.querysalesordercustomfields` | Eigene Felder suchen |
| `salesorder.querysalesordercustomfieldvalues` | Eigene Feldwerte suchen |
| `salesorder.querysalesorderfiledata` | Dateidaten abrufen |
| `salesorder.querysalesorderfiles` | Dateien suchen |
| `salesorder.querysalesorderlineitemfiledata` | Positionsdateidaten abrufen |
| `salesorder.querysalesorderlineitemfiles` | Positionsdateien suchen |
| `salesorder.querysalesorderlineitems` | Positionen suchen |
| `salesorder.querysalesordernotes` | Notizen suchen |
| `salesorder.querysalesorders` | Aufträge suchen |
| `salesorder.querysalesorderworkflowevents` | Workflow-Events suchen |
| `salesorder.triggersalesorderworkflow` | Workflow auslösen |
| `salesorder.triggersalesorderworkflowevent` | Workflow-Event auslösen |
| `salesorder.undosalesordercancellation` | Stornierung rückgängig machen |
| `salesorder.updatesalesorder` | Auftrag aktualisieren |
| `salesorder.updatesalesordercustomfield` | Eigenes Feld aktualisieren |
| `salesorder.updatesalesorderfile` | Datei aktualisieren |
| `salesorder.updatesalesorderlineitem` | Position aktualisieren |
| `salesorder.updatesalesorderlineitemfile` | Positionsdatei aktualisieren |
| `salesorder.updatesalesordernote` | Notiz aktualisieren |
| `salesorders.print` | Aufträge drucken (global) |
| `salesorders.read` | Aufträge lesen (global) |
| `salesorders.write` | Aufträge schreiben (global) |

### Versandklassen (shippingclass)

| Scope | Beschreibung |
|-------|--------------|
| `shippingclass.queryshippingclasses` | Versandklassen abfragen |

### Versandarten (shippingmethod)

| Scope | Beschreibung |
|-------|--------------|
| `shippingmethod.queryshippingmethods` | Versandarten abfragen |

### Lagerbestand (stock)

| Scope | Beschreibung |
|-------|--------------|
| `stock.queryserialnumberperwarehouse` | Seriennummern pro Lager abfragen |
| `stock.querystockchanges` | Bestandsänderungen abfragen |
| `stock.querystocksperitem` | Bestände pro Artikel abfragen |
| `stock.stockadjustment` | Bestand anpassen |

### Lieferanten (supplier)

| Scope | Beschreibung |
|-------|--------------|
| `supplier.querysuppliers` | Lieferanten abfragen |
| `suppliers.read` | Lieferanten lesen (global) |

### System

| Scope | Beschreibung |
|-------|--------------|
| `system.config.read` | Systemkonfiguration lesen |
| `system.config.write` | Systemkonfiguration schreiben |
| `system.read` | System lesen |
| `system.worker.read` | Worker lesen |
| `system.worker.write` | Worker schreiben |

### Steuerklassen (taxclass)

| Scope | Beschreibung |
|-------|--------------|
| `taxclass.querytaxclasses` | Steuerklassen abfragen |
| `taxes.read` | Steuern lesen |

### Transaktionsstatus (transactionstatus)

| Scope | Beschreibung |
|-------|--------------|
| `transactionstatus.querytransactionstatus` | Transaktionsstatus abfragen |

### Lager (warehouse)

| Scope | Beschreibung |
|-------|--------------|
| `warehouse.querystoragelocations` | Lagerplätze abfragen |
| `warehouse.querystoragelocationtype` | Lagerplatztypen abfragen |
| `warehouse.querywarehouses` | Lager abfragen |
| `warehouse.querywarehousetypes` | Lagertypen abfragen |
| `warehouse.read` | Lager lesen (global) |

### WMS (Lagerverwaltung)

| Scope | Beschreibung |
|-------|--------------|
| `wms.changereservation` | Reservierung ändern |
| `wms.createpicklist` | Pickliste erstellen |
| `wms.deletepicklistposition` | Picklisten-Position löschen |
| `wms.pickposition` | Position picken |
| `wms.querypicklist` | Pickliste abfragen |
| `wms.querypicklistposition` | Picklisten-Position abfragen |
| `wms.querypicklisttemplate` | Picklisten-Vorlage abfragen |

### Worker (Synchronisation)

| Scope | Beschreibung |
|-------|--------------|
| `worker.configuresync` | Synchronisation konfigurieren |
| `worker.getworkerstatus` | Worker-Status abrufen |
| `worker.getworkersyncs` | Worker-Syncs abrufen |
| `worker.synccontrol` | Sync-Steuerung |

---

## Beispiel-Konfigurationen

### Minimale Lese-App
```json
{
  "MandatoryApiScopes": ["all.read"]
}
```

### Kunden-Management
```json
{
  "MandatoryApiScopes": [
    "all.read",
    "customer.createcustomer",
    "customer.updatecustomer",
    "customer.deletecustomer"
  ]
}
```

### Auftragsverarbeitung
```json
{
  "MandatoryApiScopes": [
    "all.read",
    "salesorder.createsalesorder",
    "salesorder.updatesalesorder",
    "invoice.finalizeinvoice",
    "deliverynote.package"
  ]
}
```

### Lagerverwaltung
```json
{
  "MandatoryApiScopes": [
    "all.read",
    "stock.stockadjustment",
    "stock.querystockchanges",
    "warehouse.querywarehouses",
    "wms.createpicklist"
  ]
}
```

### Vollständiger Zugriff (nicht empfohlen!)
```json
{
  "MandatoryApiScopes": [
    "all.read",
    "customers.write",
    "items.write",
    "salesorders.write",
    "invoices.write",
    "deliverynotes.write"
  ]
}
```

---

## ⚠️ Häufige Fehler bei Scopes

| Fehler | Ursache | Lösung |
|--------|---------|--------|
| **403 Forbidden** | Scope fehlt | Benötigten Scope bei Registrierung hinzufügen |
| **403 Forbidden** | Falsche Schreibweise | Kleinschreibung verwenden |
| **Registrierung schlägt fehl** | Zu viele Scopes | Mit `["all.read"]` starten |
| **GET funktioniert, POST nicht** | Nur `all.read` | Spezifischen Schreib-Scope hinzufügen |
| **Scope nicht erkannt** | Scope existiert nicht | In Swagger "AUTHORIZATIONS" prüfen |

## MandatoryApiScopes vs. OptionalApiScopes

| Typ | Wann verwenden? | Verhalten |
|-----|-----------------|-----------|
| **MandatoryApiScopes** | Für Kernfunktionen | App startet nur mit diesen Scopes |
| **OptionalApiScopes** | Für optionale Features | Benutzer kann in JTL-Wawi ablehnen |

## Best Practices

1. **Minimale Berechtigungen**: Nur benötigte Scopes anfordern
2. **all.read nutzen**: Für Lesezugriff ausreichend
3. **Schrittweise erweitern**: Bei Problemen mit weniger Scopes starten
4. **Dokumentation prüfen**: Swagger zeigt benötigte Scopes pro Endpoint
5. **Nachträgliche Änderung**: Erfordert neue App-Registrierung!
