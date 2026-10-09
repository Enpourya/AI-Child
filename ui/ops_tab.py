"""
Operations Tab - AIChild
Live operations log with color coding, filtering, and file export
"""

import datetime
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QFrame, QComboBox
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor, QTextCharFormat, QTextCursor

from core.translations import t
from core.database import get_recent_operations, log_operation

LEVEL_COLORS = {
    "INFO":    "#8BAFC0",
    "SUCCESS": "#4CAF82",
    "WARNING": "#F0C060",
    "ERROR":   "#F07070",
}

LEVEL_ICONS = {
    "INFO":    "ℹ",
    "SUCCESS": "✓",
    "WARNING": "⚠",
    "ERROR":   "✗",
}


class OpsTab(QWidget):
    def __init__(self, lang: str):
        super().__init__()
        self._lang = lang
        self._filter = "ALL"
        self._build_ui()
        self._load_history()
        self._start_live_refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(10)

        # Header row
        hdr = QHBoxLayout()
        title = QLabel(t("ops_title", self._lang))
        title.setObjectName("sectionTitle")
        title.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        hdr.addWidget(title)
        hdr.addStretch()

        # Filter combo
        self._filter_combo = QComboBox()
        self._filter_combo.addItems([
            t("ops_filter_all", self._lang),
            t("ops_filter_error", self._lang),
            t("ops_filter_info", self._lang),
        ])
        self._filter_combo.setFixedWidth(140)
        self._filter_combo.currentIndexChanged.connect(self._on_filter_changed)

        self._clear_btn = QPushButton(t("ops_clear", self._lang))
        self._clear_btn.setObjectName("secondaryBtn")
        self._clear_btn.setFixedHeight(30)
        self._clear_btn.clicked.connect(self._clear_log)

        hdr.addWidget(self._filter_combo)
        hdr.addSpacing(8)
        hdr.addWidget(self._clear_btn)
        layout.addLayout(hdr)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(sep)

        # Stats row
        self._stats_label = QLabel()
        self._stats_label.setObjectName("hintLabel")
        self._update_stats_label()
        layout.addWidget(self._stats_label)

        # Log area (read-only rich text)
        self._log = QTextEdit()
        self._log.setObjectName("opsLog")
        self._log.setReadOnly(True)
        self._log.setFont(QFont("Cascadia Code", 9))
        layout.addWidget(self._log, 1)

        # Bottom info
        self._footer = QLabel(
            "💾 Logs are stored for 3 days and saved to log.txt"
            if self._lang == "en" else
            "💾 لاگ‌ها ۳ روز نگهداری می‌شن و در log.txt ذخیره می‌شن"
        )
        self._footer.setObjectName("hintLabel")
        layout.addWidget(self._footer)

    def _load_history(self):
        ops = get_recent_operations(200)
        for op in ops:
            self._append_entry(op["level"], op["message"], op["timestamp"])

    def _append_entry(self, level: str, message: str, timestamp: str = ""):
        # Filter
        if self._filter == "ERROR" and level not in ("ERROR", "WARNING"):
            return
        if self._filter == "INFO" and level not in ("INFO", "SUCCESS"):
            return

        try:
            ts = datetime.datetime.fromisoformat(timestamp).strftime("%H:%M:%S")
        except Exception:
            ts = timestamp[:8] if timestamp else ""

        icon = LEVEL_ICONS.get(level, "·")
        color = LEVEL_COLORS.get(level, "#8BAFC0")
        line = f"[{ts}] {icon} [{level:<7}] {message}"

        cursor = self._log.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)

        fmt = QTextCharFormat()
        fmt.setForeground(QColor(color))
        cursor.setCharFormat(fmt)
        cursor.insertText(line + "\n")

        self._log.setTextCursor(cursor)
        sb = self._log.verticalScrollBar()
        sb.setValue(sb.maximum())
        self._update_stats_label()

    def _on_filter_changed(self, idx: int):
        filters = ["ALL", "ERROR", "INFO"]
        self._filter = filters[idx] if idx < len(filters) else "ALL"
        self._reload_log()

    def _reload_log(self):
        self._log.clear()
        ops = get_recent_operations(200)
        for op in ops:
            self._append_entry(op["level"], op["message"], op["timestamp"])

    def _clear_log(self):
        self._log.clear()

    def _update_stats_label(self):
        ops = get_recent_operations(500)
        errors = sum(1 for o in ops if o["level"] == "ERROR")
        warnings = sum(1 for o in ops if o["level"] == "WARNING")
        if self._lang == "fa":
            self._stats_label.setText(
                f"📊 کل: {len(ops)} | خطا: {errors} | هشدار: {warnings}"
            )
        else:
            self._stats_label.setText(
                f"📊 Total: {len(ops)} | Errors: {errors} | Warnings: {warnings}"
            )

    def _start_live_refresh(self):
        """Refresh every 3 seconds for live updates"""
        self._last_seen_count = 0
        self._refresh_timer = QTimer(self)
        self._refresh_timer.timeout.connect(self._check_new_entries)
        self._refresh_timer.start(3000)

    def _check_new_entries(self):
        ops = get_recent_operations(200)
        if len(ops) != self._last_seen_count:
            new_count = len(ops) - self._last_seen_count
            if new_count > 0 and self._last_seen_count > 0:
                new_ops = ops[-new_count:]
                for op in new_ops:
                    self._append_entry(op["level"], op["message"], op["timestamp"])
            self._last_seen_count = len(ops)

    def set_lang(self, lang: str):
        self._lang = lang
        if self._lang == "fa":
            self._footer.setText("💾 لاگ‌ها ۳ روز نگهداری می‌شن و در log.txt ذخیره می‌شن")
        else:
            self._footer.setText("💾 Logs are stored for 3 days and saved to log.txt")
        self._update_stats_label()
