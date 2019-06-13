from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# 欅坂46のメンバーとブログの更新回数のカウンター
members = {
    '石森 虹花': 0, '上村 莉菜': 0, '尾関 梨香': 0, '織田 奈那': 0, \
    '小池 美波': 0, '小林 由依': 0, '齋藤 冬優花': 0, '佐藤 詩織': 0, \
    '菅井 友香': 0, '鈴本 美愉': 0, '長沢 菜々香': 0, '長濱 ねる': 0, \
    '土生 瑞穂': 0, '原田 葵': 0, '平手 友梨奈': 0, '守屋 茜': 0, \
    '渡辺 梨加': 0, '渡邉 理佐': 0, '井上 梨名': 0, '関 有美子': 0, \
    '武元 唯衣': 0, '田村 保乃': 0, '藤吉 夏鈴': 0, '松田 里奈': 0, \
    '松平 璃子': 0, '森田 ひかる': 0, '山﨑 天': 0
}

options = Options()

# options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'

# headlessモードで起動する
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

# 最初に開くページ(クロールの起点となるページ, 欅坂46の公式sブログを想定)
baseUrl = 'http://www.keyakizaka46.com/s/k46o/diary/member/list?ima=0000'

# 欅坂ブログのトップページを開く
driver.get(baseUrl)

# タイトルに欅坂46 公式ブログが含まれていることを確認する
assert '欅坂46 公式ブログ' in driver.title

# 最大10秒待機
wait = WebDriverWait(driver, 10)

while True:
    try:
        # ブログを書いたメンバーの名前を取得できるまで待つ    
        wait.until(expected_conditions.presence_of_element_located((By.XPATH, "//div[@class='box-ttl']/p[@class='name']")))
        names = driver.find_elements_by_xpath("//div[@class='box-ttl']/p[@class='name']")
        for name in names:
            for member in members:
                if member == name.text:
                    members[member] += 1
        # ページネーション要素(>ボタン)を取得できるまで待つ
        wait.until(expected_conditions.presence_of_element_located((By.XPATH, "//div[@class='pager']/ul/li/a")))
        link = driver.find_element_by_xpath("//div[@class='pager']/ul/li[last()]/a")
        link.click()
    except (KeyboardInterrupt, NoSuchElementException, TimeoutException):
        print(members)
        # ウィンドウを閉じる
        driver.quit()
        break