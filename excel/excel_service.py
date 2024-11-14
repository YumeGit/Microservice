import os
import pandas as pd
from flask import Flask, request, jsonify, send_file
from dotenv import load_dotenv
from io import BytesIO

app = Flask(__name__)
port = os.getenv("PORT", 5002)

# Функция для создания Excel файла из полученных данных
def create_excel(questions, answers, security_results):
    # Создаем DataFrame из полученных данных
    data = {
        'Вопросы': questions,
        'Ответы': answers,
        'Результат защищённости': security_results
    }

    df = pd.DataFrame(data)

    # Создаем Excel-файл в памяти
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    
    output.seek(0)  # Перемещаем указатель в начало для последующего чтения

    return output

# Endpoint для получения JSON данных и создания Excel файла
@app.route('/export_to_excel', methods=['POST'])
def export_to_excel():
    # Проверяем, что запрос содержит данные в формате JSON
    if not request.is_json:
        return jsonify({"error": "Expected JSON data"}), 422

    data = request.get_json()

    # Проверяем наличие всех необходимых параметров
    if 'questions' not in data or 'answers' not in data or 'security_results' not in data:
        return jsonify({"error": "Missing required parameters: 'questions', 'answers', 'security_results'"}), 422

    # Проверяем, что все параметры являются списками
    if not isinstance(data['questions'], list) or not isinstance(data['answers'], list) or not isinstance(data['security_results'], list):
        return jsonify({"error": "Parameters 'questions', 'answers', and 'security_results' must be lists"}), 422

    # Создаем Excel файл
    try:
        excel_file = create_excel(data['questions'], data['answers'], data['security_results'])
    except Exception as e:
        return jsonify({"error": f"Failed to create Excel file: {str(e)}"}), 500

    # Возвращаем файл в ответе
    return send_file(excel_file, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
                     as_attachment=True, download_name='report.xlsx')

# Запуск сервера
if __name__ == '__main__':
    from waitress import serve
    print(f"Running server at 0.0.0.0:{port}");
    serve(app, host="0.0.0.0", port=port)
