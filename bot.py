import logging
from datetime import datetime

from pyrogram import Client, idle
from pyrogram.errors.exceptions.bad_request_400 import BadRequest

from config import TOKEN, disabled_plugins, log_chat, API_ID, API_HASH
from utils import get_restarted, del_restarted

# قراءة الإصدار من ملف النص
with open("version.txt") as f:
    version = f.read().strip()

# إنشاء العميل مع Pyrogram
client = Client("leomedo", API_ID, API_HASH,
                bot_token=TOKEN,
                workers=24,
                parse_mode="html",
                plugins=dict(root="plugins", exclude=disabled_plugins))

# دالة للحصول على الوقت الحالي وتنسيقه
def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# تشغيل العميل ومعالجة الأحداث
with client:
    if __name__ == "__main__":
        # جلب وقت إعادة التشغيل السابق وحذفه
        wr = get_restarted()
        del_restarted()
        try:
            # إرسال رسالة بدء التشغيل مع تضمين الإصدار والوقت الحالي
            client.send_message(log_chat, f"<b>Bot started</b>\n\n"
                                           f"<b>Version:</b> {version}\n"
                                           f"<b>Time:</b> {get_current_time()}")
            print("Bot started\n"
                  f"Version: {version}\n"
                  f"Time: {get_current_time()}")
            # إذا كان هناك إعادة تشغيل سابقة، تحديث رسالتها
            if wr:
                client.edit_message_text(wr[0], wr[1], "Restarted successfully.")
        except BadRequest:
            # تسجيل تحذير في حالة فشل إرسال رسالة بدء التشغيل
            logging.warning("Unable to send message to log_chat.")
        # البقاء على انتظار الأحداث الجديدة
        idle()
