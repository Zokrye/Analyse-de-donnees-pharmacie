from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import webbrowser
import csv
import folium
from folium import plugins
import os
import matplotlib.pyplot as plt


class MyGlobals():pass

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
    ma_liste_de_medoc = []
    md1 = medoc_name.get()
    md2 = medoc2_name.get()
    ma_liste_de_medoc.append(md1)
    ma_liste_de_medoc.append(md2)
    print(ma_liste_de_medoc)
    print(ma_liste_de_medoc[0],ma_liste_de_medoc[1])
    a2 = MyGlobals.deroulant.get()
    filename=formatToFileName(a2)
    print(a2)
    chem =os.path.abspath("Cartes/"+filename)
    if not os.path.exists(os.path.abspath("Cartes/")):
        os.makedirs(os.path.abspath("Cartes/"))
    print(chem)
    graph_sexe(a2,MyGlobals.chemin)
    carto(a2,MyGlobals.chemin,chem)
    plt.show()
    return ma_liste_de_medoc

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
        with open(window.fileName, newline = '') as csvfile :
            readerMan = csv.DictReader(csvfile, delimiter=';',quotechar='|')
            header=readerMan.fieldnames
            if header != MyGlobals.fileHeader:
                MyGlobals.deroulant.set('')
                MyGlobals.deroulant['values'] = []
                MyGlobals.deroulant['state'] = 'disabled'
                bouton_de_sauvegarde['state'] = 'disabled'
                popupmsg('Le fichier selectionné est incorrect ou corrumpu')               
                return
            for row in readerMan :
                if test_de_presence(MyGlobals.myCSV,row["L_ATC3"]) == 1  or len(MyGlobals.myCSV) ==0 :
                    MyGlobals.myCSV.append(row["L_ATC3"])
        print(MyGlobals.myCSV[0])
        print(MyGlobals.myCSV[1])
        print(window.fileName)
        MyGlobals.myCSV.sort()
        for i in MyGlobals.myCSV :
            print(i)
        print("la taille = ",len(MyGlobals.myCSV))
        a = 'PREPARATIONS THYROIDIENNES'
        MyGlobals.deroulant['values']=MyGlobals.myCSV
        MyGlobals.deroulant['state'] = 'readonly'
        bouton_de_sauvegarde['state'] = 'normal'
        if(a == MyGlobals.myCSV[1]) :
            print('ok')
    else:
        MyGlobals.deroulant.set('')
        MyGlobals.deroulant['values'] = []
        MyGlobals.deroulant['state'] = 'disabled'
        bouton_de_sauvegarde['state'] = 'disabled'
    return([window.fileName,MyGlobals.myCSV])

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
    MyGlobals.liste_villes = [("Liévin",1,[50.4218,2.7876]),("Lille",2,[52.4218,3.7876])]
    MyGlobals.choix_ville = IntVar()
    MyGlobals.choix_ville.set(0)
    for val,ville in enumerate(MyGlobals.liste_villes):
        if ville[0] == "Liévin" :
            MyGlobals.choix_ville.set(1)
        else :
            MyGlobals.choix_ville.set(0)
        Radiobutton(para,text = ville[0],padx = 20, variable = MyGlobals.choix_ville,value = val,command = choix_lieu).pack()
    B1 = Button(para, text="OK", command = para.destroy)
    B1.pack()
    para.mainloop()

def choix_lieu():
    print("Vous avez choisi ",MyGlobals.liste_villes[MyGlobals.choix_ville.get()][0]," avec comme coordonnées [",MyGlobals.liste_villes[MyGlobals.choix_ville.get()][2][0],",",MyGlobals.liste_villes[MyGlobals.choix_ville.get()][2][1],"]")


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

def carto(name_atc,path_data_file,path_html_file):
    list = []
    list = get_EAN13(name_atc,path_data_file)
    m = folium.Map([50.4218,2.7876], zoom_start=14)


    m.add_child(plugins.HeatMap(list, radius=30,gradient={0: 'yellow', 0.7: 'orange', 1: 'red'}))
    if not ".html" in path_html_file:
        path_html_file+=".html"

    m.save(path_html_file)
    if valeur_case.get()==1:
        print(os.path.abspath(path_html_file))
        webbrowser.open_new_tab(os.path.abspath(path_html_file))
    print("c'est fini")

# On créé notre fenêtre
window = Tk()
window.title("Becquet Analisys")
window.geometry("1280x720")
window.iconbitmap("logo-pharmacie-médical.ico")
window.minsize(480, 360)
window.config(background='#DD1616')



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
fr = Frame(window, bg='#DD1616', bd='2', relief=SOLID)
fr2 = Frame(fr, bg='#DD1616',bd='2',relief=SOLID)
fr3 = Frame(fr, bg='#DD1616',bd='2',relief=SOLID)

# on met qqs éléments
lab_titre = Label(fr, text="Un Deux Un Deux", font=("Arial", 50), bg='#DD1616', fg='white')
lab_titre.pack(expand=YES)

lab_titre2 = Label(fr, text="Bienvenue à tous", font=("Arial", 30), bg='#DD1616', fg='white')
lab_titre2.pack(expand=YES)

medoc_name = Entry(fr2, font=("Arial", 50), bg='#DD1616', fg='white')
medoc_name.pack(expand=YES)

medoc2_name = Entry(fr2,  font=("Arial", 50), bg='#DD1616', fg='white')
medoc2_name.pack(expand=YES)

fr.pack(expand=YES)
fr2.pack(expand=YES)
#fr.grid(row=0, column=0)
#fr2.grid(row=0, column=1)

# Boutons et autres
bou = Button(fr, text="Aller voir le saladier du Auchan", font=("Arial", 30), bg='white', fg='#DD1616', command = internet)
bou.pack(pady=25, fill=X)

bouton_de_sauvegarde = Button(fr, text="Sauvegarder ma saisie", font=("Arial", 30), bg='white', fg='#DD1616', command = sauvegarde)
bouton_de_sauvegarde['state'] = 'disabled'
bouton_de_sauvegarde.pack(pady=25, fill=X)

valeur_case = BooleanVar()
case_a_cocher = Checkbutton(fr,text="Ouvrir la carte après exécution",font=("Arial", 15), bg='white', fg='#DD1616',command=cases, variable=valeur_case)
case_a_cocher.pack()


MyGlobals.fileHeader=['Ben_Unique_TI','Cli_sexe','Cli_TI','Ben_TI','nom_voie','nom_commune','lon','lat','nom','EAN13','Date_order','L_ATC3']
MyGlobals.myCSV = []
MyGlobals.deroulant = ttk.Combobox(window, values = MyGlobals.myCSV , font = ("Arial",10), width = 110)
MyGlobals.deroulant['state']='disabled'
MyGlobals.deroulant.pack(expand = YES)

# Puis on l'affiche
window.config(menu = menus)
window.mainloop()
