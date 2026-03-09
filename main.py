"""
╔══════════════════════════════════════════════════════════════╗
║              main.py — Точка входу в додаток                ║
║                                                              ║
║           СКАРБНИЦЯ ЗНАНЬ v6.0 — Modular Edition            ║
║                                                              ║
║  Структура проєкту:                                         ║
║    main.py           — точка входу (цей файл)               ║
║    config.py         — тема, стилі, локалізація             ║
║    ui_components.py  — кастомні віджети                      ║
║    ui_main.py        — головне вікно (TreasuryApp)          ║
║    core_scraper.py   — бекенд (ScrapingWorker)              ║
╚══════════════════════════════════════════════════════════════╝
"""

import sys
import platform

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette, QColor

from config import Theme, GLOBAL_STYLESHEET
from ui_main import TreasuryApp


# ═══════════════════════════════════════════════════════════════
#              DPI AWARENESS (Windows 10/11)
# ═══════════════════════════════════════════════════════════════

try:
    if platform.system() == "Windows":
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass


# ═══════════════════════════════════════════════════════════════
#                     ТОЧКА ВХОДУ
# ═══════════════════════════════════════════════════════════════

def main():
    """Створює та запускає додаток"""
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # ── Глобальні стилі (QSS) ──
    app.setStyleSheet(GLOBAL_STYLESHEET)

    # ── Темна палітра на рівні Qt ──
    palette = QPalette()
    palette.setColor(
        QPalette.ColorRole.Window,
        QColor(Theme.BG_PRIMARY)
    )
    palette.setColor(
        QPalette.ColorRole.WindowText,
        QColor(Theme.TEXT_PRIMARY)
    )
    palette.setColor(
        QPalette.ColorRole.Base,
        QColor(Theme.BG_INPUT)
    )
    palette.setColor(
        QPalette.ColorRole.AlternateBase,
        QColor(Theme.BG_SECONDARY)
    )
    palette.setColor(
        QPalette.ColorRole.ToolTipBase,
        QColor(Theme.BG_CARD)
    )
    palette.setColor(
        QPalette.ColorRole.ToolTipText,
        QColor(Theme.GOLD)
    )
    palette.setColor(
        QPalette.ColorRole.Text,
        QColor(Theme.TEXT_PRIMARY)
    )
    palette.setColor(
        QPalette.ColorRole.Button,
        QColor(Theme.BG_CARD)
    )
    palette.setColor(
        QPalette.ColorRole.ButtonText,
        QColor(Theme.TEXT_PRIMARY)
    )
    palette.setColor(
        QPalette.ColorRole.Highlight,
        QColor(Theme.GOLD_DARK)
    )
    palette.setColor(
        QPalette.ColorRole.HighlightedText,
        QColor("white")
    )
    app.setPalette(palette)

    # ── Головне вікно ──
    window = TreasuryApp()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()