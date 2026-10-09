"""
Main Window - AIChild
PyQt6 main application window with all tabs and status bar
"""

import sys
import os
import datetime
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QLabel, QFrame, QPushButton, QSizePolicy,
    QStatusBar
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QThread
from PyQt6.QtGui import QFont, QIcon, QPalette, QColor

from core.database import (
    get_identity, set_identity, get_knowledge_count, get_knowledge_size_kb,
    get_age_string, log_operation, init_db
)
from core.translations import t
from ui.chat_tab import ChatTab
from ui.learn_tab import LearnTab
from ui.update_tab import UpdateTab
from ui.ops_tab import OpsTab
from ui.settings_tab import SettingsTab
from ui.welcome_dialog import WelcomeDialog
from ui.styles import DARK_STYLE


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._lang = get_identity("language", "en")
        self._setup_window()
        self._build_ui()
        self._start_status_timer()
        log_operation("INFO", "Application started")

    def _setup_window(self):
        self.setWindowTitle(t("app_title", self._lang))
        self.setMinimumSize(1000, 700)
        self.resize(1100, 750)
        self.setStyleSheet(DARK_STYLE)

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root_layout = QVBoxLayout(central)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # Header
        header = self._build_header()
        root_layout.addWidget(header)

        # Tabs
        self._tabs = QTabWidget()
        self._tabs.setObjectName("mainTabs")
        self._tabs.setDocumentMode(True)

        self._chat_tab = ChatTab(self._lang)
        self._learn_tab = LearnTab(self._lang)
        self._update_tab = UpdateTab(self._lang)
        self._ops_tab = OpsTab(self._lang)
        self._settings_tab = SettingsTab(self._lang, self)

        self._tabs.addTab(self._chat_tab, t("tab_chat", self._lang))
        self._tabs.addTab(self._learn_tab, t("tab_learn", self._lang))
        self._tabs.addTab(self._update_tab, t("tab_update", self._lang))
        self._tabs.addTab(self._ops_tab, t("tab_ops", self._lang))
        self._tabs.addTab(self._settings_tab, t("tab_settings", self._lang))

        root_layout.addWidget(self._tabs)

        # Status bar
        self._build_status_bar()

    def _build_header(self) -> QWidget:
        header = QFrame()
        header.setObjectName("header")
        header.setFixedHeight(70)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(20, 8, 20, 8)

        # Avatar + Name
        avatar_label = QLabel("🤖")
        avatar_label.setFont(QFont("Segoe UI Emoji", 28))
        avatar_label.setFixedWidth(50)

        name_col = QVBoxLayout()
        name_col.setSpacing(2)

        child_name = get_identity("name", "AI Child")
        self._name_label = QLabel(child_name)
        self._name_label.setObjectName("childName")
        self._name_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))

        self._subtitle_label = QLabel(self._get_subtitle())
        self._subtitle_label.setObjectName("childSubtitle")
        self._subtitle_label.setFont(QFont("Segoe UI", 9))

        name_col.addWidget(self._name_label)
        name_col.addWidget(self._subtitle_label)

        # Stats row
        stats_col = QVBoxLayout()
        stats_col.setSpacing(4)
        stats_col.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self._stats_label = QLabel()
        self._stats_label.setObjectName("statsLabel")
        self._stats_label.setFont(QFont("Segoe UI", 9))
        self._stats_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self._update_stats()

        # Language toggle
        lang_row = QHBoxLayout()
        lang_row.setSpacing(6)
        lang_row.setAlignment(Qt.AlignmentFlag.AlignRight)

        self._btn_en = QPushButton("EN")
        self._btn_fa = QPushButton("FA")
        for btn in [self._btn_en, self._btn_fa]:
            btn.setObjectName("langBtn")
            btn.setFixedSize(36, 24)
            btn.setFont(QFont("Segoe UI", 8, QFont.Weight.Bold))

        self._btn_en.clicked.connect(lambda: self._switch_lang("en"))
        self._btn_fa.clicked.connect(lambda: self._switch_lang("fa"))
        self._highlight_lang_btn()

        lang_row.addWidget(self._btn_en)
        lang_row.addWidget(self._btn_fa)

        stats_col.addWidget(self._stats_label)
        stats_col.addLayout(lang_row)

        layout.addWidget(avatar_label)
        layout.addLayout(name_col)
        layout.addStretch()
        layout.addLayout(stats_col)

        return header

    def _get_subtitle(self) -> str:
        version = get_identity("version", "1.0.0")
        age = get_age_string()
        lang = self._lang
        if lang == "fa":
            return f"نسخه {version} | سن: {age}"
        return f"v{version} | Age: {age}"

    def _update_stats(self):
        count = get_knowledge_count()
        size = get_knowledge_size_kb()
        lang = self._lang
        if lang == "fa":
            self._stats_label.setText(
                f"📚 {count} مورد یادگرفته‌شده | {size} KB دانش"
            )
        else:
            self._stats_label.setText(
                f"📚 {count} topics learned | {size} KB of knowledge"
            )

    def _build_status_bar(self):
        self._status_bar = QStatusBar()
        self._status_bar.setObjectName("mainStatusBar")
        self.setStatusBar(self._status_bar)

        self._status_time = QLabel()
        self._status_time.setFont(QFont("Segoe UI", 8))
        self._status_bar.addPermanentWidget(self._status_time)
        self._update_clock()

    def _update_clock(self):
        now = datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
        self._status_time.setText(now)

    def _start_status_timer(self):
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(1000)  # every second

    def _tick(self):
        self._update_clock()
        # Update subtitle and stats every 10s
        if datetime.datetime.now().second % 10 == 0:
            self._subtitle_label.setText(self._get_subtitle())
            self._update_stats()

    def _switch_lang(self, lang: str):
        if lang == self._lang:
            return
        self._lang = lang
        set_identity("language", lang)
        self._highlight_lang_btn()
        self._reload_ui()
        log_operation("INFO", f"Language switched to {lang}")

    def _highlight_lang_btn(self):
        self._btn_en.setProperty("active", self._lang == "en")
        self._btn_fa.setProperty("active", self._lang == "fa")
        self._btn_en.style().unpolish(self._btn_en)
        self._btn_en.style().polish(self._btn_en)
        self._btn_fa.style().unpolish(self._btn_fa)
        self._btn_fa.style().polish(self._btn_fa)

    def _reload_ui(self):
        """Reload all tab labels and content for new language"""
        self._tabs.setTabText(0, t("tab_chat", self._lang))
        self._tabs.setTabText(1, t("tab_learn", self._lang))
        self._tabs.setTabText(2, t("tab_update", self._lang))
        self._tabs.setTabText(3, t("tab_ops", self._lang))
        self._tabs.setTabText(4, t("tab_settings", self._lang))
        self._subtitle_label.setText(self._get_subtitle())
        self._update_stats()
        # Propagate to tabs
        for tab in [self._chat_tab, self._learn_tab, self._update_tab,
                    self._ops_tab, self._settings_tab]:
            if hasattr(tab, "set_lang"):
                tab.set_lang(self._lang)

    def refresh_name(self, new_name: str):
        """Called from settings when name changes"""
        self._name_label.setText(new_name)

    def closeEvent(self, event):
        log_operation("INFO", "Application closed")
        event.accept()
