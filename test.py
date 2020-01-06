from tkinter import *
from tkinter import filedialog
import webbrowser
import csv


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
    return ma_liste_de_medoc

def cases():
    case_a_cocher.flash()

def ouverture_fichier_de_base():
    window.fileName = filedialog.askopenfilename(filetype =(("PDF file","*.pdf"),("HTML files","*.html"),("CSV files","*.csv")))
    with open(window.fileName, newline = '') as csvfile :
        readerMan = csv.reader(csvfile, delimiter=';',quotechar='|')
        myCSV = []
        for row in readerMan :
            if test_de_presence(myCSV,row[-1]) == 1  or len(myCSV) ==0 :
                myCSV.append(row[-1])
    print(myCSV[0])
    print(myCSV[1])
    print(window.fileName)
    for i in myCSV :
        print(i)
    print("la taille = ",len(myCSV))
    a = 'PREPARATIONS THYROIDIENNES'
    if(a == myCSV[1]) :
        print('ok')
    return(window.fileName)

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
window.title("On va gérer lol")
window.geometry("1280x720")
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
bouton_de_sauvegarde.pack(pady=25, fill=X)

case_a_cocher = Checkbutton(fr,text="Inclure ceci ?",font=("Arial", 15), bg='white', fg='#DD1616',command=cases)
case_a_cocher.pack()

# Puis on l'affiche
window.config(menu = menus)
window.mainloop()
