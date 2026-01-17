# Parametric Catalog - SCSS Stile

## Haupt-Stylesheet (_parametric-catalog.scss)

```scss
// Variablen (nutzt Bootstrap/NOVA Variablen)
// $primary, $gray-100, $border-color, $border-radius, $box-shadow aus _variables.scss

.parametric-catalog {
    // Header
    .catalog-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 3px solid $primary;

        h1 {
            margin: 0;
            font-size: 1.5rem;
        }

        .result-count {
            color: $gray-600;
        }
    }

    // Toolbar
    .catalog-toolbar {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1rem;
        flex-wrap: wrap;

        .table-tools {
            display: none;
        }

        #sortSelect {
            width: auto;
            min-width: 180px;
        }
    }

    // View-Buttons
    .view-btn {
        padding: 0.5rem 0.75rem;

        &.active {
            background: $primary;
            color: white;
            border-color: $primary;
        }
    }
}

// Filter
.parametric-filter {
    background: $gray-100;
    padding: 1rem;
    border-radius: $border-radius;
    margin-bottom: 1rem;

    .filter-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
    }

    .filter-dropdown {
        position: relative;
    }

    .filter-btn {
        padding: 0.5rem 1rem;
        background: white;
        border: 1px solid $border-color;
        border-radius: $border-radius;
        cursor: pointer;
        font-size: 0.9rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;

        &:hover {
            border-color: $primary;
        }

        .badge {
            background: $primary;
            color: white;
            padding: 0.2rem 0.5rem;
            border-radius: 50px;
            font-size: 0.75rem;
        }
    }

    .filter-dropdown-content {
        display: none;
        position: absolute;
        top: 100%;
        left: 0;
        z-index: 1000;
        min-width: 250px;
        max-height: 300px;
        overflow-y: auto;
        background: white;
        border: 1px solid $border-color;
        border-radius: $border-radius;
        box-shadow: $box-shadow;
        padding: 0.5rem;
        margin-top: 2px;

        &.show {
            display: block;
        }
    }

    .filter-search {
        width: 100%;
        padding: 0.5rem;
        margin-bottom: 0.5rem;
        border: 1px solid $border-color;
        border-radius: $border-radius;

        &:focus {
            outline: none;
            border-color: $primary;
        }
    }

    .filter-option {
        display: flex;
        align-items: center;
        padding: 0.375rem 0.5rem;
        cursor: pointer;
        border-radius: $border-radius-sm;

        &:hover {
            background: $gray-100;
        }

        input {
            margin-right: 0.5rem;
        }

        small {
            margin-left: auto;
            color: $gray-500;
        }
    }

    // Aktive Filter-Tags
    .active-filters {
        margin-top: 1rem;
        padding-top: 0.5rem;
        border-top: 1px solid $border-color;
    }

    .filter-tag {
        display: inline-flex;
        align-items: center;
        background: $primary;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 50px;
        font-size: 0.8rem;
        margin: 0.25rem;

        a {
            color: white;
            margin-left: 0.5rem;
            text-decoration: none;
            font-weight: bold;

            &:hover {
                opacity: 0.8;
            }
        }
    }
}

// Listenansicht
.product-list-item {
    padding: 1rem;
    border: 1px solid $border-color;
    border-radius: $border-radius;
    margin-bottom: 0.75rem;
    transition: box-shadow 0.2s;

    &:hover {
        box-shadow: $box-shadow;
    }

    .price {
        color: $primary;
        font-weight: bold;
    }
}

// Tabellenansicht
.product-table-wrapper {
    overflow-x: auto;
}

.product-table {
    font-size: 0.85rem;
    white-space: nowrap;

    th {
        background: $gray-100;
        position: sticky;
        top: 0;

        &.sortable {
            cursor: pointer;
            user-select: none;

            &:hover {
                background: $gray-200;
            }

            &[data-order="asc"]::after {
                content: " ↑";
                color: $primary;
            }

            &[data-order="desc"]::after {
                content: " ↓";
                color: $primary;
            }
        }
    }

    td {
        vertical-align: middle;

        img {
            border-radius: $border-radius-sm;
        }
    }

    .add-cart {
        padding: 0.25rem 0.5rem;
    }
}

// Responsive
@media (max-width: 991px) {
    .parametric-catalog {
        .catalog-toolbar {
            flex-direction: column;
            align-items: stretch;
        }
    }

    .parametric-filter {
        .filter-row {
            flex-direction: column;
        }

        .filter-dropdown-content {
            position: static;
            box-shadow: none;
            border: none;
            margin-top: 0.5rem;
        }
    }
}

@media (max-width: 767px) {
    // Tabelle als Karten
    .product-table {
        thead {
            display: none;
        }

        tbody tr {
            display: block;
            margin-bottom: 1rem;
            border: 1px solid $border-color;
            border-radius: $border-radius;
            padding: 0.75rem;
        }

        td {
            display: flex;
            justify-content: space-between;
            padding: 0.375rem 0;
            border: none;
            white-space: normal;

            &::before {
                content: attr(data-label);
                font-weight: bold;
                margin-right: 1rem;
            }

            &:first-child,
            &:last-child {
                justify-content: flex-end;
            }
        }
    }

    // Listenansicht kompakter
    .product-list-item {
        .row > div {
            margin-bottom: 0.5rem;
        }
    }
}
```

## Verwendung

1. Datei als `_parametric-catalog.scss` speichern
2. In Haupt-SCSS importieren:

```scss
// meintheme.scss
@import "~bootstrap/scss/functions";
@import "variables";
@import "~templates/NOVA/themes/base/sass/allstyles";
@import "parametric-catalog";  // Hier importieren
```

3. Theme kompilieren im Backend

## Anpassung

### Farben ändern

```scss
// In _variables.scss vor dem Import
$catalog-header-border: $success;  // Andere Farbe für Header-Border
$filter-tag-bg: $info;             // Andere Farbe für Filter-Tags
```

### Filter-Dropdown breiter

```scss
.parametric-filter .filter-dropdown-content {
    min-width: 350px;
}
```

### Tabelle mit Zebra-Streifen

```scss
.product-table tbody tr:nth-child(odd) {
    background: $gray-50;
}
```
