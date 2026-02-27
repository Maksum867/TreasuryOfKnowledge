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
import warnings
from io import BytesIO
import urllib.parse
from datetime import datetime
import ctypes

import customtkinter as ctk
from tkinter import messagebox, filedialog
from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
from PIL import Image, ImageDraw

from docx import Document as WordDocument
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from plyer import notification

from deep_translator import MicrosoftTranslator, GoogleTranslator
from docx2pdf import convert

import pystray
from pystray import MenuItem as item
import pyperclip

warnings.filterwarnings("ignore", category=UserWarning, module='requests')

# ОПТИМІЗАЦІЯ ПІД WINDOWS 10 ТА 11
try:
    if platform.system() == "Windows":
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass


class TranslationArchiveApp:
    def __init__(self):
        self.config_file = "settings.json"
        self.cache_dir = "backup_cache"

        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

        self.cancel_event = threading.Event()
        self.is_processing = False
        self.quick_menu = None

        self.temple_clicks = 0
        self.empty_clicks = 0
        self.theme_clicks = 0
        self.theme_click_time = 0
        self.title_clicks = 0
        self.font_slider_clicks = 0
        self.cancel_folder_clicks = 0
        self.format_clicks = 0
        self.format_click_time = 0
        self.about_clicks = 0
        self.bilingual_clicks = 0
        self.bilingual_click_time = 0
        self.start_process_time = 0
        self.hacker_mode = False

        self.http_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8'
        }

        self.locales = {
            "uk": {
                "title": "Скарбниця Знань v5.0",
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
                "setting_images": "🖼️ Завантажувати зображення, обкладинки та відео",
                "setting_toc": "📑 Додавати автоматичний Зміст (для довгих статей)",
                "setting_metadata": "🔗 Додавати посилання на джерело в кінці файлу",
                "setting_tray_close": "⏬ Згортати в трей при закритті вікна (для роботи у фоні)",

                "btn_about": "ℹ️ Про додаток",
                "about_title": "Про додаток",
                "about_desc": "Цей додаток створений для вільного доступу до інформації без кордонів та обмежень.\n\nОсновна мета «Скарбниці Знань» — дати вам змогу читати статті, журнали та новини, які заблоковані у вашій країні, приховані за пейволом (paywall) або вимагають платної підписки.",
                "btn_features": "Основні функції ⭐️",
                "btn_how_it_works": "Як це працює ⚙️",
                "btn_donate": "☕ Підтримати автора",
                "btn_feedback": "@ Зворотний зв'язок",

                "how_it_works_title": "Механізм роботи",
                "how_it_works_text": "🔍 Парсинг:\nПрограма використовує 'Снайперський режим' для пошуку тексту та витягує метадані (обкладинку, автора).\n\n🧠 Аналіз:\nАлгоритм відкидає меню, рекламні банери та списки 'схожих новин'.\n\n🌍 Переклад та Збірка:\nАбзаци пропускаються через перекладач і зшиваються у документ разом із картинками.",

                "premium_title": "Доступ до Premium",
                "premium_text": "Вітаю, шукачу ексклюзиву! 🎩\n\nНіякого 'Premium' у цьому додатку немає і ніколи не буде.\n\nКористуйся на здоров'я, розширюй кругозір і нехай ця програма служить тобі вірою і правдою.",

                "features_title": "Можливості додатку",
                "features_text": "Повний перелік функцій Скарбниці Знань:\n\n🔹 Згортання у Трей (робота у фоні)\n🔹 Швидке викачування статті з буфера обміну\n🔹 Обхід пейволів (читання платних статей)\n🔹 Витягування обкладинки, відео, автора та дати\n🔹 Збереження файлів у DOCX та PDF\n🔹 Двомовний режим",
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
                "qm_btn_hide": "🔽 Приховати меню",
                "qm_btn_exit": "❌ Вийти повністю",
                "qm_tray_open": "Відкрити меню"
            },
            "en": {
                "title": "Treasury of Knowledge v5.0",
                "placeholder": "Paste URLs here...",
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

                "additional_features_lbl": "🛠 Features:",
                "setting_read_time": "⏱ Add estimated reading time",
                "setting_bilingual": "📖 Bilingual Mode",
                "setting_auto_open": "🚀 Auto-open document",
                "setting_images": "🖼️ Download images, covers & videos",
                "setting_toc": "📑 Add Table of Contents",
                "setting_metadata": "🔗 Add source URL at the end",
                "setting_tray_close": "⏬ Minimize to tray on close (background mode)",

                "btn_about": "ℹ️ About",
                "about_title": "About Application",
                "about_desc": "Free access to information without borders.\nBypass paywalls and translate articles seamlessly.",
                "btn_features": "Features ⭐️",
                "btn_how_it_works": "How it works ⚙️",
                "btn_donate": "☕ Support Author",
                "btn_feedback": "@ Send Feedback",

                "how_it_works_title": "How It Works",
                "how_it_works_text": "Scraping, Cleaning, Translating and Assembling.",
                "premium_title": "Premium Access",
                "premium_text": "There is no 'Premium' in this app. Enjoy!",
                "features_title": "App Features",
                "features_text": "Background tray mode, fast clipboard parsing, bypass paywalls, extract covers, auto-translate, save PDF.",
                "btn_back": "Go Back",

                "status_single_start": "🌐 Processing...",
                "status_magic": "🌐 Batch processing ({} of {})...",
                "status_progress": "📜 Element {} of {}...",
                "status_success": "✅ Successfully saved!",
                "status_error": "❌ Error",
                "status_cancelled": "🛑 Cancelled",
                "status_pdf": "📄 Converting to PDF...",
                "msg_error_txt": "No content found.",
                "msg_invalid_url": "Invalid URL.",
                "doc_toc_title": "--- TABLE OF CONTENTS ---",
                "metadata_text": "\n\n---\n🔗 Source: {}\n📅 Saved: {}",
                "video_link_text": "▶️ [Watch attached video]",
                "tray_clipboard_err": "No URL found in clipboard!",
                "tray_processing_err": "App is already processing!",

                "qm_btn_paste": "📥 Digitize clipboard",
                "qm_btn_open": "🖥️ Open Main App",
                "qm_btn_hide": "🔽 Hide Menu",
                "qm_btn_exit": "❌ Quit App",
                "qm_tray_open": "Open Menu"
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
        self.root.protocol('WM_DELETE_WINDOW', self.on_closing)

        self.accent_gold = "#d4af37"
        self.accent_green = "#2d5a27"
        self.accent_red = "#8b0000"

        ctk.set_appearance_mode(self.state.get("theme", "dark"))
        self.update_window_title()

        try:
            self.root.iconbitmap('icon.ico')
        except Exception:
            pass

        self.main_container = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True)

        self.show_main_screen()
        self.setup_tray()

    # =========================================================================
    # ПАСХАЛКИ
    # =========================================================================
    def on_temple_click(self, event):
        self.temple_clicks += 1
        if self.temple_clicks == 7:
            self.hacker_mode = True
            ctk.set_appearance_mode("dark")
            self.accent_gold = "#00FF00"
            self.accent_green = "#00FF00"
            self.update_status("Ви знайшли секретний підвал Храму! Тепер ви Верховний Жрець Знань 🧙‍♂️", "#00FF00")
            self.show_main_screen()

    def on_title_click(self, event):
        self.title_clicks += 1
        if self.title_clicks == 3:
            self.main_title_label.configure(text="Бібліотека Піратів 🏴‍☠️")
            self.root.after(2000, lambda: self.main_title_label.configure(text="Робін Гуд PDF-формату 🏹"))
            self.root.after(4000, lambda: self.main_title_label.configure(text=self.t("title").split(" v")[0]))
            self.title_clicks = 0

    def trigger_matrix_effect(self):
        self.url_textbox.delete("1.0", "end")
        msg = "The Matrix has you... Follow the white rabbit 🐇"

        def type_char(index=0):
            if index < len(msg):
                self.url_textbox.insert("end", msg[index])
                self.root.after(100, type_char, index + 1)
            else:
                self.root.after(3000, lambda: self.url_textbox.delete("1.0", "end"))

        type_char()

    # =========================================================================

    def on_closing(self):
        if self.state.get("minimize_to_tray", False):
            self.root.withdraw()
            lang = self.state.get("ui_language", "uk")
            msg = "Програму згорнуто в трей. Вона готова до фонової роботи." if lang == "uk" else "App minimized to tray. Ready for background tasks."
            self.show_system_notification("Скарбниця Знань v5.0", msg)
        else:
            self.quit_app()

    def setup_tray(self):
        try:
            image = Image.open("icon.ico")
        except Exception:
            image = Image.new('RGB', (64, 64), color=(30, 30, 30))
            d = ImageDraw.Draw(image)
            d.rectangle([12, 12, 52, 52], fill=(212, 175, 55))

        lang = self.state.get("ui_language", "uk")
        menu = pystray.Menu(item(self.locales[lang]["qm_tray_open"], self.trigger_quick_menu, default=True))
        app_title = self.locales[lang]["title"]
        self.tray_icon = pystray.Icon("TreasuryOfKnowledge", image, app_title, menu)
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def trigger_quick_menu(self, icon=None, item=None):
        self.root.after(0, self.show_quick_menu)

    def show_quick_menu(self):
        if self.quick_menu is not None and self.quick_menu.winfo_exists():
            self.quick_menu.focus_force()
            return

        self.quick_menu = ctk.CTkToplevel(self.root)
        self.quick_menu.overrideredirect(True)
        self.quick_menu.attributes("-topmost", True)

        w, h = 280, 260
        sw = self.quick_menu.winfo_screenwidth()
        sh = self.quick_menu.winfo_screenheight()
        x = sw - w - 20
        y = sh - h - 60

        self.quick_menu.geometry(f"{w}x{h}+{x}+{y}")

        main_frame = ctk.CTkFrame(self.quick_menu, fg_color="#1e1e1e", border_width=2, border_color=self.accent_gold,
                                  corner_radius=15)
        main_frame.pack(fill="both", expand=True)

        ctk.CTkLabel(main_frame, text=self.t("title").split(" v")[0], font=("Georgia", 18, "bold"),
                     text_color=self.accent_gold).pack(pady=(15, 10))
        ctk.CTkButton(main_frame, text=self.t("qm_btn_paste"), fg_color=self.accent_green, hover_color="#1e3d1a",
                      font=("Inter", 15, "bold"), height=40, command=self.quick_process_and_close).pack(pady=5, padx=20,
                                                                                                        fill="x")
        ctk.CTkButton(main_frame, text=self.t("qm_btn_open"), fg_color="#2980b9", hover_color="#1c5980",
                      font=("Inter", 14), height=35, command=self.show_main_and_close).pack(pady=5, padx=20, fill="x")
        ctk.CTkButton(main_frame, text=self.t("qm_btn_hide"), fg_color="transparent", border_width=1,
                      border_color="gray50", text_color="gray80", font=("Inter", 12), height=30,
                      command=self.close_quick_menu).pack(pady=(10, 5), padx=20, fill="x")
        ctk.CTkButton(main_frame, text=self.t("qm_btn_exit"), fg_color="transparent", text_color=self.accent_red,
                      hover_color="#4a0000", font=("Inter", 12, "bold"), height=30, command=self.quit_app).pack(
            pady=(0, 15), padx=20, fill="x")

    def close_quick_menu(self):
        if self.quick_menu is not None and self.quick_menu.winfo_exists():
            self.quick_menu.destroy()
            self.quick_menu = None

    def quick_process_and_close(self):
        self.close_quick_menu()
        if self.is_processing:
            self.show_system_notification("Скарбниця Знань", self.t("tray_processing_err"))
            return

        clipboard_text = pyperclip.paste().strip()

        if any(w in clipboard_text.lower() for w in ["пароль", "password", "123456"]):
            self.show_system_notification("Скарбниця Знань",
                                          "Я парсер статей, а не крадій паролів! (Але я його запам'ятав 🕵️‍♂️)")
            return

        if not self.is_valid_url(clipboard_text):
            self.show_system_notification("Скарбниця Знань", self.t("tray_clipboard_err"))
            return

        self.show_system_notification("Скарбниця Знань", f"Фонова обробка: {clipboard_text[:40]}...")
        self.prepare_ui_for_processing()
        threading.Thread(target=self.batch_worker, args=([clipboard_text],), daemon=True).start()

    def show_main_and_close(self):
        self.close_quick_menu()
        self.root.deiconify()

    def quit_app(self):
        self.close_quick_menu()
        if hasattr(self, 'tray_icon'):
            self.tray_icon.stop()
        self.root.quit()
        os._exit(0)

    def prepare_ui_for_processing(self):
        self.cancel_event.clear()
        self.save_btn.configure(state="disabled")
        self.cancel_btn.configure(state="normal", fg_color=self.accent_red, text_color="white")
        self.progress_bar.pack(pady=10)
        self.progress_bar.set(0)

    # =========================================================================

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
            "add_metadata": True,
            "minimize_to_tray": False
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
        st = self.temp_state
        if not any([st["add_read_time"], st["add_toc"], st["add_metadata"], st["bilingual_mode"], st["download_images"],
                    st["auto_open"]]):
            self.update_status("Режим Максимальної Аскези увімкнено. Тільки текст, тільки хардкор! 🥷💨",
                               self.accent_gold)

        self.state = self.temp_state.copy()
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(self.state, f, ensure_ascii=False, indent=4)
        self.update_window_title()
        self.show_main_screen()
        self.tray_icon.stop()
        self.setup_tray()

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
        temple_label.bind("<Button-1>", self.on_temple_click)

        self.main_title_label = ctk.CTkLabel(title_frame, text=self.t("title").split(" v")[0],
                                             font=("Georgia", 58, "bold"), text_color=self.accent_gold)
        self.main_title_label.pack(pady=(40, 0))
        self.main_title_label.bind("<Button-1>", self.on_title_click)

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

        self.status_label = ctk.CTkLabel(self.main_container, text=self.t("status_wait"), font=("Inter", 18, "italic"),
                                         text_color=("gray20", "gray80"))
        self.status_label.pack(pady=5)

        btn_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        btn_frame.pack(pady=20)

        self.save_btn = ctk.CTkButton(btn_frame, text=self.t("btn_digitize"), font=("Inter", 24, "bold"),
                                      fg_color=self.accent_green, hover_color="#1e3d1a", height=75, width=350,
                                      corner_radius=20,
                                      command=self.run_process)
        self.save_btn.pack(side="left", padx=10)

        self.cancel_btn = ctk.CTkButton(btn_frame, text=self.t("btn_cancel"), font=("Inter", 20, "bold"),
                                        fg_color="transparent", border_width=2, border_color=self.accent_red,
                                        text_color=self.accent_red, hover_color="#4a0000", height=75, width=150,
                                        corner_radius=20,
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
        lang_combo = ctk.CTkComboBox(scroll, values=["Українська", "English", "Ельфійська (Sindarin)"], width=300,
                                     command=self.change_ui_language)
        lang_combo.set("Українська" if self.temp_state["ui_language"] == "uk" else "English")
        lang_combo.pack(anchor="w", pady=5)

        ctk.CTkLabel(scroll, text=self.t("target_lang_lbl"), font=("Inter", 16, "bold")).pack(anchor="w", pady=(10, 0))
        target_combo = ctk.CTkComboBox(scroll, values=list(self.translation_languages.keys()), width=300,
                                       command=lambda v: self.temp_state.update({"target_lang_name": v}))
        target_combo.set(self.temp_state["target_lang_name"])
        target_combo.pack(anchor="w", pady=5)

        ctk.CTkLabel(scroll, text=self.t("engine_lbl"), font=("Inter", 16, "bold")).pack(anchor="w", pady=(10, 0))
        engine_combo = ctk.CTkComboBox(scroll, values=["Google Translator", "Microsoft Translator", "Skynet v2.0"],
                                       width=300,
                                       command=self.change_engine)
        engine_combo.set(self.temp_state.get("translation_engine", "Google Translator"))
        engine_combo.pack(anchor="w", pady=5)

        ctk.CTkLabel(scroll, text=self.t("path_lbl"), font=("Inter", 16, "bold")).pack(anchor="w", pady=(10, 0))
        path_f = ctk.CTkFrame(scroll, fg_color="transparent")
        path_f.pack(fill="x", pady=5)
        self.path_lbl = ctk.CTkLabel(path_f, text=self.temp_state["save_path"], wraplength=550)
        self.path_lbl.pack(side="left")
        ctk.CTkButton(path_f, text=self.t("btn_choose"), command=self.change_path).pack(side="right")

        ctk.CTkLabel(scroll, text=self.t("font_lbl"), font=("Inter", 16, "bold")).pack(anchor="w", pady=(10, 0))
        f_combo = ctk.CTkComboBox(scroll, values=["Georgia", "Arial", "Times New Roman", "Comic Sans MS"], width=300,
                                  command=self.change_font)
        f_combo.set(self.temp_state["font_family"])
        f_combo.pack(anchor="w", pady=5)

        ctk.CTkLabel(scroll, text=self.t("format_lbl"), font=("Inter", 16, "bold")).pack(anchor="w", pady=(10, 0))
        self.format_combo = ctk.CTkComboBox(scroll, values=["docx", "pdf"], width=300, command=self.change_format)
        self.format_combo.set(self.temp_state.get("output_format", "docx"))
        self.format_combo.pack(anchor="w", pady=5)

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
                     text_color=self.accent_gold).pack(anchor="w", pady=(20, 5))

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

        self.sw_bilingual = ctk.CTkSwitch(scroll, text=self.t("setting_bilingual"), command=self.toggle_bilingual,
                                          progress_color=self.accent_gold)
        if self.temp_state.get("bilingual_mode", False): self.sw_bilingual.select()
        self.sw_bilingual.pack(anchor="w", pady=5)

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

        sw_tray = ctk.CTkSwitch(scroll, text=self.t("setting_tray_close"),
                                command=lambda: self.temp_state.update({"minimize_to_tray": sw_tray.get()}),
                                progress_color=self.accent_gold)
        if self.temp_state.get("minimize_to_tray", False): sw_tray.select()
        sw_tray.pack(anchor="w", pady=5)

        ctk.CTkLabel(scroll, text=self.t("theme_lbl"), font=("Inter", 16, "bold")).pack(anchor="w", pady=(15, 0))
        self.theme_sw = ctk.CTkSwitch(scroll, text=self.t("theme_dark"), command=self.toggle_temp_theme,
                                      progress_color=self.accent_gold)
        if self.temp_state["theme"] == "dark": self.theme_sw.select()
        self.theme_sw.pack(anchor="w", pady=10)

        self.btn_about_widget = ctk.CTkButton(scroll, text=self.t("btn_about"), fg_color="transparent", border_width=1,
                                              border_color=self.accent_gold, text_color=self.accent_gold,
                                              command=self.on_about_click)
        self.btn_about_widget.pack(pady=(30, 10))

        hidden_premium = ctk.CTkButton(scroll, text="v5.0 👑", fg_color="transparent",
                                       text_color="gray30", hover_color="#2d2d2d", font=("Inter", 12),
                                       command=self.show_premium_joke)
        hidden_premium.pack(pady=(10, 20))

    def change_ui_language(self, choice):
        if choice == "Ельфійська (Sindarin)":
            messagebox.showerror("Мордорська помилка",
                                 "Помилка API: Словник ельфійської мови згорів у Мордорі. Будь ласка, оберіть людську мову 🧝‍♂️🔥")
            self.temp_state["ui_language"] = "uk"
        else:
            self.temp_state["ui_language"] = "uk" if choice == "Українська" else "en"
        self.show_settings_screen()

    def change_engine(self, choice):
        if choice == "Skynet v2.0":
            messagebox.showwarning("Skynet",
                                   "Помилка: Skynet зараз зайнятий захопленням світу. Повертаємось до Google 🤖🔥")
            self.temp_state["translation_engine"] = "Google Translator"
        else:
            self.temp_state["translation_engine"] = choice
        self.show_settings_screen()

    def change_font(self, choice):
        if choice == "Comic Sans MS":
            messagebox.showinfo("Шрифт Лікарів",
                                "Серйозно? Comic Sans? Ваші очі вам цього не пробачать... але як скажете 🤡")
        self.temp_state["font_family"] = choice

    def change_format(self, choice):
        curr_time = time.time()
        if curr_time - self.format_click_time < 2.0:
            self.format_clicks += 1
            if self.format_clicks >= 4:
                messagebox.showinfo("Криза ідентичності", "Визначся вже! Я тобі Microsoft Word чи Acrobat Reader? 🤯📄")
                self.format_clicks = 0
        else:
            self.format_clicks = 1
        self.format_click_time = curr_time
        self.temp_state["output_format"] = choice

    def toggle_bilingual(self):
        curr_time = time.time()
        if curr_time - self.bilingual_click_time < 1.0:
            self.bilingual_clicks += 1
            if self.bilingual_clicks >= 4:
                self.sw_bilingual.configure(text="My brain is melting. Мій мозок плавиться. 🧠🔥", text_color="red")
                self.bilingual_clicks = 0
        else:
            self.bilingual_clicks = 1
        self.bilingual_click_time = curr_time
        self.temp_state.update({"bilingual_mode": self.sw_bilingual.get()})

    def on_about_click(self):
        self.about_clicks += 1
        if self.about_clicks >= 5:
            self.btn_about_widget.configure(text="Так-так, автор геній, ми вже зрозуміли. Давай краще статті качати! 🏆")
        else:
            self.show_about_screen()

    def update_font_size(self, v):
        val = int(v)
        self.temp_state["font_size"] = val
        if val == 24:
            self.font_slider_clicks += 1
            if self.font_slider_clicks >= 3:
                self.size_val_label.configure(text="24 (Ти збираєшся читати це з іншої кімнати? 🔭)")
                return
        else:
            self.font_slider_clicks = 0
        self.size_val_label.configure(text=str(val))

    def toggle_temp_theme(self):
        curr_time = time.time()
        if curr_time - self.theme_click_time < 1.0:
            self.theme_clicks += 1
            if self.theme_clicks >= 5:
                messagebox.showwarning("Світломузика",
                                       "Зупинись! Ти хочеш, щоб у мене стався епілептичний напад? Залишаємо темну! 😵‍💫🕶️")
                self.temp_state["theme"] = "dark"
                ctk.set_appearance_mode("dark")
                self.theme_sw.select()
                self.theme_clicks = 0
                return
        else:
            self.theme_clicks = 1
        self.theme_click_time = curr_time

        new_theme = "light" if self.temp_state["theme"] == "dark" else "dark"
        self.temp_state["theme"] = new_theme
        ctk.set_appearance_mode(new_theme)

    def change_path(self):
        p = filedialog.askdirectory()
        if p:
            self.temp_state["save_path"] = p
            self.path_lbl.configure(text=p)
            self.cancel_folder_clicks = 0
        else:
            self.cancel_folder_clicks += 1
            if self.cancel_folder_clicks >= 3:
                messagebox.showinfo("Шлях у нікуди",
                                    "Які ми сьогодні нерішучі... Зберігай на Робочий стіл, як всі нормальні люди! 🤷‍♂️")
                self.cancel_folder_clicks = 0

    # =========================================================================
    # ВІКНО "ПРО ДОДАТОК" ТА БРОНЬОВАНА КНОПКА ФІДБЕКУ
    # =========================================================================
    def open_donation_link(self):
        webbrowser.open("https://send.monobank.ua/jar/328DrBEZXY")

    def open_feedback_link(self):
        # ⚠️ ВПИШИ ТУТ СВОЮ НОВУ ПОШТУ ЗАМІСТЬ EMAIL_HERE ⚠️
        email = "treasuryofknowledge26@gmail.com"
        subject = "Відгук про Скарбницю Знань v5.0"

        # 1. 100% надійно: спочатку тихо копіюємо в буфер
        try:
            pyperclip.copy(email)
        except Exception:
            pass

        # 2. Намагаємося відкрити поштовик
        try:
            webbrowser.open(f"mailto:{email}?subject={urllib.parse.quote(subject)}", new=1)
        except Exception:
            pass

        # 3. Гарантоване повідомлення для користувача
        msg_text = (
            f"Адресу {email} успішно скопійовано в буфер обміну!\n\n"
            "Якщо ваша поштова програма не відкрилася автоматично, просто вставте цю адресу в поле 'Кому'."
        )
        messagebox.showinfo("Зворотний зв'язок", msg_text)

    def show_about_screen(self):
        self.clear_screen()
        back_btn = ctk.CTkButton(self.main_container, text="←", width=50, height=50, fg_color="transparent",
                                 text_color=self.accent_gold, font=("Arial", 40, "bold"),
                                 command=self.show_settings_screen)
        back_btn.place(relx=0.07, rely=0.07, anchor="center")
        ctk.CTkLabel(self.main_container, text=self.t("about_title"), font=("Georgia", 40, "bold"),
                     text_color=self.accent_gold).pack(pady=(60, 10))
        ctk.CTkLabel(self.main_container, text="🏛️", font=("Arial", 60)).pack(pady=5)

        desc_box = ctk.CTkTextbox(self.main_container, width=750, height=180, font=("Inter", 15), wrap="word",
                                  fg_color="transparent")
        desc_box.pack(pady=10)
        desc_box.insert("1.0", self.t("about_desc"))
        desc_box.configure(state="disabled")

        buttons_frame1 = ctk.CTkFrame(self.main_container, fg_color="transparent")
        buttons_frame1.pack(pady=10)
        ctk.CTkButton(buttons_frame1, text=self.t("btn_how_it_works"), height=45, width=220, corner_radius=15,
                      font=("Inter", 15, "bold"), fg_color="#2980b9", hover_color="#3498db",
                      command=self.show_how_it_works_screen).pack(side="left", padx=10)
        ctk.CTkButton(buttons_frame1, text=self.t("btn_features"), height=45, width=220, corner_radius=15,
                      font=("Inter", 15, "bold"), fg_color=self.accent_green, hover_color="#1e3d1a",
                      command=self.show_features_screen).pack(side="right", padx=10)

        buttons_frame2 = ctk.CTkFrame(self.main_container, fg_color="transparent")
        buttons_frame2.pack(pady=(0, 20))
        ctk.CTkButton(buttons_frame2, text=self.t("btn_donate"), height=45, width=220, corner_radius=15,
                      font=("Inter", 15, "bold"), fg_color="#d35400", hover_color="#e67e22",
                      command=self.open_donation_link).pack(side="left", padx=10)
        ctk.CTkButton(buttons_frame2, text=self.t("btn_feedback"), height=45, width=220, corner_radius=15,
                      font=("Inter", 15, "bold"), fg_color="#4b4b4b", hover_color="#333333",
                      command=self.open_feedback_link).pack(side="right", padx=10)

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

    def translate_text(self, text):
        if not text or len(text.strip()) < 5: return text
        target_name = self.state.get("target_lang_name", "Українська")
        target_code = self.translation_languages.get(target_name, "uk")

        engine = self.state.get("translation_engine", "Google Translator")

        if engine == "Microsoft Translator":
            try:
                return MicrosoftTranslator(target=target_code).translate(text)
            except:
                try:
                    return GoogleTranslator(source='auto', target=target_code).translate(text)
                except:
                    return text
        else:
            try:
                return GoogleTranslator(source='auto', target=target_code).translate(text)
            except:
                try:
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
        self.is_processing = False
        if time.time() - self.start_process_time < 2.0:
            self.update_status("🛑 Скасовано. Ти що, забув вимкнути праску вдома? 🏃‍♂️💨", self.accent_red)
        else:
            self.update_status(self.t("status_cancelled"), self.accent_red)

        self.save_btn.configure(state="normal")
        self.cancel_btn.configure(state="disabled", fg_color="transparent")
        self.progress_bar.pack_forget()

    def is_valid_url(self, url):
        parsed = urllib.parse.urlparse(url)
        return all([parsed.scheme in ['http', 'https'], parsed.netloc])

    def show_system_notification(self, title, message):
        try:
            icon_path = "icon.ico" if os.path.exists("icon.ico") else None
            notification.notify(title=title, message=message, app_icon=icon_path, timeout=5)
        except:
            pass

    def get_browser_driver(self):
        try:
            options = EdgeOptions()
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_experimental_option("prefs", {"profile.managed_default_content_settings.javascript": 2})
            return webdriver.Edge(options=options)
        except Exception:
            try:
                options = ChromeOptions()
                options.add_argument("--headless=new")
                options.add_argument("--disable-gpu")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_experimental_option("prefs", {"profile.managed_default_content_settings.javascript": 2})
                return webdriver.Chrome(options=options)
            except Exception:
                raise Exception("Не вдалося запустити ні Edge, ні Chrome браузер на цьому ПК.")

    def convert_image_for_docx(self, image_bytes):
        try:
            img = Image.open(BytesIO(image_bytes))
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            elif img.mode != "RGB":
                img = img.convert("RGB")
            output = BytesIO()
            img.save(output, format="JPEG")
            output.seek(0)
            return output
        except Exception:
            return None

    def resolve_url(self, url, base_url):
        if not url: return ""
        if url.startswith('data:image'): return ""
        if url.startswith('http'): return url
        if url.startswith('//'): return 'https:' + url
        return urllib.parse.urljoin(base_url, url)

    def extract_metadata(self, soup, base_url):
        meta = {"title": "", "subtitle": "", "author": "", "date": "", "cover_image": ""}

        def safe_get(d, key, default=""):
            if isinstance(d, dict): return d.get(key, default)
            return default

        try:
            og_img = soup.find('meta', property='og:image') or soup.find('meta', attrs={'name': 'twitter:image'})
            if og_img and og_img.get('content'): meta['cover_image'] = self.resolve_url(og_img['content'], base_url)
        except Exception:
            pass

        try:
            json_scripts = soup.find_all('script', type='application/ld+json')
            for script in json_scripts:
                if not script.string: continue
                try:
                    raw_data = json.loads(script.string)
                    article_data = None
                    if isinstance(raw_data, list):
                        for item in raw_data:
                            if isinstance(item, dict) and safe_get(item, '@type') in ['NewsArticle', 'Article',
                                                                                      'ReportageNewsArticle',
                                                                                      'WebPage']:
                                article_data = item
                                break
                        if not article_data and len(raw_data) > 0 and isinstance(raw_data[0], dict): article_data = \
                        raw_data[0]
                    elif isinstance(raw_data, dict):
                        article_data = raw_data
                    if not isinstance(article_data, dict): continue

                    if '@graph' in article_data and isinstance(article_data['@graph'], list):
                        for graph_item in article_data['@graph']:
                            if isinstance(graph_item, dict) and safe_get(graph_item, '@type') in ['NewsArticle',
                                                                                                  'Article', 'WebPage']:
                                article_data = graph_item
                                break

                    if not meta['title']: meta['title'] = safe_get(article_data, 'headline') or safe_get(article_data,
                                                                                                         'name')
                    if not meta['subtitle']: meta['subtitle'] = safe_get(article_data, 'description')
                    if not meta['date']:
                        d_val = safe_get(article_data, 'datePublished')
                        meta['date'] = str(d_val).split('T')[0] if d_val else ''

                    author_data = safe_get(article_data, 'author')
                    if isinstance(author_data, list):
                        authors = [safe_get(a, 'name') for a in author_data if isinstance(a, dict)]
                        meta['author'] = ", ".join(filter(None, authors))
                    else:
                        meta['author'] = safe_get(author_data, 'name') if isinstance(author_data, dict) else str(
                            author_data or "")

                    if not meta['cover_image']:
                        img_data = safe_get(article_data, 'image')
                        if isinstance(img_data, list) and len(img_data) > 0:
                            raw_img = safe_get(img_data[0], 'url') if isinstance(img_data[0], dict) else str(
                                img_data[0])
                        elif isinstance(img_data, dict):
                            raw_img = safe_get(img_data, 'url')
                        elif isinstance(img_data, str):
                            raw_img = img_data
                        meta['cover_image'] = self.resolve_url(raw_img, base_url)
                except Exception:
                    continue
        except Exception:
            pass

        try:
            if not meta['title']:
                t = soup.find('meta', property='og:title') or soup.find('meta', attrs={'name': 'title'})
                meta['title'] = t['content'] if (t and t.has_attr('content')) else ""
            if not meta['subtitle']:
                d = soup.find('meta', property='og:description') or soup.find('meta', attrs={'name': 'description'})
                meta['subtitle'] = d['content'] if (d and d.has_attr('content')) else ""
            if not meta['author']:
                a = soup.find('meta', attrs={'name': 'author'}) or soup.find('meta', property='article:author')
                meta['author'] = a['content'] if (a and a.has_attr('content')) else ""
        except Exception:
            pass

        return meta

    def clean_junk_html(self, soup):
        try:
            for unwanted in soup(['nav', 'aside', 'footer', 'header', 'script', 'style', 'button', 'form', 'svg']):
                try:
                    unwanted.decompose()
                except Exception:
                    pass

            junk_keywords = ['newsletter', 'promo', 'recirc', 'related', 'recommend', 'social', 'share', 'author-bio',
                             'bottom', 'ad-', 'advertisement', 'trending']

            for tag in soup.find_all(['div', 'section', 'ul']):
                try:
                    c_list = tag.get('class', [])
                    class_str = ' '.join(c_list).lower() if isinstance(c_list, list) else str(c_list).lower()
                    id_str = str(tag.get('id', '')).lower()
                    if any(k in class_str or k in id_str for k in junk_keywords): tag.decompose()
                except Exception:
                    continue
        except Exception:
            pass
        return soup

    def batch_worker(self, urls):
        self.is_processing = True
        driver = None
        try:
            driver = self.get_browser_driver()
            total_urls = len(urls)
            is_single_url = (total_urls == 1)

            for index, url in enumerate(urls):
                if self.cancel_event.is_set(): break

                if "wikipedia.org" in url.lower():
                    self.root.after(0, self.update_status,
                                    "Братику, Вікіпедія і так безкоштовна. Що ти намагаєшся зробити? 🧠",
                                    self.accent_gold)
                    time.sleep(2)
                    continue

                if (".ua/" in url.lower() or ".com.ua/" in url.lower()) and self.state.get(
                        "target_lang_name") == "Українська":
                    current_status = "Перекладаю з української на... ще кращу і солов'їнішу! 🇺🇦"
                else:
                    current_status = self.t("status_single_start") if is_single_url else self.t("status_magic").format(
                        index + 1, total_urls)

                self.root.after(0, self.update_status, current_status)

                driver.get(url)
                try:
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                except Exception:
                    pass
                time.sleep(5)

                raw_html = driver.page_source
                base_url = url

                try:
                    soup = BeautifulSoup(raw_html, "lxml")
                except Exception:
                    soup = BeautifulSoup(raw_html, "html.parser")

                meta = self.extract_metadata(soup, base_url)
                if not meta['title']:
                    title_tag = soup.find('title')
                    meta['title'] = title_tag.get_text().strip() if title_tag else f"Архівна стаття {index + 1}"

                article_container = soup.find('article')
                if not article_container: article_container = soup.find('main')
                if not article_container: article_container = soup.find('div', class_=re.compile(
                    r'article|story|post|content|main', re.I))
                if not article_container: article_container = soup

                article_container = self.clean_junk_html(article_container)
                elements = article_container.find_all(
                    ['p', 'img', 'picture', 'video', 'iframe', 'h2', 'h3', 'h4', 'li', 'blockquote'])

                content_list = []
                total_words = 0
                download_images = self.state.get("download_images", True)
                spam_phrases = ["підпишіться на", "subscribe to", "sign up for", "read more:", "more from",
                                "newsletter"]

                for el in elements:
                    try:
                        if el.name in ['p', 'li', 'blockquote', 'h2', 'h3', 'h4']:
                            txt = el.get_text().strip()
                            if len(txt) < 150 and any(s in txt.lower() for s in spam_phrases): continue
                            if len(txt) > 20 and "cookie" not in txt.lower() and "javascript" not in txt.lower():
                                content_list.append({"type": el.name, "data": txt})
                                total_words += len(txt.split())

                        elif el.name in ['img', 'picture'] and download_images:
                            img_url = ""
                            if el.name == 'picture':
                                img_tag = el.find('img')
                                if img_tag:
                                    el = img_tag
                                else:
                                    continue

                            img_url = el.get('src') or el.get('data-src')
                            if not img_url and el.get('srcset'):
                                img_url = el.get('srcset').split(',')[0].split(' ')[0]

                            img_url = self.resolve_url(img_url, base_url)
                            if img_url and img_url.startswith('http') and img_url != meta['cover_image']:
                                content_list.append({"type": "img", "data": img_url})

                        elif el.name in ['video', 'iframe'] and download_images:
                            vid_url = el.get('src')
                            if el.name == 'video' and not vid_url:
                                source = el.find('source')
                                if source: vid_url = source.get('src')

                            vid_url = self.resolve_url(vid_url, base_url)
                            poster_url = self.resolve_url(el.get('poster'), base_url) if el.name == 'video' else ""

                            if vid_url and vid_url.startswith('http'):
                                content_list.append({"type": "video", "data": vid_url, "poster": poster_url})
                    except Exception:
                        continue

                if not content_list: continue

                doc = WordDocument()

                title_translated = self.translate_text(meta['title'])
                t_p = doc.add_paragraph()
                t_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                t_run = t_p.add_run(title_translated)
                t_run.bold, t_run.font.size, t_run.font.name = True, Pt(24), self.state["font_family"]

                if meta['subtitle']:
                    sub_translated = self.translate_text(meta['subtitle'])
                    sub_p = doc.add_paragraph()
                    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    sub_run = sub_p.add_run(sub_translated)
                    sub_run.italic = True
                    sub_run.font.size, sub_run.font.name = Pt(14), self.state["font_family"]
                    try:
                        sub_run.font.color.rgb = doc.styles['Normal'].font.color.rgb
                    except Exception:
                        pass

                if meta['author'] or meta['date']:
                    auth_text = []
                    if meta['author']: auth_text.append(f"✍️ Автор: {self.translate_text(meta['author'])}")
                    if meta['date']: auth_text.append(f"📅 Дата: {meta['date']}")
                    auth_p = doc.add_paragraph()
                    auth_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    auth_run = auth_p.add_run(" | ".join(auth_text))
                    auth_run.bold = True
                    auth_run.font.size = Pt(11)

                if download_images and meta['cover_image']:
                    try:
                        response = requests.get(meta['cover_image'], headers=self.http_headers, timeout=10)
                        if response.status_code == 200:
                            img_stream = self.convert_image_for_docx(response.content)
                            if img_stream:
                                img_p = doc.add_paragraph()
                                img_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                                img_run = img_p.add_run()
                                img_run.add_picture(img_stream, width=Inches(6.0))
                    except Exception:
                        pass

                doc.add_paragraph()

                if self.state.get("add_read_time", True):
                    reading_time = max(1, total_words // 150)
                    if reading_time > 100:
                        rt_text = f"⏱ Час читання: ~{reading_time} хв. (Впевнений, що це не 'Війна і мир'? Завари чаю ☕📖)"
                    else:
                        rt_text = f"⏱ Час читання: ~{reading_time} хв."

                    rt_p = doc.add_paragraph()
                    rt_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    rt_run = rt_p.add_run(rt_text)
                    rt_run.italic = True
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

                    try:
                        if item["type"] in ['p', 'li', 'blockquote', 'h2', 'h3', 'h4']:
                            translated = item.get("translated_data")
                            if not translated: translated = self.translate_text(item["data"])
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
                                response = requests.get(item["data"], headers=self.http_headers, timeout=10)
                                if response.status_code == 200:
                                    img_stream = self.convert_image_for_docx(response.content)
                                    if img_stream:
                                        img_p = doc.add_paragraph()
                                        img_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                                        img_run = img_p.add_run()
                                        img_run.add_picture(img_stream, width=Inches(5.5))
                            except Exception:
                                pass

                        elif item["type"] == "video":
                            try:
                                if item.get("poster"):
                                    response = requests.get(item["poster"], headers=self.http_headers, timeout=10)
                                    if response.status_code == 200:
                                        img_stream = self.convert_image_for_docx(response.content)
                                        if img_stream:
                                            img_p = doc.add_paragraph()
                                            img_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                                            img_run = img_p.add_run()
                                            img_run.add_picture(img_stream, width=Inches(5.0))

                                vid_p = doc.add_paragraph()
                                vid_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                                vid_run = vid_p.add_run(f"{self.t('video_link_text')}\n{item['data']}")
                                vid_run.font.size = Pt(11)
                                try:
                                    vid_run.font.color.rgb = doc.styles['Hyperlink'].font.color.rgb
                                except Exception:
                                    pass
                                vid_run.underline = True
                            except Exception:
                                pass

                    except Exception:
                        continue

                if self.state.get("add_metadata", True):
                    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    meta_p = doc.add_paragraph()
                    meta_p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    meta_text = self.t("metadata_text").format(url, current_date)
                    meta_run = meta_p.add_run(meta_text)
                    meta_run.font.size = Pt(10)
                    try:
                        meta_run.font.color.rgb = doc.styles['Normal'].font.color.rgb
                    except Exception:
                        pass
                    meta_run.italic = True

                    hour = datetime.now().hour
                    if 2 <= hour < 4:
                        meta_run.add_text("\n(P.S. Справжні генії працюють вночі, але вам, мабуть, час іти спати... 🦉)")

                safe_title = re.sub(r'[\\/:*?"<>|]', "", title_translated)[:80]
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

                if os.path.exists(cache_file): os.remove(cache_file)

                final_path = full_path
                if self.state.get("output_format") == "pdf":
                    pdf_path = full_path.replace(".docx", ".pdf")
                    self.root.after(0, self.update_status, self.t("status_pdf"), self.accent_gold)
                    try:
                        convert(full_path, pdf_path)
                        if os.path.exists(full_path): os.remove(full_path)
                        final_path = pdf_path
                    except Exception:
                        pass

                if self.state.get("auto_open", True): self.open_saved_file(final_path)

            if not self.cancel_event.is_set():
                self.root.after(0, self.update_status, self.t("status_success"), self.accent_green)
                self.show_system_notification("Скарбниця Знань", "✅ Обробку успішно завершено! Файл збережено.")

        except Exception as e:
            if not self.cancel_event.is_set():
                self.root.after(0, lambda err=e: messagebox.showerror("Error", f"{err}"))
                self.root.after(0, self.update_status, self.t("status_error"), "red")

        finally:
            self.is_processing = False
            if driver: driver.quit()
            if not self.cancel_event.is_set():
                self.root.after(0, lambda: self.save_btn.configure(state="normal"))
                self.root.after(0, lambda: self.cancel_btn.configure(state="disabled", fg_color="transparent"))
                self.root.after(0, self.progress_bar.pack_forget)

    def run_process(self):
        if self.is_processing: return
        raw_text = self.url_textbox.get("1.0", "end-1c").strip()

        if not raw_text or raw_text == self.t("placeholder"):
            self.empty_clicks += 1
            if self.empty_clicks == 3:
                self.update_status("Я все ще чекаю посилання...", self.accent_gold)
            elif self.empty_clicks >= 5:
                self.update_status("Слухай, я парсер, а не телепат. Дай лінк! 🤬", self.accent_red)
            return

        self.empty_clicks = 0

        if raw_text.lower() in ["wake up", "matrix"]:
            self.trigger_matrix_effect()
            return

        if "youtube.com/watch?v=dQw4w9WgXcQ" in raw_text or raw_text.lower() == "кава":
            self.update_status("Гарна спроба! Але мене не зарікролити 😎 (або ти просто хочеш пригостити мене кавою)",
                               self.accent_gold)
            if raw_text.lower() == "кава": self.open_donation_link()
            return

        urls = [u.strip() for u in raw_text.split('\n') if u.strip()]
        valid_urls = [u for u in urls if self.is_valid_url(u)]
        if not valid_urls:
            messagebox.showwarning("Увага", self.t("msg_invalid_url"))
            return

        self.start_process_time = time.time()
        self.prepare_ui_for_processing()
        threading.Thread(target=self.batch_worker, args=(valid_urls,), daemon=True).start()


if __name__ == "__main__":
    app = TranslationArchiveApp()
    app.root.mainloop()