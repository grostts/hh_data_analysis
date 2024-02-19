import pandas as pd

df = pd.read_csv('vacancy.csv')
print(df["company_name"])