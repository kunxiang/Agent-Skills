#!/usr/bin/env python3
"""
JTL-Wawi API Client

Ein einfacher Python-Client für die JTL-Wawi REST API.

Verwendung:
    from api_client import JtlWawiClient

    client = JtlWawiClient(
        base_url="http://localhost:5883",
        api_key="FB622234-98A7-46FA-A01B-06C9D0971AAF",
        app_id="meine-firma/meine-app/v1",
        app_version="1.0.0"
    )

    # Kunden abrufen
    customers = client.query_customers(search="Mustermann")

    # Auftrag erstellen
    order = client.create_sales_order(order_data)
"""

import os
import requests
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class ApiResponse:
    """API Response Wrapper"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    status_code: int = 0


class JtlWawiClient:
    """
    JTL-Wawi REST API Client

    Attributes:
        base_url: Basis-URL der API (z.B. http://localhost:5883)
        api_key: Der bei der Registrierung erhaltene API-Key
        app_id: Die App-ID (z.B. meine-firma/meine-app/v1)
        app_version: Die App-Version (z.B. 1.0.0)
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        app_id: Optional[str] = None,
        app_version: Optional[str] = None,
        api_version: str = "1.0"
    ):
        """
        Initialisiert den Client.

        Werte können auch über Umgebungsvariablen gesetzt werden:
        - JTL_API_BASE_URL
        - JTL_API_KEY
        - JTL_APP_ID
        - JTL_APP_VERSION
        """
        self.base_url = base_url or os.getenv("JTL_API_BASE_URL", "http://localhost:5883")
        self.api_key = api_key or os.getenv("JTL_API_KEY")
        self.app_id = app_id or os.getenv("JTL_APP_ID", "my-app/v1")
        self.app_version = app_version or os.getenv("JTL_APP_VERSION", "1.0.0")
        self.api_version = api_version

        if not self.api_key:
            raise ValueError("API-Key erforderlich. Setzen Sie JTL_API_KEY oder übergeben Sie api_key.")

    def _get_headers(self) -> Dict[str, str]:
        """Erstellt die Standard-Headers für API-Anfragen"""
        return {
            "Authorization": f"Wawi {self.api_key}",
            "api-version": self.api_version,
            "X-AppID": self.app_id,
            "X-AppVersion": self.app_version,
            "Content-Type": "application/json"
        }

    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None
    ) -> ApiResponse:
        """
        Führt eine API-Anfrage durch.

        Args:
            method: HTTP-Methode (GET, POST, PUT, DELETE)
            endpoint: API-Endpoint (z.B. /customer/123)
            data: Request Body (für POST/PUT)
            params: Query-Parameter

        Returns:
            ApiResponse mit Ergebnis oder Fehler
        """
        url = f"{self.base_url}{endpoint}"

        try:
            response = requests.request(
                method=method,
                url=url,
                json=data,
                params=params,
                headers=self._get_headers(),
                timeout=30
            )

            if response.status_code in (200, 201, 202):
                return ApiResponse(
                    success=True,
                    data=response.json() if response.content else None,
                    status_code=response.status_code
                )
            elif response.status_code == 204:
                return ApiResponse(
                    success=True,
                    data=None,
                    status_code=response.status_code
                )
            else:
                error_detail = ""
                try:
                    error_data = response.json()
                    error_detail = error_data.get("detail", str(error_data))
                except:
                    error_detail = response.text

                return ApiResponse(
                    success=False,
                    error=f"HTTP {response.status_code}: {error_detail}",
                    status_code=response.status_code
                )

        except requests.exceptions.ConnectionError:
            return ApiResponse(
                success=False,
                error=f"Verbindungsfehler: {url} nicht erreichbar"
            )
        except requests.exceptions.Timeout:
            return ApiResponse(
                success=False,
                error="Timeout: Server antwortet nicht"
            )
        except Exception as e:
            return ApiResponse(
                success=False,
                error=f"Fehler: {str(e)}"
            )

    # ==================== Kunden ====================

    def get_customer(self, customer_id: int) -> ApiResponse:
        """Ruft einen Kunden anhand der ID ab"""
        return self._request("GET", f"/customer/{customer_id}")

    def query_customers(
        self,
        search: Optional[str] = None,
        page_size: int = 100,
        page_index: int = 0
    ) -> ApiResponse:
        """
        Sucht Kunden.

        Args:
            search: Suchbegriff (Name, E-Mail, etc.)
            page_size: Einträge pro Seite
            page_index: Seitennummer (0-basiert)
        """
        data = {
            "PageSize": page_size,
            "PageIndex": page_index
        }
        if search:
            data["SearchKeyWord"] = search

        return self._request("POST", "/customer/query", data=data)

    def create_customer(self, customer_data: Dict[str, Any]) -> ApiResponse:
        """
        Legt einen neuen Kunden an.

        Args:
            customer_data: Kundendaten (siehe API-Dokumentation)
        """
        return self._request("POST", "/customer", data=customer_data)

    def update_customer(self, customer_id: int, customer_data: Dict[str, Any]) -> ApiResponse:
        """Aktualisiert einen Kunden"""
        return self._request("PUT", f"/customer/{customer_id}", data=customer_data)

    def delete_customer(self, customer_id: int) -> ApiResponse:
        """Löscht einen Kunden"""
        return self._request("DELETE", f"/customer/{customer_id}")

    # ==================== Aufträge ====================

    def get_sales_order(self, order_id: int) -> ApiResponse:
        """Ruft einen Auftrag anhand der ID ab"""
        return self._request("GET", f"/salesorder/{order_id}")

    def query_sales_orders(
        self,
        search: Optional[str] = None,
        page_size: int = 100,
        page_index: int = 0
    ) -> ApiResponse:
        """Sucht Aufträge"""
        data = {
            "PageSize": page_size,
            "PageIndex": page_index
        }
        if search:
            data["SearchKeyWord"] = search

        return self._request("POST", "/salesorder/query", data=data)

    def create_sales_order(self, order_data: Dict[str, Any]) -> ApiResponse:
        """Legt einen neuen Auftrag an"""
        return self._request("POST", "/salesorder", data=order_data)

    # ==================== Artikel ====================

    def get_article(self, article_id: int) -> ApiResponse:
        """Ruft einen Artikel anhand der ID ab"""
        return self._request("GET", f"/article/{article_id}")

    def query_articles(
        self,
        search: Optional[str] = None,
        page_size: int = 100,
        page_index: int = 0
    ) -> ApiResponse:
        """Sucht Artikel"""
        data = {
            "PageSize": page_size,
            "PageIndex": page_index
        }
        if search:
            data["SearchKeyWord"] = search

        return self._request("POST", "/article/query", data=data)

    # ==================== Lagerbestand ====================

    def query_stock(
        self,
        article_id: Optional[int] = None,
        warehouse_id: Optional[int] = None,
        page_size: int = 100,
        page_index: int = 0
    ) -> ApiResponse:
        """Fragt Lagerbestand ab"""
        data = {
            "PageSize": page_size,
            "PageIndex": page_index
        }
        if article_id:
            data["ArticleId"] = article_id
        if warehouse_id:
            data["WarehouseId"] = warehouse_id

        return self._request("POST", "/stock/query", data=data)

    def adjust_stock(
        self,
        article_id: int,
        warehouse_id: int,
        quantity: float,
        reason: str = "API-Bestandsanpassung"
    ) -> ApiResponse:
        """
        Passt den Lagerbestand an.

        Args:
            article_id: Artikel-ID
            warehouse_id: Lager-ID
            quantity: Menge (positiv = Zugang, negativ = Abgang)
            reason: Grund für die Anpassung
        """
        data = {
            "ArticleId": article_id,
            "WarehouseId": warehouse_id,
            "Quantity": quantity,
            "Reason": reason
        }
        return self._request("POST", "/stock/adjustment", data=data)

    # ==================== Rechnungen ====================

    def get_invoice(self, invoice_id: int) -> ApiResponse:
        """Ruft eine Rechnung anhand der ID ab"""
        return self._request("GET", f"/invoice/{invoice_id}")

    def query_invoices(
        self,
        search: Optional[str] = None,
        page_size: int = 100,
        page_index: int = 0
    ) -> ApiResponse:
        """Sucht Rechnungen"""
        data = {
            "PageSize": page_size,
            "PageIndex": page_index
        }
        if search:
            data["SearchKeyWord"] = search

        return self._request("POST", "/invoice/query", data=data)

    # ==================== Firmen ====================

    def query_companies(self) -> ApiResponse:
        """Ruft alle Firmen/Mandanten ab"""
        return self._request("POST", "/company/query", data={"PageSize": 100})

    # ==================== Kategorien ====================

    def get_category(self, category_id: int) -> ApiResponse:
        """Ruft eine Kategorie anhand der ID ab"""
        return self._request("GET", f"/category/{category_id}")

    def query_categories(
        self,
        search: Optional[str] = None,
        page_size: int = 100,
        page_index: int = 0
    ) -> ApiResponse:
        """Sucht Kategorien"""
        data = {
            "PageSize": page_size,
            "PageIndex": page_index
        }
        if search:
            data["SearchKeyWord"] = search

        return self._request("POST", "/category/query", data=data)


# ==================== Beispiele ====================

if __name__ == "__main__":
    # Beispiel: Client initialisieren
    # API-Key aus Umgebungsvariable oder direkt angeben

    try:
        client = JtlWawiClient(
            # base_url="http://localhost:5883",
            # api_key="FB622234-98A7-46FA-A01B-06C9D0971AAF",
        )
    except ValueError as e:
        print(f"Fehler: {e}")
        print("Setzen Sie die Umgebungsvariable JTL_API_KEY oder übergeben Sie den API-Key.")
        exit(1)

    # Beispiel: Kunden suchen
    print("Suche Kunden mit 'Mustermann'...")
    result = client.query_customers(search="Mustermann")

    if result.success:
        customers = result.data.get("Items", [])
        print(f"Gefunden: {len(customers)} Kunden")
        for customer in customers[:5]:
            print(f"  - {customer.get('DisplayName', 'N/A')}")
    else:
        print(f"Fehler: {result.error}")

    # Beispiel: Firmen abfragen
    print("\nFrage Firmen ab...")
    result = client.query_companies()

    if result.success:
        companies = result.data.get("Items", [])
        print(f"Gefunden: {len(companies)} Firmen")
        for company in companies:
            print(f"  - {company.get('Name', 'N/A')}")
    else:
        print(f"Fehler: {result.error}")
