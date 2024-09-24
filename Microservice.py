from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# Укажи свой API ключ OpenAI
openai.api_key = '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'

# Функция для генерации отчета с помощью ChatGPT
def generate_report(questions, answers, expected_answers):
    prompt = f"""
    Вопросы: {questions}
    Ответы: {answers}
    Ожидаемые ответы: {expected_answers}
    
    На основе этих данных, составь отчёт о текущем состоянии компании и дай рекомендации.
    """
    try:
        # Запрос к OpenAI API
        response = openai.Completion.create(
            engine="gpt-4",  # или 'text-davinci-003'
            prompt=prompt,
            max_tokens=500,
            temperature=0.7
        )
        return response['choices'][0]['text'].strip(), 200
    except Exception as e:
        return str(e), 500

# Endpoint для получения данных и генерации отчета
@app.route('/generate_report', methods=['POST'])
def generate_report_endpoint():
    # Проверяем, что запрос содержит данные в формате JSON
    if not request.is_json:
        return jsonify({"error": "Данные должны быть в формате JSON"}), 422

    data = request.get_json()

    # Проверяем наличие всех необходимых параметров
    if 'questions' not in data or 'answers' not in data or 'expected_answers' not in data:
        return jsonify({"error": "Отсутствуют обязательные параметры: 'questions', 'answers', 'expected_answers'"}), 422

    # Проверяем, что параметры переданы в виде списков
    if not isinstance(data['questions'], list) or not isinstance(data['answers'], list) or not isinstance(data['expected_answers'], list):
        return jsonify({"error": "Параметры 'questions', 'answers' и 'expected_answers' должны быть списками"}), 422

    # Генерируем отчёт с помощью ChatGPT
    report, status_code = generate_report(data['questions'], data['answers'], data['expected_answers'])

    # Если отчёт успешно сгенерирован, возвращаем его с кодом 200
    if status_code == 200:
        return jsonify({"report": report}), 200
    else:
        # Если произошла ошибка на стороне ChatGPT, возвращаем код 500
        return jsonify({"error": "Ошибка при генерации отчёта: " + report}), 500

# Запуск сервера
if __name__ == '__main__':
    app.run(host='127.0.0.1 ', port=5436)
