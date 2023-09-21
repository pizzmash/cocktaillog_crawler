from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from tqdm import tqdm

from table import Table
from tablewriter import TableCsvWriter

CHROMEDRIVER = "/usr/bin/chromedriver"

# DB用インスタンス準備
drink_kinds_table = Table("drink_kinds", ["name"], 0)


def get_driver():
    # 　ヘッドレスモードでブラウザを起動
    options = Options()
    options.add_argument("--headless")

    # ブラウザーを起動
    driver = webdriver.Chrome(CHROMEDRIVER, options=options)

    return driver


if __name__ == "__main__":
    url = "https://cocktaillog.com/ja/ingredients"

    driver = get_driver()

    # urlにアクセス
    driver.get(url)

    sections = driver.find_elements(By.CLASS_NAME, "material_menu_list")

    for items in sections:
        for drink_kinds in items.find_elements(By.CLASS_NAME, "link_text"):
            drink_kinds_table.add([drink_kinds.text])

    TableCsvWriter.write(drink_kinds_table, "data")

    # ブラウザ停止
    driver.quit()
