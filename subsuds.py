import os # enables curl
import xml.etree.ElementTree as ET
from pyfiglet import Figlet
from clint.textui import puts, colored, indent
#import shell.py

def main():
    welcome()
    user = Log_In()
    exit = ""
    while True:
        createXmlFile(user.password)
        submitXML(user.SuvAddress())
        while True:
            print("\n\n")
            print(colored.white("="*50))
            print(colored.cyan("0. Exit Program"))
            print(colored.yellow("\n1. Submit Another File"))
            exit = input(colored.white("\nWhat would you like to do? "))
            if exit == str(0):
                bye = Figlet(font='standard')
                print("\n\n")
                print(colored.cyan(bye.renderText("Bye Felicia!")))
                print("\n\n")
                return
            elif exit == str(1):
                break
            else:
                print(colored.red("\n\nInvald entry. Please try again."))
    print("")

def welcome():
    banner = Figlet(font='speed')
    print("\n")
    print(colored.white("="*50))
    print(colored.cyan(banner.renderText("Subsuds")))
    print(colored.white("   The SOAPUI Alternative by Chase Thomas"))
    print(colored.white("="*50))
    print("\n")

class Log_In():
    '''
    Asks the user for the .suvNumber, .userName, and .password.
    Creates an .SuvAddress string from user input.
    '''
    prefix = "https://i-"
    middle = ".workdaysuv.com/ccx/service/super/"
    implementationService = "Financials_Implementation_Service"
    version = "33.0"

    def __init__(self):
        self.suvNumber = parseURL(str(input(colored.white("\nSUV number: "))))  #
        self.userName = 'superuser@super'
        self.password = str(input(colored.white("\nSUV password: ")))       #

    def SuvAddress(self):
        SuvAddress = f"{self.prefix}{self.suvNumber}{self.middle}{self.implementationService}/v{self.version}"
        return SuvAddress

def createXmlFile(password):
    '''
    Takes in the SUV password and body text entered by user.
    Creates an XML file called output.xml that is sent to the suv
    '''
    # Basic required XML structure.
    baseXml = """<?xml version='1.0' encoding='UTF-8'?><SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:bsvc='urn:com.workday/bsvc'><SOAP-ENV:Header><wsse:Security xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" SOAP-ENV:mustUnderstand="1"><wsse:UsernameToken><wsse:Username>superuser@super</wsse:Username><wsse:Password wsse:Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText"><!-- password --></wsse:Password></wsse:UsernameToken></wsse:Security></SOAP-ENV:Header><SOAP-ENV:Body><!-- body --></SOAP-ENV:Body></SOAP-ENV:Envelope>"""

    # Ask user to input xml they want to send in
    print(colored.white("\nDirections"))
    print("––––––––––")
    print(colored.white("1. Copy everything between the body tags"), colored.green("<SOAP-ENV:Body>"), colored.white("and"), colored.green("</SOAP-ENV:Body>"), colored.white(("in your XML file.")))
    print(colored.white("2. Remove all spaces. It must be"), colored.red("only one continuous line."))
    input(colored.white("3. Press press enter to continue when you're ready."))
    body = str(input(colored.white("\nPaste your XML here: ")))

    # Enter user-entered password into document
    fin = baseXml.replace("<!-- password -->", password)
    # Enter user-entered body-text into document
    newFin = fin.replace("<!-- body -->", body)
    # Create the output file and write new xml to it.
    with open("output.xml", "w") as fout:
        fout.write(newFin)
        print("\n\n...Creating XML file", end="")

def submitXML(suvAdress):
    # submits xml file to wd and save response
    print("...Submitting XML to SUV...")
    print("\n\n")
    # open a file for SUV response.
    responseFile = open("responseFile.xml", "w")
    # submit user generated XML to SUV and save to variable.
    response = os.system(f"curl -X POST --data @output.xml {suvAdress} -o responseFile.xml")
    response = str(response)
    # write the response to the file
    responseFile.write(response)
    print("\n\nResponse file created. Please check the SubSuds folder for responseFile.xml")
    responseFile.close()

def parseURL(suv):
    # If user inputs entire url, returns the correct portion to login.suvNumber
    if len(suv) > 17:
        return suv.split("-")[1].split(".")[0]
    else:
        return suv


main()
