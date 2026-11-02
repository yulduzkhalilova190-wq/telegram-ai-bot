import os
import time
import telebot
from google import genai
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

bot = telebot.TeleBot(TOKEN)
ai = genai.Client(api_key=GEMINI_API_KEY)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Salom! Men AI botman 😊 Savolingizni yozing!")

@bot.message_handler(func=lambda message: True)
def javob(message):
    print("XABAR KELDI:", message.text)
    for urinish in range(3):
        try:
            bot.send_chat_action(message.chat.id, "typing")


            response = ai.models.generate_content(
               model="gemini-3.5-flash-lite",
               contents=(
                   "Tarjima so‘ralsa, tarjimani o‘sha tilning "
                   "standart asl yozuv tizimida yoz. "
                   "Hech qachon boshqa alifboga transliteratsiya qilma. "
                   "Savolga juda tez, qisqa va aniq javob ber. "
                   "Oddiy savollarga 1-3 gap bilan javob ber. "
                   "Masalan, rus tilida kirill, arab tilida arab yozuvi, "
                   "yapon tilida yapon yozuvi, koreys tilida hangul, "
                   "xitoy tilida xitoy ierogliflaridan foydalan. "
                   "Agar foydalanuvchi lotin yozuvini alohida so‘rasa, " 
                   "Faqat kerakli ma'lumotni yoz.\n\n"
                   "Savolga qisqa, sodda va tushunarli javob ber. "
                   "Keraksiz izoh, Markdown va LaTeX belgilarini ishlatma.\n\n"
                   + message.text
               )
            )
            
            bot.reply_to(message, response.text or "Javob bo‘sh qaytdi.")
            return

        except Exception as e:
            print("Xato:", e)
            if "503" in str(e) or "UNAVAILABLE" in str(e):
                time.sleep(5 * (urinish + 1))
            else:
                break

    bot.reply_to(message, "Gemini hozir band. Keyinroq urinib ko‘ring.")

bot.infinity_polling()
