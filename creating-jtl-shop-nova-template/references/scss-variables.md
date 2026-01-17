# SCSS Variables Reference

## Theme-Struktur

```
templates/MeinTheme/
└── themes/
    └── my-nova/                    # Theme-Ordner
        ├── custom.css              # Fertig kompiliertes CSS (optional)
        └── sass/
            ├── _variables.scss     # Variable Überschreibungen
            └── my-nova.scss        # Haupt-SCSS Datei
            └── my-nova_crit.scss   # Critical CSS (above-fold)
```

## Import-Reihenfolge (WICHTIG!)

```scss
// my-nova.scss
@import "~bootstrap/scss/functions";
@import "variables";                                    // 1. ZUERST eigene Variablen
@import "~templates/NOVA/themes/base/sass/allstyles";  // 2. DANN NOVA-Stile laden
// 3. Eigene Stile UNTEN hinzufügen
```

**Falsche Reihenfolge** = Variablen werden ignoriert!

## File Locations

| File | Purpose |
|------|---------|
| `NOVA/themes/base/sass/_variables.scss` | NOVA defaults |
| `bootstrap/scss/_variables.scss` | Bootstrap defaults |
| `MeinTheme/themes/my-nova/sass/_variables.scss` | Your overrides |

## Colors

```scss
// Primary colors
$primary: #007bff;
$secondary: #6c757d;
$success: #28a745;
$info: #17a2b8;
$warning: #ffc107;
$danger: #dc3545;
$light: #f8f9fa;
$dark: #343a40;

// Grayscale
$white: #fff;
$gray-100: #f8f9fa;
$gray-200: #e9ecef;
$gray-300: #dee2e6;
$gray-400: #ced4da;
$gray-500: #adb5bd;
$gray-600: #6c757d;
$gray-700: #495057;
$gray-800: #343a40;
$gray-900: #212529;
$black: #000;

// Theme colors map
$theme-colors: (
    "primary": $primary,
    "secondary": $secondary,
    "success": $success,
    "info": $info,
    "warning": $warning,
    "danger": $danger,
    "light": $light,
    "dark": $dark
);

// Body
$body-bg: $white;
$body-color: $gray-900;
```

## Typography

```scss
// Font families
$font-family-sans-serif: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
$font-family-monospace: SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
$font-family-base: $font-family-sans-serif;

// Font sizes
$font-size-base: 1rem;      // 16px
$font-size-lg: 1.25rem;     // 20px
$font-size-sm: 0.875rem;    // 14px
$h1-font-size: 2.5rem;      // 40px
$h2-font-size: 2rem;        // 32px
$h3-font-size: 1.75rem;     // 28px
$h4-font-size: 1.5rem;      // 24px
$h5-font-size: 1.25rem;     // 20px
$h6-font-size: 1rem;        // 16px

// Font weights
$font-weight-light: 300;
$font-weight-normal: 400;
$font-weight-bold: 700;
$font-weight-base: $font-weight-normal;
$headings-font-weight: 500;

// Line height
$line-height-base: 1.5;
$line-height-sm: 1.25;
$line-height-lg: 2;
```

## Spacing

```scss
$spacer: 1rem;

$spacers: (
    0: 0,
    1: ($spacer * 0.25),    // 4px
    2: ($spacer * 0.5),     // 8px
    3: $spacer,             // 16px
    4: ($spacer * 1.5),     // 24px
    5: ($spacer * 3)        // 48px
);
```

## Grid & Layout

```scss
// Breakpoints
$grid-breakpoints: (
    xs: 0,
    sm: 576px,
    md: 768px,
    lg: 992px,
    xl: 1200px
);

// Containers
$container-max-widths: (
    sm: 540px,
    md: 720px,
    lg: 960px,
    xl: 1140px
);

// Grid
$grid-columns: 12;
$grid-gutter-width: 30px;
```

## Components

```scss
// Borders
$border-width: 1px;
$border-color: $gray-300;
$border-radius: 0.25rem;
$border-radius-lg: 0.3rem;
$border-radius-sm: 0.2rem;

// Shadows
$box-shadow-sm: 0 0.125rem 0.25rem rgba($black, 0.075);
$box-shadow: 0 0.5rem 1rem rgba($black, 0.15);
$box-shadow-lg: 0 1rem 3rem rgba($black, 0.175);

// Transitions
$transition-base: all 0.2s ease-in-out;
$transition-fade: opacity 0.15s linear;
```

## Buttons

```scss
$btn-padding-y: 0.375rem;
$btn-padding-x: 0.75rem;
$btn-font-size: $font-size-base;
$btn-line-height: $line-height-base;
$btn-border-radius: $border-radius;

// Button variants generated from $theme-colors
```

## Forms

```scss
$input-padding-y: 0.375rem;
$input-padding-x: 0.75rem;
$input-font-size: $font-size-base;
$input-line-height: $line-height-base;
$input-bg: $white;
$input-border-color: $gray-400;
$input-border-radius: $border-radius;
$input-focus-border-color: lighten($primary, 25%);
$input-focus-box-shadow: 0 0 0 0.2rem rgba($primary, 0.25);
$input-placeholder-color: $gray-600;
```

## NOVA-Specific Variables

```scss
// Header
$header-bg: $white;
$header-border-color: $border-color;
$nav-link-color: $gray-700;
$nav-link-hover-color: $primary;

// Product cards
$product-card-border: 1px solid $border-color;
$product-card-shadow: $box-shadow-sm;
$product-card-hover-shadow: $box-shadow;

// Prices
$price-color: $primary;
$price-old-color: $gray-500;
$price-special-color: $danger;

// Badges
$badge-new-bg: $success;
$badge-sale-bg: $danger;

// Footer
$footer-bg: $gray-800;
$footer-color: $gray-300;
```

## Override Example

```scss
// _variables.scss
$primary: #e63946;           // Primärfarbe ändern - wirkt auf viele Elemente
$secondary: #457b9d;
$font-family-base: 'Open Sans', sans-serif;
$border-radius: 0;           // Eckige Buttons/Inputs
$btn-border-radius: 0;
$input-border-radius: 0;

// Custom variables
$header-height: 80px;
$sidebar-width: 280px;
```

## Theme kompilieren

1. **JTL Theme-Editor aktivieren**: Backend → Plugins → JTL Theme-Editor
2. **Theme-Editor öffnen**: Plugin → Einstellungen
3. **Theme auswählen**: Dropdown oben links
4. **Datei bearbeiten**: _variables.scss oder Haupt-SCSS
5. **Speichern**: "Datei speichern"
6. **Kompilieren**: "Theme kompilieren" (oben rechts)

**Nach Änderungen immer**:
- Template-Cache leeren (Backend → Einstellungen → Template Cache)
- Browser-Cache leeren (Strg+F5)
