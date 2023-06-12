from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from tqdm import tqdm

from table import Table
from tablewriter import TableCsvWriter

CHROMEDRIVER = "/usr/bin/chromedriver"

# DB用インスタンス準備
cocktail_table = Table(
    "cocktail", ["name", "description", "alcohol", "glass_id", "technique_id", "image"]
)
drink_table = Table("drink", ["name"], 0)
glass_table = Table("glass", ["name"], 0)
technique_table = Table("technique", ["name"], 0)
cocktail_drink_table = Table("cocktail_drink", ["cocktail_id", "drink_id", "quantity"])


def add_cocktail_to_db_instance(
    name, description, alcohol, glass, technique, image, materials, quantities
):
    # drinkテーブル用インスタンスにデータ追加
    drink_ids = []
    for material in materials:
        drink_id = drink_table.idx_of(material)
        if drink_id is None:
            drink_table.add([material])
            drink_id = len(drink_table) - 1
        drink_ids.append(drink_id)

    # glassテーブル用インスタンスにデータ追加
    glass_id = glass_table.idx_of(glass)
    if glass_id is None:
        glass_table.add([glass])
        glass_id = len(glass_table) - 1

    # techniqueテーブル用インスタンスにデータ追加
    technique_id = technique_table.idx_of(technique)
    if technique_id is None:
        technique_table.add([technique])
        technique_id = len(technique_table) - 1

    # cocktailテーブル用インスタンスにデータ追加
    cocktail_table.add([name, description, alcohol, glass_id, technique_id, image])
    cocktail_id = len(cocktail_table) - 1

    # cocktail_drinkテーブル用インスタンスにデータ追加
    for drink_id, quantity in zip(drink_ids, quantities):
        cocktail_drink_table.add([cocktail_id, drink_id, quantity])


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
    for page in tqdm(range(1, N_PAGES + 1)):
        page_url = url.format(page)

        # urlにアクセス
        driver.get(page_url)

        items = driver.find_elements(By.CLASS_NAME, "item_section")
        for item in items:
            # カクテル名
            name = item.find_element(By.CLASS_NAME, "name_text").text
            # print(name.text)

            # 材料
            materials_tb = item.find_element(By.TAG_NAME, "tbody")
            materials = [
                m.text for m in materials_tb.find_elements(By.CLASS_NAME, "align_left")
            ]
            quantities = [
                q.text for q in materials_tb.find_elements(By.CLASS_NAME, "align_right")
            ]
            # for material, quantity in zip(materials, quantities):
            #     print("{} {}".format(material.text, quantity.text))

            # 説明
            try:
                description_div = item.find_element(By.CLASS_NAME, "item_remark")
                description = description_div.find_element(By.TAG_NAME, "span").text
            except NoSuchElementException:
                description = None
            # print(description)

            # 画像
            try:
                photo_button = item.find_element(By.CLASS_NAME, "photo_button")
                image = photo_button.find_element(By.TAG_NAME, "img").get_attribute(
                    "src"
                )
            except NoSuchElementException:
                image = None
            # print(image)

            # 技法とかグラスとか
            other_info_box = item.find_element(By.CLASS_NAME, "lower_box")
            other_info_tb = other_info_box.find_element(By.TAG_NAME, "tbody")
            other_infos = other_info_tb.find_elements(By.TAG_NAME, "tr")

            def compare_th(row, th_except):
                try:
                    th_actual = row.find_element(By.TAG_NAME, "th").text
                    return th_actual == th_except
                except Exception:
                    return False

            # 技法
            technique_list = list(
                filter(lambda row: compare_th(row, "技法"), other_infos)
            )
            technique = extract_td_text_if_exist_element(technique_list)
            # print(technique)

            # グラス
            glass_list = list(filter(lambda row: compare_th(row, "グラス"), other_infos))
            glass = extract_td_text_if_exist_element(glass_list)
            # print(glass)

            # アルコール
            alcohol_list = list(
                filter(lambda row: compare_th(row, "アルコール"), other_infos)
            )
            alcohol = extract_td_text_if_exist_element(alcohol_list)
            # print(alcohol)

            add_cocktail_to_db_instance(
                name,
                description,
                alcohol,
                glass,
                technique,
                image,
                materials,
                quantities,
            )

    TableCsvWriter.write(cocktail_table, "data")
    TableCsvWriter.write(drink_table, "data")
    TableCsvWriter.write(glass_table, "data")
    TableCsvWriter.write(technique_table, "data")
    TableCsvWriter.write(cocktail_drink_table, "data")

    # ブラウザ停止
    driver.quit()
