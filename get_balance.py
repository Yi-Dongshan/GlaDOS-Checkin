import requests
from collections import defaultdict
from config import headers


def get_balance(headers):
    requests.get('https://glados.one/console/income',headers)
    url = "https://glados.one/api/user/balance"

    try:
        response = requests.get(url, headers=headers)
        # print(response.text)
        balance = response.json()['data']
        return balance
    except Exception as e:
        print(f"ERROR：{e}")
    return None


def find_latest_records(records):
    """
    根据给定的记录列表，找到每种asset的最新记录。

    :param records: 包含记录的列表，每个记录是一个字典，包含'asset', 'time', 'id', 'change', 'balance', 'detail'等键。
    :return: 一个字典，包含每种asset的最新记录。
    """
    latest_records = defaultdict(lambda: {
        "id": None,
        "time": None,
        "change": None,
        "balance": None,
        "detail": None
    })

    for record in records:
        asset = record["asset"]
        # 如果这是该asset的第一个记录，或者当前记录的时间戳大于latest_records中该asset的时间戳，则更新记录
        if (record["time"] > latest_records[asset]["time"] if latest_records[asset]["time"] is not None else True):
            latest_records[asset] = record

    return latest_records


if __name__ == '__main__':
    records_list = get_balance(headers)
    balance = find_latest_records(records_list)

    msg = (f"\tUSDT\t积分\t会员\n"
        f"余额\t{1}\t{2}\t{4}")
    print(msg.format(balance['usdt']['balance'],balance['points']['balance'],balance['ss-1']['balance']))
