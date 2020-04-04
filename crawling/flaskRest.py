from flask import Flask

app = Flask(__name__)

@app.route('/')
def crawling():
    from selenium import webdriver
    import time

    driver = webdriver.Chrome("chromedriver.exe")
    url = ""
    driver.get("")

    driver.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)





