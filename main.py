import time

import undetected_chromedriver
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from settings import (BIRTH_YEAR, COUNTRY, DELAY, DRIVER_PATH, FULL_NAME,
                      PASSPORT_NUM, PROXY_HOST, PROXY_PORT, TG_TOKEN)

URL = 'https://icp.administracionelectronica.gob.es/icpco/citar?p=3&locale=es'
# URL = 'https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html'
# URL = 'https://2ip.ru'


def get_driver():
    useragent = UserAgent(use_cache_server=True)

    options = undetected_chromedriver.ChromeOptions()
    options.add_argument(f'user-agent={useragent.random}')

    driver = undetected_chromedriver.Chrome(options=options)

    return driver


def main():
    driver = get_driver()

    try:
        driver.get(URL)

        # Cookie footer click
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'cookie_action_close_header'))).click()

        # Choice office
        oficina_select = Select(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'sede'))))
        oficina_select.select_by_value('14')

        # Choice service
        service_select = Select(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'tramiteGrupo[0]'))))
        service_select.select_by_value('4031')

        # Click next button
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'btnAceptar'))).click()

        # Click enter button
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'btnEntrar'))).click()

        # Page with data
        next_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'btnEnviar')))

        # Passport number
        driver.find_element(By.ID, 'txtIdCitado').send_keys(PASSPORT_NUM)
        # Name Surname
        driver.find_element(By.ID, 'txtDesCitado').send_keys(FULL_NAME)
        # Year of birth
        driver.find_element(By.ID, 'txtAnnoCitado').send_keys(BIRTH_YEAR)
        # Country
        country_select = Select(driver.find_element(By.ID, 'txtPaisNac'))
        country_select.select_by_value(COUNTRY)

        next_btn.click()

        # Finish button
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'btnEnviar'))).click()

        while True:
            response = driver.page_source
            if 'En este momento no hay citas disponibles.' in response:
                driver.refresh()
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'html')))
                time.sleep(DELAY)
                continue
            if '<h1>Too Many Requests</h1>' in response:
                time.sleep(300)
                driver.refresh()
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'html')))
                continue
            break

        driver.get_screenshot_as_file('screen.jpg')

    except Exception as error:
        print(error)
    finally:
        driver.close()
        driver.quit()


if __name__ == '__main__':
    main()
