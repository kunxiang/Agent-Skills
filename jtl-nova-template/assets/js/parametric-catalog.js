/**
 * Parametric Product Catalog - JTL-Shop 5
 * Supports: Gallery / List / Table views with persistence
 */
class ParametricCatalog {
    constructor() {
        this.el = document.querySelector('.parametric-catalog');
        if (!this.el) return;
        this.view = this.el.dataset.view || 'gallery';
        this.compare = [];
        this.init();
    }

    init() {
        // View switching
        this.el.querySelectorAll('.view-btn').forEach(b => 
            b.addEventListener('click', () => this.switchView(b.dataset.view)));
        
        // Filter dropdowns
        this.el.querySelectorAll('[data-toggle="dropdown"]').forEach(btn => {
            btn.addEventListener('click', e => {
                e.stopPropagation();
                const dd = btn.nextElementSibling;
                this.el.querySelectorAll('.filter-dropdown-content.show').forEach(c => c !== dd && c.classList.remove('show'));
                dd.classList.toggle('show');
            });
        });
        document.addEventListener('click', () => 
            this.el.querySelectorAll('.filter-dropdown-content.show').forEach(c => c.classList.remove('show')));
        
        // Filter search
        this.el.querySelectorAll('.filter-search').forEach(inp => {
            inp.addEventListener('input', e => {
                const t = e.target.value.toLowerCase();
                e.target.parentElement.querySelectorAll('.filter-option').forEach(o => 
                    o.style.display = o.textContent.toLowerCase().includes(t) ? '' : 'none');
            });
        });
        
        // Auto-apply filters
        let tm;
        this.el.querySelectorAll('.filter-options input').forEach(cb => {
            cb.addEventListener('change', () => { clearTimeout(tm); tm = setTimeout(() => this.applyFilters(), 500); });
        });
        
        // Table sorting
        this.el.querySelectorAll('th.sortable').forEach(th => {
            th.addEventListener('click', () => {
                const key = th.dataset.sort, ord = th.dataset.order === 'asc' ? 'desc' : 'asc';
                this.el.querySelectorAll('th.sortable').forEach(h => h.dataset.order = '');
                th.dataset.order = ord;
                this.sortTable(key, ord);
            });
        });
        
        // Compare
        const cBtn = this.el.querySelector('#compareBtn'), cCnt = this.el.querySelector('#compareCount');
        this.el.querySelectorAll('.compare-cb').forEach(cb => {
            cb.addEventListener('change', e => {
                if (e.target.checked && this.compare.length < 4) this.compare.push(e.target.value);
                else if (e.target.checked) { e.target.checked = false; alert('Max 4'); return; }
                else this.compare = this.compare.filter(id => id !== e.target.value);
                if (cCnt) cCnt.textContent = this.compare.length;
                if (cBtn) cBtn.disabled = this.compare.length < 2;
            });
        });
        cBtn?.addEventListener('click', () => this.compare.length >= 2 && (location.href = `/vergleichsliste.php?a=${this.compare.join('_')}`));
        
        // Export
        this.el.querySelector('#exportBtn')?.addEventListener('click', () => {
            const p = new URLSearchParams(location.search);
            p.set('export', '1'); p.set('format', 'csv');
            location.href = `${location.pathname}?${p}`;
        });
        
        // Keyboard shortcuts
        document.addEventListener('keydown', e => {
            if (e.altKey && ['1','2','3'].includes(e.key)) {
                e.preventDefault();
                this.switchView(['gallery','list','table'][e.key-1]);
            }
        });
        
        this.switchView(this.view, false);
    }

    switchView(v, save = true) {
        this.el.querySelectorAll('.view-btn').forEach(b => b.classList.toggle('active', b.dataset.view === v));
        this.el.querySelectorAll('.catalog-view').forEach(c => c.style.display = 'none');
        this.el.querySelector(`.view-${v}`).style.display = '';
        const tt = this.el.querySelector('.table-tools');
        if (tt) tt.style.display = v === 'table' ? '' : 'none';
        this.view = v;
        if (save) {
            fetch('/io.php', { method: 'POST', headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                body: `io={"name":"setCatalogView","params":["${v}"]}` });
            localStorage.setItem('catalogView', v);
        }
    }

    applyFilters() {
        const f = document.createElement('form');
        f.method = 'GET'; f.action = location.pathname;
        this.el.querySelectorAll('.filter-options input:checked').forEach(cb => {
            const i = document.createElement('input');
            i.type = 'hidden'; i.name = cb.name; i.value = cb.value;
            f.appendChild(i);
        });
        document.body.appendChild(f); f.submit();
    }

    sortTable(key, ord) {
        const tb = this.el.querySelector('.product-table tbody');
        const rows = [...tb.querySelectorAll('tr')];
        rows.sort((a, b) => {
            let av, bv;
            if (key === 'price') { av = +a.dataset.price || 0; bv = +b.dataset.price || 0; }
            else if (key === 'stock') { av = +a.dataset.stock || 0; bv = +b.dataset.stock || 0; }
            else if (key === 'name') { av = a.cells[2].textContent.trim(); bv = b.cells[2].textContent.trim(); }
            else if (key.startsWith('param_')) {
                const id = key.slice(6);
                av = this.num(a.querySelector(`[data-merkmal="${id}"]`)?.textContent);
                bv = this.num(b.querySelector(`[data-merkmal="${id}"]`)?.textContent);
            }
            if (typeof av === 'string') return ord === 'asc' ? av.localeCompare(bv) : bv.localeCompare(av);
            return ord === 'asc' ? av - bv : bv - av;
        });
        rows.forEach(r => tb.appendChild(r));
    }

    num(s) { if (!s) return 0; const m = s.match(/[\d.,]+/); return m ? parseFloat(m[0].replace(',', '.')) : 0; }
}

document.addEventListener('DOMContentLoaded', () => new ParametricCatalog());
