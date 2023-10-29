#программа сохраняющая заметок в файл -  todo_list, где интерфейсом выступает телеграм бот
import logging
import os
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

def get_todo_data():
    return pd.read_csv(PATH_TO_TODO_TABLE)

@dp.message_handler(commands="all")
async def add_tasks(payload: types.Message):
    await payload.reply(f"'''{get_todo_data().to_markdown()}'''", parse_mode="Markdown")

@dp.message_handler(commands="add")
async def add_task(payload: types.Message):
    text = payload.get_args().strip()
    new_task = pd.DataFrame({"text": [text], "status": ["active"]})
    updated_tasks = pd.concat([get_todo_data(), new_task], ignore_index=True, axis=0)
    updated_tasks.to_csv(PATH_TO_TODO_TABLE, index=False)
    logging.info(f"Добавил задачу: - {text}")
    await payload.reply(f"Выполнено:  *{text}*", parse_mode="Markdown")

if __name__ == "__main__":
    executor.start_polling(dp)
