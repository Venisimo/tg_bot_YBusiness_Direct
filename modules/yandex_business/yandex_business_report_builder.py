import asyncio
from models.account import Account
from typing import List
from modules.yandex_direct.budget_formatter import BudgetFormatter

class YandexBusinessReportBuilder:
    def __init__(self):
        # Можно инициализировать внутренние переменные, если нужно
        pass
    
    async def fetch_campaigns(self, account: Account, date_from: str, date_to: str):
        """
        Возвращает список рекламных кампаний аккаунта Яндекс.Бизнеса (тестовые данные)
        """
        mock_campaigns = [
            {
                "id": 1,
                "name": "Тестовая кампания №1",
                "status": "RUNNING",
                "remainingDays": 8,
                "paused": "Нет",
                "mapsOnly": "Нет",
                "url": "https://yandex.ru/business/1",
            },
            {
                "id": 2,
                "name": "Тестовая кампания №2",
                "status": "PAUSED",
                "remainingDays": 15,
                "paused": "Да",
                "mapsOnly": "Да",
                "url": "https://yandex.ru/business/2",
            },
        ]
        return mock_campaigns

    async def fetch_summary_statistics(self, accounts: List[Account], date_from: str, date_to: str) -> str:
        """
        Возвращает сводную статистику для аккаунта Яндекс.Бизнеса
        """

        # Заглушка
        result = "*Сводная статистика Яндекс.Бизнеса*\n"

        for account in accounts:
            result += (
                f"Аккаунт: {account.account_name}\n"
                f"Показы: 123\n"
                f"Клики: 45\n"
                f"Расход: 678\n"
                f"Конверсии: 9\n\n"
            )

        return result

    async def fetch_budgets(self, accounts: List[Account]) -> str:
        """
        Тестовый метод для получения бюджетов Яндекс.Бизнеса
        """
        if not accounts:
            return "❌ *Нет аккаунтов Яндекс.Бизнеса*"

        parts = ["*Бюджеты Яндекс.Бизнеса*"]
        for account in accounts:
            # Заглушка данных бюджета
            parts.append(
                f"Аккаунт: {account.account_name}\n"
                f"Бюджет: 10000 ₽\n"
                f"Потрачено: 3456 ₽\n"
                f"Остаток: 6544 ₽"
            )

        return "\n\n".join(parts)

    async def fetch_detailed_statistics(self, account: Account, date_from: str, date_to: str):
        """
        Возвращает детальную статистику для аккаунта Яндекс.Бизнеса
        """
        # Исправлено: правильный вызов метода fetch_campaigns
        mock_campaigns = await self.fetch_campaigns(account, date_from, date_to)

        reports = [f"*Детальный отчет Яндекс.Бизнеса*\nАккаунт: {account.account_name}\n"]

        for campaign in mock_campaigns:
            warning = ""
            if campaign["remainingDays"] < 10:
                warning = "\n⚠️ *Внимание!* До окончания кампании осталось <10 дней!"

            reports.append(
                f"{warning}\n"
                f"ID кампании: {campaign['id']}\n"
                f"Название кампании: {campaign['name']}\n"
                f"Статус: {campaign['status']}\n"
                f"Дней до окончания: {campaign['remainingDays']}\n"
                f"Приостановлена: {campaign['paused']}\n"
                f"Только на картах: {campaign['mapsOnly']}\n"
                f"Ссылка: {campaign['url']}\n"
                "-----------------------------"
            )

        return ["\n".join(reports)]