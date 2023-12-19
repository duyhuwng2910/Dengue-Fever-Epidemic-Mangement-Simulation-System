
-- Truy vấn ở bảng thông tin đơn vị hành chính
-- Ví dụ tìm toàn bộ thông tin các phường tại quận Đống Đa của thành phố Hà Nội
SELECT *
FROM administrative_units_information_2023
WHERE city_name COLLATE SQL_Latin1_General_CP1_CS_AS = N'Thành phố Hà Nội'
AND district_name COLLATE SQL_Latin1_General_CP1_CS_AS = N'Quận Đống Đa';

-- Truy vấn ở bảng thông tin các cơ sở y tế
-- Ví dụ tìm toàn bộ thông tin các cơ sở y tế trên địa bàn thành phố Hà Nội
SELECT *
FROM medical_centers_information mci
WHERE mci.[city/province] COLLATE SQL_Latin1_General_CP1_CS_AS = N'Thành phố Hà Nội'
AND mci.district COLLATE SQL_Latin1_General_CP1_CS_AS = N'Quận Đống Đa';
