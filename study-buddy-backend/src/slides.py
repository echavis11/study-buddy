from openai import AsyncOpenAI

client = AsyncOpenAI()
MODEL = "gpt-4o-mini"

async def slide_generation(text: str, n: int) -> str:
    """
    Generate n flashcards from the given text using OpenAI.
    Returns JSON string with flashcards.
    """
    prompt = (
        f"Generate {n} flashcards utilizing the content provided. "
        f"Each flashcard should have a 1-sentence question with an answer. "
        f"The flashcards should cover the breadth of the entirety of the content. "
        f"The content is: {text}. "
        f"The response should be a JSON array of objects in the form: "
        f'{{"q": "...", "a": "..."}} for each flashcard.'
    )

    response = await client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content