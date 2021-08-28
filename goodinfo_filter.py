import os
import sys
import json
from time import time
import pandas as pd
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
from line_notify import sendline
# from matplotlib_table import dataframe2image
sys.path.append('D:\General')
from mysql import MySQL
import setting



####################################################################################################
#                                             Setting                                              #
####################################################################################################



####################################################################################################
#                                             Variable                                             #
####################################################################################################
NOW = datetime.now()
CLOSE_TIME = NOW.replace(hour=15, minute=0, second=0, microsecond=0)
# 若執行當前時間，股市尚未收盤，結束程式
if NOW < CLOSE_TIME:
    os._exit(0)

TODAY = datetime.strftime(NOW, '%Y%m%d')
YEAR = TODAY[:4]
BASE_DIR = r'D:/Project/PyStock/'

# Load Config
with open(f'{BASE_DIR}/config.json', 'r') as j:
    config = json.load(j)
# GoodInfo
URL = config['GOODINFO']['URL']
COOKIE = config['GOODINFO']['COOKIE']
# Line
LINE = config['LINE']
# MySQL
SERVER = config['MYSQL']['SERVER']
PORT = config['MYSQL']['PORT']
DATABASE = config['MYSQL']['DATABASE']
USER = config['MYSQL']['USER']
PASSWORD = config['MYSQL']['PASSWORD']

# Record File
RECORD_DIR = f'{BASE_DIR}/record/'
if not os.path.exists(RECORD_DIR):
    os.makedirs(RECORD_DIR)
RECORD_FILE = f'{RECORD_DIR}/{YEAR}_record.csv'

# Master File
MASTER_DIR = f'{BASE_DIR}/master/'
if not os.path.exists(f'{MASTER_DIR}/{YEAR}/'):
    os.makedirs(f'{MASTER_DIR}/{YEAR}/')
MASTER_FILE = f'{MASTER_DIR}/{YEAR}/{TODAY}_target.csv'



####################################################################################################
#                                             Function                                             #
####################################################################################################
def create_record(record_file: str=RECORD_FILE, date: str=TODAY, status: str=''):
# record_file=RECORD_FILE, date=TODAY, status=''
    """Create record file

    Args:
        record_file (str): Path of record file
        date (str): Today
        status (str): What status of today
    """

    if not os.path.exists(record_file):
        with open(record_file, 'w') as fw:
            fw.writelines('Date,Status')
    
    df_record = pd.read_csv(record_file, encoding='utf-8')
    df_record['Date'] = df_record['Date'].astype(str)
    if TODAY in df_record['Date'].unique():
        df_record.loc[df_record['Date'] == TODAY, 'Status'] = status
    else:
        df_record = df_record.append(pd.DataFrame({'Date': [TODAY], 'Status': [status]}))
    df_record.to_csv(record_file, index=False, encoding='utf-8-sig')



####################################################################################################
#                                               Main                                               #
####################################################################################################
try:
    # requests
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
    cookies = {'cookie': COOKIE}
    r = requests.get(url=URL, headers=headers, cookies=cookies)
    r.encoding ='utf-8'

    # BeautifulSoup
    soup = BeautifulSoup(r.text, 'lxml')
    data = soup.select_one('#tblStockList')

    if data:
        df = pd.read_html(data.prettify())[0]
        # Rename Columns
        dict_rename = {
            '代號': '股票代號', '名稱': '股票名稱', '成交': '成交價', 
            '漲跌  價': '漲跌價', '漲跌  幅': '漲跌幅', '月  均線  乖離率': '月均線乖離率',
        }
        df = df.rename(columns=dict_rename)
        # Adjust Data
        df['日期'] = f'{TODAY[:4]}-{TODAY[4:6]}-{TODAY[6:]}'
        df['月均線乖離率'] = df['月均線乖離率'].str[1:-1]
        # 欄位型態為 numpy.int32 或 numpy.int64 時，會無法匯入!!!
        for col in df.columns:
            df[col] = df[col].astype(object)

        ### To csv
        df.to_csv(MASTER_FILE, index=False, encoding='utf-8-sig')

        ### To MySQL
        mysql = MySQL(server=SERVER, port=PORT, database=DATABASE, user=USER, password=PASSWORD)
        # Check MySQL, If today's data exist in database, then delete.
        query = f"DELETE FROM stock.goodinfo_filter WHERE `日期` = '{TODAY[:4]}-{TODAY[4:6]}-{TODAY[6:]}'"
        mysql.executeMySQL(query=query)
        # Insert Today's Data
        mysql.dataframe2mysql(df=df, table='stock.goodinfo_filter')

        ### Log
        create_record(status='Target get')

        ### Send Line
        for idx in df.index:
            message = f'\n{idx+1}.\n'
            for col in df.columns:
                message += f'{col}: {df.loc[idx, col]}\n'
            message += '-'*25
            sendline(line=LINE, message=message)

    else:
        # Log
        create_record(status='No Target')

except:
    # Log
    create_record(status='Error')
