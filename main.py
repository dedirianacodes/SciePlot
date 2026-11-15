"""Scientific Figure Studio – publication-quality scientific figures without code.

Usage:
    python main.py [data_or_project_files ...]
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

os.environ.setdefault("MPLBACKEND", "Agg")          # we render off-screen; Qt shows the result
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def main() -> int:
    try:
        from PySide6.QtCore import Qt, QTimer
        from PySide6.QtGui import QGuiApplication, QIcon
        from PySide6.QtWidgets import QApplication
    except ImportError:
        print("PySide6 is required:  pip install -r requirements.txt", file=sys.stderr)
        return 1

    QGuiApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app = QApplication(sys.argv)
    app.setApplicationName("Scientific Figure Studio")
    app.setOrganizationName("ScientificFigureStudio")
    app.setWindowIcon(QIcon(str(ROOT / "assets" / "icons" / "app.svg")))

    from ui.main_window import MainWindow

    window = MainWindow()
    window.show()
    files = [a for a in sys.argv[1:] if Path(a).exists()]
    if files:
        QTimer.singleShot(0, lambda: [window.open_path(f) for f in files])
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
