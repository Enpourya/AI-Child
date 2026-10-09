"""
Update Tab - AIChild
AI-powered self-modification with preview and rollback
"""

import sys
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit,
    QPushButton, QFrame, QMessageBox, QSplitter
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont

from core.translations import t
from core.database import get_backup_count, log_operation


class UpdateWorker(QThread):
    plan_ready = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(self, request: str):
        super().__init__()
        self.request = request

    def run(self):
        try:
            from core.ai_engine import generate_update
            plan = generate_update(self.request)
            self.plan_ready.emit(plan)
        except Exception as e:
            self.error.emit(str(e))


class ApplyWorker(QThread):
    success = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, plan: dict):
        super().__init__()
        self.plan = plan

    def run(self):
        try:
            from core.ai_engine import apply_update
            ok = apply_update(self.plan)
            if ok:
                self.success.emit()
            else:
                self.error.emit("Update apply returned False")
        except Exception as e:
            self.error.emit(str(e))


class UpdateTab(QWidget):
    def __init__(self, lang: str):
        super().__init__()
        self._lang = lang
        self._current_plan = None
        self._gen_worker = None
        self._apply_worker = None
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(14)

        # Title
        title = QLabel(t("update_title", self._lang))
        title.setObjectName("sectionTitle")
        title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        layout.addWidget(title)

        hint = QLabel(
            "⚠️  The AI will modify the source code. A backup is created automatically before each update."
            if self._lang == "en" else
            "⚠️  هوش مصنوعی سورس کد رو تغییر می‌ده. قبل از هر بروزرسانی بکاپ خودکار ساخته می‌شه."
        )
        hint.setObjectName("hintLabel")
        hint.setWordWrap(True)
        layout.addWidget(hint)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(sep)

        # Request input
        desc_label = QLabel(t("update_desc", self._lang))
        desc_label.setObjectName("fieldLabel")
        layout.addWidget(desc_label)

        self._request_input = QTextEdit()
        self._request_input.setPlaceholderText(t("update_placeholder", self._lang))
        self._request_input.setFixedHeight(90)

        layout.addWidget(self._request_input)

        # Generate button
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        self._gen_btn = QPushButton(t("update_btn", self._lang))
        self._gen_btn.setObjectName("primaryBtn")
        self._gen_btn.setFixedHeight(40)
        self._gen_btn.setMinimumWidth(200)
        self._gen_btn.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self._gen_btn.clicked.connect(self._generate_update)

        self._rollback_btn = QPushButton(t("update_rollback", self._lang))
        self._rollback_btn.setObjectName("dangerBtn")
        self._rollback_btn.setFixedHeight(40)
        self._rollback_btn.setMinimumWidth(180)
        self._rollback_btn.clicked.connect(self._do_rollback)
        self._rollback_btn.setEnabled(get_backup_count() > 0)

        btn_row.addWidget(self._gen_btn)
        btn_row.addStretch()
        btn_row.addWidget(self._rollback_btn)
        layout.addLayout(btn_row)

        # Status
        self._status_label = QLabel("")
        self._status_label.setObjectName("thinkingLabel")
        layout.addWidget(self._status_label)

        # Preview
        preview_label = QLabel(t("update_preview", self._lang))
        preview_label.setObjectName("fieldLabel")
        layout.addWidget(preview_label)

        self._preview = QTextEdit()
        self._preview.setObjectName("updatePreview")
        self._preview.setReadOnly(True)
        self._preview.setPlaceholderText(
            "The update plan will be shown here before applying..."
            if self._lang == "en" else
            "پلن بروزرسانی قبل از اعمال اینجا نمایش داده می‌شه..."
        )
        layout.addWidget(self._preview, 1)

        # Apply
        self._apply_btn = QPushButton(t("update_apply", self._lang))
        self._apply_btn.setObjectName("successBtn")
        self._apply_btn.setFixedHeight(44)
        self._apply_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self._apply_btn.setEnabled(False)
        self._apply_btn.clicked.connect(self._apply_update)
        layout.addWidget(self._apply_btn)

    def _generate_update(self):
        request = self._request_input.toPlainText().strip()
        if not request or self._gen_worker is not None:
            return

        self._gen_btn.setEnabled(False)
        self._apply_btn.setEnabled(False)
        self._current_plan = None
        self._set_status(t("update_generating", self._lang), "thinking")
        self._preview.clear()

        self._gen_worker = UpdateWorker(request)
        self._gen_worker.plan_ready.connect(self._on_plan_ready)
        self._gen_worker.error.connect(self._on_error)
        self._gen_worker.finished.connect(lambda: setattr(self, "_gen_worker", None) or
                                          self._gen_btn.setEnabled(True))
        self._gen_worker.start()

    def _on_plan_ready(self, plan: dict):
        self._current_plan = plan
        # Format preview
        lines = []
        lines.append(f"📋 DESCRIPTION: {plan.get('description', 'N/A')}")
        lines.append("")
        for i, change in enumerate(plan.get("changes", []), 1):
            lines.append(f"  [{i}] {change.get('action', '?').upper()}: {change.get('file', '?')}")
        if plan.get("notes"):
            lines.append("")
            lines.append(f"📝 NOTES: {plan['notes']}")
        self._preview.setPlainText("\n".join(lines))
        self._apply_btn.setEnabled(True)
        self._set_status("✓ Update plan generated. Review and click Apply.", "success")

    def _on_error(self, error: str):
        self._set_status(f"✗ {error}", "error")
        log_operation("ERROR", f"Update generation failed: {error}")

    def _apply_update(self):
        if not self._current_plan:
            return

        reply = QMessageBox.question(
            self,
            "Apply Update",
            t("update_confirm", self._lang),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        self._apply_btn.setEnabled(False)
        self._gen_btn.setEnabled(False)
        self._set_status("Applying update...", "thinking")

        self._apply_worker = ApplyWorker(self._current_plan)
        self._apply_worker.success.connect(self._on_apply_success)
        self._apply_worker.error.connect(self._on_error)
        self._apply_worker.finished.connect(lambda: setattr(self, "_apply_worker", None))
        self._apply_worker.start()

    def _on_apply_success(self):
        self._set_status(t("update_success", self._lang), "success")
        self._rollback_btn.setEnabled(True)
        # Restart
        QMessageBox.information(self, "Update Applied",
                                "✓ Update applied successfully!\nThe application will now restart.")
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def _do_rollback(self):
        reply = QMessageBox.question(
            self, "Rollback",
            "Are you sure you want to rollback to the previous version?\nThis will restart the application.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        from core.ai_engine import rollback_to_last_backup
        ok = rollback_to_last_backup()
        if ok:
            QMessageBox.information(self, "Rollback", "✓ Rolled back! Restarting...")
            python = sys.executable
            os.execl(python, python, *sys.argv)
        else:
            QMessageBox.warning(self, "Rollback", t("update_no_backup", self._lang))

    def _set_status(self, text: str, kind: str = "thinking"):
        obj_map = {
            "thinking": "thinkingLabel",
            "success": "successLabel",
            "error": "errorLabel"
        }
        self._status_label.setObjectName(obj_map.get(kind, "thinkingLabel"))
        self._status_label.setText(text)
        self._status_label.style().unpolish(self._status_label)
        self._status_label.style().polish(self._status_label)

    def set_lang(self, lang: str):
        self._lang = lang
