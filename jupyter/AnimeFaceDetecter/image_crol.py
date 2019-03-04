from selenium import webdriver
from time import sleep

web = webdriver.Chrome('./chromedriver.exe')

url_list = dict()
def get_link(driver, count):
    try:
        url = driver.find_element_by_xpath("""//*[@id="{}"]/div[2]/a""".format(count))\
            .get_attribute('href')\
            .split('t_id=')[1]\
            .split('&')[0]
    except Exception:
        return ''
    if url in url_list.keys():
        return ''
    url_list[url] = True
    return url

def scrol(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight); return 10")
    
def one_day(driver, download_image_count):
    scrol(driver)
    sleep(5)
    page_ids = []
    for i in range(download_image_count):
        link = get_link(driver, i+1)
        if not link:
            continue
        page_ids.append(link)
    return page_ids


def next_date(now):
    day = get_day(now)
    mon = get_mon(now)
    year = get_year(now)
    if day > 28:
        day = 1
        if mon > 12:
            mon = 1
            year += 1
        else:
            mon += 1
    else:
        day += 1
    return "{year}%02d%02d".format(year=year) % (mon, day)

def get_day(now):
    return int(now[-2:])

def get_mon(now):
    return int(now[-4:6])

def get_year(now):
    return int(now[:4])


def driver_next_day(driver, now):
    driver.get('https://www.pixiv.net/ranking.php?mode=daily&content=illust&date='+next_date(now))
    return next_date(now)


now = "20170122"
for i in range(500):
    now = driver_next_day(web, now)
    print(one_day(web, 60))