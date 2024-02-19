from bs4 import BeautifulSoup
import time
import requests
import csv


start_time = time.time()
job_vacancy_data_list = []


def gather_data(page):
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/"
                  "*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/"
                      "91.0.4472.106 Safari/537.36"
    }

    url = (f"https://hh.ru/search/vacancy?area=1&search_field=name&search_field=company_name&search_field=description&"
           f"enable_snippets=true&text=%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D1%82%D0%B8%D0%BA+"
           f"%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85&only_with_salary=true&page={page}")
    req = requests.get(headers=headers, url=url)

    vacancy_file = f"data/vacancy_{page}"

    with open(f'{vacancy_file}.html', 'w', encoding='utf-8') as file:
        file.write(req.text)

    with open(f'{vacancy_file}.html', 'r', encoding='utf-8') as file:
        scrap = file.read()

    soup = BeautifulSoup(scrap, "lxml")


    vacancy = soup.find_all(class_="vacancy-serp-item__layout")

    for el in vacancy:
        # get url of the current vacancy
        vacancy_url = el.find(class_="bloko-link").get("href")
        # get title of the current vacancy
        vacancy_title = el.find(class_='serp-item__title').text
        # get company name of the current vacancy
        vacancy_company_name = el.find(class_="vacancy-serp-item__meta-info-company").text
        # get experience of the current vacancy
        vacancy_experience = el.find(class_="bloko-h-spacing-container bloko-h-spacing-container_base-0").text
        # get salary of the current vacancy
        vacancy_salary = el.find(class_="bloko-header-section-2").text

        job_vacancy_data_list.append(
            {
                "salary": vacancy_salary,
                "title": vacancy_title,
                "url": vacancy_url,
                "company_name": vacancy_company_name,
                "experience": vacancy_experience
            }
        )



def main():
    for page in range(0, 39):
        gather_data(page)
        current_time = time.time() - start_time
        print(f"Information from page {page} was downloded. {round(current_time, 2)} seconds have passed.")

    "create csv file with vacancy data"
    columns = ['salary', 'title', 'url', 'company_name', 'experience']
    with open('vacancy.csv', 'a', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=columns, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        for row in job_vacancy_data_list:
            writer.writerow(row)

    finish_time = time.time() - start_time
    print(f"Total time is {round(finish_time, 2)}")


main()