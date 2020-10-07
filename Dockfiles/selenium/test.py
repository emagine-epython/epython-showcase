from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=800x600")
chrome_options.add_argument("--remote-debugging-port=9222")
chrome_driver = '/usr/bin/chromedriver'
driver = webdriver.Chrome(options=chrome_options,
                          executable_path=chrome_driver)
driver.get('http://www.google.com/')
search_box = driver.find_element_by_name('q')
print(search_box)
driver.quit()
