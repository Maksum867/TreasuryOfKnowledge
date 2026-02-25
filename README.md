

# 📜 Treasury of Knowledge / Скарбниця Знань

---

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows%20|%20macOS%20|%20Linux-blue?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-4.0-gold?style=for-the-badge)

**🏛️ Read any article. In any language. Without restrictions.**

**🏛️ Читайте будь-яку статтю. Будь-якою мовою. Без обмежень.**

[English](#-english) • [Українська](#-українська)

</div>

---

## 🇬🇧 English

### 📖 What is this?

**Treasury of Knowledge** is a desktop application that gives you free access to information without borders and restrictions.

It lets you read articles, journals, and news that are:
- 🚫 **Geo-blocked** in your country
- 💰 **Hidden behind a paywall** (requiring paid subscriptions)
- 🌐 **Written in a language** you don't understand

The program algorithmically extracts the hidden text from websites, translates it into your preferred language, and saves it as a clean, beautifully formatted document on your computer.

> **Knowledge should be free and accessible to everyone.**

---

### ✨ Features

| Feature | Description |
|---------|-------------|
| 🔓 **Paywall & Geo-block Bypass** | Read paid and restricted articles for free |
| 🌍 **Auto-Translation** | Google Translator or Microsoft Translator (with automatic fallback) |
| 📄 **DOCX & PDF Export** | Save articles in professional document formats |
| 🧹 **Intelligent Reader Mode** | Automatically removes ads, banners, pop-ups, and navigation menus |
| 📑 **Auto Table of Contents** | Generates a clickable TOC for long articles |
| 📖 **Bilingual Mode** | Side-by-side original + translation paragraph by paragraph |
| 🖼️ **Image Download** | Embeds article images (or skip them for faster processing) |
| ⏱️ **Reading Time Estimate** | Shows estimated reading time for each article |
| 📦 **Batch Processing** | Process multiple URLs at once (one per line) |
| 🔗 **Source Metadata** | Saves original URL and date at the end of the document |
| 🌓 **Dark & Light Themes** | Comfortable UI for any lighting condition |
| 🌐 **Bilingual UI** | Interface available in Ukrainian and English |
| 💾 **Auto-Backup Cache** | Progress is cached during processing to prevent data loss |
| 🚀 **Auto-Open** | Automatically opens the saved document after creation |

---

### 🎯 Supported Translation Languages

| Language | Code |
|----------|------|
| Українська (Ukrainian) | `uk` |
| English | `en` |
| Polski (Polish) | `pl` |
| Deutsch (German) | `de` |
| Français (French) | `fr` |
| Español (Spanish) | `es` |

---

### ⚙️ How It Works

```
┌─────────────────────────────────────────────────────┐
│  1. 🔗 You paste a URL (or multiple URLs)           │
│                    ↓                                 │
│  2. 🌐 Hidden browser opens the page                │
│     (JavaScript disabled → bypasses blockers)        │
│                    ↓                                 │
│  3. 🧹 Reader Mode extracts pure article content    │
│     (removes ads, menus, popups)                     │
│                    ↓                                 │
│  4. 🧠 Analyzes structure: headings, paragraphs,    │
│     lists, images, blockquotes                       │
│                    ↓                                 │
│  5. 🌍 Each paragraph is translated via selected     │
│     engine (Google/Microsoft with fallback)          │
│                    ↓                                 │
│  6. 📄 Assembles a formatted DOCX/PDF document      │
│     with TOC, images, and metadata                   │
│                    ↓                                 │
│  7. ✅ Saves to your chosen folder & auto-opens      │
└─────────────────────────────────────────────────────┘
```

---

### 🛠️ Installation

#### Prerequisites

- **Python 3.9+**
- **Microsoft Edge** browser installed
- **Microsoft Word** (required only for PDF conversion via `docx2pdf`)

#### Step 1: Clone the repository

```bash
git clone https://github.com/Maksum867/TreasuryOfKnowledge.git
cd treasury-of-knowledge
```

#### Step 2: Install dependencies

```bash
pip install -r requirements.txt
```

#### Step 3: Run the application

```bash
python main.py
```

---

### 📦 Dependencies

```
customtkinter
selenium
beautifulsoup4
lxml
python-docx
deep-translator
docx2pdf
plyer
requests
readability-lxml
```

<details>
<summary>📋 Create requirements.txt</summary>

```
customtkinter>=5.0
selenium>=4.0
beautifulsoup4>=4.12
lxml>=4.9
python-docx>=0.8
deep-translator>=1.11
docx2pdf>=0.4
plyer>=2.1
requests>=2.28
readability-lxml>=0.8
```

</details>

---

### 📸 Screenshots

<details>
<summary>🖥️ Click to see the interface</summary>

```
┌──────────────────────────────────────────┐
│                    ⚙️                    │
│                  🏛️                      │
│         Скарбниця Знань                  │
│                                          │
│  ┌────────────────────────────────────┐  │
│  │ Paste URLs here...                │  │
│  │                                    │  │
│  └────────────────────────────────────┘  │
│                                          │
│  ████████████████████░░░░░  75%          │
│                                          │
│  📜 Processing element 12 of 16...       │
│                                          │
│  ┌──────────────┐  ┌──────────────┐      │
│  │ DIGITIZE TO  │  │   CANCEL     │      │
│  │   ARCHIVE    │  │              │      │
│  └──────────────┘  └──────────────┘      │
└──────────────────────────────────────────┘
```

</details>

---

### 🗂️ Project Structure

```
treasury-of-knowledge/
├── main.py              # Main application file
├── settings.json        # User settings (auto-generated)
├── backup_cache/        # Translation cache directory
├── requirements.txt     # Python dependencies
├── LICENSE              # Project license
└── README.md            # This file
```

---

### ⚠️ Disclaimer

This tool is intended for **personal educational use only**. The author does not encourage copyright infringement. Please respect content creators and use this tool responsibly. If you find an article valuable, consider supporting its author.

---

### 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

### ☕ Support the Author

If this app saved you time and effort, you can buy me a coffee:

[![Monobank](https://img.shields.io/badge/Monobank-Donate-yellow?style=for-the-badge)](https://send.monobank.ua/jar/328DrBEZXY)

---

---

## 🇺🇦 Українська

### 📖 Що це таке?

**Скарбниця Знань** — це десктопний додаток, що дає вам вільний доступ до інформації без кордонів та обмежень.

Він дозволяє читати статті, журнали та новини, які:
- 🚫 **Заблоковані** у вашій країні (гео-блокування)
- 💰 **Приховані за пейволом** (потребують платної підписки)
- 🌐 **Написані мовою**, якої ви не розумієте

Програма алгоритмічно «витягує» прихований текст із сайту, перекладає його на зручну для вас мову та зберігає у вигляді чистого, акуратного документа на вашому комп'ютері.

> **Знання мають бути безкоштовними та доступними для кожного.**

---

### ✨ Можливості

| Функція | Опис |
|---------|------|
| 🔓 **Обхід блокувань та пейволів** | Читайте платні та обмежені статті безкоштовно |
| 🌍 **Автоматичний переклад** | Google або Microsoft перекладач (з автоматичною підстраховкою) |
| 📄 **Експорт у DOCX та PDF** | Збереження у професійних форматах документів |
| 🧹 **Інтелектуальний режим читання** | Автоматичне видалення реклами, банерів, попапів та меню |
| 📑 **Автоматичний Зміст** | Генерація змісту для довгих статей |
| 📖 **Двомовний режим** | Оригінал + переклад паралельно по абзацах |
| 🖼️ **Завантаження зображень** | Вбудовування картинок зі статті (або пропуск для швидкості) |
| ⏱️ **Оцінка часу читання** | Показує орієнтовний час на читання кожної статті |
| 📦 **Пакетна обробка** | Обробка кількох посилань одночасно (кожне з нового рядка) |
| 🔗 **Метадані джерела** | Збереження оригінального посилання та дати в кінці документа |
| 🌓 **Темна та світла тема** | Комфортний інтерфейс для будь-якого освітлення |
| 🌐 **Двомовний інтерфейс** | Інтерфейс українською та англійською |
| 💾 **Кешування прогресу** | Прогрес зберігається під час обробки для запобігання втраті даних |
| 🚀 **Автовідкриття** | Автоматичне відкриття збереженого документа після створення |

---

### 🎯 Підтримувані мови перекладу

| Мова | Код |
|------|-----|
| Українська | `uk` |
| English (Англійська) | `en` |
| Polski (Польська) | `pl` |
| Deutsch (Німецька) | `de` |
| Français (Французька) | `fr` |
| Español (Іспанська) | `es` |

---

### ⚙️ Як це працює

```
┌─────────────────────────────────────────────────────┐
│  1. 🔗 Ви вставляєте посилання (одне або кілька)    │
│                    ↓                                 │
│  2. 🌐 Прихований браузер відкриває сторінку         │
│     (JavaScript вимкнено → обходить блокувальники)   │
│                    ↓                                 │
│  3. 🧹 Режим читання видобуває чистий контент        │
│     (видаляє рекламу, меню, попапи)                  │
│                    ↓                                 │
│  4. 🧠 Аналізує структуру: заголовки, абзаци,       │
│     списки, зображення, цитати                       │
│                    ↓                                 │
│  5. 🌍 Кожен абзац перекладається через обраний      │
│     рушій (Google/Microsoft з підстраховкою)         │
│                    ↓                                 │
│  6. 📄 Збирає форматований документ DOCX/PDF         │
│     зі Змістом, картинками та метаданими             │
│                    ↓                                 │
│  7. ✅ Зберігає в обрану папку та автоматично         │
│     відкриває файл                                   │
└─────────────────────────────────────────────────────┘
```

---

### 🛠️ Встановлення

#### Передумови

- **Python 3.9+**
- Встановлений браузер **Microsoft Edge**
- **Microsoft Word** (потрібен лише для конвертації в PDF через `docx2pdf`)

#### Крок 1: Клонуйте репозиторій

```bash
git clone https://github.com/Maksum867/TreasuryOfKnowledge.git
cd treasury-of-knowledge
```

#### Крок 2: Встановіть залежності

```bash
pip install -r requirements.txt
```

#### Крок 3: Запустіть додаток

```bash
python main.py
```

---

### 📦 Залежності

```
customtkinter
selenium
beautifulsoup4
lxml
python-docx
deep-translator
docx2pdf
plyer
requests
readability-lxml
```

---

### 🗂️ Структура проєкту

```
treasury-of-knowledge/
├── main.py              # Головний файл додатку
├── settings.json        # Налаштування користувача (створюється автоматично)
├── backup_cache/        # Директорія кешу перекладів
├── requirements.txt     # Залежності Python
├── LICENSE              # Ліцензія проєкту
└── README.md            # Цей файл
```

---

### ⚠️ Відмова від відповідальності

Цей інструмент призначений **виключно для особистого навчального використання**. Автор не заохочує порушення авторських прав. Будь ласка, поважайте авторів контенту та використовуйте цей інструмент відповідально. Якщо стаття виявилась для вас цінною, підтримайте її автора.

---

### 🤝 Внесок у проєкт

Внески вітаються! Ви можете:

1. Зробити Fork репозиторію
2. Створити гілку для нової функції (`git checkout -b feature/amazing-feature`)
3. Зафіксувати зміни (`git commit -m 'Add amazing feature'`)
4. Запушити гілку (`git push origin feature/amazing-feature`)
5. Відкрити Pull Request

---

### ☕ Підтримати автора

Якщо цей додаток зекономив вам час та зусилля, ви можете пригостити мене кавою:

[![Monobank](https://img.shields.io/badge/Monobank-Підтримати-yellow?style=for-the-badge)](https://send.monobank.ua/jar/328DrBEZXY)

---

<div align="center">

**Made with ❤️ for free access to knowledge**

**Зроблено з ❤️ заради вільного доступу до знань**

</div>