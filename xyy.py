from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options


def main():
    options = Options()
    options.add_argument('-headless')
    driver = Firefox(executable_path='/usr/local/bin/geckodriver', firefox_options=options)
    driver.get("http://uland.taobao.com/sem/tbsearch?spm=a2e15.8261149.07626516003.1.722e29b4oSJgTh&refpid=mm_26632258_3504122_32538762&clk1=0bd2b02e5a13ebfb74b4518ebb51633d&keyword=%E4%B9%90%E9%AB%98&page=2&_input_charset=utf-8")
    #driver.find_element_by_xpath('//div[@class="search-combobox-input-wrap"]/input').send_keys('乐高')
    #driver.find_element_by_xpath('//button[@class="btn-search tb-bg"]').click()
    print(driver.page_source)
    driver.close()


if __name__ == '__main__':
    main()