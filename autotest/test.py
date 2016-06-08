import time
from selenium import webdriver


driver = webdriver.Firefox()
driver.implicitly_wait(30)
driver.maximize_window()

driver.get("https://www.baidu.com")
search_field = driver.find_element_by_name("wd")
search_field.clear()

# enter search keyword and submit
search_field.send_keys("webdriver")
search_field.submit()

#time.sleep(6)
products = driver.find_elements_by_xpath("//div[@class='result c-container ']")
# get the number of anchor elements found
print "Found " + str(len(products)) + " pages:"

# iterate through each anchor element and
# print the text that is name of the product
for product in products:
    print product.find_element_by_tag_name("a").get_attribute("href")


# close the browser window
driver.quit()