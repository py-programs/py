import requests

API_KEY = "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"

url = "https://openrouter.ai/api/v1/chat/completions"

while True:
    question = input("\nYou: ")

    if question.lower() == "exit":
        print("Goodbye!")
        break

    response = requests.post(
        url,
        headers={
            "Authorization": "Bearer " + API_KEY,
            "Content-Type": "application/json"
        },
        json={
            "model": "openrouter/free",
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        }
    )

    if response.status_code == 200:
        data = response.json()
        answer = data["choices"][0]["message"]["content"]
        print("\nAI:", answer)
    else:
        print("\nError:", response.status_code)
        print(response.text)
