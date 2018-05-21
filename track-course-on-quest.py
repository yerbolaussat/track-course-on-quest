from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import sys
import os
import getpass
from selenium.webdriver.support.ui import Select
import time
import datetime

SPEED_CONSTANT = 2

_login_url = "https://quest.pecs.uwaterloo.ca/psp/SS/?cmd=login&languageCd=ENG"

mode = 1 # PhantomJS
# mode = 2 # Google Chrome

try:
	username = sys.argv[1]
	password = sys.argv[2]
except IndexError:
	username = raw_input("Enter your username: ")
	password = getpass.getpass("Enter your password: ")
	dept = raw_input("Enter department: ")
	course_num_input = raw_input("Enter course number: ")

def initialize():
	global driver
	if mode == 1:
		print('\nInitializing PhantomJS WebDriver...')
		driver = webdriver.PhantomJS()
	elif mode == 2:
		print('\nInitializing Chrome WebDriver...')
		driver = webdriver.Chrome('/Users/yerbol/Desktop/chromedriver')

	# Change default timeout and window size.
	driver.implicitly_wait(120)
	driver.set_window_size(700, 500)
    
	print('Logging into Quest...')

	driver.get(_login_url)
	driver.save_screenshot('screen1.png')
	emailBox = driver.find_element_by_name('userid')
	emailBox.send_keys(username)
	passwordBox = driver.find_element_by_name('pwd')
	passwordBox.send_keys(password)
	driver.find_element_by_name('Submit').click()
	time.sleep(SPEED_CONSTANT)
	global _student_center_url
	_student_center_url = str(driver.current_url)
	driver.save_screenshot('student_center.png')
	
def check_status():
	driver.get(_student_center_url)
	driver.switch_to_frame('TargetContent')
	
	search_classes = driver.find_element_by_id('DERIVED_SSS_SCR_SSS_LINK_ANCHOR2').click()
	time.sleep(SPEED_CONSTANT)

	# choose term
	select = Select(driver.find_element_by_id('CLASS_SRCH_WRK2_STRM$35$'))
	
	year = raw_input("Enter year: ")
	term = raw_input("Enter term: ")
	term_yterm = term + " " + year
	
	select.select_by_visible_text(term_yterm)
	time.sleep(SPEED_CONSTANT)
	
	# insert course number
	course_num = driver.find_element_by_id("SSR_CLSRCH_WRK_CATALOG_NBR$1")
	course_num.send_keys(course_num_input)
	time.sleep(SPEED_CONSTANT)
	
	# uncheck "Show Open Classes Only"
	check = driver.find_element_by_id("SSR_CLSRCH_WRK_SSR_OPEN_ONLY$3")
	check.click()
	time.sleep(SPEED_CONSTANT)
	
	#insert department
	subject = driver.find_element_by_name("SSR_CLSRCH_WRK_SUBJECT$0")
	subject.send_keys(dept)
	time.sleep(SPEED_CONSTANT)

	# choose academic career
	career = driver.find_element_by_id("SSR_CLSRCH_WRK_ACAD_CAREER$2")
	Select(career).select_by_visible_text('Graduate')
	time.sleep(SPEED_CONSTANT)

	# Search
	search=driver.find_element_by_id('CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH')
	if mode == 1:
		search.click()
	elif mode == 2:
		ActionChains(driver).move_to_element_with_offset(search, 0, 0).click().perform()
	
	time.sleep(SPEED_CONSTANT)
	driver.save_screenshot('search_result.png')
	
	num_classes_element = driver.find_element_by_id("win0divSSR_CLSRSLT_WRK_GROUPBOX1")
	num_classes_text = str(num_classes_element.find_element_by_tag_name("td").text)
	num_classes = int(num_classes_text.split(" ")[0])
	
	current_time = str(datetime.datetime.now())[:-7]

	print "\n\n\n"
	print current_time
	print "-" * 15
	print "Course:", dept, course_num_input
	print "-" * 15
	print "Number of sections available", num_classes
	
	
	
	for i in range(num_classes):
		section = i+1
		element_id = "win0divDERIVED_CLSRCH_SSR_STATUS_LONG$" + str(i)
		status_window = driver.find_element_by_id(element_id)	
		img = status_window.find_element_by_tag_name("img")
		status = img.get_attribute("alt")
		
		instructor_id = "MTG_INSTR$" + str(i)
		instructor_element = driver.find_element_by_id(instructor_id)	
		instructor = instructor_element.text
		
		time_id = "MTG_DAYTIME$" + str(i)
		time_element = driver.find_element_by_id(time_id)	
		daytime = time_element.text
		
		topic_id = "DERIVED_CLSRCH_DESCRLONG$" + str(i)
		topic_element = driver.find_element_by_id(topic_id)	
		topic = topic_element.text
						
		print "Section", section, ":", topic
		print "     Instructor:", instructor
		print "     Time:", daytime
		print "     Status:", status
		print "\n"

initialize()

while True:
	check_status()
	time.sleep(20)
