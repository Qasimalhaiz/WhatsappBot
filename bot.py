from whatsapp_web_wrapper import WhatsAPIDriver
import time
import re
import os

AD_KEYWORDS = [
    r"\+966\d{8,}",
    r"سكليف|عذر|إجازة|بحوث|واجبات|اختبارات|خدمات|فل مارك|تواصل|تقارير|مشاريع|عروض|تصاميم|سيرة",
    r"chat\.whatsapp\.com"
]

MENTION_CMD = "!mention"
SPAM_CMD = "!spam"

driver = WhatsAPIDriver()
print("QR Code scanned, WhatsApp bot running...")

def is_advertisement(message):
    for pattern in AD_KEYWORDS:
        if re.search(pattern, message, re.IGNORECASE):
            return True
    return False

while True:
    time.sleep(3)
    for contact in driver.get_unread():
        for message in contact.messages:
            if message.type == 'chat':
                chat = message.chat
                sender = message.sender

                # Process commands
                if message.content == MENTION_CMD:
                    if chat.is_group:
                        mentions = " ".join([f"@{p.id.split('@')[0]}" for p in chat.participants])
                        chat.send_message(f"نداء للجميع:\n{mentions}")
                    continue

                if message.content.strip() == SPAM_CMD and message.quoted_message:
                    offender = message.quoted_message.sender
                    chat.send_message(f"تم حذف إعلان المستخدم {offender.pushname} 🚫")
                    chat.remove_participant(offender.id)
                    continue

                # Detect ad
                if is_advertisement(message.content):
                    print(f"Detected ad from {sender.pushname}: {message.content}")
                    chat.send_message(f"🚫 إعلان ممنوع من {sender.pushname}، تم الطرد.")
                    chat.remove_participant(sender.id)

            elif message.type == 'contact':
                # Someone shared a contact – assume ad
                chat = message.chat
                sender = message.sender
                chat.send_message(f"🚫 تم مشاركة جهة اتصال، افترضنا أنها إعلان من {sender.pushname}. تم الطرد.")
                chat.remove_participant(sender.id)
