import pandas as pd
import os
os.chdir(r'D:\UKWhisky_pro\data')

def merge_multiple_excel_files(years, output_file):
    # 初始化一个空的数据框
    merged_df = pd.DataFrame()

    # 遍历年份列表，合并数据
    for year in years:
        file_name = f'./whiskey_info{year}.xlsx'

        try:
            # 读取文件并合并到数据框
            df = pd.read_excel(file_name)
            df['origin'] = df['origin'].str.replace(' ', '')
            merged_df = pd.concat([merged_df, df], ignore_index=True)
            print(f'Successfully merged data for {year}.')
        except FileNotFoundError:
            print(f'File {file_name} not found. Skipping...')

    # 保存到新文件
    merged_df.to_excel(output_file, index=False)
    print(f'Merged data saved to {output_file}.')


# 使用示例
years_to_merge = ['2023','2022','2021','2020','2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010', '2009', '2008', '2007', '2006',
         '2005', '2004', '2003', '2002', '2001', '2000', '1999', '1998', '1997', '1996', '1995', '1994', '1993', '1992',
         '1991', '1990', '1989', '1988', '1987', '1986', '1985', '1984', '1983', '1982', '1981', '1980', '1979', '1978',
         '1977', '1976', '1975', '1974', '1973', '1972', '1971', '1970', '1969', '1968', '1967', '1966', '1965', '1964',
         '1963', '1962', '1961', '1960', '1959', '1958', '1957', '1956', '1955', '1954', '1953', '1952', '1951', '1950',
         '1949', '1948', '1947', '1946', '1945', '1943', '1941', '1940', '1939', '1938', '1937', '1936', '1935', '1933',
         '1930', '1929', '1928', '1926', '1924', '1921', '1919', '1914', '1907', '1906', '1904', '1900', '1899', '1898',
         '1894', '1891', '1889', '1887', '1883', '1881', '1879', '1877', '1876', '1874', '1872', '1871', '1870', '1867',
         '1866', '1865', '1861', '1841', '1836', '1826']

merge_multiple_excel_files(years_to_merge, 'merged_whiskey_info.xlsx')
