from selenium import webdriver

driver = webdriver.PhantomJS() # or add to your PATH
driver.set_window_size(1920,1080) # optional
driver.get('http://152.66.254.91/static/printtest.html')
#driver.save_screenshot('screen.png') # save a screenshot to disk
#sbtn = driver.find_element_by_css_selector('button.gbqfba')
#sbtn.click()



rect = driver.execute_script("return document.getElementsByClassName('page')[0].getBoundingClientRect();")
print(rect)

neptun_cells=[]
for i in range(6):
	rect = driver.execute_script("return document.getElementById('header').getElementsByClassName('codecell')[%d].getBoundingClientRect();"%i)
	neptun_cells.append(rect)
print(neptun_cells)