from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from PIL import Image
import io

def get_top_hero_img(pos=None):
    pos_url =''
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    fox = webdriver.Firefox(options=options)
    match pos:
        case 1:
            pos_url = 'pos%2B1'
        case 2:
            pos_url = 'pos%2B2'
        case 3:
            pos_url = 'pos%2B3'
        case 4:
            pos_url = 'pos%2B4'
        case 5:
            pos_url = 'pos%2B5'
        case _:
            pos = "all"
            pos_url = 'all'
    

    fox.get(f'https://dota2protracker.com/meta?mmr=7000&position={pos_url}&period=8')

    try:
        close_btn = WebDriverWait(fox, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.absolute.top-3.right-3"))
        )
        close_btn.click()
    except Exception as e:
        print("No popup or close button found:", e)

    element = WebDriverWait(fox, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".w-full.mb-6"))
    )
    location = element.location_once_scrolled_into_view
    size = element.size

    png = fox.get_screenshot_as_png()
    fox.quit()

    im = Image.open(io.BytesIO(png))
    left = location['x']
    top = location['y']
    right = left + size['width']
    bottom = top + size['height']
    im = im.crop((left, top, right, bottom))
    photo_name = str(pos) + "_top_" + datetime.now().strftime("%H%M%S")
    im.save(f'Photo/{photo_name}.png')
    photo_url = f'Photo/{photo_name}.png'
    return photo_url


get_top_hero_img()
get_top_hero_img(5)