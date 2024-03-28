import time
import csv 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

RMP_URL = "https://www.ratemyprofessors.com/search/professors/1118?q=*"

TEACHER_CARD_CLASS = "TeacherCard__StyledTeacherCard-syjs0d-0" # contains link, is anchor tag
TEACHER_NAME_CLASS = "CardName__StyledCardName-sc-1gyrgim-0"
TEACHER_DIFFICULTY = "CardFeedback__CardFeedbackNumber-lq6nix-2"
TEACHER_WOULD_TAKE_AGAIN = "CardFeedback__CardFeedbackNumber-lq6nix-2"
TEACHER_NUM_RATINGS = "CardNumRating__CardNumRatingCount-sc-17t4b9u-3"
TEACHER_QUALITY = "CardNumRating__CardNumRatingNumber-sc-17t4b9u-2"
TEACHER_DEPT = "CardSchool__Department-sc-19lmz2k-0"

COOKIES_BUTTON = "CCPAModal__StyledCloseButton-sc-10x9kq-2"
SHOW_MORE = "PaginationButton__StyledPaginationButton-txi1dr-1"

# path to data dir for chrome 
USER_DATA_DIR = "/home/keaton/.config/google-chrome/"

options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=" + USER_DATA_DIR)
options.add_argument('--profile-directory=Profile 1')
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)

driver.get(RMP_URL)

# allow cookies disclaimer to appear
time.sleep(4)

# close cookies disclaimer
driver.find_element(By.CLASS_NAME, COOKIES_BUTTON).click()

# expand list 
for _ in range(50):
    try:
        driver.find_element(By.CLASS_NAME, SHOW_MORE).click()
    except:
        break
    time.sleep(1)

time.sleep(1) # paranoia

# get professor cards
professors = driver.find_elements(By.CLASS_NAME, TEACHER_CARD_CLASS)

professorList = []

# for each prof
for p in professors:
    name = p.find_element(By.CLASS_NAME, TEACHER_NAME_CLASS).text
    difficulty = p.find_element(By.CLASS_NAME, TEACHER_DIFFICULTY).text
    take_again = p.find_element(By.CLASS_NAME, TEACHER_WOULD_TAKE_AGAIN).text
    num_ratings = p.find_element(By.CLASS_NAME, TEACHER_NUM_RATINGS).text
    quality = p.find_element(By.CLASS_NAME, TEACHER_QUALITY).text
    dept = p.find_element(By.CLASS_NAME, TEACHER_DEPT).text
    link = p.get_attribute("href")
    professorList.append((name, difficulty, take_again, num_ratings, quality, dept, link))

fields = ['name', 'difficulty', 'would_take_again', 'num_ratings', 'quality', 'department', 'link']

with open('profs.csv', 'w') as f:
    write = csv.writer(f)
    write.writerow(fields)
    write.writerows(professorList)

for p in professorList:
    print(p)

print(len(professorList))

