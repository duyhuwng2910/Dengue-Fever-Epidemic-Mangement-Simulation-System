import pandas as pd
import time
import pyodbc
import os
import numpy as np

medical_data_folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Data', 'Public data', 'Medical data')


def change_file_format():
    dengue_fever_report_file_path = os.path.join(medical_data_folder_path, 'Số liệu dịch bệnh SXH theo thời gian.xlsx')
    
    df = pd.read_excel(dengue_fever_report_file_path, header=0)

    # print(df.dtypes)
    
    # print(df)

    df['ngày bắt đầu'] = pd.to_datetime(df['ngày bắt đầu'], errors='coerce')
    df['ngày kết thúc'] = pd.to_datetime(df['ngày kết thúc'], errors='coerce')
    
    # Các cột cần chuyển đổi kiểu dữ liệu
    columns_to_convert = ['tháng', 'tuần', 'số ca nhiễm bệnh', 'số ca ghi nhận tại bệnh viện', 'số ca tử vong']

    # Chuyển đổi kiểu dữ liệu của các cột
    df[columns_to_convert] = df[columns_to_convert].astype('Int64')    

    # print(df.dtypes)
    
    # print(df)

    df.to_csv(os.path.join(medical_data_folder_path, 'Số liệu dịch bệnh SXH theo thời gian.csv'), index=False, encoding='utf-8-sig')
    
    print("Chuyển định dạng file chứa thông tin báo cáo dịnh bệnh sốt xuất huyết theo thời gian thành công!")
    

def import_dengue_fever_report_data():
    connection = pyodbc.connect('DRIVER={SQL Server};'
                                'SERVER=DUYHUNGNGUYEN;'
                                'DATABASE=dengue_fever_epidemic_management_simulation_system;'
                                'Trusted_Connection=yes;')
    
    dengue_fever_report_data = pd.read_csv(os.path.join(medical_data_folder_path, 'Số liệu dịch bệnh SXH theo thời gian.csv'),
                                           encoding='utf-8',
                                           header=0)

    df = pd.DataFrame(dengue_fever_report_data)

    df['ngày bắt đầu'] = pd.to_datetime(df['ngày bắt đầu'], errors='coerce')
    df['ngày kết thúc'] = pd.to_datetime(df['ngày kết thúc'], errors='coerce')
    
    # Các cột cần chuyển đổi kiểu dữ liệu
    columns_to_convert = ['tháng', 'tuần', 'số ca nhiễm bệnh', 'số ca ghi nhận tại bệnh viện', 'số ca tử vong']

    # Chuyển đổi kiểu dữ liệu của các cột
    df[columns_to_convert] = df[columns_to_convert].astype('Int64')

    # Thay thế <NA> bằng None
    df.replace('<NA>', None, inplace=True)
    
    df[columns_to_convert] = np.where(df[columns_to_convert].isna(), None, df[columns_to_convert])

    print(df.dtypes)
    
    print(df)
    
    cursor = connection.cursor()
    
    print("Tiến hành nhập dữ liệu")
    
    try:
        cursor.execute('TRUNCATE TABLE dengue_fever_report;')
        
        for row in df.itertuples(index=False):
            year = row[0]
            month = row[1]
            week = row[2]
            start_date = row[3]
            end_date = row[4]
            number_of_cases = row[5]
            number_of_hospitalized_cases = row[6]
            number_of_deaths = row[7]
            
            cursor.execute('''
                           INSERT INTO dengue_fever_report (year,month,week,start_date,end_date,number_of_cases,number_of_hospitalized_cases,number_of_deaths)
                           VALUES (?,?,?,?,?,?,?,?)
                           ''',
                           year,
                           month,
                           week,
                           start_date,
                           end_date,
                           number_of_cases,
                           number_of_hospitalized_cases,
                           number_of_deaths)
            
        cursor.commit()
        
        time.sleep(1)
        
        print("Nhập dữ liệu về báo cáo dịch bệnh sốt xuất huyết lên cơ sở dữ liệu thành công!")
        
    except Exception as e:
        print(f"Xuất hiện lỗi sau: {e}")

    finally:
        connection.close()            
    

change_file_format()
time.sleep(1)
import_dengue_fever_report_data()