from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import xlsxwriter
import time
import Urls

# Import Urls
urls = Urls.input_()
#Set up the webdriver

CHROMEDRIVER_PATH = 'Z:\SeleniumScrape\chromedriver.exe'
WINDOW_SIZE = "1920,1080"

chrome_options = Options()
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)

driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,
                        chrome_options=chrome_options
                        )
inEx = Urls.InputHandler("for_price_mining.xlsx")
#Initalize Excel File
workbook = xlsxwriter.Workbook('DataBase.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write(0,0,'Product ')
worksheet.write(1,0,)
worksheet.write(2,0,)
worksheet.write(3,0,)
worksheet.write(4,0,)


i = 0
for url in urls:
    driver.get("https://www.skroutz.gr/s/23141882/Apple-iPhone-SE-2020-64GB-Product-Red.html")
    time.sleep(1)
    pr_type = driver.find_element_by_css_selector('body')
    pr_type = pr_type.get_attribute('id')
    print(pr_type)

    if pr_type == 'skus_show':
        elements = driver.find_elements_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "item", '
                                                 '" " ))]//*[contains(concat( " ", @class, " " ), concat( " ", '
                                                 '"content-placeholder", " " ))]')
        print(len(elements))
        for element in elements:
            var = element.location_once_scrolled_into_view
            time.sleep(1)
        res = driver.execute_script("return document.documentElement.outerHTML")

        products = driver.find_elements_by_css_selector(".js-product-card")
        for product in products:
            shop_name = product.find_element_by_css_selector(".shop-name").text
            final_price = product.find_element_by_css_selector(
                ".final-price .content-placeholder , .not-supported").text
            antikataboli = product.find_elements_by_css_selector("em")
            price = product.find_element_by_css_selector(".product-link").text
            shipping = product.find_element_by_css_selector(".content-placeholder+ .cf em").text
            availability = product.find_element_by_css_selector(".instock, .availability").text

            print(shop_name + ": " + final_price + " = " + antikataboli[1].text + " + " + shipping + " + " + price + ' ' + availability)
        i += 1

driver.quit()

for element in elements:
    var = element.location_once_scrolled_into_view
    time.sleep(1)
res = driver.execute_script("return document.documentElement.outerHTML")

products = driver.find_elements_by_css_selector(".js-product-card")
for product in products:
    shop_name = product.find_element_by_css_selector(".shop-name").text
    final_price = product.find_element_by_css_selector(".final-price .content-placeholder , .not-supported").text
    antikataboli = product.find_elements_by_css_selector("em")
    price = product.find_element_by_css_selector(".product-link").text
    shipping = product.find_element_by_css_selector(".content-placeholder+ .cf em").text

    print(shop_name + ": " + final_price + " = " + antikataboli[1].text + " + " + shipping + " + " + price)

driver.quit()
