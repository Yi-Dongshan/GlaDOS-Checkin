
# GLaDOS 自动签到工具

一个基于 Python 实现的 GLaDOS 自动签到工具，支持邮件和 Telegram 通知。

## 功能特性

- ✨ 自动执行每日签到
- 📧 支持邮件通知
- 🤖 支持 Telegram 机器人通知
- 📝 详细的日志记录
- ⏰ 支持 Windows 计划任务和 Linux Cron 定时执行

## 使用方法

### 1. 环境准备

#### Windows
```bash
# 克隆仓库
git clone https://github.com/Yi-Dongshan/glados-checkin.git

# 安装依赖
pip install -r requirements.txt
```

#### Linux
```bash
# 安装 Python3 和 pip
apt update
apt install -y python3 python3-pip git

# 克隆仓库
git clone https://github.com/Yi-Dongshan/glados-checkin.git

# 创建 Python 虚拟环境
cd glados-checkin
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置文件
1. 复制配置文件模板：
   - 将 `config.example.py` 复制为 `config.py`
   - 修改配置文件中的相关信息

2. 配置说明：
   ```python
   # GLaDOS Headers配置
   headers = {
       "cookie": "your_cookie_here",
       "user-agent": "your_user_agent_here",
   }

   # 邮箱配置（使用QQ邮箱）
   EMAIL_CONFIG = {
       'sender_email': 'your_email@qq.com',
       'sender_password': 'your_smtp_password',
       'receiver_email': 'receiver@example.com'
   }

   # Telegram 配置（可选）
   TELEGRAM_CONFIG = {
       'bot_token': 'your_bot_token_here',
       'chat_id': 'your_chat_id_here'
   }

   # 通知方式配置
   NOTIFY_CONFIG = {
       'email': True,    # 是否启用邮件通知
       'telegram': False # 是否启用 Telegram 通知
   }
   ```

### 3. 邮箱配置（QQ邮箱）
1. 登录 QQ 邮箱网页版
2. 点击「设置」->「账户」
3. 找到「POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务」
4. 开启「POP3/SMTP服务」
5. 按照提示发送短信获取授权码
6. 将获取到的授权码填入配置文件的 `sender_password`
7. 注意事项：
   - 发件人邮箱必须是 QQ 邮箱
   - 授权码不是 QQ 密码
   - 如遇到发送失败，检查授权码是否正确

### 4. Telegram 机器人配置（可选）
1. 在 Telegram 中找到 @BotFather，创建新机器人获取 `bot_token`
2. 找到 @userinfobot 获取你的 `chat_id`
3. 将获取的信息填入配置文件

### 5. Linux 服务器部署
1. 创建日志目录：
```bash
mkdir -p log
```

2. 设置权限：
```bash
chmod +x auto_checkin.py
```

3. 测试运行：
```bash
./auto_checkin.py
```

4. 配置定时任务：
```bash
# 编辑 crontab
crontab -e

# 添加定时任务（每天早上 8 点执行）
0 8 * * * cd /path/to/glados-checkin && source venv/bin/activate && python3 auto_checkin.py

# 查看定时任务
crontab -l
```

5. 查看日志：
```bash
tail -f log/checkin.log
```

### 6. Windows 计划任务配置
1. 打开任务计划程序
2. 创建基本任务
3. 设置每天运行的时间
4. 选择启动程序
5. 设置程序路径为 python.exe，参数为脚本的完整路径

## 目录结构
```
glados-checkin/
├── auto_checkin.py    # 主程序
├── config.example.py  # 配置文件模板
├── email_sender.py    # 邮件发送模块
├── telegram_sender.py # Telegram通知模块
├── requirements.txt   # 依赖包列表
└── log/              # 日志目录
    └── checkin.log   # 日志文件
```

## 依赖说明
- Python 3.6+
- requests
- zstandard
- python-telegram-bot（可选，用于 Telegram 通知）

## 常见问题
1. 邮件发送失败
   - 检查 QQ 邮箱是否开启 SMTP 服务
   - 确认授权码是否正确
   - 查看日志文件获取详细错误信息

2. 签到失败
   - 检查 cookie 是否过期
   - 确认网络连接是否正常
   - 查看日志文件排查具体原因

3. Linux 定时任务不执行
   - 检查 crontab 语法是否正确
   - 确认 Python 虚拟环境路径
   - 查看系统日志 `journalctl -u cron`

## 许可证
本项目采用 Apache License 2.0 开源许可证。

## 贡献
欢迎提交 Issue 和 Pull Request！

## 免责声明
本项目仅供学习交流使用，请遵守相关服务条款。
