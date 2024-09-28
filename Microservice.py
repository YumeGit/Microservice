import os
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# Укажи свой API ключ OpenAI
client = OpenAI(
api_key='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',
)
# Функция для генерации отчета с помощью ChatGPT
def generate_report(questions, answers, expected_answers):
    prompt = f"""
    Вопросы: {questions}
    Ответы: {answers}
    Ожидаемые ответы: {expected_answers}
    
    На основе этих данных, составь отчёт о текущем состоянии компании и дай рекомендации.
    """
    
   # return """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus sed justo leo. Proin at volutpat augue. Aliquam hendrerit, massa a fermentum lobortis, orci dui venenatis ante, eget facilisis magna tellus sit amet lacus. Aenean mi felis, consequat vel volutpat non, laoreet congue dolor. Praesent mattis vel leo nec feugiat. Nulla sem odio, scelerisque vel arcu eget, molestie posuere neque. Proin efficitur bibendum odio. Fusce sapien neque, accumsan vitae mauris a, aliquam gravida purus. Sed quis massa porttitor erat euismod accumsan. Proin et aliquet nisi.

#Integer lorem libero, iaculis eget imperdiet quis, posuere vitae lectus. Aenean euismod quis nibh vel ullamcorper. Suspendisse sodales eros ac interdum ullamcorper. Nullam mollis, tortor ut dapibus rutrum, libero risus iaculis metus, volutpat tempor magna mi sit amet turpis. Proin finibus eleifend nunc, et malesuada metus dapibus in. Maecenas eu quam tincidunt, tempor sapien vitae, interdum ante. Fusce eget tortor quis tellus aliquam placerat. Maecenas a luctus lorem. Sed pharetra libero tortor, in rhoncus mauris laoreet et. Aliquam fermentum ante vitae mollis viverra. Sed non pellentesque diam. Duis sed sem vestibulum nulla iaculis cursus vitae sed massa.

#Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Fusce a diam quis orci tempus pharetra quis viverra risus. Mauris quis justo rutrum, laoreet ligula ac, commodo nunc. Integer vitae ex mollis, congue dolor id, pulvinar arcu. Donec vitae lorem dui. Mauris a tempor nibh. Quisque dictum euismod orci, nec convallis massa tristique ut.""", 200
    try:
        # Запрос к OpenAI API
        response = client.completions.create(
            model="gpt-4o-mini",
            prompt=prompt,
            max_tokens=1000,
            temperature=0.7
        )
        return response['choices'][0]['text'].strip(), 200
    except Exception as e:
        return str(e), 500

# Endpoint для получения данных и генерации отчета
@app.route('/generate_report', methods=['GET'])
def generate_report_endpoint():
    # Проверяем, что запрос содержит данные в формате JSON
    if not request.is_json:
        return jsonify({"error": "Data is not taken from JSON"}), 422

    data = request.get_json()

    # Проверяем наличие всех необходимых параметров
    if 'questions' not in data or 'answers' not in data or 'expected_answers' not in data:
        return jsonify({"error": "No required parameter: 'questions', 'answers', 'expected_answers'"}), 422

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
    app.run(host='127.0.0.1', port=5436)
