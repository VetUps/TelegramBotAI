import httpx

async def get_game_discount(game_title: str) -> str:
    """Ищет самую низкую цену на игру через CheapShark API."""
    url = "https://www.cheapshark.com/api/1.0/games"
    params = {"title": game_title, "limit": 3}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
            data = response.json()

            if not data:
                return f"❌ Игра «{game_title}» не найдена. Проверьте название."

            result_text = f"🎮 **Результаты поиска скидок по запросу «{game_title}»:**\n\n"
            
            for game in data:
                title = game.get("external")
                cheapest_price = game.get("cheapest")
                deal_link = f"https://www.cheapshark.com/redirect?dealID={game.get('cheapestDealID')}"
                
                result_text += f"🔹 **{title}**\n"
                result_text += f"💰 Лучшая цена: ${cheapest_price}\n"
                result_text += f"🔗 [Ссылка на скидку]({deal_link})\n\n"

            return result_text

        except Exception as e:
            print(f"Ошибка CheapShark API: {e}")
            return "⚠️ Произошла ошибка при поиске скидок. Попробуйте позже."