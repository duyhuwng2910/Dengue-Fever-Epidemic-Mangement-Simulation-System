import csv
from geopy.geocoders import Nominatim
import pandas as pd
import pyodbc
import time

# Khởi tạo đối tượng Nominatim
geolocator = Nominatim(user_agent="my_geocoder")

# Danh sách tên tỉnh thành
vietnam_provinces = [
    "Hà Nội", "Hồ Chí Minh", "Đà Nẵng", "Hải Phòng", "Hòa Bình", "Sơn La", "Lai Châu", "Lào Cai", "Yên Bái",
    "Tuyên Quang", "Lạng Sơn", "Bắc Kạn", "Thái Nguyên", "Cao Bằng", "Lâm Đồng", "Đắk Lắk", "Đắk Nông", "Khánh Hòa",
    "Phú Yên", "Bình Định", "Gia Lai", "Kon Tum", "Quảng Nam", "Quảng Ngãi", "Quảng Bình", "Quảng Trị", "Thừa Thiên Huế",
    "Quảng Ninh", "Hải Dương", "Hưng Yên", "Bắc Ninh", "Nam Định", "Thái Bình", "Ninh Bình", "Vĩnh Phúc", "Phú Thọ",
    "Bắc Giang", "Bắc Ninh", "Hà Nam", "Hà Tĩnh", "Nghệ An", "Quảng Ninh", "Quảng Trị", "Sóc Trăng", "Tiền Giang",
    "Trà Vinh", "Vĩnh Long", "Bến Tre", "Cần Thơ", "Đồng Tháp", "Hậu Giang", "Kiên Giang", "Long An", "An Giang",
    "Bà Rịa - Vũng Tàu", "Bình Dương", "Bình Phước", "Đồng Nai", "Tây Ninh",
    "Đắk Lắk", "Đồng Nai", "Bà Rịa - Vũng Tàu", "Bình Dương"
]

# Mảng để lưu dữ liệu
vietnam_provinces_coordinate = []
vietnam_provinces_latitude = []
vietnam_provinces_longitude = []

# Lặp qua từng tỉnh, thành phố và lấy tọa độ
for province in vietnam_provinces:
    location = geolocator.geocode(province + ", Việt Nam", timeout=10)
    
    if location:
        vietnam_provinces_coordinate.append([province, round(location.longitude, 3), round(location.latitude, 3)])
        vietnam_provinces_latitude.append(round(location.latitude, 3))
        vietnam_provinces_longitude.append(round(location.longitude, 3))
    else:
        print(f"Can not find the coordinate for {province}")

vietnam_provinces_coordinate_file_path = "Data/Public data/Weather data/vietnam_provinces_coordinate.csv"

with open(vietnam_provinces_coordinate_file_path, mode="w", newline='', encoding="utf-8-sig") as csv_file:
    writer = csv.writer(csv_file)

    # Viết dòng tiêu đề
    writer.writerow(["name", "longitude", "latitude"])

    # Viết dữ liệu
    writer.writerows(vietnam_provinces_coordinate)

print(f"Toàn bộ tọa độ các tỉnh thành đã được cập nhật trong file tại đường dẫn sau: {vietnam_provinces_coordinate_file_path}")

# Kết nối đến cơ sở dữ liệu SQL Server
connection = pyodbc.connect('DRIVER={SQL Server};'
                            'SERVER=DUYHUNGNGUYEN;'
                            'DATABASE=dengue_fever_epidemic_management_simulation_system;'
                            'Trusted_Connection=yes;')

# Đọc dữ liệu từ file CSV vào DataFrame (header=0 để sử dụng dòng đầu tiên làm header)
data = pd.read_csv(vietnam_provinces_coordinate_file_path, encoding='utf-8', header=0)

df = pd.DataFrame(data)

# Xóa dữ liệu cũ trong bảng (nếu cần)
with connection.cursor() as cursor:
    cursor.execute(f'TRUNCATE TABLE Vietnam_provinces_coordinate')
    connection.commit()

# Chuyển dữ liệu từ DataFrame vào SQL Server
for row in df.itertuples():
    cursor.execute('''
                   INSERT INTO Vietnam_provinces_coordinate (name, longitude, latitude)
                   VALUES (?, ?, ?)
                   ''',
                   row.name,
                   row.longitude,
                   row.latitude
                   )

connection.commit()

print("Nhập dữ liệu thành công!")

# Đóng kết nối
connection.close()