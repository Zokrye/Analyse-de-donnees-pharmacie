from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import webbrowser
import csv
import folium
from folium import plugins
import os
import matplotlib.pyplot as plt
from PIL import ImageTk
from all_years_curves_one_atc import show_graph_atc3
from histo_between_two_atc import show_histo_between_atc,get_day_month_year
import threading

class MyGlobals():pass

MyGlobals.fileHeader=['Ben_Unique_TI','Cli_sexe','Cli_TI','Ben_TI','nom_voie','nom_commune','lon','lat','nom','EAN13','Date_order','L_ATC3']
MyGlobals.myCSV = []
MyGlobals.lieu_actuel = ["Liévin",[50.4218,2.7876]]
MyGlobals.liste_villes = [("Liévin",1,[50.4218,2.7876]),("Lille",2,[50.6333,3.0667])]
MyGlobals.mesDates = []

def popupmsg(msg):
    popup = Toplevel()
    popup.iconbitmap("logo-pharmacie-médical.ico")
    popup.title("Attention")
    label = Label(popup, text=msg) #Can add a font arg here
    label.pack(side="top", fill="x", pady=10)
    B1 = Button(popup, text="OK", command = popup.destroy)
    B1.pack()
    #popup.wait_window()
    return

def internet():
    webbrowser.open_new("http://www.jeuxvideo.com/forums/1-51-44890961-1-0-1-0-j-ai-chie-dans-un-saladier-a-auchan.htm")

def sauvegarde():
    a2 = MyGlobals.deroulant.get()
    if a2 !='':
        filename=formatToFileName(a2)
        print(a2)
        chemin_carte =os.path.abspath("Cartes/"+filename)
        if not os.path.exists(os.path.abspath("Cartes/")):
            os.makedirs(os.path.abspath("Cartes/"))
        print(chemin_carte)
        thr2 = threading.Thread(target=performAnalysis, args=(a2,chemin_carte), kwargs={})
        thr2.start() 
    else:
        popupmsg("Veuillez sélectionner une catégorie de médicaments avant de lancer l'analyse")
    return

def performAnalysis(a2,chemin_carte):
    nb_operations=valeur_case_graph_annee.get()+valeur_case_graph_sexe.get()+valeur_case_calcul_carte.get()

    if valeur_case_calcul_carte.get():
        progressbar_title["text"]='Création de la carte en cours'
        carto(a2,MyGlobals.chemin,chemin_carte)
        progressbar["value"]+=100/nb_operations
    if valeur_case_graph_sexe.get():
        progressbar_title["text"]='Creation du graph \"Répartition selon le sexe\" en cours'
        graph_sexe(a2,MyGlobals.chemin)
        progressbar["value"]+=100/nb_operations
    if valeur_case_graph_annee.get() :
        progressbar_title["text"]='Creation du graph \"Année\" en cours'
        show_graph_atc3(a2,MyGlobals.chemin)
        progressbar["value"]+=100/nb_operations
    if bouton_ajout_ligne['text']=='-' and MyGlobals.deroulant2.get() != '' and MyGlobals.deroulant_dates.get() != '':
        nb_operations= nb_operations+1
        progressbar_title["text"]='Creation du graph \"Croisement\" en cours'
        show_histo_between_atc(a2,MyGlobals.deroulant2.get(),MyGlobals.deroulant_dates.get(),MyGlobals.chemin)
        progressbar["value"]+=100/nb_operations
    progressbar["value"]=0
    progressbar_title["text"]=''
    plt.show()

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

def cases():
    print("coché")
    #case_a_cocher.flash()

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

def getAllATCCodes(fileName):
    #progressbar.pack(side=TOP)
    progressbar_title['text']='Chargement du fichier en cours'
    #progressbar_title.pack(expand=YES)
    progressbar['mode']='indeterminate'
    #progressbar.pack_forget()
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
    print(MyGlobals.myCSV[0])
    print(MyGlobals.myCSV[1])
    print(window.fileName)
    MyGlobals.mesDates.sort()
    MyGlobals.myCSV.sort()
    for i in MyGlobals.myCSV :
        print(i)
    print("la taille = ",len(MyGlobals.myCSV))
    a = 'PREPARATIONS THYROIDIENNES'
    MyGlobals.deroulant['values']=MyGlobals.myCSV
    MyGlobals.deroulant['state'] = 'readonly'
    MyGlobals.deroulant2['values']=MyGlobals.myCSV
    MyGlobals.deroulant2['state'] = 'readonly'
    MyGlobals.deroulant_dates['values'] = MyGlobals.mesDates
    MyGlobals.deroulant_dates['state'] = 'readonly'
    bouton_analyse['state'] = 'normal'
    if(a == MyGlobals.myCSV[1]) :
        print('ok')
    progressbar_title['text']=''
    #progressbar_title.pack_forget()
    progressbar.stop()
    progressbar['mode']='determinate'
    #progressbar.pack_forget()

def test_de_presence(maListe,monSujet):
    x = 1
    if len(maListe) != 0 :
        for i in maListe:
            if i == monSujet:
                x = 0
    return x

def showCity():
    print(MyGlobals.choix_ville.get())

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

def choix_lieu():
    MyGlobals.lieu_actuel = [MyGlobals.liste_villes[MyGlobals.choix_ville.get()][0],[MyGlobals.liste_villes[MyGlobals.choix_ville.get()][2][0],MyGlobals.liste_villes[MyGlobals.choix_ville.get()][2][1]]]
    print("Vous avez choisi ",MyGlobals.lieu_actuel[0]," avec comme coordonnées ",MyGlobals.lieu_actuel[1])


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
        plt.close()
        plt.pie(sizes, labels=labels, colors=colors, 
                autopct='%1.1f%%', shadow=True, startangle=90)
        plt.axis('equal')
        if not os.path.exists(os.path.abspath("Diagrammes\Sexes")): 
            os.makedirs(os.path.abspath("Diagrammes\Sexes"))
        plt.savefig(os.path.abspath('Diagrammes\Sexes\\'+name_atc+'.png'))
        plt.show(block=False)
    return  

def sauve_annee(fig,name_atc):
    if 1==1 :
        if not os.path.exists(os.path.abspath("Diagrammes\Année")):
            os.makedirs(os.path.abspath("Diagrammes\Année"))
        plt.savefig(os.path.abspath('Diagrammes\Année\\'+name_atc+'.png'))

def carto(name_atc,path_data_file,path_html_file):
    list = []
    list = get_EAN13(name_atc,path_data_file)
    m = folium.Map(MyGlobals.lieu_actuel[1], zoom_start=14)
    m.add_child(plugins.HeatMap(list, radius=30,gradient={0: 'yellow', 0.7: 'orange', 1: 'red'}))
    if not ".html" in path_html_file:
        path_html_file+=".html"

    m.save(path_html_file)
    if valeur_case_affichage_carte.get()==1:
        print(os.path.abspath(path_html_file))
        webbrowser.open_new_tab(os.path.abspath(path_html_file))
    print("c'est fini")



# On créé notre fenêtre
window = Tk()
window.title("Becquet Analisys")
window.geometry("850x500")
window.iconbitmap("logo-pharmacie-médical.ico")
window.minsize(480, 360)
window.resizable(False, False)
#window.config(background='#DD1616')

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
# on met qqs éléments
#lab_titre = Label(fr, text="Un Deux Un Deux", font=("Arial", 50), bg='#DD1616', fg='white')
#lab_titre.pack(expand=YES)
#
#lab_titre2 = Label(fr, text="Bienvenue à tous", font=("Arial", 30), bg='#DD1616', fg='white')
#lab_titre2.pack(expand=YES)


fr.grid(row=0,column=0,sticky=W,padx=20, pady=20)


#fr.grid(row=0, column=0)


def coche_calcul_carte():
    if valeur_case_calcul_carte.get()==False:
        case_affichage_carte['state']='disabled'
        valeur_case_affichage_carte.set(False)
    else:
        case_affichage_carte['state']='normal'


def ajout_retrait_ligne():   
    if MyGlobals.deroulant2.winfo_ismapped() and MyGlobals.deroulant_dates.winfo_ismapped():
        MyGlobals.deroulant2.grid_forget()
        MyGlobals.deroulant_dates.grid_forget()
        bouton_ajout_ligne['text']='+'
    else:
        MyGlobals.deroulant2.grid(row=1,column=0,pady =10)
        MyGlobals.deroulant_dates.grid(row=2,column=0,pady=5)
        bouton_ajout_ligne['text']='-'

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
