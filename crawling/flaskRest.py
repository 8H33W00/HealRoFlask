from flask import Flask, render_template

app = Flask(__name__)

@app.route("/", methods=['GET'])
def main():
    return "Welcome!"

@app.route('/crawling', methods=['GET'])
def crawling():
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

    driver = webdriver.Chrome("chromedriver.exe")

    cities = ['Seoul', 'Busan', 'Daegu', 'Incheon', 'Gwangju', 'Daejeon', 'Ulsan', 'Gyeonggi-do', 'Gangwon-do',
              'Chungcheongbuk-do', 'Chungcheongnam-do', 'Jeollabuk-do', 'Jeollanam-do', 'Gyeongsangbuk-do',
              'Gyeongsangnam-do', 'Jeju-do']

    for city in cities:
        url = 'http://www.hospitalmaps.or.kr/hm/frHospital/hospital_list_1.jsp?s_mid=010100&s_addr_1=' + city + '&s_hosp_gb_cd=01'
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
                img = 'http://www.hospitalmaps.or.kr/hm' + rawImg[2:]
                title = driver.find_element_by_css_selector(
                    f'#DIV_LIST > table > tbody > tr:nth-child({index}) > td:nth-child(2) > b > a').text
                webAddr = driver.find_element_by_css_selector(
                    f'#DIV_LIST > table > tbody > tr:nth-child({index}) > td:nth-child(2) > a:nth-child(4)').text

                if webAddr.find('http') == -1:
                    webAddr = '-'

                print(title)
                print(img)
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

                # DB에 INSERT
                sql = """insert into hospital(hospital_city, hospital_img, hospital_name, hospital_addr, hospital_web, hospital_phone)
                            values (%s, %s, %s, %s, %s, %s)"""
                curs.execute(sql, (city, img, title, test_list2, webAddr, realNum))
                conn.commit()

                driver.back()
                time.sleep(1)
                index += 2
            except:
                break

    conn.close()
    driver.close()

    return render_template('index.html')

if __name__ == '__main__':
    app.run()
    # app.run(host='0.0.0.0', port=5000, debug=True)