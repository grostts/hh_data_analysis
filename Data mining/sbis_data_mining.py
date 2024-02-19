import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from sbis_auth import sbis_password
from sbis_auth import sbis_login
import pandas as pd
import glob

start_time = time.time()



# Using Selenium
url = 'https://online.sbis.ru'

# set webdriver options
chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : "/Users/rostislavgrebensikov/PycharmProjects/hh_data_analysis/Data mining/data"}
chromeOptions.add_experimental_option("prefs",prefs)
chromeOptions.add_argument("--disable-blink-features=AutomationControlled")
# headless mode
# chromeOptions.headless = True
driver = webdriver.Chrome(options=chromeOptions)


try:
    print('Login Sbis Website...')
    # Open and login  Sbis website
    driver.get(url=url)
    time.sleep(5)

    # entering a email
    # login_input_class = ("controls-Field js-controls-Field controls-InputBase__nativeField controls-InputBase__nativeField"
    #                      "_caretFilled controls-InputBase__nativeField_caretFilled_theme_default   controls-InputBase__"
    #                      "nativeField_hideCustomPlaceholder")
    login_input = driver.find_element(By.CLASS_NAME, 'controls-InputBase__placeholder controls-InputBase__placeholder_displayed-under-caret')
    login_input.clear()
    login_input.send_keys(sbis_login)
    driver.implicitly_wait(10)
    time.sleep(20)

    # press login button
    login_button_class = ("controls-BaseButton__wrapper controls-Button__wrapper_viewMode-filled controls-BaseButton__"
                          "wrapper_captionPosition_end controls-Button_textAlign-center controls-Button__wrapper_filled_4xl")
    login_button_click = driver.find_element(By.CLASS_NAME, login_button_class).click()
    driver.implicitly_wait(20)
    time.sleep(10)




    # # Open ariel parts page
    # driver.get(url='https://www.arielcorp.com/parts/portal/')
    # driver.implicitly_wait(10)
    #
    # # press equipment button
    # equipment_button = driver.find_element(By.ID, 'tab-1449-btnInnerEl')
    # equipment_button.click()
    # driver.implicitly_wait(10)
    #
    # print('Start downloading the bom files...')
    # counter = 0
    # for elem in serial_numbers:
    #     # fill in the field with the serial number
    #     text_field = driver.find_element(By.ID, 'textfield-1181-inputEl')
    #     text_field.clear()
    #     text_field.send_keys(elem)
    #
    #     # press search button
    #     search_button = driver.find_element(By.ID, 'button-1186')
    #     search_button.click()
    #     driver.implicitly_wait(10)
    #
    #     try:
    #         # press parts button
    #         parts_button = driver.find_element(By.ID, 'button-1202-btnEl')
    #         parts_button.click()
    #         driver.implicitly_wait(10)
    #         try:
    #             # press view as list button
    #             view_as_list_button = driver.find_element(By.ID, 'button-1246-btnEl')
    #             view_as_list_button.click()
    #             driver.implicitly_wait(10)
    #
    #             # downloading BOM file
    #             download_button = driver.find_element(By.ID, 'button-1241-btnInnerEl')
    #             download_button.click()
    #             driver.implicitly_wait(10)
    #         except:
    #             # downloading BOM file
    #             download_button = driver.find_element(By.ID, 'button-1241-btnInnerEl')
    #             download_button.click()
    #             driver.implicitly_wait(10)
    #
    #         # back to the equipment page
    #         back = driver.find_element(By.ID, 'button-1288-btnInnerEl')
    #         back.click()
    #         driver.implicitly_wait(30)
    #
    #         counter += 1
    #         current_time = time.time()
    #
    #         print(f'{counter}/ {total_sn} was downloaded. {round(current_time - start_time, 1)} seconds have passed.')
    #
    #     finally:
    #         continue
    # time.sleep(10)


except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()

#
# # Create excel file
# # getting excel files to be merged from the Downloads
# path = "C:\\Users\\hp\\GitHubProjects\\ArielSparePartsDatabase\\Downloads"
#
# # read all the files with extension .xlsx i.e. excel
# filenames = glob.glob(path + "\*.xlsx")
#
# # empty data frame for the new output excel file with the merged excel files
# outputxlsx = pd.DataFrame()
#
# # for loop to iterate all excel files
# for file in filenames:
#    # using concat for excel files
#    # after reading them with read_excel()
#    df = pd.concat(pd.read_excel( file, sheet_name=None), ignore_index=True, sort=False)
#
#    # appending data of excel files
#    outputxlsx = outputxlsx._append( df, ignore_index=True)
#
# print(f'Final Excel sheet now generated at the same location: C:\\Users\\hp\\GitHubProjects\\Ariel\\ArielSparePartsDatabase\\Result_{file_name}.xlsx')
# outputxlsx.to_excel(f"C:\\Users\\hp\\GitHubProjects\\ArielSparePartsDatabase\\Result_{file_name}.xlsx", index=False)
#
# # Program runtime output
# end_time = time.time()
# elapsed_time = end_time - start_time
# print(f'Program running time  = {round(elapsed_time)} seconds')