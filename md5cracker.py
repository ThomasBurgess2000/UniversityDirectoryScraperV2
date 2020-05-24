import hashlib
from itertools import islice
import time

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
        with open ("PATH",'r') as f:
            #Iterates through every fourth line (starting at line 3 when you start counting at line 0)
            for line in islice(f,0,None,1):
                #Checks if the md5 hash value is in that line
                if result.hexdigest() in line:
                    #Opens file and saves all the lines to a list
                    f2=open("PATH",'r')
                    contents=f2.readlines()
                    f2.close()

                    #If it is, that means the ID that generated that hash is the ID of the student's photo being checked on 'line'. Output that student ID and the student's name.
                    print ("ID #"+stringed+" found and logged: "+contents[lineNum-2])

                    #Inserts the ID found into that list and logs the ID in listOfFoundIDs.txt
                    contents.insert(lineNum-1,stringed+"\n")
                    with open ("PATH","a") as foundFile:
                        foundFile.write(stringed+"\n")
                    #Writes that list to the file
                    f2=open("PATH",'w')
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

findID()
