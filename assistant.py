import json
import os
import datetime
from load_models import load_all_models, generate_code

# Memory file
MEMORY_FILE = "assistant_memory.json"

# Load models
load_all_models()

# Load memory from file
def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {"history": [], "calendar": []}

# Save memory to file
def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)

# Add event to memory
def add_event(memory, event):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    memory["calendar"].append({"event": event, "timestamp": timestamp})
    save_memory(memory)
    print(f"📅 Event saved: {event} at {timestamp}")

# Show calendar events
def show_calendar(memory):
    if not memory["calendar"]:
        print("📭 No events saved.")
    for e in memory["calendar"]:
        print(f"🕒 {e['timestamp']}: {e['event']}")

# Main assistant logic
def main():
    memory = load_memory()
    print("🧠 Thorax Assistant (Dev Mode) - Type 'exit' to quit")

    while True:
        user_input = input("👤 You: ").strip()

        if user_input.lower() == "exit":
            print("👋 Goodbye!")
            break
        elif user_input.startswith("remember "):
            add_event(memory, user_input[9:])
        elif user_input == "calendar":
            show_calendar(memory)
        elif user_input.startswith("code "):
            prompt = user_input[5:]
            results = generate_code(prompt)
            for name, code in results.items():
                print(f"\n⚙️ [{name.upper()} OUTPUT]:\n{code}")
        else:
            # Save history
            memory["history"].append({"input": user_input})
            save_memory(memory)
            print("🤖 I'm still learning to answer general questions (coming soon).")
            print("👉 You can use: 'remember ...', 'calendar', 'code ...', or 'exit'")

if __name__ == "__main__":
    main()
