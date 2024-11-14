from flask import Flask, request, jsonify
from datetime import datetime
import os
import json
from dotenv import load_dotenv

app = Flask(__name__)

# Получаем настройки из .env
LOG_FOLDER = os.getenv('LOG_FOLDER', 'logs')
PORT = int(os.getenv('PORT', 5003))

# Создаем папку для логов, если ее нет
os.makedirs(LOG_FOLDER, exist_ok=True)

# Имя файла логов с текущей датой
log_file_name = f"{datetime.now().strftime('%Y-%m-%d')}.log"
log_file_path = os.path.join(LOG_FOLDER, log_file_name)

# Функция для записи логов в файл
def write_log(log_entry):
    with open(log_file_path, 'a') as f:
        f.write(log_entry)

# Маршрут для получения логов от главного сервиса
@app.route('/log', methods=['POST'])
def log_data():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Нет данных"}), 400

    # Записываем лог в файл (в формате JSON для читаемости)
    write_log(data["message"])

    return jsonify({"status": "Лог записан"}), 201

# Запуск сервиса
if __name__ == '__main__':
    from waitress import serve
    print(f"Running server at 0.0.0.0:{PORT}");
    serve(app, host="0.0.0.0", port=PORT)
