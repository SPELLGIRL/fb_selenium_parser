import os

BASE_DIR = os.path.abspath(__file__)

# Скрытие окна браузера
HEADLESS = True
# Отображение изображений
IMAGES = False
# Отображение flash анимации
FLASH = False
# Использование css (рекомендуется не отключать)
CSS = True
# Отображение всплывающих уведомлений
NOTIFICATIONS = False

# Количество собираемых публикаций
POSTS_COUNT = 5

FB_MAINPAGE = 'https://www.facebook.com/'
FB_USERNAME = 'YOUR EMAIL'
FB_PASSWORD = 'YOUR PASSWORD'

# Использование прокси
USE_PROXY = False
# Использование Tor
USE_TOR = False

FIREFOX_BINARY = r'C:\Program Files\Mozilla Firefox\firefox.exe'

PROXY_HOST = "127.0.0.1"
PROXY_PORT = 9050

TOR_EXE = r'D:\System Files\Program Files\Tor\Tor Browser\Browser\TorBrowser\Tor\tor.exe'
TOR_PROFILE = r'D:\System Files\Program Files\Tor\Tor Browser\Browser\TorBrowser\Data\Browser\profile.default'
