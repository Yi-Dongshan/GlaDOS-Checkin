# 修复导入错误：jsonp -> json
import io
import json  # 这里改正了 jsonp 为 json
import time
import requests
import logging
from datetime import timedelta, date
from config import headers, EMAIL_CONFIG
import zstandard as zstd
from email_sender import send_email

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
        start_time = time.time()
        res = checkin(headers)
        
        checkin_result = res['message']
        points_balance = res['list'][0]['balance'].split('.')[0]
        change = res['list'][0]['change'].split('.')[0]
        
        leftdays = get_leftdays(headers)
        time_taken = time.time() - start_time
        exp_date = calculate_expiration_date(int(leftdays))
        
        msg = (
            f"📬 GLaDOS 签到结果\n"
            f"✅ 状态：{checkin_result}\n"
            f"🕐 用时：{time_taken:.2f}s\n"
            f"🧧 积分余额：{points_balance}(+{change})\n"
            f"⏳ 剩余会员：{leftdays} 天（到期时间：{exp_date}）"
        )
        
        # 发送邮件通知
        if send_email(
            subject="GLaDOS 每日签到通知",
            content=msg,
            sender_email=EMAIL_CONFIG['sender_email'],
            sender_password=EMAIL_CONFIG['sender_password'],
            receiver_email=EMAIL_CONFIG['receiver_email']
        ):
            logging.info("邮件发送成功")
        else:
            logging.error("邮件发送失败")
            
        logging.info(msg)
        
    except Exception as e:
        error_msg = f"签到程序执行出错：{str(e)}"
        logging.error(error_msg)
        # 发送错误通知
        send_email(
            subject="GLaDOS 签到失败通知",
            content=error_msg,
            sender_email=EMAIL_CONFIG['sender_email'],
            sender_password=EMAIL_CONFIG['sender_password'],
            receiver_email=EMAIL_CONFIG['receiver_email']
        )

