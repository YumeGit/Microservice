import openai

# Укажи свой API ключ
openai.api_key = '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'

def generate_text(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",  # или другой движок, например 'gpt-4'
        prompt=prompt,
        max_tokens=150,  # Максимальное количество токенов в ответе
        n=1,  # Количество ответов
        stop=None,  # Можешь указать стоп-слова для остановки генерации
        temperature=0.7  # Температура управления креативностью
    )
    
    # Получаем текст из ответа
    return response['choices'][0]['text'].strip()

# Пример вызова функции
result = generate_text("Привет! Расскажи мне про Python.")
print(result)
