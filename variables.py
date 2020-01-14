import queue

class MyGlobals():pass
MyGlobals.queue1 = queue.Queue()
MyGlobals.fileHeader=['Ben_Unique_TI','Cli_sexe','Cli_TI','Ben_TI','nom_voie','nom_commune','lon','lat','nom','EAN13','Date_order','L_ATC3'] #Liste des noms des colonnes du fichier csv placé en entrée
MyGlobals.myCSV = [] #Va contenir le chemin vers le csv d'entrée
MyGlobals.lieu_actuel = ["Liévin",[50.4218,2.7876]] #Lieu sur lequel la carte sera centrée à l'ouverture
MyGlobals.liste_villes = [("Liévin",1,[50.4218,2.7876]),("Lille",2,[50.6333,3.0667])] #Liste des lieux où on peut centrer la carte
MyGlobals.mesDates = [] #Va contenir les différentes années présentes dans le csv d'entrée
