import os # enables curl
import xml.etree.ElementTree as ET

def main():
    user = Log_In()
    exit = 1
    while exit > 0:
        createXmlFile(user.password)
        submitXML(user.SuvAddress())
        exit = int(input("\n\nPress 1 to continue or 0 to exit program. "))
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
    self.suvNumber = parseURL(str(input("\nSUV number: ")))  #
    self.userName = 'superuser@super'
    self.password = str(input("\nSUV password: "))

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
    print("\nPlease copy everything between the body tags <SOAP-ENV:Body> and </SOAP-ENV:Body> in your XML.")
    body = str(input("\nRemove all spaces so it's all one continuous line, and then paste it here: "))
    # Enter user-entered password into document
    fin = baseXml.replace("<!-- password -->", password)
    # Enter user-entered body-text into document
    newFin = fin.replace("<!-- body -->", body)
    # Create the output file and write new xml to it.
    with open("output.xml", "w") as fout:
        fout.write(newFin)
        print("\nCreating XML file...\n")

def submitXML(suvAdress):
    # submits xml file to wd and save response
    print("\nSubmitting XML to SUV...\n\n")
    # open a file for SUV response.
    responseFile = open("responseFile.xml", "w")
    # submit user generated XML to SUV and save to variable.
    response = os.system(f"curl -X POST --data @output.xml {suvAdress} -o responseFile.xml")
    # convert response to string
    response = str(response)
    # write the response to the file
    responseFile.write(response)
    responseFile.close()

def parseURL(suv):
    # If user inputs entire url, returns the correct portion to login.suvNumber
    if len(suv) > 17:
        return suv.split("-")[1].split(".")[0]
    else:
        return suv

main()
