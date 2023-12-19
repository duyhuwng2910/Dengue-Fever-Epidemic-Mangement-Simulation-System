import pandas as pd

area_and_population_data = pd.read_csv("Data/Public data/Administrative units data/Diện tích, dân số, mật độ dân số (2022).csv", encoding='utf-8', header=0)

df = pd.DataFrame(area_and_population_data)

print(df.dtypes)

print(df)