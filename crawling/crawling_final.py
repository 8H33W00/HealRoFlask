from selenium import webdriver
import time
import pymysql

conn = pymysql.connect(host='healrodb.ciovcwimqlrt.us-east-2.rds.amazonaws.com',
                       user='healro',
                       password='hongikhealro',
                       db='healrodb',
                       charset='utf8',
                       )

curs = conn.cursor(pymysql.cursors.DictCursor)

# driver = webdriver.Chrome("chromedriver.exe")

# 'Jeju-do', 'Seoul'


# cities = ['Seoul', 'Ulsan', 'Busan', 'Daegu', 'Incheon', 'Gwangju', 'Daejeon', 'Gyeonggi-do', 'Gangwon-do',
#           'Chungcheongbuk-do', 'Chungcheongnam-do', 'Jeollabuk-do', 'Jeollanam-do', 'Gyeongsangbuk-do',
#           'Gyeongsangnam-do', 'Jeju-do']
cities = ['Seoul', 'Gyeonggi-do']
driver = webdriver.Chrome(executable_path='chromedriver.exe')
driver.execute_script('window.open("https://www.google.com/maps/", "_blank");')
tabs = driver.window_handles
driver.switch_to.window(tabs[0])

for city in cities:
    url = 'http://www.hospitalmaps.or.kr/hm/frHospital/hospital_list_1.jsp?s_mid=010100&s_addr_1=' + city + '&s_hosp_gb_cd=01'
    # &s_curr_page=2
    driver.get(url)

    containers = driver.find_elements_by_css_selector('#DIV_LIST > table > tbody > tr')
    print(len(containers))
    index = 1
    for container in containers:
        try:
            # 이미지주소, 병원명, 병원사이트주소 크롤링
            rawImg = driver.find_element_by_css_selector(
                f'#DIV_LIST > table > tbody > tr:nth-child({index}) > td:nth-child(1) > div > img').get_attribute(
                'src')
            # img = 'http://www.hospitalmaps.or.kr/hm' + rawImg[2:]
            title = driver.find_element_by_css_selector(
                f'#DIV_LIST > table > tbody > tr:nth-child({index}) > td:nth-child(2) > b > a').text
            webAddr = driver.find_element_by_css_selector(
                f'#DIV_LIST > table > tbody > tr:nth-child({index}) > td:nth-child(2) > a:nth-child(4)').text

            if webAddr.find('http') == -1:
                webAddr = '-'

            print(title)
            print(rawImg)
            print(webAddr)

            # 상세페이지로 이동
            driver.find_element_by_css_selector(
                f'#DIV_LIST > table > tbody > tr:nth-child({index}) > td:nth-child(2) > b > a').click()

            # 주소 크롤링
            test = driver.find_element_by_css_selector(
                'body > center > table:nth-child(3) > tbody > tr > td > table:nth-child(3) > tbody > tr > td:nth-child(1) > table > tbody > tr:nth-child(4) > td').text
            test_list2 = test.split('TEL')[0][:-1].replace("\'", "").strip()

            if len(test_list2) <= 3:
                test_list2 = '-'

            print(test_list2)

            # 전화번호 크롤링
            test_list = test.split('FAX')
            temp = test_list[0]
            realNum = temp.split('TEL : ')[1][:-1].replace("\'", "").strip()

            if realNum.find('-') == -1:
                realNum = '-'

            print(realNum)

            time.sleep(2)
            # google maps에서 위도, 경도 변환
            driver.switch_to.window(tabs[1])

            driver.implicitly_wait(10)
            # time.sleep(2)

            search_box = driver.find_element_by_css_selector('#gs_lc50 #searchboxinput')
            search_box.clear()
            search_box.send_keys(test_list2)

            search_button = driver.find_element_by_css_selector('.searchbox-searchbutton-container #searchbox-searchbutton')
            search_button.click()

            driver.implicitly_wait(10)
            time.sleep(3)
            try:
                raw_coordinate = driver.current_url
                seperate = raw_coordinate.split('@')[1].split(',')

                latitude = float(seperate[0])
                longitude = float(seperate[1])
                print(latitude, longitude)
            except:
                latitude = 0.0
                longitude = 0.0
                print(latitude, longitude)

            # print(latitude, longitude)
            time.sleep(2)
            driver.implicitly_wait(10)

            # DB에 INSERT
            sql = """insert into hospital(hospital_city, hospital_img, hospital_name, hospital_addr, hospital_web, hospital_phone, hospital_latitude, hospital_longitude)
                        values (%s, %s, %s, %s, %s, %s, %s, %s)"""
            curs.execute(sql, (city, rawImg, title, test_list2, webAddr, realNum, latitude, longitude))
            conn.commit()
            time.sleep(2)
            driver.implicitly_wait(10)

            driver.switch_to.window(tabs[0])
            driver.back()
            time.sleep(1)
            index += 2
        except:
            break

conn.close()
driver.close()

