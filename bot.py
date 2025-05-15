# filename: bot.py

import json
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    ContextTypes,
)

TOKEN = "PASTE_YOUR_TOKEN_HERE"

QUESTIONS = [
    "1️⃣ Что произошло? (Факт)",
    "2️⃣ Как это подаётся в источнике? (Интерпретация)",
    "3️⃣ Кому это выгодно? (Классовая функция)",
    "4️⃣ О чём умалчивают? (Молчание)",
    "5️⃣ Каковы материальные причины? (Противоречие)",
    "6️⃣ Зачем это сообщение? (Цель, телеология)",
    "7️⃣ Пролетарская трактовка события?",
]

STATE = range(7)
user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Напиши /analyze чтобы начать анализ новости.")

async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data[update.effective_chat.id] = []
    await update.message.reply_text(QUESTIONS[0])
    return STATE[0]

async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid = update.effective_chat.id
    step = len(user_data[cid])
    user_data[cid].append(update.message.text)

    if step + 1 < len(QUESTIONS):
        await update.message.reply_text(QUESTIONS[step + 1])
        return STATE[step + 1]
    else:
        # Сборка финального отчёта
        summary = "\n".join([f"{QUESTIONS[i]}\n{user_data[cid][i]}" for i in range(7)])
        # Сохраняем в файл
        with open(f"analysis_{cid}.json", "a", encoding="utf-8") as f:
            json.dump({"user": cid, "answers": user_data[cid]}, f, ensure_ascii=False)
            f.write("\n")

        await update.message.reply_text("📝 Готово! Вот твой анализ:\n\n" + summary)
        return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Анализ отменён.")
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("analyze", analyze)],
        states={STATE[i]: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer)] for i in range(7)},
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == "__main__":
    main()

import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Получение токена из переменных среды Railway
TOKEN = os.environ.get("TOKEN")

# Текст шаблона анализа
ANALYSIS_SCHEMA = """
🔧 Шаблон пролетарского анализа новости

1. **Факт (бытие)**  
Что конкретно произошло, без интерпретации?  
Пример: «Центральный банк повысил ключевую ставку на 1%.»

2. **Интерпретация (надстройка)**  
Как это подаётся в источнике? Какие причины названы? Какие чувства формируются?  
Пример: «Для сдерживания инфляции и укрепления доверия к рублю.»

3. **Классовая функция**  
Кому выгодна такая подача? Чьи интересы обслуживает сообщение?  
Пример: Укрепляет позицию буржуазии, формирует представление о «необходимости» антинародной меры.

4. **Молчание (что скрыто?)**  
О чём не сказано? Какие аспекты намеренно упущены?  
Пример: Не упомянуто, как рост ставки ударит по заемщикам, производству, ЖКХ.

5. **Материальная подоплёка**  
Какие экономические интересы и противоречия лежат в основе явления?  
Пример: Инфляция вызвана ростом издержек и монополизацией, а не «паникой».

6. **Цель (телеология)**  
Зачем именно эта новость появилась в таком виде? Что она должна вызвать?  
Пример: Снизить возмущение, внушить фатализм, оправдать буржуазную политику.

7. **Альтернативная (пролетарская) трактовка**  
Как бы выглядело сообщение, если бы его писали с позиции рабочего класса?  
Пример: «ЦБ переложил инфляционные издержки на трудящихся, чтобы спасти спекулятивный капитал.»
"""

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Напиши /schema чтобы получить шаблон анализа новости.")

# Команда /schema
async def schema(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(ANALYSIS_SCHEMA, parse_mode="Markdown")

# Запуск приложения
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("schema", schema))

    print("Бот запущен...")
    app.run_polling()
