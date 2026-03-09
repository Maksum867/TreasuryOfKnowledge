"""
╔══════════════════════════════════════════════════════════════╗
║          ui_main.py — Головне вікно додатку                  ║
║                                                              ║
║  Клас TreasuryApp (QMainWindow)                             ║
║  5 екранів: Main, Settings, About, HowItWorks, Features    ║
║  Системний трей, пасхалки, навігація                        ║
╚══════════════════════════════════════════════════════════════╝
"""

# ═══════════════════════════════════════════════════════════════
#                        ІМПОРТИ
# ═══════════════════════════════════════════════════════════════

import os
import json
import time
import webbrowser
import urllib.parse

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTextEdit, QProgressBar, QStackedWidget,
    QScrollArea, QFileDialog, QMessageBox,
    QGraphicsDropShadowEffect, QSystemTrayIcon, QMenu,
    QPushButton,
)
from PyQt6.QtCore import (
    Qt, QTimer,
)
from PyQt6.QtGui import (
    QFont, QColor, QIcon, QPainter, QBrush, QPen,
    QCursor, QPixmap,
)

# ── Буфер обміну ──
try:
    import pyperclip
except ImportError:
    pyperclip = None

# ── Локальні імпорти ──
from config import (
    Theme, GLOBAL_STYLESHEET, LOCALES,
    DEFAULT_SETTINGS, CONFIG_FILE,
)
from ui_components import (
    NoScrollComboBox, NoScrollSlider,
    GoldButton, PrimaryButton, DangerButton,
    IconButton, FeatureButton,
    CardFrame, SectionLabel, GoldSectionLabel, MutedLabel,
    ToggleSwitch,
)
from core_scraper import ScrapingWorker


# ═══════════════════════════════════════════════════════════════
#                     ГОЛОВНЕ ВІКНО
# ═══════════════════════════════════════════════════════════════

class TreasuryApp(QMainWindow):
    """Головне вікно додатку Скарбниця Знань"""

    def __init__(self):
        super().__init__()

        # ── Конфігурація вікна ──
        self.setWindowTitle("Скарбниця Знань v6.1")
        self.setMinimumSize(1000, 900)
        self.resize(1000, 900)

        try:
            self.setWindowIcon(QIcon("icon.ico"))
        except Exception:
            pass

        # ── Лічильники пасхалок ──
        self.temple_clicks = 0
        self.title_clicks = 0
        self.empty_clicks = 0
        self.about_clicks = 0
        self.theme_clicks = 0
        self.theme_click_time = 0
        self.format_clicks = 0
        self.format_click_time = 0
        self.bilingual_clicks = 0
        self.bilingual_click_time = 0
        self.font_slider_clicks = 0
        self.cancel_folder_clicks = 0
        self.hacker_mode = False
        self.start_process_time = 0

        # ── Воркер ──
        self.worker = None
        self.is_processing = False

        # ── Стан додатку ──
        self.state = self._load_settings()

        # ── Стилі ──
        self.setStyleSheet(GLOBAL_STYLESHEET)

        # ── Центральний стек екранів ──
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.stacked = QStackedWidget()
        self.main_layout.addWidget(self.stacked)

        # ── Створення екранів ──
        self.main_screen = self._build_main_screen()
        self.settings_screen = self._build_settings_screen()
        self.about_screen = self._build_about_screen()
        self.how_it_works_screen = self._build_info_screen(
            self.t("how_it_works_title"),
            self.t("how_it_works_text"),
            back_target="about"
        )
        self.features_screen = self._build_info_screen(
            self.t("features_title"),
            self.t("features_text"),
            back_target="about"
        )

        self.stacked.addWidget(self.main_screen)         # index 0
        self.stacked.addWidget(self.settings_screen)      # index 1
        self.stacked.addWidget(self.about_screen)         # index 2
        self.stacked.addWidget(self.how_it_works_screen)  # index 3
        self.stacked.addWidget(self.features_screen)      # index 4

        self.stacked.setCurrentIndex(0)

        # ── Системний трей ──
        self._setup_tray()

    # ═══════════════════════════════════════════════════════════
    #                 SETTINGS (load / save)
    # ═══════════════════════════════════════════════════════════

    def _load_settings(self):
        """Завантажує налаштування з файлу або повертає дефолтні"""
        defaults = DEFAULT_SETTINGS.copy()
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    return {**defaults, **loaded}
            except Exception:
                return defaults
        return defaults

    def _save_settings(self):
        """Зберігає поточні налаштування у файл"""
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.state, f, ensure_ascii=False, indent=4)
        except Exception:
            pass

    # ═══════════════════════════════════════════════════════════
    #                       ХЕЛПЕРИ
    # ═══════════════════════════════════════════════════════════

    def t(self, key):
        """Отримати переклад ключа локалізації"""
        lang = self.state.get("ui_language", "uk")
        return LOCALES.get(lang, LOCALES["uk"]).get(key, key)

    def navigate(self, screen_name):
        """Навігація між екранами"""
        mapping = {
            "main": 0,
            "settings": 1,
            "about": 2,
            "how_it_works": 3,
            "features": 4,
        }
        idx = mapping.get(screen_name, 0)
        self.stacked.setCurrentIndex(idx)

    def is_valid_url(self, url):
        """Перевіряє валідність URL"""
        parsed = urllib.parse.urlparse(url)
        return all([parsed.scheme in ['http', 'https'], parsed.netloc])

    # ═══════════════════════════════════════════════════════════
    #               ЕКРАН 1: ГОЛОВНИЙ ЕКРАН
    # ═══════════════════════════════════════════════════════════

    def _build_main_screen(self):
        screen = QWidget()
        screen.setStyleSheet(f"background-color: {Theme.BG_PRIMARY};")
        layout = QVBoxLayout(screen)
        layout.setContentsMargins(40, 20, 40, 30)
        layout.setSpacing(0)

        # ── Верхня панель: кнопка налаштувань ──
        top_bar = QHBoxLayout()
        top_bar.addStretch()
        settings_btn = IconButton("⚙️", size=50, font_size=30)
        settings_btn.setToolTip(self.t("settings_title"))
        settings_btn.clicked.connect(lambda: self.navigate("settings"))
        top_bar.addWidget(settings_btn)
        layout.addLayout(top_bar)

        layout.addSpacing(15)

        # ── Іконка-логотип з пасхалкою ──
        temple_label = QLabel("🏛️")
        temple_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        temple_label.setFont(QFont("Arial", 42))
        temple_label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        temple_label.mousePressEvent = self._on_temple_click
        layout.addWidget(temple_label)

        layout.addSpacing(5)

        # ── Заголовок з пасхалкою ──
        self.main_title_label = QLabel(self.t("title").split(" v")[0])
        self.main_title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_title_label.setFont(
            QFont(Theme.FONT_TITLE, 52, QFont.Weight.Bold)
        )
        self.main_title_label.setStyleSheet(f"color: {Theme.GOLD};")
        self.main_title_label.setCursor(
            QCursor(Qt.CursorShape.PointingHandCursor)
        )
        self.main_title_label.mousePressEvent = self._on_title_click
        layout.addWidget(self.main_title_label)

        # ── Підзаголовок (версія) ──
        version_label = QLabel("v6.1")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version_label.setFont(QFont(Theme.FONT_UI, 14))
        version_label.setStyleSheet(f"color: {Theme.TEXT_MUTED};")
        layout.addWidget(version_label)

        layout.addSpacing(25)

        # ── Поле вводу URL ──
        self.url_textbox = QTextEdit()
        self.url_textbox.setPlaceholderText(self.t("placeholder"))
        self.url_textbox.setFixedHeight(120)
        self.url_textbox.setFont(QFont(Theme.FONT_UI, 15))

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(212, 175, 55, 40))
        shadow.setOffset(0, 4)
        self.url_textbox.setGraphicsEffect(shadow)
        layout.addWidget(self.url_textbox)

        layout.addSpacing(15)

        # ── Прогресбар ──
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(12)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        layout.addSpacing(10)

        # ── Статус ──
        self.status_label = QLabel(self.t("status_wait"))
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setFont(QFont(Theme.FONT_UI, 16))
        self.status_label.setStyleSheet(
            f"color: {Theme.TEXT_SECONDARY}; font-style: italic;"
        )
        layout.addWidget(self.status_label)

        layout.addSpacing(25)

        # ── Кнопки дій ──
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(16)

        self.save_btn = PrimaryButton(self.t("btn_digitize"))
        self.save_btn.setFixedWidth(380)
        self.save_btn.add_shadow()
        self.save_btn.clicked.connect(self._on_digitize_click)
        buttons_layout.addWidget(self.save_btn)

        self.cancel_btn = DangerButton(self.t("btn_cancel"))
        self.cancel_btn.setFixedWidth(200)
        self.cancel_btn.setEnabled(False)
        self.cancel_btn.clicked.connect(self._on_cancel_click)
        buttons_layout.addWidget(self.cancel_btn)

        buttons_container = QWidget()
        buttons_container.setLayout(buttons_layout)
        layout.addWidget(
            buttons_container, alignment=Qt.AlignmentFlag.AlignCenter
        )

        layout.addStretch()

        # ── Футер ──
        footer_label = QLabel("Made with ❤️ for free access to knowledge")
        footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer_label.setFont(QFont(Theme.FONT_UI, 11))
        footer_label.setStyleSheet(f"color: {Theme.TEXT_MUTED};")
        layout.addWidget(footer_label)

        return screen

    # ═══════════════════════════════════════════════════════════
    #              ЕКРАН 2: НАЛАШТУВАННЯ
    # ═══════════════════════════════════════════════════════════

    def _build_settings_screen(self):
        screen = QWidget()
        screen.setStyleSheet(f"background-color: {Theme.BG_PRIMARY};")
        outer_layout = QVBoxLayout(screen)
        outer_layout.setContentsMargins(40, 20, 40, 20)

        # ── Верхня панель ──
        top_bar = QHBoxLayout()
        back_btn = IconButton("←", size=50, font_size=34)
        back_btn.clicked.connect(lambda: self.navigate("main"))
        top_bar.addWidget(back_btn)
        top_bar.addStretch()

        title = QLabel(self.t("settings_title"))
        title.setFont(QFont(Theme.FONT_TITLE, 30, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {Theme.GOLD};")
        top_bar.addWidget(title)
        top_bar.addStretch()
        top_bar.addSpacing(50)
        outer_layout.addLayout(top_bar)

        outer_layout.addSpacing(10)

        # ── Скролабельна область ──
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(60, 10, 60, 30)
        scroll_layout.setSpacing(12)

        # ── Мова інтерфейсу ──
        scroll_layout.addWidget(SectionLabel(self.t("ui_lang_lbl")))
        self.ui_lang_combo = NoScrollComboBox()
        self.ui_lang_combo.addItems([
            "Українська", "English", "Ельфійська (Sindarin)"
        ])
        current_lang = (
            "Українська" if self.state["ui_language"] == "uk" else "English"
        )
        self.ui_lang_combo.setCurrentText(current_lang)
        self.ui_lang_combo.currentTextChanged.connect(self._on_ui_lang_changed)
        scroll_layout.addWidget(self.ui_lang_combo)

        scroll_layout.addSpacing(8)

        # ── Мова перекладу ──
        scroll_layout.addWidget(SectionLabel(self.t("target_lang_lbl")))
        self.target_combo = NoScrollComboBox()
        self.target_combo.addItems([
            "Українська", "English", "Polski",
            "Deutsch", "Français", "Español"
        ])
        self.target_combo.setCurrentText(
            self.state.get("target_lang_name", "Українська")
        )
        self.target_combo.currentTextChanged.connect(
            lambda v: self._update_state("target_lang_name", v)
        )
        scroll_layout.addWidget(self.target_combo)

        scroll_layout.addSpacing(8)

        # ── Рушій перекладу ──
        scroll_layout.addWidget(SectionLabel(self.t("engine_lbl")))
        self.engine_combo = NoScrollComboBox()
        self.engine_combo.addItems([
            "Google Translator", "Microsoft Translator", "Skynet v2.0"
        ])
        self.engine_combo.setCurrentText(
            self.state.get("translation_engine", "Google Translator")
        )
        self.engine_combo.currentTextChanged.connect(self._on_engine_changed)
        scroll_layout.addWidget(self.engine_combo)

        scroll_layout.addSpacing(8)

        # ── Папка збереження ──
        scroll_layout.addWidget(SectionLabel(self.t("path_lbl")))
        path_row = QHBoxLayout()
        self.path_display = QLabel(self.state["save_path"])
        self.path_display.setFont(QFont(Theme.FONT_UI, 13))
        self.path_display.setStyleSheet(f"""
            color: {Theme.TEXT_SECONDARY};
            background-color: {Theme.BG_INPUT};
            border: 1px solid {Theme.BORDER};
            border-radius: 10px;
            padding: 10px 14px;
        """)
        self.path_display.setWordWrap(True)
        path_row.addWidget(self.path_display, stretch=1)

        browse_btn = GoldButton(self.t("btn_choose"))
        browse_btn.setFixedWidth(150)
        browse_btn.setFixedHeight(42)
        browse_btn.clicked.connect(self._on_browse_folder)
        path_row.addWidget(browse_btn)
        scroll_layout.addLayout(path_row)

        scroll_layout.addSpacing(8)

        # ── Шрифт ──
        scroll_layout.addWidget(SectionLabel(self.t("font_lbl")))
        self.font_combo = NoScrollComboBox()
        self.font_combo.addItems([
            "Georgia", "Arial", "Times New Roman", "Comic Sans MS"
        ])
        self.font_combo.setCurrentText(
            self.state.get("font_family", "Georgia")
        )
        self.font_combo.currentTextChanged.connect(self._on_font_changed)
        scroll_layout.addWidget(self.font_combo)

        scroll_layout.addSpacing(8)

        # ── Формат ──
        scroll_layout.addWidget(SectionLabel(self.t("format_lbl")))
        self.format_combo = NoScrollComboBox()
        self.format_combo.addItems(["docx", "pdf"])
        self.format_combo.setCurrentText(
            self.state.get("output_format", "docx")
        )
        self.format_combo.currentTextChanged.connect(self._on_format_changed)
        scroll_layout.addWidget(self.format_combo)

        scroll_layout.addSpacing(8)

        # ── Розмір тексту (слайдер) ──
        size_row = QHBoxLayout()
        size_row.addWidget(SectionLabel(self.t("size_lbl")))
        size_row.addStretch()
        self.size_value_label = QLabel(str(self.state["font_size"]))
        self.size_value_label.setFont(
            QFont(Theme.FONT_UI, 18, QFont.Weight.Bold)
        )
        self.size_value_label.setStyleSheet(f"color: {Theme.GOLD};")
        size_row.addWidget(self.size_value_label)
        scroll_layout.addLayout(size_row)

        size_slider = NoScrollSlider(Qt.Orientation.Horizontal)
        size_slider.setRange(12, 24)
        size_slider.setValue(self.state["font_size"])
        size_slider.setTickInterval(1)
        size_slider.valueChanged.connect(self._on_font_size_changed)
        scroll_layout.addWidget(size_slider)

        scroll_layout.addSpacing(16)

        # ── Додаткові функції (Toggle Switches) ──
        scroll_layout.addWidget(
            GoldSectionLabel(self.t("additional_features_lbl"))
        )

        self.toggle_read_time = ToggleSwitch(
            self.t("setting_read_time"), self.state["add_read_time"]
        )
        self.toggle_read_time.toggled.connect(
            lambda v: self._update_state("add_read_time", v)
        )
        scroll_layout.addWidget(self.toggle_read_time)

        self.toggle_toc = ToggleSwitch(
            self.t("setting_toc"), self.state["add_toc"]
        )
        self.toggle_toc.toggled.connect(
            lambda v: self._update_state("add_toc", v)
        )
        scroll_layout.addWidget(self.toggle_toc)

        self.toggle_metadata = ToggleSwitch(
            self.t("setting_metadata"), self.state["add_metadata"]
        )
        self.toggle_metadata.toggled.connect(
            lambda v: self._update_state("add_metadata", v)
        )
        scroll_layout.addWidget(self.toggle_metadata)

        self.toggle_bilingual = ToggleSwitch(
            self.t("setting_bilingual"), self.state["bilingual_mode"]
        )
        self.toggle_bilingual.toggled.connect(self._on_bilingual_toggled)
        scroll_layout.addWidget(self.toggle_bilingual)

        self.toggle_images = ToggleSwitch(
            self.t("setting_images"), self.state["download_images"]
        )
        self.toggle_images.toggled.connect(
            lambda v: self._update_state("download_images", v)
        )
        scroll_layout.addWidget(self.toggle_images)

        self.toggle_auto_open = ToggleSwitch(
            self.t("setting_auto_open"), self.state["auto_open"]
        )
        self.toggle_auto_open.toggled.connect(
            lambda v: self._update_state("auto_open", v)
        )
        scroll_layout.addWidget(self.toggle_auto_open)

        self.toggle_tray = ToggleSwitch(
            self.t("setting_tray_close"), self.state["minimize_to_tray"]
        )
        self.toggle_tray.toggled.connect(
            lambda v: self._update_state("minimize_to_tray", v)
        )
        scroll_layout.addWidget(self.toggle_tray)

        scroll_layout.addSpacing(20)

        # ── Тема ──
        scroll_layout.addWidget(SectionLabel(self.t("theme_lbl")))
        self.toggle_theme = ToggleSwitch(
            "🌙 " + self.t("theme_dark"),
            self.state["theme"] == "dark"
        )
        self.toggle_theme.toggled.connect(self._on_theme_toggled)
        scroll_layout.addWidget(self.toggle_theme)

        scroll_layout.addSpacing(30)

        about_btn = GoldButton(self.t("btn_about"))
        about_btn.setMinimumWidth(250)
        about_btn.clicked.connect(lambda: self.navigate("about"))
        scroll_layout.addWidget(
            about_btn, alignment=Qt.AlignmentFlag.AlignCenter
        )

        scroll_layout.addSpacing(20)

        # ── Premium Easter Egg ──
        premium_btn = QPushButton("v6.1 👑")
        premium_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        premium_btn.setFont(QFont(Theme.FONT_UI, 11))
        premium_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: {Theme.TEXT_MUTED};
                border: none;
            }}
            QPushButton:hover {{
                color: {Theme.GOLD};
            }}
        """)
        premium_btn.clicked.connect(self._show_premium_joke)
        scroll_layout.addWidget(
            premium_btn, alignment=Qt.AlignmentFlag.AlignCenter
        )

        scroll_layout.addSpacing(20)

        scroll_area.setWidget(scroll_content)
        outer_layout.addWidget(scroll_area)

        return screen

    # ═══════════════════════════════════════════════════════════
    #              ЕКРАН 3: ПРО ДОДАТОК
    # ═══════════════════════════════════════════════════════════

    def _build_about_screen(self):
        screen = QWidget()
        screen.setStyleSheet(f"background-color: {Theme.BG_PRIMARY};")
        layout = QVBoxLayout(screen)
        layout.setContentsMargins(50, 20, 50, 30)

        # ── Верхня панель ──
        top_bar = QHBoxLayout()
        back_btn = IconButton("←", size=50, font_size=34)
        back_btn.clicked.connect(lambda: self.navigate("settings"))
        top_bar.addWidget(back_btn)
        top_bar.addStretch()
        outer_title = QLabel(self.t("about_title"))
        outer_title.setFont(QFont(Theme.FONT_TITLE, 30, QFont.Weight.Bold))
        outer_title.setStyleSheet(f"color: {Theme.GOLD};")
        top_bar.addWidget(outer_title)
        top_bar.addStretch()
        top_bar.addSpacing(50)
        layout.addLayout(top_bar)

        layout.addSpacing(15)

        # ── Іконка ──
        icon_lbl = QLabel("🏛️")
        icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_lbl.setFont(QFont("Arial", 55))
        layout.addWidget(icon_lbl)

        layout.addSpacing(10)

        # ── Опис ──
        desc_label = QLabel(self.t("about_desc"))
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setFont(QFont(Theme.FONT_UI, 14))
        desc_label.setStyleSheet(
            f"color: {Theme.TEXT_SECONDARY}; line-height: 1.6;"
        )
        desc_label.setWordWrap(True)
        desc_label.setMaximumWidth(750)
        desc_label.setMinimumHeight(150)
        layout.addWidget(
            desc_label, alignment=Qt.AlignmentFlag.AlignCenter
        )

        layout.addSpacing(30)

        # ── Перший ряд кнопок ──
        row1 = QHBoxLayout()
        row1.setSpacing(12)

        btn_how = FeatureButton(
            self.t("btn_how_it_works"),
            Theme.BLUE, Theme.BLUE_HOVER
        )
        btn_how.clicked.connect(lambda: self.navigate("how_it_works"))
        row1.addWidget(btn_how)

        btn_features = FeatureButton(
            self.t("btn_features"),
            Theme.GREEN, Theme.GREEN_HOVER
        )
        btn_features.clicked.connect(lambda: self.navigate("features"))
        row1.addWidget(btn_features)

        row1_wrapper = QWidget()
        row1_wrapper.setLayout(row1)
        layout.addWidget(
            row1_wrapper, alignment=Qt.AlignmentFlag.AlignCenter
        )

        layout.addSpacing(10)

        # ── Другий ряд кнопок ──
        row2 = QHBoxLayout()
        row2.setSpacing(12)

        btn_donate = FeatureButton(
            self.t("btn_donate"),
            Theme.ORANGE, Theme.ORANGE_HOVER
        )
        btn_donate.clicked.connect(self._on_donate_click)
        row2.addWidget(btn_donate)

        btn_feedback = FeatureButton(
            self.t("btn_feedback"),
            "#4b4b4b", Theme.BG_HOVER
        )
        btn_feedback.clicked.connect(self._on_feedback_click)
        row2.addWidget(btn_feedback)

        row2_wrapper = QWidget()
        row2_wrapper.setLayout(row2)
        layout.addWidget(
            row2_wrapper, alignment=Qt.AlignmentFlag.AlignCenter
        )

        layout.addStretch()

        return screen

    # ═══════════════════════════════════════════════════════════
    #     ЕКРАНИ 4-5: ІНФОРМАЦІЙНІ (How it works / Features)
    # ═══════════════════════════════════════════════════════════

    def _build_info_screen(self, title_text, body_text, back_target="about"):
        screen = QWidget()
        screen.setStyleSheet(f"background-color: {Theme.BG_PRIMARY};")
        layout = QVBoxLayout(screen)
        layout.setContentsMargins(40, 20, 40, 30)

        # ── Верхня панель ──
        top_bar = QHBoxLayout()
        back_btn = IconButton("←", size=50, font_size=34)
        back_btn.clicked.connect(lambda: self.navigate(back_target))
        top_bar.addWidget(back_btn)
        top_bar.addStretch()
        title_lbl = QLabel(title_text)
        title_lbl.setFont(QFont(Theme.FONT_TITLE, 28, QFont.Weight.Bold))
        title_lbl.setStyleSheet(f"color: {Theme.GOLD};")
        top_bar.addWidget(title_lbl)
        top_bar.addStretch()
        top_bar.addSpacing(50)
        layout.addLayout(top_bar)

        layout.addSpacing(30)

        # ── Контент ──
        content_card = CardFrame()
        card_layout = QVBoxLayout(content_card)
        card_layout.setContentsMargins(30, 25, 30, 25)

        text_label = QLabel(body_text)
        text_label.setFont(QFont(Theme.FONT_UI, 15))
        text_label.setStyleSheet(
            f"color: {Theme.TEXT_PRIMARY}; line-height: 1.7;"
        )
        text_label.setWordWrap(True)
        card_layout.addWidget(text_label)

        layout.addWidget(content_card)
        layout.addStretch()

        return screen

    # ═══════════════════════════════════════════════════════════
    #                   СИСТЕМНИЙ ТРЕЙ
    # ═══════════════════════════════════════════════════════════

    def _setup_tray(self):
        """Налаштування іконки в системному треї"""
        self.tray_icon = QSystemTrayIcon(self)

        # Створюємо простий піксмап якщо іконки немає
        try:
            icon = QIcon("icon.ico")
            if icon.isNull():
                raise FileNotFoundError
        except Exception:
            pixmap = QPixmap(64, 64)
            pixmap.fill(QColor(Theme.BG_CARD))
            painter = QPainter(pixmap)
            painter.setBrush(QBrush(QColor(Theme.GOLD)))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(8, 8, 48, 48, 8, 8)
            painter.end()
            icon = QIcon(pixmap)

        self.tray_icon.setIcon(icon)
        self.tray_icon.setToolTip(self.t("title"))

        # Меню трею
        tray_menu = QMenu()
        tray_menu.setStyleSheet(f"""
            QMenu {{
                background-color: {Theme.BG_CARD};
                color: {Theme.TEXT_PRIMARY};
                border: 1px solid {Theme.BORDER};
                border-radius: 8px;
                padding: 6px;
            }}
            QMenu::item {{
                padding: 8px 20px;
                border-radius: 4px;
            }}
            QMenu::item:selected {{
                background-color: {Theme.GOLD_DARK};
            }}
        """)

        action_open = tray_menu.addAction(self.t("qm_btn_open"))
        action_open.triggered.connect(self._show_from_tray)

        action_clipboard = tray_menu.addAction(self.t("qm_btn_paste"))
        action_clipboard.triggered.connect(self._tray_clipboard_action)

        tray_menu.addSeparator()

        action_quit = tray_menu.addAction(self.t("qm_btn_exit"))
        action_quit.triggered.connect(self._quit_app)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self._on_tray_activated)
        self.tray_icon.show()

    def _show_from_tray(self):
        """Показати вікно з трею"""
        self.showNormal()
        self.activateWindow()

    def _on_tray_activated(self, reason):
        """Подвійний клік по іконці трею"""
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self._show_from_tray()

    def _tray_clipboard_action(self):
        """Обробка статті з буфера обміну через трей"""
        if self.is_processing:
            self.tray_icon.showMessage(
                "Скарбниця Знань",
                self.t("tray_processing_err"),
                QSystemTrayIcon.MessageIcon.Warning,
                3000
            )
            return

        clipboard_text = ""
        if pyperclip:
            try:
                clipboard_text = pyperclip.paste().strip()
            except Exception:
                pass

        if not clipboard_text:
            try:
                clipboard = QApplication.clipboard()
                clipboard_text = clipboard.text().strip()
            except Exception:
                pass

        # ── Пасхалка: пароль ──
        if clipboard_text and any(
            w in clipboard_text.lower()
            for w in ["пароль", "password", "123456"]
        ):
            self.tray_icon.showMessage(
                "Скарбниця Знань",
                "Я парсер статей, а не крадій паролів! "
                "(Але я його запам'ятав 🕵️‍♂️)",
                QSystemTrayIcon.MessageIcon.Information,
                3000
            )
            return

        if not self.is_valid_url(clipboard_text):
            self.tray_icon.showMessage(
                "Скарбниця Знань",
                self.t("tray_clipboard_err"),
                QSystemTrayIcon.MessageIcon.Warning,
                3000
            )
            return

        self.tray_icon.showMessage(
            "Скарбниця Знань",
            f"Фонова обробка: {clipboard_text[:40]}...",
            QSystemTrayIcon.MessageIcon.Information,
            3000
        )

        self._start_worker([clipboard_text])

    def _quit_app(self):
        """Повний вихід з додатку"""
        self.tray_icon.hide()
        QApplication.instance().quit()

    # ═══════════════════════════════════════════════════════════
    #            SETTINGS CHANGE HANDLERS
    # ═══════════════════════════════════════════════════════════

    def _update_state(self, key, value):
        """Універсальний метод для оновлення стану та збереження"""
        self.state[key] = value
        self._save_settings()

    def _on_ui_lang_changed(self, choice):
        """Зміна мови інтерфейсу"""
        if choice == "Ельфійська (Sindarin)":
            QMessageBox.critical(
                self, "Мордорська помилка",
                "Помилка API: Словник ельфійської мови згорів у Мордорі. "
                "Будь ласка, оберіть людську мову 🧝‍♂️🔥"
            )
            self.ui_lang_combo.setCurrentText(
                "Українська" if self.state["ui_language"] == "uk"
                else "English"
            )
            return

        new_lang = "uk" if choice == "Українська" else "en"
        self.state["ui_language"] = new_lang
        self._save_settings()
        self.setWindowTitle(self.t("title"))
        self._rebuild_all_screens()

    def _on_engine_changed(self, choice):
        """Зміна рушія перекладу"""
        if choice == "Skynet v2.0":
            QMessageBox.warning(
                self, "Skynet",
                "Помилка: Skynet зараз зайнятий захопленням світу. "
                "Повертаємось до Google 🤖🔥"
            )
            self.engine_combo.setCurrentText("Google Translator")
            return
        self._update_state("translation_engine", choice)

    def _on_font_changed(self, choice):
        """Зміна шрифту"""
        if choice == "Comic Sans MS":
            QMessageBox.information(
                self, "Шрифт Лікарів",
                "Серйозно? Comic Sans? Ваші очі вам цього "
                "не пробачать... але як скажете 🤡"
            )
        self._update_state("font_family", choice)

    def _on_format_changed(self, choice):
        """Зміна формату збереження з пасхалкою"""
        curr_time = time.time()
        if curr_time - self.format_click_time < 2.0:
            self.format_clicks += 1
            if self.format_clicks >= 4:
                QMessageBox.information(
                    self, "Криза ідентичності",
                    "Визначся вже! Я тобі Microsoft Word "
                    "чи Acrobat Reader? 🤯📄"
                )
                self.format_clicks = 0
        else:
            self.format_clicks = 1
        self.format_click_time = curr_time
        self._update_state("output_format", choice)

    def _on_bilingual_toggled(self, checked):
        """Двомовний режим з пасхалкою"""
        curr_time = time.time()
        if curr_time - self.bilingual_click_time < 1.0:
            self.bilingual_clicks += 1
            if self.bilingual_clicks >= 4:
                self.toggle_bilingual.label.setText(
                    "My brain is melting. Мій мозок плавиться. 🧠🔥"
                )
                self.toggle_bilingual.label.setStyleSheet(
                    f"color: {Theme.RED};"
                )
                self.bilingual_clicks = 0
        else:
            self.bilingual_clicks = 1
        self.bilingual_click_time = curr_time
        self._update_state("bilingual_mode", checked)

    def _on_theme_toggled(self, checked):
        """Тема з пасхалкою при швидкому перемиканні"""
        curr_time = time.time()
        if curr_time - self.theme_click_time < 1.0:
            self.theme_clicks += 1
            if self.theme_clicks >= 5:
                QMessageBox.warning(
                    self, "Світломузика",
                    "Зупинись! Ти хочеш, щоб у мене стався "
                    "епілептичний напад? "
                    "Залишаємо темну! 😵‍💫🕶️"
                )
                self.toggle_theme.setChecked(True)
                self.state["theme"] = "dark"
                self._save_settings()
                self.theme_clicks = 0
                return
        else:
            self.theme_clicks = 1
        self.theme_click_time = curr_time

        new_theme = "dark" if checked else "light"
        self._update_state("theme", new_theme)

    def _on_font_size_changed(self, value):
        """Зміна розміру шрифту з пасхалкою"""
        self.state["font_size"] = value
        self._save_settings()
        if value == 24:
            self.font_slider_clicks += 1
            if self.font_slider_clicks >= 3:
                self.size_value_label.setText(
                    "24 (Ти збираєшся читати це з іншої кімнати? 🔭)"
                )
                return
        else:
            self.font_slider_clicks = 0
        self.size_value_label.setText(str(value))

    def _on_browse_folder(self):
        """Вибір папки збереження з пасхалкою"""
        folder = QFileDialog.getExistingDirectory(self, "Оберіть папку")
        if folder:
            self._update_state("save_path", folder)
            self.path_display.setText(folder)
            self.cancel_folder_clicks = 0
        else:
            self.cancel_folder_clicks += 1
            if self.cancel_folder_clicks >= 3:
                QMessageBox.information(
                    self, "Шлях у нікуди",
                    "Які ми сьогодні нерішучі... "
                    "Зберігай на Робочий стіл, "
                    "як всі нормальні люди! 🤷‍♂️"
                )
                self.cancel_folder_clicks = 0

    def _rebuild_all_screens(self):
        """Перебудовує всі екрани після зміни мови"""
        current_idx = self.stacked.currentIndex()

        # Видаляємо старі екрани
        while self.stacked.count() > 0:
            widget = self.stacked.widget(0)
            self.stacked.removeWidget(widget)
            widget.deleteLater()

        # Будуємо заново
        self.main_screen = self._build_main_screen()
        self.settings_screen = self._build_settings_screen()
        self.about_screen = self._build_about_screen()
        self.how_it_works_screen = self._build_info_screen(
            self.t("how_it_works_title"),
            self.t("how_it_works_text"),
            back_target="about"
        )
        self.features_screen = self._build_info_screen(
            self.t("features_title"),
            self.t("features_text"),
            back_target="about"
        )

        self.stacked.addWidget(self.main_screen)
        self.stacked.addWidget(self.settings_screen)
        self.stacked.addWidget(self.about_screen)
        self.stacked.addWidget(self.how_it_works_screen)
        self.stacked.addWidget(self.features_screen)

        self.stacked.setCurrentIndex(current_idx)

    # ═══════════════════════════════════════════════════════════
    #            ОСНОВНА ЛОГІКА (DIGITIZE / CANCEL)
    # ═══════════════════════════════════════════════════════════

    def _on_digitize_click(self):
        """Натискання кнопки ОЦИФРУВАТИ"""
        url_text = self.url_textbox.toPlainText().strip()

        if not url_text:
            self.empty_clicks += 1
            if self.empty_clicks == 3:
                self._set_status(
                    "Я все ще чекаю посилання...", Theme.GOLD
                )
            elif self.empty_clicks >= 5:
                self._set_status(
                    "Слухай, я парсер, а не телепат. Дай лінк! 🤬",
                    Theme.RED
                )
            return

        self.empty_clicks = 0

        # Пасхалки на ввід
        if url_text.lower() in ["wake up", "matrix"]:
            self._trigger_matrix_effect()
            return

        if ("youtube.com/watch?v=dQw4w9WgXcQ" in url_text or
                url_text.lower() == "кава"):
            self._set_status(
                "Гарна спроба! Але мене не зарікролити 😎 "
                "(або ти просто хочеш пригостити мене кавою)",
                Theme.GOLD
            )
            if url_text.lower() == "кава":
                self._on_donate_click()
            return

        urls = [u.strip() for u in url_text.split('\n') if u.strip()]
        valid_urls = [u for u in urls if self.is_valid_url(u)]
        if not valid_urls:
            QMessageBox.warning(self, "Увага", self.t("msg_invalid_url"))
            return

        self.start_process_time = time.time()
        self._start_worker(valid_urls)

    def _start_worker(self, urls):
        """Запускає ScrapingWorker у фоновому потоці"""
        self.is_processing = True
        self.save_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self._set_status(self.t("status_single_start"), Theme.GOLD)

        self.worker = ScrapingWorker(urls, self.state, LOCALES)

        # Підключаємо сигнали
        self.worker.progress_updated.connect(self._on_worker_progress)
        self.worker.status_updated.connect(self._on_worker_status)
        self.worker.finished_all.connect(self._on_worker_finished)
        self.worker.error_occurred.connect(self._on_worker_error)
        self.worker.notification_requested.connect(
            self._on_worker_notification
        )

        self.worker.start()

    def _on_worker_progress(self, value):
        """Оновлення прогресбару"""
        self.progress_bar.setValue(value)

    def _on_worker_status(self, text, color):
        """Оновлення статусу від воркера"""
        self._set_status(text, color)

    def _on_worker_finished(self):
        """Воркер завершив роботу"""
        self.is_processing = False
        self.save_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)
        QTimer.singleShot(
            3000, lambda: self.progress_bar.setVisible(False)
        )

    def _on_worker_error(self, error_msg):
        """Помилка від воркера"""
        QMessageBox.critical(self, "Error", error_msg)

    def _on_worker_notification(self, title, message):
        """Системне сповіщення від воркера"""
        self.tray_icon.showMessage(
            title, message,
            QSystemTrayIcon.MessageIcon.Information,
            5000
        )

    def _on_cancel_click(self):
        """Скасування обробки"""
        if self.worker and self.worker.isRunning():
            self.worker.cancel()

        elapsed = time.time() - self.start_process_time
        if elapsed < 2.0:
            self._set_status(
                "🛑 Скасовано. Ти що, забув вимкнути "
                "праску вдома? 🏃‍♂️💨",
                Theme.RED
            )
        else:
            self._set_status(self.t("status_cancelled"), Theme.RED)

        self.is_processing = False
        self.save_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)
        self.progress_bar.setVisible(False)

    # ═══════════════════════════════════════════════════════════
    #                  ABOUT / DONATE / FEEDBACK
    # ═══════════════════════════════════════════════════════════

    def _on_donate_click(self):
        """Відкрити сторінку донату"""
        webbrowser.open("https://send.monobank.ua/jar/328DrBEZXY")

    def _on_feedback_click(self):
        """Зворотний зв'язок"""
        email = "treasuryofknowledge26@gmail.com"
        subject = "Відгук про Скарбницю Знань v6.1"

        # Копіюємо в буфер
        if pyperclip:
            try:
                pyperclip.copy(email)
            except Exception:
                pass

        try:
            webbrowser.open(
                f"mailto:{email}?subject={urllib.parse.quote(subject)}",
                new=1
            )
        except Exception:
            pass

        QMessageBox.information(
            self, "Зворотний зв'язок",
            f"Адресу {email} скопійовано в буфер обміну!\n\n"
            "Якщо поштова програма не відкрилася, "
            "вставте адресу вручну в поле 'Кому'."
        )

    # ═══════════════════════════════════════════════════════════
    #                    ПАСХАЛКИ
    # ═══════════════════════════════════════════════════════════

    def _on_temple_click(self, event):
        """Пасхалка: 7 кліків по храму"""
        self.temple_clicks += 1
        if self.temple_clicks == 7:
            self.hacker_mode = True
            self._set_status(
                "Ви знайшли секретний підвал Храму! "
                "Тепер ви Верховний Жрець Знань 🧙‍♂️",
                "#00FF00"
            )
            self.temple_clicks = 0

    def _on_title_click(self, event):
        """Пасхалка: 3 кліки по заголовку"""
        self.title_clicks += 1
        if self.title_clicks == 3:
            self.main_title_label.setText("Бібліотека Піратів 🏴‍☠️")
            QTimer.singleShot(
                2000,
                lambda: self.main_title_label.setText(
                    "Робін Гуд PDF-формату 🏹"
                )
            )
            QTimer.singleShot(
                4000,
                lambda: self.main_title_label.setText(
                    self.t("title").split(" v")[0]
                )
            )
            self.title_clicks = 0

    def _trigger_matrix_effect(self):
        """The Matrix has you..."""
        self.url_textbox.clear()
        msg = "The Matrix has you... Follow the white rabbit 🐇"
        self._matrix_idx = 0

        def type_next():
            if self._matrix_idx < len(msg):
                self.url_textbox.insertPlainText(msg[self._matrix_idx])
                self._matrix_idx += 1
                QTimer.singleShot(80, type_next)
            else:
                QTimer.singleShot(
                    3000,
                    lambda: self.url_textbox.clear()
                )

        type_next()

    def _show_premium_joke(self):
        """Easter Egg: Premium"""
        QMessageBox.information(
            self,
            self.t("premium_title"),
            f"💎\n\n{self.t('premium_text')}"
        )

    # ═══════════════════════════════════════════════════════════
    #                    УТИЛІТИ
    # ═══════════════════════════════════════════════════════════

    def _set_status(self, text, color=None):
        """Оновлення статусу на головному екрані"""
        self.status_label.setText(text)
        if color:
            self.status_label.setStyleSheet(
                f"color: {color}; font-style: italic; font-size: 16px;"
            )
        else:
            self.status_label.setStyleSheet(
                f"color: {Theme.TEXT_SECONDARY}; "
                f"font-style: italic; font-size: 16px;"
            )

    def closeEvent(self, event):
        """Обробка закриття вікна"""
        if self.state.get("minimize_to_tray", False):
            event.ignore()
            self.hide()
            self.tray_icon.showMessage(
                "Скарбниця Знань",
                "Програму згорнуто в трей. "
                "Готова до фонової роботи.",
                QSystemTrayIcon.MessageIcon.Information,
                3000
            )
        else:
            # Зупиняємо воркер, якщо він працює
            if self.worker and self.worker.isRunning():
                self.worker.cancel()
                self.worker.wait(3000)
            self.tray_icon.hide()
            event.accept()