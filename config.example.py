# GLaDOS 账号配置
ACCOUNTS = [
    {
        "name": "账号1",
        "headers": {
            "cookie": "your_cookie_here_1",
            "user-agent": "Mozilla/5.0...",
            # ... 其他必要的 headers
        }
    },
    {
        "name": "账号2",
        "headers": {
            "cookie": "your_cookie_here_2",
            "user-agent": "Mozilla/5.0...",
            # ... 其他必要的 headers
        }
    }
]

# 通知方式配置
NOTIFY_CONFIG = {
    'email': True,    # 是否启用邮件通知, 默认开启
    'telegram': False  # 是否启用 Telegram 通知, 默认关闭
}

# 邮箱配置(可选)
EMAIL_CONFIG = {
    'sender_email': 'your_email@qq.com',
    'sender_password': 'your_smtp_password',
    'receiver_email': 'receiver@example.com'
}

# Telegram 配置(可选)
TELEGRAM_CONFIG = {
    'bot_token': 'your_bot_token_here',  # 从 @BotFather 获取
    'chat_id': 'your_chat_id_here'       # 可以从 @userinfobot 获取
}
