const express = require('express');
const fs = require('fs');
const path = require('path');
const dotenv = require('dotenv');

// Загружаем настройки из .env файла
dotenv.config();

const app = express();
app.use(express.json());

// Получаем настройки из .env
const LOG_FOLDER = process.env.LOG_FOLDER || 'logs';
const PORT = process.env.PORT || 8080;

// Создаем папку для логов, если ее нет
if (!fs.existsSync(LOG_FOLDER)) {
  fs.mkdirSync(LOG_FOLDER, { recursive: true });
}

// Имя файла логов с текущей датой
const logFileName = `${new Date().toISOString().split('T')[0]}.log`;
const logFilePath = path.join(LOG_FOLDER, logFileName);

// Функция для записи логов в файл
const writeLog = (logEntry) => {
  fs.appendFileSync(logFilePath, logEntry);
};

// Маршрут для получения логов от главного сервиса
app.post('/log', (req, res) => {
  const data = req.body;

  if (!data || !data.message) {
    return res.status(400).json({ error: 'Нет данных' });
  }

  // Записываем лог в файл (в формате JSON для читаемости)
  writeLog(`${data.message}\n`);

  return res.status(201).json({ status: 'Лог записан' });
});

// Запуск сервера
app.listen(PORT, () => {
  console.log(`Running server at http://0.0.0.0:${PORT}`);
});
