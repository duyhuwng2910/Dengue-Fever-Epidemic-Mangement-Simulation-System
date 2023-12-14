import pandas as pd

def extract_xlsx_file_1():
    df = pd.read_excel("Data/Public data/Medical center data/bệnh viện thuộc bộ ngành khác.xlsx", skiprows=3, usecols=lambda x:x != "STT ")

    df.to_csv("Data/Public data/Medical center data/bệnh viện thuộc bộ ngành khác.csv", index=False)


def extract_xlsx_file_2():
    df = pd.read_excel("Data/Public data/Medical center data/cơ sở tuyến tw.xlsx", skiprows=3, usecols=lambda x:x != "STT ")
    
    df.to_csv("Data/Public data/Medical center data/cơ sở tuyến tw.csv", index=False)


def extract_xlsx_file_3():
    df = pd.read_excel("Data/Public data/Medical center data/cơ sở tuyến tỉnh.xlsx", skiprows=3, usecols=lambda x:x != "STT ")
    
    df.to_csv("Data/Public data/Medical center data/cơ sở tuyến tỉnh.csv", index=False)
    
    
def extract_xlsx_file_4():
    df = pd.read_excel("Data/Public data/Medical center data/cơ sở tuyến huyện.xlsx", skiprows=3, usecols=lambda x:x != "STT ")
    
    df.to_csv("Data/Public data/Medical center data/cơ sở tuyến huyện.csv", index=False)


extract_xlsx_file_1()
extract_xlsx_file_2()
extract_xlsx_file_3()
extract_xlsx_file_4()