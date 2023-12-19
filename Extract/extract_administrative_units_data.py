import pandas as pd
import os
import pyodbc
import time


# Biến lưu đường dẫn tuyệt đối đến thư mục dữ liệu đơn vị hành chính
administrative_units_data_folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Data', 'Public data', 'Administrative units data')

connection = pyodbc.connect('DRIVER={SQL Server};'
                                'SERVER=DUYHUNGNGUYEN;'
                                'DATABASE=dengue_fever_epidemic_management_simulation_system;'
                                'Trusted_Connection=yes;')

# Hàm chuyển định dạng file Excel từ xls/xlsx sang csv
def change_files_format():
    #administrative_units_data_folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Data', 'Public data', 'Administrative units data')

    administrative_units_information_file_path = os.path.join(administrative_units_data_folder_path, 'Danh sách cấp tỉnh kèm theo quận huyện, phường xã - 2023.xls')
    
    df = pd.read_excel(administrative_units_information_file_path, dtype={'Mã TP': object, 'Mã QH': object, 'Mã PX': object}, header=0)
    
    df.to_csv(os.path.join(administrative_units_data_folder_path, 'Danh sách cấp tỉnh kèm theo quận huyện, phường xã - 2023.csv'), index=False, encoding='utf-8-sig')
    
    print("Chuyển định dạng file chứa thông tin danh sách cấp tỉnh kèm theo quân huyện, phường xã thành công!")
    
    area_and_population_file_path = os.path.join(administrative_units_data_folder_path, 'Diện tích, dân số, mật độ dân số (2022).xlsx')
    
    df = pd.read_excel(area_and_population_file_path, skiprows=3)
    
    df = df.rename(columns={'Unnamed: 0':'Tên khu vực'})
    
    df.to_csv(os.path.join(administrative_units_data_folder_path, 'Diện tích, dân số, mật độ dân số (2022).csv'), index=False, encoding='utf-8-sig')
    
    print("Chuyển định dạng file chúa thông tin về diện tích, dân số, mật độ dân số thành công!")


# Hàm nhập dữ liệu về đơn vị hành chính vào bảng trong SQL Server
def import_administrative_units_data():
    administrative_units_information_file_path = os.path.join(administrative_units_data_folder_path, 'Danh sách cấp tỉnh kèm theo quận huyện, phường xã - 2023.csv')
    
    administrative_units_data = pd.read_csv(administrative_units_information_file_path, dtype={'Mã TP': object, 'Mã QH': object, 'Mã PX': object}, encoding='utf-8', header=0)
    
    df = pd.DataFrame(administrative_units_data)
    
    df = df.astype(str)
    
    cursor = connection.cursor()
    
    try:
        cursor.execute('TRUNCATE TABLE administrative_units_information_2023')
        
        for row in df.itertuples(index=False):
            city_name = row[df.columns.get_loc('Tỉnh Thành Phố')]
            city_id = row[df.columns.get_loc('Mã TP')]
            district_name = row[df.columns.get_loc('Quận Huyện')]
            district_id = row[df.columns.get_loc('Mã QH')]
            ward_name = row[df.columns.get_loc('Phường Xã')]
            ward_id = row[df.columns.get_loc('Mã PX')]
            administrative_unit_level = row[df.columns.get_loc('Cấp')]
            english_name = row[df.columns.get_loc('Tên Tiếng Anh')]
            
            cursor.execute('''
                        INSERT INTO administrative_units_information_2023 
                        (city_name, city_id, district_name, district_id, ward_name, ward_id, administrative_unit_level, english_name)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        ''',
                        city_name,
                        city_id,
                        district_name,
                        district_id,
                        ward_name,
                        ward_id,
                        administrative_unit_level,
                        english_name
                        )
        
        connection.commit()

        print("Nhập dữ liệu về thông tin đơn vị hành chính thành công!")
        
    except Exception as e:
        # Rollback nếu có lỗi
        connection.rollback()
        print(f"Error: {e}")

    finally:
        connection.close()
        

# Hàm nhập dữ liệu về diện tích và dân số vào bảng trong SQL Server        
def import_area_and_population_2022_data():
    area_and_population_file_path = os.path.join(administrative_units_data_folder_path, 'Diện tích, dân số, mật độ dân số (2022).csv')
    
    area_and_population_data = pd.read_csv(area_and_population_file_path, encoding='utf-8', header=0)
    
    df = pd.DataFrame(area_and_population_data)
    
    df['Diện tích(Km2)'] = df['Diện tích(Km2)'].apply(lambda x: round(x, 2) if not pd.isna(x) else x)
    df['Dân số trung bình (Nghìn người)'] = df['Dân số trung bình (Nghìn người)'].apply(lambda x: round(x, 2) if not pd.isna(x) else x)
    
    cursor = connection.cursor()
    
    try:
        cursor.execute('TRUNCATE TABLE area_and_population_2022')
        
        for row in df.itertuples(index=False):
            name = row[0]
            square = row[1]
            average_population = row[2]
            population_density = row[3]
            
            cursor.execute('''
                           INSERT INTO area_and_population_2022 
                           (name, [square(Km2)], [average_population(thousands)], [population_density(person/Km2)])
                           VALUES (?, ?, ?, ?)
                           ''',
                           name,
                           square,
                           average_population,
                           population_density)
            
        connection.commit()
        
        print("Nhập dữ liệu về diện tích và dân số thành công!")
        
    except Exception as e:
        print(f"Error as {e}")
        
    finally:
        connection.close()
        

change_files_format()
# time.sleep(1)
# import_administrative_units_data()
# time.sleep(1)
# import_area_and_population_2022_data()