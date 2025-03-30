
# GLaDOS 自动签到⚡

_✨ 基于 Python 实现的 GLaDOS 自动签到程序 ✨_

## 功能特点

- 自动执行每日签到
- 邮件通知签到结果
- 详细的日志记录
- 支持 Windows 计划任务和 Linux Cron 定时执行

## 环境要求

- Python 3.8+
- 依赖包：见 requirements.txt

## 快速开始

1. 克隆仓库：
```bash
git clone https://github.com/your-username/GlaDOS-Checkin.git
cd GlaDOS-Checkin
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 配置文件：
   - 复制 `config.example.py` 为 `config.py`
   - 在 `config.py` 中填入你的 GLaDOS 账号 headers 信息
   - 配置邮箱信息（推荐使用 QQ 邮箱）

## 部署说明

### Windows 系统

1. 打开任务计划程序
2. 创建基本任务
3. 设置每天 00:01 运行
4. 操作选择运行 Python 脚本
5. 填写脚本完整路径

### Linux 系统

1. 上传文件到服务器：
```bash
mkdir -p /root/glados-checkin
# 使用 SFTP 等工具上传文件
```

2. 安装依赖：
```bash
cd /root/glados-checkin
pip3 install -r requirements.txt
```

3. 创建日志目录：
```bash
mkdir -p /root/glados-checkin/log
chmod 755 /root/glados-checkin/log
```

4. 添加定时任务：
```bash
crontab -e
# 添加以下内容：
1 0 * * * cd /root/glados-checkin && /usr/bin/python3 auto_checkin.py >> /root/glados-checkin/log/cron.log 2>&1
```

## 配置说明

### 邮箱配置

1. 使用 QQ 邮箱
2. 开启 SMTP 服务
3. 获取授权码
4. 在 config.py 中配置：
```python
EMAIL_CONFIG = {
    'sender_email': 'your_qq_email@qq.com',
    'sender_password': 'your_smtp_auth_code',
    'receiver_email': 'receiver@example.com'
}
```

### GLaDOS Headers 获取

1. 登录 GLaDOS 网站
2. 打开开发者工具（F12）
3. 复制任意请求中的 headers
4. 填入 config.py

## 日志说明

- 日志位置：`log/checkin.log`
- 记录内容：签到状态、积分变化、剩余天数等
- 格式：时间 + 日志级别 + 信息

## 注意事项

1. 请勿泄露你的 headers 信息
2. 建议先本地测试成功后再部署到服务器
3. 遇到问题先查看日志文件
4. 确保服务器时区正确设置

## 许可证

Apache License 2.0
