# JTL-Wawi API Vollständige Endpoint-Referenz

**Quelle**: OpenAPI v1.2 (JTL-Wawi 1.12.0)

**Base URL**: `http://<HOST>:<PORT>/api/<MANDANT>`

## Wichtige Hinweise

- Alle Endpoints benötigen den `Authorization: Wawi {API-KEY}` Header (außer /authentication)
- `api-version: 1.0` Header immer angeben
- Bei POST/PATCH: `Content-Type: application/json` setzen

---

## Configuration

| Methode | Endpoint | Beschreibung |
|---------|----------|--------------|
| `GET` | `/configuration/numberRanges` | Get Number Ranges |
| `DELETE` | `/configuration/numberRanges/{numberRangeId}` | Delete Number Range |
| `GET` | `/configuration/numberRanges/{numberRangeId}` | Get Number Range |
| `POST` | `/configuration/numberRanges/{numberRangeId}` | Create Number Range |
| `PUT` | `/configuration/numberRanges/{numberRangeId}` | Update Number Range |
| `POST` | `/configuration/numberRanges/{numberRangeId}/increment` | Number Range Increment |
| `GET` | `/configuration/numberRanges/{numberRangeId}/preview` | Number Range Preview |

## Extensibility

| Methode | Endpoint | Beschreibung |
|---------|----------|--------------|
| `GET` | `/extensions` | Get Extensions |
| `POST` | `/extensions` | Create Extension |
| `DELETE` | `/extensions/{extensionId}` | Delete Extension |
| `GET` | `/extensions/{extensionId}` | Get Extension |
| `PATCH` | `/extensions/{extensionId}` | Update Extension |
| `PUT` | `/extensions/{extensionId}/manifest` | Put Extension Manifest |

## accountingData

| Methode | Endpoint | Beschreibung |
|---------|----------|--------------|
| `GET` | `/accountingData` | Query Accounting Data |

## appRegistration

| Methode | Endpoint | Beschreibung |
|---------|----------|--------------|
| `POST` | `/authentication` | Register App |
| `GET` | `/authentication/{registrationId}` | Fetch Registration Status |
| `POST` | `/authentication/{registrationId}` | Register Multi Instance App |

## cancellationreason

| Methode | Endpoint | Beschreibung |
|---------|----------|--------------|
| `GET` | `/cancellationReasons` | Query Cancellation Reasons |
| `GET` | `/invoices/cancellationReasons` | Query Invoice Cancellation Reasons |
| `GET` | `/refunds/cancellationReasons` | Query Refund Cancellation Reasons |
| `GET` | `/salesInvoiceCorrections/cancellationReasons` | Query Sales Invoice Correction Cancellation Reasons |
| `GET` | `/salesOrders/cancellationReasons` | Query Sales Order Cancellation Reasons |

## category

| Methode | Endpoint | Beschreibung |
|---------|----------|--------------|
| `GET` | `/categories` | Query Categories |
| `POST` | `/categories` | Create Category |
| `GET` | `/categories/{categoryId}` | Get Category |
| `PATCH` | `/categories/{categoryId}` | Update Category |
| `GET` | `/categories/{categoryId}/descriptions` | Query Category Descriptions |
| `POST` | `/categories/{categoryId}/descriptions` | Create Category Description |
| `DELETE` | `/categories/{categoryId}/descriptions/{salesChannelId}/{languageIso}` | Delete Category Description |
| `PATCH` | `/categories/{categoryId}/descriptions/{salesChannelId}/{languageIso}` | Update Category Description |
| `POST` | `/categories/{categoryId}/items` | Add Category Items |

## colorcodes

| Methode | Endpoint | Beschreibung |
|---------|----------|--------------|
| `GET` | `/colorCodes` | Query Color Codes |

## company

| Methode | Endpoint | Beschreibung |
|---------|----------|--------------|
| `GET` | `/companies` | Query Companies |

## creditnote

| Methode | Endpoint | Beschreibung |
|---------|----------|--------------|
| `POST` | `/creditNotes/{creditNoteId}/output/mail` | Mail Credit Note |
| `POST` | `/creditNotes/{creditNoteId}/output/pdf` | Pdf Credit Note |
| `POST` | `/creditNotes/{creditNoteId}/output/print` | Print Credit Note |

## customer

| Methode | Endpoint | Beschreibung |
|---------|----------|--------------|
| `GET` | `/customers` | Query Customers |
| `POST` | `/customers` | Create Customer |
| `GET` | `/customers/customfields` | Query Customer Custom Fields |
| `GET` | `/customers/workflowEvents` | Query Customer Workflow Events |
| `DELETE` | `/customers/{customerId}` | Delete Customer |
| `GET` | `/customers/{customerId}` | Get Customer |
| `PATCH` | `/customers/{customerId}` | Update Customer |
| `GET` | `/customers/{customerId}/bankaccounts` | Query Customer Bank Accounts |
| `POST` | `/customers/{customerId}/bankaccounts` | Create Customer Bank Account |
| `DELETE` | `/customers/{customerId}/bankaccounts/{customerBankAccountId}` | Delete Customer Bank Account |
| `GET` | `/customers/{customerId}/bankaccounts/{customerBankAccountId}` | Get Customer Bank Account |
| `PATCH` | `/customers/{customerId}/bankaccounts/{customerBankAccountId}` | Update Customer Bank Account |
| `GET` | `/customers/{customerId}/contacts` | Query Customer Contacts |
| `POST` | `/customers/{customerId}/contacts` | Create Customer Contact |
| `DELETE` | `/customers/{customerId}/contacts/{customerContactId}` | Delete Customer Contact |
| `GET` | `/customers/{customerId}/contacts/{customerContactId}` | Get Customer Contact |
| `PATCH` | `/customers/{customerId}/contacts/{customerContactId}` | Update Customer Contact |
| `GET` | `/customers/{customerId}/customfields` | Query Customer Custom Field Values |
| `DELETE` | `/customers/{customerId}/customfields/{customfieldId}` | Delete Customer Custom Field |
| `PATCH` | `/customers/{customerId}/customfields/{customfieldId}` | Update Customer Custom Field |
| `GET` | `/customers/{customerId}/lastChange` | Get Customer Last Change |
| `GET` | `/customers/{customerId}/notes` | Query Customer Notes |
| `POST` | `/customers/{customerId}/notes` | Create Customer Note |
| `DELETE` | `/customers/{customerId}/notes/{noteId}` | Delete Customer Note |
| `GET` | `/customers/{customerId}/notes/{noteId}` | Get Customer Note |
| `PATCH` | `/customers/{customerId}/notes/{noteId}` | Update Customer Note |
| `POST` | `/customers/{customerId}/workflow/{workflowEventId}` | Trigger Customer Workflow |
| `POST` | `/customers/{customerId}/workflowEvents` | Trigger Customer Workflow Event |

## customerCategory

| Methode | Endpoint | Beschreibung |
|---------|----------|--------------|
| `GET` | `/customerCategories` | Query Customer Categories |
| `POST` | `/customerCategories` | Create Customer Category |
| `DELETE` | `/customerCategories/{customercategoryId}` | Delete Customer Category |
| `GET` | `/customerCategories/{customercategoryId}` | Get Customer Category |
| `PATCH` | `/customerCategories/{customercategoryId}` | Update Customer Category |

## customerGroup

| Methode | Endpoint | Beschreibung |
|---------|----------|--------------|
| `GET` | `/customerGroups` | Query Customer Groups |
| `POST` | `/customerGroups` | Create Customer Group |
| `DELETE` | `/customerGroups/{customergroupId}` | Delete Customer Group |
| `GET` | `/customerGroups/{customergroupId}` | Get Customer Group |
| `PATCH` | `/customerGroups/{customergroupId}` | Update Customer Group |

## deliverynote

| Methode | Endpoint | Beschreibung |
|---------|----------|--------------|
| `GET` | `/deliveryNotes` | Query Delivery Notes |
| `PATCH` | `/deliveryNotes/packages/{packageId}` | Patch Package Data |
| `GET` | `/deliveryNotes/{deliveryNoteId}` | Get Delivery Note |
| `POST` | `/deliveryNotes/{deliveryNoteId}/output/mail` | Mail Delivery Note |
| `POST` | `/deliveryNotes/{deliveryNoteId}/output/pdf` | Pdf Delivery Note |
| `POST` | `/deliveryNotes/{deliveryNoteId}/output/print` | Print Delivery Note |
| `GET` | `/deliveryNotes/{deliveryNoteId}/packages` | Get Delivery Note Packages |
| `POST` | `/deliveryNotes/{deliveryNoteId}/packages` | Post Package Data For Delivery Note |
| `POST` | `/deliveryNotes/{deliveryNoteId}/workflow/{workflowEventId}` | Trigger Delivery Note Workflow |

## features

| Methode | Endpoint | Beschreibung |
|---------|----------|--------------|
| `GET` | `/feature` | Get Features |

## info

| Methode | Endpoint | Beschreibung |
|---------|----------|--------------|
| `GET` | `/info` | Get Status |

## invoice

| Methode | Endpoint | Beschreibung |
|---------|----------|--------------|
| `GET` | `/invoices` | Query Invoices |
| `GET` | `/invoices/workflowEvents` | Query Invoice Workflow Events |
| `GET` | `/invoices/{invoiceId}` | Get Invoice |
| `POST` | `/invoices/{invoiceId}/cancel` | Cancel Invoice |
| `POST` | `/invoices/{invoiceId}/finalize` | Finalize Invoice |
| `GET` | `/invoices/{invoiceId}/lineitems` | Query Invoice Line Items |
| `POST` | `/invoices/{invoiceId}/output/mail` | Mail Invoice |
| `POST` | `/invoices/{invoiceId}/output/pdf` | Pdf Invoice |
| `POST` | `/invoices/{invoiceId}/output/print` | Print Invoice |
| `POST` | `/invoices/{invoiceId}/workflow/{workflowEventId}` | Trigger Invoice Workflow |
| `POST` | `/invoices/{invoiceId}/workflowEvents` | Trigger Invoice Workflow Event |

## item

| Methode | Endpoint | Beschreibung |
|---------|----------|--------------|
| `GET` | `/availabilities` | Query Availabilities |
| `GET` | `/conditions` | Query Conditions |
| `GET` | `/items` | Query Items |
| `POST` | `/items` | Create Item |
| `GET` | `/items/customfields` | Query Item Custom Fields |
| `GET` | `/items/imagedata/{imageId}` | Query Item Image Data |
| `PATCH` | `/items/salesChannels` | Update Item Sales Channels |
| `GET` | `/items/workflowEvents` | Query Item Workflow Events |
| `GET` | `/items/{itemId}` | Get Item |
| `PATCH` | `/items/{itemId}` | Update Item |
| `POST` | `/items/{itemId}/children/{childItemId}` | Assign Child Item To Parent |
| `GET` | `/items/{itemId}/customerPrices` | Query Item Customer Prices |
| `POST` | `/items/{itemId}/customerPrices` | Create Item Customer Price |
| `DELETE` | `/items/{itemId}/customerPrices/{customerId}/{fromQuantity}` | Delete Item Customer Price |
| `PATCH` | `/items/{itemId}/customerPrices/{customerId}/{fromQuantity}` | Update Item Customer Price |
| `GET` | `/items/{itemId}/customfields` | Query Item Custom Field Values |
| `DELETE` | `/items/{itemId}/customfields/{customfieldId}` | Delete Item Custom Field |
| `PATCH` | `/items/{itemId}/customfields/{customfieldId}` | Update Item Custom Field |
| `GET` | `/items/{itemId}/descriptions` | Query Item Descriptions |
| `POST` | `/items/{itemId}/descriptions` | Create Item Description |
| `DELETE` | `/items/{itemId}/descriptions/{salesChannelId}/{languageIso}` | Delete Item Description |
| `PATCH` | `/items/{itemId}/descriptions/{salesChannelId}/{languageIso}` | Update Item Description |
| `GET` | `/items/{itemId}/images` | Query Item Images |
| `POST` | `/items/{itemId}/images` | Create Item Image |
| `DELETE` | `/items/{itemId}/images/{imageId}` | Delete Item Image |
| `PATCH` | `/items/{itemId}/images/{imageId}` | Update Item Image |
| `GET` | `/items/{itemId}/properties` | Query Item Properties |
| `POST` | `/items/{itemId}/properties` | Create Item Property |
| `DELETE` | `/items/{itemId}/properties/{propertyValueId}` | Delete Item Property |
| `GET` | `/items/{itemId}/salesChannelPrices` | Query Item Sales Channel Price |
| `POST` | `/items/{itemId}/salesChannelPrices` | Create Item Sales Channel Price |
| `DELETE` | `/items/{itemId}/salesChannelPrices/{salesChannelId}/{customerGroupId}/{fromQuantity}` | Delete Item Sales Channel Price |
| `PATCH` | `/items/{itemId}/salesChannelPrices/{salesChannelId}/{customerGroupId}/{fromQuantity}` | Update Item Sales Channel Price |
| `GET` | `/items/{itemId}/specialprices` | Query Item Special Price |
| `PATCH` | `/items/{itemId}/specialprices` | Update Item Special Price |
| `GET` | `/items/{itemId}/suppliers` | Query Item Suppliers |
| `POST` | `/items/{itemId}/suppliers` | Create Item Supplier |
| `DELETE` | `/items/{itemId}/suppliers/{supplierId}` | Delete Item Supplier |
| `PATCH` | `/items/{itemId}/suppliers/{supplierId}` | Update Item Supplier |
| `GET` | `/items/{itemId}/variations` | Query Item Variations |
| `POST` | `/items/{itemId}/variations` | Create Item Variation |
| `DELETE` | `/items/{itemId}/variations/{variationId}` | Delete Item Variation |
| `PATCH` | `/items/{itemId}/variations/{variationId}` | Update Item Variation |
| `GET` | `/items/{itemId}/variations/{variationId}/values` | Query Item Variation Values |
| `POST` | `/items/{itemId}/variations/{variationId}/values` | Create Item Variation Value |
| `DELETE` | `/items/{itemId}/variations/{variationId}/values/{variationValueId}` | Delete Item Variation Value |
| `PATCH` | `/items/{itemId}/variations/{variationId}/values/{variationValueId}` | Update Item Variation Value |
| `POST` | `/items/{itemId}/workflow/{workflowEventId}` | Trigger Item Workflow |
| `POST` | `/items/{itemId}/workflowEvents` | Trigger Item Workflow Event |
| `GET` | `/manufacturers` | Query Manufacturers |
| `GET` | `/productGroups` | Query Product Groups |
| `GET` | `/responsiblePersons` | Query Responsible Persons |
| `GET` | `/shippingClasses` | Query Shipping Classes |
| `GET` | `/taxClasses` | Query Tax Classes |

## login

| Methode | Endpoint | Beschreibung |
|---------|----------|--------------|
| `POST` | `/authentication/login` | Login |

## logout

| Methode | Endpoint | Beschreibung |
|---------|----------|--------------|
| `POST` | `/authentication/logout` | Logout |

## offer

| Methode | Endpoint | Beschreibung |
|---------|----------|--------------|
| `POST` | `/offer/{offerId}/output/mail` | Mail Offer |
| `POST` | `/offer/{offerId}/output/pdf` | Pdf Offer |
| `POST` | `/offer/{offerId}/output/print` | Print Offer |

## onholdreason

| Methode | Endpoint | Beschreibung |
|---------|----------|--------------|
| `GET` | `/onHoldReasons` | Query On Hold Reasons |

## paymentmethod

| Methode | Endpoint | Beschreibung |
|---------|----------|--------------|
| `GET` | `/paymentMethods` | Query Payment Methods |

## printer

| Methode | Endpoint | Beschreibung |
|---------|----------|--------------|
| `GET` | `/printers` | Installed Printers |

## property

| Methode | Endpoint | Beschreibung |
|---------|----------|--------------|
| `GET` | `/properties` | Query Properties |
| `POST` | `/properties` | Create Property |
| `GET` | `/properties/groups` | Query Property Groups |
| `POST` | `/properties/groups` | Create Property Group |
| `GET` | `/properties/{propertyId}/values` | Query Property Values |
| `POST` | `/properties/{propertyId}/values` | Create Property Value |
| `DELETE` | `/properties/{propertyId}/values/{propertyValueId}` | Delete Property Value |
| `PATCH` | `/properties/{propertyId}/values/{propertyValueId}` | Update Property Value |
| `GET` | `/properties/{propertyId}/values/{propertyValueId}/descriptions` | Query Property Value Descriptions |
| `POST` | `/properties/{propertyId}/values/{propertyValueId}/descriptions` | Create Property Value Description |
| `DELETE` | `/properties/{propertyId}/values/{propertyValueId}/descriptions/{languageIso}` | Delete Property Value Description |
| `PATCH` | `/properties/{propertyId}/values/{propertyValueId}/descriptions/{languageIso}` | Update Property Value Description |

## return

| Methode | Endpoint | Beschreibung |
|---------|----------|--------------|
| `GET` | `/returns` | Query Returns |
| `POST` | `/returns` | Create Return |
| `GET` | `/returns/{returnId}` | Get Return |
| `GET` | `/returns/{returnId}/lineitems` | Query Return Line Items |
| `GET` | `/returns/{returnId}/packages` | Query Return Packages |

## returnreason

| Methode | Endpoint | Beschreibung |
|---------|----------|--------------|
| `GET` | `/returnReasons` | Query Return Reasons |

## returnstate

| Methode | Endpoint | Beschreibung |
|---------|----------|--------------|
| `GET` | `/returnStates` | Query Return States |

## saleschannel

| Methode | Endpoint | Beschreibung |
|---------|----------|--------------|
| `GET` | `/salesChannels` | Get Sales Channels |

## salesinvoicecorrection

| Methode | Endpoint | Beschreibung |
|---------|----------|--------------|
| `POST` | `/salesInvoiceCorrections/{salesInvoiceCorrectionId}/finalize` | Finalize Sales Invoice Correction |

## salesorder

| Methode | Endpoint | Beschreibung |
|---------|----------|--------------|
| `GET` | `/salesOrders` | Query Sales Orders |
| `POST` | `/salesOrders` | Create Sales Order |
| `GET` | `/salesOrders/customfields` | Query Sales Order Custom Fields |
| `GET` | `/salesOrders/workflowEvents` | Query Sales Order Workflow Events |
| `GET` | `/salesOrders/{salesOrderId}` | Get Sales Order |
| `PATCH` | `/salesOrders/{salesOrderId}` | Update Sales Order |
| `POST` | `/salesOrders/{salesOrderId}/cancel` | Cancel Sales Order |
| `POST` | `/salesOrders/{salesOrderId}/createinvoice` | New Invoice |
| `GET` | `/salesOrders/{salesOrderId}/customfields` | Query Sales Order Custom Field Values |
| `DELETE` | `/salesOrders/{salesOrderId}/customfields/{customfieldId}` | Delete Sales Order Custom Field |
| `PATCH` | `/salesOrders/{salesOrderId}/customfields/{customfieldId}` | Update Sales Order Custom Field |
| `GET` | `/salesOrders/{salesOrderId}/files` | Query Sales Order Files |
| `POST` | `/salesOrders/{salesOrderId}/files` | Create Sales Order File |
| `DELETE` | `/salesOrders/{salesOrderId}/files/{salesOrderFileId}` | Delete Sales Order File |
| `GET` | `/salesOrders/{salesOrderId}/files/{salesOrderFileId}` | Query Sales Order File Data |
| `PATCH` | `/salesOrders/{salesOrderId}/files/{salesOrderFileId}` | Update Sales Order File |
| `GET` | `/salesOrders/{salesOrderId}/lineitems` | Query Sales Order Line Items |
| `POST` | `/salesOrders/{salesOrderId}/lineitems` | Create Sales Order Line Item |
| `DELETE` | `/salesOrders/{salesOrderId}/lineitems/{salesOrderLineItemId}` | Delete Sales Order Line Item |
| `PATCH` | `/salesOrders/{salesOrderId}/lineitems/{salesOrderLineItemId}` | Update Sales Order Line Item |
| `GET` | `/salesOrders/{salesOrderId}/lineitems/{salesOrderLineItemId}/files` | Query Sales Order Line Item Files |
| `POST` | `/salesOrders/{salesOrderId}/lineitems/{salesOrderLineItemId}/files` | Create Sales Order Line Item File |
| `DELETE` | `/salesOrders/{salesOrderId}/lineitems/{salesOrderLineItemId}/files/{salesOrderLineItemFileId}` | Delete Sales Order Line Item File |
| `GET` | `/salesOrders/{salesOrderId}/lineitems/{salesOrderLineItemId}/files/{salesOrderLineItemFileId}` | Query Sales Order Line Item File Data |
| `PATCH` | `/salesOrders/{salesOrderId}/lineitems/{salesOrderLineItemId}/files/{salesOrderLineItemFileId}` | Update Sales Order Line Item File |
| `GET` | `/salesOrders/{salesOrderId}/notes` | Query Sales Order Notes |
| `POST` | `/salesOrders/{salesOrderId}/notes` | Create Sales Order Note |
| `DELETE` | `/salesOrders/{salesOrderId}/notes/{noteId}` | Delete Sales Order Note |
| `PATCH` | `/salesOrders/{salesOrderId}/notes/{noteId}` | Update Sales Order Note |
| `POST` | `/salesOrders/{salesOrderId}/output/mail` | Mail Sales Order |
| `POST` | `/salesOrders/{salesOrderId}/output/pdf` | Pdf Sales Order |
| `POST` | `/salesOrders/{salesOrderId}/output/print` | Print Sales Order |
| `POST` | `/salesOrders/{salesOrderId}/undocancellation` | Undo Sales Order Cancellation |
| `POST` | `/salesOrders/{salesOrderId}/workflow/{workflowEventId}` | Trigger Sales Order Workflow |
| `POST` | `/salesOrders/{salesOrderId}/workflowEvents` | Trigger Sales Order Workflow Event |

## shipping

| Methode | Endpoint | Beschreibung |
|---------|----------|--------------|
| `POST` | `/delivery/cancelReservation` | Cancel Reservation |
| `POST` | `/delivery/deliver` | Deliver Sales Order |
| `POST` | `/delivery/reassign` | Reassign Stock |
| `GET` | `/delivery/reservations` | Query Reservations |
| `POST` | `/delivery/reserve` | Reserve Sales Orders |

## shippingmethod

| Methode | Endpoint | Beschreibung |
|---------|----------|--------------|
| `GET` | `/shippingMethods` | Query Shipping Methods |

## stock

| Methode | Endpoint | Beschreibung |
|---------|----------|--------------|
| `GET` | `/stocks` | Query Stocks Per Item |
| `POST` | `/stocks` | Stock Adjustment |
| `GET` | `/stocks/changes` | Query Stock Changes |
| `GET` | `/stocks/serialnumbers` | Query Serial Number Per Warehouse |

## supplier

| Methode | Endpoint | Beschreibung |
|---------|----------|--------------|
| `GET` | `/suppliers` | Query Suppliers |

## tax

| Methode | Endpoint | Beschreibung |
|---------|----------|--------------|
| `GET` | `/tax/item/{itemId}/{companyId}/{departureCountryISO}/{shipmentCountryISO}` | Get Tax For Item |
| `GET` | `/tax/taxclass/{taxClassId}/{companyId}/{departureCountryISO}/{shipmentCountryISO}` | Get Tax For Tax Class |

## transactionStatus

| Methode | Endpoint | Beschreibung |
|---------|----------|--------------|
| `GET` | `/transactionStatuses` | Query Transaction Status |

## warehouse

| Methode | Endpoint | Beschreibung |
|---------|----------|--------------|
| `GET` | `/warehouses` | Query Warehouses |
| `GET` | `/warehouses/storagelocationtypes` | Query Storage Location Type |
| `GET` | `/warehouses/types` | Query Warehouse Types |
| `GET` | `/warehouses/{warehouseId}/storagelocations` | Query Storage Locations |

## wms

| Methode | Endpoint | Beschreibung |
|---------|----------|--------------|
| `GET` | `/wms/picklisttemplates` | Query Pick List Template |
| `GET` | `/wms/{warehouseId}/picklists` | Query Pick List |
| `POST` | `/wms/{warehouseId}/picklists` | Create Pick List |
| `GET` | `/wms/{warehouseId}/picklists/{picklistId}` | Query Pick List Position |
| `DELETE` | `/wms/{warehouseId}/picklists/{picklistId}/positions/{picklistPositionId}` | Delete Pick List Position |
| `PATCH` | `/wms/{warehouseId}/picklists/{picklistId}/positions/{picklistPositionId}/changeReservation` | Change Reservation |
| `PATCH` | `/wms/{warehouseId}/picklists/{picklistId}/positions/{picklistPositionId}/pickPosition` | Pick Position |

## worker

| Methode | Endpoint | Beschreibung |
|---------|----------|--------------|
| `GET` | `/workers` | Get Worker Syncs |
| `GET` | `/workers/status` | Get Worker Status |
| `POST` | `/workers/{syncId}` | Configure Sync |
| `PUT` | `/workers/{syncId}` | Sync Control |

---

## Statistik

- **Gesamt**: 243 Endpoints
- **Kategorien**: 39

## Häufig verwendete Endpoints

### Kunden

| Aktion | Methode | Endpoint |
|--------|---------|----------|
| Liste abrufen | GET | /customers |
| Einzeln abrufen | GET | /customers/{customerId} |
| Anlegen | POST | /customers |
| Aktualisieren | PATCH | /customers/{customerId} |
| Löschen | DELETE | /customers/{customerId} |

### Aufträge

| Aktion | Methode | Endpoint |
|--------|---------|----------|
| Liste abrufen | GET | /salesOrders |
| Einzeln abrufen | GET | /salesOrders/{salesOrderId} |
| Anlegen | POST | /salesOrders |
| Aktualisieren | PATCH | /salesOrders/{salesOrderId} |
| Stornieren | POST | /salesOrders/{salesOrderId}/cancel |
| Rechnung erstellen | POST | /salesOrders/{salesOrderId}/createinvoice |

### Artikel

| Aktion | Methode | Endpoint |
|--------|---------|----------|
| Liste abrufen | GET | /items |
| Einzeln abrufen | GET | /items/{itemId} |
| Anlegen | POST | /items |
| Aktualisieren | PATCH | /items/{itemId} |

### Lagerbestand

| Aktion | Methode | Endpoint |
|--------|---------|----------|
| Bestände abrufen | GET | /stocks |
| Bestand anpassen | POST | /stocks |
| Änderungen abrufen | GET | /stocks/changes |

### Rechnungen

| Aktion | Methode | Endpoint |
|--------|---------|----------|
| Liste abrufen | GET | /invoices |
| Einzeln abrufen | GET | /invoices/{invoiceId} |
| Abschließen | POST | /invoices/{invoiceId}/finalize |
| Stornieren | POST | /invoices/{invoiceId}/cancel |
| Als PDF | POST | /invoices/{invoiceId}/output/pdf |
