import os
from datetime import datetime
import csv
from exceptions import LivreInexistantError, MembreInexistantError, LivreIndisponibleError, QuotaEmpruntDepasseError
CHEMIN_DATA = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))

class Livre:
  def __init__(self,ISBN,titre,auteur,annee,genre,statut="disponible"):

    self.ISBN=ISBN
    self.titre=titre
    self.auteur=auteur
    self.annee=annee
    self.genre=genre
    self.statut=statut

  def __str__(self):
     return f"Livre: {self.titre} (ISBN: {self.ISBN}) par {self.auteur} - Statut: {self.statut}"
   
class Membre:
  def __init__(self,id,nom):
    self.id=id
    self.nom=nom
    self.livres_empruntes=[]
  def emprunter(self, livre):
    self.livres_empruntes.append(livre.ISBN)

  def retourner(self, ISBN):
    if ISBN in self.livres_empruntes:
        self.livres_empruntes.remove(ISBN)

  def __str__(self):
        return f"Membre {self.id}: {self.nom} - Livres empruntés: {', '.join(self.livres_empruntes)}"

class Bibliotheque:

  def __init__(self):
    self.liste_livres=[]
    self.liste_membres=[]

  def ajouter_livre(self,livre):
    self.liste_livres.append(livre)#self ici definition de la liste localement 

  def supprimer_livre(self, isbn):
    isbn = str(isbn).strip()
    initial = len(self.liste_livres)
    self.liste_livres = [livre for livre in self.liste_livres if str(livre.ISBN).strip() != isbn]
    if len(self.liste_livres) == initial:
        raise Exception(f"Livre avec ISBN {isbn} non trouvé.")
    print(f"Livre avec ISBN {isbn} supprimé.")

  def enregistrer_membre(self,membre):  
    for m in self.liste_membres:
        if m.id == membre.id:
            print(f" Le membre avec ID {membre.id} existe déjà.")
            return
    self.liste_membres.append(membre)
    
  def supprimer_membre(self, id_membre):
    id_membre = str(id_membre).strip()
    initial = len(self.liste_membres)
    self.liste_membres = [membre for membre in self.liste_membres if str(membre.id).strip() != id_membre]
    if len(self.liste_membres) == initial:
        raise Exception(f"Membre avec ID {id_membre} non trouvé.")
    print(f"Membre avec ID {id_membre} supprimé.")


  #on a besoin de methode chercher livre
  def chercher_livre(self,ISBN):
    ISBN= str(ISBN).strip()
    for livre in self.liste_livres:
        if str(livre.ISBN).strip() == ISBN :
           return livre
    raise LivreInexistantError(f"livre introuvable.")  
   #on a besoin de methode chercher membre
  def chercher_membre(self,id):
    id=str(id).strip()
    for membre in self.liste_membres:#si le livre existe dans la liste des livres
      if membre.id == id :
        return membre
    raise MembreInexistantError(f"membre introuvable.")  

  def emprunter(self,ISBN,id):
    livre=self.chercher_livre(ISBN)
    membre=self.chercher_membre(id)
    if livre.statut !="disponible":#deja emprunté
      raise LivreIndisponibleError(f"Le livre '{livre.titre}' n'est pas disponible pour le moment.")
     
    if len(membre.livres_empruntes) >=3:
      raise QuotaEmpruntDepasseError("quota de 3 livres deja atteint")  
    livre.statut="emprunté"
    membre.emprunter(livre)
     
  def retourner(self,ISBN,id):   
     livre=self.chercher_livre(ISBN)
     membre=self.chercher_membre(id)
     livre.statut="disponible"#apres returne ywli dispo
     membre.retourner(ISBN)

  def sauvegarder_donnees(self):
     self.sauvegarder_livres()
     self.sauvegarder_membres()
     print("Données sauvegardées avec succès.")

# Charge les livres depuis data/livres.txt
  def charger_livre(self, filename=os.path.join(CHEMIN_DATA, "livres.txt")):
    try:
        with open(filename, "r", encoding="utf-8") as f:#ouvrir mode lecture 
            for ligne in f:
                isbn, titre, auteur, annee, genre, statut = ligne.strip().split(";")#enlève les espaces et coupe la ligne en plusieurs morceaux séparés par ;
                livre = Livre(isbn, titre, auteur, annee, genre, statut)
                self.liste_livres.append(livre)
    except FileNotFoundError:
        print("⚠️ Fichier livres.txt introuvable.")

# Charge les membres depuis data/membres.txt
  def charger_membre(self, filename=os.path.join(CHEMIN_DATA, "membres.txt")):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for ligne in f:
                parties = ligne.strip().split(";")
                if len(parties) == 3:
                    id, nom, empruntes = parties
                    membre = Membre(id, nom)
                    if empruntes:
                        membre.livres_empruntes = empruntes.split(",")
                    self.liste_membres.append(membre)
                else:
                    print(f"⚠️ Ligne ignorée dans membres.txt (format invalide) : {ligne.strip()}")
    except FileNotFoundError:
        print("⚠️ Fichier membres.txt introuvable.")


  def sauvegarder_livres(self, filename=os.path.join(CHEMIN_DATA, "livres.txt")):
    with open(filename, "w", encoding="utf-8") as f:
        for livre in self.liste_livres:
            ligne = f"{livre.ISBN};{livre.titre};{livre.auteur};{livre.annee};{livre.genre};{livre.statut}\n"
            f.write(ligne)#pour ecrire cette ligne dans le fichier

  def sauvegarder_membres(self, filename=os.path.join(CHEMIN_DATA, "membres.txt")):
    with open(filename, "w", encoding="utf-8") as f:
        for membre in self.liste_membres:
            empruntes = ",".join(membre.livres_empruntes)
            ligne = f"{membre.id};{membre.nom};{empruntes}\n"
            f.write(ligne)

  def enregistrer_historique(self, ISBN, id, action, filename=os.path.join(CHEMIN_DATA, "historique.csv")):
    with open(filename, "a", newline="", encoding="utf-8") as f:#a pour ajouter a la fin du fichier sans ecraser
        writer = csv.writer(f, delimiter=";")
        writer.writerow([datetime.now().date(), ISBN, id, action])#date daujourdui

    
