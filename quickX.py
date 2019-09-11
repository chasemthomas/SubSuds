import os # enables curl
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import fromstring

def main():
  user = Log_In()
  suvAddress = user.SuvAddress()
  cont = 1
  while cont > 0:
      input("\nPaste your xml into 'generic.xml,' save the file, and then press enter to continue.")
      createXml = createXmlFile(user.password)
      submitXML(suvAddress)

      # submitXML(suv_address)
      cont = int(input("\n\nPress 1 to continue or 0 to exit program. "))
  print("\n")

class Log_In:
  '''
  Asks the user for the .suvNumber, .userName, and .password.
  Creates an .SuvAddress string from user input.
  '''
  prefix = "https://i-"
  middle = ".workdaysuv.com/ccx/service/super/"
  implementationService = "Financials_Implementation_Service"
  version = "33.0"

  def __init__(self):
    self.suvNumber = str(input("\nSUV number: "))
    self.userName = 'superuser@super'
    self.password = str(input("SUV password: "))

  def SuvAddress(self):
      SuvAddress = f"{self.prefix}{self.suvNumber}{self.middle}{self.implementationService}/v{self.version}"
      return SuvAddress

def createXmlFile(password):
    '''
    Takes in password and userXML.
    Returns a new xml document.
    '''
    # parse XML base string into element tree
    tree = ET.parse("input.xml")
    # set the root element
    root = tree.getroot()
    # namespaces must be registered or they will be overridden by tree.write()
    ET.register_namespace("SOAP-ENV","http://schemas.xmlsoap.org/soap/envelope/", )
    ET.register_namespace("bsvc","urn:com.workday/bsvc")
    ET.register_namespace("wsse","http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd")
    # mapping the namespaces so they can be found with root.find
    namespaces = {
    'SOAP-ENV': 'http://schemas.xmlsoap.org/soap/envelope/',
    'bsvc': 'urn:com.workday/bsvc',
    'wsse': 'http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd'
    }
    # Write user-entered password to xml document
    headerPassword = root.find('.//wsse:Password', namespaces=namespaces)
    headerPassword.text = password
    print("\nCreating XML file...")
    # save info to new xml file
    with open('output.xml', 'w'):
        tree.write("output.xml")

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


main()
