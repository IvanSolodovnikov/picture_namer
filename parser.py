import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from saver import ExcelResultsSaver

URL = 'https://yandex.ru/images'
WAIT_TIMEOUT = 5

def start(images):
    try:
        saver = ExcelResultsSaver()
        wd = create_driver()
        wd.get(URL)
        if images:
            print(f'Found {len(images)} images')
            for image in images:
                text = get_text(wd, image)
                if text:
                    saver.add_result(image, text)
                time.sleep(2)
        saver.save_all()
        wd.quit()
    except Exception as e:
        print(e)

def get_images(driver, path):
    images = []
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        if os.path.isfile(file_path) and filename.endswith(('.jpg', '.png', '.jpeg', '.bmp', '.gif', '.webr')):
            images.append(file_path)
        else:
            print(f'Skipping {filename} - not a image')
    return images


def get_text(driver, im):
    try:
        # Обновляем страницу перед обработкой нового изображения
        driver.get(URL)
        time.sleep(2)  # Даем странице полностью загрузиться

        # нажимаем на поиск по фото
        search_btn = WebDriverWait(driver, WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Поиск по картинке"]'))
        )
        print(f"{'Search button found':.<30}")
        search_btn.click()
        print(f"{'Search button clicked':.<30}")

        # вставляем картинку
        paste_btn = WebDriverWait(driver, WAIT_TIMEOUT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))
        )
        print(f"{'paste_btn found':.<30}")
        paste_btn.send_keys(im)
        print(f"{'paste_btn clicked':.<30}")

        # достаём текст (добавляем проверку на видимость элемента)
        try:
            text_element = WebDriverWait(driver, WAIT_TIMEOUT).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'CbirObjectResponse-Title'))
            )
            text = text_element.text.strip()
            if text:
                return text
        except Exception as e:
            print(f"Не удалось получить основной текст: {e}")

        # Альтернативный вариант получения текста
        try:
            tags = WebDriverWait(driver, WAIT_TIMEOUT).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                                                     '.Button.Button_width_auto.Button_view_default.Button_size_l.Button_link.Tags-Item'))
            )
            if tags:
                return ', '.join(tag.text.strip() for tag in tags if tag.text.strip())
        except Exception as e:
            print(f"Не удалось получить теги: {e}")

        return "Текст не распознан"

    except Exception as e:
        print(f"Ошибка в get_text: {e}")
        return None


    except Exception as e:
        print(e)
        return

def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)
