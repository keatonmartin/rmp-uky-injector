import time
import csv 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

RMP_URL = "https://www.ratemyprofessors.com/search/professors/1118?q=*"
NUM_PROFS = 3802 # weird quirks with rmp make this necessary

TEACHER_CARD_CLASS = "TeacherCard__StyledTeacherCard-syjs0d-0" # contains link, is anchor tag
TEACHER_NAME_CLASS = "CardName__StyledCardName-sc-1gyrgim-0"
TEACHER_DIFFICULTY = "CardFeedback__CardFeedbackNumber-lq6nix-2"
TEACHER_WOULD_TAKE_AGAIN = "CardFeedback__CardFeedbackNumber-lq6nix-2"
TEACHER_NUM_RATINGS = "CardNumRating__CardNumRatingCount-sc-17t4b9u-3"
TEACHER_QUALITY = "CardNumRating__CardNumRatingNumber-sc-17t4b9u-2"
TEACHER_DEPT = "CardSchool__Department-sc-19lmz2k-0"

COOKIES_BUTTON = "CCPAModal__StyledCloseButton-sc-10x9kq-2"
DEPARTMENT_DROPDOWN = "css-1hwfws3" #"TeacherSearchDropdown__StyledSelect-im1yvx-0"
DROPDOWN_STEM = "react-select-3-option-"
SHOW_MORE = "PaginationButton__StyledPaginationButton-txi1dr-1"

USER_DATA_DIR = "/home/keaton/.config/google-chrome/"

options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=" + USER_DATA_DIR)
options.add_argument('--profile-directory=Profile 1')
#options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)

driver.get(RMP_URL)

# allow cookies disclaimer to appear
time.sleep(4)

# close cookies disclaimer
driver.find_element(By.CLASS_NAME, COOKIES_BUTTON).click()

# keep track of which department we're on
department = 1
professorList = []
while True:

    time.sleep(1)
    # open department drop down 
    driver.find_element(By.CLASS_NAME, DEPARTMENT_DROPDOWN).click()

    time.sleep(1)
    try:
        current_dept = driver.find_element(By.ID, DROPDOWN_STEM + str(department))
    except:
        break
    print(current_dept.text)
    current_dept.click()
    time.sleep(2)

    while True: 
        try:
            driver.find_element(By.CLASS_NAME, SHOW_MORE).click()
        except:
            break
        time.sleep(1.5)
    time.sleep(1) # paranoia
    # get professor cards
    professors = driver.find_elements(By.CLASS_NAME, TEACHER_CARD_CLASS)

    # process professor elements on page
    for p in professors:
        name = p.find_element(By.CLASS_NAME, TEACHER_NAME_CLASS).text
        difficulty = p.find_element(By.CLASS_NAME, TEACHER_DIFFICULTY).text
        take_again = p.find_element(By.CLASS_NAME, TEACHER_WOULD_TAKE_AGAIN).text
        num_ratings = p.find_element(By.CLASS_NAME, TEACHER_NUM_RATINGS).text
        quality = p.find_element(By.CLASS_NAME, TEACHER_QUALITY).text
        dept = p.find_element(By.CLASS_NAME, TEACHER_DEPT).text
        link = p.get_attribute("href")
        professorList.append((name, difficulty, take_again, num_ratings, quality, dept, link))

    department += 1
    driver.get(RMP_URL)

fields = ['name', 'difficulty', 'would_take_again', 'num_ratings', 'quality', 'department', 'link']

with open('profs.csv', 'w') as f:
    write = csv.writer(f)
    write.writerow(fields)
    write.writerows(professorList)

for p in professorList:
    print(p)

print(len(professorList))

