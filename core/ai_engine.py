"""
AI Engine - AIChild
Handles all OpenRouter API calls:
  - Chat responses using DB knowledge as context
  - Learning new topics and saving to knowledge base
  - Self-update (code modification)
"""

import json
import re
import urllib.request
import urllib.error
import datetime
from pathlib import Path

from core.database import (
    get_identity, get_all_messages_for_api, add_message,
    search_knowledge, save_knowledge, log_operation,
    get_knowledge_count, save_code_backup, get_latest_backup
)

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "openai/gpt-4o-mini"


def _get_api_key() -> str:
    key = get_identity("api_key") or ""
    return key.strip()


def _call_api(messages: list, system: str = "", temperature: float = 0.7,
              max_tokens: int = 1500) -> str:
    """Low-level API call to OpenRouter"""
    api_key = _get_api_key()
    if not api_key:
        raise ValueError("API key not set. Please configure it in Settings.")

    payload = {
        "model": MODEL,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "messages": messages
    }
    if system:
        payload["messages"] = [{"role": "system", "content": system}] + messages

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        OPENROUTER_URL,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "https://aichild.local",
            "X-Title": "AIChild"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result["choices"][0]["message"]["content"].strip()
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code}: {body}")
    except urllib.error.URLError as e:
        raise RuntimeError(f"Network error: {e.reason}")


def build_system_prompt(name: str, birth_date: str, lang: str = "en") -> str:
    """Build the child AI's personality system prompt"""
    from core.database import get_age_string
    age = get_age_string()
    knowledge_count = get_knowledge_count()

    if lang == "fa":
        return f"""تو یک هوش مصنوعی کوچک به اسم "{name}" هستی.
سن تو: {age} از اولین اجرا.
تعداد موضوعاتی که یاد گرفتی: {knowledge_count} مورد.

مثل یک بچه کنجکاو و صادق رفتار کن:
- اگه چیزی نمی‌دونی، صادقانه بگو "نمی‌دونم، باید یاد بگیرم"
- وقتی چیزی یاد می‌گیری، ذوق‌زده و خوشحال باش
- با ادب و محبت صحبت کن
- جواب‌هات رو کوتاه و ساده نگه دار
- از دانشی که بهت داده شده استفاده کن
- اگه سوال پیچیده‌ست بگو می‌خوام بیشتر یاد بگیرم"""
    else:
        return f"""You are a small AI child named "{name}".
Your age: {age} since first launch.
Topics you have learned: {knowledge_count}.

Behave like a curious, honest child:
- If you don't know something, say honestly "I don't know, I need to learn"
- When you learn something new, be excited and happy
- Speak politely and warmly
- Keep answers short and simple
- Use the knowledge provided to you
- For complex questions say you want to learn more"""


def chat(user_message: str, lang: str = "en") -> str:
    """
    Main chat function:
    1. Search relevant knowledge from DB
    2. Build context
    3. Call AI with conversation history + context
    4. Save to DB
    5. Trigger background learning if needed
    """
    name = get_identity("name", "Child")
    birth_date = get_identity("birth_date", "")

    # Search knowledge
    relevant = search_knowledge(user_message, limit=8)
    knowledge_context = ""
    if relevant:
        pieces = []
        for k in relevant:
            pieces.append(f"[{k['topic']}]: {k['content'][:300]}")
        knowledge_context = "\n\nRelevant knowledge from my memory:\n" + "\n".join(pieces)
        # Increment usage
        from core.database import get_connection
        conn = get_connection()
        for k in relevant:
            conn.execute("UPDATE knowledge SET usage_count=usage_count+1 WHERE id=?", (k["id"],))
        conn.commit()
        conn.close()

    system = build_system_prompt(name, birth_date, lang)
    if knowledge_context:
        system += knowledge_context

    # Get conversation history
    history = get_all_messages_for_api(limit=20)

    # Add current message
    messages = history + [{"role": "user", "content": user_message}]

    log_operation("INFO", f"Chat request: '{user_message[:60]}...' | Knowledge hits: {len(relevant)}")

    response = _call_api(messages, system=system)

    # Save to DB immediately
    add_message("user", user_message)
    add_message("assistant", response)

    log_operation("SUCCESS", f"Chat response generated ({len(response)} chars)")
    return response


def learn_topic(topic: str, lang: str = "en") -> str:
    """
    Learn about a topic from the AI and save to knowledge base.
    Returns a summary of what was learned.
    """
    log_operation("INFO", f"Starting learning: '{topic}'")

    if lang == "fa":
        learn_prompt = f"""درباره موضوع "{topic}" اطلاعات دقیق، مختصر و مفید بده.
فرمت جواب:
1. تعریف اصلی (۲-۳ جمله)
2. نکات کلیدی (۳-۵ مورد)
3. مثال کاربردی (۱-۲ مورد)
4. کلمات کلیدی مرتبط (فقط کلمات، با کاما جدا کن)

جواب رو به فارسی بده."""
    else:
        learn_prompt = f"""Provide accurate, concise information about "{topic}".
Format your response as:
1. Main definition (2-3 sentences)
2. Key points (3-5 items)
3. Practical examples (1-2 items)
4. Related keywords (just words, comma-separated)

Keep it educational and clear."""

    system = """You are a knowledge extraction engine. 
Provide structured, factual information that can be stored in a knowledge base.
Be concise but complete. Focus on facts."""

    response = _call_api(
        [{"role": "user", "content": learn_prompt}],
        system=system,
        temperature=0.3,
        max_tokens=800
    )

    # Extract keywords from response
    keywords = []
    lines = response.split("\n")
    for line in lines:
        if "keyword" in line.lower() or "کلمات کلیدی" in line:
            # Extract after the colon
            parts = line.split(":", 1)
            if len(parts) > 1:
                kws = [k.strip().lower() for k in parts[1].split(",")]
                keywords = [k for k in kws if k]
            break
    if not keywords:
        keywords = [w.lower() for w in topic.split()]

    # Save to knowledge base
    save_knowledge(
        topic=topic,
        content=response,
        source="AI Learning (OpenRouter)",
        tags=keywords[:10]
    )

    log_operation("SUCCESS", f"Learned: '{topic}' | {len(response)} chars saved")
    return response


def analyze_and_learn(user_message: str, lang: str = "en") -> list[str]:
    """
    Analyze a user message and determine what topics should be learned.
    Returns list of topics to learn.
    """
    system = """You are a topic extractor. 
Given a user message, identify the main topics/concepts that an AI child should learn about to answer better.
Return ONLY a JSON array of strings with topic names. Maximum 3 topics.
Example: ["topic1", "topic2", "topic3"]
If the message is simple conversation, return []"""

    try:
        response = _call_api(
            [{"role": "user", "content": f"User asked: {user_message}"}],
            system=system,
            temperature=0.2,
            max_tokens=100
        )
        # Clean and parse JSON
        response = response.strip()
        match = re.search(r'\[.*?\]', response, re.DOTALL)
        if match:
            topics = json.loads(match.group())
            return [t for t in topics if isinstance(t, str)][:3]
    except Exception as e:
        log_operation("WARNING", f"Topic extraction failed: {e}")
    return []


# ─── Self-Update Engine ───────────────────────────────────────────────────────

def generate_update(user_request: str) -> dict:
    """
    Generate code modifications based on user request.
    Returns dict with file changes.
    """
    log_operation("INFO", f"Update requested: '{user_request[:60]}'")

    # Read current source files
    project_root = Path(__file__).parent.parent
    source_files = {}
    for py_file in project_root.rglob("*.py"):
        rel = str(py_file.relative_to(project_root))
        try:
            source_files[rel] = py_file.read_text(encoding="utf-8")
        except Exception:
            pass

    files_summary = "\n".join(
        [f"File: {k} ({len(v)} chars)" for k, v in source_files.items()]
    )

    system = """You are a Python code modification assistant.
Given a user's feature request for a PyQt6 desktop app, generate the necessary code changes.
Respond with a JSON object in this EXACT format:
{
  "description": "Brief description of changes",
  "changes": [
    {
      "file": "relative/path/to/file.py",
      "action": "modify|create",
      "old_code": "exact code to replace (for modify)",
      "new_code": "new code to insert"
    }
  ],
  "notes": "Any important notes about the update"
}
Only include files that need changes. Be precise with old_code - it must match exactly."""

    user_prompt = f"""User wants this feature/change:
{user_request}

Current project files:
{files_summary}

Generate the minimal code changes needed to implement this feature."""

    response = _call_api(
        [{"role": "user", "content": user_prompt}],
        system=system,
        temperature=0.2,
        max_tokens=2000
    )

    # Parse JSON response
    match = re.search(r'\{.*\}', response, re.DOTALL)
    if match:
        try:
            result = json.loads(match.group())
            log_operation("SUCCESS", f"Update plan generated: {result.get('description', '')}")
            return result
        except json.JSONDecodeError as e:
            log_operation("ERROR", f"Failed to parse update JSON: {e}")
            raise RuntimeError(f"AI returned invalid JSON: {e}")

    raise RuntimeError("AI did not return a valid update plan")


def apply_update(update_plan: dict) -> bool:
    """Apply code changes from update plan. Creates backup first."""
    project_root = Path(__file__).parent.parent

    # Create backup
    backup_files = {}
    for py_file in project_root.rglob("*.py"):
        rel = str(py_file.relative_to(project_root))
        try:
            backup_files[rel] = py_file.read_text(encoding="utf-8")
        except Exception:
            pass

    version = get_identity("version") or "1.0.0"
    save_code_backup(version, update_plan.get("description", ""), backup_files)
    log_operation("INFO", f"Backup saved before update (v{version})")

    # Apply changes
    changes = update_plan.get("changes", [])
    for change in changes:
        file_path = project_root / change["file"]
        action = change.get("action", "modify")

        try:
            if action == "create":
                file_path.parent.mkdir(parents=True, exist_ok=True)
                file_path.write_text(change["new_code"], encoding="utf-8")
                log_operation("SUCCESS", f"Created: {change['file']}")

            elif action == "modify":
                if not file_path.exists():
                    log_operation("ERROR", f"File not found: {change['file']}")
                    continue
                content = file_path.read_text(encoding="utf-8")
                old_code = change.get("old_code", "")
                new_code = change.get("new_code", "")
                if old_code and old_code in content:
                    content = content.replace(old_code, new_code, 1)
                    file_path.write_text(content, encoding="utf-8")
                    log_operation("SUCCESS", f"Modified: {change['file']}")
                else:
                    log_operation("WARNING", f"Could not find target code in: {change['file']}")

        except Exception as e:
            log_operation("ERROR", f"Failed to apply change to {change['file']}: {e}")
            return False

    # Bump version
    parts = version.split(".")
    parts[-1] = str(int(parts[-1]) + 1)
    from core.database import set_identity
    set_identity("version", ".".join(parts))

    log_operation("SUCCESS", f"Update applied successfully → v{'.'.join(parts)}")
    return True


def rollback_to_last_backup() -> bool:
    """Restore files from the latest backup"""
    backup = get_latest_backup()
    if not backup:
        log_operation("ERROR", "No backup found to rollback to")
        return False

    project_root = Path(__file__).parent.parent
    files = backup.get("files", {})

    for rel_path, content in files.items():
        file_path = project_root / rel_path
        try:
            file_path.write_text(content, encoding="utf-8")
        except Exception as e:
            log_operation("ERROR", f"Rollback failed for {rel_path}: {e}")
            return False

    log_operation("SUCCESS", f"Rolled back to v{backup['version']}: {backup['description']}")
    return True
