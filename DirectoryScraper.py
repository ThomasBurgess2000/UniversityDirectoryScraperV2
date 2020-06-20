#DEPENDENCIES
# Selenium
# Chrome WebDriver
import time
import getpass
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import face_recognition
import pickle
import numpy as np
import re
from itertools import islice

def scraper():

    #User Variables
    username=input("NetID: ")
    password=getpass.getpass()

    #LOAD PAGE
    options=Options()
    options.headless=False
    driver=webdriver.Chrome('C:/Users/Thomas/Desktop/Directory Scraper/chromedriver_win32/chromedriver.exe',chrome_options=options)
    driver.get("https://www.university.edu/directory/search?_type=person")

    #GO TO LOGIN PAGE
    loginLink=driver.find_element_by_xpath('//*[@id="universityHeader"]/div/div/a')
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
    universityDirectory = {}
    counter=0

    for t in range(1,376):
        tStr=str(t)
        driver.get("https://www.university.edu/directory/search?_type=person&page="+tStr)
        #Creates list of current page's names, emails, and image links.
        pageListOfNames=driver.find_elements_by_class_name('title')
        pageListOfEmails=driver.find_elements_by_class_name('contact-info')
        pageListOfImageLinks=driver.find_elements_by_css_selector("div.result_image img")
        i=0
        # Adds the elements of the above lists to the master list of names, emails, and addresses as well as adds them all
        # to the dictionary 'universityDirectory' where the key is the name and the value is a list containing the information
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
                image="https://apps.university.edu/idphotos/d36ec5f30a0cd006d11f2c953ac844fb_medium.jpg"
                i-=1
            finalListOfImageLinks.append(image)
            fixedPageListOfImages.append(image)
            i+=1
        i=0
        p=0
        while (i<len(pageListOfEmails)):
            #Frickin idiot Tom
            if (pageListOfNames[i].text=='Tom Keene'):
                universityDirectory['Tom Keene']=['',"https://apps.university.edu/idphotos/d36ec5f30a0cd006d11f2c953ac844fb_medium.jpg"]
                p-=1
            else:
                universityDirectory[pageListOfNames[i].text]=[fixedPageListOfEmails[i],fixedPageListOfImages[p]]
            #I don't really utilize the dictionary yet, but if I wanted to add some search functionality this would be the way to do it.
            x=universityDirectory[pageListOfNames[i].text]
            print (pageListOfNames[i].text)
            print (x)
            i+=1
            p+=1
        i=0
        p=0

    i=0
    p=0
    # Writes names, emails, and image URLs to a text file in the local directory.

    with open('universitydirectory6202020.txt','w+') as output:
        while (i<len(finalListOfEmails)):
            output.write("%s\n" % str(i+1))
            output.write("%s\n" % str(finalListOfNames[i]))
            output.write("%s\n" % str(finalListOfEmails[i]))
            if (str(finalListOfNames[i])=='Tom Keene'):
                output.write("%s\n" % "https://apps.university.edu/idphotos/d36ec5f30a0cd006d11f2c953ac844fb_medium.jpg")
                p-=1
            else:
                output.write("%s\n" % str(finalListOfImageLinks[p]))
            i+=1
            p+=1

    i=0
    p=0

    with open ('universityphotos6202020.txt','w+') as output:
        while (i<len(finalListOfEmails)):
            if (str(finalListOfNames[i])=='Tom Keene'):
                output.write("%s\n" % "https://apps.university.edu/idphotos/d36ec5f30a0cd006d11f2c953ac844fb_medium.jpg")
                p-=1
            else:
                output.write("%s\n" % str(finalListOfImageLinks[p]))
            i+=1
            p+=1

    print ("\n")
    print (counter)

def exportNamesAndEmails():
    lines=[line.rstrip('\n') for line in open ('universitydirectory6202020.txt')]

    # Names
    name_lines=lines[1::4]
    nameString=""
    for element in name_lines:
        nameString += element
        nameString += ("\n")
        print (element)

    with open ('universitynames6202020.txt','w+') as output:
        output.write(nameString)

    #Emails
    email_lines=lines[2::4]
    emailString=""
    for element in email_lines:
        emailString += element
        emailString += ("\n")
        print (element)

    with open ('universityemails6202020.txt','w+') as output:
        output.write(emailString)

def downloadImages():
    t=0
    imageURLs=[line.rstrip('\n') for line in open ('universityphotos6202020.txt')]
    names=[line.rstrip('\n') for line in open ('universitynames6202020.txt')]
    for url in imageURLs:
        personName=names[t]
        fileName=personName+".png"
        fullFileName=os.path.join("C:/Users/Thomas/Desktop/Directory Scraper/Photos",fileName)
        urlretrieve(url,fullFileName)
        print ("Downloaded: "+fileName+"\n")
        t=t+1

    print ("Finished Downloading")

def newlinetocommalist():
    lines=[line.rstrip('\n') for line in open ('universityphotos2.txt')]

    listString=""
    for element in lines:
        listString += ("\"")
        listString += element
        listString += ("\"")
        listString += (",")

    with open ('universityphotoslist3.txt','w+') as output:
        output.write(listString)

def facecomparison():
    

    #Initial variables
    goAgain="z"
    with open ('dataset_faces.dat', 'rb') as f:
            all_face_encodings=pickle.load(f)
    face_names=list(all_face_encodings.keys())
    face_encodings=np.array(list(all_face_encodings.values()))

    #compareFace function
    def compareFace():
        filename=input("Please enter the filename of the file with the unknown face, stored in the 'Unknowns' folder (e.g. face3.jpg): ")
        unknown_image=face_recognition.load_image_file("C:/Users/Thomas/Desktop/Face Comparison/Unknowns/"+filename)
        unknown_face=face_recognition.face_encodings(unknown_image)

        toleranceVal=0.61
        
        matches="foo"

        #Increases strictness until there is only one result left
        while (len(matches)>1):
            toleranceVal=toleranceVal-0.01
            result=face_recognition.compare_faces(face_encodings,unknown_face,tolerance=toleranceVal)
            names_with_result=list(zip(face_names,result))
            matches=[item for item in names_with_result if True in item]

        if len(matches)<1:
            print ("NO MATCH FOUND.")
        else:
            prettyMatch=str(matches[0][0])
            capMatch=prettyMatch.upper()
            print ("\n********************")
            print ("Match found: "+capMatch)
            print ("********************\n")
        goAgain=input("Would you like to analyze another photo? (y/n) ")
        print ("\n")
        if goAgain=="y":
            compareFace()

    #MAIN

    print ("university FACE FINDER\n")
    print ("Given an unknown face, this program will search the university database and return any match it finds.\n")

    compareFace()

def create_encodings():
    all_face_encodings={}

    directory = os.fsencode("C:/Users/Thomas/Desktop/Face Comparison/Photos")

    i=0
    for file in os.listdir(directory):
        filename=os.fsdecode(file)
        img1=face_recognition.load_image_file("C:/Users/Thomas/Desktop/Face Comparison/Photos/"+filename)
        name=filename[:-4]
        print (name)
        if len(face_recognition.face_encodings(img1)) > 0:
            all_face_encodings[name]=face_recognition.face_encodings(img1)[0]

    with open ('dataset_faces.dat', 'wb') as f:
        pickle.dump(all_face_encodings, f)

    k=input("press close to exit")

#md5 cracker
def findID():
    #Log start time
    start_time=time.time()
    #Starting ID number
    ID=180000
    #Iterator
    i=0
    #Number of ID numbers identified
    numberFound=0    
    #Iterates through X number of possible ID numbers, converts those numbers to md5 hash values, and compares those hash values to the photo URLs already acquired.
    while i<20000:
        #Line number for output
        lineNum=0
        #Converts ID to string, then gets the md5 hash of that string
        stringed=str(ID)
        
        result=hashlib.md5(stringed.encode())
        #Opens file
        with open ("C:/Users/Thomas/Desktop/Directory Scraper/universityDirectoryWithID.txt",'r') as f:
            #Iterates through every fourth line (starting at line 3 when you start counting at line 0)
            for line in islice(f,0,None,1):
                #Checks if the md5 hash value is in that line
                if result.hexdigest() in line:
                    #Opens file and saves all the lines to a list
                    f2=open("C:/Users/Thomas/Desktop/Directory Scraper/universityDirectoryWithID.txt",'r')
                    contents=f2.readlines()
                    f2.close()

                    #If it is, that means the ID that generated that hash is the ID of the student's photo being checked on 'line'. Output that student ID and the student's name.
                    print ("ID #"+stringed+" found and logged: "+contents[lineNum-2])

                    #Inserts the ID found into that list and logs the ID in listOfFoundIDs.txt
                    contents.insert(lineNum-1,stringed+"\n")
                    with open ("C:/Users/Thomas/Desktop/Directory Scraper/listOfFoundIDs.txt","a") as foundFile:
                        foundFile.write(stringed+"\n")
                    #Writes that list to the file
                    f2=open("C:/Users/Thomas/Desktop/Directory Scraper/universityDirectoryWithID.txt",'w')
                    contents="".join(contents)
                    f2.write(contents)
                    f2.close()

                    #Increment how many ID's have been found.
                    numberFound=numberFound+1
                #Increment the line number for output
                lineNum=lineNum+1
        #Increase the ID iterator to check the next one
        ID=ID+1
        #Print whenever another 1000 numbers have been checked
        if (i%1000==0):
            print (str(i)+" numbers checked in "+str(round((time.time()-start_time),1))+" seconds. "+str(numberFound)+" ID numbers found so far.\n")
        #Increase the iterator to start another check of the next ID
        i=i+1
        
    print ("Total ID numbers found: "+str(numberFound))

userChoice = 99
while (userChoice!='0'):
    print ("\nSelect your choice from the menu (e.g. '2'):\n1: Scrape\n2: Export names and emails\n3: Download images\n4: Newline to comma separated list\n5: Face comparison\n6: Create face comparison encodings\n0: Exit\n")
    userChoice=input()
    if (userChoice=='1'):
        scraper()
    elif (userChoice=='2'):
        exportNamesAndEmails()
    elif (userChoice=='3'):
        downloadImages()
    elif (userChoice=='4'):
        newlinetocommalist()
    elif (userChoice=='5'):
        facecomparison()
    elif (userChoice=='6'):
        create_encodings()
    elif (userChoice=='0'):
        print ("Goodbyte!")
    else:
        print("You entered: " + userChoice + ". That was not a valid option, please try again.\n")

