
from selenium import webdriver


driver = webdriver.Firefox()
driver.get('http://0.0.0.0:5000/input_custom_data')
element = driver.find_element_by_name('input_data')
element.send_keys(120)  # input custom number for test
element = driver.find_element_by_id('send')
element.click()
driver.get('http://0.0.0.0:5000/')
element = driver.find_element_by_id('calculate')
element.click()
elem = driver.find_element_by_id('result_worker')
if elem != 0:
    print elem.text
driver.close()




