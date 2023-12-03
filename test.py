import requests
import json

vietnam_provinces = [
    "An Giang",
    "Ba Ria - Vung Tau",
    "Bac Giang",
    "Bac Kan",
    "Bac Lieu",
    "Bac Ninh",
    "Ben Tre",
    "Binh Dinh",
    "Binh Duong",
    "Binh Phuoc",
    "Binh Thuan",
    "Ca Mau",
    "Cao Bang",
    "Dak Lak",
    "Dak Nong",
    "Dien Bien",
    "Dong Nai",
    "Dong Thap",
    "Gia Lai",
    "Ha Giang",
    "Ha Nam",
    "Ha Tinh",
    "Hai Duong",
    "Hau Giang",
    "Hoa Binh",
    "Hung Yen",
    "Khanh Hoa",
    "Kien Giang",
    "Kon Tum",
    "Lai Chau",
    "Lam Dong",
    "Lang Son",
    "Lao Cai",
    "Long An",
    "Nam Dinh",
    "Nghe An",
    "Ninh Binh",
    "Ninh Thuan",
    "Phu Tho",
    "Phu Yen"
    "Quang Binh",
    "Quang Nam",
    "Quang Ngai",
    "Quang Ninh",
    "Quang Tri",
    "Soc Trang",
    "Son La",
    "Tay Ninh",
    "Thai Binh",
    "Thai Nguyen",
    "Thanh Hoa",
    "Thua Thien Hue",
    "Tien Giang",
    "Tra Vinh",
    "Tuyen Quang",
    "Vinh Long",
    "Vinh Phuc",
    "Yen Bai",
    "Can Tho",
    "Da Nang",
    "Hai Phong",
    "Hanoi",
    "Ho Chi Minh City"
]


vietnam_provinces_longitude = []
vietnam_provinces_latitude = []

vietnam_provinces_longitude.append(105.1259)
vietnam_provinces_latitude.append(10.5216)

for i in range(0, len(vietnam_provinces), 1):
    url = f'http://api.openweathermap.org/geo/1.0/direct?q={vietnam_provinces[i]},+84&limit=3&appid=88ec58173d2be009908c974b114bb0f8'

    response = requests.get(url)


    # Kiểm tra xem request có thành công không (status code 200)
    if response.status_code == 200:
        # Parse dữ liệu JSON
        weather_data = response.json()

        # Xử lý dữ liệu thời tiết theo nhu cầu của bạn
        for city in weather_data:
            # Kiểm tra trường country có giá trị là "VN" hay không
            if city['country'] == 'VN':                
                vietnam_provinces_latitude.append(city['lat'])
                vietnam_provinces_longitude.append(city['lon'])

                print(f"Coordinate of {vietnam_provinces[i]}, Vietnam:(Latitude:{city['lat']}, Longitude:{city['lon']})")

                break

    else:
        print(f"API call failed with status code {response.status_code}")