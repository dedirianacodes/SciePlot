# Scientific Figure Studio

A native desktop application (PySide6 + Matplotlib) for turning CSV/TSV/TXT/XLSX
data into publication-ready figures for high-impact journals — without writing code.

![Example 2×2 figure (Optics Express style)](docs/example_2x2_optics_express.png)

## Install & run

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate      macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python main.py                        # or: python main.py examples/spectrum.csv
```

Python 3.12+ recommended. Try the files in `examples/` – each one exercises a
different importer path and plot recommendation.

## Workflow (< 5 minutes)

1. **Drop a file** on the window (or Ctrl+O). Delimiter, decimal comma, comment
   lines, header row, unit row and numeric columns are detected automatically.
2. The **Smart Figure Assistant** proposes a plot and configures the panel
   instantly (e.g. *Angle + Intensity → Polar*, *x, y, z grid → Heatmap/Contour*,
   *exp/sim columns → Scatter + Line overlay*, *err/std columns → Error bars*).
3. Adjust in the right-hand **Plot / Style / Analysis / Export** tabs – the
   preview updates live at true journal size (WYSIWYG page view).
4. Press **★ Q1 Journal Figure** (Ctrl+J).
5. **Export** (Ctrl+E) as PDF/SVG/EPS/TIFF/PNG at 300/600/1200 dpi, or write a
   whole submission package (PDF + EPS + 600 dpi TIFF + PNG preview).

## Features

| Area | What you get |
|---|---|
| Layout | Data explorer (left), live figure (centre), settings (right), data table / statistics / quality report / log (bottom). All docks movable, floatable, restorable. |
| Import | CSV, TSV, TXT/DAT (whitespace), XLSX (every sheet becomes a dataset). Units parsed from `Name (unit)`, `Name [unit]`, `Name / unit`, `name_unit` or a separate unit row. |
| Plots | Line, Scatter, Scatter + Line overlay (exp. vs sim.), Error bar, Bar, Histogram, Box, Heatmap, Contour, Polar, 3D Surface. |
| Multi-panel | 1×1, 1×2, 2×1, 1×3, 2×2, 2×3, 3×2, 3×3 – each panel has its own data & type; (a)(b)(c)… labels aligned to the panel edges. Click a panel in the preview to edit it. |
| Journal styles | Nature, Science, IEEE, APS, Optics Express, Applied Optics, Advanced Materials, Generic. Each sets column widths, fonts, sizes, tick style, line/marker widths, panel-label format and a colour-blind-safe palette. |
| Fitting | Linear, Polynomial, Exponential, Gaussian, Lorentzian – parameters ± standard errors, R², RMSE, FWHM/area; optional fit x-range. |
| Peaks | Detection with prominence/distance, FWHM, baseline-corrected area, optional annotation. |
| Processing | Savitzky–Golay, moving average, ALS & polynomial baseline subtraction, normalisation (max, min–max, area, z-score), interpolation (linear/cubic/PCHIP), derivative. Results become new columns – originals are never modified. |
| Quality checker | Runs after every change: missing labels/units, fonts below journal minimum, legend covering data, too many curves/colours, low-contrast colours, non-uniform colormaps, thin lines, text outside the figure, width beyond journal limits, insufficient dpi. Score 0–100. |
| Q1 button | Journal column width & aspect, journal fonts/line widths, inward/outward & mirrored ticks with minor ticks and ≤5 major ticks, colour-blind palette, open markers for experimental data, removes chartjunk (grid, single-entry legends), panel labels, and moves legends to the position with zero data overlap (or outside). Fully undoable. |
| Export | Vector PDF/SVG/EPS with editable text (TrueType fonts), LZW-compressed RGB TIFF, PNG; transparent background option. |
| Other | Undo/redo, projects (`.sfsproj`, data embedded), recent files, copy figure to clipboard, dark mode (the figure paper stays white), drag & drop, keyboard shortcuts (F1). |

## Keyboard shortcuts

| Keys | Action |
|---|---|
| Ctrl+O / Ctrl+Shift+O | Open data / open project |
| Ctrl+S / Ctrl+Shift+S | Save project / save as |
| Ctrl+E / Ctrl+Shift+E | Export / quick re-export |
| Ctrl+Shift+C | Copy figure (300 dpi PNG) |
| Ctrl+J | ★ Q1 Journal Figure |
| F7 | Quality check |
| Ctrl+1 … Ctrl+9, Ctrl+0, Ctrl+Shift+0 | Plot types (line … contour, polar, surface) |
| Ctrl+PgDown / Ctrl+PgUp | Next / previous panel |
| Ctrl+= / Ctrl+- / Ctrl+Shift+F / Ctrl+Shift+1 | Zoom in / out / fit / 100 % (also Ctrl+wheel) |
| Ctrl+Z / Ctrl+Y | Undo / redo |
| Ctrl+D | Dark mode |
| F5 / F1 | Redraw / shortcut list |

## Architecture

```
main.py                  entry point
ui/
  main_window.py         window, docks, menus, actions, render loop, undo/redo, D&D
  plot_canvas.py         WYSIWYG page preview (Agg → QPixmap), zoom, hover read-out, panel picking
  panels.py              data explorer, plot/style/analysis/export settings, data preview
core/                    Qt-free engine (unit-testable, usable from scripts)
  models.py              FigureSpec / PanelSpec dataclasses (JSON-serialisable)
  data_manager.py        importer (delimiter/header/unit detection) + dataset store
  style_manager.py       journal styles, palettes, rcParams
  plot_manager.py        renderers for every plot type
  figure_builder.py      spec → Matplotlib figure (layout, labels, legends, fits, panel letters)
  quality_checker.py     publication-readiness analysis
  optimizer.py           ★ Q1 Journal Figure
  recommender.py         Smart Figure Assistant
  export_manager.py      PNG/SVG/PDF/EPS/TIFF export, submission package
  project_io.py          .sfsproj save/load
analysis/
  fitting.py  peak_analysis.py  processing.py
assets/icons, assets/themes   SVG icons, light/dark QSS
examples/                sample datasets
tests/test_core.py       headless tests (python tests/test_core.py)
```

The same `FigureBuilder` produces the preview, the exports and the quality
analysis, so the exported file matches what you see. Layout is computed once
(constrained layout) and then frozen, so the figure keeps its exact journal width.

### Scripting

```python
from core.data_manager import DataManager
from core.figure_builder import FigureBuilder
from core.export_manager import ExportManager
from core.models import FigureSpec, PanelSpec

dm = DataManager(); ds = dm.load_file("examples/spectrum.csv")[0]
spec = FigureSpec(journal="APS", panels=[PanelSpec("line", ds.id, x=ds.columns[0], y=[ds.columns[1]])])
ExportManager(FigureBuilder(dm)).export(spec, "fig.pdf")
```

## Notes

- Journal dimensions and fonts follow publicly available author guidelines;
  publishers revise them occasionally, so confirm current requirements before submission.
- Arial/Helvetica/Times are used when installed; otherwise metric-compatible
  fallbacks (Liberation, Nimbus, TeX Gyre) or DejaVu are used.
- `pyqtgraph` is not required: the preview renders with Matplotlib's Agg backend
  so the on-screen figure is identical to the exported one.
