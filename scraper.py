import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

RMP_URL = "https://www.ratemyprofessors.com/search/professors/1118?q=*"
TEACHER_CLASS = "TeacherCard__StyledTeacherCard-syjs0d-0"
NAME_CLASS = "CardName__StyledCardName-sc-1gyrgim-0"
COOKIES_BUTTON = "CCPAModal__StyledCloseButton-sc-10x9kq-2"
SHOW_MORE = "PaginationButton__StyledPaginationButton-txi1dr-1"

options = webdriver.ChromeOptions()
#options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)

driver.get(RMP_URL)

time.sleep(5)

# Close cookies disclaimer
driver.find_element(By.CLASS_NAME, COOKIES_BUTTON).click()

# get professor names

while True:
    try:
        driver.find_element(By.CLASS_NAME, SHOW_MORE).click()
    except:
        break

time.sleep(5)

professors = driver.find_elements(By.CLASS_NAME, NAME_CLASS)

for p in professors:
    print(p.text)

