from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import webbrowser
import csv
import folium
from folium import plugins
import os
import matplotlib.dates as mdates
from matplotlib import pyplot as plt
from PIL import ImageTk
from all_years_curves_one_atc import show_graph_atc3,get_dayMonth_list_dateTimeFormat,add_plot as annee_add_plot,interactive_legend
from histo_between_two_atc import show_histo_between_atc,get_day_month_year,show_bar_atc1_and_atc2, add_plot as twoatc_add_plot
import threading
import queue
from variables import MyGlobals



#Fonction qui permet de notifier l'utilisateur en cas de mauvaise manipulation de sa part
def popupmsg(msg):
    popup = Toplevel()
    popup.iconbitmap("logo-pharmacie-médical.ico")
    popup.title("Attention")
    label = Label(popup, text=msg) #Can add a font arg here
    label.pack(side="top", fill="x", pady=10)
    B1 = Button(popup, text="OK", command = popup.destroy)
    B1.pack()
    return


#Fonction permettant de lancer toutes les analyses selectionnées puis de sauvegarder les fichiers d'analyses dans des dossiers prévus pour
def sauvegarde():
    a2 = MyGlobals.deroulant.get()#On récupère ici le nom de l'ATC que l'utilisateur a décidé de traîter
    if MyGlobals.deroulant2.winfo_ismapped() and (MyGlobals.deroulant2.get() == '' or MyGlobals.deroulant_dates.get() == '' or a2 ==''):
        popupmsg("Veuillez sélectionner les deux catégories de médicaments ainsi que la période avant de lancer l'analyse")
    elif a2 =='' and not MyGlobals.deroulant2.winfo_ismapped():
        popupmsg("Veuillez sélectionner une catégorie de médicaments avant de lancer l'analyse")
    else:
        filename=formatToFileName(a2)
        chemin_carte =os.path.abspath("Cartes/"+filename)
        if not os.path.exists(os.path.abspath("Cartes/")):
            os.makedirs(os.path.abspath("Cartes/"))
        MyGlobals.queue1 = queue.Queue()
        plt.close()
        thr2 = threading.Thread(target=performAnalysis, args=(MyGlobals.deroulant.get(),chemin_carte,queue), kwargs={})
        thr2.start()
    return


#Fonction qui permet de faire l'analyse de la répartition de la maladie choidie sur les deux sexes
def process_queue_sexe():
    try:
        queue_variables=MyGlobals.queue1.get(0)
        sizes = queue_variables[0]
        labels=queue_variables[1]
        colors=queue_variables[2]
        name_atc=queue_variables[3]
        plt.pie(sizes, labels=labels, colors=colors,autopct='%1.1f%%', shadow=True, startangle=90)
        plt.axis('equal')
        if not os.path.exists(os.path.abspath("Diagrammes\Sexes")): 
            os.makedirs(os.path.abspath("Diagrammes\Sexes"))
        plt.savefig(os.path.abspath('Diagrammes\Sexes\\'+name_atc+'.png'))
        plt.show()
    except queue.Empty:
        window.after(500, process_queue_sexe)


def process_queue_annee():
    try:
        queue_variables=MyGlobals.queue1.get(0)
        list_tupple_date = queue_variables[0]
        list_year=queue_variables[1]
        name_atc=queue_variables[2]
        plt.rcParams["figure.figsize"] = (12,5)
        plt.figure(name_atc)
        locator = mdates.MonthLocator()
        fmt = mdates.DateFormatter('%b')
        X = plt.gca().xaxis
        X.set_major_locator(locator)
        X.set_major_formatter(fmt)
        for i in list_year:
            # On convertit les dates d'une année choisit pour qu'elles correspondent au format d'affichage
            list_dateformat = get_dayMonth_list_dateTimeFormat(list_tupple_date,i)
            annee_add_plot(list_dateformat,i)
        plt.legend( bbox_to_anchor=(1, 1), loc='upper left', borderaxespad=0.)
        plt.title(name_atc)
        leg = interactive_legend()
        if 1==1 :
            if not os.path.exists(os.path.abspath("Diagrammes\Année")):
                os.makedirs(os.path.abspath("Diagrammes\Année"))
            plt.savefig(os.path.abspath('Diagrammes\Année\\'+name_atc+'.png'))
        plt.show()
    except queue.Empty:
        print("queue empty")
        window.after(500, process_queue_annee)


def process_queue_croisement():
    try:
        queue_variables=MyGlobals.queue1.get(0)
        name_atc1=queue_variables[0]
        name_atc2 = queue_variables[1]
        year=queue_variables[2]
        list_atc1=queue_variables[3]
        list_atc2=queue_variables[4]
        list_client_atc1=queue_variables[5]
        list_client_atc2=queue_variables[6]
        width_bar = 4
        fix_day1=1
        fix_day2=5
        fix_day3=9
        plt.rcParams["figure.figsize"] = (12,7)
        plt.figure(year+": "+name_atc1 +" VS "+name_atc2)
        twoatc_add_plot(name_atc1,list_atc1,width_bar,fix_day1)
        twoatc_add_plot(name_atc2,list_atc2,width_bar,fix_day2)
        show_bar_atc1_and_atc2(list_client_atc1,list_client_atc2,fix_day3,width_bar,"Achat des deux par une même personne le même mois")
        locator = mdates.MonthLocator()
        fmt = mdates.DateFormatter('%b')
        X = plt.gca().xaxis
        X.set_major_locator(locator)
        X.set_major_formatter(fmt)
        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
                mode="expand", borderaxespad=0.,fontsize='small')
        if 1==1 :
            if not os.path.exists(os.path.abspath("Diagrammes\Croisements")):
                os.makedirs(os.path.abspath("Diagrammes\Croisements"))
            plt.savefig(os.path.abspath('Diagrammes\Croisements\\'+formatToFileName(name_atc1+'+'+name_atc2)+'.png'))
        plt.show()
    except queue.Empty:
        print("queue empty")
        window.after(500, process_queue_sexe)


#Fonction qui est appelé par sauvegarde() et qui permet de lancer les calculs qui sont selectionnés par l'utilisateur
def performAnalysis(a2,chemin_carte,queue):
    nb_operations=valeur_case_graph_annee.get()+valeur_case_graph_sexe.get()+valeur_case_calcul_carte.get()+MyGlobals.deroulant2.winfo_ismapped()
    if valeur_case_calcul_carte.get():
        progressbar_title["text"]='Création de la carte en cours'
        carto(a2,MyGlobals.chemin,chemin_carte)
        progressbar["value"]+=100/nb_operations
    if valeur_case_graph_sexe.get():
        progressbar_title["text"]='Creation du graph \"Répartition selon le sexe\" en cours'
        graph_sexe(a2,MyGlobals.chemin)
        window.after(0,process_queue_sexe)
        progressbar["value"]+=100/nb_operations
    if valeur_case_graph_annee.get() :
        progressbar_title["text"]='Creation du graph \"Année\" en cours'
        show_graph_atc3(a2,MyGlobals.chemin)
        window.after(100,process_queue_annee)
        progressbar["value"]+=100/nb_operations
    if MyGlobals.deroulant2.winfo_ismapped():
        progressbar_title["text"]='Creation du graph \"Croisement\" en cours'
        show_histo_between_atc(a2,MyGlobals.deroulant2.get(),MyGlobals.deroulant_dates.get(),MyGlobals.chemin)      
        window.after(0,process_queue_croisement)
        progressbar["value"]+=100/nb_operations
    progressbar["value"]=0
    progressbar_title["text"]=''


#Fonction qui permet de regler les problèmes de lecture de certains caractères lors de la récupération du texte dans les menus déroulants
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


#Fonction permettant d'ouvrir le fichier csv necessaire en entrée du programme et de remplir les menus déroulant
def ouverture_fichier_de_base():
    window.fileName = filedialog.askopenfilename(filetype =(("CSV files","*.csv"),("PDF file","*.pdf"),("HTML files","*.html")))
    MyGlobals.chemin = window.fileName
    MyGlobals.myCSV = []
    if window.fileName!='':
        thr = threading.Thread(target=getAllATCCodes, args=(window.fileName,), kwargs={})
        thr.start()
    else:
        MyGlobals.deroulant.set('')
        MyGlobals.deroulant['values'] = []
        MyGlobals.deroulant['state'] = 'disabled'
        MyGlobals.deroulant2.set('')
        MyGlobals.deroulant2['values'] = []
        MyGlobals.deroulant2['state'] = 'disabled'
        bouton_analyse['state'] = 'disabled'
    return([window.fileName,MyGlobals.myCSV])


#Permet de lire tous les codes ATC présents dans le csv et de remplir les menus déroulants avec
def getAllATCCodes(fileName):
    progressbar_title['text']='Chargement du fichier en cours'
    progressbar['mode']='indeterminate'
    progressbar.start()
    with open(fileName, newline = '') as csvfile :
        readerMan = csv.DictReader(csvfile, delimiter=';',quotechar='|')
        header=readerMan.fieldnames
        if header != MyGlobals.fileHeader:
            MyGlobals.deroulant.set('')
            MyGlobals.deroulant['values'] = []
            MyGlobals.deroulant['state'] = 'disabled'
            MyGlobals.deroulant2.set('')
            MyGlobals.deroulant2['values'] = []
            MyGlobals.deroulant2['state'] = 'disabled'
            bouton_analyse['state'] = 'disabled'
            popupmsg('Le fichier selectionné est incorrect ou corrumpu')               
            return
        for row in readerMan :
            if test_de_presence(MyGlobals.myCSV,row["L_ATC3"]) == 1  or len(MyGlobals.myCSV) ==0 :
                MyGlobals.myCSV.append(row["L_ATC3"])
            annee = get_day_month_year(row["Date_order"])[2]
            if test_de_presence(MyGlobals.mesDates,annee) == 1 or len(MyGlobals.mesDates)==0 :
                MyGlobals.mesDates.append(annee)
    MyGlobals.mesDates.sort()
    MyGlobals.myCSV.sort()
    MyGlobals.deroulant['values']=MyGlobals.myCSV
    MyGlobals.deroulant['state'] = 'readonly'
    MyGlobals.deroulant2['values']=MyGlobals.myCSV
    MyGlobals.deroulant2['state'] = 'readonly'
    MyGlobals.deroulant_dates['values'] = MyGlobals.mesDates
    MyGlobals.deroulant_dates['state'] = 'readonly'
    bouton_analyse['state'] = 'normal'
    progressbar_title['text']=''
    progressbar.stop()
    progressbar['mode']='determinate'


#Fonction permettant de vérifier si un élément (ici MonSujet) est déjà présent dans une liste
def test_de_presence(maListe,monSujet):
    x = 1
    if len(maListe) != 0 :
        for i in maListe:
            if i == monSujet:
                x = 0
    return x


#Fonction qui permet à l'utilisateur de choisir sur quelle ville centrer la carte (Création de la fenêtre)
def menuParametre():
    para = Toplevel()
    para.title("Paramètres")
    para.geometry("360x140")
    para.iconbitmap("logo-pharmacie-médical.ico")
    labelPara = Label(para) #Can add a font arg here
    labelPara.pack(side="top", fill="x", pady=10)
    MyGlobals.choix_ville = IntVar()
    MyGlobals.choix_ville.set(0)
    for val,ville in enumerate(MyGlobals.liste_villes):
        if ville[0] == MyGlobals.lieu_actuel[0] :
            MyGlobals.choix_ville.set(1)
        else :
            MyGlobals.choix_ville.set(0)
        Radiobutton(para,text = ville[0],padx = 20, variable = MyGlobals.choix_ville,value = val,command = choix_lieu).pack()
    B1 = Button(para, text="OK", command = para.destroy)
    B1.pack()
    para.mainloop()


#Fonction qui permet à l'utilisateur de choisir sur quelle ville centrer la carte (Modification de la variable)
def choix_lieu():
    MyGlobals.lieu_actuel = [MyGlobals.liste_villes[MyGlobals.choix_ville.get()][0],[MyGlobals.liste_villes[MyGlobals.choix_ville.get()][2][0],MyGlobals.liste_villes[MyGlobals.choix_ville.get()][2][1]]]


#Fonction permettant l'ouverture de la carte
def ouvrir_carte():
    window.fileName = filedialog.askopenfilename(filetype =(("HTML files","*.html"),))
    webbrowser.open_new(window.fileName)
    return(window.fileName)


def get_EAN13(name_atc,path_file):
    with open(path_file,newline='') as csvfile:
        reader = csv.DictReader(csvfile,delimiter=';',quotechar='|')
        list =[]
        for row in reader:
            if(name_atc == row["L_ATC3"]):
                l = [row["lat"],row["lon"]]
                list.append(l)
        return list


def graph_sexe(name_atc,path_data_file):
    nb_individuals=[0,0,0] # indexes: 0=man, 1=woman, 2=other
    list_ids=[]
    with open(path_data_file,newline='') as csvfile:
        reader = csv.DictReader(csvfile,delimiter=';',quotechar='|')
        for row in reader:
            if row["Ben_TI"]=='0' and row["Cli_TI"] not in list_ids and row["L_ATC3"]==name_atc:
                nb_individuals[int(row["Cli_sexe"])]+=1
                list_ids.append(row["Cli_TI"])
        men_proportion=100*nb_individuals[0]/(nb_individuals[0]+nb_individuals[1])
        women_proportion=100*nb_individuals[1]/(nb_individuals[0]+nb_individuals[1])
        labels = 'Homme','Femme'
        sizes = [men_proportion,women_proportion]
        colors = ['blue','red']
        MyGlobals.queue1.put((sizes,labels,colors,name_atc))
    return


#Fonction permettant de sauvegarder le diagramme des années.
def sauve_annee(fig,name_atc):
    if not os.path.exists(os.path.abspath("Diagrammes\Année")):
        os.makedirs(os.path.abspath("Diagrammes\Année"))
    plt.savefig(os.path.abspath('Diagrammes\Année\\'+name_atc+'.png'))


# Grace à Folium on crée une heatmap représentant la densité d'achat pour un atc
def carto(name_atc,path_data_file,path_html_file):
    list = []
    list = get_EAN13(name_atc,path_data_file)
    m = folium.Map(MyGlobals.lieu_actuel[1], zoom_start=14)
    m.add_child(plugins.HeatMap(list, radius=30,gradient={0: 'blue', 0.6: 'green', 1: 'red'}))
    if not ".html" in path_html_file:
        path_html_file+=".html"
    m.save(path_html_file)
    if valeur_case_affichage_carte.get()==1:
        print(os.path.abspath(path_html_file))
        webbrowser.open_new_tab(os.path.abspath(path_html_file))


#Fonction qui autorise l'utilisateur à cocher la case d'affichage de la carte après analyse ou non
def coche_calcul_carte():
    if valeur_case_calcul_carte.get()==False:
        case_affichage_carte['state']='disabled'
        valeur_case_affichage_carte.set(False)
    else:
        case_affichage_carte['state']='normal'


#Fonction permettant d'ajouter les menus déroulants supplémentaires pour l'analyse de croisement de maladie ou de les enlever
def ajout_retrait_ligne():   
    if MyGlobals.deroulant2.winfo_ismapped() and MyGlobals.deroulant_dates.winfo_ismapped():
        MyGlobals.deroulant2.grid_forget()
        MyGlobals.deroulant_dates.grid_forget()
        bouton_ajout_ligne['text']='+'
    else:
        MyGlobals.deroulant2.grid(row=1,column=0,pady =10)
        MyGlobals.deroulant_dates.grid(row=2,column=0,pady=5)
        bouton_ajout_ligne['text']='-'


#Fonction qui met en place toute la fenêtre du programme
# On créé notre fenêtre
window = Tk()
window.title("Medical Data Analyser")
window.geometry("850x500")
window.iconbitmap("logo-pharmacie-médical.ico")
window.minsize(480, 360)
window.resizable(False, False)
canvas = Canvas(window,width = 1920, height = 1920, bg = 'blue')
canvas.pack(expand = YES, fill = BOTH)
image = ImageTk.PhotoImage(file = os.path.abspath("background.jpg"))
canvas.create_image(0, 0, image = image, anchor = NW)

#On créé des onglets menus etc
menus = Menu(window)
menuFichier = Menu(menus)
menuEdition = Menu(menus)
menuOutils = Menu(menus)
menuHelp = Menu(menus)
menus.add_cascade(label="Fichiers",menu=menuFichier)
menus.add_cascade(label="Cartes",menu=menuEdition)
menus.add_cascade(label="Outils",menu=menuOutils)
menus.add_cascade(label="Help",menu=menuHelp)
menuFichier.add_command(label = "Nouveau")
menuFichier.add_command(label = "Ouvrir",command = ouverture_fichier_de_base)
menuFichier.add_command(label = "Paramètres",command = menuParametre)
menuFichier.add_command(label = "Quitter",command = quit)
menuEdition.add_command(label = "Ouvrir",command = ouvrir_carte)

# On ajoute une frame
fr = Frame(canvas, bd='2', relief=SOLID)
fr.place(x=10,y=10)
fr2 = Frame(fr, bd='2', relief=SOLID)
fr.grid(row=0,column=0,sticky=W,padx=20, pady=20)

MyGlobals.deroulant = ttk.Combobox(fr, values = MyGlobals.myCSV , font = ("Arial",10), width = 110)
MyGlobals.deroulant['state']='disabled'
MyGlobals.deroulant.grid(row=0,column=0,pady =10)

MyGlobals.deroulant2 = ttk.Combobox(fr, values = MyGlobals.myCSV , font = ("Arial",10), width = 110)
MyGlobals.deroulant2['state']='disabled'

MyGlobals.deroulant_dates = ttk.Combobox(fr, values = MyGlobals.mesDates , font = ("Arial",10), width = 30)
MyGlobals.deroulant_dates['state']='disabled'

bouton_ajout_ligne= Button(fr, text="+",command = ajout_retrait_ligne)
bouton_ajout_ligne.grid(row=0,column=1,pady = 10)

fr2.grid(row=3,column=0,sticky=E+W)

bouton_analyse = Button(fr, text="Lancer l'analyse", font=("Arial", 30), bg='white', fg='#000000', command = sauvegarde)
bouton_analyse['state'] = 'disabled'
bouton_analyse.grid(row=4,column=0,pady =10)

progressbar=ttk.Progressbar(fr,orient="horizontal",length=300,mode="determinate")
progressbar.grid(row=5,column=0,pady =10)

progressbar_title=Label(fr, text="")
progressbar_title.grid(row=6,column=0,pady = 10)

valeur_case_affichage_carte = BooleanVar()
valeur_case_graph_sexe = BooleanVar()
valeur_case_graph_annee = BooleanVar()
valeur_case_calcul_carte = BooleanVar()

case_calcul_carte = Checkbutton(fr2,text="Créer la carte",font=("Arial", 15), fg='#000000', variable=valeur_case_calcul_carte, command=coche_calcul_carte)
case_calcul_carte.grid(row=0,column=0,pady = 10,sticky=W)
case_affichage_carte = Checkbutton(fr2,text="Ouvrir la carte après exécution", font=("Arial", 15), fg='#000000', variable=valeur_case_affichage_carte)
case_affichage_carte.grid(row=0,column=1,padx=80,pady =10,sticky=W)
case_affichage_carte['state']='disabled'

case_graph_sexe = Checkbutton(fr2,text="Répartition selon le sexe",font=("Arial", 15), fg='#000000', variable=valeur_case_graph_sexe)
case_graph_sexe.grid(row=1,column=0,pady =10,sticky=W)
case_graph_annee = Checkbutton(fr2,text="Répartion sur l'année",font=("Arial", 15), fg='#000000', variable=valeur_case_graph_annee)
case_graph_annee.grid(row=1,column=1,padx=80,pady=10,sticky=W)

# Puis on l'affiche
window.config(menu = menus)
window.mainloop()
