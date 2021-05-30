__author__ = "Elad Ben David"

import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def go(username, password_text, path, course_name,
       worknum):  # need to receive username,password,file path to upload, desired course, desired homework num
    chrome_path = 'C:\Program Files\chromedriver.exe'
    driver = webdriver.Chrome(chrome_path)
    action = webdriver.ActionChains(driver)
    website = 'https://yedion.jce.ac.il/yedion/fireflyweb.aspx'
    driver.get(website)
    email = driver.find_element_by_xpath('//*[@id="R1C1"]')
    password = driver.find_element_by_xpath('//*[@id="R1C2"]')
    submit = driver.find_element_by_xpath('//*[@id="loginbtn"]')
    email.send_keys(username)  # required username
    password.send_keys(password_text)  # required password
    submit.click()
    # try:
    #     time.sleep(2)
    #     password_error = driver.find_element_by_id('loginError')
    #     password_error = driver.find_element_by_xpath('//div[@id="loginError"]')
    #     first = 'חובה למלא משתמש תקף וסיסמה (קוד 5)  שים לב, זוהי כניסת סטודנט'
    #     second = 'סיסמה קצרה מידי (קוד 1)'
    #     third = 'חובה למלא משתמש תקף וסיסמה(קוד 8)'
    #     print(password_error.text)
    #     if str(password_error.text) == first or str(password_error.text) == second or str(
    #             password_error.text) == third:  # need to be fixed
    #         to_return = -1
    #         queue.put(to_return)
    #         driver.quit()
    #         return
    # except:  # didnt find any login error
    #     pass
    time.sleep(1)
    assignments_list = driver.find_element_by_xpath('//*[@id="MenuIcon_6"]')
    assignments_list.click()
    course_select = driver.find_elements_by_xpath('//div[@class="NotInUse col-12"]')
    for course in course_select:
        if course.find_element_by_tag_name('h2').text == course_name:
            print(f'found {course_name}')
            course.click()
            print(
                course.find_element_by_xpath(".//div[contains(@onclick,'ShowHideContentfa')]").get_attribute('onclick'))
            break
    hidden_course = driver.find_element_by_xpath('//div[@style="display: inherit;"]')
    assignments_list = hidden_course.find_elements_by_xpath(
        './/div[@class="col-md-4 col-xl-3 Father"]')  # '   './/' -  make  webelement search in hes childs and not all the page
    for assignment in assignments_list:
        temp = str(assignment.find_element_by_tag_name('h2').text)
        if temp.find(str(worknum)) != -1:
            print(f'found the exc its {temp}')
            assignment.find_element_by_partial_link_text('הגש').click()  # were going to the assignment page
    # here the driver should be in the assignment page

    # need to make function to extract the Class number from each tr[i]
    # driver.quit()
    # panel_titles = driver.find_elements_by_class_name('panel-title')
    # search_title = find_title(panel_titles, course_name)
    # search_name = search_title.find_elements_by_xpath("//div[contains(@style, 'background-color:#e0e0e0')]")
    # find_homework_num(search_name, worknum)
    # time.sleep(1)
    upload = driver.find_element_by_id('fileupload1')  # find upload button
    upload.send_keys(path)
    text_edit = driver.find_element_by_id('R1C22')
    text_edit.send_keys(f'תרגיל {worknum}')  # edit text

    # change that we dont need to upload more files
    change_to_no = driver.find_element_by_id('select2-R1C2-container')
    change_to_no.click()
    write_no = driver.find_element_by_class_name('select2-search__field')
    write_no.send_keys('לא')
    write_no.send_keys(Keys.RETURN)
    time.sleep(5)
    submit_btn = driver.find_element_by_id('btnNext') # last button to send
    submit_btn.click()
    confirm_btn = driver.find_element_by_xpath('//*[@id="modalProcessAction"]')
    confirm_btn.click()
    time.sleep(10)


def find_title(titles, course):  # dont touch!!
    for title in titles:
        temp = str(title.text)
        if temp.find(course) != -1:
            print(title.text)
            return title
    return -1


def find_homework_num(title, homework_num):
    for homework_title in title:
        temp = str(homework_title.text)
        if temp.find(homework_num) != -1:
            return homework_title.find_element_by_class_name('btn-u').click()
    return -1
