from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

CHROMEDRIVER = "/usr/bin/chromedriver"


def get_driver():
    # 　ヘッドレスモードでブラウザを起動
    options = Options()
    options.add_argument("--headless")

    # ブラウザーを起動
    driver = webdriver.Chrome(CHROMEDRIVER, options=options)

    return driver


def extract_td_text(row):
    td = row.find_element(By.TAG_NAME, "td")
    try:
        span = td.find_element(By.TAG_NAME, "span")
        return span.text
    except NoSuchElementException:
        return td.text


def extract_td_text_if_exist_element(row_list):
    if len(row_list) > 0:
        return extract_td_text(row_list[0])
    else:
        return None


if __name__ == "__main__":
    url = "https://cocktaillog.com/ja/cocktails?page={}"

    driver = get_driver()

    N_PAGES = 913
    for page in range(1, N_PAGES + 1):
        page_url = url.format(page)

        # urlにアクセス
        driver.get(page_url)

        items = driver.find_elements(By.CLASS_NAME, "item_section")
        for item in items:
            # カクテル名
            name = item.find_element(By.CLASS_NAME, "name_text")
            print(name.text)

            # 材料
            materials_table = item.find_element(By.TAG_NAME, "tbody")
            materials = materials_table.find_elements(By.CLASS_NAME, "align_left")
            quantities = materials_table.find_elements(By.CLASS_NAME, "align_right")
            for material, quantity in zip(materials, quantities):
                print("{} {}".format(material.text, quantity.text))

            # 説明
            description_div = item.find_element(By.CLASS_NAME, "item_remark")
            description = description_div.find_element(By.TAG_NAME, "span").text
            print(description)

            # 画像
            try:
                photo_button = item.find_element(By.CLASS_NAME, "photo_button")
                image = photo_button.find_element(By.TAG_NAME, "img").get_attribute(
                    "src"
                )
            except NoSuchElementException:
                image = None
            print(image)

            # 技法とかグラスとか
            other_info_box = item.find_element(By.CLASS_NAME, "lower_box")
            other_info_table = other_info_box.find_element(By.TAG_NAME, "tbody")
            other_infos = other_info_table.find_elements(By.TAG_NAME, "tr")

            def compare_th(row, th_except):
                try:
                    th_actual = row.find_element(By.TAG_NAME, "th").text
                    # print(th_actual)
                    return th_actual == th_except
                except Exception:
                    return False

            # 技法
            technique_list = list(
                filter(lambda row: compare_th(row, "技法"), other_infos)
            )
            technique = extract_td_text_if_exist_element(technique_list)
            print(technique)

            # グラス
            glass_list = list(filter(lambda row: compare_th(row, "グラス"), other_infos))
            glass = extract_td_text_if_exist_element(glass_list)
            print(glass)

            # アルコール
            alcohol_list = list(
                filter(lambda row: compare_th(row, "アルコール"), other_infos)
            )
            alcohol = extract_td_text_if_exist_element(alcohol_list)
            print(alcohol)

            input()

    # ブラウザ停止
    driver.quit()
