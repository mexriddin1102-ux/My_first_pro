import telebot
from telebot import types

# Rasmlardan olingan aniq ma'lumotlar
BOT_TOKEN = "8897530069:AAHZRt0xzOMalHvpXlCo5u18VqumdBThlAw"
GROUP_CH_ID = "@ariza_ber_uz_bot_ibraimov"  # Havola o'rniga username formatida to'g'rilandi

bot = telebot.TeleBot(BOT_TOKEN)

# Foydalanuvchi ma'lumotlarini vaqtinchalik saqlash uchun lug'at
user_data = {}

# 1. /start buyrug'i
@bot.message_handler(commands=['start'])
def start_command(message):
    chat_id = message.chat.id
    user_data[chat_id] = {} # Yangi foydalanuvchi uchun joy ajratish
    
    welcome_text = "Assalomu alaykum! Ro'yxatdan o'tish uchun quyidagi ma'lumotlarni to'ldiring.\n\n" \
                   "Iltimos, **O'quvchining F.I.Sh.** (Familiya, Ism, Sharifini) kiriting:"
    
    bot.send_message(chat_id, welcome_text, parse_mode="Markdown")
    bot.register_next_step_handler(message, get_student_name)

# 2. O'quvchi F.I.Sh. qabul qilish
def get_student_name(message):
    chat_id = message.chat.id
    user_data[chat_id]['student_name'] = message.text
    
    bot.send_message(chat_id, "Yoshingizni kiriting:")
    bot.register_next_step_handler(message, get_age)

# 3. Yoshini qabul qilish
def get_age(message):
    chat_id = message.chat.id
    user_data[chat_id]['age'] = message.text
    
    bot.send_message(chat_id, "Sinfingizni kiriting (Masalan: 9-A):")
    bot.register_next_step_handler(message, get_class)

# 4. Sinfi qabul qilish
def get_class(message):
    chat_id = message.chat.id
    user_data[chat_id]['class'] = message.text
    
    bot.send_message(chat_id, "Ota-onangizning F.I.Sh. kiriting:")
    bot.register_next_step_handler(message, get_parent_name)

# 5. Ota-onasi F.I.Sh. qabul qilish va Telefon raqam tugmasini ko'rsatish
def get_parent_name(message):
    chat_id = message.chat.id
    user_data[chat_id]['parent_name'] = message.text
    
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    contact_button = types.KeyboardButton(text="📱 Telefon raqamni yuborish", request_contact=True)
    markup.add(contact_button)
    
    bot.send_message(chat_id, "Pastdagi tugmani bosib telefon raqamingizni yuboring:", reply_markup=markup)
    bot.register_next_step_handler(message, get_phone)

# 6. Telefon raqamni qabul qilish
def get_phone(message):
    chat_id = message.chat.id
    
    if message.contact is not None:
        phone = message.contact.phone_number
    else:
        phone = message.text

    user_data[chat_id]['phone'] = phone
    
    remove_markup = types.ReplyKeyboardRemove()
    bot.send_message(chat_id, "Yashash manzilingizni kiriting:", reply_markup=remove_markup)
    bot.register_next_step_handler(message, get_address)

# 7. Yashash manzilini qabul qilish va Kanalga yuborish
def get_address(message):
    chat_id = message.chat.id
    user_data[chat_id]['address'] = message.text
    
    data = user_data[chat_id]
    
    report_text = f"📝 **Yangi Ariza!**\n\n" \
                  f"👤 **O'quvchi:** {data['student_name']}\n" \
                  f"🎂 **Yoshi:** {data['age']}\n" \
                  f"🏫 **Sinfi:** {data['class']}\n" \
                  f"👨‍👩‍👦 **Ota-onasi:** {data['parent_name']}\n" \
                  f"📞 **Tel:** {data['phone']}\n" \
                  f"📍 **Manzil:** {data['address']}\n" \
                  f"🆔 **Telegram ID:** `{chat_id}`"
                  
    try:
        bot.send_message(GROUP_CH_ID, report_text, parse_mode="Markdown")
        success_text = "Arizangiz muvaffaqiyatli qabul qilindi. Tez orada operatorlarimiz siz bilan bog‘lanadi."
        bot.send_message(chat_id, success_text)
    except Exception as e:
        bot.send_message(chat_id, "Xatolik yuz berdi. Iltimos qaytadan urinib ko'ring yoki admin bilan bog'laning.")
        print(f"Kanalga yuborishda xatolik: {e}")
        
    if chat_id in user_data:
        del user_data[chat_id]

# Botni uzluksiz ishga tushirish
print("Bot muvaffaqiyatli ishga tushdi...")
bot.infinity_polling()




