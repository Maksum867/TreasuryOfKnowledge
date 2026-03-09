"""
╔══════════════════════════════════════════════════════════════╗
║         ui_components.py — Кастомні PyQt6 віджети           ║
║                                                              ║
║  Кнопки, слайдери, комбобокси, ToggleSwitch                ║
║  Карткові фрейми, мітки секцій                              ║
╚══════════════════════════════════════════════════════════════╝
"""

# ═══════════════════════════════════════════════════════════════
#                        ІМПОРТИ
# ═══════════════════════════════════════════════════════════════

from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QSlider, QFrame,
    QGraphicsDropShadowEffect,
)
from PyQt6.QtCore import (
    Qt, QTimer, pyqtSignal,
)
from PyQt6.QtGui import (
    QFont, QColor, QPainter, QBrush, QCursor,
)

from config import Theme


# ═══════════════════════════════════════════════════════════════
#              NO-SCROLL КОМБОБОКС / СЛАЙДЕР
# ═══════════════════════════════════════════════════════════════

class NoScrollComboBox(QComboBox):
    """Комбобокс, який не змінює значення при прокрутці колесом миші"""

    def wheelEvent(self, event):
        event.ignore()


class NoScrollSlider(QSlider):
    """Слайдер, який не змінює значення при прокрутці колесом миші"""

    def wheelEvent(self, event):
        event.ignore()


# ═══════════════════════════════════════════════════════════════
#                    КНОПКИ
# ═══════════════════════════════════════════════════════════════

class GoldButton(QPushButton):
    """Кнопка з золотим бордером — для другорядних дій"""

    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setFixedHeight(48)
        self.setFont(QFont(Theme.FONT_UI, 14, QFont.Weight.Bold))
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {Theme.GOLD};
                border: 2px solid {Theme.GOLD};
                border-radius: 14px;
                padding: 8px 36px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {Theme.GOLD};
                color: {Theme.BG_PRIMARY};
            }}
            QPushButton:pressed {{
                background-color: {Theme.GOLD_HOVER};
            }}
        """)


class PrimaryButton(QPushButton):
    """Головна зелена кнопка — для основних дій"""

    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setFixedHeight(72)
        self.setFont(QFont(Theme.FONT_UI, 20, QFont.Weight.Bold))
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {Theme.GREEN};
                color: white;
                border: none;
                border-radius: 20px;
                padding: 12px 40px;
                font-weight: bold;
                font-size: 20px;
            }}
            QPushButton:hover {{
                background-color: {Theme.GREEN_LIGHT};
            }}
            QPushButton:pressed {{
                background-color: {Theme.GREEN_HOVER};
            }}
            QPushButton:disabled {{
                background-color: {Theme.BG_HOVER};
                color: {Theme.TEXT_MUTED};
            }}
        """)

    def add_shadow(self):
        """Додає тінь до кнопки"""
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25)
        shadow.setColor(QColor(45, 90, 39, 120))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)


class DangerButton(QPushButton):
    """Червона кнопка — для скасування"""

    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setFixedHeight(72)
        self.setFont(QFont(Theme.FONT_UI, 16, QFont.Weight.Bold))
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {Theme.RED};
                border: 2px solid {Theme.RED};
                border-radius: 20px;
                padding: 12px 32px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {Theme.RED};
                color: white;
            }}
            QPushButton:pressed {{
                background-color: {Theme.RED_HOVER};
                color: white;
            }}
            QPushButton:disabled {{
                border-color: {Theme.TEXT_MUTED};
                color: {Theme.TEXT_MUTED};
            }}
        """)


class IconButton(QPushButton):
    """Іконка-кнопка без фону (для ⚙️, ← тощо)"""

    def __init__(self, text="", size=40, font_size=28, parent=None):
        super().__init__(text, parent)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setFixedSize(size, size)
        self.setFont(QFont("Arial", font_size))
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {Theme.GOLD};
                border: none;
                border-radius: {size // 2}px;
            }}
            QPushButton:hover {{
                background-color: {Theme.BG_HOVER};
            }}
        """)


class FeatureButton(QPushButton):
    """Кнопка для меню "Про додаток" з кольоровим фоном"""

    def __init__(self, text="", bg_color="", hover_color="", parent=None):
        super().__init__(text, parent)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setFixedHeight(50)
        self.setFixedWidth(260)
        self.setFont(QFont(Theme.FONT_UI, 14, QFont.Weight.Bold))
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_color};
                color: white;
                border: none;
                border-radius: 16px;
                padding: 10px 24px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
        """)


# ═══════════════════════════════════════════════════════════════
#               КАРТКОВІ ФРЕЙМИ ТА МІТКИ
# ═══════════════════════════════════════════════════════════════

class CardFrame(QFrame):
    """Карточний контейнер з заокругленими кутами"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {Theme.BG_CARD};
                border: 1px solid {Theme.BORDER};
                border-radius: 16px;
            }}
        """)


class SectionLabel(QLabel):
    """Заголовок секції в налаштуваннях"""

    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setFont(QFont(Theme.FONT_UI, 15, QFont.Weight.Bold))
        self.setStyleSheet(f"color: {Theme.TEXT_PRIMARY}; padding: 4px 0;")


class GoldSectionLabel(QLabel):
    """Золотий заголовок секції"""

    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setFont(QFont(Theme.FONT_UI, 15, QFont.Weight.Bold))
        self.setStyleSheet(f"color: {Theme.GOLD}; padding: 8px 0;")


class MutedLabel(QLabel):
    """Сірий підпис"""

    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setFont(QFont(Theme.FONT_UI, 12))
        self.setStyleSheet(f"color: {Theme.TEXT_MUTED};")


# ═══════════════════════════════════════════════════════════════
#            КАСТОМНИЙ TOGGLE SWITCH (замість QCheckBox)
# ═══════════════════════════════════════════════════════════════

class ToggleSwitch(QWidget):
    """
    Красивий перемикач (Toggle Switch) у стилі iOS/macOS.

    Сигнали:
        toggled(bool) — викликається при зміні стану.

    Використання:
        toggle = ToggleSwitch("⏱ Час читання", checked=True)
        toggle.toggled.connect(lambda val: print(val))
    """

    toggled = pyqtSignal(bool)

    # ── Константи розмірів ──
    TRACK_WIDTH = 50
    TRACK_HEIGHT = 24
    TRACK_RADIUS = 12
    KNOB_SIZE = 18
    KNOB_MARGIN_Y = 5
    KNOB_OFF_X = 4.0
    KNOB_ON_X = 26.0
    ANIMATION_STEPS = 8
    ANIMATION_INTERVAL_MS = 16

    def __init__(self, text="", checked=False, parent=None):
        super().__init__(parent)
        self._checked = checked
        self._animation_pos = (
            self.KNOB_ON_X if checked else self.KNOB_OFF_X
        )

        self.setFixedHeight(40)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # ── Горизонтальний layout ──
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        # 1. Віджет для малювання повзунка
        self.switch_visual = QWidget()
        self.switch_visual.setFixedSize(
            self.TRACK_WIDTH, self.TRACK_HEIGHT + 4
        )
        self.switch_visual.setAttribute(
            Qt.WidgetAttribute.WA_StyledBackground, False
        )
        self.switch_visual.paintEvent = self._paint_switch

        # 2. Текстова мітка
        self.label = QLabel(text)
        self.label.setFont(QFont(Theme.FONT_UI, 14))
        self.label.setStyleSheet(f"color: {Theme.TEXT_PRIMARY};")

        # ── Збірка ──
        layout.addWidget(self.switch_visual)
        layout.addWidget(self.label)
        layout.addStretch()

    # ── Малювання ──

    def _paint_switch(self, event):
        """Малює повзунок (трек + кружечок)"""
        painter = QPainter(self.switch_visual)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Трек (фон)
        if self._checked:
            painter.setBrush(QBrush(QColor(Theme.GOLD)))
        else:
            painter.setBrush(QBrush(QColor(Theme.BORDER)))

        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(
            0, 2,
            self.TRACK_WIDTH, self.TRACK_HEIGHT,
            self.TRACK_RADIUS, self.TRACK_RADIUS
        )

        # Кнопка (білий кружечок)
        painter.setBrush(QBrush(QColor("white")))
        painter.drawEllipse(
            int(self._animation_pos),
            self.KNOB_MARGIN_Y,
            self.KNOB_SIZE,
            self.KNOB_SIZE
        )

        painter.end()

    # ── Взаємодія ──

    def mousePressEvent(self, event):
        """Обробка кліку — перемикання стану"""
        self._checked = not self._checked
        target = self.KNOB_ON_X if self._checked else self.KNOB_OFF_X
        self._start_animation(target)
        self.toggled.emit(self._checked)
        super().mousePressEvent(event)

    def _start_animation(self, target):
        """Плавна анімація переміщення кружечка"""
        start = self._animation_pos
        step = (target - start) / self.ANIMATION_STEPS
        self._anim_timer = QTimer(self)

        def animate():
            self._animation_pos += step
            if ((step > 0 and self._animation_pos >= target) or
                    (step < 0 and self._animation_pos <= target)):
                self._animation_pos = target
                self._anim_timer.stop()
            self.switch_visual.update()

        self._anim_timer.timeout.connect(animate)
        self._anim_timer.start(self.ANIMATION_INTERVAL_MS)

    # ── Публічний API ──

    def isChecked(self):
        """Повертає поточний стан перемикача"""
        return self._checked

    def setChecked(self, val):
        """Встановлює стан перемикача без анімації"""
        self._checked = val
        self._animation_pos = (
            self.KNOB_ON_X if val else self.KNOB_OFF_X
        )
        self.switch_visual.update()

    def setText(self, text):
        """Змінює текст мітки"""
        self.label.setText(text)

    def text(self):
        """Повертає текст мітки"""
        return self.label.text()