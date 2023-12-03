DROP TABLE IF EXISTS dengue_fever_case_record;

CREATE TABLE dengue_fever_case_record (
    record_id INTEGER AUTO_INCREMENT PRIMARY KEY,
    
    -- Personal Information 
    gender VARCHAR(20) NOT NULL,
    date_of_birth DATE NOT NULL,
    city_name VARCHAR(50) NOT NULL,
    district_name VARCHAR(50) NULL,
    ward_name VARCHAR(50) NULL,
    is_pregnant VARCHAR(10) NOT NULL,
    hospital_name VARCHAR(50) NOT NULL,
    hospital_type VARCHAR(20) NOT NULL,
    admit_date DATE NOT NULL,
    discharge_date DATE NULL,

    dengue_fever_times INTEGER NOT NULL,
    latest_dengue_fever_date DATE NULL,
    first_date_have_symptoms DATE NULL,

    -- Các triệu chứng lâm sàng
    fever VARCHAR(10) NOT NULL,
    highest_temperature DECIMAL(2,1) NULL,
    chills_or_rigors VARCHAR(10) NULL, -- Lạnh người, rùng mình
    headache VARCHAR(10) NULL, -- Đau đầu
    fatigue_or_malaise VARCHAR(10) NULL, -- Mệt mỏi, khó chịu
    nausea_or_vomiting VARCHAR(10) NULL, -- Buồn nôn, nôn mửa
    diarrhea VARCHAR(10) NULL, -- Tiêu chảy
    muscle_pain VARCHAR(10) NULL, -- Đau bắp thịt, cơ
    joint_pain VARCHAR(10) NULL, -- Đau xương khớp
    arthritis VARCHAR(10) NULL, -- Viêm khớp
    paresis_or_paralysis VARCHAR(10) NULL, -- Liệt, tê liệt
    stiff_neck VARCHAR(10) NULL, -- Cứng cổ
    seizures VARCHAR(10) NULL, -- Co giật
    abdominal_pain VARCHAR(10) NOT NULL, -- Đau bụng

    -- Các triệu chứng xuất huyết
    tourniquet_positive_sign VARCHAR(20) NULL, -- Dấu hiệu dây thắt
    rash VARCHAR(10) NOT NULL, -- Phát ban
    clot_bleeding VARCHAR(10) NOT NULL, -- Xuất huyết nổi cục 
    leukopenia VARCHAR(10) NOT NULL, -- Giảm bạch cầu
    altered_mental_status VARCHAR(10) NOT NULL, -- Xuất huyết lợi răng
    vomiting_blood VARCHAR(10) NOT NULL, -- Nôn ra máu
    urinate_blood VARCHAR(10) NOT NULL, -- Đi tiểu ra máu
    defecate_blood VARCHAR(10) NOT NULL, -- Đi ngoài ra máu
    pleural_effusion VARCHAR(10) NOT NULL, --  Tràn dịch màng phổi
    mucosal_bleeding VARCHAR(10) NOT NULL, -- Chảy máu niêm mạc
    liver_pain VARCHAR(10) NOT NULL, -- Đau bụng vùng gan
    
    -- Các xét nghiệm
    NS1_test_date DATE NULL, -- Ngày xét nghiệm NS1
    NS1_test_result VARCHAR(10) NULL, -- Kết quả xét nghiệm NS1
    PCR_test_date DATE NULL, -- Ngày xét nghiệm PCR
    PCR_test_result VARCHAR(10) NULL, -- Kết quả xét nghiệm PCR
    dengue_virus_isolation_test_date DATE NULL, --Ngày xét nghiệm phân lập vi rút Dengue
    dengue_virus_isolation_test_result VARCHAR(10) NULL, -- Kết quả xét nghiệm phân lập vi rút Dengue
    
    -- Chuẩn đoán cuối cùng
    dengue_fever_diagnosis VARCHAR(10) NOT NULL, -- Chẩn đoán sốt xuất huyết dengue
    dengue_fever_level_rank VARCHAR(30) NOT NULL, -- Phân độ nặng của sốt xuất huyết dengue
    treatment_action VARCHAR(20) NOT NULL, -- Điều trị
    change_hospital_type VARCHAR(10) NOT NULL, -- Chuyển tuyến bệnh viện
    new_hospital_name VARCHAR(50) NULL, -- Tên cơ sở điều trị nếu có chuyển tuyến
    result VARCHAR(20) NOT NULL -- Kết quả
    result_date DATE NULL -- Ngày trả kết quả
);