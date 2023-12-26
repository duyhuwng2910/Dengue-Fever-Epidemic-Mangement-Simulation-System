import requests
import pandas as pd
import csv
import os
from datetime import datetime
import time
import pyodbc

# API key để lấy dữ liệu từ trang web openweathermap.org
api_key="88ec58173d2be009908c974b114bb0f8"

weather_data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Data', 'Public data', 'Weather data')

vietnam_provinces_coordinate_file_path = os.path.join(weather_data_folder, 'vietnam_provinces_coordinate.csv')

present_day = datetime.now().strftime("%Y-%m-%d")


'''
Hàm lấy dữ liệu về thời tiết trong ngày của toàn bộ các tỉnh thành và cập nhật vào file csv
'''
def update_weather_data():
    coordinate_df = pd.read_csv(vietnam_provinces_coordinate_file_path)

    vietnam_provinces = coordinate_df['name'].tolist()
    vietnam_provinces_latitude = coordinate_df['latitude'].tolist()
    vietnam_provinces_longitude = coordinate_df['longitude'].tolist()

    weather_information = []

    max_retries = 3
    
    for i in range(len(vietnam_provinces)):
        for j in range(max_retries):
            try:
                current_weather_api_call = f"https://api.openweathermap.org/data/2.5/weather?lat={vietnam_provinces_latitude[i]}&lon={vietnam_provinces_longitude[i]}&appid={api_key}&units=metric&lang=vi"
                
                daily_aggregation_weather_api_call = f"https://api.openweathermap.org/data/3.0/onecall/day_summary?lat={vietnam_provinces_latitude[i]}&lon={vietnam_provinces_longitude[i]}&date={present_day}&appid={api_key}&units=metric&lang=vi"
                
                current_weather_api_call_response = requests.get(current_weather_api_call)

                daily_aggregation_weather_api_call_response = requests.get(daily_aggregation_weather_api_call)
                
                if current_weather_api_call_response.status_code == 200 and daily_aggregation_weather_api_call_response.status_code == 200:
                    current_weather_data = current_weather_api_call_response.json()
                    
                    daily_aggregation_weather_api_call_data = daily_aggregation_weather_api_call_response.json()
                    
                    weather_information.append(
                        [
                            present_day,
                            vietnam_provinces[i],
                            current_weather_data['weather'][0]['main'],
                            current_weather_data['weather'][0]['description'],
                            current_weather_data['main']['temp'],
                            current_weather_data['main']['feels_like'],
                            daily_aggregation_weather_api_call_data['temperature']['min'],
                            daily_aggregation_weather_api_call_data['temperature']['max'],
                            current_weather_data['main']['humidity']
                        ]
                    )
                        
                    break  # Nếu thành công, thoát khỏi vòng lặp
            
            except requests.exceptions.RequestException as e:
                print(f"Attempt {i + 1} failed. Error: {e}")

    daily_weather_by_city_file_path = os.path.join(weather_data_folder,'daily_weather_by_city.csv')

    with open(daily_weather_by_city_file_path, mode="a", newline='', encoding='utf-8') as csv_file:
        # Tạo đối tượng writer từ thư viện csv
        writer = csv.writer(csv_file)

        # Kiểm tra xem file đã tồn tại hay chưa
        # Nếu không tồn tại, viết dòng tiêu đề vào file
        if csv_file.tell() == 0:
            writer.writerow(["Ngày", "Tỉnh/Thành phố", "Thời tiết", "Mô tả", "Nhiệt độ (°C)", "Nhiệt độ cảm nhận (°C)", "Nhiệt độ thấp nhất(°C)", "Nhiệt độ cao nhất(°C)", "Độ ẩm (%)"])

        # Ghi dữ liệu vào cuối file
        writer.writerows(weather_information)

    print(f"Dữ liệu về thời tiết trên cả nước trong ngày {datetime.now().strftime("%d-%m-%Y")} đã được ghi tiếp vào file CSV: {daily_weather_by_city_file_path}")
    
'''
Hàm nhập dữ liệu về thời tiết trong ngày từ file csv (Trong trường hợp clone repo về)
'''
def import_weather_data_from_csv_file():
    weather_data = pd.read_csv(os.path.join(weather_data_folder, 'daily_weather_by_city.csv'))
    
    df = pd.DataFrame(weather_data)
    
    df['Ngày'] = pd.to_datetime(df['Ngày'], errors='coerce')

    # Tạo biến kết nối đến database trong SQL Server
    connection = pyodbc.connect('DRIVER={SQL Server};'
                                    'SERVER=DUYHUNGNGUYEN;'
                                    'DATABASE=dengue_fever_epidemic_management_simulation_system;'
                                    'Trusted_Connection=yes;')

    cursor = connection.cursor()
    
    try:
        cursor.execute('TRUNCATE TABLE daily_weather_by_city;')
        
        for row in df.itertuples():
            date = row[1]
            province = row[2]
            weather = row[3]
            description = row[4]
            temp = row[5]
            feels_like = row[6]
            min_temp = row[7]
            max_temp = row[8]
            humidity = row[9]
            
            cursor.execute('''
                        INSERT INTO daily_weather_by_city (date, [city/province], weather, description, [temp(°C)], [feels_like(°C)], [min_temp(°C)], [max_temp(°C)], [humidity(%)])
                        VALUES (?,?,?,?,?,?,?,?,?)
                        ''',
                        date,
                        province,
                        weather,
                        description,
                        temp,
                        feels_like,
                        min_temp,
                        max_temp,
                        humidity)
            
        cursor.commit()
        
        print(f"Cập nhật dữ liệu về thời tiết trong ngày {datetime.now().strftime('%d-%m-%Y')} lên cơ sở dữ liệu thành công!")
        
    except Exception as e:
        # rollback nếu có lỗi
        connection.rollback()
        
        print(f"Xuất hiện lỗi sau: {e}")
        
    finally:
        connection.close()

'''
Hàm nhập dữ liệu về thời tiết trong ngày từ dataframe.
Trong trường hợp đã có dữ liệu sẵn trong SQL Server, thì nên dùng hàm này
để tối ưu thời gian thực hiện truy vấn, do hàm này chỉ nhập thêm dữ liệu của
ngày hiện tại
'''
def import_weather_data_from_data_frame():
    coordinate_df = pd.read_csv(vietnam_provinces_coordinate_file_path)

    vietnam_provinces = coordinate_df['name'].tolist()
    vietnam_provinces_latitude = coordinate_df['latitude'].tolist()
    vietnam_provinces_longitude = coordinate_df['longitude'].tolist()

    weather_information_df = pd.DataFrame(columns=['date','province','weather','description','temp','feels_like','min_temp','max_temp','humidity'])
    
    max_retries = 3
    
    for i in range(len(vietnam_provinces)):
        for j in range(max_retries):
            try:
                current_weather_api_call = f"https://api.openweathermap.org/data/2.5/weather?lat={vietnam_provinces_latitude[i]}&lon={vietnam_provinces_longitude[i]}&appid={api_key}&units=metric&lang=vi"
                
                daily_aggregation_weather_api_call = f"https://api.openweathermap.org/data/3.0/onecall/day_summary?lat={vietnam_provinces_latitude[i]}&lon={vietnam_provinces_longitude[i]}&date={datetime.now().strftime("%Y-%m-%d")}&appid={api_key}&units=metric&lang=vi"
                
                current_weather_api_call_response = requests.get(current_weather_api_call)

                daily_aggregation_weather_api_call_response = requests.get(daily_aggregation_weather_api_call)
                
                if current_weather_api_call_response.status_code == 200 and daily_aggregation_weather_api_call_response.status_code == 200:
                    current_weather_data = current_weather_api_call_response.json()
                    
                    daily_aggregation_weather_api_call_data = daily_aggregation_weather_api_call_response.json()
                    
                    weather_information_df.loc[len(weather_information_df.index)] = [present_day,vietnam_provinces[i], \
                                                                                    current_weather_data['weather'][0]['main'], \
                                                                                    current_weather_data['weather'][0]['description'], \
                                                                                    current_weather_data['main']['temp'], \
                                                                                    current_weather_data['main']['feels_like'], \
                                                                                    daily_aggregation_weather_api_call_data['temperature']['min'], \
                                                                                    daily_aggregation_weather_api_call_data['temperature']['max'], \
                                                                                    current_weather_data['main']['humidity']]
                        
                    break  # Nếu thành công, thoát khỏi vòng lặp
            
            except requests.exceptions.RequestException as e:
                print(f"Attempt {i + 1} failed. Error: {e}")

    print(weather_information_df)
    
    # Tạo biến kết nối đến database trong SQL Server
    connection = pyodbc.connect('DRIVER={SQL Server};'
                                    'SERVER=DUYHUNGNGUYEN;'
                                    'DATABASE=dengue_fever_epidemic_management_simulation_system;'
                                    'Trusted_Connection=yes;')

    cursor = connection.cursor()
    
    try:
        for row in weather_information_df.itertuples():
            date = row[1]
            province = row[2]
            weather = row[3]
            description = row[4]
            temp = row[5]
            feels_like = row[6]
            min_temp = row[7]
            max_temp = row[8]
            humidity = row[9]
            
            cursor.execute('''
                        INSERT INTO daily_weather_by_city (date, [city/province], weather, description, [temp(°C)], [feels_like(°C)], [min_temp(°C)], [max_temp(°C)], [humidity(%)])
                        VALUES (?,?,?,?,?,?,?,?,?)
                        ''',
                        date,
                        province,
                        weather,
                        description,
                        temp,
                        feels_like,
                        min_temp,
                        max_temp,
                        humidity)
            
        cursor.commit()
        
        print(f"Cập nhật dữ liệu về thời tiết trong ngày {datetime.now().strftime('%d-%m-%Y')} lên cơ sở dữ liệu thành công!")
        
    except Exception as e:
        # rollback nếu có lỗi
        connection.rollback()
        
        print(f"Xuất hiện lỗi sau: {e}")
        
    finally:
        connection.close()

update_weather_data()
time.sleep(1)
import_weather_data_from_csv_file()
# time.sleep(1)
# import_weather_data_from_data_frame()