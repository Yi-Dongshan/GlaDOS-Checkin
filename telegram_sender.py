import requests
import logging

def send_telegram(bot_token, chat_id, message):
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML"
        }
        response = requests.post(url, data=data)
        if response.status_code == 200:
            logging.info("Telegram 消息发送成功")
            return True
        else:
            logging.error(f"Telegram 发送失败: {response.text}")
            return False
    except Exception as e:
        logging.error(f"Telegram 发送异常: {str(e)}")
        return False