import pandas as pd
import os
os.chdir(r'D:\UKWhisky_pro\data')
filtered_excel_file_path = r'D:\UKWhisky_pro\filtered_whisky_data.xlsx'  # 绝对路径

# 读取Excel文件
excel_file_path = './merged_whiskey_info.xlsx'
df = pd.read_excel(excel_file_path)

# 继续筛选操作
filtered_df = df[df['name'].str.lower().str.contains('whisky')]

# 筛选第一列为 'name' 的数据
filtered_df = df[df['name'].str.lower().str.contains('whisky')]

# 保存筛选后的数据到新的Excel文件
filtered_df.to_excel(filtered_excel_file_path, index=False)
print(f"Filtered data has been saved to {filtered_excel_file_path}")
print("筛选后的行数：", len(filtered_df))