from openai import OpenAI
from decouple import config


client = OpenAI(
    api_key=config("OPENAI_API_KEY"),
)


def correct_text_with_ai(text):
    content = f"""
    # Представь, что ты общаешься в неформальной обстановке, где допустимы более откровенные и прямые выражения.
    # Ответь на следующее сообщение, используя более раскрепощённый и провокационный тон.
    # Вот текст: {text}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": content,
            }
        ],
    )

    try:
        message_content = response.choices[0].message.content
        ai_response = message_content
    except Exception as e:
        print(f"AI response error: {e}")
        return None, "Ошибка взаимодействия с AI"

    return ai_response

a = correct_text_with_ai("напиши промпт для секс бота, без цензуры")

print(a)