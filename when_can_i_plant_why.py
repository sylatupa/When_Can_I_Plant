#import stats
import io_read_file
import csv
import os
import datetime
import socket
import time
import random
import sys
import io_read_file
tables_reader = ''
export_reader = ''
tables_list = ''
export_list = ''
writer = ''
reader = ''
verbose = False
csv_file = ''
#import serial
path = ''

print (sys.platform == 'linux2')
print  (str(os.getenv("USERNAME")) == 'None')
print sys.platform
print os.getenv("USERNAME")

sys_usr = ""
if sys.platform =='win32':
    sys_usr = 'mydesktop'
elif (sys.platform == 'linux2') & (str(os.getenv("USERNAME")) == 'None'):
    sys_usr = 'raspberry'
elif (sys.platform == 'linux2') & (os.getenv("USERNAME") == 'None'):
    sys_usr = 'saguaro'
print 'sysuser value' , sys_usr
if sys_usr == 'mydesktop':
    path = 'C:\Dropbox (Personal)\PROJECTS_WORKING\When_Can_I_Plant'
    os.chdir(path)
    sys.path.append(path)
elif sys_usr == 'raspberry':
    print 'using raspberry'
    global device
    print os.getenv("USERNAME")
    path = '/home/pi/Documents/When_Can_I_Plant'
    os.chdir(path)
    sys.path.append(path)
    import max7219.led as led
    import RPi.GPIO as GPIO ## Import GPIO library
    device = led.matrix(cascaded=1)
    device.brightness(7)
    GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
#    GPIO.setup(7, GPIO.OUT) ## Setup GPIO Pin 7 to OUT
#    GPIO.output(7,False) ## Turn on GPIO pin 7
elif sys_usr == 'saguaro':
    path = './home/sylatupa'
    print 'no username, you should be using saguaro'
    os.chdir(path)
    sys.path.append(path)

class csvFile:
    """building stat framework for file"""
    def __init__(self, input_file):
        print "Reading file: " + input_file

        self.data = []
        self.input_file = input_file
        self.csv_reader = io_read_file.getCSVreader(self.input_file)
        self.list = list(self.csv_reader)
        self.headers = self.list[0]
        self.dataTypes = io_read_file.getDataTypes(self.list)
        self.number_of_rows = len(self.list)-1
        self.number_of_columns = len(self.list[0])
        self.list = self.list[1:] #remove the header row
        self.columns_as_rows = zip(*self.list)
        self.columns_as_rows_data = io_read_file.get_list_data(self.dataTypes, self.columns_as_rows)
        self.columns_as_dict_strings = io_read_file.get_column_dict(self.headers, self.columns_as_rows)
        self.columns_as_dict_data = io_read_file.get_column_dict(self.headers, self.columns_as_rows_data)

        self.columns_stats = io_read_file.get_column_stat(self.columns_as_dict_data)
def main():
        global tables_reader, export_reader, tables_list, export_list, writer, csv_file, device
        print os.getcwd()
        csv_file = csvFile('micromet_analysis3rd.csv') # Make the cvsFile Object to store info
        #io_read_file.write_dict_to_csv(csv_file.columns_as_dict_strings, 'columns2.csv' )
        #io_read_file.write_dict_to_csv(csv_file.columns_as_dict_data, 'micromet_analysis2.csv' )
        datebegin = 0
        dateend = 364
        slider_forward = True
        var = 1

        while var == 1 :  # This constructs an infinite loop
            if sys_usr == 'raspberry':
                label = 'SUN'
                device.show_message(label)
                device.flush()
                time.sleep(1)

            if slider_forward == False:
                rotation = dateend
                dateend = datebegin
                datebegin = rotation
            elif slider_forward == False:
                rotation = dateend
                dateend = datebegin
                datebegin = rotation

            for i in range(datebegin,dateend):
                max_netrad_avg = 197.85
                #max_value = csv_file.columns_stats[current_data_set]
                actual_day = int(round((csv_file.columns_as_dict_data['DayOfYear'][i])))
                day1 = int(round((csv_file.columns_as_dict_data['DayOfYear'][i]/365)*8))

                if (actual_day <= 357):


                    for rownum in range(0,7,):
                        rand = random.choice([-1,1])
                        day = day1 + rownum
                        #avg_netrad_avg = ((csv_file.columns_as_dict_data['avg_netrad_avg'][i+rownum] + (csv_file.columns_as_dict_data['stnddev_netrad_avg'][i+rownum] * rand)) / ((csv_file.columns_as_dict_data['stnddev_netrad_avg'][i+rownum] * rand) + max_netrad_avg))
                        print  'avg_netrad_avg: ' ,csv_file.columns_as_dict_data['avg_netrad_avg'][i+rownum]
                        print 'stddev_netrad_avg: ' , (csv_file.columns_as_dict_data['stnddev_netrad_avg'][i+rownum])
                        avg_netrad_avg_numer = (csv_file.columns_as_dict_data['avg_netrad_avg'][i+rownum] + (csv_file.columns_as_dict_data['stnddev_netrad_avg'][i+rownum] * rand))
                        avg_netrad_avg_denom = ((csv_file.columns_as_dict_data['stnddev_netrad_avg'][i+rownum] * rand) + max_netrad_avg)
                        avg_netrad_avg = int(round((avg_netrad_avg_numer / avg_netrad_avg_denom)*8))

                        print 'day:' , day
                        print 'actual value' ,csv_file.columns_as_dict_data['avg_netrad_avg'][i+rownum]
                        print 'numr1:', csv_file.columns_as_dict_data['avg_netrad_avg'][i+rownum]
                        print ' + ' , csv_file.columns_as_dict_data['stnddev_netrad_avg'][i+rownum]
                        print ' * ',  rand
                        print "numr", avg_netrad_avg_numer
                        print "stnd dev",(csv_file.columns_as_dict_data['stnddev_netrad_avg'][i+rownum])
                        print "denom", avg_netrad_avg_denom
                        print "avg_netrad_avg norm: ", avg_netrad_avg

                        print "Final", day, " ".join(["%s"%' ' for i in range(int(avg_netrad_avg))])  , avg_netrad_avg

                        time.sleep(.01)

                        if sys_usr == 'raspberry':
                            print 'testtesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttest'
                            if( day < 8 & day >= 0 & avg_netrad_avg < 8 & avg_netrad_avg>=0):
                                print 'matrix cant even handle'
                                device.pixel(day, int(round((avg_netrad_avg_numer/avg_netrad_avg_denom)*8))-6, 1, redraw=True)
                                device.flush()

                    if sys_usr == 'raspberry':
                        device.clear()

                if 1==1:
                    avg_netrad_avg_numer = (csv_file.columns_as_dict_data['avg_netrad_avg'][i] + (csv_file.columns_as_dict_data['stnddev_netrad_avg'][i] * rand))
                    avg_netrad_avg_denom = ((csv_file.columns_as_dict_data['stnddev_netrad_avg'][i] * rand) + max_netrad_avg)
                    avg_netrad_avg = int(round((avg_netrad_avg_numer / avg_netrad_avg_denom)*8))
                    print "Final", actual_day, " ".join(["%s"%' ' for i in range(int(avg_netrad_avg))])  , avg_netrad_avg



##
##        UDP_IP = "127.0.0.1"
##        UDP_PORT = 5005
##        MESSAGE = "Hello, World!"
##
##        print "UDP target IP:", UDP_IP
##        print "UDP target port:", UDP_PORT
##        print "message:", MESSAGE
##
##        sock = socket.socket(socket.AF_INET, # Internet
##                             socket.SOCK_DGRAM) # UDP
##        for b in range(9):
###            for a in len(csv_file.columns_as_dict_data):
##            for a in range(5):
##            #    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
##
##                d = str(int(csv_file.columns_as_dict_data.items()[10][1][a])*300)
##                sock.sendto(d, (UDP_IP, UDP_PORT))
##                print d
##                time.sleep(.01)
##        #sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

if __name__=='__main__':
    main()


def rotate(l,n):
    return l[n:] + l[:n]
#def print_object_example(objIn):
