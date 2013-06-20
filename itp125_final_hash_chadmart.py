__author__ = 'Chad Martin'

import urllib.request
import hashlib
from datetime import datetime
import argparse
import os

def downloadFile(inputURL, outputFile):
    #this function downloads file from URL and saves file locally in outputFile
    #Parameter inputURL: external URL of file to be downloaded
    #Parameter outputFile: local file address of file to be saved
    with open(outputFile, 'w') as out_file:
        result =  urllib.request.urlopen(inputURL)
        data = result.read()
        text = data.decode('utf-8')
        out_file.write(text)
        out_file.close()

def findHash(hashIn, hashType, database, outputFile):
    #this function looks for a hash in database that matches hashIn
    #if matching hash found, then return 1 and write original hash and corresponding password to outputFile
    #if matching hash not found, return 0
    #Parameter hashIn: hash to compare against database
    #Parameter hashType: type of hash to compare either "md5" or "sha1"
    #Parameter database: database to search through
    #Parameter outputFile: local file to write to
    crackList = open(outputFile, "a")
    DB = open(database, "r")

    for line in DB:
        DBLine = line.strip('\n').strip('\r')
        DBLineList = DBLine.split(":")

        if hashType == "md5":
            if DBLineList[0] == hashIn:
                crackList.write(hashIn + ":" + DBLineList[2] + "\n")
                DB.close()
                crackList.close()
                return 1
        elif hashType == "sha1":
            if DBLineList[1] == hashIn:
                crackList.write(hashIn + ":" + DBLineList[2] + "\n")
                DB.close()
                crackList.close()
                return 1
        else:
            print("Error: Blue 42")

    DB.close()
    crackList.close()
    return 0

def makeHash(inputFile, tstart):
    # this function reads in list of passwords from file
    # and writes out "md5 hash : sha1 hash : corresponding password" to "database.rbt"
    # Parameter inputFile: local file that contains list of passwords
    # Parameter tstart: time program started running
    hashCount = 0

    passList = open(inputFile, "r")
    hashList = open("database.rbt", "w")

    for line in passList:
        hashCount = hashCount + 1
        password = line.strip('\n').strip('\r')

        md5Hash = hashlib.md5(password.encode('utf-8')).hexdigest()
        sha1Hash = hashlib.sha1(password.encode('utf-8')).hexdigest()
        hashList.write(md5Hash + ":" + sha1Hash + ":" + password + "\n")

    passList.close()
    hashList.close()

    tend = datetime.now()

    print("Number of hashes created:\t" + str(hashCount))
    print("Time to create the table:\t" + str(tend - tstart))




def crackHash(database, hashType, inputFile, outputFile, tstart):
    # This function reads in list of hashes from inputFile
    # and checks if each hash matches a hash in database
    # if the password hash exists in database, it knows what the original password was.
    # The program will then write the original hash, and the password associated with the hash to the file outputFile
    # Parameter database: database of hashes and corresponding passwords
    # Parameter hashType: type of hash to compare either "md5" or "sha1"
    # Parameter inputFile: list of hashes
    # Parameter outputFile: local file to write to
    # Parameter tstart: time program started running
    hashCount = 0
    crackCount = 0

    hashList = open(inputFile, "r")
    #clear output file
    crackList = open(outputFile, "w")
    crackList.close()

    for line in hashList:
        hashCount = hashCount + 1
        hashIn = line.strip('\n').strip('\r')
        crackCount = crackCount + findHash(hashIn, hashType, database, outputFile)

    hashList.close()

    tend = datetime.now()

    print("Number of hashes found:\t\t" + str(hashCount))
    print("Number of hashes cracked:\t" + str(crackCount))
    print("Time to crack the hashes:\t" + str(tend - tstart))
    print("Type of hash used to crack:\t" + str(hashType))

def fileExists(inFile):
    #this function tests if inFile is a valid local file
    #if valid, program continues
    #if invalid, program displays error message and quits program
    #Parameter inFile: string of local file address
    try:
        with open(inFile): pass
    except IOError:
        print('Local file not found.')

        exit()


def findType(inFile):
    #this function returns whether inFile is a local address or url
    #if inFile is url, functions returns 'url'
    #if inFIle is a local file, function returns 'file'
    #Parameter inFile: string of file address
    indexF = inFile.find("://")
    if indexF > 1 and indexF < 15:
        return "url"
    else:
        return "file"

def validateInput(args):
    #this function validates operation(-ops) and type(-t)
    #if invalid -ops or -t, then return false
    #if valid -ops and -t, then return true
    if args.ops != "generate" and args.ops != "crack":
        print("Invalid operations flag. It can be either 'generate' or 'crack'.")
        return False

    if args.ops == "crack" and args.t != "md5" and args.t != "sha1":
        print("Invalid type of hash. It can be either 'md5' or 'sha1'.")
        return False

    if args.i == None:
        print("No input file specified. Please specify an input file.")
        return False

    if args.ops == "crack" and args.o == None:
        print("No output file specified. Please specify an output file.")
        return False

    return True

# This function parses command line arguments and selects which tasks to run based on command line arguments
# Argument -ops: this is the operations flag. It can be either 'generate' or 'crack'
# Argument -t: this is the type of hash to use. It can be either 'md5' or 'sha1'.
# Argument -i: this is the input file to be used. It is used for both operations.
# Argument -o: this is the output file to be used. It is used only for 'crack'.
if __name__ == "__main__":
    tstart = datetime.now()
    parser = argparse.ArgumentParser(description="Its a secret")
    parser.add_argument("-ops", dest="ops", help="The operations flag. It can be either 'generate' or 'crack'." )
    parser.add_argument("-t", dest="t", help="The type of hash to use. It can be either 'md5' or 'sha1'.")
    parser.add_argument("-i", dest="i", help="The input file to be used. It is used for both operations.")
    parser.add_argument("-o", dest="o", help="The output file to be used. It is used only for 'crack'.")
    args = parser.parse_args()

    fileType = ""

    if validateInput(args):
        fileType = findType(args.i)
        if fileType == "url":
            downloadFile(args.i, "tempFile.in")
            inputFile = "tempFile.in"
        elif fileType == "file":
            fileExists(args.i)
            inputFile = args.i

        if args.ops == "generate":
            makeHash(inputFile, tstart)
        elif args.ops == "crack":
            crackHash("database.rbt", args.t, inputFile, args.o, tstart)
        else:
            print("How did you get here? What are you doing?")
    else:
        print("Invalid Input. Correct yourself before you wreck yourself...")

    if fileType == "url":
        os.remove("tempFile.in")