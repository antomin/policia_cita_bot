import time

import requests
from seleniumwire import webdriver
# from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from settings import BIRTH_YEAR, DELAY, DRIVER_PATH, FULL_NAME, PASSPORT_NUM, TG_TOKEN
from proxy_settings import PROXY_PASSWORD, PROXY_USERNAME, PROXY_LIST

URL = 'https://icp.administracionelectronica.gob.es/icpco/citar?p=3&locale=es'


def sent_to_telegram(message: str):
    requests.get(f'https://api.telegram.org/bot{TG_TOKEN}/sendMessage?chat_id=@sita_policia_ch&text={message}')


def get_driver():
    options = webdriver.ChromeOptions()
    proxy_options = {
        'proxy': {'https': f'https://{PROXY_USERNAME}:{PROXY_PASSWORD}@{next(PROXY_LIST)}'}
    }
    return webdriver.Chrome(executable_path=DRIVER_PATH, options=options, seleniumwire_options=proxy_options)


def make_enter(driver: webdriver.Chrome):
    driver.get(URL)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'html')))

    select_office = Select(driver.find_element(By.ID, 'sede'))
    select_office.select_by_value('14')

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'tramiteGrupo[0]')))

    select_service = Select(driver.find_element(By.ID, 'tramiteGrupo[0]'))
    select_service.select_by_value('4031')

    driver.find_element(By.ID, 'cookie_action_close_header').click()

    btn_next = driver.find_element(By.ID, 'btnAceptar')
    btn_next.click()

    btn_next = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'btnEntrar')))
    btn_next.click()

    btn_next = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'btnEnviar')))

    driver.find_element(By.ID, 'txtIdCitado').send_keys(PASSPORT_NUM)
    driver.find_element(By.ID, 'txtDesCitado').send_keys(FULL_NAME)
    driver.find_element(By.ID, 'txtAnnoCitado').send_keys(BIRTH_YEAR)

    select_country = Select(driver.find_element(By.ID, 'txtPaisNac'))
    select_country.select_by_value('149')

    btn_next.click()

    btn_next = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'btnEnviar')))
    btn_next.click()

    return driver


def main():
    driver = get_driver()
    try:
        driver = make_enter(driver)

        while True:
            response = driver.page_source

            if 'En este momento no hay citas disponibles.' in response:
                driver.refresh()
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'html')))
                time.sleep(DELAY)
                continue

            if '<h1>Too Many Requests</h1>' in response:
                sent_to_telegram('Блокировка!!!')
                driver = get_driver()
                driver = make_enter(driver)
                continue
            break

        sent_to_telegram('НОВЫЙ ОТВЕТ!!!')
        driver.get_screenshot_as_file('screen.jpg')
        waiter = input('what next?')

    except Exception as error:
        print(error)

    finally:
        driver.close()
        driver.quit()


if __name__ == '__main__':
    main()
