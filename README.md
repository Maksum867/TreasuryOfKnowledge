<!-- ═══════════════════════════════════════════════════════════════════════════════ -->
<!-- HEADER -->
<!-- ═══════════════════════════════════════════════════════════════════════════════ -->

<div align="center">

# 📜 Скарбниця Знань | Treasury of Knowledge

### *Your Smart Article Parser & Offline Reader*

<br>

![Version](https://img.shields.io/badge/version-6.1-blue?style=for-the-badge&logo=semanticrelease&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PyQt6](https://img.shields.io/badge/PyQt6-Desktop_App-41CD52?style=for-the-badge&logo=qt&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-Web_Scraping-43B02A?style=for-the-badge&logo=selenium&logoColor=white)
![Windows](https://img.shields.io/badge/Windows_10%2F11-Exclusive-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge&logo=opensourceinitiative&logoColor=white)

<br>

**🇺🇦 Українська** ・ [🇬🇧 English](#-english-version)

<br>

> *Вставив посилання — отримав красивий документ. Без реклами. Без paywall. З перекладом.*

<br>


</div>

<br>

<!-- ═══════════════════════════════════════════════════════════════════════════════ -->
<!-- ЗМІСТ (УКРАЇНСЬКА) -->
<!-- ═══════════════════════════════════════════════════════════════════════════════ -->

## 📑 Зміст

- [🎯 Про проект](#-про-проект)
- [✨ Ключові можливості](#-ключові-можливості)
- [🖼️ Скріншоти](#️-скріншоти)
- [⚡ Швидкий старт](#-швидкий-старт)
- [🗂️ Структура проекту](#️-структура-проекту)
- [🛠️ Технологічний стек](#️-технологічний-стек)
- [🗺️ Дорожня карта](#️-дорожня-карта)
- [🤝 Як долучитися](#-як-долучитися)
- [📄 Ліцензія](#-ліцензія)

<br>

<!-- ═══════════════════════════════════════════════════════════════════════════════ -->
<!-- ПРО ПРОЕКТ -->
<!-- ═══════════════════════════════════════════════════════════════════════════════ -->

## 🎯 Про проект

**Скарбниця Знань** — це десктопний додаток для Windows, створений на PyQt6, який перетворює будь-яку онлайн-статтю на красивий офлайн-документ в один клік.

Як це працює? Дуже просто:

1. 📋 **Скопіюйте посилання** на статтю (або програма сама підхопить його з буфера обміну).
2. 🤖 **Додаток запускає Selenium** у фоновому режимі, відкриває сторінку як справжній браузер.
3. 🧹 **Алгоритми Readability** аналізують DOM-дерево та витягують лише головний контент — ніякої реклами, бічних панелей, хедерів чи футерів.
4. 🌍 **Перекладач** (якщо потрібно) перекладає текст обраною мовою — абзац за абзацом.
5. 📄 **Генератор документів** формує стильний **DOCX** або **PDF** файл з картинками, змістом та метаданими.

**Навіщо це потрібно?**

| Проблема | Рішення від Скарбниці |
|:---|:---|
| 😤 Стаття за paywall | 🔓 Обхід paywall через Selenium-рендеринг |
| 😤 Реклама та сміття на сторінці | 🧹 Readability вирізає все зайве |
| 😤 Стаття іноземною мовою | 🌍 Двомовні документи: оригінал + переклад |
| 😤 Сайт може зникнути | 💾 Офлайн-копія назавжди у DOCX/PDF |
| 😤 Незручно читати з екрану | 📖 Красивий документ зі змістом та часом читання |

<br>

<!-- ═══════════════════════════════════════════════════════════════════════════════ -->
<!-- КЛЮЧОВІ МОЖЛИВОСТІ -->
<!-- ═══════════════════════════════════════════════════════════════════════════════ -->

## ✨ Ключові можливості

<table>
<tr>
<td width="50%" valign="top">

### 🌐 Універсальний парсинг
Працює на переважній більшості сайтів у мережі. Розумний алгоритм Readability аналізує структуру сторінки та безпомилково знаходить основний контент — незалежно від того, це Medium, Habr, Wikipedia чи ваш улюблений блог.

### 🔓 Обхід Paywall
Забудьте про повідомлення «Підпишіться, щоб читати далі». Selenium завантажує сторінку так, як бачить її браузер, — а інтелектуальний парсер витягує повний текст статті, навіть якщо вона захована за paywall.

### 📄 Збереження у DOCX та PDF
На виході — не сирий текст, а красиво оформлений документ. Із заголовками, збереженим форматуванням, зображеннями та коректною типографікою. Обирайте формат, який вам зручніший.

### 🌍 Двомовні документи
Унікальна функція: генерація документів, де оригінальний текст та переклад розташовані поруч — абзац за абзацом. Ідеально для вивчення мов або для точної перевірки перекладу.

</td>
<td width="50%" valign="top">

### 📑 Автоматичний зміст та час читання
Для довгих лонгрідів додаток автоматично генерує клікабельний **Table of Contents** на основі заголовків статті та розраховує приблизний час читання. Навігація стає легкою.

### 🔲 Робота у System Tray
Додаток може згортатися у системний трей та чекати у фоні. Скопіювали посилання — він миттєво підхоплює URL з буфера обміну та починає парсинг. Максимальна продуктивність без зайвих вікон.

### 🎨 Кастомний Dark / Light інтерфейс
Жодних стандартних нудних кнопок Windows. Повністю кастомний UI із власним заголовком вікна, стильними контролами та плавним перемиканням між темною та світлою темами.

### 🥚 15+ пасхалок
Для найуважніших користувачів у додатку сховано понад **15 прихованих пасхалок**. Знайдете всі? 😏

</td>
</tr>
</table>

<br>

<!-- ═══════════════════════════════════════════════════════════════════════════════ -->
<!-- СКРІНШОТИ -->
<!-- ═══════════════════════════════════════════════════════════════════════════════ -->



<!-- ═══════════════════════════════════════════════════════════════════════════════ -->
<!-- ШВИДКИЙ СТАРТ -->
<!-- ═══════════════════════════════════════════════════════════════════════════════ -->

## ⚡ Швидкий старт

### 📋 Вимоги

| Вимога | Деталі |
|:---|:---|
| **ОС** | Windows 10 або Windows 11 (ексклюзивна підтримка) |
| **Python** | Версія **3.10** або новіша |
| **Інтернет** | Потрібен для завантаження залежностей та парсингу статей |
| **Місце на диску** | ~500 МБ (для віртуального середовища та ChromeDriver) |

### 🚀 Встановлення та запуск

Процес максимально простий — вам потрібен лише Python та один клік.

**Крок 1 — Клонуйте репозиторій:**

```bash
git clone https://github.com/your-username/treasury-of-knowledge.git
cd treasury-of-knowledge
```

**Крок 2 — Запустіть `Start.bat`:**

```
📁 treasury-of-knowledge/
└── 🖱️ Двічі клікніть на Start.bat
```

#### 🔮 Що робить `Start.bat`?

Це розумний лаунчер, який бере на себе всю рутину:

| Запуск | Що відбувається | Час |
|:---|:---|:---|
| 🟡 **Перший клік** | Автоматично створюється папка `.venv`, встановлюються **всі залежності** з `requirements.txt` у ізольоване віртуальне середовище. Після встановлення — додаток запускається. | ~2-3 хв |
| 🟢 **Наступні кліки** | Миттєвий запуск додатку у **фоновому режимі** (без чорного вікна терміналу). Жодних зайвих дій. | ~3 сек |

> 💡 **Порада:** Створіть ярлик на `Start.bat` та закріпіть його на панелі завдань для максимальної зручності.

> ⚠️ **Важливо:** Переконайтеся, що Python додано до системної змінної `PATH`. Перевірити можна командою `python --version` у терміналі.

<br>

<!-- ═══════════════════════════════════════════════════════════════════════════════ -->
<!-- СТРУКТУРА ПРОЕКТУ -->
<!-- ═══════════════════════════════════════════════════════════════════════════════ -->

## 🗂️ Структура проекту

```
📁 treasury-of-knowledge/
│
├── 🚀 Start.bat              # Розумний лаунчер: створює .venv, ставить залежності,
│                              # запускає додаток без терміналу
│
├── 📄 requirements.txt        # Перелік усіх Python-залежностей
│
├── 🎯 main.py                 # Точка входу — ініціалізація QApplication та запуск
│
├── ⚙️ config.py               # Конфігурація додатку: константи, шляхи, стилі QSS,
│                              # словники локалізації (UA/EN), палітри тем
│
├── 🧩 ui_components.py        # Кастомні PyQt6-віджети: кнопки заголовка,
│                              # стилізовані поля вводу, анімовані елементи
│
├── 🖥️ ui_main.py              # Головне вікно додатку: layout, обробка подій,
│                              # System Tray, взаємодія з буфером обміну
│
├── 🤖 core_scraper.py         # Ядро: Selenium WebDriver, BeautifulSoup,
│                              # Readability-алгоритми, переклад, генерація DOCX/PDF
│
├── 📁 .venv/                  # (auto-generated) Віртуальне середовище Python
│
└── 📁 docs/                   # Скріншоти та додаткова документація
    └── 📁 screenshots/
```

<br>

<!-- ═══════════════════════════════════════════════════════════════════════════════ -->
<!-- ТЕХНОЛОГІЧНИЙ СТЕК -->
<!-- ═══════════════════════════════════════════════════════════════════════════════ -->

## 🛠️ Технологічний стек

<div align="center">

| Технологія | Призначення |
|:---:|:---|
| ![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) | Основна мова розробки |
| ![PyQt6](https://img.shields.io/badge/PyQt6-41CD52?style=flat-square&logo=qt&logoColor=white) | Фреймворк для десктопного GUI |
| ![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=flat-square&logo=selenium&logoColor=white) | Headless-браузер для рендерингу сторінок |
| ![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup4-grey?style=flat-square&logo=python&logoColor=white) | Парсинг та обробка HTML/DOM |
| ![Readability](https://img.shields.io/badge/Readability-orange?style=flat-square&logo=mozilla&logoColor=white) | Витягування основного контенту сторінки |
| ![python-docx](https://img.shields.io/badge/python--docx-2B579A?style=flat-square&logo=microsoftword&logoColor=white) | Генерація документів DOCX |
| ![ReportLab / WeasyPrint](https://img.shields.io/badge/PDF_Engine-red?style=flat-square&logo=adobeacrobatreader&logoColor=white) | Генерація документів PDF |

</div>

<br>

<!-- ═══════════════════════════════════════════════════════════════════════════════ -->
<!-- ДОРОЖНЯ КАРТА -->
<!-- ═══════════════════════════════════════════════════════════════════════════════ -->

## 🗺️ Дорожня карта

- [x] Парсинг статей через Selenium + Readability
- [x] Експорт у DOCX та PDF із зображеннями
- [x] Двомовні документи (оригінал + переклад)
- [x] Автоматичний зміст (TOC) та час читання
- [x] Dark / Light теми з кастомним UI
- [x] System Tray та парсинг з буфера обміну
- [x] Обхід paywall
- [x] 15+ пасхалок 🥚
- [ ] Пакетний парсинг (черга з декількох URL)
- [ ] Підтримка EPUB-формату
- [ ] Інтеграція з Notion / Obsidian
- [ ] Портативний .exe через PyInstaller

<br>

<!-- ═══════════════════════════════════════════════════════════════════════════════ -->
<!-- ЯК ДОЛУЧИТИСЯ -->
<!-- ═══════════════════════════════════════════════════════════════════════════════ -->

## 🤝 Як долучитися

Маєте ідею, знайшли баг або хочете додати фічу? Ми раді будь-якому внеску!

1. 🍴 **Форкніть** цей репозиторій
2. 🌿 Створіть свою гілку: `git checkout -b feature/amazing-feature`
3. 💾 Зробіть коміт: `git commit -m 'feat: add amazing feature'`
4. 📤 Запушіть: `git push origin feature/amazing-feature`
5. 🔀 Відкрийте **Pull Request**

> 💬 Для обговорення ідей — створюйте [Issue](https://github.com/your-username/treasury-of-knowledge/issues).

<br>

<!-- ═══════════════════════════════════════════════════════════════════════════════ -->
<!-- ЛІЦЕНЗІЯ -->
<!-- ═══════════════════════════════════════════════════════════════════════════════ -->

## 📄 Ліцензія

Розповсюджується під ліцензією **MIT**. Дивіться файл [`LICENSE`](LICENSE) для деталей.

```
MIT License — Copyright (c) 2025 Treasury of Knowledge

Дозволяється безоплатно будь-якій особі використовувати, копіювати,
змінювати, публікувати, розповсюджувати, субліцензувати та/або продавати
копії цього програмного забезпечення без обмежень.
```

<br>

---

<br>

<!-- ═══════════════════════════════════════════════════════════════════════════════ -->
<!-- ═══════════════════════════════════════════════════════════════════════════════ -->
<!-- ENGLISH VERSION -->
<!-- ═══════════════════════════════════════════════════════════════════════════════ -->
<!-- ═══════════════════════════════════════════════════════════════════════════════ -->

<div align="center">

# 🇬🇧 English Version

<br>

[🇺🇦 Українська](#-зміст) ・ **🇬🇧 English**

<br>

> *Paste a link — get a beautiful document. No ads. No paywall. With translation.*

</div>

<br>

## 📑 Table of Contents

- [🎯 About](#-about)
- [✨ Key Features](#-key-features)
- [🖼️ Screenshots](#️-screenshots-1)
- [⚡ Quick Start](#-quick-start-1)
- [🗂️ Project Structure](#️-project-structure)
- [🛠️ Tech Stack](#️-tech-stack)
- [🗺️ Roadmap](#️-roadmap)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

<br>

## 🎯 About

**Treasury of Knowledge** is a Windows desktop application built with PyQt6 that transforms any online article into a beautiful offline document with a single click.

Here's how it works:

1. 📋 **Copy a link** to any article (or let the app grab it from your clipboard automatically).
2. 🤖 **The app launches Selenium** in the background, opening the page like a real browser.
3. 🧹 **Readability algorithms** analyze the DOM tree and extract only the main content — no ads, sidebars, headers, or footers.
4. 🌍 **The translator** (if needed) translates the text into your chosen language — paragraph by paragraph.
5. 📄 **The document generator** produces a polished **DOCX** or **PDF** file with images, table of contents, and metadata.

**Why do you need this?**

| Problem | Treasury's Solution |
|:---|:---|
| 😤 Article behind a paywall | 🔓 Paywall bypass via Selenium rendering |
| 😤 Ads and clutter on the page | 🧹 Readability strips everything unnecessary |
| 😤 Article in a foreign language | 🌍 Bilingual documents: original + translation |
| 😤 Website might disappear | 💾 Permanent offline copy in DOCX/PDF |
| 😤 Uncomfortable reading on screen | 📖 Beautiful document with TOC and reading time |

<br>

## ✨ Key Features

<table>
<tr>
<td width="50%" valign="top">

### 🌐 Universal Parsing
Works on the vast majority of websites. The smart Readability algorithm analyzes page structure and accurately identifies the main content — whether it's Medium, Habr, Wikipedia, or your favorite blog.

### 🔓 Paywall Bypass
Forget about "Subscribe to continue reading" messages. Selenium loads the page exactly as a browser sees it, and the intelligent parser extracts the full article text, even when it's hidden behind a paywall.

### 📄 Save to DOCX & PDF
The output isn't raw text — it's a beautifully formatted document with headings, preserved formatting, images, and proper typography. Choose whichever format suits you best.

### 🌍 Bilingual Documents
A unique feature: generate documents where the original text and translation are placed side by side — paragraph by paragraph. Perfect for language learning or precise translation verification.

</td>
<td width="50%" valign="top">

### 📑 Auto Table of Contents & Reading Time
For long-form articles, the app automatically generates a clickable **Table of Contents** based on the article's headings and calculates the estimated reading time. Navigation made easy.

### 🔲 System Tray Mode
The app can minimize to the system tray and wait in the background. Copy a link — it instantly picks up the URL from the clipboard and starts parsing. Maximum productivity with zero extra windows.

### 🎨 Custom Dark / Light Interface
No standard boring Windows buttons. A fully custom UI with a custom title bar, stylish controls, and smooth switching between dark and light themes.

### 🥚 15+ Easter Eggs
For the most attentive users, the app hides over **15 secret easter eggs**. Can you find them all? 😏

</td>
</tr>
</table>

<br>

## 🖼️ Screenshots





## ⚡ Quick Start

### 📋 Requirements

| Requirement | Details |
|:---|:---|
| **OS** | Windows 10 or Windows 11 (exclusive support) |
| **Python** | Version **3.10** or higher |
| **Internet** | Required for downloading dependencies and parsing articles |
| **Disk Space** | ~500 MB (for virtual environment and ChromeDriver) |

### 🚀 Installation & Launch

The process is as simple as it gets — you only need Python and a single click.

**Step 1 — Clone the repository:**

```bash
git clone https://github.com/your-username/treasury-of-knowledge.git
cd treasury-of-knowledge
```

**Step 2 — Run `Start.bat`:**

```
📁 treasury-of-knowledge/
└── 🖱️ Double-click Start.bat
```

#### 🔮 What does `Start.bat` do?

It's a smart launcher that handles all the routine work for you:

| Launch | What happens | Time |
|:---|:---|:---|
| 🟡 **First click** | Automatically creates a `.venv` folder, installs **all dependencies** from `requirements.txt` into an isolated virtual environment. After installation — the app launches. | ~2-3 min |
| 🟢 **Subsequent clicks** | Instant app launch in **background mode** (no black terminal window). No extra steps needed. | ~3 sec |

> 💡 **Tip:** Create a shortcut to `Start.bat` and pin it to your taskbar for maximum convenience.

> ⚠️ **Important:** Make sure Python is added to your system `PATH` variable. You can verify by running `python --version` in the terminal.

<br>

## 🗂️ Project Structure

```
📁 treasury-of-knowledge/
│
├── 🚀 Start.bat              # Smart launcher: creates .venv, installs dependencies,
│                              # launches the app without a terminal window
│
├── 📄 requirements.txt        # List of all Python dependencies
│
├── 🎯 main.py                 # Entry point — QApplication initialization and launch
│
├── ⚙️ config.py               # App configuration: constants, paths, QSS styles,
│                              # localization dictionaries (UA/EN), theme palettes
│
├── 🧩 ui_components.py        # Custom PyQt6 widgets: title bar buttons,
│                              # stylized input fields, animated elements
│
├── 🖥️ ui_main.py              # Main application window: layout, event handling,
│                              # System Tray, clipboard interaction
│
├── 🤖 core_scraper.py         # Core engine: Selenium WebDriver, BeautifulSoup,
│                              # Readability algorithms, translation, DOCX/PDF generation
│
├── 📁 .venv/                  # (auto-generated) Python virtual environment
│
└── 📁 docs/                   # Screenshots and additional documentation
    └── 📁 screenshots/
```

<br>

## 🛠️ Tech Stack

<div align="center">

| Technology | Purpose |
|:---:|:---|
| ![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) | Core programming language |
| ![PyQt6](https://img.shields.io/badge/PyQt6-41CD52?style=flat-square&logo=qt&logoColor=white) | Desktop GUI framework |
| ![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=flat-square&logo=selenium&logoColor=white) | Headless browser for page rendering |
| ![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup4-grey?style=flat-square&logo=python&logoColor=white) | HTML/DOM parsing and processing |
| ![Readability](https://img.shields.io/badge/Readability-orange?style=flat-square&logo=mozilla&logoColor=white) | Main content extraction from pages |
| ![python-docx](https://img.shields.io/badge/python--docx-2B579A?style=flat-square&logo=microsoftword&logoColor=white) | DOCX document generation |
| ![ReportLab / WeasyPrint](https://img.shields.io/badge/PDF_Engine-red?style=flat-square&logo=adobeacrobatreader&logoColor=white) | PDF document generation |

</div>

<br>

## 🗺️ Roadmap

- [x] Article parsing via Selenium + Readability
- [x] Export to DOCX and PDF with images
- [x] Bilingual documents (original + translation)
- [x] Automatic Table of Contents (TOC) & reading time
- [x] Dark / Light themes with custom UI
- [x] System Tray & clipboard parsing
- [x] Paywall bypass
- [x] 15+ easter eggs 🥚
- [ ] Batch parsing (queue of multiple URLs)
- [ ] EPUB format support
- [ ] Notion / Obsidian integration
- [ ] Portable .exe via PyInstaller

<br>

## 🤝 Contributing

Have an idea, found a bug, or want to add a feature? We welcome any contributions!

1. 🍴 **Fork** this repository
2. 🌿 Create your branch: `git checkout -b feature/amazing-feature`
3. 💾 Commit your changes: `git commit -m 'feat: add amazing feature'`
4. 📤 Push to the branch: `git push origin feature/amazing-feature`
5. 🔀 Open a **Pull Request**

> 💬 To discuss ideas — create an [Issue](https://github.com/your-username/treasury-of-knowledge/issues).

<br>

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for more information.

```
MIT License — Copyright (c) 2025 Treasury of Knowledge

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software without restriction.
```

<br>

---

<div align="center">

<br>

**📜 Скарбниця Знань v6.1**

Зроблено з ❤️ та ☕ в Україні

*Зберігайте знання. Діліться мудрістю.*

<br>

![Stars](https://img.shields.io/github/stars/your-username/treasury-of-knowledge?style=social)
![Forks](https://img.shields.io/github/forks/your-username/treasury-of-knowledge?style=social)
![Watchers](https://img.shields.io/github/watchers/your-username/treasury-of-knowledge?style=social)

</div>
```
