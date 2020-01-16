import csv
import matplotlib.pyplot as plt
from collections import Counter
from future.backports import datetime
from variables import MyGlobals

#Retourne deux listes:
#Une liste de date de commandes d'un ATC pour une année donnée
#Une liste des clients qui ont effectués ces commandes
def get_date_for_one_year(name_atc,path_file,year):
    with open(path_file,newline='') as csvfile:
        reader = csv.DictReader(csvfile,delimiter=';',quotechar='|')
        list =[]
        list_client = []
        for row in reader:
            if(name_atc == row["L_ATC3"] and ("/"+year) in row["Date_order"]):
                l = row["Date_order"]
                list.append(l)
                list_client.append([row["Ben_Unique_TI"],row["Date_order"]])
        return list,list_client



# Retourne trois strings, le jour, le mois, l'année
def get_day_month_year(s):
    s2 = s.split(' ')
    s3 = s2[0].split('/')
    return s3[0],s3[1],s3[2]



# Retourne deux strings
#La première au format "%m-%d" avec d la valeur du jour spécifié
#La deuxième étant l'année
def get_month_year(s,d):
    s1 = get_day_month_year(s)
    return s1[1]+"-"+str(d),s1[2]



# Retourne une liste de date traitée par la fonction get_month_year(s):
def get_month_year_list(l,d):
    l2 = []
    for i in l:
        l2.append([get_month_year(i,d)])
    return l2



# Convertit les dates dans un format compatible pour le traitement (timestamp)
def get_dayMonth_list_dateTimeFormat_oneYear(l):
    l2 = []
    for i in l:
        l2.append(datetime.datetime.strptime("1980-"+i[0][0], '%Y-%m-%d'))
    return l2



# Ajoute un "bar" à la figure courante
def add_plot(name_atc,list_atc,width_bar,fix_day):
    list_tupple_date = get_month_year_list(list_atc,str(fix_day))
    list_one_year=get_dayMonth_list_dateTimeFormat_oneYear(list_tupple_date)
    if(len(list_one_year) == 0):
        return
    list_one_year_count =Counter(list_one_year)
    list_one_year_count_sorted = sorted(list_one_year_count.items(), key=lambda t: t[0])
    x_val = [x[0] for x in list_one_year_count_sorted]
    y_val = [x[1] for x in list_one_year_count_sorted]
    plt.bar(x_val,y_val,width=width_bar,label=name_atc+" ( nombre de commandes : "+str(len(list_atc))+" )")



def show_bar_atc1_and_atc2(list_client1,list_client2,day,width_bar,name_bar):
    list_mix = []
    for i in list_client1:
        i[1]=get_month_year(i[1],day)[0]
        for j in list_client2:
            if("-" not in j[1]):
                j[1]=get_month_year(j[1],day)[0]
            if(i[0]==j[0] and i[1]==j[1]):
                list_mix.append(datetime.datetime.strptime("1980-"+i[1], '%Y-%m-%d'))
                break
    if(len(list_mix)==0):
        return
    list_mix_count =Counter(list_mix)
    list_one_year_count_sorted = sorted(list_mix_count.items(), key=lambda t: t[0])
    x_val = [x[0] for x in list_one_year_count_sorted]
    y_val = [x[1] for x in list_one_year_count_sorted]
    plt.bar(x_val,y_val,width=width_bar,label=name_bar+" ( nombre : "+str(len(list_mix))+" )")



def show_histo_between_atc(name_atc1,name_atc2,year,path_data_file):
    list_atc1,list_client_atc1 = get_date_for_one_year(name_atc1,path_data_file,year)
    list_atc2,list_client_atc2 = get_date_for_one_year(name_atc2,path_data_file,year)
    MyGlobals.queue1.put((name_atc1,name_atc2,year,list_atc1,list_atc2,list_client_atc1,list_client_atc2))
    return



def formatToFileName(string):
    string=string.replace("/","")
    string=string.replace("\\","")
    string=string.replace(":","")
    string=string.replace("*","")
    string=string.replace("?","")
    string=string.replace("\"","")
    string=string.replace("<","")
    string=string.replace(">","")
    string=string.replace("|","")
    return string




