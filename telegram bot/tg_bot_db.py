#программа сохраняющая заметок в БД -  todo_list, где интерфейсом выступает телеграм бот
#сначала надо установить зависимость pip install -r requirements.txt, а потом создать БД и таблицу через командную строку: cat ddl.py
import logging
import os
from clickhouse_driver import Client
import pandas as pd
from aiogram import Bot, Dispatcher, executor, types

logging.basicConfic(
    format="(%levelname)s: %(asctime)s - %(message)s",
    datefmt="%d-%b-%y %H-%M-%S",
    level=logging.INFO,
)

#ТАК ДЕЛАТЬ НЕ НАДО, ХРАНИТЬ СЕКРЕТНУЮ ИНФОРМАЦИЮ ЛУЧШЕ ИНАЧЕ, ПОТОМУ ЧТО МОГУТ ЕЁ УКРАСТЬ
#APP_TOKEN = "SECRET_TOKEN"
#лучше так
APP_TOKEN = os.environ.get("APP_TOKEN")
#и далее при поднятии образа задавать токен например так docker run --rn -e APP_TOKEN=abcsdgsg to_bot_env_files
PATH_TO_TODO_TABLE = "todo_result/todo_list.csv"

bot = Bot(token=APP_TOKEN)
dp = Dispatcher(bot)

connection = Client(
    host="localhost",
    user="default",
    password="",
    port=9000,
    database="todo"
)

@dp.message_handler(commands="all")
async def add_tasks(payload: types.Message):
    ch_all_data = connection.execute("SELECT * FROM todo.todo")
    await payload.reply(f"'''{pd.DataFrame(ch_all_data, colomns=['text', 'status']).to_markdown()}'''", parse_mode="Markdown")

@dp.message_handler(commands="done")
async def complete_task(payload: types.Message):
    text = payload.get_args().strip()
    connection.execute(
        "ALTER TABLE todo.todo UPDATE status = 'complete' WHERE text = %(text)s", {"text": text}
    )
    logging.info(f"Добавил задачу: - {text}")
    await payload.reply(f"Выполнено:  *{text}*", parse_mode="Markdown")

if __name__ == "__main__":
    executor.start_polling(dp)
