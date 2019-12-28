from optparse import OptionParser
from time_util import TimeUtil
import binascii
import os

DELIMITER = "//-_-_-//"
ENCODING = "utf-8"

def put(args):
    targetFile = args[0]
    targetFileName = os.path.basename(targetFile)
    patchedFileName = targetFileName.split(".")[0] + "_patched." + targetFileName.split(".")[1]

    with open(targetFile, "rb") as hostFile, open(patchedFileName, "wb+") as patchedFile:
        patchedFile.write(hostFile.read())
        index = 1
        while index < len(args):
            sourceFile = args[index]
            sourceFileName = os.path.basename(sourceFile)
            print("trying to hide", sourceFile, "...")
            with open(sourceFile, "rb") as fileToHide:
                patchedFile.write(binascii.hexlify(bytes(sourceFileName + DELIMITER, ENCODING)))
                patchedFile.write(binascii.hexlify(fileToHide.read()))
                patchedFile.write(binascii.hexlify(bytes(sourceFileName + DELIMITER, ENCODING)))
                print("...", sourceFileName, "hidden!")
            index += 1

    util = TimeUtil()
    util.setModTime( patchedFileName, util.getModTime(targetFile) )

def get(args):
    with open(args[0], "rb") as targetFile:
        fileContent = targetFile.read()
        fileContentSplit = fileContent.split(bytes("%%EOF", ENCODING))
        fileContent = fileContentSplit[len(fileContentSplit)-1]
        fileContent = binascii.unhexlify(fileContent.strip())

    if fileContent is None:
        print("something went wrong ...")
        exit

    hiddenFiles = fileContent.split(bytes(DELIMITER, ENCODING))
    fileName = None
    fileContent = None
    for index, element in enumerate(hiddenFiles):
        if index % 2 != 0:
            print("extract", fileName, "...")
            with open(fileName, "wb") as hiddenFile:
                hiddenFile.write(element)
                print("...", fileName, "extracted!")            
        elif index % 2 == 0:
            fileName = bytes.decode(element)

if __name__ == "__main__":
    parser = OptionParser()  
    parser.add_option("-p", "--put", action="store_true", help="hide files in PDF")  
    parser.add_option("-g", "--get", action="store_true", help="extract hidden files")  
    (options, args) = parser.parse_args() 

    if options.put and options.get is None:
        put(args)
    elif options.put is None and options.get:
        get(args)
    
