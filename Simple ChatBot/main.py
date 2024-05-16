import json
from difflib import get_close_matches
from typing import List, Optional, Dict, Any

def load_knowledge_base(file_path: str) -> Dict[str, Any]:
    try:
        with open(file_path, 'r') as file:
            data: Dict[str, Any] = json.load(file)
        return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading knowledge base: {e}")
        return {"questions": []}

def save_knowledge_base(file_path: str, data: Dict[str, Any]):
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=2)
    except IOError as e:
        print(f"Error saving knowledge base: {e}")

def find_best_match(user_question: str, questions: List[str]) -> Optional[str]:
    exact_match = next((q for q in questions if q.lower() == user_question.lower()), None)
    if exact_match:
        return exact_match
    matches = get_close_matches(user_question, questions, n=1, cutoff=0.8)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: Dict[str, Any]) -> Optional[str]:
    for q in knowledge_base["questions"]:
        if q["question"].lower() == question.lower():
            return q["answer"]
    return None

def chat_bot():
    knowledge_base: Dict[str, Any] = load_knowledge_base('knowledge_base.json')

    while True:
        user_input: str = input('User: ').strip()

        if user_input.lower() == 'quit':
            print('Bot: Goodbye!')
            break

        best_match: Optional[str] = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

        if best_match:
            answer: Optional[str] = get_answer_for_question(best_match, knowledge_base)
            print(f'Bot: {answer}')
        else:
            print('Bot: Sorry, I don\'t know the answer. Can you teach me?')
            new_answer: str = input('Type the answer or "skip" to skip: ').strip()

            if new_answer.lower() != 'skip':
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base('knowledge_base.json', knowledge_base)
                print('Bot: Thank you! I learned a new response.')

if __name__ == '__main__':
    chat_bot()

