import os
from telegram.ext import ApplicationBuilder, CommandHandler

TOKEN = os.getenv("BOT_TOKEN")
print("BOT_TOKEN from env:", TOKEN)

if not TOKEN:
    raise ValueError("BOT_TOKEN is not set. Please check your environment variables.")

app = ApplicationBuilder().token(TOKEN).build()

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

# Обработка команд
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Напиши /schema для шаблона анализа или /analyze чтобы разобрать новость.")

async def schema(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(ANALYSIS_SCHEMA, parse_mode="Markdown")

async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Отправь новость или фрагмент текста, и я помогу разобрать её по пролетарскому шаблону.")

# Обработка любых сообщений после /analyze
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    response = f"""
Начинаем анализ:

1. **Факт (бытие)**  
🔹 {user_text}

2. **Интерпретация (надстройка)**  
🔸 (Как это подаётся? Кто говорит? Какие чувства вызывает?)

3. **Классовая функция**  
🔸 (Чьи интересы обслуживаются? Кому выгодно?)

4. **Молчание (что скрыто?)**  
🔸 (О чём умолчали?)

5. **Материальная подоплёка**  
🔸 (Какие противоречия в основе события?)

6. **Цель (телеология)**  
🔸 (Зачем именно в таком виде? Что формирует?)

7. **Альтернативная трактовка**  
🔸 (Как бы выглядело с позиции трудящихся?)
"""
    await update.message.reply_text(response, parse_mode="Markdown")

# Запуск приложения
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("schema", schema))
    app.add_handler(CommandHandler("analyze", analyze))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен...")
    app.run_polling()
