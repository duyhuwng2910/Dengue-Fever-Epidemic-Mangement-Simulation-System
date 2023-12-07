import csv
from geopy.geocoders import Nominatim

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

# Lặp qua từng tỉnh và lấy tọa độ
for province in vietnam_provinces:
    location = geolocator.geocode(province + ", Việt Nam", timeout=10)
    
    if location:
        vietnam_provinces_coordinate.append([province, round(location.longitude, 3), round(location.latitude, 6)])
        vietnam_provinces_latitude.append(round(location.latitude, 3))
        vietnam_provinces_longitude.append(round(location.longitude, 3))
    else:
        print(f"Can not find the coordinate for {province}")

vietnam_provinces_coordinate_file_path = "vietnam_provinces_coordinate.csv"

with open(vietnam_provinces_coordinate_file_path, mode="w", newline='', encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)

    # Viết dòng tiêu đề
    writer.writerow(["city_name", "longitude", "latitude"])

    # Viết dữ liệu
    writer.writerows(vietnam_provinces_coordinate)

print(f"Coordinates of all the provinces in Vietnam were saved CSV: {vietnam_provinces_coordinate_file_path}")