import matplotlib.pyplot as plt
import csv
import os
from datetime import datetime, timedelta #la manipulation des dates
from collections import Counter

def camembert(livres):
  genres={}
  for livre in livres:
    if livre.genre in genres:
      genres[livre.genre]+=1
    else:
      genres[livre.genre]=1
      
  labels =list(genres.keys())#noms des genres
  valeurs=list(genres.values())#la valeur de chauqe livre pour chaque genre
        
#dessin camembert 
  plt.pie(valeurs,labels=labels)
  plt.title("Repartition des livres par genre")
  plt.axis("equal")
#sauvegarder
  os.makedirs(os.path.join(os.path.dirname(__file__), "..", "assets"), exist_ok=True)
  chemin = os.path.join(os.path.dirname(__file__), "..", "assets", "stats_genres.png")
  plt.savefig(chemin)
  plt.show()
def top_auteurs(livres):
  auteurs={}
  for livre in livres:
    if livre.auteur in auteurs:
      auteurs[livre.auteur] +=1
    else:
      auteurs[livre.auteur]=1
      
  auteurs_tries=sorted(auteurs.items(),key=lambda x: x[1],reverse=True)
  top_10=auteurs_tries[:10]

  noms=[auteur for auteur,_ in top_10] 
  valeurs=[nb for _,nb in top_10]

#dessin histogramme
  plt.figure(figsize=(10, 6))
  plt.bar(noms, valeurs, color='skyblue')
  plt.xticks(rotation=45, ha="right")
  plt.title("Top 10 des auteurs les plus présents")
  plt.xlabel("Auteurs")
  plt.ylabel("Nombre de livres")
  plt.tight_layout()
  chemin_dossier = os.path.join(os.path.dirname(__file__), "..", "assets")
  os.makedirs(chemin_dossier, exist_ok=True)
  chemin_complet = os.path.join(chemin_dossier, "stats_auteurs.png")
  plt.savefig(chemin_complet)
  plt.show()

def courbe_emprunts(filename="../data/historique.csv"):  
  emprunts_par_jour=Counter()#un compteur des emprunts par jouur

  try:
    with open(filename,"r") as f :
      lecteur=csv.reader(f,delimiter=";")
      for ligne in lecteur:
        date_str,ISBN , id, action = ligne#une ligne contient ces 4 partie separé par ;
        if action=="emprunt":
          date_obj = datetime.strptime(date_str,"%Y-%m-%d").date()#transforme en vrr date python
          emprunts_par_jour[date_obj]+=1#on incremente pour ce jour laa
  except FileNotFoundError:
    print("le fichier historique.csv est introuvable")           
  aujourd_hui = datetime.now().date()
  jours = [aujourd_hui - timedelta(days=i) for i in range(29, -1, -1)]  # J-29 à aujourd’hui cadd 30 jours
  jours_str = [j.strftime("%Y-%m-%d") for j in jours]#list des dates sous forme de txt
  valeurs = [emprunts_par_jour.get(j, 0) for j in jours]#combien demprunts pour chaque jouur

#la courbeee
  plt.figure(figsize=(10, 5))
  plt.plot(jours_str, valeurs, marker='o', linestyle='-', color='green')
  plt.xticks(rotation=45)
  plt.title("Activité des emprunts - 30 derniers jours")
  plt.xlabel("Date")
  plt.ylabel("Nombre d'emprunts")
  plt.tight_layout()
  chemin_dossier = os.path.join(os.path.dirname(__file__), "..", "assets")
  os.makedirs(chemin_dossier, exist_ok=True)
  chemin_complet = os.path.join(chemin_dossier, "stats_emprunts.png")
  plt.savefig(chemin_complet)
  plt.show()
def afficher_toutes_les_stats(livres):
    camembert(livres)
    top_auteurs(livres)
    courbe_emprunts()
  