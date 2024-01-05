import csv
from geopy.geocoders import Nominatim
import pandas as pd
import pyodbc
import time

# Khởi tạo đối tượng Nominatim
geolocator = Nominatim(user_agent="my_geocoder")

# Danh sách tên tỉnh thành
vietnam_provinces = [
    "Thành phố Hà Nội",
    "Tỉnh Hà Giang",
    "Tỉnh Cao Bằng",
    "Tỉnh Bắc Kạn",
    "Tỉnh Tuyên Quang",
    "Tỉnh Lào Cai",
    "Tỉnh Điện Biên",
    "Tỉnh Lai Châu",
    "Tỉnh Sơn La",
    "Tỉnh Yên Bái",
    "Tỉnh Hoà Bình",
    "Tỉnh Thái Nguyên",
    "Tỉnh Lạng Sơn",
    "Tỉnh Quảng Ninh",
    "Tỉnh Bắc Giang",
    "Tỉnh Phú Thọ",
    "Tỉnh Vĩnh Phúc",
    "Tỉnh Bắc Ninh",
    "Tỉnh Hải Dương",
    "Thành phố Hải Phòng",
    "Tỉnh Hưng Yên",
    "Tỉnh Thái Bình",
    "Tỉnh Hà Nam",
    "Tỉnh Nam Định",
    "Tỉnh Ninh Bình",
    "Tỉnh Thanh Hóa",
    "Tỉnh Nghệ An",
    "Tỉnh Hà Tĩnh",
    "Tỉnh Quảng Bình",
    "Tỉnh Quảng Trị",
    "Tỉnh Thừa Thiên Huế",
    "Thành phố Đà Nẵng",
    "Tỉnh Quảng Nam",
    "Tỉnh Quảng Ngãi",
    "Tỉnh Bình Định",
    "Tỉnh Phú Yên",
    "Tỉnh Khánh Hòa",
    "Tỉnh Ninh Thuận",
    "Tỉnh Bình Thuận",
    "Tỉnh Kon Tum",
    "Tỉnh Gia Lai",
    "Tỉnh Đắk Lắk",
    "Tỉnh Đắk Nông",
    "Tỉnh Lâm Đồng",
    "Tỉnh Bình Phước",
    "Tỉnh Tây Ninh",
    "Tỉnh Bình Dương",
    "Tỉnh Đồng Nai",
    "Tỉnh Bà Rịa - Vũng Tàu",
    "Thành phố Hồ Chí Minh",
    "Tỉnh Long An",
    "Tỉnh Tiền Giang",
    "Tỉnh Bến Tre",
    "Tỉnh Trà Vinh",
    "Tỉnh Vĩnh Long",
    "Tỉnh Đồng Tháp",
    "Tỉnh An Giang",
    "Tỉnh Kiên Giang",
    "Thành phố Cần Thơ",
    "Tỉnh Hậu Giang",
    "Tỉnh Sóc Trăng",
    "Tỉnh Bạc Liêu",
    "Tỉnh Cà Mau"
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