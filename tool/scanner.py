from easyprocess import EasyProcess
import json
import requests
import os


# ************************************#
# print info about host               #
# ************************************#
def url_string( ip, port ):
     return 'http://'+ip+':'+str(port)+''


# ***************************************#
# check if the host is a domotic device  #
# ***************************************#
def checkHost( host ):
    host = host +"/domotic" # get url string about host
    try:
        response = requests.get( host, timeout=0.5 )
        if response.status_code == 200 and response.text == 'true':
            return True
    except:
        #print ""
        return False
    return False


# ************************************#
# explore all the host in a network   #
#*************************************#
def explore( networks ):
    networks = networks
    for network in networks:
            rango = range(0,254)
            if network == '127.0.0.1':
                rango = [1]
            for index in rango:

                ip = network[:-1] + str( index )
                myport = 9100

                host = url_string( ip, myport )
                print( "[-] check host " + host)
                if checkHost( host ) :
                    try:
                        response = requests.get( host, timeout=0.5)
                        print( response.json())

                        response = requests.post( host + "/register/amenizador/irvin/00012", data = {"providers":"[\"chismogate\"]", "locations":"[\"b\"]"} )
                        return response.json()['port']

                    except:
                        print( " NO JSON ")
                    #print "    [!]domotic device found :) !"
                else:
                    print( "    FAIL :(")
                    print()

    return None
