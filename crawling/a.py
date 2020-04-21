from selenium import webdriver
import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome(executable_path='chromedriver.exe')
driver.execute_script('window.open("about:blank", "_blank");')
tabs = driver.window_handles

cities = ['Seoul', 'Busan', 'Daegu', 'Incheon', 'Gwangju', 'Daejeon', 'Ulsan', 'Gyeonggi-do', 'Gangwon-do',
          'Chungcheongbuk-do', 'Chungcheongnam-do', 'Jeollabuk-do', 'Jeollanam-do', 'Gyeongsangbuk-do',
          'Gyeongsangnam-do', 'Jeju-do']


driver.switch_to.window(tabs[0])
driver.get("https://helpx.adobe.com/flash-player.html")

## Step 2  Once your page is loaded in chrome, go to the URL where lock sign is there visit the
##setting page where you will see that the flash is disabled.

## step 3 copy that link and paste below
driver.get("chrome://settings/content/siteDetails?site=https%3A%2F%2Fhelpx.adobe.com")

## below code is for you to reach to flash dialog box and change it to allow from block.
actions = ActionChains(driver)
actions = actions.send_keys(Keys.TAB * 12)
actions = actions.send_keys(Keys.SPACE)
actions = actions.send_keys("a")
actions = actions.send_keys(Keys.ENTER)
actions.perform()

time.sleep(10)
driver.switch_to.window(tabs[1])
driver.get('http://www.dawuljuso.com/')
driver.set_
search_box = driver.find_element_by_css_selector('#input_juso.juso')
search_box.clear()
search_box.send_keys('서울시')

search_button = driver.find_element_by_css_selector('div#btnSch')
search_button.click()

time.sleep(3)
raw_coordinate = driver.find_element_by_css_selector('tr > #insert_data_5').text
print(raw_coordinate)
seperate = raw_coordinate.split(' ')
print(seperate)





time.sleep(10)
driver.close()