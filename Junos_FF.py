## import all needed module ##
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from pprint import pprint
from jinja2 import Template
import yaml

## Menu ##
menu = ''
while menu != 'e' : 
    print('===== Welcone to JUNOS FF =====')
    print('select menu')
    print('1) Connect to Juniper device')
    print('2) Check connection info')
    print('3) New Customer FF Service')
    print('4) ??????')
    print('5) Close connection')
    print('e) Exit')
    ##print('t) Test yaml + jinja2')
    print('=============================')
    menu = input('Enter your choice : ')

    ## Menu 1 ##
    if menu == '1' :
        IP = input('Enter your device IP (eg. 192.168.100.250) : ')
        username = input('Enter your user name : ')
        pssword = input('Enter password : ')
        dev = Device(host=IP,user=username,password=pssword)
        
        dev.open()

        print('Your device is connected? : ', dev.connected)

    ## Menu 2 ##
    elif menu == '2' : 
        pprint(dev.facts)

    ## Menu 3 ##
    elif menu == '3' : 

        ## input info ##
        cusName = input('Add your customer name : ')
        prefix = input('Add your prefix (eg. 192.168.100.0/24) : ')
        cusBW = input('Add limit B/W (Mbps) : ')
        cusUpload = input('Add upload speed (Mbps) : ')
        cusUploadName = cusName+'-upload'
        cusDownload = input('Add download speed (Mbps) : ')
        cusDownloadName = cusName+'-download'

        ## check configuration ##
        print('Check configuration : ')
        print(cusName)
        print(prefix)
        print(cusBW+' Mbps')
        print(cusUploadName + ': Upload speed = ' + cusUpload + ' Mbps')
        print(cusDownloadName + ': Download speed = ' + cusDownload + ' Mbps')
        
        ## translate to junos set configuration ##
        jtemp = open("Junos_Tmp_FF.j2").read()
        jRender = Template(jtemp)
        
        with open('sampleConfig.conf','w') as outFile : 
            outFile.write(jRender.render(cusName=cusName,prefix=prefix,cusBW=cusBW,cusUpload=cusUpload,cusUploadName=cusUploadName,cusDownload=cusDownload,cusDownloadName=cusDownloadName))
        
        cfg = Config(dev)
        cfg.load(path='sampleConfig.conf',merge=True,format='set')
        cfg.pdiff()
        cfg.commit()
        dev.close()
        
    ## Menu 5 ##
    elif menu == '5' :
        dev.close()
        print('Your device is connected? : ', dev.connected)

     ## Menu Test ##
    ##elif menu == 't' :
        ## yim = open('Junos_Prefix.yml').read()
        ## print(yim)

        ## translate to junos set configuration ##
        ##jtemp = open("Junos_Tmp_FF.j2").read()
        ##jRender = Template(jtemp)
        
        ##with open('sampleConfig.conf','w') as outFile : 
            ##outFile.write(jRender.render(cusName=cusName,prefix=prefix,cusBW=cusBW,cusUpload=cusUpload,cusUploadName=cusUploadName,cusDownload=cusDownload,cusDownloadName=cusDownloadName))
            
            ##hostname = input('Enter Hostname : ')
        ##cfg = Config(dev)
            ##varSet = ('set system host-name '+hostname)
            ##cfg.load(varSet,format='set',merge=True)

        ##cfg.load(path='sampleConfig.conf',merge=True,format='set')

        ##cfg.pdiff()

        ##cfg.commit()
            ##dev.close()




        


    



