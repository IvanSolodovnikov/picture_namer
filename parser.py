from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

URL = 'https://yandex.ru/images?lr=213'
WAIT_TIMEOUT = 3


def get_text(driver, im):
    try:
        # Обновляем страницу перед обработкой нового изображения
        driver.get(URL)
        text = 'Текст не распознан'

        # нажимаем на поиск по фото
        try:
            search_btn = WebDriverWait(driver, WAIT_TIMEOUT).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Поиск по картинке"]'))
            )
        except TimeoutException:
            ...

        search_btn.click()

        # вставляем картинку
        paste_btn = WebDriverWait(driver, WAIT_TIMEOUT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))
        )
        paste_btn.send_keys(im)

        # достаём текст
        try:
            text_element = WebDriverWait(driver, WAIT_TIMEOUT).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'CbirObjectResponse-Title'))
            )
            text = text_element.text.strip()
        except Exception as e:
            ...

        # Альтернативный вариант получения текста
        try:
            tags = WebDriverWait(driver, WAIT_TIMEOUT).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                                                     '.Button.Button_width_auto.Button_view_default.Button_size_l.Button_link.Tags-Item'))
            )
            if tags:
                text = ', '.join(tag.text.strip() for tag in tags if tag.text.strip())
        except Exception as e:
            ...

        try:
            products = WebDriverWait(driver, WAIT_TIMEOUT).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.Link.EProductSnippetTitle'))
            )
            if products:
                text = products[0].text.strip()
        except Exception as e:
            ...

        return text


    except Exception as e:
        ...
        return None

def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    service = Service(ChromeDriverManager().install())
    driver =  webdriver.Chrome(service=service, options=options)
    try:
        driver.get(URL)
        search_btn = WebDriverWait(driver, WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Поиск по картинке"]'))
        )
    except TimeoutException:
        driver.quit()
        driver = create_driver()
    return driver
