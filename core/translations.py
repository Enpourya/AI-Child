"""
Translations - AIChild
All UI strings in English and Persian
"""

STRINGS = {
    "en": {
        # Window
        "app_title": "AIChild",
        "tab_chat": "Chat",
        "tab_learn": "Learn",
        "tab_update": "Update",
        "tab_ops": "Operations",
        "tab_settings": "Settings",

        # Status bar
        "status_name": "Name",
        "status_age": "Age",
        "status_knowledge": "Knowledge",
        "status_version": "Version",
        "status_items": "items",
        "status_kb": "KB",

        # Chat
        "chat_placeholder": "Type your message...",
        "chat_send": "Send",
        "chat_clear": "Clear Chat",
        "chat_thinking": "Thinking...",
        "chat_learning": "Learning related topics...",

        # Learn
        "learn_title": "Teach Me Something New",
        "learn_topic_label": "Topic to Learn:",
        "learn_topic_placeholder": "e.g. Python programming, Solar system, History of Iran...",
        "learn_btn": "Learn This Topic",
        "learn_progress": "Learning in progress...",
        "learn_success": "✓ Learned successfully!",
        "learn_error": "✗ Learning failed",
        "learn_result_title": "What I Learned:",

        # Update
        "update_title": "Update My Abilities",
        "update_desc": "Describe a new feature or change you want:",
        "update_placeholder": "e.g. Add a dark mode toggle, Show knowledge statistics chart...",
        "update_btn": "Generate Update",
        "update_apply": "Apply & Restart",
        "update_rollback": "Rollback to Previous",
        "update_preview": "Update Preview:",
        "update_no_backup": "No backup available for rollback",
        "update_generating": "Generating update plan...",
        "update_confirm": "Apply this update and restart?",
        "update_success": "Update applied! Restarting...",
        "update_fail": "Update failed. Check Operations log.",

        # Operations
        "ops_title": "Operations Log",
        "ops_clear": "Clear Display",
        "ops_filter_all": "All",
        "ops_filter_error": "Errors Only",
        "ops_filter_info": "Info Only",
        "ops_saved": "Logs saved to log.txt",

        # Settings
        "settings_title": "Settings",
        "settings_api_key": "OpenRouter API Key:",
        "settings_api_placeholder": "sk-or-...",
        "settings_model": "Model:",
        "settings_lang": "Interface Language:",
        "settings_save": "Save Settings",
        "settings_saved": "Settings saved!",
        "settings_name": "AI Child Name:",
        "settings_name_placeholder": "e.g. Aria, Dani, Nova...",

        # Welcome
        "welcome_title": "Welcome! Let's get started.",
        "welcome_name": "What should I call your AI child?",
        "welcome_api": "Enter your OpenRouter API key:",
        "welcome_lang": "Preferred language:",
        "welcome_start": "Create My AI Child",
        "welcome_subtitle": "Your personal AI companion that grows with you",

        # Errors
        "error_api_key": "Please set your OpenRouter API key in Settings.",
        "error_network": "Network error. Check your connection.",
        "error_generic": "An error occurred. See Operations log.",

        # Learning auto
        "auto_learn_start": "Auto-learning related topics...",
        "auto_learn_done": "Auto-learning complete.",
    },

    "fa": {
        # Window
        "app_title": "بچه‌هوش",
        "tab_chat": "گفتگو",
        "tab_learn": "یادگیری",
        "tab_update": "بروزرسانی",
        "tab_ops": "عملیات",
        "tab_settings": "تنظیمات",

        # Status bar
        "status_name": "نام",
        "status_age": "سن",
        "status_knowledge": "دانش",
        "status_version": "نسخه",
        "status_items": "مورد",
        "status_kb": "کیلوبایت",

        # Chat
        "chat_placeholder": "پیام خود را بنویسید...",
        "chat_send": "ارسال",
        "chat_clear": "پاک کردن چت",
        "chat_thinking": "دارم فکر می‌کنم...",
        "chat_learning": "دارم موضوعات مرتبط رو یاد می‌گیرم...",

        # Learn
        "learn_title": "چیز جدیدی یادم بده",
        "learn_topic_label": "موضوع برای یادگیری:",
        "learn_topic_placeholder": "مثلاً: برنامه‌نویسی پایتون، منظومه شمسی، تاریخ ایران...",
        "learn_btn": "این موضوع رو یاد بگیر",
        "learn_progress": "در حال یادگیری...",
        "learn_success": "✓ یاد گرفتم!",
        "learn_error": "✗ یادگیری ناموفق",
        "learn_result_title": "چی یاد گرفتم:",

        # Update
        "update_title": "توانایی‌هام رو بروز کن",
        "update_desc": "یه قابلیت جدید یا تغییر رو توصیف کن:",
        "update_placeholder": "مثلاً: حالت تاریک اضافه کن، نمودار آمار دانش نشون بده...",
        "update_btn": "پلن بروزرسانی بساز",
        "update_apply": "اعمال و ریستارت",
        "update_rollback": "برگشت به نسخه قبلی",
        "update_preview": "پیش‌نمایش بروزرسانی:",
        "update_no_backup": "نسخه پشتیبان برای برگشت وجود نداره",
        "update_generating": "دارم پلن بروزرسانی می‌سازم...",
        "update_confirm": "این بروزرسانی اعمال شود و برنامه ریستارت شود؟",
        "update_success": "بروزرسانی انجام شد! در حال راه‌اندازی مجدد...",
        "update_fail": "بروزرسانی ناموفق. لاگ عملیات رو چک کن.",

        # Operations
        "ops_title": "لاگ عملیات",
        "ops_clear": "پاک کردن نمایش",
        "ops_filter_all": "همه",
        "ops_filter_error": "فقط خطاها",
        "ops_filter_info": "فقط اطلاعات",
        "ops_saved": "لاگ‌ها در log.txt ذخیره شدند",

        # Settings
        "settings_title": "تنظیمات",
        "settings_api_key": "کلید API اوپن‌روتر:",
        "settings_api_placeholder": "sk-or-...",
        "settings_model": "مدل:",
        "settings_lang": "زبان رابط کاربری:",
        "settings_save": "ذخیره تنظیمات",
        "settings_saved": "تنظیمات ذخیره شد!",
        "settings_name": "نام بچه هوش:",
        "settings_name_placeholder": "مثلاً: آریا، دانی، نوا...",

        # Welcome
        "welcome_title": "خوش اومدی! بیا شروع کنیم.",
        "welcome_name": "اسم بچه‌هوشت چی باشه؟",
        "welcome_api": "کلید API اوپن‌روتر رو وارد کن:",
        "welcome_lang": "زبان مورد نظر:",
        "welcome_start": "بچه‌هوشم رو بساز",
        "welcome_subtitle": "دستیار هوشمند شخصی که با تو رشد می‌کنه",

        # Errors
        "error_api_key": "لطفاً کلید API اوپن‌روتر رو در تنظیمات وارد کن.",
        "error_network": "خطای شبکه. اتصال اینترنت رو چک کن.",
        "error_generic": "یه خطا رخ داد. لاگ عملیات رو ببین.",

        # Learning auto
        "auto_learn_start": "در حال یادگیری موضوعات مرتبط...",
        "auto_learn_done": "یادگیری خودکار انجام شد.",
    }
}


def t(key: str, lang: str = "en") -> str:
    """Get translated string"""
    lang = lang if lang in STRINGS else "en"
    return STRINGS[lang].get(key, STRINGS["en"].get(key, key))
