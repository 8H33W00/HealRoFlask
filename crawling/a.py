from selenium import webdriver
import time

driver = webdriver.Chrome("chromedriver.exe")

cities = ['Seoul', 'Busan', 'Daegu', 'Incheon', 'Gwangju', 'Daejeon', 'Ulsan', 'Gyeonggi-do', 'Gangwon-do',
          'Chungcheongbuk-do', 'Chungcheongnam-do', 'Jeollabuk-do', 'Jeollanam-do', 'Gyeongsangbuk-do',
          'Gyeongsangnam-do', 'Jeju-do']


url = 'http://www.dawuljuso.com/index.php'
driver.get(url)

search_box = driver.find_element_by_css_selector('#input_juso')
search_box.send_keys('서울시 마포구 토정로 11길 47-1')

search_button = driver.find_element_by_css_selector('#btnSch')
search_button.click()

