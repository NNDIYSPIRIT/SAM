import datetime as dt
import json
import random
import re

# File to persist custom user-taught responses
MEMORY_FILE = "responses.json"


def main():
    print("Bot: Hello! I'm ChatPy Pro. Type 'help' to see what I can do, or 'bye' to exit.")
    responses = load_memory()

    while True:
        try:
            user_input = input("\nYou: ").strip()
            if not user_input:
                continue

            # Exit condition
            if user_input.lower() in ["bye", "exit", "quit"]:
                print("Bot: Goodbye! Happy coding!")
                break

            response = get_response(user_input, responses)
            print(f"Bot: {response}")

        except (KeyboardInterrupt, EOFError):
            print("\nBot: Goodbye! Happy coding!")
            break


def load_memory():
    """Load custom responses from a JSON file using file I/O and exception handling."""
    try:
        with open(MEMORY_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_memory(responses):
    """Save custom responses back to the JSON file."""
    with open(MEMORY_FILE, "w") as file:
        json.dump(responses, file, indent=4)


def teach_bot(user_input, responses):
    """Parse commands to teach the chatbot new responses."""
    # Matches patterns like: teach "key phrase" = "bot response"
    match = re.search(r'^teach\s+"([^"]+)"\s*=\s*"([^"]+)"$', user_input, re.IGNORECASE)
    if match:
        trigger = match.group(1).lower().strip()
        answer = match.group(2).strip()
        responses[trigger] = answer
        save_memory(responses)
        return f"Got it! Now when you say '{trigger}', I'll respond with '{answer}'."
    return "To teach me, use the format: teach \"phrase\" = \"response\""


def get_response(text, responses):
    cleaned_text = text.lower().strip()

    # Check user-defined memory first
    if cleaned_text in responses:
        return responses[cleaned_text]

    # Handle teaching command
    if cleaned_text.startswith("teach"):
        return teach_bot(text, responses)

    # Smart pattern matching using Regular Expressions
    if re.search(r"\b(hi|hello|hey|greetings)\b", cleaned_text):
        greetings = ["Hey there!", "Hello!", "Hi! How can I help you today?"]
        return random.choice(greetings)

    if re.search(r"time|date|day", cleaned_text):
        now = dt.datetime.now()
        return f"Today is {now.strftime('%A, %B %d, %Y')} and the current time is {now.strftime('%I:%M %p')}."

    if re.search(r"how are you", cleaned_text):
        return "I'm running smoothly! How about you?"

    if re.search(r"your name", cleaned_text):
        return "I'm ChatPy Pro, an chatbot."

    if re.search(r"\bhelp\b", cleaned_text):
        return (
            "Here is what I can do:\n"
            "  - Ask me for the 'time' or 'date'\n"
            "  - Ask me to 'calculate' simple math (+, -, *, /)\n"
            "  - Teach me new replies using: teach \"your phrase\" = \"my response\"\n"
            "  - Say 'bye' to exit"
        )

    # Basic Math Evaluator (CS50P Week 6 regex concept)
    math_match = re.search(r"^calculate\s+([\d\s\+\-\*\/\.\(\)]+)$", cleaned_text)
    if math_match:
        try:
            # Safely evaluate simple math expressions
            result = eval(math_match.group(1))
            return f"The result is {result}"
        except Exception:
            return "Sorry, that math expression was invalid."

    # Default fallback
    return "I'm not sure how to answer that yet. You can teach me using: teach \"phrase\" = \"response\""


if __name__ == "__main__":
    main()