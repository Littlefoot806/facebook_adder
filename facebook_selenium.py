from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from time import sleep
from datetime import date, timedelta
import logging

def start_webdriver():
    logging.info('Starting webdriver')
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome(chrome_options=chrome_options)
    #driver = webdriver.Firefox()
    driver.get("https://www.facebook.com/")
    sleep(2)
    return driver

def loggining(driver, login, passwd):
    try:
        logging.info('Authorization')
        login_elem = driver.find_element_by_xpath('//input[@id="email"]')
        login_elem.clear()
        login_elem.send_keys(login)
        #ogin_elem.send_keys(Keys.RETURN)

        sleep(2)

        pass_elem = driver.find_element_by_xpath('//input[@id="pass"]')
        pass_elem.clear()
        pass_elem.send_keys(passwd)
        pass_elem.send_keys(Keys.RETURN)
        sleep(2)
        return True
    except Exception as e:
        logging.critical(e)
        return False

def get_data(driver, group):

    driver.get(group)

    for _ in range(20):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(1)
    members = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH , '//button[text()="Add Friend" and not(contains(@class, "hidden"))]')))
    names =  WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH , '//button[text()="Add Friend" and not(contains(@class, "hidden"))]/../../../../../../div[contains(@class, "uiProfileBlockContent")]//div/a')))
    count = 0

    for add, name in zip(members, names):
        
        if count == 50:
            break
        count += 1
        driver.execute_script("arguments[0].scrollIntoView();", name)
        driver.execute_script("window.scrollBy(0, -200);")
        sleep(2)
        
        try:
            confirm = driver.find_element_by_xpath('//div[@role="dialog"]//button[contains(@class,"layerConfirm")]')
            confirm.click()
            sleep(1)
            print('confirm')
        except Exception as e:
            print(e)
            

        try:
            add.click()
            print('[+] "{}" is added'.format(name.get_attribute('textContent')))
        except:
            print('[-] cant add "{}"'.format(name.get_attribute('textContent')))
            driver.save_screenshot("{}.png".format(name.get_attribute('textContent')))
    return count

def main():
    login = "pawlik806@gmail.com" # facebook email
    passwd = "pawlik806"      # facebook password
    group = "https://www.facebook.com/groups/241830595964149/"+"members/" 
    # Менять только ссылку на группу или числовой id
    
    driver = start_webdriver()

    if loggining(driver, login, passwd):
        count = get_data(driver, group)
        print(count)
        driver.quit()
        return count
    else:
        logging.critical('Failed Authorization')
        driver.quit()
        return False


if __name__ == '__main__':
    main()