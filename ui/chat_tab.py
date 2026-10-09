"""
Chat Tab - AIChild
Message bubbles, input area, background auto-learning
"""

import datetime
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton,
    QLabel, QScrollArea, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QKeyEvent

from core.translations import t
from core.database import get_recent_messages, log_operation


class ChatWorker(QThread):
    """Background thread for AI chat"""
    response_ready = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    learning_started = pyqtSignal(list)
    learning_done = pyqtSignal()

    def __init__(self, message: str, lang: str):
        super().__init__()
        self.message = message
        self.lang = lang

    def run(self):
        try:
            from core.ai_engine import chat, analyze_and_learn, learn_topic
            response = chat(self.message, self.lang)
            self.response_ready.emit(response)

            # Auto-learn related topics
            topics = analyze_and_learn(self.message, self.lang)
            if topics:
                self.learning_started.emit(topics)
                for topic in topics:
                    try:
                        learn_topic(topic, self.lang)
                    except Exception as e:
                        log_operation("WARNING", f"Auto-learn '{topic}' failed: {e}")
                self.learning_done.emit()

        except Exception as e:
            self.error_occurred.emit(str(e))


class BubbleWidget(QWidget):
    """A single chat message bubble"""
    def __init__(self, role: str, content: str, timestamp: str = "", parent=None):
        super().__init__(parent)
        self._build(role, content, timestamp)

    def _build(self, role: str, content: str, timestamp: str):
        outer = QHBoxLayout(self)
        outer.setContentsMargins(8, 3, 8, 3)
        outer.setSpacing(0)

        bubble = QLabel(content)
        bubble.setWordWrap(True)
        bubble.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        bubble.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        if role == "user":
            bubble.setObjectName("userBubble")
            outer.addStretch()
            outer.addWidget(bubble)
            bubble.setMaximumWidth(600)
        elif role == "system":
            bubble.setObjectName("systemBubble")
            bubble.setAlignment(Qt.AlignmentFlag.AlignCenter)
            outer.addStretch()
            outer.addWidget(bubble)
            outer.addStretch()
        else:
            bubble.setObjectName("aiBubble")
            # Avatar emoji
            avatar = QLabel("🤖")
            avatar.setFont(QFont("Segoe UI Emoji", 14))
            avatar.setFixedWidth(32)
            avatar.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
            outer.addWidget(avatar)
            outer.addSpacing(6)
            outer.addWidget(bubble)
            outer.addStretch()
            bubble.setMaximumWidth(620)


class ChatTab(QWidget):
    def __init__(self, lang: str):
        super().__init__()
        self._lang = lang
        self._worker = None
        self._build_ui()
        self._load_history()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Messages scroll area
        self._scroll = QScrollArea()
        self._scroll.setObjectName("chatArea")
        self._scroll.setWidgetResizable(True)
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self._messages_widget = QWidget()
        self._messages_widget.setObjectName("chatArea")
        self._messages_layout = QVBoxLayout(self._messages_widget)
        self._messages_layout.setContentsMargins(0, 10, 0, 10)
        self._messages_layout.setSpacing(4)
        self._messages_layout.addStretch()

        self._scroll.setWidget(self._messages_widget)
        layout.addWidget(self._scroll, 1)

        # Status label
        self._status_label = QLabel("")
        self._status_label.setObjectName("thinkingLabel")
        self._status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._status_label.setFixedHeight(22)
        layout.addWidget(self._status_label)

        # Input area
        input_frame = QFrame()
        input_frame.setObjectName("inputFrame")
        input_frame.setStyleSheet("""
            #inputFrame {
                background-color: #161B22;
                border-top: 1px solid #1E2A3A;
            }
        """)
        input_layout = QHBoxLayout(input_frame)
        input_layout.setContentsMargins(12, 10, 12, 10)
        input_layout.setSpacing(10)

        self._input = QTextEdit()
        self._input.setObjectName("chatInput")
        self._input.setPlaceholderText(t("chat_placeholder", self._lang))
        self._input.setFixedHeight(60)
        self._input.setAcceptRichText(False)
        self._input.installEventFilter(self)

        self._send_btn = QPushButton(t("chat_send", self._lang))
        self._send_btn.setObjectName("primaryBtn")
        self._send_btn.setFixedSize(90, 44)
        self._send_btn.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self._send_btn.clicked.connect(self._send_message)

        self._clear_btn = QPushButton("🗑")
        self._clear_btn.setObjectName("secondaryBtn")
        self._clear_btn.setFixedSize(44, 44)
        self._clear_btn.setFont(QFont("Segoe UI Emoji", 12))
        self._clear_btn.setToolTip(t("chat_clear", self._lang))
        self._clear_btn.clicked.connect(self._clear_chat)

        input_layout.addWidget(self._input)
        input_layout.addWidget(self._clear_btn)
        input_layout.addWidget(self._send_btn)

        layout.addWidget(input_frame)

    def eventFilter(self, obj, event):
        if obj is self._input and isinstance(event, QKeyEvent):
            if (event.key() == Qt.Key.Key_Return and
                    event.modifiers() == Qt.KeyboardModifier.NoModifier):
                self._send_message()
                return True
        return super().eventFilter(obj, event)

    def _load_history(self):
        messages = get_recent_messages(30)
        for msg in messages:
            self._add_bubble(msg["role"], msg["content"])

    def _send_message(self):
        text = self._input.toPlainText().strip()
        if not text or self._worker is not None:
            return

        self._input.clear()
        self._add_bubble("user", text)
        self._set_status(t("chat_thinking", self._lang))
        self._send_btn.setEnabled(False)

        self._worker = ChatWorker(text, self._lang)
        self._worker.response_ready.connect(self._on_response)
        self._worker.error_occurred.connect(self._on_error)
        self._worker.learning_started.connect(self._on_learning_started)
        self._worker.learning_done.connect(self._on_learning_done)
        self._worker.finished.connect(self._on_worker_done)
        self._worker.start()

    def _on_response(self, text: str):
        self._add_bubble("assistant", text)

    def _on_error(self, error: str):
        self._add_bubble("system", f"⚠️ {error}")
        log_operation("ERROR", f"Chat error: {error}")

    def _on_learning_started(self, topics: list):
        self._set_status(f"📖 {t('auto_learn_start', self._lang)} {', '.join(topics)}")

    def _on_learning_done(self):
        self._set_status(t("auto_learn_done", self._lang))
        QTimer.singleShot(3000, lambda: self._set_status(""))

    def _on_worker_done(self):
        self._worker = None
        self._send_btn.setEnabled(True)
        self._set_status("")

    def _add_bubble(self, role: str, content: str):
        bubble = BubbleWidget(role, content)
        # Insert before the stretch at the end
        count = self._messages_layout.count()
        self._messages_layout.insertWidget(count - 1, bubble)
        # Scroll to bottom
        QTimer.singleShot(50, self._scroll_bottom)

    def _scroll_bottom(self):
        sb = self._scroll.verticalScrollBar()
        sb.setValue(sb.maximum())

    def _set_status(self, text: str):
        self._status_label.setText(text)

    def _clear_chat(self):
        from core.database import clear_conversations
        while self._messages_layout.count() > 1:
            item = self._messages_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        clear_conversations()
        log_operation("INFO", "Chat history cleared")

    def set_lang(self, lang: str):
        self._lang = lang
        self._input.setPlaceholderText(t("chat_placeholder", lang))
        self._send_btn.setText(t("chat_send", lang))
