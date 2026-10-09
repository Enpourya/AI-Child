# AI-Child
A personal smart assistant that starts from scratch, which you transform into a mature smart assistant.
# AI Child 🤖

**A Self-Learning AI Companion Built with Python and PyQt6**

AI Child is a desktop AI companion designed to learn from its user, remember conversations, build a persistent knowledge base, and evolve over time.

Powered by **OpenRouter**, the application combines online AI conversations, knowledge acquisition, SQLite storage, bilingual support, and AI-assisted source code updates in a modern desktop interface.

The project is designed for Windows and Linux, with a futuristic blue dark theme and an interface that supports both English and Persian.

## ✨ Features

### 🧠 AI Conversation and Learning
- Chat with an AI companion powered by OpenRouter.
- Start with a customizable identity and gradually expand its knowledge.
- Learn new information from user requests.
- Retrieve relevant information from the local knowledge database.
- Combine stored knowledge with online AI reasoning to generate relevant answers.
- Learn in the background when appropriate.
- Preserve conversation history across application sessions.

### 📚 Manual Learning
- Enter a topic that you want the AI to learn.
- Use OpenRouter to process and explain the requested subject.
- Store structured knowledge in SQLite.
- Reuse previously learned information in future conversations.
- Keep learning activity organized and traceable.

### 💾 Persistent SQLite Database
The database layer manages:

- Conversation history.
- Learned knowledge.
- Database backups.
- Operational logs.

Information should be saved promptly and reliably to minimize data loss. Database transactions, error handling, and recovery mechanisms should protect stored information.

### 👤 Personalized AI Identity
Customize the AI companion with a user-defined name and identity.

The main window displays important information, including:

- AI name.
- AI age, calculated from the saved relationship start time.
- Conversation and learning activity.
- Accumulated knowledge statistics.
- A timer that updates the displayed age or elapsed time.

The identity and related statistics must be based on persistent application data.

### 🌐 Bilingual Interface
- English is the default interface language.
- Switch to Persian using the language control.
- Translate all interface text through a centralized translation module.
- Support right-to-left (RTL) layouts for Persian and left-to-right (LTR) layouts for English.
- Save the selected language between sessions.

### 🔄 AI-Assisted Source Code Updates
The Update tab allows users to describe new features or modifications in natural language.

The AI engine can assist with:

1. Understanding the requested feature.
2. Analyzing relevant source code.
3. Preparing proposed code changes.
4. Validating the changes with automated checks.
5. Creating a backup before activation.
6. Applying approved changes and restarting the application when necessary.
7. Rolling back to the previous version if the update is rejected or fails.

**Security requirement:** AI-generated code must be reviewed and validated before execution. Updates should run in an isolated workspace, preserve user data, and require explicit user approval before activation.

### 📊 Operations Monitoring
The Operations tab provides visibility into application activity.

- Color-coded operational logs.
- Error and warning highlighting.
- Filtering by log level or event type.
- Automatic refresh.
- Timestamped database and AI activity.
- API connection and learning status.
- Persistent log storage.
- Automatic removal of records older than three days.

Errors should appear in red, warnings in yellow, and successful operations in green. Sensitive information, including API keys, must never be exposed in logs.

### 🎨 Modern Desktop Interface
- Futuristic blue dark theme.
- Modern tab-based navigation.
- Chat bubbles for conversations.
- Header displaying AI identity and age.
- Live timer.
- Dedicated tabs for chatting, learning, updating, operations, and settings.
- Desktop support for Windows and Linux.

## 🏗️ Project Structure

The application uses a compact, modular architecture.

```text
aichild/
├── main.py               # Application entry point
├── requirements.txt      # PyQt6 dependency
├── core/
│   ├── database.py       # SQLite: conversations, knowledge,
│   │                     # backups, and logs
│   ├── ai_engine.py      # OpenRouter, chat, learning,
│   │                     # and self-updates
│   └── translations.py   # All Persian and English UI text
└── ui/
    ├── main_window.py    # Main window, header, and timer
    ├── chat_tab.py       # Chat bubbles and background learning
    ├── learn_tab.py      # Manual topic learning
    ├── update_tab.py     # AI source updates and rollback
    ├── ops_tab.py        # Colored logs, filters, auto-refresh
    ├── settings_tab.py   # API key, name, and language
    ├── welcome_dialog.py # First-run welcome dialog
    └── styles.py         # Futuristic blue dark theme
```

### Module Responsibilities

| File | Responsibility |
|---|---|
| `main.py` | Initialize and launch the application. |
| `core/database.py` | Manage SQLite data, persistence, backups, and logs. |
| `core/ai_engine.py` | Handle OpenRouter requests, conversations, learning, and update workflows. |
| `core/translations.py` | Centralize English and Persian translations. |
| `ui/main_window.py` | Build the main window, header, navigation, and timer. |
| `ui/chat_tab.py` | Display chat bubbles and coordinate background learning. |
| `ui/learn_tab.py` | Provide manual topic-based learning. |
| `ui/update_tab.py` | Manage proposed code changes, approvals, and rollback. |
| `ui/ops_tab.py` | Display, filter, and refresh operational logs. |
| `ui/settings_tab.py` | Configure the API key, AI name, and language. |
| `ui/welcome_dialog.py` | Collect initial identity information on first launch. |
| `ui/styles.py` | Define the application's visual theme and styling. |

## ⚙️ Requirements

- Python 3.10 or later.
- PyQt6.
- An OpenRouter API key for online AI functionality.
- Windows or Linux.

The only external Python package declared in `requirements.txt` is PyQt6, as specified by the project structure. Other functionality should use Python's standard library unless additional dependencies are deliberately introduced.

## 🚀 Quick Installation

### 1. Extract the ZIP

Extract the project archive and open a terminal in the project directory.

### 2. Install PyQt6

```bash
pip install PyQt6
```

Alternatively, install the declared dependencies:

```bash
pip install -r requirements.txt
```

### 3. Run AI Child

```bash
cd aichild
python main.py
```

On Linux systems where Python 3 is invoked separately, use:

```bash
python3 main.py
```

## 🔑 OpenRouter Configuration

Configure your OpenRouter API key through the application's Settings tab.

The application should store credentials securely and avoid exposing them in source code, database records, or operational logs.

OpenRouter API access may require an active account, a valid API key, and sufficient provider credits or usage allowance.

## 🗃️ Data Persistence and Backups

SQLite is the local storage layer for the application's conversations, learned knowledge, backups, and operational logs.

The database implementation should provide:

- Reliable writes and transaction handling.
- Persistence across application restarts.
- Backup creation before risky operations.
- Recovery from failed updates.
- Efficient retrieval of relevant knowledge.
- Three-day log retention.
- Protection against accidental deletion of user data.

Database backups and source code backups should be managed separately so that a source rollback does not erase conversations or learned knowledge.

## 🛡️ Safe Self-Update Design

AI-assisted code modification is a sensitive operation. The update workflow should:

- Preserve the current working version.
- Generate changes in a separate workspace.
- Validate syntax and run relevant tests.
- Present a change summary to the user.
- Require explicit approval before applying changes.
- Restart only after successful activation.
- Provide a rollback mechanism.
- Preserve the SQLite database and user settings.

The application must not execute untrusted AI-generated code without validation.

## 🧪 Testing Checklist

- [ ] Application launches on Windows and Linux.
- [ ] First-run welcome dialog works correctly.
- [ ] OpenRouter connection and error handling work.
- [ ] Conversations persist after restarting.
- [ ] Learned knowledge is stored and retrieved correctly.
- [ ] Background learning does not freeze the GUI.
- [ ] AI name and age are displayed correctly.
- [ ] English and Persian translations work.
- [ ] Persian layout uses RTL direction.
- [ ] Operational logs display timestamps and severity colors.
- [ ] Log filters and automatic refresh work.
- [ ] Logs older than three days are removed.
- [ ] Database backups can be restored.
- [ ] AI-assisted updates are validated before activation.
- [ ] Rollback restores the previous working source version.

## 🗺️ Roadmap

- [ ] Complete the PyQt6 graphical interface.
- [ ] Integrate OpenRouter into the AI engine.
- [ ] Implement persistent conversation memory.
- [ ] Implement structured knowledge acquisition.
- [ ] Optimize knowledge retrieval.
- [ ] Complete English/Persian localization.
- [ ] Implement live operational monitoring.
- [ ] Add automatic backup and recovery.
- [ ] Implement safe AI-assisted source updates.
- [ ] Test compatibility with Windows and Linux.
- [ ] Prepare distributable application packages.

## 🤝 Contributing

Contributions, bug reports, feature requests, and suggestions are welcome.

Please maintain the existing modular structure and ensure that changes preserve data integrity, application security, and cross-platform compatibility.

## 📄 License

No license has been specified yet. Add an appropriate license file before distributing the project as open-source software.

## 📌 Project Status

AI Child is designed as an evolving AI companion that learns from its user, remembers useful information, and supports controlled improvements to its own source code.

The features described in this README define the intended functionality and should be considered implemented only when verified in the actual codebase.

---

*Start with curiosity. Learn through experience. Remember what matters. Grow with your user.*
