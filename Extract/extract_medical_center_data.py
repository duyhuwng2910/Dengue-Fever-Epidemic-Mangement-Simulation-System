import pandas as pd
import os
import pyodbc
import time

# Biến lưu đường dẫn tuyệt đối đến thư mục dữ liệu đơn vị hành chính
medical_center_data_folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Data', 'Public data', 'Medical center data')

# Hàm chuyển định dạng file Excel từ xls/xlsx sang csv
def change_files_format():
    # Chuyển định dạng đối với file lưu thông tin các cơ sở y tế cấp TW
    tw_level_medical_center_file_path = os.path.join(medical_center_data_folder_path, 'cơ sở tuyến tw.xlsx')
    
    df = pd.read_excel(tw_level_medical_center_file_path, header=0)
    
    df.to_csv(os.path.join(medical_center_data_folder_path, 'cơ sở tuyến tw.csv'), index=False, encoding='utf-8-sig')
    
    print("Chuyển định dạng file chứa thông tin danh sách các cơ sở y tế cấp TW thành công!")
    
    
    # Chuyển định dạng đối với file lưu thông tin các cơ sở y tế cấp tỉnh
    province_level_medical_center_file_path = os.path.join(medical_center_data_folder_path, 'cơ sở tuyến tỉnh.xlsx')
    
    df = pd.read_excel(province_level_medical_center_file_path, header=0)
    
    df['Mã KCB'] = df['Mã KCB'].str.strip()
    
    df.to_csv(os.path.join(medical_center_data_folder_path, 'cơ sở tuyến tỉnh.csv'), index=False, encoding='utf-8-sig')
    
    print("Chuyển định dạng file chứa thông tin danh sách các cơ sở y tế cấp tỉnh thành công!")
    
    
    # Chuyển định dạng đối với file lưu thông tin các cơ sở y tế cấp huyện
    district_level_medical_center_file_path = os.path.join(medical_center_data_folder_path, 'cơ sở tuyến huyện.xlsx')

    df = pd.read_excel(district_level_medical_center_file_path, header=0)
    
    df['Mã KCB'] = df['Mã KCB'].str.strip()
    
    df.to_csv(os.path.join(medical_center_data_folder_path, 'cơ sở tuyến huyện.csv'), index=False, encoding='utf-8-sig')
    
    print("Chuyển định dạng file chứa thông tin danh sách các cơ sở y tế cấp huyện thành công!")
    
    
    # Chuyển định dạng đối với file lưu thông tin các bệnh viện thuộc bộ ngành khác
    other_ministries_medical_center_file_path = os.path.join(medical_center_data_folder_path, 'bệnh viện thuộc bộ ngành khác.xlsx')
    
    df = pd.read_excel(other_ministries_medical_center_file_path, header=0)
    
    df.to_csv(os.path.join(medical_center_data_folder_path, 'bệnh viện thuộc bộ ngành khác.csv'), index=False, encoding='utf-8-sig')
    
    print("Chuyển định dạng file chứa thông tin danh sách các bệnh viện thuộc bộ ngành khác thành công!")


# Hàm nhập dữ liệu về thông tin các cơ sở y tế tuyến TW
def import_tw_level_medical_centers_data():
    # Tạo biến kết nối đến database trong SQL Server
    connection = pyodbc.connect('DRIVER={SQL Server};'
                                    'SERVER=DUYHUNGNGUYEN;'
                                    'DATABASE=dengue_fever_epidemic_management_simulation_system;'
                                    'Trusted_Connection=yes;')

    cursor = connection.cursor()
    
    tw_level_medical_centers_data = pd.read_csv(os.path.join(medical_center_data_folder_path, 'cơ sở tuyến tw.csv'),
                                                dtype={'Mã KCB': object}, header=0)
    
    df = pd.DataFrame(tw_level_medical_centers_data)
    
    df = df.fillna('')  # Thay giá trị NaN bằng giá trị rỗng
    
    try:
        cursor.execute('TRUNCATE TABLE medical_centers_information;')
        
        for row in df.itertuples(index=False):
            center_id = row[0]
            center_name = row[1]
            english_center_name = row[2]
            center_type = row[3]
            center_level = row[4]
            province = row[5]
            district = row[6]
            ward = row[7]
            
            cursor.execute('''
                           INSERT INTO medical_centers_information
                           (center_id, center_name, english_center_name, center_type, center_level, [city/province], district, ward)
                           VALUES (?,?,?,?,?,?,?,?)
                           ''',
                           center_id,
                           center_name,
                           english_center_name,
                           center_type,
                           center_level,
                           province,
                           district,
                           ward                                          
            )
    
        cursor.commit()
        
        print("Nhập thông tin cơ sở y tế tuyến TW thành công")
        
    except Exception as e:
        # Rollback nếu có lỗi
        connection.rollback()
        print(f"Error as {e}")
        
    finally:
        connection.close()
    

# Hàm nhập dữ liệu về thông tin các cơ sở y tế tuyến tỉnh
def import_province_level_medical_centers_data():
    # Tạo biến kết nối đến database trong SQL Server
    connection = pyodbc.connect('DRIVER={SQL Server};'
                                    'SERVER=DUYHUNGNGUYEN;'
                                    'DATABASE=dengue_fever_epidemic_management_simulation_system;'
                                    'Trusted_Connection=yes;')

    cursor = connection.cursor()
    

    province_level_medical_centers_data = pd.read_csv(os.path.join(medical_center_data_folder_path, 'cơ sở tuyến tỉnh.csv'),
                                                dtype={'Mã KCB': object}, header=0)
    
    df = pd.DataFrame(province_level_medical_centers_data)
    
    df = df.fillna('')  # Thay giá trị NaN bằng giá trị rỗng
    
    try:
        for row in df.itertuples(index=False):
            center_id = row[0]
            center_name = row[1]
            english_center_name = row[2]
            center_type = row[3]
            center_level = row[4]
            province = row[5]
            district = row[6]
            ward = row[7]
            
            cursor.execute('''
                           INSERT INTO medical_centers_information
                           (center_id, center_name, english_center_name, center_type, center_level, [city/province], district, ward)
                           VALUES (?,?,?,?,?,?,?,?)
                           ''',
                           center_id,
                           center_name,
                           english_center_name,
                           center_type,
                           center_level,
                           province,
                           district,
                           ward                                          
            )
    
        cursor.commit()
        
        print("Nhập thông tin cơ sở y tế tuyến tỉnh thành công")
        
    except Exception as e:
        # Rollback nếu có lỗi
        connection.rollback()
        print(f"Error as {e}")
        
    finally:
        connection.close()
     
     
# Hàm nhập dữ liệu về thông tin các cơ sở y tế tuyến huyện
def import_district_level_medical_centers_data():
    # Tạo biến kết nối đến database trong SQL Server
    connection = pyodbc.connect('DRIVER={SQL Server};'
                                    'SERVER=DUYHUNGNGUYEN;'
                                    'DATABASE=dengue_fever_epidemic_management_simulation_system;'
                                    'Trusted_Connection=yes;')

    cursor = connection.cursor()
    
    district_level_medical_centers_data = pd.read_csv(os.path.join(medical_center_data_folder_path, 'cơ sở tuyến huyện.csv'),
                                                dtype={'Mã KCB': object}, header=0)
    
    df = pd.DataFrame(district_level_medical_centers_data)
    
    df = df.fillna('')  # Thay giá trị NaN bằng giá trị rỗng
    
    try:
        for row in df.itertuples(index=False):
            center_id = row[0]
            center_name = row[1]
            english_center_name = row[2]
            center_type = row[3]
            center_level = row[4]
            province = row[5]
            district = row[6]
            ward = row[7]
            
            cursor.execute('''
                           INSERT INTO medical_centers_information
                           (center_id, center_name, english_center_name, center_type, center_level, [city/province], district, ward)
                           VALUES (?,?,?,?,?,?,?,?)
                           ''',
                           center_id,
                           center_name,
                           english_center_name,
                           center_type,
                           center_level,
                           province,
                           district,
                           ward                                          
            )
    
        cursor.commit()
        
        print("Nhập thông tin cơ sở y tế tuyến huyện thành công")
        
    except Exception as e:
        # Rollback nếu có lỗi
        connection.rollback()
        print(f"Error as {e}")
        
    finally:
        connection.close()
        

# Hàm nhập dữ liệu về thông tin các bệnh viện thuộc bộ ngành khác
def import_other_ministries_medical_centers_data():
    # Tạo biến kết nối đến database trong SQL Server
    connection = pyodbc.connect('DRIVER={SQL Server};'
                                    'SERVER=DUYHUNGNGUYEN;'
                                    'DATABASE=dengue_fever_epidemic_management_simulation_system;'
                                    'Trusted_Connection=yes;')

    cursor = connection.cursor()
    
    other_ministries_medical_centers_data = pd.read_csv(os.path.join(medical_center_data_folder_path, 'bệnh viện thuộc bộ ngành khác.csv'),
                                                dtype={'Mã KCB': object}, header=0)
    
    df = pd.DataFrame(other_ministries_medical_centers_data)
    
    df = df.fillna('')  # Thay giá trị NaN bằng giá trị rỗng
    
    try:
        for row in df.itertuples(index=False):
            center_id = row[0]
            center_name = row[1]
            english_center_name = row[2]
            center_type = row[3]
            center_level = row[4]
            province = row[5]
            district = row[6]
            ward = row[7]
            
            cursor.execute('''
                           INSERT INTO medical_centers_information
                           (center_id, center_name, english_center_name, center_type, center_level, [city/province], district, ward)
                           VALUES (?,?,?,?,?,?,?,?)
                           ''',
                           center_id,
                           center_name,
                           english_center_name,
                           center_type,
                           center_level,
                           province,
                           district,
                           ward                                          
            )
    
        cursor.commit()
        
        print("Nhập thông tin về các bệnh viên thuộc bộ ngành khác thành công!")
        
    except Exception as e:
        # Rollback nếu có lỗi
        connection.rollback()
        print(f"Error as {e}")
        
    finally:
        connection.close()
        

change_files_format()
time.sleep(1)
import_tw_level_medical_centers_data()
time.sleep(1)
import_province_level_medical_centers_data()
time.sleep(1)
import_district_level_medical_centers_data()
time.sleep(1)
import_other_ministries_medical_centers_data()