import requests

class LLMService:
    def __init__(self, model: str = "llama3.1"):
        self.model = model
        self.base_url = "http://localhost:11434/api/generate"

    def generate_answer(self, question: str, context: list[str]) -> str:
        context_text = "\n\n".join(context)

        prompt = f"""
            You are a helpful assistant.

            Use ONLY the context below to answer.

            Context:
            {context_text}

            Question:
            {question}

            If the answer is not in context, say "I don't know".
        """

        response = requests.post(
            self.base_url,
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
        )

        print(response.status_code)
        print(response.text)

        return response.json()["response"]