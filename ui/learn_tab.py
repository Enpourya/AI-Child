"""
Learn Tab - AIChild
Manually teach topics, view what was learned
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTextEdit, QFrame, QScrollArea
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont

from core.translations import t
from core.database import get_knowledge_count, get_knowledge_size_kb, log_operation


class LearnWorker(QThread):
    done = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, topic: str, lang: str):
        super().__init__()
        self.topic = topic
        self.lang = lang

    def run(self):
        try:
            from core.ai_engine import learn_topic
            result = learn_topic(self.topic, self.lang)
            self.done.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class LearnTab(QWidget):
    def __init__(self, lang: str):
        super().__init__()
        self._lang = lang
        self._worker = None
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)

        # Title
        title = QLabel(t("learn_title", self._lang))
        title.setObjectName("sectionTitle")
        title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        layout.addWidget(title)

        # Stats bar
        self._stats_label = QLabel()
        self._stats_label.setObjectName("hintLabel")
        self._update_stats()
        layout.addWidget(self._stats_label)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(sep)

        # Topic input
        topic_label = QLabel(t("learn_topic_label", self._lang))
        topic_label.setObjectName("fieldLabel")
        layout.addWidget(topic_label)

        input_row = QHBoxLayout()
        input_row.setSpacing(10)

        self._topic_input = QLineEdit()
        self._topic_input.setPlaceholderText(t("learn_topic_placeholder", self._lang))
        self._topic_input.setFixedHeight(40)
        self._topic_input.returnPressed.connect(self._start_learn)

        self._learn_btn = QPushButton(t("learn_btn", self._lang))
        self._learn_btn.setObjectName("primaryBtn")
        self._learn_btn.setFixedHeight(40)
        self._learn_btn.setMinimumWidth(160)
        self._learn_btn.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self._learn_btn.clicked.connect(self._start_learn)

        input_row.addWidget(self._topic_input)
        input_row.addWidget(self._learn_btn)
        layout.addLayout(input_row)

        # Status
        self._status_label = QLabel("")
        self._status_label.setObjectName("thinkingLabel")
        self._status_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self._status_label)

        # Result
        result_title = QLabel(t("learn_result_title", self._lang))
        result_title.setObjectName("fieldLabel")
        layout.addWidget(result_title)

        self._result_text = QTextEdit()
        self._result_text.setObjectName("learnResult")
        self._result_text.setReadOnly(True)
        self._result_text.setPlaceholderText(
            "Learning results will appear here..." if self._lang == "en"
            else "نتایج یادگیری اینجا نمایش داده می‌شود..."
        )
        layout.addWidget(self._result_text, 1)

    def _start_learn(self):
        topic = self._topic_input.text().strip()
        if not topic or self._worker is not None:
            return

        self._learn_btn.setEnabled(False)
        self._status_label.setObjectName("thinkingLabel")
        self._set_status(t("learn_progress", self._lang))
        self._result_text.clear()

        self._worker = LearnWorker(topic, self._lang)
        self._worker.done.connect(self._on_done)
        self._worker.error.connect(self._on_error)
        self._worker.finished.connect(self._on_finished)
        self._worker.start()

    def _on_done(self, result: str):
        self._result_text.setPlainText(result)
        self._status_label.setObjectName("successLabel")
        self._set_status(t("learn_success", self._lang))
        self._topic_input.clear()
        self._update_stats()

    def _on_error(self, error: str):
        self._status_label.setObjectName("errorLabel")
        self._set_status(f"{t('learn_error', self._lang)}: {error}")
        log_operation("ERROR", f"Learn failed: {error}")

    def _on_finished(self):
        self._worker = None
        self._learn_btn.setEnabled(True)

    def _set_status(self, text: str):
        self._status_label.setText(text)
        # Force style refresh
        self._status_label.style().unpolish(self._status_label)
        self._status_label.style().polish(self._status_label)

    def _update_stats(self):
        count = get_knowledge_count()
        size = get_knowledge_size_kb()
        lang = self._lang
        if lang == "fa":
            self._stats_label.setText(
                f"📚 {count} موضوع یاد گرفته‌شده — {size} کیلوبایت دانش ذخیره‌شده"
            )
        else:
            self._stats_label.setText(
                f"📚 {count} topics learned — {size} KB of knowledge stored"
            )

    def set_lang(self, lang: str):
        self._lang = lang
        # Refresh labels
        for widget, key in [
            (self._topic_input, "learn_topic_placeholder"),
            (self._learn_btn, "learn_btn"),
        ]:
            if hasattr(widget, "setPlaceholderText"):
                widget.setPlaceholderText(t(key, lang))
            elif hasattr(widget, "setText"):
                widget.setText(t(key, lang))
        self._update_stats()
