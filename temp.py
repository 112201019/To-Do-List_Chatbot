import google.generativeai as genai

genai.configure(api_key="AIzaSyBlMM4x2iIvVAh_j_4fw9Rzwdi2BX8NhUA")

model = genai.GenerativeModel("gemini-2.0-flash")

print("Welcome to SnelloBot! Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break

    response = model.generate_content(user_input)
    print("Gemini:", response.text)
