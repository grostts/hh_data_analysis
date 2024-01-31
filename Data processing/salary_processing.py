import pandas as pd
import re
import requests



#read vacancy csv
vacancy = pd.read_csv('/Users/rostislavgrebensikov/PycharmProjects/hh_data_analysis/Data mining/vacancy.csv')
pd.set_option('display.max_rows', None)


#get echange rate
def get_dollar_exchange_rate():
    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        dollar_exchange_rate = data['Valute']['USD']['Value']
        return dollar_exchange_rate
    else:
        print("Error code:", response.status_code)
        return None


#delete dividers from salary
def del_divider(string: str):
    return string.replace(" ", "")
vacancy['salary'] = vacancy['salary'].apply(del_divider)


#convert all salaries to ₽ format
def salary_handling(string: str):
    type1 = re.compile(r'(\d+)\s*–\s*(\d+)\s*₽')
    type2 = re.compile(r'от\s*(\d+)\s*₽')
    type3 = re.compile(r'до\s*(\d+)\s*₽')
    type4 = re.compile(r'(\d+)\s*–\s*(\d+)\s*\$')
    type5 = re.compile(r'от\s*(\d+)\s*\$')
    type6 = re.compile(r'до\s*(\d+)\s*\$')
    if re.search(type1, string):
        return (int(re.search(type1, string).group(1)) + int(re.search(type1, string).group(2)))/2
    elif re.search(type2, string):
        return int(re.search(type2, string).group(1))
    elif re.search(type3, string):
        return int(re.search(type3, string).group(1))*0.8
    elif re.search(type4, string):
        return ((int(re.search(type4, string).group(1)) +
                 int(re.search(type4, string).group(2)))/2)*get_dollar_exchange_rate()
    elif re.search(type5, string):
        return int(re.search(type5, string).group(1))*get_dollar_exchange_rate()
    elif re.search(type6, string):
        return int(re.search(type6, string).group(1))*0.8*get_dollar_exchange_rate()


vacancy['salary'] = vacancy['salary'].apply(salary_handling)
print(vacancy)

