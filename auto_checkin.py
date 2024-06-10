import json
import time
import requests
import logging
from datetime import timedelta, date
from plyer import notification
from config import headers

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler("log/checkin.log", encoding='utf-8'),  # 写入日志文件
        # logging.StreamHandler()  # 同时打印到控制台
    ]
)

def checkin(headers):
    checkin_url = "https://glados.one/api/user/checkin"
    payload = {
        'token': 'glados.one'
    }
    try:
        response = requests.post(checkin_url,
                                 headers=headers,
                                 data=json.dumps(payload))
        checkin_result = response.json()['message']
        # logging.info(f"签到成功，结果：{checkin_result}")
        # print(f"{response.json()['message']}")

        # 签到成功，获取余额和积分
        if response.json()['code'] == 1:
            balance = response.json()['list'][0]['balance'].split('.')[0]
            change = response.json()['list'][0]['change'].split('.')[0]
            # print(f"本次签到获得 {change} 分，累计获得 {balance:>2} 分")
            return checkin_result, balance, change

    except Exception as e:
        logging.error(f"签到失败：{e}")
    return None


# 获取账号信息
def get_status(headers):
    url = "https://glados.one/api/user/status"
    referer = 'https://glados.one/console/checkin'
    origin = "https://glados.one"
    useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
    try:
        response = requests.get(url, headers={
            'cookie': headers['Cookie'],
            'referer': referer,
            'origin': origin,
            'user-agent': useragent})
        # print(response.text)
        mail = response.json()['data']['email']
        leftdays = response.json()['data']['leftDays'].split('.')[0]
        # print(f"{mail:>2} 会员有效期剩余 {leftdays} 天，预计 {calculate_expiration_date(int(leftdays))} 到期")
        return leftdays
    except Exception as e:
        print(f"ERROR：{e}")
    return None


def send_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        app_name='GLaDOS签到通知',
        app_icon=None,  # 可以设置为你的应用图标
        timeout=10,  # 通知显示的时间，单位为秒
        toast=True
    )


def calculate_expiration_date(remaining_days):
    # 获取今天的日期
    current_date = date.today()
    # 计算到期日
    expiration_date = current_date + timedelta(days=remaining_days)
    # 返回到期日的字符串表示
    return expiration_date.strftime('%Y-%m-%d')


if __name__ == '__main__':
    start_time = time.time()

    # 签到
    checkin_result, points_balance, change = checkin(headers)

    # 获取状态
    leftdays = get_status(headers)

    time_taken = time.time() - start_time

    exp_date = calculate_expiration_date(int(leftdays))

    # 发送通知
    msg = (f"签到结果：{checkin_result}\n"
           f"签到用时：{time_taken:.2f} 秒\n"
           "----------------------------------------"
           "\n\t积分\t会员\n"
           f"余额\t{points_balance}(+{change})\t{leftdays}( {exp_date} 到期)"
           )
    
    logging.info('\n'+msg)  # 记录运行结束日志

    send_notification(title=' ', message=msg)


