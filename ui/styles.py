"""
Styles - AIChild
Dark futuristic theme for PyQt6
"""

DARK_STYLE = """
/* ─── Global ─────────────────────────────── */
* {
    font-family: "Segoe UI", "Tahoma", "Arial", sans-serif;
    color: #E0E6F0;
    selection-background-color: #3A7BF7;
}

QMainWindow, QDialog {
    background-color: #0D1117;
}

QWidget {
    background-color: #0D1117;
}

/* ─── Header ─────────────────────────────── */
#header {
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #161B22,
        stop:0.5 #1A2236,
        stop:1 #161B22
    );
    border-bottom: 1px solid #2A3548;
}

#childName {
    color: #58A6FF;
    font-size: 18px;
    font-weight: bold;
    letter-spacing: 1px;
}

#childSubtitle {
    color: #7A8FA6;
    font-size: 9px;
}

#statsLabel {
    color: #4CAF82;
    font-size: 9px;
}

/* ─── Language Buttons ───────────────────── */
#langBtn {
    background-color: #1E2A3A;
    border: 1px solid #2A3548;
    border-radius: 4px;
    color: #7A8FA6;
    font-size: 8px;
    font-weight: bold;
    padding: 0px;
}

#langBtn:hover {
    background-color: #2A3A52;
    color: #A0B4CC;
}

#langBtn[active="true"] {
    background-color: #1D3557;
    border-color: #3A7BF7;
    color: #3A7BF7;
}

/* ─── Tab Widget ─────────────────────────── */
#mainTabs {
    background-color: #0D1117;
}

QTabWidget::pane {
    border: none;
    background-color: #0D1117;
}

QTabBar::tab {
    background-color: #161B22;
    color: #7A8FA6;
    padding: 10px 22px;
    border: none;
    border-bottom: 2px solid transparent;
    font-size: 10px;
    font-weight: 500;
    letter-spacing: 0.5px;
}

QTabBar::tab:hover {
    background-color: #1E2A3A;
    color: #C0D0E0;
}

QTabBar::tab:selected {
    background-color: #161B22;
    color: #58A6FF;
    border-bottom: 2px solid #3A7BF7;
}

/* ─── Scroll Areas ───────────────────────── */
QScrollArea {
    border: none;
    background-color: transparent;
}

QScrollBar:vertical {
    background-color: #161B22;
    width: 8px;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background-color: #2A3A52;
    border-radius: 4px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #3A7BF7;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    background-color: #161B22;
    height: 8px;
    border-radius: 4px;
}

QScrollBar::handle:horizontal {
    background-color: #2A3A52;
    border-radius: 4px;
}

/* ─── Chat Bubbles ───────────────────────── */
#chatArea {
    background-color: #0D1117;
    border: none;
}

#userBubble {
    background-color: #1D3557;
    border-radius: 14px;
    border-bottom-right-radius: 4px;
    padding: 10px 14px;
    color: #E0E6F0;
    font-size: 10px;
}

#aiBubble {
    background-color: #161B22;
    border: 1px solid #2A3548;
    border-radius: 14px;
    border-bottom-left-radius: 4px;
    padding: 10px 14px;
    color: #C0D0E0;
    font-size: 10px;
}

#systemBubble {
    background-color: #1A2236;
    border: 1px solid #2A3A52;
    border-radius: 8px;
    padding: 6px 12px;
    color: #4CAF82;
    font-size: 9px;
}

/* ─── Input Area ─────────────────────────── */
#chatInput {
    background-color: #161B22;
    border: 1px solid #2A3548;
    border-radius: 10px;
    padding: 10px 14px;
    color: #E0E6F0;
    font-size: 10px;
    min-height: 40px;
}

#chatInput:focus {
    border-color: #3A7BF7;
    background-color: #1A2236;
}

/* ─── Primary Buttons ────────────────────── */
#primaryBtn {
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #1A6CF7, stop:1 #3A7BF7
    );
    border: none;
    border-radius: 8px;
    color: #FFFFFF;
    font-size: 10px;
    font-weight: 600;
    padding: 10px 20px;
    letter-spacing: 0.5px;
}

#primaryBtn:hover {
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #2A7CF7, stop:1 #4A8BFF
    );
}

#primaryBtn:pressed {
    background-color: #1055CC;
}

#primaryBtn:disabled {
    background-color: #2A3548;
    color: #4A5A6A;
}

/* ─── Secondary / Danger Buttons ─────────── */
#secondaryBtn {
    background-color: #1E2A3A;
    border: 1px solid #2A3A52;
    border-radius: 8px;
    color: #A0B4CC;
    font-size: 10px;
    padding: 8px 16px;
}

#secondaryBtn:hover {
    background-color: #2A3A52;
    color: #E0E6F0;
}

#dangerBtn {
    background-color: #2A1A1A;
    border: 1px solid #5A2A2A;
    border-radius: 8px;
    color: #F07070;
    font-size: 10px;
    padding: 8px 16px;
}

#dangerBtn:hover {
    background-color: #3A2020;
    color: #FF9090;
}

#successBtn {
    background-color: #1A2E1A;
    border: 1px solid #2A5A2A;
    border-radius: 8px;
    color: #4CAF82;
    font-size: 10px;
    padding: 8px 16px;
}

#successBtn:hover {
    background-color: #203820;
    color: #6CDF9A;
}

/* ─── Text Inputs ────────────────────────── */
QLineEdit, QTextEdit, QPlainTextEdit {
    background-color: #161B22;
    border: 1px solid #2A3548;
    border-radius: 6px;
    padding: 8px 12px;
    color: #E0E6F0;
    font-size: 10px;
    selection-background-color: #3A7BF7;
}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
    border-color: #3A7BF7;
    background-color: #1A2236;
}

QLineEdit[echoMode="2"] {
    letter-spacing: 4px;
}

/* ─── Labels ─────────────────────────────── */
QLabel {
    color: #C0D0E0;
    background-color: transparent;
}

#sectionTitle {
    color: #58A6FF;
    font-size: 13px;
    font-weight: bold;
    padding-bottom: 4px;
}

#fieldLabel {
    color: #7A8FA6;
    font-size: 9px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

#hintLabel {
    color: #4A5A6A;
    font-size: 8px;
    font-style: italic;
}

/* ─── Operations Log ─────────────────────── */
#opsLog {
    background-color: #0A0F16;
    border: 1px solid #1A2236;
    border-radius: 6px;
    font-family: "Cascadia Code", "Consolas", "Courier New", monospace;
    font-size: 9px;
    color: #8BAFC0;
}

/* ─── Knowledge / Learn area ─────────────── */
#learnResult {
    background-color: #0F1620;
    border: 1px solid #1D3045;
    border-radius: 8px;
    padding: 12px;
    color: #C0D8E0;
    font-size: 10px;
    line-height: 1.6;
}

/* ─── Update Panel ───────────────────────── */
#updatePreview {
    background-color: #0A1520;
    border: 1px solid #1A3050;
    border-radius: 8px;
    padding: 12px;
    color: #A0C8E0;
    font-size: 9px;
    font-family: "Cascadia Code", "Consolas", monospace;
}

/* ─── Separators ─────────────────────────── */
QFrame[frameShape="4"], QFrame[frameShape="5"] {
    color: #1E2A3A;
    background-color: #1E2A3A;
    border: none;
    max-height: 1px;
}

/* ─── Combo Box ──────────────────────────── */
QComboBox {
    background-color: #161B22;
    border: 1px solid #2A3548;
    border-radius: 6px;
    padding: 6px 10px;
    color: #E0E6F0;
    font-size: 10px;
}

QComboBox::drop-down {
    border: none;
    width: 20px;
}

QComboBox QAbstractItemView {
    background-color: #1A2236;
    border: 1px solid #2A3548;
    selection-background-color: #3A7BF7;
    color: #E0E6F0;
}

/* ─── Status Bar ─────────────────────────── */
#mainStatusBar {
    background-color: #161B22;
    border-top: 1px solid #1E2A3A;
    color: #4A5A6A;
    font-size: 8px;
}

/* ─── Progress / Thinking animation ─────── */
#thinkingLabel {
    color: #3A7BF7;
    font-size: 10px;
    font-style: italic;
}

#errorLabel {
    color: #F07070;
    font-size: 9px;
}

#successLabel {
    color: #4CAF82;
    font-size: 9px;
}

/* ─── Welcome Dialog ─────────────────────── */
#welcomeDialog {
    background-color: #0D1117;
}

#welcomeTitle {
    color: #58A6FF;
    font-size: 22px;
    font-weight: bold;
}

#welcomeSubtitle {
    color: #4A5A6A;
    font-size: 11px;
}
"""
