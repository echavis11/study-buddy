from openai import OpenAI

client = OpenAI()
model = "gpt-4o-mini"

async def slide_generation(text: str, n: int) -> str:

    size = str(n)
    input = "Generate {size} flashcards utilizing the content provided." \
        "Each flashcard should have a 1 sentence question with an answer." \
        "The flashcards should cover the breadth of the entirety of the content. " \
        "The content is {text}. " \
        "The response should be a json of the form:" \
        "{" \
        "   q:" \
        "   a:" \
        "} For each flash card."
    response = await client.responses.create(
        model= {model},
        input= [ 
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": input}
                ],
            }
        ],
    )

    return response