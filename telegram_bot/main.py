import asyncio
import json
import time
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
import websockets

BOT_TOKEN = "8427374146:AAGKKjXspg0GwSId9YJL1Wo-ABUSYHzTr6A"
kostya_user_id = 8427374146
last_send_time = 0

bot = Bot(
    token=BOT_TOKEN,
)
dp = Dispatcher()

binance_url = "wss://fstream.binance.com/ws/btcusdt@aggTrade"

@dp.message(CommandStart())
async def get_start(msg: Message):
    user_id = msg.from_user.id
    await msg.answer(text= f"{user_id=}")

async def fetch_binance_trades(url:str):
    async with websockets.connect(url) as ws:
        global last_send_time
        async for msg in ws:
            #print(msg)
            data = json.loads(msg)
            price = data["p"]
            if (time.time() - last_send_time) > 5:
                await send_message_to_tg(
                                           msg = f"Last price {price}"
                                        )
                last_send_time = time.time()

async def send_message_to_tg(msg:str):
   await bot.send_message(
       chat_id= kostya_user_id,
       text = msg
   )

async def main():
    await dp.start_polling(bot)
    async with asyncio.TaskGroup() as task_group:
        task_group.create_task(fetch_binance_trades(binance_url))
        task_group.create_task(dp.start_polling(bot, handle_signals=False))



if __name__ == '__main__':
    asyncio.run(main())