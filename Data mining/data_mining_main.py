from bs4 import BeautifulSoup
import time
import asyncio
import aiohttp
import csv


start_time = time.time()
job_vacancy_data_list = []


async def get_current_vacancy_data(session, vacancy_url, vacancy_title):
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/"
                  "*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/"
                      "91.0.4472.106 Safari/537.36"
    }
    async with session.get(url=vacancy_url, headers=headers) as response:
        response_text = await response.text()

        soup = BeautifulSoup(response_text, 'lxml')

        """Get info for every vacancy"""

        """Get salary"""
        try:
            vacancy_salary = soup.find(class_="vacancy-title").find(class_='bloko-header-'
                                                                    'section-2 bloko-header-section-2_lite').text
        except Exception:
            vacancy_salary = "No salary info"

        """Get company name"""
        try:
            vacancy_company_name = soup.find("span", class_="vacancy-company-name").text
        except Exception:
            vacancy_company_name = "No company name info"

        """Get experience"""
        try:
            vacancy_experience = soup.find(class_="vacancy-description-list-item").text
        except Exception:
            vacancy_experience = "No experience info"

        job_vacancy_data_list.append(
            {
                "salary": vacancy_salary,
                "title": vacancy_title,
                "url": vacancy_url,
                "company_name": vacancy_company_name,
                "experience": vacancy_experience
            }
        )





async def gather_data(page):
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/"
                  "*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/"
                      "91.0.4472.106 Safari/537.36"
    }

    # url = f"https://hh.ru/vacancies/analitik-dannyh?page={page}"
    url = (f"https://hh.ru/search/vacancy?area=1&search_field=name&search_field=company_name&search_field=description&"
           f"enable_snippets=true&text=%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D1%82%D0%B8%D0%BA+"
           f"%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85&only_with_salary=true&page={page}")


    async with aiohttp.ClientSession(trust_env=True) as session:
        response = await session.get(url=url, headers=headers)
        soup = BeautifulSoup(await response.text(), "lxml")

        vacancy = soup.find_all(class_="vacancy-serp-item-body__main-info")
        vacancy_urls = []
        vacancy_titles = []
        for el in vacancy:
            #get url of the current vacancy
            vacancy_url = el.find(class_="bloko-link").get("href")
            vacancy_urls.append(vacancy_url)
            #get title of the current vacancy
            vacancy_title = el.find(class_='serp-item__title').text
            vacancy_titles.append(vacancy_title)
            # # get company name of the current vacancy
            # vacancy_company_name = soup.find(class_="vacancy-serp-item__meta-info-company").text
            #
            #
            #
            # vacancy_experience = soup.find(class_="bloko-h-spacing-container bloko-h-spacing-container_base-0").text


        tasks = []

        for vacancy_url, vacancy_title in zip(vacancy_urls, vacancy_titles):
            task = asyncio.create_task(get_current_vacancy_data(session, vacancy_url, vacancy_title))
            tasks.append(task)
        await asyncio.gather(*tasks)



def main():
    for page in range(0, 39):
        asyncio.run(gather_data(page))
        current_time = time.time() - start_time
        print(f"Information from page {page} was downloded. {round(current_time, 2)} seconds have passed.")


    "create csv file with vacancy data"
    columns = ['salary', 'title', 'url', 'company_name', 'experience']
    with open('vacancy.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=columns, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        for row in job_vacancy_data_list:
            writer.writerow(row)

    finish_time = time.time() - start_time
    print(f"Total time is {round(finish_time, 2)}")


main()