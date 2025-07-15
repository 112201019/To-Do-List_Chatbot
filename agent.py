import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import StructuredTool
from langchain.memory import ConversationBufferMemory
from langchain import hub

# --- Initialize LLM ---
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key="AIzaSyBlMM4x2iIvVAh_j_4fw9Rzwdi2BX8NhUA"
)

# --- Load or initialize todo list ---
TODO_FILE = "todos.json"
try:
    with open(TODO_FILE, "r") as f:
        todo_list = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    todo_list = []

# --- Define tools ---
def add_todo(item: str) -> str:
    """Add an item to the to-do list, avoiding duplicates."""
    item = item.strip()
    if any(existing.lower() == item.lower() for existing in todo_list):
        return f"'{item}' is already on your to-do list."
    todo_list.append(item)
    with open(TODO_FILE, "w") as f:
        json.dump(todo_list, f)
    return f"Added '{item}' to your to-do list."

def remove_todo(item: str) -> str:
    """Remove an item from the to-do list."""
    item = item.strip()
    if item in todo_list:
        todo_list.remove(item)
        with open(TODO_FILE, "w") as f:
            json.dump(todo_list, f)
        return f"Removed '{item}' from your to-do list."
    else:
        return f"'{item}' was not found in your to-do list."

def list_todos() -> str:
    """List all items in the to-do list."""
    if not todo_list:
        return "Your to-do list is empty."
    items = "\n".join(f"{i+1}. {item}" for i, item in enumerate(todo_list))
    return f"Here's your current to-do list:\n{items}"

# --- Wrap functions as tools ---
tools = [
    StructuredTool.from_function(add_todo),
    StructuredTool.from_function(remove_todo),
    StructuredTool.from_function(list_todos)
]

# --- Memory & Prompt ---
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
prompt = hub.pull("hwchase17/react")

# --- Build the ReAct agent & executor ---
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=False,
    handle_parsing_errors=True
)

# If you want a CLI fallback when running directly:
if __name__ == "__main__":
    print("Welcome to SnelloBot CLI! Type 'exit' to quit.\n")
    while True:
        user_input = input("You: ")
        if user_input.strip().lower() == "exit":
            break
        try:
            resp = agent_executor.invoke({"input": user_input})
            print("Agent:", resp["output"])
        except Exception as e:
            print("Error:", e)
            print("Please try again.")
