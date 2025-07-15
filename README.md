# SnelloBot: Your Personal To-Do List Assistant

SnelloBot is an AI-powered conversational chatbot that helps you manage your to-do list using natural language. It uses **LangChain**, Google's **Gemini** model, and a simple Flask web frontend. You can run it as:

- A command-line chatbot (`agent.py`)
- A web-based chat app (`app.py` + `index.html`)

---

## **Project Architecture**

**Flow Overview:**
```
User Input → Flask (app.py) → LangChain Agent → Gemini LLM
    ↓                                              ↑
Tools: add, remove, list to-dos → JSON file storage
```

**Step-by-step process:**

1️The **frontend** (web browser or terminal) takes your natural text:
> "Add 'Buy groceries' to my list."

2️ The **LangChain Agent** checks if the input matches any registered **tool**:
- `add_todo`
- `remove_todo`
- `list_todos`

3️ If yes, the tool runs and updates your `todos.json` file.

4️ The LLM replies with the result (or a fallback chat if no tool matches).

---

## **How Memory Works**

SnelloBot uses `ConversationBufferMemory` from LangChain. This means:

- It remembers the full chat history for the **current session only** (in RAM).
- The **to-do list itself** is stored persistently in `todos.json`.
- Each new question or command considers the whole conversation context.

---

## **How Tools Work**

- Each function (`add_todo`, `remove_todo`, `list_todos`) is defined in **Python** with a clear docstring.
- These functions are wrapped using `StructuredTool.from_function()`.
- They are registered with the Agent:

```python
tools = [
    StructuredTool.from_function(add_todo),
    StructuredTool.from_function(remove_todo),
    StructuredTool.from_function(list_todos)
]
```

LangChain's ReAct Agent decides whether to use a tool or just reply naturally.

---

## How to Run

### 1️⃣ Local Setup

**Clone this repo:**
```bash
git clone <YOUR_REPO_URL>
cd <YOUR_PROJECT_DIR>
```
For this initial version, I hardcoded the API key directly into the script because the main goal was to get the core functionality working — natural language handling, tool execution, memory, and a working web UI. I’m aware that best practice is to store secrets in a .env file and load them securely with os.environ or python-dotenv. If time allows, I plan to refactor it to use proper environment variable management and add .gitignore to avoid committing secrets. For now, I prioritized demonstrating the working integration over production-grade security.

**Install dependencies:**
```bash
pip install -r requirements.txt
```

### 2️⃣ Run as a CLI Bot

```bash
python3 agent.py
```

You'll see:
```
Welcome to SnelloBot! Type 'exit' to quit.
```

**Example:**
```
You: Add making sandwich to my to-do list
Agent: Added 'making sandwich' to your to-do list.
```

### 3️⃣ Run as a Web App

```bash
python3 app.py
```

Visit `http://localhost:5000`

Type messages in the chat box.

**Example prompts:**
- "Add making a sandwich to my list"
- "Remove making a sandwich"
- "What's on my to-do list?"
- "Hi SnelloBot!"

---

## Requirements

Your `requirements.txt` includes:

```
Flask
langchain
langchain-google-genai
```

---

## Known Limitations

- **Free API quota**: Using Gemini's free tier may exhaust your daily quota → you'll see 429 errors if this happens.
- **Session-only memory**: The memory forgets when you restart.
- **Single user**: No multi-user accounts yet.
- **Simple text-based list**: No dates, priorities, or reminders.

---

## Future Improvements

- Add user authentication (multi-user to-do lists)
- Add due dates, priorities, and categories
- Deploy securely to Render, Railway, or Vercel
- Use `.env` and `.gitignore` for safe key management
- Add a database (SQLite/PostgreSQL) instead of JSON files
- Improve the UI with modern frameworks (React, Vue)

---
## By Sriram Nangunoori Owner of this Repo and the code. 
This project uses Google Gemini via the Google Generative AI API.

The model is owned and operated by Google.

This project does not include or redistribute Google’s proprietary LLM — it only calls the model via a public API.

To use SnelloBot, I provided My own valid Google API key and comply with Google’s terms of service for Gemini and Generative AI.

I claim no ownership over the Gemini model or any part of Google’s infrastructure.

This project is for educational/demo purposes only. (For submission).
