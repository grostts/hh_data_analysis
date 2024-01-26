import pandas as pd
import os

print(os.listdir())
vacancy = pd.read_csv('vacancy.csv')
print(vacancy)