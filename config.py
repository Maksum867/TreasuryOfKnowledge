"""
╔══════════════════════════════════════════════════════════════╗
║              config.py — Конфігурація додатку                ║
║                                                              ║
║  Theme (кольори, шрифти)                                    ║
║  GLOBAL_STYLESHEET (QSS стилі)                             ║
║  LOCALES (словник локалізації uk/en)                        ║
╚══════════════════════════════════════════════════════════════╝
"""


# ═══════════════════════════════════════════════════════════════
#                    КЛАС ТЕМИ (КОЛЬОРИ / ШРИФТИ)
# ═══════════════════════════════════════════════════════════════

class Theme:
    """Централізоване управління кольорами та шрифтами"""

    # ── Основна палітра ──
    GOLD = "#d4af37"
    GOLD_HOVER = "#b5952f"
    GOLD_DARK = "#8B7530"

    GREEN = "#2d5a27"
    GREEN_HOVER = "#1e3d1a"
    GREEN_LIGHT = "#3d7a37"

    RED = "#8b0000"
    RED_HOVER = "#4a0000"
    RED_LIGHT = "#c0392b"

    BLUE = "#2980b9"
    BLUE_HOVER = "#1c5980"

    ORANGE = "#d35400"
    ORANGE_HOVER = "#e67e22"

    # ── Фони (Dark Mode) ──
    BG_PRIMARY = "#0d0d0d"
    BG_SECONDARY = "#1a1a1a"
    BG_CARD = "#1e1e1e"
    BG_INPUT = "#2a2a2a"
    BG_HOVER = "#333333"

    # ── Текст ──
    TEXT_PRIMARY = "#f0f0f0"
    TEXT_SECONDARY = "#999999"
    TEXT_MUTED = "#666666"

    # ── Бордери ──
    BORDER = "#3a3a3a"
    BORDER_GOLD = "#d4af37"
    BORDER_FOCUS = "#e6c565"

    # ── Шрифти ──
    FONT_TITLE = "Georgia"
    FONT_UI = "Segoe UI"
    FONT_MONO = "Cascadia Code"


# ═══════════════════════════════════════════════════════════════
#                   ГЛОБАЛЬНІ СТИЛІ (QSS)
# ═══════════════════════════════════════════════════════════════

GLOBAL_STYLESHEET = f"""
    /* ── Загальне ── */
    QMainWindow {{
        background-color: {Theme.BG_PRIMARY};
    }}

    QWidget {{
        color: {Theme.TEXT_PRIMARY};
        font-family: "{Theme.FONT_UI}";
    }}

    /* ── Скролбари ── */
    QScrollBar:vertical {{
        background: {Theme.BG_SECONDARY};
        width: 8px;
        border-radius: 4px;
        margin: 0;
    }}
    QScrollBar::handle:vertical {{
        background: {Theme.GOLD_DARK};
        border-radius: 4px;
        min-height: 30px;
    }}
    QScrollBar::handle:vertical:hover {{
        background: {Theme.GOLD};
    }}
    QScrollBar::add-line:vertical,
    QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
    QScrollBar::add-page:vertical,
    QScrollBar::sub-page:vertical {{
        background: none;
    }}

    /* ── Текстові поля ── */
    QTextEdit {{
        background-color: {Theme.BG_INPUT};
        color: {Theme.TEXT_PRIMARY};
        border: 2px solid {Theme.BORDER};
        border-radius: 16px;
        padding: 16px;
        font-size: 15px;
        font-family: "{Theme.FONT_UI}";
        selection-background-color: {Theme.GOLD_DARK};
    }}
    QTextEdit:focus {{
        border-color: {Theme.GOLD};
    }}

    /* ── Комбобокси ── */
    QComboBox {{
        background-color: {Theme.BG_INPUT};
        color: {Theme.TEXT_PRIMARY};
        border: 2px solid {Theme.BORDER};
        border-radius: 12px;
        padding: 10px 16px;
        font-size: 14px;
        min-width: 280px;
    }}
    QComboBox:hover {{
        border-color: {Theme.GOLD};
    }}
    QComboBox::drop-down {{
        border: none;
        width: 30px;
    }}
    QComboBox::down-arrow {{
        image: none;
        border: none;
    }}
    QComboBox QAbstractItemView {{
        background-color: {Theme.BG_CARD};
        color: {Theme.TEXT_PRIMARY};
        border: 1px solid {Theme.BORDER};
        border-radius: 8px;
        selection-background-color: {Theme.GOLD_DARK};
        padding: 4px;
    }}

    /* ── Слайдери ── */
    QSlider {{
        min-height: 30px;
    }}
    QSlider::groove:horizontal {{
        border: none;
        height: 6px;
        background: {Theme.BORDER};
        border-radius: 3px;
    }}
    QSlider::handle:horizontal {{
        background: {Theme.GOLD};
        border: 2px solid {Theme.GOLD_DARK};
        width: 20px;
        height: 20px;
        margin: -7px 0;
        border-radius: 10px;
    }}
    QSlider::handle:horizontal:hover {{
        background: {Theme.GOLD_HOVER};
        border-color: {Theme.GOLD};
    }}
    QSlider::sub-page:horizontal {{
        background: {Theme.GOLD};
        border-radius: 3px;
    }}

    /* ── Чекбокси ── */
    QCheckBox {{
        spacing: 12px;
        font-size: 14px;
        color: {Theme.TEXT_PRIMARY};
        padding: 6px 0;
    }}
    QCheckBox::indicator {{
        width: 22px;
        height: 22px;
        border-radius: 6px;
        border: 2px solid {Theme.BORDER};
        background-color: {Theme.BG_INPUT};
    }}
    QCheckBox::indicator:checked {{
        background-color: {Theme.GOLD};
        border-color: {Theme.GOLD};
    }}
    QCheckBox::indicator:hover {{
        border-color: {Theme.GOLD};
    }}

    /* ── Прогресбар ── */
    QProgressBar {{
        background-color: {Theme.BG_INPUT};
        border: none;
        border-radius: 6px;
        height: 12px;
        text-align: center;
        font-size: 0px;
    }}
    QProgressBar::chunk {{
        background: qlineargradient(
            x1:0, y1:0, x2:1, y2:0,
            stop:0 {Theme.GOLD_DARK},
            stop:1 {Theme.GOLD}
        );
        border-radius: 6px;
    }}

    /* ── Скрол-область ── */
    QScrollArea {{
        border: none;
        background-color: transparent;
    }}
    QScrollArea > QWidget > QWidget {{
        background-color: transparent;
    }}

    /* ── Тултіпи ── */
    QToolTip {{
        background-color: {Theme.BG_CARD};
        color: {Theme.GOLD};
        border: 1px solid {Theme.GOLD_DARK};
        border-radius: 8px;
        padding: 8px 12px;
        font-size: 13px;
    }}
"""


# ═══════════════════════════════════════════════════════════════
#              ЛОКАЛІЗАЦІЯ (uk / en)
# ═══════════════════════════════════════════════════════════════

LOCALES = {
    "uk": {
        "title": "Скарбниця Знань v6.1",
        "placeholder": "Вставте посилання (можна кілька, кожне з нового рядка)...",
        "status_wait": "Очікування посилань...",
        "btn_digitize": "ОЦИФРУВАТИ В АРХІВ",
        "btn_cancel": "СКАСУВАТИ",

        "settings_title": "Налаштування",
        "path_lbl": "📍 Папка збереження:",
        "btn_choose": "Обрати",
        "font_lbl": "🖋️ Шрифт:",
        "size_lbl": "📏 Розмір тексту:",
        "format_lbl": "📄 Формат збереження:",
        "engine_lbl": "🤖 Рушій перекладу:",
        "theme_lbl": "🌓 Тема інтерфейсу:",
        "theme_dark": "Темний режим",
        "ui_lang_lbl": "🌍 Мова інтерфейсу:",
        "target_lang_lbl": "🎯 Перекладати статтю на:",

        "additional_features_lbl": "🛠 Додаткові функції",
        "setting_read_time": "⏱ Додавати орієнтовний час читання",
        "setting_bilingual": "📖 Двомовний режим (Оригінал + переклад)",
        "setting_auto_open": "🚀 Автоматично відкривати документ",
        "setting_images": "🖼️ Завантажувати зображення та відео",
        "setting_toc": "📑 Додавати автоматичний Зміст",
        "setting_metadata": "🔗 Додавати посилання на джерело",
        "setting_tray_close": "⏬ Згортати в трей при закритті",

        "btn_about": "ℹ️ Про додаток",
        "about_title": "Про додаток",
        "about_desc": (
            "Цей додаток створений для вільного доступу до інформації "
            "без кордонів та обмежень.\n\n"
            "Основна мета «Скарбниці Знань» — дати вам змогу читати "
            "статті, журнали та новини, які заблоковані у вашій країні, "
            "приховані за пейволом або вимагають платної підписки."
        ),
        "btn_features": "Основні функції ⭐️",
        "btn_how_it_works": "Як це працює ⚙️",
        "btn_donate": "☕ Підтримати автора",
        "btn_feedback": "@ Зворотний зв'язок",

        "how_it_works_title": "Механізм роботи",
        "how_it_works_text": (
            "🔍 Парсинг:\nПрограма використовує 'Снайперський режим' для пошуку "
            "тексту та витягує метадані (обкладинку, автора).\n\n"
            "🧠 Аналіз:\nАлгоритм відкидає меню, рекламні банери та списки "
            "'схожих новин'.\n\n"
            "🌍 Переклад та Збірка:\nАбзаци пропускаються через перекладач і "
            "зшиваються у документ разом із картинками."
        ),

        "premium_title": "Доступ до Premium",
        "premium_text": (
            "Вітаю, шукачу ексклюзиву! 🎩\n\n"
            "Ніякого 'Premium' у цьому додатку немає і ніколи не буде.\n\n"
            "Користуйся на здоров'я, розширюй кругозір і нехай ця програма "
            "служить тобі вірою і правдою."
        ),

        "features_title": "Можливості додатку",
        "features_text": (
            "Повний перелік функцій Скарбниці Знань:\n\n"
            "🔹 Згортання у Трей (робота у фоні)\n"
            "🔹 Швидке викачування статті з буфера обміну\n"
            "🔹 Обхід пейволів (читання платних статей)\n"
            "🔹 Витягування обкладинки, відео, автора та дати\n"
            "🔹 Збереження файлів у DOCX та PDF\n"
            "🔹 Двомовний режим\n"
            "🔹 Автоматичний Зміст для довгих статей\n"
            "🔹 15+ пасхалок 🥚"
        ),
        "btn_back": "Повернутися",

        "status_single_start": "🌐 Завантаження та обробка статті...",
        "status_magic": "🌐 Старт пакетної обробки (Стаття {} з {})...",
        "status_progress": "📜 Обробка {} з елементів...",
        "status_success": "✅ Усі документи успішно збережено!",
        "status_error": "❌ Помилка обробки",
        "status_cancelled": "🛑 Процес скасовано",
        "status_pdf": "📄 Конвертація у PDF...",
        "msg_error_txt": "Текст або контент не знайдено.",
        "msg_invalid_url": "Знайдено некоректне посилання. Перевірте ввід.",
        "doc_toc_title": "--- ЗМІСТ ---",
        "metadata_text": "\n\n---\n🔗 Джерело: {}\n📅 Збережено: {}",
        "video_link_text": "▶️ [Дивитися прикріплене відео]",
        "tray_clipboard_err": "У буфері обміну немає посилання!",
        "tray_processing_err": "Програма вже зайнята обробкою!",

        "qm_btn_paste": "📥 Оцифрувати з буфера",
        "qm_btn_open": "🖥️ Відкрити програму",
        "qm_btn_exit": "❌ Вийти повністю",
        "qm_tray_open": "Відкрити меню",
    },
    "en": {
        "title": "Treasury of Knowledge V6.1",
        "placeholder": "Paste URLs here (one per line)...",
        "status_wait": "Waiting for URLs...",
        "btn_digitize": "DIGITIZE TO ARCHIVE",
        "btn_cancel": "CANCEL",

        "settings_title": "Settings",
        "path_lbl": "📍 Save Directory:",
        "btn_choose": "Browse",
        "font_lbl": "🖋️ Font:",
        "size_lbl": "📏 Text Size:",
        "format_lbl": "📄 Format:",
        "engine_lbl": "🤖 Translation Engine:",
        "theme_lbl": "🌓 Theme:",
        "theme_dark": "Dark Mode",
        "ui_lang_lbl": "🌍 UI Language:",
        "target_lang_lbl": "🎯 Target Language:",

        "additional_features_lbl": "🛠 Features",
        "setting_read_time": "⏱ Add estimated reading time",
        "setting_bilingual": "📖 Bilingual Mode (Original + Translation)",
        "setting_auto_open": "🚀 Auto-open document after creation",
        "setting_images": "🖼️ Download images, covers & videos",
        "setting_toc": "📑 Add Table of Contents (for long articles)",
        "setting_metadata": "🔗 Add source URL at the end of file",
        "setting_tray_close": "⏬ Minimize to tray on close (background mode)",

        "btn_about": "ℹ️ About",
        "about_title": "About Application",
        "about_desc": (
            "This application was created for free access to information "
            "without borders and restrictions.\n\n"
            "The main goal of «Treasury of Knowledge» is to let you read "
            "articles, magazines and news that are blocked in your country, "
            "hidden behind a paywall, or require a paid subscription."
        ),
        "btn_features": "Features ⭐️",
        "btn_how_it_works": "How it works ⚙️",
        "btn_donate": "☕ Support Author",
        "btn_feedback": "@ Send Feedback",

        "how_it_works_title": "How It Works",
        "how_it_works_text": (
            "🔍 Parsing:\nThe app uses 'Sniper Mode' to locate the article text "
            "and extracts metadata (cover image, author).\n\n"
            "🧠 Analysis:\nThe algorithm discards menus, ad banners, and "
            "'related articles' lists.\n\n"
            "🌍 Translation & Assembly:\nParagraphs are passed through the translator "
            "and assembled into a document along with images."
        ),

        "premium_title": "Premium Access",
        "premium_text": (
            "Greetings, seeker of exclusives! 🎩\n\n"
            "There is no 'Premium' in this app and there never will be.\n\n"
            "Use it freely, broaden your horizons and may this program "
            "serve you faithfully!"
        ),

        "features_title": "App Features",
        "features_text": (
            "Full list of Treasury of Knowledge features:\n\n"
            "🔹 System Tray mode (background operation)\n"
            "🔹 Quick article download from clipboard\n"
            "🔹 Bypass paywalls (read paid articles)\n"
            "🔹 Extract cover images, videos, author & date\n"
            "🔹 Save files as DOCX and PDF\n"
            "🔹 Bilingual mode\n"
            "🔹 Automatic Table of Contents for long articles\n"
            "🔹 15+ Easter Eggs 🥚"
        ),
        "btn_back": "Go Back",

        "status_single_start": "🌐 Loading and processing article...",
        "status_magic": "🌐 Batch processing (Article {} of {})...",
        "status_progress": "📜 Processing element {} ...",
        "status_success": "✅ All documents saved successfully!",
        "status_error": "❌ Processing error",
        "status_cancelled": "🛑 Cancelled",
        "status_pdf": "📄 Converting to PDF...",
        "msg_error_txt": "No text or content found.",
        "msg_invalid_url": "Invalid URL detected. Please check your input.",
        "doc_toc_title": "--- TABLE OF CONTENTS ---",
        "metadata_text": "\n\n---\n🔗 Source: {}\n📅 Saved: {}",
        "video_link_text": "▶️ [Watch attached video]",
        "tray_clipboard_err": "No URL found in clipboard!",
        "tray_processing_err": "App is already processing!",

        "qm_btn_paste": "📥 Digitize from clipboard",
        "qm_btn_open": "🖥️ Open Main App",
        "qm_btn_exit": "❌ Quit App",
        "qm_tray_open": "Open Menu",
    },
}


# ═══════════════════════════════════════════════════════════════
#           НАЛАШТУВАННЯ ЗА ЗАМОВЧУВАННЯМ
# ═══════════════════════════════════════════════════════════════

import os

DEFAULT_SETTINGS = {
    "save_path": os.path.join(os.path.expanduser("~"), "Desktop"),
    "font_family": "Georgia",
    "font_size": 16,
    "output_format": "docx",
    "translation_engine": "Google Translator",
    "theme": "dark",
    "ui_language": "uk",
    "target_lang_name": "Українська",
    "add_read_time": True,
    "bilingual_mode": False,
    "auto_open": True,
    "download_images": True,
    "add_toc": True,
    "add_metadata": True,
    "minimize_to_tray": False,
}

# Файл конфігурації
CONFIG_FILE = "settings.json"