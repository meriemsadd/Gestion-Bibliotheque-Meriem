from bibliotheque import Bibliotheque, Livre, Membre
from exceptions import *
from exceptions import LivreInexistantError, MembreInexistantError, LivreIndisponibleError, QuotaEmpruntDepasseError
import os
print("Dossier courant:", os.getcwd())

import sys
sys.path.append("..")


def afficher_menu():
    print("\n=== GESTION BIBLIOTHÈQUE ===")
    print("1. Ajouter un livre")
    print("2. Inscrire un membre")
    print("3. Emprunter un livre")
    print("4. Rendre un livre")
    print("5. Lister tous les livres")
    print("6.Afficher les statistiques")
    print("7.Sauvegarder et quitter")

def main():
    biblio = Bibliotheque()
    biblio.charger_livre()
    biblio.charger_membre()

    while True:
        afficher_menu()
        choix = input("Choisissez une option : ")

        if choix == "1":
            isbn = input("ISBN : ")
            try:
                biblio.chercher_livre(isbn)
                print("⚠️ Ce livre existe déjà.")
                continue
            except LivreInexistantError:
                pass
            titre = input("Titre : ")
            auteur = input("Auteur : ")
            annee = input("Année : ")
            genre = input("Genre : ")
            livre = Livre(isbn, titre, auteur, annee, genre)
            biblio.ajouter_livre(livre)
            print("Livre ajouté avec succes")

        elif choix == "2":
            while True:
                id = input("ID Membre : ")
                try:
                    biblio.chercher_membre(id)
                    print(f"ce id {id} existe deja, veuiller choisir un autre")
                except MembreInexistantError: 
                
                nom = input("Nom : ")
                membre = Membre(id, nom)
                biblio.enregistrer_membre(membre)
                biblio.sauvegarder_membres()  
                print("Membre inscrit avec succes")

        elif choix == "3":
            isbn = input("ISBN du livre : ")
            id = input("ID du membre : ")
            try:
                biblio.emprunter(isbn, id)
                biblio.enregistrer_historique(isbn, id, "emprunt")
                print("Livre emprunté avec succes")
            except Exception as e:
                print("error", e)

        elif choix == "4":
            isbn = input("ISBN du livre : ")
            id = input("ID du membre : ")
            try:
                biblio.retourner(isbn, id)
                biblio.enregistrer_historique(isbn, id, "retour")
                print("Livre retourné avec succes")
            except Exception as e:
                print("error", e)

        elif choix == "5":
            for livre in biblio.liste_livres:
                print(livre)

        elif choix == "7":
            biblio.sauvegarder_donnees()
            print("Données sauvegardées.Bonne journée !")
            break
        elif choix == "6":
            from visualisations import afficher_toutes_les_stats
            afficher_toutes_les_stats(biblio.liste_livres)
        else:
            print("Choix invalide.")

if __name__ == "__main__":
    main()
