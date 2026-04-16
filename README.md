# GLaDOS 自动签到工具

一个基于 Python 的 GLaDOS 自动签到脚本，支持邮件与 Telegram 通知，适合本地、服务器或 GitHub Actions 自动化运行。

**[快速开始](#快速开始) | [配置说明](#配置说明) | [常见问题](#常见问题)**

---

## 快速开始

### ✨ 推荐方式：GitHub Actions

1. Fork 本仓库
2. 准备好 `config.example.py` 中所需的配置信息, 包括 GLaDOS 网站 **cookie（必需）** , 邮箱授权码（可选）和Telegram(可选)
3. 前往**仓库（而不是GitHub账号）的Settings → Secrets and variables → Actions**，添加 Repository secret 并命名为 CONFIG_PY , 将你的 config.py 配置信息复制到Secrets中
4. 启用 Actions，脚本将每日自动运行

---

## 配置说明

- 配置信息主要包含： **cookie（必需）**, 邮箱（可选）和Telegram(可选)
- **若部署于本地/服务器**：将 `config.example.py` 复制为 `config.py`，并填写配置信息;
- **若部署于 GitHub Actions**：前往**仓库（而不是GitHub账号）的Settings → Secrets and variables → Actions**，添加 Repository secret 并命名为 CONFIG_PY , 将你的 config.py 配置信息复制到Secrets中;
- **安全建议**：请不要将含有真实 Cookie、邮箱授权码等敏感信息直接提交到仓库，使用 GitHub Secrets 或其他加密方式替代。

---

## 环境依赖

- **Python 3.6+**
- 依赖包：

安装依赖：

```bash
pip install -r requirements.txt
```

---

## 本地运行（Windows / Linux）

**Windows：**

```powershell
git clone <repo>
cd GLaDOS-Checkin
pip install -r requirements.txt
# 将 config.example.py 复制为 config.py 并填入信息
python auto_checkin.py
```

**Linux：**

```bash
git clone <repo>
cd GLaDOS-Checkin
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp config.example.py config.py
nano config.py  # 编辑
python3 auto_checkin.py
```

---

## 定时任务

- Linux (cron)：

```bash
mkdir -p log
# 每天 08:00 运行（示例）
0 8 * * * cd /path/to/GlaDOS-Checkin && source /path/to/venv/bin/activate && python3 auto_checkin.py
```

- Windows：使用任务计划程序创建每日任务，执行 `python C:\path\to\GlaDOS-Checkin\auto_checkin.py`。


---

## 目录结构

```
GLaDOS-Checkin/
├── auto_checkin.py       # 主程序
├── config.example.py     # 配置模板
├── config.py             # 配置文件（本地）
├── email_sender.py       # 邮件发送模块
├── telegram_sender.py    # Telegram 通知模块
├── requirements.txt      # 依赖包列表
├── .gitignore            # Git 忽略列表
├── log/
│   └── checkin.log       # 日志文件
└── .github/workflows/
    └── checkin.yml       # GitHub Actions 工作流
```

---

## 常见问题

### Q1: 邮件发送失败怎么办？

**A:** 对于 QQ 邮箱，请使用 SMTP 授权码（不是登录密码），并确认已开启 POP3/SMTP 服务。

### Q2: 如何获取 GLaDOS Cookie？

**A:** 打开 GLaDOS 网站 → F12 → Network → 复制请求头的 Cookie 

### Q3: GitHub Actions 停止运行？

**A:** GitHub 可能在仓库 2 个月无活动时暂停 workflow：
- 前往 **Actions** 页面重新启用一次 workflow
- 或在仓库提交一次代码触发自动运行

---

## 许可证

本项目采用 [Apache License 2.0](LICENSE) 开源许可证。

---

## 免责声明

本项目仅供学习交流使用。请勿用于非法用途，作者不对因使用本脚本造成的任何账号封禁或损失负责。
