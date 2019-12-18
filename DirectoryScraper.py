#DEPENDENCIES
# Selenium
# Chrome WebDriver
import time
import getpass
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

#User Variables
username=input("NetID: ")
password=getpass.getpass()

#LOAD PAGE
driver=webdriver.Chrome('C:/Users/Thomas/Desktop/chromedriver_win32/chromedriver.exe')
driver.get("https://www.RANDOMSCHOOL.edu/directory/search?_type=person")

#GO TO LOGIN PAGE
loginLink=driver.find_element_by_xpath('//*[@id="RANDOMSCHOOLHeader"]/div/div/a')
loginLink.click()
time.sleep(3)

#Login Variables 
netidForm=driver.find_element_by_id('username')
passwordForm=driver.find_element_by_id('password')
submitForm=driver.find_element_by_name('submit')

#LOGIN
netidForm.send_keys(username)
passwordForm.send_keys(password)
submitForm.click()

#Data Variables
finalListOfNames=[]
finalListOfEmails=[]
finalListOfImageLinks=[]
RANDOMSCHOOLDirectory = {}
counter=0

#SCRAPE NAMES, EMAILS, AND IMAGES
for t in range(1,371):
    tStr=str(t)
    driver.get("https://www.RANDOMSCHOOL.edu/directory/search?_type=person&page="+tStr)
    #Creates list of current page's names, emails, and image links.
    pageListOfNames=driver.find_elements_by_class_name('title')
    pageListOfEmails=driver.find_elements_by_class_name('contact-info')
    pageListOfImageLinks=driver.find_elements_by_css_selector("div.result_image img")
    i=0
    # Adds the elements of the above lists to the master list of names, emails, and addresses as well as adds them all
    # to the dictionary 'RANDOMSCHOOLDirectory' where the key is the name and the value is a list containing the information
    # about the person (so far just email and image link).

    # fixedPage variables are the corrected versions of their pageList counterparts (i.e. the strings I want).
    # I didn't correct the pageList directly in case I wanted to modify how I did this in the future.
    fixedPageListOfEmails=[]
    fixedPageListOfImages=[]
    while (i<len(pageListOfNames)):
        name=pageListOfNames[i].text
        finalListOfNames.append(name)
        counter+=1
        email=pageListOfEmails[i].text
        email=email.split('\n')[0]
        finalListOfEmails.append(email)
        fixedPageListOfEmails.append(email)
        i+=1
    i=0
    # The images had to be done in a separate loop because of Tom Keene, the only guy who doesn't have a photo so he throws the iterator off.
    # As you can see, I do this two separate ways. Here, I just create a whole different while loop. Later you'll see I do it in the same loop, but just have
    # a different iterator.
    while (i<len(pageListOfImageLinks)):
        image=pageListOfImageLinks[i].get_attribute('src')
        image=str(image)
        # This guy is the only wacko in the whole directory who doesn't have a picture and screws the whole thing up
        if (name=="Tom Keene"):
            image="https://apps.RANDOMSCHOOL.edu/idphotos/d36ec5f30a0cd006d11f2c953ac844fb_medium.jpg"
            i-=1
        finalListOfImageLinks.append(image)
        fixedPageListOfImages.append(image)
        i+=1
    i=0
    p=0
    while (i<len(pageListOfEmails)):
        #Frickin idiot Tom
        if (pageListOfNames[i].text=='Tom Keene'):
            RANDOMSCHOOLDirectory['Tom Keene']=['',"https://apps.RANDOMSCHOOL.edu/idphotos/d36ec5f30a0cd006d11f2c953ac844fb_medium.jpg"]
            p-=1
        else:
            RANDOMSCHOOLDirectory[pageListOfNames[i].text]=[fixedPageListOfEmails[i],fixedPageListOfImages[p]]
        #I don't really utilize the dictionary yet, but if I wanted to add some search functionality this would be the way to do it.
        x=RANDOMSCHOOLDirectory[pageListOfNames[i].text]
        print (pageListOfNames[i].text)
        print (x)
        i+=1
        p+=1
    i=0
    p=0

i=0
p=0
# Writes names, emails, and image URLs to a text file in the local directory.
with open('RANDOMSCHOOLdirectory.txt','w+') as output:
    while (i<len(finalListOfEmails)):
        output.write("%s\n" % str(i+1))
        output.write("%s\n" % str(finalListOfNames[i]))
        output.write("%s\n" % str(finalListOfEmails[i]))
        if (str(finalListOfNames[i])=='Tom Keene'):
            output.write("%s\n" % "https://apps.RANDOMSCHOOL.edu/idphotos/d36ec5f30a0cd006d11f2c953ac844fb_medium.jpg")
            p-=1
        else:
            output.write("%s\n" % str(finalListOfImageLinks[p]))
        i+=1
        p+=1

print ("\n")
print (counter)
