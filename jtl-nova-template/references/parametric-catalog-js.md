# Parametric Catalog - JavaScript

## ParametricCatalog Klasse

Vollständige JavaScript-Klasse für Ansichtenwechsel, Filter, Sortierung, Vergleich und Export.

```javascript
class ParametricCatalog {
    constructor() {
        this.container = document.querySelector('.parametric-catalog');
        if (!this.container) return;
        this.view = this.container.dataset.view || 'gallery';
        this.compareList = [];
        this.init();
    }

    init() {
        this.initViewSwitcher();
        this.initFilters();
        this.initTableSort();
        this.initCompare();
        this.initExport();
        this.initKeyboard();
        this.switchView(this.view, false);
    }

    // Ansichtenwechsel
    initViewSwitcher() {
        this.container.querySelectorAll('.view-btn').forEach(btn => {
            btn.addEventListener('click', () => this.switchView(btn.dataset.view));
        });
    }

    switchView(view, save = true) {
        // Buttons aktualisieren
        this.container.querySelectorAll('.view-btn').forEach(b =>
            b.classList.toggle('active', b.dataset.view === view));

        // Ansichten wechseln
        this.container.querySelectorAll('.catalog-view').forEach(v => v.style.display = 'none');
        this.container.querySelector(`.view-${view}`).style.display = '';

        // Tabellen-Tools ein-/ausblenden
        const tools = this.container.querySelector('.table-tools');
        if (tools) tools.style.display = view === 'table' ? '' : 'none';

        this.view = view;

        // Einstellung speichern
        if (save) {
            fetch('/io.php', {
                method: 'POST',
                headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                body: `io={"name":"setCatalogView","params":["${view}"]}`
            });
            localStorage.setItem('catalogView', view);
        }
    }

    // Filter-Dropdowns
    initFilters() {
        this.container.querySelectorAll('[data-toggle="dropdown"]').forEach(btn => {
            btn.addEventListener('click', e => {
                e.stopPropagation();
                const content = btn.nextElementSibling;
                this.container.querySelectorAll('.filter-dropdown-content.show').forEach(c => {
                    if (c !== content) c.classList.remove('show');
                });
                content.classList.toggle('show');
            });
        });

        document.addEventListener('click', () => {
            this.container.querySelectorAll('.filter-dropdown-content.show').forEach(c => c.classList.remove('show'));
        });

        // Filter-Suche
        this.container.querySelectorAll('.filter-search').forEach(input => {
            input.addEventListener('input', e => {
                const term = e.target.value.toLowerCase();
                e.target.parentElement.querySelectorAll('.filter-option').forEach(opt => {
                    opt.style.display = opt.textContent.toLowerCase().includes(term) ? '' : 'none';
                });
            });
        });

        // Auto-Apply mit Debounce
        let timeout;
        this.container.querySelectorAll('.filter-options input').forEach(cb => {
            cb.addEventListener('change', () => {
                clearTimeout(timeout);
                timeout = setTimeout(() => this.applyFilters(), 500);
            });
        });
    }

    applyFilters() {
        const form = document.createElement('form');
        form.method = 'GET';
        form.action = location.pathname;
        this.container.querySelectorAll('.filter-options input:checked').forEach(cb => {
            const input = document.createElement('input');
            input.type = 'hidden';
            input.name = cb.name;
            input.value = cb.value;
            form.appendChild(input);
        });
        document.body.appendChild(form);
        form.submit();
    }

    // Tabellensortierung
    initTableSort() {
        this.container.querySelectorAll('th.sortable').forEach(th => {
            th.addEventListener('click', () => {
                const key = th.dataset.sort;
                const order = th.dataset.order === 'asc' ? 'desc' : 'asc';
                this.container.querySelectorAll('th.sortable').forEach(h => h.dataset.order = '');
                th.dataset.order = order;
                this.sortTable(key, order);
            });
        });
    }

    sortTable(key, order) {
        const tbody = this.container.querySelector('.product-table tbody');
        const rows = Array.from(tbody.querySelectorAll('tr'));

        rows.sort((a, b) => {
            let av, bv;
            if (key === 'price') {
                av = parseFloat(a.dataset.price) || 0;
                bv = parseFloat(b.dataset.price) || 0;
            } else if (key === 'stock') {
                av = parseInt(a.dataset.stock) || 0;
                bv = parseInt(b.dataset.stock) || 0;
            } else if (key === 'name') {
                av = a.querySelector('td:nth-child(3)').textContent.trim();
                bv = b.querySelector('td:nth-child(3)').textContent.trim();
            } else if (key.startsWith('param_')) {
                const id = key.replace('param_', '');
                av = this.extractNum(a.querySelector(`[data-merkmal="${id}"]`)?.textContent);
                bv = this.extractNum(b.querySelector(`[data-merkmal="${id}"]`)?.textContent);
            }
            if (typeof av === 'string') return order === 'asc' ? av.localeCompare(bv) : bv.localeCompare(av);
            return order === 'asc' ? av - bv : bv - av;
        });

        rows.forEach(r => tbody.appendChild(r));
    }

    extractNum(str) {
        if (!str) return 0;
        const m = str.match(/[\d.,]+/);
        return m ? parseFloat(m[0].replace(',', '.')) : 0;
    }

    // Produktvergleich
    initCompare() {
        const btn = this.container.querySelector('#compareBtn');
        const count = this.container.querySelector('#compareCount');

        this.container.querySelectorAll('.compare-cb').forEach(cb => {
            cb.addEventListener('change', e => {
                if (e.target.checked && this.compareList.length < 4) {
                    this.compareList.push(e.target.value);
                } else if (e.target.checked) {
                    e.target.checked = false;
                    alert('Max 4 Produkte');
                } else {
                    this.compareList = this.compareList.filter(id => id !== e.target.value);
                }
                count.textContent = this.compareList.length;
                btn.disabled = this.compareList.length < 2;
            });
        });

        btn.addEventListener('click', () => {
            if (this.compareList.length >= 2) {
                location.href = `/vergleichsliste.php?a=${this.compareList.join('_')}`;
            }
        });
    }

    // Export
    initExport() {
        this.container.querySelector('#exportBtn')?.addEventListener('click', () => {
            const params = new URLSearchParams(location.search);
            params.set('export', '1');
            params.set('format', 'csv');
            location.href = `${location.pathname}?${params}`;
        });
    }

    // Tastaturkürzel
    initKeyboard() {
        document.addEventListener('keydown', e => {
            if (e.altKey) {
                if (e.key === '1') this.switchView('gallery');
                if (e.key === '2') this.switchView('list');
                if (e.key === '3') this.switchView('table');
            }
        });
    }
}

// Initialisierung
document.addEventListener('DOMContentLoaded', () => new ParametricCatalog());
```

## Verwendung

1. Script in `templates/MeinTheme/js/parametric-catalog.js` speichern
2. Im Template einbinden:

```smarty
{inline_script}
<script src="{$ShopURL}/templates/{$template->getName()}/js/parametric-catalog.js"></script>
{/inline_script}
```

## Funktionen

| Funktion | Beschreibung |
|----------|--------------|
| `switchView(view)` | Wechselt Ansicht (gallery/list/table) |
| `applyFilters()` | Wendet ausgewählte Filter an |
| `sortTable(key, order)` | Sortiert Tabelle nach Spalte |
| `initCompare()` | Aktiviert Produktvergleich (max 4) |
| `initExport()` | CSV-Export der aktuellen Ansicht |

## Tastaturkürzel

| Kürzel | Aktion |
|--------|--------|
| Alt+1 | Galerie-Ansicht |
| Alt+2 | Listen-Ansicht |
| Alt+3 | Tabellen-Ansicht |
