
# GLaDOS 自动签到工具

一个基于 Python 的 GLaDOS 自动签到脚本，支持邮件与 Telegram 通知，适合本地、服务器或 GitHub Actions 自动化运行。

---

## 快速开始（推荐：GitHub Actions）

1. Fork 或 Clone 本仓库。
2. 在仓库 Settings → Secrets → Actions 添加所需 Secrets（参见下方“GitHub Actions 部署”）。
3. 在仓库根目录添加工作流文件 `.github/workflows/daily_checkin.yml`（示例见下方），保存并在 Actions 页面手动触发一次以验证。


---

## 先决条件

- Python 3.6+
- 依赖见 `requirements.txt`（本项目主要依赖 `requests`、`zstandard`，可选 `python-telegram-bot` 用于 Telegram）

安装（示例）：

```bash
pip install -r requirements.txt
```

---

## 配置说明

1. 复制模板：将 `config.example.py` 复制为 `config.py`，并填写信息；或者在 CI 中用 Secrets 动态生成 `config.py`（推荐）。

2. `config.example.py` 中主要变量：

```python
headers = {
    'cookie': 'your_cookie',
    'user-agent': 'your_user_agent'
}

EMAIL_CONFIG = {
    'sender_email': 'your_email@qq.com',
    'sender_password': 'your_smtp_password',
    'receiver_email': 'receiver@example.com'
}

TELEGRAM_CONFIG = {
    'bot_token': 'your_bot_token',
    'chat_id': 'your_chat_id'
}

NOTIFY_CONFIG = {
    'email': True,
    'telegram': False
}
```

安全建议：请不要将含有真实 Cookie、邮箱授权码等敏感信息直接提交到仓库，使用 GitHub Secrets 或其他加密方式替代。

---

## 本地运行（Windows / Linux）

Windows：

```powershell
git clone <repo>
cd GLaDOS-Checkin
pip install -r requirements.txt
# 将 config.example.py 复制为 config.py 并填入信息
python auto_checkin.py
```

Linux（建议在虚拟环境中运行）：

```bash
git clone <repo>
cd GLaDOS-Checkin
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp config.example.py config.py
vim config.py  # 编辑
python3 auto_checkin.py
```

---

## 服务器/定时任务

- Linux (cron)：

```bash
mkdir -p log
# 每天 08:00 运行（示例）
0 8 * * * cd /path/to/GlaDOS-Checkin && source /path/to/venv/bin/activate && python3 auto_checkin.py
```

- Windows：使用任务计划程序创建每日任务，执行 `python C:\path\to\GlaDOS-Checkin\auto_checkin.py`。

查看日志：

```bash
tail -n 200 log/checkin.log
```

---

## GitHub Actions 部署（细节）

推荐将敏感信息拆成多个 Secrets（例如 `HEADERS_JSON`、`EMAIL_SENDER` 等），而不是把整个 `config.py` 内容作为单个 Secret，这样更易维护与旋转凭据。

需添加的 Secrets（示例）：

- `HEADERS_JSON`：headers 的 JSON 字符串（含 cookie 等）
- `EMAIL_SENDER`、`EMAIL_PASSWORD`、`EMAIL_RECEIVER`
- `TELEGRAM_BOT_TOKEN`、`TELEGRAM_CHAT_ID`
- `NOTIFY_EMAIL`、`NOTIFY_TELEGRAM`（可选，true/false）

在 workflow 中使用这些 Secrets 动态生成 `config.py`（参见上方示例）。

---

## 目录结构

```
GlaDOS-Checkin/
├── auto_checkin.py    # 主程序
├── config.example.py  # 配置文件模板
├── email_sender.py    # 邮件发送模块
├── telegram_sender.py # Telegram通知模块
├── requirements.txt   # 依赖包列表
└── log/               # 日志目录
    └── checkin.log    # 日志文件
```

---

## 常见问题 (FAQ)

Q: 为什么 GitHub Actions 报错 `ImportError: cannot import name 'headers'`？

A: 请检查 workflow 中生成的 `config.py` 是否包含 `headers`、`EMAIL_CONFIG` 等变量，且 Secrets 名称与 workflow 中引用一致。

Q: 邮件发送失败怎么办？

A: 对于 QQ 邮箱，请使用 SMTP 授权码（不是登录密码），并确认已开启 POP3/SMTP 服务。

Q: Actions 停止触发怎么办？

A: 如果仓库长时间无活动，GitHub 可能暂停 workflow。前往 Actions 页面重新启用或在仓库做一次提交/手动触发。

---

## 许可证

本项目采用 [Apache License 2.0](LICENSE) 开源许可证。

---

## 免责声明

本项目仅供学习交流使用。请勿用于非法用途，作者不对因使用本脚本造成的任何账号封禁或损失负责。


