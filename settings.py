import os
from sys import platform

BASE_DIR = os.path.abspath(os.curdir)

if platform == 'darwin':
    DRIVER_PATH = f'{BASE_DIR}/drivers/chrome_mac'
elif platform == 'linux':
    DRIVER_PATH = f'{BASE_DIR}/drivers/chrome_linux'
else:
    raise Exception('Unknown OS')

# PROFILE_PATH = f'{BASE_DIR}/firefox_profile'

PASSPORT_NUM = '54553366'
FULL_NAME = 'Alexandr Lukashenko'
BIRTH_YEAR = '1985'
COUNTRY = '149'

DELAY = 5

TG_TOKEN = '5666073037:AAEt-Bae6HG_L0farQc1rdz7jWznUcwtzYY'

PROXY_HOST = 'http://gate.smartproxy.com'
PROXY_PORT = '7000'
