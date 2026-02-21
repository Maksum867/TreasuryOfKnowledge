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
from io import BytesIO
import urllib.parse

import customtkinter as ctk
from tkinter import messagebox, filedialog
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from bs4 import BeautifulSoup

from docx import Document as WordDocument
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from plyer import notification

from deep_translator import MicrosoftTranslator, GoogleTranslator


class TranslationArchiveApp:
    def __init__(self):
        self.config_file = "settings.json"
        self.cache_dir = "backup_cache"

        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

        self.cancel_event = threading.Event()

        # СЛОВНИК ЛОКАЛІЗАЦІЇ
        self.locales = {
            "uk": {
                "title": "Скарбниця Знань v3.3 Pro",
                "placeholder": "Вставте посилання (можна кілька, кожне з нового рядка)...",
                "status_wait": "Очікування посилань...",
                "btn_digitize": "ОЦИФРУВАТИ В АРХІВ",
                "btn_cancel": "СКАСУВАТИ",

                "settings_title": "Налаштування",
                "path_lbl": "📍 Папка збереження:",
                "btn_choose": "Обрати",
                "font_lbl": "🖋️ Шрифт:",
                "size_lbl": "📏 Розмір тексту:",
                "theme_lbl": "🌓 Тема інтерфейсу:",
                "theme_dark": "Темний режим",
                "ui_lang_lbl": "🌍 Мова інтерфейсу:",
                "target_lang_lbl": "🎯 Перекладати статтю на:",

                "setting_read_time": "⏱ Додавати орієнтовний час читання у Word",
                "setting_bilingual": "📖 Двомовний режим (Зберігати оригінал + переклад)",
                "setting_auto_open": "🚀 Автоматично відкривати документ після створення",

                "btn_about": "ℹ️ Про додаток",
                "about_title": "Про додаток",
                "about_desc": "Автоматизований парсинг веб-статей з картинками\nта конвертація у Word-документи з перекладом.\nСтворено з душею для комфортного читання без меж.",
                "btn_changelog": "Історія версій",
                "btn_how_it_works": "Як це працює ⚙️",
                "btn_donate": "☕ Підтримати автора",

                "how_it_works_title": "Механізм роботи",
                "how_it_works_text": "Розробляючи цей інструмент, я ставив за мету зробити інтернет чистішим.\n\n🔍 Парсинг (Видобуток контенту):\nПрограма відкриває невидиме вікно браузера. Головна фішка — вона примусово вимикає JavaScript на сайті. Це миттєво 'вбиває' 90% рекламних банерів, вікон 'Прийміть кукі' та штучних блокувань контенту (paywalls). Залишається лише чистий текст та зображення.\n\n🧠 Аналіз структури:\nАлгоритм сканує сторінку, відкидаючи меню та коментарі, знаходить заголовки (H2/H3), списки та абзаци, щоб зберегти логіку автора.\n\n🌍 Переклад та Збірка:\nКожен абзац обережно пропускається через API перекладача. Після цього програма буквально 'зшиває' перекладений текст і завантажені картинки у красивий, відформатований Word-документ, готовий до друку чи читання з екрану.",

                "premium_title": "Доступ до Premium",
                "premium_text": "Вітаю, шукачу ексклюзиву! 🎩\n\nНіякого 'Premium' у цьому додатку немає і, мабуть, ніколи не буде.\n\nМожливо, колись світ і змусить мене повісити тут цінник чи ввести якусь підписку, але це зовсім не в моїй натурі. Я створював цей інструмент для того, щоб він приносив користь і робив знання доступними, а не для того, щоб витягувати гроші з людей.\n\nТому — видихай! Користуйся на здоров'я, поки є нагода, розширюй кругозір і нехай ця програма служить тобі вірою і правдою.\n\n(Але якщо вона дійсно зекономила тобі купу часу або просто підняла настрій — ти завжди можеш пригостити мене кавою. Кнопка підтримки скромно чекає на тебе в розділі 'Про додаток' 😉).",

                "changelog_title": "Changelog",
                "changelog_text": "v3.3 Pro:\n- Додано нові налаштування (Час читання, Двомовний режим, Авто-відкриття)\n- Розширено розділ 'Про додаток'\n- Додано приховану 'Premium' пасхалку\n\nv3.2 Pro:\n- Пакетна обробка (кілька посилань одночасно)\n- Збереження структури (заголовки h2/h3, списки)\n- Система кешування та сповіщення",
                "btn_back": "Повернутися",
                "status_magic": "🌐 Старт пакетної обробки (Стаття {} з {})...",
                "status_progress": "📜 Обробка {} з елементів...",
                "status_success": "✅ Усі документи успішно збережено!",
                "status_error": "❌ Помилка обробки",
                "status_cancelled": "🛑 Процес скасовано",
                "msg_error_txt": "Текст або контент не знайдено.",
                "msg_invalid_url": "Знайдено некоректне посилання. Перевірте ввід."
            },
            "en": {
                "title": "Treasury of Knowledge v3.3 Pro",
                "placeholder": "Paste URLs here (multiple allowed, one per line)...",
                "status_wait": "Waiting for URLs...",
                "btn_digitize": "DIGITIZE TO ARCHIVE",
                "btn_cancel": "CANCEL",

                "settings_title": "Settings",
                "path_lbl": "📍 Save Directory:",
                "btn_choose": "Browse",
                "font_lbl": "🖋️ Font Family:",
                "size_lbl": "📏 Text Size:",
                "theme_lbl": "🌓 Interface Theme:",
                "theme_dark": "Dark Mode",
                "ui_lang_lbl": "🌍 Interface Language:",
                "target_lang_lbl": "🎯 Translate article to:",

                "setting_read_time": "⏱ Add estimated reading time to Word",
                "setting_bilingual": "📖 Bilingual Mode (Save Original + Translation)",
                "setting_auto_open": "🚀 Auto-open document after creation",

                "btn_about": "ℹ️ About",
                "about_title": "About Application",
                "about_desc": "Automated web scraping of articles with images\nand converting them into Word documents with translation.\nMade with soul for comfortable reading.",
                "btn_changelog": "Version History",
                "btn_how_it_works": "How it works ⚙️",
                "btn_donate": "☕ Support Author",

                "how_it_works_title": "How It Works",
                "how_it_works_text": "The goal was to make the internet cleaner.\n\n🔍 Scraping:\nA hidden browser opens and turns off JavaScript. This kills 90% of ads, cookie popups, and paywalls, leaving only clean text.\n\n🧠 Structure Analysis:\nIt scans for H2/H3 headings, lists, and paragraphs, ignoring menus and footers.\n\n🌍 Translation & Assembly:\nEach paragraph is translated and stitched together with downloaded images into a beautifully formatted Word document.",

                "premium_title": "Premium Access",
                "premium_text": "Greetings, seeker of exclusivity! 🎩\n\nThere is no 'Premium' in this app, and probably never will be.\n\nMaybe someday the world will force me to put a price tag on this, but that's not in my nature. I created this tool to be useful and make knowledge accessible, not to drain money.\n\nSo breathe out! Use it freely while you can. Expand your horizons, and let this program serve you well.\n\n(But if it really saved you a lot of time or just cheered you up, you can always buy me a coffee. The support button is modestly waiting for you in the 'About' section 😉).",

                "changelog_title": "Changelog",
                "changelog_text": "v3.3 Pro:\n- Added new settings (Read Time, Bilingual, Auto-open)\n- Expanded 'About' section\n- Added hidden 'Premium' easter egg\n\nv3.2 Pro:\n- Batch processing (multiple URLs)\n- Structural formatting (h2/h3, lists)",
                "btn_back": "Go Back",
                "status_magic": "🌐 Starting batch process (Article {} of {})...",
                "status_progress": "📜 Processing element {} of {}...",
                "status_success": "✅ All documents saved successfully!",
                "status_error": "❌ Processing error",
                "status_cancelled": "🛑 Process cancelled",
                "msg_error_txt": "Text or content not found.",
                "msg_invalid_url": "Invalid URL found. Please check your input."
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
            "theme": "dark",
            "ui_language": "uk",
            "target_lang_name": "Українська",
            "add_read_time": True,
            "bilingual_mode": False,
            "auto_open": True
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

        ctk.CTkLabel(scroll, text="🛠 Додаткові функції:", font=("Inter", 16, "bold"), text_color=self.accent_gold).pack(
            anchor="w", pady=(20, 5))

        sw_read_time = ctk.CTkSwitch(scroll, text=self.t("setting_read_time"),
                                     command=lambda: self.temp_state.update({"add_read_time": sw_read_time.get()}),
                                     progress_color=self.accent_gold)
        if self.temp_state.get("add_read_time", True): sw_read_time.select()
        sw_read_time.pack(anchor="w", pady=5)

        sw_bilingual = ctk.CTkSwitch(scroll, text=self.t("setting_bilingual"),
                                     command=lambda: self.temp_state.update({"bilingual_mode": sw_bilingual.get()}),
                                     progress_color=self.accent_gold)
        if self.temp_state.get("bilingual_mode", False): sw_bilingual.select()
        sw_bilingual.pack(anchor="w", pady=5)

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

        # ПАСХАЛКА: Прихована кнопка в самому низу
        hidden_premium = ctk.CTkButton(scroll, text="v3.3 👑", fg_color="transparent",
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

        desc = ctk.CTkLabel(self.main_container, text=self.t("about_desc"), font=("Inter", 18), justify="center")
        desc.pack(pady=15)

        buttons_frame1 = ctk.CTkFrame(self.main_container, fg_color="transparent")
        buttons_frame1.pack(pady=10)

        how_btn = ctk.CTkButton(buttons_frame1, text=self.t("btn_how_it_works"), height=45, width=220, corner_radius=15,
                                fg_color="#2980b9", hover_color="#3498db", command=self.show_how_it_works_screen)
        how_btn.pack(side="left", padx=10)

        changelog_btn = ctk.CTkButton(buttons_frame1, text=self.t("btn_changelog"), height=45, width=220,
                                      corner_radius=15, fg_color=self.accent_green, command=self.show_changelog_screen)
        changelog_btn.pack(side="right", padx=10)

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

    def show_changelog_screen(self):
        self.clear_screen()
        back_btn = ctk.CTkButton(self.main_container, text="←", width=50, height=50, fg_color="transparent",
                                 text_color=self.accent_gold, font=("Arial", 40, "bold"),
                                 command=self.show_about_screen)
        back_btn.place(relx=0.07, rely=0.07, anchor="center")
        ctk.CTkLabel(self.main_container, text=self.t("changelog_title"), font=("Georgia", 34, "bold"),
                     text_color=self.accent_gold).pack(pady=(80, 20))
        textbox = ctk.CTkTextbox(self.main_container, width=700, height=400, font=("Inter", 16))
        textbox.pack(pady=20)
        textbox.insert("1.0", self.t("changelog_text"))
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
        try:
            return MicrosoftTranslator(target=target_code).translate(text)
        except:
            try:
                return GoogleTranslator(source='auto', target=target_code).translate(text)
            except:
                return text

    # ВІДНОВЛЕНА ФУНКЦІЯ!
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
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
            options.add_experimental_option("prefs", {"profile.managed_default_content_settings.javascript": 2})

            try:
                service = EdgeService(EdgeChromiumDriverManager().install())
                driver = webdriver.Edge(service=service, options=options)
            except Exception as wm_error:
                print(f"Fallback to local driver: {wm_error}")
                driver = webdriver.Edge(options=options)

            total_urls = len(urls)

            for index, url in enumerate(urls):
                if self.cancel_event.is_set(): break

                batch_status = self.t("status_magic").format(index + 1, total_urls)
                self.root.after(0, self.update_status, batch_status)

                driver.get(url)
                time.sleep(2)

                soup = BeautifulSoup(driver.page_source, "lxml")
                h1 = soup.find('h1') or soup.find('title')
                title = self.translate_text(h1.get_text().strip()) if h1 else f"Архівна стаття {index + 1}"

                main_body = soup.find('article') or soup.find('div', class_=re.compile(
                    'ArticleBody|content|body|post')) or soup

                elements = main_body.find_all(['p', 'img', 'h2', 'h3', 'h4', 'li', 'blockquote'])

                content_list = []
                total_words = 0

                for el in elements:
                    if el.name in ['p', 'li', 'blockquote', 'h2', 'h3', 'h4']:
                        txt = el.get_text().strip()
                        if len(txt) > 20 and "cookie" not in txt.lower():
                            content_list.append({"type": el.name, "data": txt})
                            total_words += len(txt.split())
                    elif el.name == 'img':
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

                    time.sleep(0.1)

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

                if self.state.get("auto_open", True):
                    self.open_saved_file(full_path)

            if not self.cancel_event.is_set():
                self.root.after(0, self.update_status, self.t("status_success"), self.accent_green)
                self.show_system_notification("Скарбниця Знань", "Пакетну обробку успішно завершено!")

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