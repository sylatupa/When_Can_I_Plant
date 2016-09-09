import csv
import os
import itertools
import ast
verbose = False
global reader
reader = csv.reader('')

# curdir = os.getcwd()[:-11] #subtract 'testingAuto to get working directory
# fileWriter = csv.writer(open(curdir+currentFileName, 'w'), delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
# fileWriter.writerow(writeThis)

def getOPENfile(fileName):
    print fileName
    return open(fileName, 'r')

def getCSVreader(fileName):
    reader = csv.reader(getOPENfile(fileName))
    if(verbose):
        for row in reader:
            print row
    return reader


def write_dict_to_csv(columns_as_dict, file_name):
    with open('./'+file_name, 'wb') as f:  # Just use 'w' mode in 3.x
        #w = csv.DictWriter(f,fieldnames = columns_as_dict.keys())
        #w = csv.DictWriter(f, columns_as_dict)
        #w = csv.DictWriter(f, columns_as_dict)
        w = csv.writer(f)
        #l = zip(columns_as_dict.items())
        #w.writerows(l[0],l[1])
        w.writerow(columns_as_dict.keys())
        #print(columns_as_dict.items())
        w.writerows(zip(*columns_as_dict.values()))
        #w.writerows(columns_as_dict.items)
        #for row in columns_as_dict :
            #w.writerow(row)
         #   print row
        #w = csv.DictWriter(f,(*columns_as_dict()))

        #w.writerows(zip(*columns_as_dict.values()))

##        with open('in.csv') as f:
##            r = csv.reader(f)
##            d = defaultdict(columns_as_dict)
##            for row in r:
##                columns_as_dict[row[0]].append(row[1:])
##        print(d)
def getDataTypes(reader):
    #reader.next()
    list = []
    print reader[1]
    for column in reader[1]:
        try:
            list.append(type(ast.literal_eval(column)).__name__)
        except:
            list.append(type(column).__name__)
    if(verbose):
        print list
    return list

def create_histogram( columns_as_dict, column_stats, bins, number_of_rows):
    hists_dict = dict()
    for column in columns_as_dict.keys():
        column_max = column_stats['max'][column]
        column_min = column_stats['min'][column]
        hists = []
        bin_span = 0
        #positive max numbr and negative min number I add it and then divide by bin-1
        if(column_max >= 0 and column_min < 0):
            distance_from_zero = column_max + column_min
            bin_span = distance_from_zero / (bins - 1)
        #negative max number (and min): subract the abs max from the abs min (3-1=2) and then divide by bin-1
        elif(column_max < 0 and column_min < 0):
            bin_span = (abs(column_min) - column_max) / (bins-1)
        #positive max and positive min number I subract the min from the max then divide by bin
        elif(column_max > 0 and column_min >= 0):
            distance_from_zero = column_max - column_min
            bin_span = distance_from_zero / bins
        for b in range(0,bins):
            if(b == 0):
                hists.insert(b,column_min)
            elif(b == bins-1):
                hists.insert(b,column_max)
            else:
                hists.insert(b,hists[b-1]+bin_span)
        hists_dict[column] = hists

    return hists_dict

def get_column_dict(headers, columns_as_row_data):
    column_dict = dict()
    columnNum = 0
    for header in headers:
        #print header
        #print type(columns_as_row_data[columnNum])
        column_dict[header] = list(columns_as_row_data[columnNum])
        columnNum = columnNum + 1
    return column_dict

def subtract_columns(Hipx,Hipy,Hipz, columns_as_dict, number_of_rows):
    column_subract_dict = dict()
    for column in columns_as_dict.keys():
        column_name = 'substr' + column
        templist = []
        if 'x' in column:
            substr_column = Hipx
        if 'y' in column:
            substr_column = Hipy
        if 'z' in column:
            substr_column = Hipz
        for row_number in range(0,number_of_rows):
            templist.append(round(columns_as_dict[substr_column][row_number] - columns_as_dict[column][row_number],5))
        column_subract_dict[column_name] =  templist
    return column_subract_dict

# FUNTION USES A LIST OF DATATYPES AND THE DATA AND CONVERTS THE DATA TO THE APPROPRIATE DATATYPE
# TODO: ONLY GOOD FOR INT AND FLOAT
def get_list_data(dataTypes, list):
    list_of_data_w_types = []
    column_num = 0  #skip first row
    for type in dataTypes:
        if(type == 'int'):
            list_of_data_w_types.append([float(i) for i in list[column_num]])
        elif(type == 'float'):
            #print 'float ' + list[column_num][1]
            list_of_data_w_types.append([float(i) for i in list[column_num]])
        else:
            list_of_data_w_types.append([i for i in list[column_num]])
        column_num = column_num + 1
    return list_of_data_w_types

def get_column_stat(columns_as_dict):
        columns_stats = dict()
        internal_dict = dict()
        for key in columns_as_dict.keys():
            internal_dict[key] = max(columns_as_dict[key])
        columns_stats['max'] = internal_dict

        internal_dict = dict()
        for key in columns_as_dict.keys():
            internal_dict[key] = min(columns_as_dict[key])
        columns_stats['min'] = internal_dict

        #internal_dict = dict()
        #for key in columns_as_dict.keys():
        #    internal_dict[key] = ([sum(i)/number_of_rows for i in columns_as_rows_data])
        #columns_stats['avg'] = internal_dict

        return columns_stats

def add_classified_columns(columns_as_dict, column_stats):
    classified_columns = dict()
    for key in columns_as_dict:
        temp_list = []
        rownum = 0
        for element in columns_as_dict[key]:
            bin_num = 0
            for bin in column_stats['hist'][key]:
                if element <= bin:
                    temp_list.append(bin_num)
                    break;
                else:
                    bin_num = bin_num + 1
            rownum = rownum + 1
        classified_columns['hist'+key] = temp_list
    return classified_columns



##positive max numbr and negative min number I add it and then divide by bin-1
##positive max and positive min number I subract the min from the max then divide by bin
##negative max number (and min): subract the abs max from the abs min (3-1=2) and then divide by bin-1
##
##positive max numbr and negative min number I add it and then divide by bin-1
##1.5	2		8	11
##1	1.5		5.25	8.25
##0.5	1		2.5	5.5
##0	0.5		-0.25	2.75
##-0.5	0		-3	0
##
##
##positive max and positive min number I subract the min from the max then divide by bin
##1.75	1.25
##	1
##	0.75
##	0.5
##	0.25
##0.5	0
##
##negative max number (and min): subract the abs max from the abs min (3-1=2) and then divide by bin-1
##	-1	1
##	-1.4	0.2
##	-1.8	-0.6
##	-2.2	-1.4
##	-2.6	-2.2
##	-3	-3
