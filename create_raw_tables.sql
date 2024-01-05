DROP TABLE IF EXISTS dengue_fever_case_record;

CREATE TABLE dengue_fever_case_record (
    -- Số xác định ca bệnh
    record_id BIGINT IDENTITY(1,1) PRIMARY KEY,
    city_id NVARCHAR(10) NOT NULL,
    year_of_illness INT NOT NULL,

    -- Xác định điều tra ca bệnh 
    gender NVARCHAR(20) NOT NULL,
    date_of_birth DATE NOT NULL,
    ward_name NVARCHAR(50) NULL,
    district_name NVARCHAR(50) NULL,
    city_name NVARCHAR(50) NOT NULL,
    examined_at_ward_health_clinic NVARCHAR(10) NOT NULL,
    examined_at_hospital NVARCHAR(10) NOT NULL,
    is_pregnant NVARCHAR(10) NOT NULL,
    hospital_name NVARCHAR(50) NOT NULL,
    hospital_typeN VARCHAR(20) NOT NULL,
    admit_date DATE NOT NULL,
    discharge_date DATE NULL,

    -- Tiền sử dịch tễ
    used_to_be_infected_with_dengue_fever INT NOT NULL,
    latest_dengue_fever_date DATE NULL,
    live_in_epidemic_areas_within_one_week NVARCHAR(10) NULL,

    -- Các triệu chứng lâm sàng
    fever NVARCHAR(10) NOT NULL,
    first_date_got_sick DATE NOT NULL,-- Ngày bắt đầu sốt, trung bình 4-7 ngày, có thể kéo dài đến 14 ngày
    highest_temperature DECIMAL(2,1) NOT NULL, -- 39-41 độ
    chills_or_rigors NVARCHAR(10) NOT NULL, -- Lạnh người, rùng mình
    headache NVARCHAR(10) NOT NULL, -- Đau đầu
    muscle_pain NVARCHAR(10) NOT NULL, -- Đau bắp thịt, cơ
    joint_pain NVARCHAR(10) NOT NULL, -- Đau xương khớp
    tourniquet_positive_sign NVARCHAR(20) NOT NULL, -- Dấu hiệu dây thắt
    fatigue_or_malaise NVARCHAR(10) NOT NULL, -- Mệt mỏi, khó chịu
    nausea_or_vomiting NVARCHAR(10) NOT NULL, -- Buồn nôn, nôn mửa
    diarrhea NVARCHAR(10) NOT NULL, -- Tiêu chảy
    arthritis NVARCHAR(10) NOT NULL, -- Viêm khớp
    paresis_or_paralysis NVARCHAR(10) NOT NULL, -- Liệt, tê liệt
    stiff_neck NVARCHAR(10) NOT NULL, -- Cứng cổ
    seizures NVARCHAR(10) NOT NULL, -- Co giật
    abdominal_pain NVARCHAR(10) NOT NULL, -- Đau bụng

    -- Các triệu chứng xuất huyết
    
    rash NVARCHAR(10) NOT NULL, -- Nổi, phát ban
    petechiae NVARCHAR(10) NOT NULL, -- Chấm xuất huyết
    clot_bleeding NVARCHAR(10) NOT NULL, -- Xuất huyết nổi cục 
    hemorrhagic_plaque NVARCHAR(10) NOT NULL, -- Mảng xuất huyết
    altered_mental_status NVARCHAR(10) NOT NULL, -- Xuất huyết lợi răng
    vomiting_blood NVARCHAR(10) NOT NULL, -- Nôn ra máu
    defecate_blood NVARCHAR(10) NOT NULL, -- Đi ngoài ra máu
    urinate_blood NVARCHAR(10) NOT NULL, -- Đi tiểu ra máu
    liver_pain NVARCHAR(10) NOT NULL, -- Đau bụng vùng gan
    liver_below_rib_margin NVARCHAR(10) NOT NULL, -- Gan dưới bờ sườn
    swollen_lymph_nodes NVARCHAR(10) NOT NULL, -- Sưng hạch bạch huyết
    pleural_effusion NVARCHAR(10) NOT NULL, --  Tràn dịch màng phổi
    mucosal_bleeding NVARCHAR(10) NOT NULL, -- Chảy máu niêm mạc
    
    -- Chẩn đoán sơ bộ
    preliminary_diagnosis NVARCHAR(50) NOT NULL,

    -- Dấu hiện tiền và sốc
    is_struggle NVARCHAR(10) NOT NULL, -- Vật vã
    lethargy NVARCHAR(10) NOT NULL, -- Li bì
    cold_limbs NVARCHAR(10) NOT NULL, -- Chân tay lạnh
    cold_and_damp_skin NVARCHAR(10) NOT NULL, -- Da lạnh ẩm
    [pulse_rate(beats/minute)] NVARCHAR(10) NULL, --  Nhịp mạch (lần/phút)
    [max/min_blood_pressure] NVARCHAR(50) NULL, -- Huyết áp tối đa/tối thiểu
    other_symptoms NVARCHAR(250) NULL,

    /*
        Xét nghiệm
    */
    -- Xét nghiệm huyết học
    [Hematocrit(%)] INT NOT NULL, -- Trước khi mắc sốt xuất huyết, hematocrit bình thường có thể là khoảng 38-47%. Trong trường hợp sốt xuất huyết, nó có thể giảm xuống, ví dụ, dưới 30%. 
    [Platelet(G/L)] INT NOT NULL, -- Số lượng tiểu cầu bình thường là khoảng 150-450 G/L. Trong sốt xuất huyết, có thể thấy giảm đáng kể, ví dụ, dưới 100 G/L hoặc thậm chí dưới 50 G/L.
    [red_blood_cell(units/microliter)] BIGINT NULL, -- Số lượng hồng cầu bình thường là khoảng 4.5-5.5 triệu/microliter. Trong trường hợp sốt xuất huyết, có thể thấy giảm đáng kể, ví dụ, dưới 4 triệu/microliter.
    [whiet_blood_cell(units/microliter)] BIGINT NULL, -- Số lượng bạch cầu bình thường là khoảng 4,000-11,000/microliter. Trong sốt xuất huyết, bạch cầu có thể tăng lên, ví dụ, trên 15,000/microliter, do cơ thể cố gắng chống lại nhiễm trùng.
    -- Xét nghiệm NS1
    NS1_test_date DATE NULL, -- Ngày lấy mẫu xét nghiệm NS1
    NS1_test_result NVARCHAR(10) NULL, -- Kết quả xét nghiệm NS1
    -- Xét nghiệm PCR
    PCR_test_date DATE NULL, -- Ngày xét nghiệm PCR
    PCR_test_result NVARCHAR(10) NULL, -- Kết quả xét nghiệm PCR
    -- Xét nghiệm phân lập vi rút Dengue
    dengue_virus_isolation_test_date DATE NULL, -- Ngày xét nghiệm phân lập vi rút Dengue
    dengue_virus_isolation_test_result NVARCHAR(10) NULL, -- Kết quả xét nghiệm phân lập vi rút Dengue
    -- Xét nghiệm IgM. Nếu mắc bệnh sốt xuất huyết từ ngày thứ 4 thì IgM sẽ cho kết quả dương tính.
    IgM_test_date DATE NULL, -- Ngày xét nghiệm IgM
    [first_serological_test_date(IgM)] DATE NULL, -- Ngày lấy huyết thanh 1
    [first_serological_test_result(IgM)] NVARCHAR(10) NULL, -- Kết quả xét nghiệm huyết thanh 1
    [second_serological_test_date(IgM)] DATE NULL, -- Ngày lấy huyết thanh 2
    [second_serological_test_result(IgM)] NVARCHAR(10) NULL, -- Kết quả xét nghiệm huyết thanh 2
    
    -- Chuẩn đoán cuối cùng
    dengue_fever_diagnosis NVARCHAR(10) NOT NULL, -- Chẩn đoán sốt xuất huyết dengue
    dengue_fever_level_rank NVARCHAR(30) NOT NULL, -- Phân độ nặng của sốt xuất huyết dengue
    treatment_action NVARCHAR(20) NOT NULL, -- Điều trị
    change_hospital_type NVARCHAR(10) NOT NULL, -- Chuyển tuyến bệnh viện
    new_hospital_name NVARCHAR(50) NULL, -- Tên cơ sở điều trị nếu có chuyển tuyến
    result NVARCHAR(20) NOT NULL, -- Kết quả
    result_date DATE NULL -- Ngày trả kết quả
);

CREATE TABLE administrative_units_information_2023 (
	city_name NVARCHAR(50) NOT NULL, 
	city_id NVARCHAR(50) NOT NULL,
	district NVARCHAR(50) NOT NULL,
	district_id NVARCHAR(50) NOT NULL,
	ward NVARCHAR(50) NOT NULL,
	ward_id NVARCHAR(50) NOT NULL,
	administrative_unit_level NVARCHAR(15) NOT NULL,
	english_name NVARCHAR(50) NULL
);

CREATE TABLE area_and_population_2022 (
	name NVARCHAR(50),
	[square(Km2)] DECIMAL(6,2),
	[average_population(thousands)] DECIMAL(6,2),
	[population_density(person/Km2)] INT
);