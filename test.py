from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import webbrowser
import csv


class MyGlobals():pass
def popupmsg(msg):
    popup = Toplevel()
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
    print(a2)
    return ma_liste_de_medoc

def cases():
    case_a_cocher.flash()

def ouverture_fichier_de_base():
    window.fileName = filedialog.askopenfilename(filetype =(("CSV files","*.csv"),("PDF file","*.pdf"),("HTML files","*.html")))
    MyGlobals.myCSV = []
    if window.fileName!='':
        with open(window.fileName, newline = '') as csvfile :
            header=next(csvfile) #saute lapremière ligne (header)
            if header!='nom_voie;nom_commune;lon;lat;nom;EAN13;Date_order;L_ATC3\r\n':
                popupmsg('Le fichier selectionné est incorrect ou corrumpu')
                return
            readerMan = csv.reader(csvfile, delimiter=';',quotechar='|')        
            for row in readerMan :
                if test_de_presence(MyGlobals.myCSV,row[-1]) == 1  or len(MyGlobals.myCSV) ==0 :
                    MyGlobals.myCSV.append(row[-1])
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

def ouvrir_carte():
    window.fileName = filedialog.askopenfilename(filetype =(("HTML files","*.html"),))
    webbrowser.open_new(window.fileName)
    return(window.fileName)

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
menuFichier.add_command(label = "Enregistrer")
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

MyGlobals.myCSV = []
MyGlobals.deroulant = ttk.Combobox(window, values = MyGlobals.myCSV , font = ("Arial",10), width = 110)
MyGlobals.deroulant['state']='disabled'
MyGlobals.deroulant.pack(expand = YES)

# Puis on l'affiche
window.config(menu = menus)
window.mainloop()
