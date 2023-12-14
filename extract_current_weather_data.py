import requests
import pandas as pd
import csv
from datetime import datetime

api_key="88ec58173d2be009908c974b114bb0f8"

vietnam_provinces_coordinate_file_path = "vietnam_provinces_coordinate.csv"

df = pd.read_csv(vietnam_provinces_coordinate_file_path)

vietnam_provinces = df['city_name'].tolist()
vietnam_provinces_latitude = df['latitude'].tolist()
vietnam_provinces_longitude = df['longitude'].tolist()

weather_information = []

for i in range(len(vietnam_provinces)):
    weather_api_call = f"https://api.openweathermap.org/data/2.5/weather?lat={vietnam_provinces_latitude[i]}&lon={vietnam_provinces_longitude[i]}&appid={api_key}&units=metric&lang=vi"

    response = requests.get(weather_api_call)

    if response.status_code == 200:
        data = response.json()
        
        weather_information.append(
            [
                datetime.now().strftime("%d-%m-%Y"),
                vietnam_provinces[i],
                data['weather'][0]['main'],
                data['weather'][0]['description'],
                data['main']['temp'],
                data['main']['temp_min'],
                data['main']['temp_max'],
                data['main']['humidity']
            ]
        )    
    
#print(weather_information)

daily_weather_data_by_city_file_path = "daily_weather_data_by_city.csv"

with open(daily_weather_data_by_city_file_path, mode="a", newline='', encoding='utf-8') as csv_file:
    # Tạo đối tượng writer từ thư viện csv
    writer = csv.writer(csv_file)

    # Kiểm tra xem file đã tồn tại hay chưa
    # Nếu không tồn tại, viết dòng tiêu đề vào file
    if csv_file.tell() == 0:
        writer.writerow(["Ngày", "Tỉnh/Thành phố", "Thời tiết", "Mô tả", "Nhiệt độ (°C)", "Nhiệt độ cao nhất (°C)", "Nhiệt độ thấp nhất (°C)", "Độ ẩm (%)"])

    # Ghi dữ liệu vào cuối file
    writer.writerows(weather_information)

print(f"Dữ liệu đã được ghi tiếp vào file CSV: {daily_weather_data_by_city_file_path}")