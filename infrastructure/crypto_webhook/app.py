import logging

from aiocryptopay import AioCryptoPay, Networks
from aiocryptopay.models.update import Update
from aiogram import Bot
from aiohttp import web
from infrastructure.database.repo.requests import RequestsRepo
from infrastructure.database.setup import create_engine, create_session_pool

from tgbot.config import load_config

web_app = web.Application()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
config = load_config()
crypto = AioCryptoPay(token=config.crypto_pay.token, network=Networks.TEST_NET)
bot = Bot(config.tg_bot.token)

engine = create_engine(config.db)
session_pool = create_session_pool(engine)


@crypto.pay_handler()
async def invoice_paid(update: Update, app) -> None:
    async with session_pool() as session:
        repo = RequestsRepo(session)
        await repo.transactions.update_transaction(update.payload)
        user_id = await repo.transactions.get_user_for_invoice(
            update.payload.invoice_id
        )
        await bot.send_message(
            chat_id=user_id,
            text=f"Your invoice {update.payload.invoice_id} was paid!",
        )


async def on_startup(app) -> None:
    logging.info("Starting up")


async def close_session(app) -> None:
    await crypto.close()
    await bot.session.close()


web_app.add_routes([web.post(config.crypto_pay.webhook_url, crypto.get_updates)])
web_app.on_startup.append(on_startup)
web_app.on_shutdown.append(close_session)

web.run_app(app=web_app, host="0.0.0.0", port=3001)
