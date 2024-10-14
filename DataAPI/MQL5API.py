import time
from datetime import datetime

import baostock as bs
import pytz
import numpy as np
import pandas as pd

from Common.CEnum import AUTYPE, DATA_FIELD, KL_TYPE
from Common.CTime import CTime
from Common.func_util import kltype_lt_day, str2float
from KLine.KLine_Unit import CKLine_Unit

from .CommonStockAPI import CCommonStockApi
import MetaTrader5 as mt5


def create_item_dict(data, column_name):
    for i in range(len(data)):
        data[i] = parse_time(data[i]) if i == 0 else str2float(data[i])
    return dict(zip(column_name, data))


def parse_time(time):
    dt = pd.to_datetime(time, unit='s')
    return CTime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, auto=False)


def parse_time_column(inp):
    # if inp is None:
    #     return CTime()
    # 20210902113000000
    # 2021-09-13
    if len(inp) == 10:
        year = int(inp[:4])
        month = int(inp[5:7])
        day = int(inp[8:10])
        hour = minute = 0
    elif len(inp) == 17:
        year = int(inp[:4])
        month = int(inp[4:6])
        day = int(inp[6:8])
        hour = int(inp[8:10])
        minute = int(inp[10:12])
    elif len(inp) == 19:
        year = int(inp[:4])
        month = int(inp[5:7])
        day = int(inp[8:10])
        hour = int(inp[11:13])
        minute = int(inp[14:16])
    else:
        raise Exception(f"unknown time column from baostock:{inp}")
    return CTime(year, month, day, hour, minute)


def GetColumnNameFromFieldList(fileds: str):
    _dict = {
        "time": DATA_FIELD.FIELD_TIME,
        "date": DATA_FIELD.FIELD_TIME,
        "open": DATA_FIELD.FIELD_OPEN,
        "high": DATA_FIELD.FIELD_HIGH,
        "low": DATA_FIELD.FIELD_LOW,
        "close": DATA_FIELD.FIELD_CLOSE,
        "volume": DATA_FIELD.FIELD_VOLUME,
    }
    return [_dict[x] for x in fileds.split(",")]


class CMQL5(CCommonStockApi):
    is_connect = None

    def __init__(self, code, k_type=KL_TYPE.K_DAY, begin_date=None, end_date=None, autype=None):
        super(CMQL5, self).__init__(code, k_type, begin_date, end_date, autype)

    def get_kl_data(self):
        fields = "time,open,high,low,close,volume"

        begin = parse_time_column(self.begin_date)
        end = parse_time_column(self.end_date)
        timezone = pytz.timezone("Etc/UTC")
        utc_from = datetime(begin.year, begin.month, begin.day, begin.hour, begin.minute, tzinfo=timezone)
        utc_to = datetime(end.year, end.month, end.day, end.hour, end.minute, tzinfo=timezone)

        rates = mt5.copy_rates_range(self.code, self.__convert_type(), utc_from, utc_to)

        ckus = []
        for rs in rates:
            field_list = GetColumnNameFromFieldList(fields)
            data = [rs[0], rs[1], rs[2], rs[3], rs[4], rs[5]]
            item_dict = create_item_dict(data, field_list)
            ckus.append(CKLine_Unit(item_dict))

        return ckus

    def SetBasciInfo(self):
        # rs = bs.query_stock_basic(code=self.code)
        # if rs.error_code != '0':
        #     raise Exception(rs.error_msg)
        # code, code_name, ipoDate, outDate, stock_type, status = rs.get_row_data()
        # self.name = code_name
        # self.is_stock = (stock_type == '1')
        None

    @classmethod
    def do_init(cls):
        if not cls.is_connect:
            cls.is_connect = mt5.initialize()
            # print(mt5.terminal_info())
            # 获取有关MetaTrader 5版本的数据
            # print(mt5.version())

    @classmethod
    def do_close(cls):
        if cls.is_connect:
            mt5.shutdown()
            cls.is_connect = None

    def __convert_type(self):
        _dict = {
            KL_TYPE.K_DAY: mt5.TIMEFRAME_D1,
            KL_TYPE.K_WEEK: mt5.TIMEFRAME_W1,
            KL_TYPE.K_MON: mt5.TIMEFRAME_M1,
            KL_TYPE.K_5M: mt5.TIMEFRAME_M5,
            KL_TYPE.K_15M: mt5.TIMEFRAME_M15,
            KL_TYPE.K_30M: mt5.TIMEFRAME_M30,
            KL_TYPE.K_H1: mt5.TIMEFRAME_H1,
            KL_TYPE.K_H4: mt5.TIMEFRAME_H4,
            KL_TYPE.K_H12: mt5.TIMEFRAME_H12,
        }
        return _dict[self.k_type]
