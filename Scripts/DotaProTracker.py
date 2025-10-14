from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from PIL import Image
import io
import re


def get_top_hero_img(pos=None):
    pos_url = ""
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    fox = webdriver.Firefox(options=options)
    match pos:
        case 1:
            pos_url = "pos%2B1"
        case 2:
            pos_url = "pos%2B2"
        case 3:
            pos_url = "pos%2B3"
        case 4:
            pos_url = "pos%2B4"
        case 5:
            pos_url = "pos%2B5"
        case _:
            pos = "all"
            pos_url = "all"

    fox.get(f"https://dota2protracker.com/meta?mmr=7000&position={pos_url}&period=8")

    try:
        close_btn = WebDriverWait(fox, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.absolute.top-3.right-3")
            )
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
    left = location["x"]
    top = location["y"]
    right = left + size["width"]
    bottom = top + size["height"]
    im = im.crop((left, top, right, bottom))
    photo_name = str(pos) + "_top_" + datetime.now().strftime("%H%M%S")
    im.save(f"photo/{photo_name}.png")
    photo_url = f"photo/{photo_name}.png"
    return photo_url


def send_dota2_stat(text):
    text = text.strip("/Dota2_stat")
    if not text:
        return ["Top Heroes by Win Rate(All Positions)", get_top_hero_img()]

    switch = {
        1: ["pos1", "carry", "position 1", "pos 1", "position1", "core"],
        2: ["pos2", "midline", "position 2", "pos 2", "position2", "mid"],
        3: ["pos3", "offlane", "position 3", "pos 3", "position3", "tank"],
        4: ["pos4", "soft", "position 4", "pos 4", "position4", "soft support"],
        5: [
            "pos5",
            "hard",
            "position 5",
            "pos 5",
            "position5",
            "hard support",
            "support",
        ],
    }
    for pos, keywords in switch.items():
        if any(re.search(keyword, text, re.IGNORECASE) for keyword in keywords):
            return [f"Top Heroes by Win Rate({switch[pos][0]})", get_top_hero_img(pos)]
    return [
        "Sorry, I couldn't identify the position.\n"
        "Please specify one of the following Dota positions:\n"
        "- Carry (pos1)\n"
        "- Mid (pos2)\n"
        "- Offlane (pos3)\n"
        "- Soft Support (pos4)\n"
        "- Hard Support (pos5)\n",
        "",
    ]
