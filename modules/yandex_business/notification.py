from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot
from modules.yandex_business.yandex_business_report_builder import YandexBusinessReportBuilder
from database.db import get_all_accounts
from enums.sources import Source
from models.account import Account

async def check_campaigns_and_notify(bot: Bot):
    """
    Проверка кампаний Яндекс.Бизнеса и отправка уведомлений,
    если осталось < 10 дней.
    """

    raw_accounts = await get_all_accounts("accounts.db")
    accounts = [Account(**acc) for acc in raw_accounts if acc["source"] == Source.YANDEX_BUSINESS.value]
    builder = YandexBusinessReportBuilder()

    for acc in accounts:
        campaigns = await builder.fetch_campaigns(acc, "2025-08-01", "2025-08-25")

        for campaign in campaigns:
            if campaign["remainingDays"] <= 10:
                text = (
                    f"⚠️ *Внимание!* До окончания кампании осталось <10 дней!\n"
                    f"Аккаунт: {acc.account_name}\n"
                    f"Кампания: {campaign['name']}\n"
                    f"Статус: {campaign['status']}\n"
                    f"Дней до окончания: {campaign['remainingDays']}\n"
                    f"Ссылка: {campaign['url']}"
                )
                await bot.send_message(acc.user_id, text, parse_mode="Markdown")



async def setup_scheduler(bot: Bot):
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(check_campaigns_and_notify, "interval", hours=12, args=[bot])
    scheduler.start()
