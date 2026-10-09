"""
Settings Tab - AIChild
API key, model, language, name configuration
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFrame, QComboBox
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

from core.translations import t
from core.database import get_identity, set_identity, log_operation


class SettingsTab(QWidget):
    def __init__(self, lang: str, main_window=None):
        super().__init__()
        self._lang = lang
        self._main_window = main_window
        self._build_ui()
        self._load_settings()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(20)

        title = QLabel(t("settings_title", self._lang))
        title.setObjectName("sectionTitle")
        title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        layout.addWidget(title)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(sep)

        # Child Name
        layout.addWidget(self._field_label(t("settings_name", self._lang)))
        self._name_input = QLineEdit()
        self._name_input.setPlaceholderText(t("settings_name_placeholder", self._lang))
        self._name_input.setFixedHeight(40)
        layout.addWidget(self._name_input)

        # API Key
        layout.addWidget(self._field_label(t("settings_api_key", self._lang)))
        self._api_key_input = QLineEdit()
        self._api_key_input.setPlaceholderText(t("settings_api_placeholder", self._lang))
        self._api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self._api_key_input.setFixedHeight(40)
        layout.addWidget(self._api_key_input)

        # Show/hide API key
        show_row = QHBoxLayout()
        show_row.setAlignment(Qt.AlignmentFlag.AlignRight)
        self._show_key_btn = QPushButton("👁 Show Key")
        self._show_key_btn.setObjectName("secondaryBtn")
        self._show_key_btn.setFixedHeight(28)
        self._show_key_btn.setCheckable(True)
        self._show_key_btn.toggled.connect(self._toggle_key_visibility)
        show_row.addWidget(self._show_key_btn)
        layout.addLayout(show_row)

        # Model info
        layout.addWidget(self._field_label(t("settings_model", self._lang)))
        model_label = QLabel("openai/gpt-4o-mini  (via OpenRouter)")
        model_label.setObjectName("hintLabel")
        model_label.setFont(QFont("Cascadia Code", 9))
        layout.addWidget(model_label)

        # Language
        layout.addWidget(self._field_label(t("settings_lang", self._lang)))
        self._lang_combo = QComboBox()
        self._lang_combo.addItem("English", "en")
        self._lang_combo.addItem("فارسی (Persian)", "fa")
        self._lang_combo.setFixedHeight(38)
        layout.addWidget(self._lang_combo)

        layout.addStretch()

        sep2 = QFrame()
        sep2.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(sep2)

        # Save button
        btn_row = QHBoxLayout()
        self._save_btn = QPushButton(t("settings_save", self._lang))
        self._save_btn.setObjectName("primaryBtn")
        self._save_btn.setFixedHeight(44)
        self._save_btn.setMinimumWidth(180)
        self._save_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self._save_btn.clicked.connect(self._save_settings)

        self._saved_label = QLabel("")
        self._saved_label.setObjectName("successLabel")

        btn_row.addWidget(self._save_btn)
        btn_row.addSpacing(16)
        btn_row.addWidget(self._saved_label)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        # API key hint
        api_hint = QLabel(
            "🔑 Get your API key at openrouter.ai/keys"
            if self._lang == "en" else
            "🔑 کلید API رو از openrouter.ai/keys بگیر"
        )
        api_hint.setObjectName("hintLabel")
        layout.addWidget(api_hint)

    def _field_label(self, text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setObjectName("fieldLabel")
        lbl.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        return lbl

    def _load_settings(self):
        name = get_identity("name", "")
        key = get_identity("api_key", "")
        lang = get_identity("language", "en")

        self._name_input.setText(name)
        self._api_key_input.setText(key)

        idx = self._lang_combo.findData(lang)
        if idx >= 0:
            self._lang_combo.setCurrentIndex(idx)

    def _save_settings(self):
        name = self._name_input.text().strip()
        api_key = self._api_key_input.text().strip()
        lang = self._lang_combo.currentData()

        if name:
            set_identity("name", name)
            if self._main_window:
                self._main_window.refresh_name(name)

        if api_key:
            set_identity("api_key", api_key)

        if lang:
            set_identity("language", lang)

        log_operation("SUCCESS", "Settings saved")
        self._saved_label.setText(t("settings_saved", self._lang))
        QTimer.singleShot(2500, lambda: self._saved_label.setText(""))

    def _toggle_key_visibility(self, checked: bool):
        if checked:
            self._api_key_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self._show_key_btn.setText("🙈 Hide Key")
        else:
            self._api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
            self._show_key_btn.setText("👁 Show Key")

    def set_lang(self, lang: str):
        self._lang = lang
