import os
import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from collections import Counter
from future.backports import datetime
from interactiveLegend import InteractiveLegend
import numpy as np
from variables import Variables


def interactive_legend(ax=None):
    if ax is None:
        ax = plt.gca()
    if ax.legend_ is None:
        ax.legend()

    return InteractiveLegend(ax.get_legend())


def get_EAN13(name_atc,path_file):
    with open(path_file,newline='') as csvfile:
        reader = csv.DictReader(csvfile,delimiter=';',quotechar='|')
        list =[]
        for row in reader:
            if(name_atc == row["L_ATC3"]):
                l = [row["lat"],row["lon"]]
                list.append(l)
        return list

def get_date(name_atc,path_file):
    with open(path_file,newline='') as csvfile:
        reader = csv.DictReader(csvfile,delimiter=';',quotechar='|')
        list =[]
        for row in reader:
            if(name_atc == row["L_ATC3"]):
                l = row["Date_order"]
                list.append(l)
        return list




def get_day_month_year(s):
    s2 = s.split(' ')
    s3 = s2[0].split('/')
    return s3[0],s3[1],s3[2]

def get_dayMonth_year(s):
    s1 = get_day_month_year(s)
    #return s1[1],s1[2]
    #return s1[1]+"-"+s1[0],s1[2]
    if(0<=int(s1[0])<=15):
        return s1[1]+"-1",s1[2]
    else:
        return s1[1]+"-15",s1[2]



def get_dayMonth_year_list(l):
    l2 = []
    for i in l:
        l2.append([get_dayMonth_year(i)])
    #print(l2)
    return l2

def get_dayMonth_list_dateTimeFormat(l,year):
    l2 = []
    for i in l:
        if(year==i[0][1]):
            l2.append(datetime.datetime.strptime("2000-"+i[0][0]+" 11:11:11.11", '%Y-%m-%d %H:%M:%S.%f'))
        #l2.append("0-"+i[0][0]+" 00:00:00.0")

    return l2


def yeared_list(list):
    year_list = []
    for i in list:

        if(i[0][1] not in year_list):
            year_list.append(i[0][1])
    return year_list



def show_graph_atc3(name_atc,path_data_file):
    # On récupère toutes les dates de commandes de l'atc rentré
    list_all_date= get_date(name_atc,path_data_file)

    # On récupère une liste de tupple de la forme ('m-d','y') avec le jour arrondit à 1 ou à 15
    list_tupple_date = get_dayMonth_year_list(list_all_date)

    # On récupère une liste de toutes les années différentes
    list_year = yeared_list(list_tupple_date)

    Variables.queue1.put((list_tupple_date,list_year,name_atc))
    return

def add_plot(list,label):
    l=Counter(list)
    l = sorted(l.items(), key=lambda t: t[0])
    x_val = [x[0] for x in l]
    y_val = [x[1] for x in l]
    plt.plot(x_val,y_val,label=label)





