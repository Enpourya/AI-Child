"""
Welcome Dialog - AIChild
First-run setup: name, API key, language
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from core.translations import t
from core.database import initialize_identity, set_identity


class WelcomeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("AIChild — First Setup")
        self.setFixedSize(480, 520)
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowTitleHint)
        self.setObjectName("welcomeDialog")
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 32, 40, 32)
        layout.setSpacing(18)

        # Header
        emoji = QLabel("🤖")
        emoji.setFont(QFont("Segoe UI Emoji", 52))
        emoji.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(emoji)

        title = QLabel("Welcome to AIChild")
        title.setObjectName("welcomeTitle")
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel("Your personal AI companion that grows with you")
        subtitle.setObjectName("welcomeSubtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(sep)

        # Name input
        name_label = QLabel("What should I call your AI child?")
        name_label.setObjectName("fieldLabel")
        name_label.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        layout.addWidget(name_label)

        self._name_input = QLineEdit()
        self._name_input.setPlaceholderText("e.g. Aria, Dani, Nova, Roya...")
        self._name_input.setFixedHeight(42)
        self._name_input.setFont(QFont("Segoe UI", 12))
        layout.addWidget(self._name_input)

        # API key
        key_label = QLabel("OpenRouter API Key:")
        key_label.setObjectName("fieldLabel")
        key_label.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        layout.addWidget(key_label)

        self._key_input = QLineEdit()
        self._key_input.setPlaceholderText("sk-or-v1-...")
        self._key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self._key_input.setFixedHeight(42)
        layout.addWidget(self._key_input)

        key_hint = QLabel("🔑 Get your key at: openrouter.ai/keys (free tier available)")
        key_hint.setObjectName("hintLabel")
        layout.addWidget(key_hint)

        # Language
        lang_label = QLabel("Preferred Language:")
        lang_label.setObjectName("fieldLabel")
        lang_label.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        layout.addWidget(lang_label)

        self._lang_combo = QComboBox()
        self._lang_combo.addItem("English", "en")
        self._lang_combo.addItem("فارسی (Persian)", "fa")
        self._lang_combo.setFixedHeight(40)
        layout.addWidget(self._lang_combo)

        # Error label
        self._error_label = QLabel("")
        self._error_label.setObjectName("errorLabel")
        self._error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._error_label)

        layout.addStretch()

        # Create button
        self._create_btn = QPushButton("🚀  Create My AI Child")
        self._create_btn.setObjectName("primaryBtn")
        self._create_btn.setFixedHeight(50)
        self._create_btn.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self._create_btn.clicked.connect(self._on_create)
        layout.addWidget(self._create_btn)

    def _on_create(self):
        name = self._name_input.text().strip()
        api_key = self._key_input.text().strip()
        lang = self._lang_combo.currentData()

        if not name:
            self._error_label.setText("⚠ Please enter a name for your AI child")
            self._name_input.setFocus()
            return

        if not api_key:
            self._error_label.setText("⚠ API key is required to connect to OpenRouter")
            self._key_input.setFocus()
            return

        # Save to DB
        initialize_identity(name, lang)
        set_identity("api_key", api_key)

        self.accept()
