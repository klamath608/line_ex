#這是台股上市股票除權息預告

import requests
import pandas as pd
import io
from io import StringIO
import csv
#from tabulate import tabulate
from datetime import date
from pathlib import Path

#----------------------------------------------------------------------------------------------------
def stock_info():
    today = date.today()
    today1=str(today).replace("-","")
    #print(today1)    
    today1="20250613"
    global df
    url=f'https://www.twse.com.tw/exchangeReport/BWIBBU_d?response=csv&date={today1}&selectType=ALL'
    headers={'User-Agent':'Mozilla/5.0'}
    response=requests.get(url, headers=headers)
    df=pd.read_csv(StringIO(response.text),header=1)
    
    #display(df)
    #header=1 代表讀第二列 因為第一列是標題 不是欄位
    #print(df.columns)看欄位名稱
    #print(df.head(10))
    return df
#-----------------------------------------------------------------------------------------------------
url1 = "https://www.twse.com.tw/exchangeReport/TWT48U?response=csv"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
}
response = requests.get(url1, headers=headers)
df=pd.read_csv(StringIO(response.text),header=1)
#print(df)
df1=df[["股票代號","名稱","除權除息日期"]].copy()  
#print(df1)

def convert_roc_date(roc_date_str):
    try:
        roc_date_str = str(roc_date_str).strip()
        if not roc_date_str or "年" not in roc_date_str:
            return pd.NaT  # 回傳空日期
        y, m, d = roc_date_str.replace("年", "-").replace("月", "-").replace("日", "").split("-")
        y = int(y) + 1911
        return pd.Timestamp(f"{y}-{m}-{d}")
    except Exception as e:
        print(f"無法轉換日期：{roc_date_str}，錯誤：{e}")
        return pd.NaT

# 新增一欄轉換後的 datetime
df1["西元日期"] = df1["除權除息日期"].apply(convert_roc_date)



#股票代號資料清洗
df1["股票代號"] = df1["股票代號"].str.strip().str.replace(r"=", "", regex=True)
df1["股票代號"] = df1["股票代號"].str.strip().str.replace(r'"', '', regex=True)
#print(df1)

#導入股價/殖利率資料
df_infor =stock_info()
#轉成字串
df_infor["證券代號"] = df_infor["證券代號"].astype(str)
#print(df_infor)

#轉換資料型態
df1["股票代號"] = df1["股票代號"].astype(str)

#合併df資料
#合併時指定左右欄位名稱
df_all = pd.merge(df_infor, df1, left_on='證券代號', right_on='股票代號', how='right')
#print(df_all)

#取需要的欄位
merged=df_all[["股票代號", "名稱", "收盤價", "本益比", "殖利率(%)","除權除息日期","西元日期"]].copy()
#print(merged)

# 取前50筆
#df_top50 = merged.head(50)

# 排序
df_sorted = merged.sort_values("西元日期")
#print("列數:", len(df_sorted))
#print(df_sorted.head(50))
#-------------------------------------------------------------
# 產生 HTML 並寫入 docs/report.html
html_path = Path("docs/report.html")
html_path.parent.mkdir(parents=True, exist_ok=True)

# ⚠️ 注意這段需放在產出 df 的後面
html = df_sorted.to_html(index=False, classes='styled-table')

# 寫入 HTML 檔案
with open("docs/report.html", "w", encoding="utf-8") as f:
    f.write(f"""
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>台股除權息報表</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            padding: 16px;
            background-color: #fefefe;
        }}
        .table-wrapper {{
            overflow-x: auto;
        }}
        table {{
            width: 100%;
            table-layout: auto; /* 根據內容調整欄寬 */
            border-collapse: collapse;
            font-size: 15px;
        }}
        th, td {{
            text-align: center;
            padding: 8px 12px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        th {{
            background-color: #4CAF50;
            color: white;
        }}
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}

        @media (max-width: 600px) {{
            table {{
                font-size: 14px;
            }}
            th, td {{
                padding: 6px 8px;
            }}
        }}
    </style>
</head>
<body>
    <h2>📈 除權息預告表</h2>
    <div class="table-wrapper">
        {html}
    </div>
</body>
</html>
""")


#--------------------------------------------
# 用 tabulate 格式化輸出
#table_str = tabulate(df_sorted, headers='keys', tablefmt='pretty', showindex=False)
#print(table_str)

#--------------------------------------------------------------------------------------
"""
import os

# 確保 reports 目錄存在
os.makedirs("reports", exist_ok=True)

#假設 df_sorted 是你排序後的 DataFrame
excel_path = "reports/dividend_report.xlsx"

# 寫入 Excel，不含索引欄
df_sorted.to_excel(excel_path, index=False)

print(f"已成功寫入 Excel 檔案：{excel_path}")
"""
#-----------------------------------------------------------
