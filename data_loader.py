import pandas as pd
from config import CSV_FILE_PATH

def load_laptop_data():
    df = pd.read_csv(CSV_FILE_PATH)
    return df