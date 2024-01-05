import random
import pandas as pd
import time
import os
import pyodbc
import numpy as np


# Tạo biến kết nối đến database trong SQL Server
connection = pyodbc.connect('DRIVER={SQL Server};'
                                'SERVER=DUYHUNGNGUYEN;'
                                'DATABASE=dengue_fever_epidemic_management_simulation_system;'
                                'Trusted_Connection=yes;')

administrative_units_data_query = f'SELECT * FROM administrative_units_information_2023'

medical_center_data_query = f'SELECT * FROM medical_centers_information'

administrative_units_df = pd.read_sql(administrative_units_data_query, connection)

# Biến df lưu dữ liệu đọc từ bảng medical_center_informations trong CSDL thông qua truy vấn
medical_center_df = pd.read_sql(medical_center_data_query, connection)

number_of_dengue_cases_each_day = random.randint(150,750)

gender_list = ['male', 'female']

values_list = ['yes','no','unknown']

test_values_list = ['positive','negative']

# Ánh xạ kiểu dữ liệu từ SQL Server sang DataFrame
sql_server_data_types = {
    'NVARCHAR': 'object',  # hoặc có thể chọn 'string'
    'INT': 'Int64',
    'DATE': 'datetime64[D]',
    'DECIMAL': 'float64',
    'BIGINT': 'Int64'
}

# Khai báo biến data với kiểu dữ liệu và đơn vị thời gian
dengue_case_records_data = {
    'record_id': pd.array([None], dtype='Int64'),
    'city_id': pd.array([None], dtype='object'),
    'year_of_illness': pd.array([None], dtype='Int64'),
    'gender': pd.array([None], dtype='object'),
    'date_of_birth': pd.array([None], dtype='datetime64[D]'),  # Đơn vị thời gian là ngày (D)
    'ward_name': pd.array([None], dtype='object'),
    'district_name': pd.array([None], dtype='object'),
    'city_name': pd.array([None], dtype='object'),
    'examined_at_ward_health_clinic': pd.array([None], dtype='object'),
    'examined_at_hospital': pd.array([None], dtype='object'),
    'is_pregnant': pd.array([None], dtype='object'),
    'hospital_name': pd.array([None], dtype='object'),
    'hospital_typeN': pd.array([None], dtype='object'),
    'admit_date': pd.array([None], dtype='datetime64[D]'),  # Đơn vị thời gian là ngày (D)
    'discharge_date': pd.array([None], dtype='datetime64[D]'),  # Đơn vị thời gian là ngày (D)
    # ... (Các cột khác)
    'NS1_test_date': pd.array([None], dtype='datetime64[D]'),  # Đơn vị thời gian là ngày (D)
    'NS1_test_result': pd.array([None], dtype='object'),
    'PCR_test_date': pd.array([None], dtype='datetime64[D]'),  # Đơn vị thời gian là ngày (D)
    'PCR_test_result': pd.array([None], dtype='object'),
    'dengue_virus_isolation_test_date': pd.array([None], dtype='datetime64[D]'),  # Đơn vị thời gian là ngày (D)
    'dengue_virus_isolation_test_result': pd.array([None], dtype='object'),
    'IgM_test_date': pd.array([None], dtype='datetime64[D]'),  # Đơn vị thời gian là ngày (D)
    'first_serological_test_date(IgM)': pd.array([None], dtype='datetime64[D]'),  # Đơn vị thời gian là ngày (D)
    'first_serological_test_result(IgM)': pd.array([None], dtype='object'),
    'second_serological_test_date(IgM)': pd.array([None], dtype='datetime64[D]'),  # Đơn vị thời gian là ngày (D)
    'second_serological_test_result(IgM)': pd.array([None], dtype='object'),
    'dengue_fever_diagnosis': pd.array([None], dtype='object'),
    'dengue_fever_level_rank': pd.array([None], dtype='object'),
    'treatment_action': pd.array([None], dtype='object'),
    'change_hospital_type': pd.array([None], dtype='object'),
    'new_hospital_name': pd.array([None], dtype='object'),
    'result': pd.array([None], dtype='object'),
    'result_date': pd.array([None], dtype='datetime64[D]')  # Đơn vị thời gian là ngày (D)
}

# Tạo DataFrame
dengue_case_records_df = pd.DataFrame(dengue_case_records_data)

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

hanoi = 'Thành phố Hà Nội'

hochiminh_city = 'Thành phố Hồ Chí Minh'

red_river_delta = ['Tỉnh Vĩnh Phúc', 'Tỉnh Bắc Ninh', 'Tình Hà Nam', 'Tỉnh Hưng Yên', 'Tỉnh Hải Dương', 'Thành phố Hải Phòng', 'Tỉnh Thái Bình', 'Tỉnh Nam Định', 'Tỉnh Ninh Bình', 'Tỉnh Quảng Ninh']

mekong_delta = ['Thành phố Cần Thơ', 'Tỉnh An Giang', 'Tỉnh Bạc Liêu', 'Tỉnh Bến Tre', 'Tỉnh Long An', 'Tỉnh Cà Mau', 'Tỉnh Sóc Trăng', 'Tỉnh Hậu Giang', 'Tỉnh Trà Vinh', 'Tỉnh Đồng Tháp', 'Tỉnh Vĩnh Long', 'Tỉnh Kiên Giang', 'Tỉnh Tiền Giang']

coastal_city = ['Tỉnh Thanh Hóa', 'Tỉnh Nghệ An', 'Tỉnh Hà Tĩnh', 'Tỉnh Quảng Bình', 'Tỉnh Quảng Trị', 'Tỉnh Thừa Thiên Huế', 'Thành phố Đà Nẵng', 'Tỉnh Quảng Nam', 'Tỉnh Quảng Ngãi', 'Tỉnh Bình Định', 'Tỉnh Phú Yên', 'Tỉnh Khánh Hòa', 'Tỉnh Ninh Thuận', 'Tỉnh Bình Thuận', 'Thành phố Hồ Chí Minh']

# Tạo danh sách rest_provinces
rest_provinces = list(set(vietnam_provinces) - set(red_river_delta) - set(mekong_delta) - set(coastal_city))

def generate_random_province(n):
    """
    Tạo một tập giá trị với tỉ lệ random khác nhau cho từng tập.

    Parameters:
    - n: Số lượng giá trị cần tạo.

    Returns:
    - provinces: Một mảng numpy chứa các giá trị tỉnh thành được tạo ra.
    """

    p_hanoi = 0.26
    p_hochiminh_city = 0.12
    p_red_river_delta = 0.2
    p_mekong_delta = 0.22
    p_coastal_city = 0.1
    p_rest_provinces = 0.1

    # probabilities = [
    #     p_hanoi,
    #     p_hochiminh_city,
    #     p_red_river_delta / len(red_river_delta),
    #     p_mekong_delta / len(mekong_delta),
    #     p_coastal_city / len(coastal_city),
    #     p_rest_provinces / len(rest_provinces)
    # ]

    provinces = np.concatenate([
        np.random.choice([hanoi], size=max(1, int(n * p_hanoi))),
        np.random.choice([hochiminh_city], size=max(1, int(n * p_hochiminh_city))),
        np.random.choice(red_river_delta, size=max(1, int(n * p_red_river_delta))),
        np.random.choice(mekong_delta, size=max(1, int(n * p_mekong_delta))),
        np.random.choice(coastal_city, size=max(1, int(n * p_coastal_city))),
        np.random.choice(rest_provinces, size=max(1, int(n * p_rest_provinces)))
    ])

    return provinces

# Sử dụng hàm với ví dụ
n_values = 20

result = generate_random_province(n_values)

# Kiểm tra xem có giá trị nào không
if len(result) > 0:
    for i in range(len(result)):
        city_sample = result[i]
        random_record = administrative_units_df[administrative_units_df['city_name'] == city_sample].sample(n=1)
        print(random_record)
else:
    print("Không có giá trị nào được tạo.")

# for i in range(number_of_dengue_cases_each_day):
