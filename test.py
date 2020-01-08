from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import webbrowser
import csv
import folium
from folium import plugins



class MyGlobals():pass

def popupmsg(msg):
    popup = Toplevel()
    popup.iconbitmap("logo-pharmacie-médical.ico")
    popup.title("Attention")
    label = Label(popup, text=msg) #Can add a font arg here
    label.pack(side="top", fill="x", pady=10)
    B1 = Button(popup, text="OK", command = popup.destroy)
    B1.pack()
    popup.mainloop()

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
    chem = "Cartes/"+filename
    print(chem)
    carto(a2,MyGlobals.chemin,chem)
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
    case_a_cocher.flash()

def ouverture_fichier_de_base():
    window.fileName = filedialog.askopenfilename(filetype =(("CSV files","*.csv"),("PDF file","*.pdf"),("HTML files","*.html")))
    MyGlobals.chemin = window.fileName
    MyGlobals.myCSV = []
    if window.fileName!='':
        with open(window.fileName, newline = '') as csvfile :
            readerMan = csv.DictReader(csvfile, delimiter=';',quotechar='|')
            header=readerMan.fieldnames
            if header != MyGlobals.fileHeader:
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
    return([window.fileName,MyGlobals.myCSV])

def test_de_presence(maListe,monSujet):
    x = 1
    if len(maListe) != 0 :
        for i in maListe:
            if i == monSujet:
                x = 0
    return x

def menuParametre():
    para = Toplevel()
    para.title("Paramètres")
    para.geometry("360x140")
    para.iconbitmap("logo-pharmacie-médical.ico")
    labelPara = Label(para) #Can add a font arg here
    labelPara.pack(side="top", fill="x", pady=10)
    MyGlobals.varLille = 0
    MyGlobals.varLievin = 1
    MyGlobals.lille = Checkbutton(para,text="Lille",font=("Arial", 15), bg='white', fg='#DD1616',command = choix_lieu, variable = MyGlobals.varLille)
    MyGlobals.lievin = Checkbutton(para,text="Liévin",font=("Arial", 15), bg='white', fg='#DD1616',command = choix_lieu2, variable = MyGlobals.varLievin)
    B1 = Button(para, text="OK", command = para.destroy)
    MyGlobals.lille.pack()
    MyGlobals.lievin.pack()
    B1.pack()
    para.mainloop()
    return

def choix_lieu():
    if MyGlobals.lievin.value == 1 :
        MyGlobals.lievin.toggle()

def choix_lieu2():
    if MyGlobals.lille.value == 1 :
        MyGlobals.lille.toggle()

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

def carto(name_atc,path_data_file,path_html_file):
    list = []
    list = get_EAN13(name_atc,path_data_file)
    m = folium.Map([50.4218,2.7876], zoom_start=14)


    m.add_child(plugins.HeatMap(list, radius=30,gradient={0: 'yellow', 0.7: 'orange', 1: 'red'}))
    if ".html" in path_html_file:
        m.save(path_html_file)
    else:
        m.save(path_html_file+".html")
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

case_a_cocher = Checkbutton(fr,text="Inclure ceci ?",font=("Arial", 15), bg='white', fg='#DD1616',command=cases)
case_a_cocher.pack()

MyGlobals.fileHeader=['genre','Cli_TI','Ben_TI','nom_voie','nom_commune','lon','lat','nom','EAN13','Date_order','L_ATC3']
MyGlobals.myCSV = []
MyGlobals.deroulant = ttk.Combobox(window, values = MyGlobals.myCSV , font = ("Arial",10), width = 110)
MyGlobals.deroulant['state']='disabled'
MyGlobals.deroulant.pack(expand = YES)

# Puis on l'affiche
window.config(menu = menus)
window.mainloop()