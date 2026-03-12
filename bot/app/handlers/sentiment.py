from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from app.states.fsm import BotStates
from app.services.ml_service.ml_client import MlClient

router = Router()


@router.message(F.text == "📊 Классификация тональности")
async def sentiment_start(message: types.Message, state: FSMContext):
    await state.set_state(BotStates.waiting_for_sentiment_text)
    await message.answer("Отправьте текст, и я проверю его на токсичность:")


@router.message(BotStates.waiting_for_sentiment_text)
async def sentiment_analyze(
    message: types.Message, state: FSMContext, ml_client: MlClient
):
    text_to_analyze = message.text
    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")

    try:
        response = await ml_client.classify(text_to_analyze, model="base_bert")

        res = response.get("result", {})
        preds = res.get("predictions", {})

        status = "✅ Текст чист" if preds.get("normal") else "⚠️ Обнаружена токсичность"

        details = "\n".join(
            [f"- {k}: {'✅' if v else '❌'}" for k, v in preds.items() if k != "normal"]
        )

        await message.answer(
            f"📊 **Результат анализа:**\n\nИтог: {status}\nДетали:\n{details}",
            parse_mode="Markdown",
        )
    except Exception as e:
        await message.answer(f"❌ Ошибка ML-сервиса: {str(e)}")

    await state.clear()
