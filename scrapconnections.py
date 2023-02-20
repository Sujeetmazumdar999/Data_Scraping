# Import libraries and packages for the project 
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import csv

#Enter URL
url = input("Enter Your Url : ")
#Enter Username
Username = input("Enter Your linkdin mail : ")
#Enter Password
Password = input("Enter Your linkdin password : ")
#Enter the page Number for Scraping data
page_no = int(input("Enter how many page to be scrap : "))

# Task 1: Login to Linkedin
# Task 1.1: Open Chrome and Access Linkedin login site
driver = webdriver.Chrome()
sleep(2)

driver.get(url)
print('- Finish initializing a driver')   
sleep(2)

signin_field = driver.find_element_by_xpath('/html/body/div[1]/main/p[1]/a')
signin_field.click()
sleep(3)

# Task 1.2: Key in login credentials
email_field = driver.find_element_by_id('username')
email_field.send_keys(Username)
print('- Finish keying in email')
sleep(3)

password_field = driver.find_element_by_name('session_password')
password_field.send_keys(Password)
print('- Finish keying in password')
sleep(3)

# Task 1.2: Click the Login button
signin_field = driver.find_element_by_xpath('//*[@id="organic-div"]/form/div[3]/button')
signin_field.click()
sleep(20)


def scrap():
    soup = BeautifulSoup(driver.page_source, "html.parser")
    profiles = soup.find_all("li",class_= "reusable-search__result-container")
    data = []
    for i in profiles:
        try:
            yrl=i.find(class_= "entity-result__title-text t-16").find("a", href = True )
            profile_link = yrl["href"]
            name = i.find(class_= "entity-result__title-text t-16").find("span").find("span").text.strip()
            title = i.find(class_ = "entity-result__primary-subtitle t-14 t-black t-normal").text.strip()
            location = i.find(class_="entity-result__secondary-subtitle t-14 t-normal").text.strip()
            data_=[name, profile_link, title, location]
            data.append(data_)
        except:
            continue
    return data

# First page initialization !!
initial_data = scrap()
sleep(5)

for page in range(2,page_no+1):
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);') #scroll to the end of the page
    sleep(5)
    next_button = driver.find_element_by_class_name("artdeco-pagination__button--next") #click to next page
    next_button.click()
    sleep(10)
    next_page_data = scrap()
    initial_data = initial_data + next_page_data
    sleep(5)

header = ["Name", "Profile_link", "Title","Location"]

with open('linkdin_data.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(initial_data)

sleep(10)
driver.close()






