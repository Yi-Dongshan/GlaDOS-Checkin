import os
import io
import json
import time
import requests
import logging
from datetime import timedelta, date
from config import ACCOUNTS, EMAIL_CONFIG, TELEGRAM_CONFIG, NOTIFY_CONFIG
import zstandard as zstd
from email_sender import send_email
from telegram_sender import send_telegram

os.chdir(os.path.dirname(os.path.abspath(__file__)))

if not os.path.exists('log'):
    os.makedirs('log')

# 保持原有的日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler("log/checkin.log", encoding='utf-8'),
    ]
)

# 保持原有的 checkin 和 get_leftdays 函数不变
def checkin(headers):
    checkin_url = "https://glados.one/api/user/checkin"
    payload = {"token":"glados.one"}
    
    try:
        logging.info(f"开始签到请求: {checkin_url}")
        
        # 在请求头中明确指定接受的编码
        headers['Accept-Encoding'] = 'gzip, deflate'  # 移除 zstd
        
        response = requests.post(checkin_url, headers=headers, data=json.dumps(payload))
        
        logging.info(f"响应状态码: {response.status_code}")
        logging.info(f"响应头: {response.headers}")
        logging.info(f"原始响应内容: {response.content[:100]}")  # 记录前100个字节的响应内容

        try:
            # 首先尝试直接解析响应
            text = response.text
            res = json.loads(text)
        except:
            # 如果直接解析失败，且确实是 zstd 编码，则尝试解压
            if response.headers.get("Content-Encoding") == "zstd":
                try:
                    dctx = zstd.ZstdDecompressor()
                    decompressed = dctx.decompress(response.content)
                    text = decompressed.decode('utf-8', errors='ignore')
                    res = json.loads(text)
                except Exception as decomp_error:
                    logging.error(f"zstd解压失败：{decomp_error}")
                    raise
            else:
                raise

        return res

    except Exception as e:
        logging.error(f"❌ 签到请求失败：{str(e)}")
        logging.error("详细错误信息：", exc_info=True)
        return {"message": "签到失败", "error": str(e)}


# 获取账号信息
def get_leftdays(headers):
    url = "https://glados.one/api/user/status"

    try:
        # 在请求头中明确指定接受的编码
        headers['Accept-Encoding'] = 'gzip, deflate'
        
        response = requests.get(url, headers=headers)
        
        try:
            text = response.text
            res = json.loads(text)
        except:
            if response.headers.get("Content-Encoding") == "zstd":
                dctx = zstd.ZstdDecompressor()
                decompressed = dctx.decompress(response.content)
                text = decompressed.decode('utf-8', errors='ignore')
                res = json.loads(text)
            else:
                raise

        return int(res['data']['leftDays'].split('.')[0])
    
    except Exception as e:
        logging.error(f"获取天数失败：{str(e)}")
        logging.error("详细错误信息：", exc_info=True)
        return None

def calculate_expiration_date(remaining_days):
    # 获取今天的日期
    current_date = date.today()
    # 计算到期日
    expiration_date = current_date + timedelta(days=remaining_days)
    # 返回到期日的字符串表示
    return expiration_date.strftime('%Y-%m-%d')


if __name__ == '__main__':
    try:

        all_messages = [] # 用于汇总所有账号的运行结果
        summary_status = "成功"

        logging.info(f"开始执行多账号签到任务，共 {len(ACCOUNTS)} 个账号")

        for idx, account in enumerate(ACCOUNTS):
            acc_name = account.get('name', f"账号 {idx+1}")
            acc_headers = account.get('headers')
            
            logging.info(f"--- 正在处理账号: {acc_name} ---")
            
            try:
                start_time = time.time()
                res = checkin(acc_headers)
                
                checkin_result = res.get('message', '未知错误')
                # 兼容 balance 可能不存在的情况
                points_balance = res['list'][0]['balance'].split('.')[0] if 'list' in res else "N/A"
                change = res['list'][0]['change'].split('.')[0] if 'list' in res else "0"
                
                leftdays = get_leftdays(acc_headers)
                time_taken = time.time() - start_time
                exp_date = calculate_expiration_date(int(leftdays)) if leftdays is not None else "未知"
                
                msg = (
                    f"👤 账号：{acc_name}\n"
                    f"✅ 状态：{checkin_result}\n"
                    f"⏳ 剩余：{leftdays} 天 ({exp_date})\n"
                    f"🧧 积分：{points_balance} (+{change})\n"
                )
                all_messages.append(msg)
                logging.info(f"{acc_name} 签到完成")

            except Exception as e:
                error_msg = f"❌ 账号 {acc_name} 执行出错：{str(e)}"
                all_messages.append(error_msg)
                logging.error(error_msg)
                summary_status = "部分失败"

            # 账号之间稍微停顿一下，防止请求过快被封 IP
            time.sleep(2)

        # 汇总所有账号的消息内容
        final_full_msg = f"📅 GLaDOS 每日签到汇总报告\n{'='*25}\n" + "\n".join(all_messages)
        
        # --- 发送汇总通知 ---
        if NOTIFY_CONFIG.get('email', True):
            subject = f"GLaDOS 签到通知 - {summary_status}"
            send_email(subject, final_full_msg, EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['sender_password'], EMAIL_CONFIG['receiver_email'])
        
        if NOTIFY_CONFIG.get('telegram', True):
            send_telegram(TELEGRAM_CONFIG['bot_token'], TELEGRAM_CONFIG['chat_id'], final_full_msg)

        logging.info("所有任务执行完毕")

    except Exception as e:
        error_msg = f"签到程序执行出错：{str(e)}"
        logging.error(error_msg)
        
        # 发送错误通知
        if NOTIFY_CONFIG.get('email', True):
            send_email(
                subject="GLaDOS 签到失败通知",
                content=error_msg,
                sender_email=EMAIL_CONFIG['sender_email'],
                sender_password=EMAIL_CONFIG['sender_password'],
                receiver_email=EMAIL_CONFIG['receiver_email']
            )
        
        if NOTIFY_CONFIG.get('telegram', True):
            send_telegram(
                bot_token=TELEGRAM_CONFIG['bot_token'],
                chat_id=TELEGRAM_CONFIG['chat_id'],
                message=f"❌ {error_msg}"
            )

