<?php
/**
 * JTL-Shop 5 Child-Template Bootstrap with Parametric Catalog Support
 * Copy to: templates/YourTheme/Bootstrap.php
 * Update namespace to match your template folder name
 */
declare(strict_types=1);

namespace Template\YourTheme;  // ← Change to your template folder name

class Bootstrap extends \Template\NOVA\Bootstrap
{
    public function boot(): void
    {
        parent::boot();
        $this->handleViewSwitch();
        $this->handleExport();
    }
    
    /**
     * Handle AJAX view switch request
     */
    protected function handleViewSwitch(): void
    {
        if (!isset($_POST['io'])) return;
        
        $io = json_decode($_POST['io'], true);
        if ($io && ($io['name'] ?? '') === 'setCatalogView') {
            $view = $io['params'][0] ?? 'gallery';
            if (in_array($view, ['gallery', 'list', 'table'], true)) {
                $_SESSION['catalogView'] = $view;
            }
            header('Content-Type: application/json');
            echo json_encode(['success' => true, 'view' => $view]);
            exit;
        }
    }
    
    /**
     * Handle CSV/Excel export request
     */
    protected function handleExport(): void
    {
        if (($_GET['export'] ?? '') !== '1') return;
        
        $format = $_GET['format'] ?? 'csv';
        $filename = 'produkte_' . date('Y-m-d_H-i') . '.' . $format;
        
        header('Content-Type: text/csv; charset=utf-8');
        header('Content-Disposition: attachment; filename="' . $filename . '"');
        
        $out = fopen('php://output', 'w');
        
        // UTF-8 BOM for Excel
        fprintf($out, chr(0xEF) . chr(0xBB) . chr(0xBF));
        
        // Headers
        fputcsv($out, ['Artikelnummer', 'Name', 'Hersteller', 'Preis', 'Lagerbestand'], ';');
        
        // TODO: Get products from current category/filter
        // foreach ($products as $p) {
        //     fputcsv($out, [$p->cArtNr, $p->cName, $p->cHersteller, $p->Preise->fVKNetto, $p->fLagerbestand], ';');
        // }
        
        fclose($out);
        exit;
    }
}
