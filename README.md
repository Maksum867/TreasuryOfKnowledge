

```markdown
# 📜 Treasury of Knowledge

### *Скарбниця Знань*

<div align="center">

**Break paywalls. Bypass geo-blocks. Translate. Save. Own your knowledge.**

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Version](https://img.shields.io/badge/Version-5.0_Ultimate-gold?style=for-the-badge)](#)
[![Windows](https://img.shields.io/badge/OS-Windows_10%2F11-0078D6?style=for-the-badge&logo=windows&logoColor=white)](#)
[![macOS](https://img.shields.io/badge/OS-macOS-000000?style=for-the-badge&logo=apple&logoColor=white)](#)

<br/>

<img src="assets/screenshot.png" alt="Treasury of Knowledge — App Screenshot" width="720"/>

<br/>

*One click. Any article. Any language. Yours forever.*

</div>

<br/>

---

## 🌐 English

---

### 🔍 What is this?

**Treasury of Knowledge** is a powerful desktop application built with **Python**, **CustomTkinter**, and **Selenium** that lets you **bypass paywalls**, **circumvent geo-restrictions**, and **automatically translate** articles from any media outlet in the world — saving them as beautifully formatted **DOCX** or **PDF** files.

No subscriptions. No restrictions. No compromises.

> Paste a link → Get a perfectly formatted, translated document on your desktop.

---

### ⚡ Features

| | Feature | Description |
|---|---|---|
| 🎯 | **Sniper Parsing** | Algorithmically locates the `<article>` container, surgically ignores site menus, and strips all spam — "related articles", "subscribe to newsletter" blocks, ads, and other noise. Pure content only. |
| 🧠 | **Smart Metadata** | Extracts the real author, publication date, subtitle, and **Hero Image** by mining hidden SEO data layers (JSON-LD & OpenGraph) embedded in every modern website. |
| 🖼️ | **Modern Media Engine** | On-the-fly conversion of **WebP** & **AVIF** images to **JPEG** via Pillow for flawless Word compatibility. Extracts video preview thumbnails and inserts clickable links. |
| 🔽 | **System Tray Mode** | Minimize to the system tray (near the clock). Zero resource consumption while idle in the background. |
| 📋 | **Quick Menu (Clipboard)** | Copy a link → Click "Digitize from Clipboard" in the tray → The app silently parses the article in the background and sends you a **Windows push notification** when done. |
| 🚀 | **Smart Launcher (`Start.bat`)** | No terminal knowledge required. Just double-click `Start.bat`. It auto-checks & installs dependencies, **creates a beautiful shortcut with the app icon on your Desktop**, shows a system MessageBox confirmation, and launches the app — no ugly console windows. |
| 🔎 | **DPI Awareness** | Crystal-clear, non-blurry fonts on modern high-DPI monitors (Windows 10/11) powered by native `ctypes` API calls. |
| 🛡️ | **Armored Architecture** | **Anti-crash** protection — gracefully handles broken/malformed websites. **Anti-bot** shield — bypasses Cloudflare protection when downloading images. |
| 🥚 | **The Soul of the App** | Over **15 hidden Easter Eggs** react to your actions — funny messages triggered by specific clicks, links, or even the time of day. Can you find them all? |
| 🌍 | **Bilingual Interface** | Full UI in **Ukrainian** and **English**. |
| 📖 | **Bilingual Save Mode** | Save articles as **Original + Translation** side by side in a single document. |
| 📑 | **Auto Table of Contents** | Automatically generated TOC for long-form articles. |
| ⏱️ | **Reading Time Estimate** | Know how long an article will take to read before you start. |
| 🌗 | **Dark / Light Themes** | Switch between dark and light mode for comfortable reading at any hour. |
| 🗣️ | **6 Translation Languages** | Українська · English · Polski · Deutsch · Français · Español |

---

### ⚙️ How It Works

<div align="center">

```
  ┌─────────────────────────────────┐
  │  📋  Paste an article URL       │
  └────────────────┬────────────────┘
                   ▼
  ┌─────────────────────────────────┐
  │  🌐  Selenium loads the page    │
  │      (bypasses paywall &        │
  │       geo-restrictions)         │
  └────────────────┬────────────────┘
                   ▼
  ┌─────────────────────────────────┐
  │  🎯  Sniper Parsing extracts    │
  │      pure article content       │
  │      (no ads, no spam)          │
  └────────────────┬────────────────┘
                   ▼
  ┌─────────────────────────────────┐
  │  🧠  Smart Metadata finds       │
  │      author, date, hero image   │
  │      via JSON-LD & OpenGraph    │
  └────────────────┬────────────────┘
                   ▼
  ┌─────────────────────────────────┐
  │  🌍  Auto-translation to your   │
  │      chosen language            │
  └────────────────┬────────────────┘
                   ▼
  ┌─────────────────────────────────┐
  │  🖼️  Images converted           │
  │      (WebP/AVIF → JPEG)        │
  └────────────────┬────────────────┘
                   ▼
  ┌─────────────────────────────────┐
  │  📄  Beautiful DOCX or PDF      │
  │      saved to your computer     │
  └────────────────┬────────────────┘
                   ▼
            ✅  D O N E !
```

</div>

---

### 📥 Installation

> **It's literally one click.**

#### Windows (Recommended)

1. **Download** or **clone** this repository:
   ```bash
   git clone https://github.com/your-username/treasury-of-knowledge.git
   ```
2. **Double-click** `Start.bat`

That's it. The smart launcher will:
- ✅ Check if Python 3.9+ is installed
- ✅ Automatically install all required dependencies
- ✅ Create a **beautiful shortcut** with the app icon on your **Desktop**
- ✅ Show a system notification confirming everything is ready
- ✅ Launch the app silently — no console windows, no terminal

> 💡 **You don't need to know what a terminal is.** Just click `Start.bat` and the magic handles the rest.

#### macOS / Manual

1. Make sure you have **Python 3.9+** installed.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run:
   ```bash
   python main.py
   ```

---

### 💬 Feedback

The app has a built-in **Feedback button** — feel free to report bugs, suggest features, or just say hello. Your voice shapes the future of Treasury of Knowledge.

---

### ⚠️ Disclaimer

> **Treasury of Knowledge** is an educational and research tool designed for **personal use only**.
>
> It is intended to help users access publicly available information for learning, study, and archival purposes. The developers do **not** encourage or condone copyright infringement. Please **respect the intellectual property** of journalists and content creators. If you find value in an article — **consider supporting the original publisher**.
>
> Use responsibly. You are solely responsible for how you use this software.

---

### ☕ Support the Author

If this project saved you time, gave you access to knowledge, or simply made you smile with an Easter Egg — consider buying me a coffee:

<div align="center">

[![Donate](https://img.shields.io/badge/💛_Buy_Me_a_Coffee-Support-FFDD00?style=for-the-badge)](https://send.monobank.ua/jar/328DrBEZXY)

**[☕ send.monobank.ua/jar/328DrBEZXY](https://send.monobank.ua/jar/328DrBEZXY)**

</div>

---

---

## 🇺🇦 Українська

---

### 🔍 Що це таке?

**Treasury of Knowledge (Скарбниця Знань)** — це потужна десктопна програма, створена на **Python**, **CustomTkinter** та **Selenium**, яка дозволяє **обходити пейволи** (платні підписки), **геоблокування** та **автоматично перекладати** статті з будь-яких світових ЗМІ — зберігаючи їх у красиво оформлені файли **DOCX** або **PDF**.

Без підписок. Без обмежень. Без компромісів.

> Вставив посилання → Отримав ідеально оформлений, перекладений документ на Робочому столі.

---

### ⚡ Можливості

| | Функція | Опис |
|---|---|---|
| 🎯 | **Снайперський парсинг** | Алгоритмічно знаходить контейнер `<article>`, жорстко ігнорує меню сайту та видаляє весь спам — «схожі новини», «підпишіться на розсилку», рекламу. Тільки чистий контент. |
| 🧠 | **Розумна метадата** | Витягує справжнього автора, дату публікації, підзаголовок та **Головну обкладинку** (Hero Image) через приховані SEO-шари сайтів (JSON-LD та OpenGraph). |
| 🖼️ | **Сучасне медіа** | Конвертація "на льоту" зображень **WebP** та **AVIF** у **JPEG** через Pillow для ідеальної сумісності з Word. Витягує прев'ю-картинки з відео та вставляє клікабельні посилання. |
| 🔽 | **Фоновий режим (System Tray)** | Програма згортається у системний трей (біля годинника). Нуль споживання ресурсів у фоновому режимі. |
| 📋 | **Блискавичне меню (Буфер обміну)** | Скопіюй посилання → Клікни "Оцифрувати з буфера" у треї → Програма тихо парсить статтю у фоні та надсилає **push-сповіщення Windows** про результат. |
| 🚀 | **Розумний лаунчер (`Start.bat`)** | Жодних знань консолі не потрібно. Просто двічі клікни `Start.bat`. Скрипт сам перевірить та встановить залежності, **створить красивий ярлик з іконкою на Робочому столі**, покаже системне MessageBox-повідомлення та запустить програму без чорних вікон консолі. |
| 🔎 | **DPI Awareness** | Ідеально чіткі, не розмиті шрифти на сучасних моніторах у Windows 10/11 завдяки нативному виклику `ctypes`. |
| 🛡️ | **Броньована архітектура** | **Anti-crash** захист — програма грамотно обробляє "зламані" сайти і не падає. **Anti-bot** щит — обходить захист Cloudflare при скачуванні зображень. |
| 🥚 | **"Душа програми"** | Понад **15 прихованих пасхалок** (Easter Eggs), які реагують на ваші дії — смішні повідомлення при певних кліках, посиланнях чи навіть залежно від часу доби. Знайдете всі? |
| 🌍 | **Двомовний інтерфейс** | Повний UI **Українською** та **Англійською** мовами. |
| 📖 | **Двомовне збереження** | Збереження статті як **Оригінал + Переклад** в одному документі. |
| 📑 | **Авто-зміст (TOC)** | Автоматично згенерований зміст для довгих статей. |
| ⏱️ | **Оцінка часу читання** | Дізнайтеся, скільки часу займе читання, ще до початку. |
| 🌗 | **Темна / Світла теми** | Перемикайтесь між темною та світлою темою для комфортного читання в будь-який час. |
| 🗣️ | **6 мов перекладу** | Українська · English · Polski · Deutsch · Français · Español |

---

### ⚙️ Як це працює

<div align="center">

```
  ┌──────────────────────────────────┐
  │  📋  Вставте посилання на статтю │
  └────────────────┬─────────────────┘
                   ▼
  ┌──────────────────────────────────┐
  │  🌐  Selenium завантажує сторінку│
  │      (обходить пейвол та         │
  │       геоблокування)             │
  └────────────────┬─────────────────┘
                   ▼
  ┌──────────────────────────────────┐
  │  🎯  Снайперський парсинг        │
  │      витягує чистий контент      │
  │      (без реклами, без спаму)    │
  └────────────────┬─────────────────┘
                   ▼
  ┌──────────────────────────────────┐
  │  🧠  Розумна метадата знаходить  │
  │      автора, дату, обкладинку    │
  │      через JSON-LD & OpenGraph   │
  └────────────────┬─────────────────┘
                   ▼
  ┌──────────────────────────────────┐
  │  🌍  Авто-переклад на обрану     │
  │      мову                        │
  └────────────────┬─────────────────┘
                   ▼
  ┌──────────────────────────────────┐
  │  🖼️  Конвертація зображень       │
  │      (WebP/AVIF → JPEG)         │
  └────────────────┬─────────────────┘
                   ▼
  ┌──────────────────────────────────┐
  │  📄  Красивий DOCX або PDF       │
  │      збережено на ваш комп'ютер  │
  └────────────────┬─────────────────┘
                   ▼
            ✅  Г О Т О В О !
```

</div>

---

### 📥 Встановлення

> **Це буквально один клік.**

#### Windows (Рекомендовано)

1. **Завантажте** або **клонуйте** цей репозиторій:
   ```bash
   git clone https://github.com/your-username/treasury-of-knowledge.git
   ```
2. **Двічі клікніть** `Start.bat`

Це все. Розумний лаунчер сам:
- ✅ Перевірить наявність Python 3.9+
- ✅ Автоматично встановить усі необхідні бібліотеки
- ✅ Створить **красивий ярлик** з іконкою програми на **Робочому столі**
- ✅ Покаже системне сповіщення, що все готово
- ✅ Запустить програму тихо — без консольних вікон, без терміналу

> 💡 **Вам не потрібно знати, що таке термінал.** Просто клікніть `Start.bat` — і магія зробить все сама.

#### macOS / Вручну

1. Переконайтеся, що у вас встановлено **Python 3.9+**.
2. Встановіть залежності:
   ```bash
   pip install -r requirements.txt
   ```
3. Запустіть:
   ```bash
   python main.py
   ```

---

### 💬 Зворотний зв'язок

У програмі є вбудована **кнопка Зворотного зв'язку** — повідомляйте про помилки, пропонуйте ідеї або просто скажіть привіт. Ваш голос формує майбутнє Скарбниці Знань.

---

### ⚠️ Відмова від відповідальності

> **Treasury of Knowledge** — це освітній та дослідницький інструмент, призначений **виключно для особистого використання**.
>
> Він створений, щоб допомогти користувачам отримувати доступ до публічно доступної інформації для навчання, вивчення та архівних цілей. Розробники **не заохочують і не підтримують** порушення авторських прав. Будь ласка, **поважайте інтелектуальну власність** журналістів і авторів контенту. Якщо стаття була для вас цінною — **підтримайте оригінальне видання**.
>
> Використовуйте відповідально. Ви несете повну відповідальність за те, як ви використовуєте цю програму.

---

### ☕ Підтримати автора

Якщо цей проект зекономив вам час, дав доступ до знань або просто порадував пасхалкою — закиньте автору на каву:

<div align="center">

[![Donate](https://img.shields.io/badge/💛_Закинути_на_каву-Підтримати-FFDD00?style=for-the-badge)](https://send.monobank.ua/jar/328DrBEZXY)

**[☕ send.monobank.ua/jar/328DrBEZXY](https://send.monobank.ua/jar/328DrBEZXY)**

</div>

---

<div align="center">

**Made with ❤️ and ☕ in Ukraine**

*Knowledge should be free. Always.*

</div>
```