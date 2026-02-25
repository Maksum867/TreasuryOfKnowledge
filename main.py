import os
import re
import time
import json
import threading
import platform
import subprocess
import webbrowser
import requests
import hashlib
import warnings  # ДОДАНО: Для приховування попереджень
from io import BytesIO
import urllib.parse
from datetime import datetime

import customtkinter as ctk
from tkinter import messagebox, filedialog
from selenium import webdriver
from selenium.webdriver.edge.options import Options
#from selenium.webdriver.edge.service import Service as EdgeService
#from webdriver_manager.microsoft import EdgeChromiumDriverManager
from bs4 import BeautifulSoup

from docx import Document as WordDocument
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from plyer import notification

from deep_translator import MicrosoftTranslator, GoogleTranslator
from docx2pdf import convert
from readability import Document

# ПРИХОВУЄМО ЧЕРВОНЕ ПОПЕРЕДЖЕННЯ В ТЕРМІНАЛІ
warnings.filterwarnings("ignore", category=UserWarning, module='requests')


class TranslationArchiveApp:
    def __init__(self):
        self.config_file = "settings.json"
        self.cache_dir = "backup_cache"

        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

        self.cancel_event = threading.Event()

        self.locales = {
            "uk": {
                "title": "Скарбниця Знань v4.0",
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

                "additional_features_lbl": "🛠 Додаткові функції:",
                "setting_read_time": "⏱ Додавати орієнтовний час читання",
                "setting_bilingual": "📖 Двомовний режим (Оригінал + переклад)",
                "setting_auto_open": "🚀 Автоматично відкривати документ після створення",
                "setting_images": "🖼️ Завантажувати зображення (вимкніть для швидкості)",
                "setting_toc": "📑 Додавати автоматичний Зміст (для довгих статей)",
                "setting_metadata": "🔗 Додавати посилання на джерело та дату в кінці файлу",

                "btn_about": "ℹ️ Про додаток",
                "about_title": "Про додаток",
                # НОВИЙ ОПИС ПРОГРАМИ
                "about_desc": "Цей додаток створений для вільного доступу до інформації без кордонів та обмежень.\n\nОсновна мета «Скарбниці Знань» — дати вам змогу читати статті, журнали та новини, які заблоковані у вашій країні, приховані за пейволом (paywall) або вимагають платної підписки, на яку у вас немає коштів.\n\nПрограма алгоритмічно «витягує» прихований текст з сайту, перекладає його на зручну для вас мову та зберігає у вигляді чистого, акуратного документа на вашому комп'ютері. Знання мають бути безкоштовними та доступними для кожного.",
                "btn_features": "Основні функції ⭐️",  # ЗМІНЕНО КНОПКУ
                "btn_how_it_works": "Як це працює ⚙️",
                "btn_donate": "☕ Підтримати автора",

                "how_it_works_title": "Механізм роботи",
                "how_it_works_text": "Розробляючи цей інструмент, я ставив за мету зробити інтернет чистішим.\n\n🔍 Парсинг (Видобуток контенту):\nПрограма використовує 'Режим читання' (Readability) для точного виділення статті, відкидаючи меню та рекламу.\n\n🧠 Аналіз структури:\nАлгоритм сканує сторінку, знаходить заголовки (H2/H3), списки та абзаци. Якщо стаття велика, автоматично генерується Зміст для зручної навігації.\n\n🌍 Переклад та Збірка:\nКожен абзац обережно пропускається через API обраного перекладача. Після цього програма буквально 'зшиває' текст і картинки у красивий документ.",

                "premium_title": "Доступ до Premium",
                "premium_text": "Вітаю, шукачу ексклюзиву! 🎩\n\nНіякого 'Premium' у цьому додатку немає і, мабуть, ніколи не буде.\n\nКористуйся на здоров'я, розширюй кругозір і нехай ця програма служить тобі вірою і правдою.\n\n(Але якщо вона дійсно зекономила тобі купу часу — ти завжди можеш пригостити мене кавою 😉).",

                "features_title": "Можливості додатку",  # ЗМІНЕНО ЗАГОЛОВОК
                "features_text": "Повний перелік функцій Скарбниці Знань:\n\n🔹 Обхід блокувань та пейволів (читання платних статей безкоштовно)\n🔹 Автоматичний переклад (Пріоритет Google або Microsoft на вибір)\n🔹 Збереження файлів у форматах DOCX та ідеальному PDF\n🔹 Інтелектуальний 'Режим читання' — автоматичне видалення реклами, банерів та меню з сайтів\n🔹 Автоматична генерація Змісту для великих статей\n🔹 Можливість зберегти статтю без картинок (Тільки текст)\n🔹 Двомовний режим (оригінал + переклад по абзацах)\n🔹 Оцінка орієнтовного часу читання статті\n🔹 Збереження оригінального посилання та дати створення\n🔹 Підтримка темної та світлої теми інтерфейсу",
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
                "metadata_text": "\n\n---\n🔗 Джерело: {}\n📅 Дата збереження: {}"
            },
            "en": {
                "title": "Treasury of Knowledge v4.0",
                "placeholder": "Paste URLs here (multiple allowed, one per line)...",
                "status_wait": "Waiting for URLs...",
                "btn_digitize": "DIGITIZE TO ARCHIVE",
                "btn_cancel": "CANCEL",

                "settings_title": "Settings",
                "path_lbl": "📍 Save Directory:",
                "btn_choose": "Browse",
                "font_lbl": "🖋️ Font Family:",
                "size_lbl": "📏 Text Size:",
                "format_lbl": "📄 Save Format:",
                "engine_lbl": "🤖 Translation Engine:",
                "theme_lbl": "🌓 Interface Theme:",
                "theme_dark": "Dark Mode",
                "ui_lang_lbl": "🌍 Interface Language:",
                "target_lang_lbl": "🎯 Translate article to:",

                "additional_features_lbl": "🛠 Additional Features:",
                "setting_read_time": "⏱ Add estimated reading time",
                "setting_bilingual": "📖 Bilingual Mode (Original + Translation)",
                "setting_auto_open": "🚀 Auto-open document after creation",
                "setting_images": "🖼️ Download images (turn off for speed)",
                "setting_toc": "📑 Add automatic Table of Contents",
                "setting_metadata": "🔗 Add source URL and date to the end of document",

                "btn_about": "ℹ️ About",
                "about_title": "About Application",
                # НОВИЙ ОПИС ПРОГРАМИ (Англ)
                "about_desc": "This app is created for free access to information without borders and restrictions.\n\nThe main goal of 'Treasury of Knowledge' is to let you read articles, journals, and news that are geo-blocked in your country, hidden behind a paywall, or require a paid subscription you cannot afford.\n\nThe program algorithmically extracts the hidden text, translates it into your preferred language, and saves it as a clean document on your PC. Knowledge should be free and accessible to everyone.",
                "btn_features": "Core Features ⭐️",  # ЗМІНЕНО КНОПКУ
                "btn_how_it_works": "How it works ⚙️",
                "btn_donate": "☕ Support Author",

                "how_it_works_title": "How It Works",
                "how_it_works_text": "🔍 Scraping:\nA hidden browser opens and uses 'Reader Mode' to extract only the pure article, ignoring ads.\n\n🧠 Structure Analysis:\nIt scans for headings, lists, and paragraphs. Automatically generates a Table of Contents for long reads.\n\n🌍 Translation & Assembly:\nEach paragraph is translated and stitched together into a beautiful document.",

                "premium_title": "Premium Access",
                "premium_text": "Greetings, seeker of exclusivity! 🎩\n\nThere is no 'Premium' in this app, and probably never will be.\n\nUse it freely while you can. Expand your horizons, and let this program serve you well.",

                "features_title": "App Features",  # ЗМІНЕНО ЗАГОЛОВОК
                "features_text": "Full list of Treasury of Knowledge features:\n\n🔹 Bypass geo-blocks and paywalls (read paid articles for free)\n🔹 Auto-translation (Google or Microsoft priority choice)\n🔹 Save files in DOCX and perfect PDF formats\n🔹 Intelligent 'Reader Mode' — removes ads, banners, and menus\n🔹 Auto-generates Table of Contents for long reads\n🔹 Option to save without images (Text only mode)\n🔹 Bilingual mode (original + translation by paragraph)\n🔹 Estimated reading time calculator\n🔹 Source URL and date saved metadata\n🔹 Dark and Light interface themes",
                "btn_back": "Go Back",

                "status_single_start": "🌐 Downloading and processing article...",
                "status_magic": "🌐 Starting batch process (Article {} of {})...",
                "status_progress": "📜 Processing element {} of {}...",
                "status_success": "✅ All documents saved successfully!",
                "status_error": "❌ Processing error",
                "status_cancelled": "🛑 Process cancelled",
                "status_pdf": "📄 Converting to PDF...",
                "msg_error_txt": "Text or content not found.",
                "msg_invalid_url": "Invalid URL found. Please check your input.",
                "doc_toc_title": "--- TABLE OF CONTENTS ---",
                "metadata_text": "\n\n---\n🔗 Source: {}\n📅 Date saved: {}"
            }
        }

        self.translation_languages = {
            "Українська": "uk", "English": "en", "Polski": "pl",
            "Deutsch": "de", "Français": "fr", "Español": "es"
        }

        self.state = self.load_settings()
        self.temp_state = self.state.copy()

        self.root = ctk.CTk()
        self.root.geometry("950x850")

        self.accent_gold = "#d4af37"
        self.accent_green = "#2d5a27"
        self.accent_red = "#8b0000"

        ctk.set_appearance_mode(self.state.get("theme", "dark"))
        self.update_window_title()

        self.main_container = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True)

        self.show_main_screen()

    def t(self, key):
        lang = self.temp_state.get("ui_language", "uk")
        return self.locales[lang][key]

    def update_window_title(self):
        lang = self.state.get("ui_language", "uk")
        self.root.title(self.locales[lang]["title"])

    def load_settings(self):
        default_path = os.path.join(os.path.expanduser("~"), "Desktop")
        defaults = {
            "save_path": default_path,
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
            "add_metadata": True
        }
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    return {**defaults, **loaded}
            except:
                return defaults
        return defaults

    def save_all_changes(self):
        self.state = self.temp_state.copy()
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(self.state, f, ensure_ascii=False, indent=4)
        self.update_window_title()
        self.show_main_screen()

    def clear_screen(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def update_status(self, text, color=None):
        if color:
            self.status_label.configure(text=text, text_color=color)
        else:
            self.status_label.configure(text=text)

    def show_premium_joke(self):
        joke_win = ctk.CTkToplevel(self.root)
        joke_win.title(self.t("premium_title"))
        joke_win.geometry("550x450")
        joke_win.attributes("-topmost", True)

        ctk.CTkLabel(joke_win, text="💎", font=("Arial", 60)).pack(pady=(20, 10))

        text_box = ctk.CTkTextbox(joke_win, width=480, height=250, font=("Inter", 16), wrap="word",
                                  fg_color="transparent")
        text_box.pack(pady=10)
        text_box.insert("1.0", self.t("premium_text"))
        text_box.configure(state="disabled")

        ctk.CTkButton(joke_win, text="Зрозуміло 😄", command=joke_win.destroy,
                      fg_color=self.accent_gold, text_color="black", hover_color="#b5952f",
                      font=("Inter", 16, "bold")).pack(pady=10)

    def show_main_screen(self):
        self.clear_screen()
        self.temp_state = self.state.copy()

        settings_btn = ctk.CTkButton(self.main_container, text="⚙️", width=45, height=45,
                                     fg_color="transparent", text_color=self.accent_gold,
                                     font=("Arial", 32), command=self.show_settings_screen)
        settings_btn.place(relx=0.93, rely=0.07, anchor="center")

        title_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        title_frame.pack(pady=(70, 20))

        temple_label = ctk.CTkLabel(title_frame, text="🏛️", font=("Arial", 35))
        temple_label.place(relx=0.542, rely=0.12, anchor="center")

        main_title = ctk.CTkLabel(title_frame, text=self.t("title").split(" v")[0],
                                  font=("Georgia", 58, "bold"), text_color=self.accent_gold)
        main_title.pack(pady=(40, 0))

        self.url_textbox = ctk.CTkTextbox(self.main_container, width=720, height=120,
                                          border_width=2, border_color=self.accent_gold,
                                          font=("Inter", 15), corner_radius=15)
        self.url_textbox.pack(pady=10)
        self.url_textbox.insert("1.0", self.t("placeholder"))
        self.url_textbox.bind("<FocusIn>", lambda e: self.clear_placeholder())

        self.progress_bar = ctk.CTkProgressBar(self.main_container, width=500, height=10,
                                               progress_color=self.accent_gold)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=10)
        self.progress_bar.pack_forget()

        self.status_label = ctk.CTkLabel(self.main_container, text=self.t("status_wait"),
                                         font=("Inter", 18, "italic"), text_color=("gray20", "gray80"))
        self.status_label.pack(pady=5)

        btn_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        btn_frame.pack(pady=20)

        self.save_btn = ctk.CTkButton(btn_frame, text=self.t("btn_digitize"),
                                      font=("Inter", 24, "bold"),
                                      fg_color=self.accent_green, hover_color="#1e3d1a",
                                      height=75, width=350, corner_radius=20,
                                      command=self.run_process)
        self.save_btn.pack(side="left", padx=10)

        self.cancel_btn = ctk.CTkButton(btn_frame, text=self.t("btn_cancel"),
                                        font=("Inter", 20, "bold"),
                                        fg_color="transparent", border_width=2, border_color=self.accent_red,
                                        text_color=self.accent_red, hover_color="#4a0000",
                                        height=75, width=150, corner_radius=20,
                                        command=self.cancel_process, state="disabled")
        self.cancel_btn.pack(side="right", padx=10)

    def clear_placeholder(self):
        current_text = self.url_textbox.get("1.0", "end-1c").strip()
        if current_text == self.t("placeholder"):
            self.url_textbox.delete("1.0", "end")

    def show_settings_screen(self):
        self.clear_screen()
        back_btn = ctk.CTkButton(self.main_container, text="←", width=50, height=50, fg_color="transparent",
                                 text_color=self.accent_gold, font=("Arial", 40, "bold"), command=self.save_all_changes)
        back_btn.place(relx=0.07, rely=0.07, anchor="center")
        ctk.CTkLabel(self.main_container, text=self.t("settings_title"), font=("Georgia", 34, "bold"),
                     text_color=self.accent_gold).pack(pady=(50, 10))

        scroll = ctk.CTkScrollableFrame(self.main_container, fg_color="transparent", width=800, height=600)
        scroll.pack(padx=50, pady=10, fill="both", expand=True)

        ctk.CTkLabel(scroll, text=self.t("ui_lang_lbl"), font=("Inter", 16, "bold")).pack(anchor="w")
        lang_combo = ctk.CTkComboBox(scroll, values=["Українська", "English"], width=300,
                                     command=self.change_ui_language)
        lang_combo.set("Українська" if self.temp_state["ui_language"] == "uk" else "English")
        lang_combo.pack(anchor="w", pady=5)

        ctk.CTkLabel(scroll, text=self.t("target_lang_lbl"), font=("Inter", 16, "bold")).pack(anchor="w", pady=(10, 0))
        target_combo = ctk.CTkComboBox(scroll, values=list(self.translation_languages.keys()), width=300,
                                       command=lambda v: self.temp_state.update({"target_lang_name": v}))
        target_combo.set(self.temp_state["target_lang_name"])
        target_combo.pack(anchor="w", pady=5)

        ctk.CTkLabel(scroll, text=self.t("engine_lbl"), font=("Inter", 16, "bold")).pack(anchor="w", pady=(10, 0))
        engine_combo = ctk.CTkComboBox(scroll, values=["Google Translator", "Microsoft Translator"], width=300,
                                       command=lambda v: self.temp_state.update({"translation_engine": v}))
        engine_combo.set(self.temp_state.get("translation_engine", "Google Translator"))
        engine_combo.pack(anchor="w", pady=5)

        ctk.CTkLabel(scroll, text=self.t("path_lbl"), font=("Inter", 16, "bold")).pack(anchor="w", pady=(10, 0))
        path_f = ctk.CTkFrame(scroll, fg_color="transparent")
        path_f.pack(fill="x", pady=5)
        self.path_lbl = ctk.CTkLabel(path_f, text=self.temp_state["save_path"], wraplength=550)
        self.path_lbl.pack(side="left")
        ctk.CTkButton(path_f, text=self.t("btn_choose"), command=self.change_path).pack(side="right")

        ctk.CTkLabel(scroll, text=self.t("font_lbl"), font=("Inter", 16, "bold")).pack(anchor="w", pady=(10, 0))
        f_combo = ctk.CTkComboBox(scroll, values=["Georgia", "Arial", "Times New Roman"], width=300,
                                  command=lambda v: self.temp_state.update({"font_family": v}))
        f_combo.set(self.temp_state["font_family"])
        f_combo.pack(anchor="w", pady=5)

        ctk.CTkLabel(scroll, text=self.t("format_lbl"), font=("Inter", 16, "bold")).pack(anchor="w", pady=(10, 0))
        format_combo = ctk.CTkComboBox(scroll, values=["docx", "pdf"], width=300,
                                       command=lambda v: self.temp_state.update({"output_format": v}))
        format_combo.set(self.temp_state.get("output_format", "docx"))
        format_combo.pack(anchor="w", pady=5)

        size_head = ctk.CTkFrame(scroll, fg_color="transparent")
        size_head.pack(fill="x", pady=(10, 0))
        ctk.CTkLabel(size_head, text=self.t("size_lbl"), font=("Inter", 16, "bold")).pack(side="left")
        self.size_val_label = ctk.CTkLabel(size_head, text=str(self.temp_state["font_size"]),
                                           font=("Inter", 18, "bold"), text_color=self.accent_gold)
        self.size_val_label.pack(side="right", padx=20)
        s_slider = ctk.CTkSlider(scroll, from_=12, to=24, number_of_steps=12,
                                 command=lambda v: self.update_font_size(v), progress_color=self.accent_gold)
        s_slider.set(self.temp_state["font_size"])
        s_slider.pack(fill="x", pady=5)

        ctk.CTkLabel(scroll, text=self.t("additional_features_lbl"), font=("Inter", 16, "bold"),
                     text_color=self.accent_gold).pack(
            anchor="w", pady=(20, 5))

        sw_read_time = ctk.CTkSwitch(scroll, text=self.t("setting_read_time"),
                                     command=lambda: self.temp_state.update({"add_read_time": sw_read_time.get()}),
                                     progress_color=self.accent_gold)
        if self.temp_state.get("add_read_time", True): sw_read_time.select()
        sw_read_time.pack(anchor="w", pady=5)

        sw_toc = ctk.CTkSwitch(scroll, text=self.t("setting_toc"),
                               command=lambda: self.temp_state.update({"add_toc": sw_toc.get()}),
                               progress_color=self.accent_gold)
        if self.temp_state.get("add_toc", True): sw_toc.select()
        sw_toc.pack(anchor="w", pady=5)

        sw_metadata = ctk.CTkSwitch(scroll, text=self.t("setting_metadata"),
                                    command=lambda: self.temp_state.update({"add_metadata": sw_metadata.get()}),
                                    progress_color=self.accent_gold)
        if self.temp_state.get("add_metadata", True): sw_metadata.select()
        sw_metadata.pack(anchor="w", pady=5)

        sw_bilingual = ctk.CTkSwitch(scroll, text=self.t("setting_bilingual"),
                                     command=lambda: self.temp_state.update({"bilingual_mode": sw_bilingual.get()}),
                                     progress_color=self.accent_gold)
        if self.temp_state.get("bilingual_mode", False): sw_bilingual.select()
        sw_bilingual.pack(anchor="w", pady=5)

        sw_images = ctk.CTkSwitch(scroll, text=self.t("setting_images"),
                                  command=lambda: self.temp_state.update({"download_images": sw_images.get()}),
                                  progress_color=self.accent_gold)
        if self.temp_state.get("download_images", True): sw_images.select()
        sw_images.pack(anchor="w", pady=5)

        sw_auto_open = ctk.CTkSwitch(scroll, text=self.t("setting_auto_open"),
                                     command=lambda: self.temp_state.update({"auto_open": sw_auto_open.get()}),
                                     progress_color=self.accent_gold)
        if self.temp_state.get("auto_open", True): sw_auto_open.select()
        sw_auto_open.pack(anchor="w", pady=5)

        ctk.CTkLabel(scroll, text=self.t("theme_lbl"), font=("Inter", 16, "bold")).pack(anchor="w", pady=(15, 0))
        theme_sw = ctk.CTkSwitch(scroll, text=self.t("theme_dark"), command=self.toggle_temp_theme,
                                 progress_color=self.accent_gold)
        if self.temp_state["theme"] == "dark": theme_sw.select()
        theme_sw.pack(anchor="w", pady=10)

        about_btn = ctk.CTkButton(scroll, text=self.t("btn_about"), fg_color="transparent", border_width=1,
                                  border_color=self.accent_gold, text_color=self.accent_gold,
                                  command=self.show_about_screen)
        about_btn.pack(pady=(30, 10))

        hidden_premium = ctk.CTkButton(scroll, text="v4.0 👑", fg_color="transparent",
                                       text_color="gray30", hover_color="#2d2d2d", font=("Inter", 12),
                                       command=self.show_premium_joke)
        hidden_premium.pack(pady=(10, 20))

    def update_font_size(self, v):
        val = int(v)
        self.temp_state["font_size"] = val
        self.size_val_label.configure(text=str(val))

    def change_ui_language(self, choice):
        self.temp_state["ui_language"] = "uk" if choice == "Українська" else "en"
        self.show_settings_screen()

    def open_donation_link(self):
        webbrowser.open("https://send.monobank.ua/jar/328DrBEZXY")

    def show_about_screen(self):
        self.clear_screen()
        back_btn = ctk.CTkButton(self.main_container, text="←", width=50, height=50, fg_color="transparent",
                                 text_color=self.accent_gold, font=("Arial", 40, "bold"),
                                 command=self.show_settings_screen)
        back_btn.place(relx=0.07, rely=0.07, anchor="center")
        ctk.CTkLabel(self.main_container, text=self.t("about_title"), font=("Georgia", 40, "bold"),
                     text_color=self.accent_gold).pack(pady=(60, 10))
        ctk.CTkLabel(self.main_container, text="🏛️", font=("Arial", 60)).pack(pady=5)

        desc_box = ctk.CTkTextbox(self.main_container, width=750, height=180, font=("Inter", 15),
                                  wrap="word", fg_color="transparent")
        desc_box.pack(pady=10)
        desc_box.insert("1.0", self.t("about_desc"))
        desc_box.configure(state="disabled")

        buttons_frame1 = ctk.CTkFrame(self.main_container, fg_color="transparent")
        buttons_frame1.pack(pady=10)

        how_btn = ctk.CTkButton(buttons_frame1, text=self.t("btn_how_it_works"), height=45, width=220, corner_radius=15,
                                fg_color="#2980b9", hover_color="#3498db", command=self.show_how_it_works_screen)
        how_btn.pack(side="left", padx=10)

        # ТУТ КНОПКУ ЗМІНЕНО НА "ФУНКЦІЇ"
        features_btn = ctk.CTkButton(buttons_frame1, text=self.t("btn_features"), height=45, width=220,
                                     corner_radius=15, fg_color=self.accent_green, command=self.show_features_screen)
        features_btn.pack(side="right", padx=10)

        donate_btn = ctk.CTkButton(self.main_container, text=self.t("btn_donate"), height=45, width=220,
                                   corner_radius=15, fg_color="#d35400", hover_color="#e67e22",
                                   command=self.open_donation_link)
        donate_btn.pack(pady=20)

    def show_how_it_works_screen(self):
        self.clear_screen()
        back_btn = ctk.CTkButton(self.main_container, text="←", width=50, height=50, fg_color="transparent",
                                 text_color=self.accent_gold, font=("Arial", 40, "bold"),
                                 command=self.show_about_screen)
        back_btn.place(relx=0.07, rely=0.07, anchor="center")
        ctk.CTkLabel(self.main_container, text=self.t("how_it_works_title"), font=("Georgia", 34, "bold"),
                     text_color=self.accent_gold).pack(pady=(80, 20))

        textbox = ctk.CTkTextbox(self.main_container, width=750, height=450, font=("Inter", 16), wrap="word")
        textbox.pack(pady=20)
        textbox.insert("1.0", self.t("how_it_works_text"))
        textbox.configure(state="disabled")

    # ТУТ ФУНКЦІЮ ЗМІНЕНО ДЛЯ ВІДОБРАЖЕННЯ СПИСКУ ФУНКЦІЙ
    def show_features_screen(self):
        self.clear_screen()
        back_btn = ctk.CTkButton(self.main_container, text="←", width=50, height=50, fg_color="transparent",
                                 text_color=self.accent_gold, font=("Arial", 40, "bold"),
                                 command=self.show_about_screen)
        back_btn.place(relx=0.07, rely=0.07, anchor="center")
        ctk.CTkLabel(self.main_container, text=self.t("features_title"), font=("Georgia", 34, "bold"),
                     text_color=self.accent_gold).pack(pady=(80, 20))
        textbox = ctk.CTkTextbox(self.main_container, width=750, height=400, font=("Inter", 16), wrap="word")
        textbox.pack(pady=20)
        textbox.insert("1.0", self.t("features_text"))
        textbox.configure(state="disabled")

    def toggle_temp_theme(self):
        new_theme = "light" if self.temp_state["theme"] == "dark" else "dark"
        self.temp_state["theme"] = new_theme
        ctk.set_appearance_mode(new_theme)

    def change_path(self):
        p = filedialog.askdirectory()
        if p:
            self.temp_state["save_path"] = p
            self.path_lbl.configure(text=p)

    def translate_text(self, text):
        if not text or len(text.strip()) < 5: return text
        target_name = self.state.get("target_lang_name", "Українська")
        target_code = self.translation_languages.get(target_name, "uk")

        # ЛОГІКА ПЕРЕКЛАДАЧА: ПРІОРИТЕТ ЗІ СТРАХОВКОЮ
        engine = self.state.get("translation_engine", "Google Translator")

        if engine == "Microsoft Translator":
            try:
                # Пріоритет: Microsoft
                return MicrosoftTranslator(target=target_code).translate(text)
            except:
                try:
                    # Страховка: Google
                    return GoogleTranslator(source='auto', target=target_code).translate(text)
                except:
                    return text
        else:
            try:
                # Пріоритет: Google
                return GoogleTranslator(source='auto', target=target_code).translate(text)
            except:
                try:
                    # Страховка: Microsoft
                    return MicrosoftTranslator(target=target_code).translate(text)
                except:
                    return text

    def open_saved_file(self, path):
        try:
            if platform.system() == 'Darwin':
                subprocess.call(('open', path))
            elif platform.system() == 'Windows':
                os.startfile(path)
            else:
                subprocess.call(('xdg-open', path))
        except Exception:
            pass

    def cancel_process(self):
        self.cancel_event.set()
        self.save_btn.configure(state="normal")
        self.cancel_btn.configure(state="disabled", fg_color="transparent")
        self.update_status(self.t("status_cancelled"), self.accent_red)
        self.progress_bar.pack_forget()

    def is_valid_url(self, url):
        parsed = urllib.parse.urlparse(url)
        return all([parsed.scheme in ['http', 'https'], parsed.netloc])

    def show_system_notification(self, title, message):
        try:
            notification.notify(title=title, message=message, timeout=5)
        except:
            pass

    def batch_worker(self, urls):
        driver = None
        try:
            options = Options()
            # Поки що залишаємо браузер видимим, щоб ти бачив, що відбувається
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")

            # ОСЬ ВІН - ТОЙ САМИЙ КОРОТКИЙ РЯДОК, ЯКИЙ ВИМИКАЄ JAVASCRIPT:
            options.add_experimental_option("prefs", {"profile.managed_default_content_settings.javascript": 2})

            try:
                # Сучасний запуск браузера без зайвих милиць
                driver = webdriver.Edge(options=options)
            except Exception as e:
                raise Exception(f"Помилка запуску Edge: {e}")

            total_urls = len(urls)
            is_single_url = (total_urls == 1)

            for index, url in enumerate(urls):
                if self.cancel_event.is_set(): break

                if is_single_url:
                    current_status = self.t("status_single_start")
                else:
                    current_status = self.t("status_magic").format(index + 1, total_urls)

                self.root.after(0, self.update_status, current_status)

                # Заходимо на сайт (JS вимкнено, тому блокувальник не спрацює)
                driver.get(url)

                # Чекаємо 2 секунди (цього достатньо, бо важкі скрипти не вантажаться)
                time.sleep(2)

                # Одразу читаємо чистий текст
                doc_readability = Document(driver.page_source)

                driver.get(url)
                time.sleep(5)

                # Беремо весь код сторінки без Режиму читання
                soup = BeautifulSoup(driver.page_source, "lxml")

                # Шукаємо заголовок
                title_tag = soup.find('title')
                extracted_title = title_tag.get_text() if title_tag else ""
                title = self.translate_text(
                    extracted_title.strip()) if extracted_title else f"Архівна стаття {index + 1}"

                elements = soup.find_all(['p', 'img', 'h2', 'h3', 'h4', 'li', 'blockquote'])

                content_list = []
                total_words = 0
                download_images = self.state.get("download_images", True)

                for el in elements:
                    if el.name in ['p', 'li', 'blockquote', 'h2', 'h3', 'h4']:
                        txt = el.get_text().strip()
                        if len(txt) > 20 and "cookie" not in txt.lower():
                            content_list.append({"type": el.name, "data": txt})
                            total_words += len(txt.split())
                    elif el.name == 'img' and download_images:
                        img_url = el.get('src') or el.get('data-src')
                        if img_url and img_url.startswith('http'):
                            content_list.append({"type": "img", "data": img_url})

                if not content_list:
                    continue

                doc = WordDocument()

                t_p = doc.add_paragraph()
                t_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                t_run = t_p.add_run(title)
                t_run.bold, t_run.font.size, t_run.font.name = True, Pt(22), self.state["font_family"]

                if self.state.get("add_read_time", True):
                    reading_time = max(1, total_words // 150)
                    rt_p = doc.add_paragraph()
                    rt_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    rt_run = rt_p.add_run(f"⏱ Орієнтовний час читання: ~{reading_time} хв.")
                    rt_run.italic = True
                    rt_run.font.color.rgb = doc.styles['Normal'].font.color.rgb
                    rt_run.font.size = Pt(12)

                if self.state.get("add_toc", True):
                    headings = [item for item in content_list if item["type"] in ['h2', 'h3', 'h4']]
                    if headings:
                        doc.add_paragraph()
                        toc_title_p = doc.add_paragraph()
                        toc_title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                        toc_title_run = toc_title_p.add_run(self.t("doc_toc_title"))
                        toc_title_run.bold, toc_title_run.font.name = True, self.state["font_family"]

                        for h in headings:
                            if self.cancel_event.is_set(): return

                            translated_h = self.translate_text(h["data"])
                            h["translated_data"] = translated_h

                            level = int(h["type"][1])
                            indent = Inches((level - 2) * 0.3)

                            toc_p = doc.add_paragraph()
                            toc_p.paragraph_format.left_indent = indent
                            toc_run = toc_p.add_run(f"• {translated_h}")
                            toc_run.font.name = self.state["font_family"]
                            toc_run.font.size = Pt(self.state["font_size"] - 2)

                        doc.add_paragraph()

                total_elements = len(content_list)
                url_hash = hashlib.md5(url.encode()).hexdigest()
                cache_file = os.path.join(self.cache_dir, f"{url_hash}.json")
                cached_data = []

                for i, item in enumerate(content_list):
                    if self.cancel_event.is_set(): return

                    progress_txt = self.t("status_progress").format(f"{i + 1}/{total_elements}")
                    self.root.after(0, self.update_status, progress_txt, self.accent_gold)
                    self.root.after(0, self.progress_bar.set, (i + 1) / total_elements)

                    if item["type"] in ['p', 'li', 'blockquote', 'h2', 'h3', 'h4']:
                        translated = item.get("translated_data")
                        if not translated:
                            translated = self.translate_text(item["data"])

                        cached_data.append({"type": item["type"], "text": translated})
                        with open(cache_file, "w", encoding="utf-8") as f:
                            json.dump(cached_data, f, ensure_ascii=False)

                        if self.state.get("bilingual_mode", False) and item["type"] == 'p':
                            orig_p = doc.add_paragraph()
                            orig_p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                            orig_run = orig_p.add_run(item["data"])
                            orig_run.italic = True
                            orig_run.font.size, orig_run.font.name = Pt(self.state["font_size"] - 2), self.state[
                                "font_family"]

                        if item["type"] in ['h2', 'h3', 'h4']:
                            h_level = int(item["type"][1])
                            h_p = doc.add_heading(translated, level=h_level)
                            h_p.runs[0].font.name = self.state["font_family"]
                        elif item["type"] == 'li':
                            p = doc.add_paragraph(translated, style='List Bullet')
                            p.runs[0].font.name, p.runs[0].font.size = self.state["font_family"], Pt(
                                self.state["font_size"])
                        elif item["type"] == 'blockquote':
                            p = doc.add_paragraph(translated, style='Intense Quote')
                            p.runs[0].font.name, p.runs[0].font.size = self.state["font_family"], Pt(
                                self.state["font_size"])
                        else:
                            p = doc.add_paragraph()
                            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                            run = p.add_run(translated)
                            run.font.size, run.font.name = Pt(self.state["font_size"]), self.state["font_family"]

                    elif item["type"] == "img":
                        try:
                            response = requests.get(item["data"], timeout=5)
                            if response.status_code == 200:
                                image_stream = BytesIO(response.content)
                                img_p = doc.add_paragraph()
                                img_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                                img_run = img_p.add_run()
                                img_run.add_picture(image_stream, width=Inches(5.5))
                        except Exception:
                            pass

                if self.state.get("add_metadata", True):
                    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    meta_p = doc.add_paragraph()
                    meta_p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    meta_text = self.t("metadata_text").format(url, current_date)
                    meta_run = meta_p.add_run(meta_text)
                    meta_run.font.size = Pt(10)
                    meta_run.font.color.rgb = doc.styles['Normal'].font.color.rgb
                    meta_run.italic = True

                safe_title = re.sub(r'[\\/:*?"<>|]', "", title)[:80]
                base_path = os.path.join(self.state["save_path"], safe_title)
                full_path = f"{base_path}.docx"

                counter = 1
                while True:
                    try:
                        doc.save(full_path)
                        break
                    except PermissionError:
                        full_path = f"{base_path} ({counter}).docx"
                        counter += 1

                if os.path.exists(cache_file):
                    os.remove(cache_file)

                final_path = full_path
                if self.state.get("output_format") == "pdf":
                    pdf_path = full_path.replace(".docx", ".pdf")
                    self.root.after(0, self.update_status, self.t("status_pdf"), self.accent_gold)
                    try:
                        convert(full_path, pdf_path)
                        if os.path.exists(full_path):
                            os.remove(full_path)
                        final_path = pdf_path
                    except Exception as e:
                        print(f"Помилка конвертації PDF: {e}")

                if self.state.get("auto_open", True):
                    self.open_saved_file(final_path)

            if not self.cancel_event.is_set():
                self.root.after(0, self.update_status, self.t("status_success"), self.accent_green)
                self.show_system_notification("Скарбниця Знань", "Обробку успішно завершено!")

        except Exception as e:
            if not self.cancel_event.is_set():
                self.root.after(0, lambda err=e: messagebox.showerror("Error", f"{err}"))
                self.root.after(0, self.update_status, self.t("status_error"), "red")

        finally:
            if driver: driver.quit()
            if not self.cancel_event.is_set():
                self.root.after(0, lambda: self.save_btn.configure(state="normal"))
                self.root.after(0, lambda: self.cancel_btn.configure(state="disabled", fg_color="transparent"))
                self.root.after(0, self.progress_bar.pack_forget)

    def run_process(self):
        raw_text = self.url_textbox.get("1.0", "end-1c").strip()
        if raw_text == self.t("placeholder") or not raw_text:
            return

        urls = [u.strip() for u in raw_text.split('\n') if u.strip()]
        valid_urls = [u for u in urls if self.is_valid_url(u)]

        if not valid_urls:
            messagebox.showwarning("Увага", self.t("msg_invalid_url"))
            return

        self.cancel_event.clear()
        self.save_btn.configure(state="disabled")

        self.cancel_btn.configure(state="normal", fg_color=self.accent_red, text_color="white")
        self.progress_bar.pack(pady=10)
        self.progress_bar.set(0)

        threading.Thread(target=self.batch_worker, args=(valid_urls,), daemon=True).start()


if __name__ == "__main__":
    app = TranslationArchiveApp()
    app.root.mainloop()