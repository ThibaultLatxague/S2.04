"""
Créateurs : 
 - Latxague Thibault TD2/TP4
 - Masson Rafael TD2/TP4
"""

import pyodbc  # import de la bibliotheque pyodbc pour faire des requetes sql en python
import matplotlib.pyplot as plt

# on connecte notre base de donnee ODBC
conn = pyodbc.connect('DSN=tlatxague')
cursor = conn.cursor()


#%% S2.04 -- Fonctions requetes

conn = pyodbc.connect('DSN=tlatxague')
cursor = conn.cursor()
tracesExec = False

#Requete 1
def r1():
    #Création de listes qui représenteront chacune une colonne de notre BD
    nomVille = []
    nbrHotes = []
    pop2021 = []
    comm = []
    propLogsPrincSec = []
    propHotesHabts = []
    
    nombreParam = input("Combien de villes cherchez-vous ? ") #On demande le nombre de villes pour l'exécution du programme
    for i in range(int(nombreParam)):
        nomVille.append(input("Quel est le nom de la ville ? : ")) #On ajoute la réponse dans la liste
        
        #La requete SQL
        SQLCommand = ("""
                      SELECT COUNT(L.host_id) AS nombreHosts,
                                              APB.Population_2021, APB.Commune, 
                                              (APB.Res_principales_2020/APB.Logements_2020)*100
                                              AS proportionLgtsPrincSec, 
                                              (COUNT(L.host_id)/APB.Population_2021)*100 
                                              AS proportionHotesHabitants FROM logements L
                    JOIN nodenot_bd.agglo_paysbasque APB ON APB.code_insee = L.logt_codeINSEE
                    WHERE APB.Commune = ?
                    GROUP BY APB.Commune, APB.Population_2021, proportionLgtsPrincSec
                    """)
    
    print("\n")
                    
    #On exécute la requête autant de fois qu'il y a de paramètres donnés par l'utilisateur
    for i in range(int(nombreParam)):
        param = (nomVille[i])
        cursor.execute(SQLCommand, param)
        
        #On ajoute les élements de réponse dans les listes correspondantes
        for row in cursor.fetchall(): 
            if tracesExec : print("Résultats de la requête : ", row)
            nombreHotes, population2021, commune, proportionLogementsPrincipauxSecondaires, proportionHotesHabitants = row
            nbrHotes.append(nombreHotes)
            pop2021.append(population2021)
            comm.append(commune)
            propLogsPrincSec.append(proportionLogementsPrincipauxSecondaires)
            propHotesHabts.append(proportionHotesHabitants)
    
    #Affichage des tableaux pour les traces d'exécution
    if tracesExec : print("Tableau du nombre d\'hotes : ", nbrHotes)
    if tracesExec : print("Tableau de la population en 2021 : ", pop2021)
    if tracesExec : print("Tableau du nom de la commune : ", comm)
    if tracesExec : print("Tableau de la proportion de logements secondaires avec les logements principaux : ", propLogsPrincSec)
    if tracesExec : print("Tableau de la proportion d\'hotes avec les habitants : ", propHotesHabts)
        
    #On génère notre graphique avec les listes comm et propHotesHabts
    plt.bar(comm, propHotesHabts)
    plt.xlabel("Villes")
    plt.ylabel("Pourcentage de logements secondaires")
    plt.title("Graphique des villes en fonction du pourcentage de logements secondaires")
    plt.ylim(0, max(propHotesHabts)+10)
    plt.show()

#○Requete 2
def r2():
    #Création de listes qui représenteront chacune une colonne de notre BD
    langueParlee = []
    pourcentageLangue = []

    #On demande à l'utilisateur le nm de l'unique ville
    nomVille = (input("Quel est le nom de la ville ? : ")) 
    
    #On demande à l'utilisateur le pourcentage minimal de pourcentage de la langue parlée
    pourcentageMinimal = (input("Quel est le pourcentage minimale de la langue parlée souhaité ? (nombre positif entier ou décimal) : ")) 
    
    #La requete SQL
    SQLCommand = ("""
                  SELECT R.langue_detectee, ROUND(COUNT(R.langue_detectee)/(SELECT COUNT(R.review_id) 
                                  FROM reviews R
                                  JOIN logements L on L.log_id = R.logement_id 
                                  JOIN nodenot_bd.agglo_paysbasque APB ON APB.code_insee =                                                              L.logt_codeINSEE
                                  WHERE APB.Commune = ?)*100,2) AS langueSurRevues 
                  FROM reviews R
                  JOIN logements L ON L.log_id = R.logement_id
                  JOIN nodenot_bd.agglo_paysbasque APB ON APB.code_insee = L.logt_codeINSEE
                  WHERE APB.Commune = ?
                  GROUP BY R.langue_detectee
                  ORDER BY langueSurRevues DESC""")
                  
    #On exécute la requête
    param = (nomVille, nomVille)
    cursor.execute(SQLCommand, param)

    #On ajoute les élements de réponse dans les listes correspondantes
    for row in cursor.fetchall(): 
        if tracesExec : print("Résultats de la requête : ", row)
        lang, prct = row
        langueParlee.append(lang)
        pourcentageLangue.append(prct)
    
    longueurLangues = len(langueParlee)
    print("\n")
    
    #On enlève les communes qui ont un pourcentage de langues parlées égal à pourcentageMinimal
    for i in range(len(langueParlee)):
        if pourcentageLangue[i] < float(pourcentageMinimal):
            valeurLimite = i
            if tracesExec : print("Valeur limite : ", valeurLimite)
            print("\n")
            break
        if tracesExec : print("Pourcentage de la langue parlée : ", pourcentageLangue[i])
        if tracesExec : print("Langue parlée : ", langueParlee[i])   
        
    #On supprime tous les éléments après la première langue qui atteint 0.1%
    for j in range(longueurLangues - valeurLimite):
        if tracesExec : print("Valeur qui va être supprimée (pourcentage) : ", pourcentageLangue[-1])
        if tracesExec : print("Valeur qui va être supprimée (langue) : ", langueParlee[-1])
        pourcentageLangue.pop()
        langueParlee.pop()
    
    print("\n")
    
    #On affiche les tableaux pour les traces d'exécution
    if tracesExec : print("Tableau des langues parlées : ", langueParlee)
    if tracesExec : print("Tableau des langues : ", pourcentageLangue)
    
    #On génère notre graphique avec les listes langueParlee et pourcentageLangue
    plt.bar(langueParlee, pourcentageLangue)
    plt.xlabel("Langues")
    plt.ylabel("Pourcentage")
    plt.title("Pourcentage d'apparition de la langue dans les commentaires de " + nomVille)
    plt.xticks(rotation=90)  # rotation des étiquettes à 90 degrés
    plt.show()
    plt.ylim(0, 100)



def r3():
    #Création de listes qui représenteront chacune une colonne de notre BD
    nomVille = []
    comm = []
    avgLgtScoreMoyen = []
    
    #On demande le nombre de villes pour l'exécution du programme
    nombreParam = input("Combien de villes cherchez-vous ? ")
    for i in range(int(nombreParam)):
        #On ajoute la réponse dans la liste
        nomVille.append(input("Quel est le nom de la ville ? : "))  
    
    #La requete SQL
    SQLCommand = ("""
                  SELECT a.Commune, ROUND(AVG(l.logt_review_scores_rating)*4,2) AS score_moyen
                  FROM logements l
                  INNER JOIN reviews r ON l.log_id = r.logement_id
                  INNER JOIN nodenot_bd.agglo_paysbasque a ON l.logt_codeINSEE = a.code_insee
                  WHERE l.logt_instant_bookable = 1 AND a.Commune = ?
                  GROUP BY a.Commune;
                  """)
    
    print("\n")
    
    #On exécute la requête autant de fois qu'il y a de paramètres donnés par l'utilisateur
    for i in range(int(nombreParam)):
        param = (nomVille[i])
        cursor.execute(SQLCommand, param)
    
        #On ajoute les élements de réponse dans les listes correspondantes
        for row in cursor.fetchall(): 
            if tracesExec : print("Résultats de la requête : ", row)
            nomCommune, scoreMoyenLgt = row
            comm.append(nomCommune)
            avgLgtScoreMoyen.append(scoreMoyenLgt)
    
    print("\n")
    
    #On affiche les tableaux pour les traces d'exécution
    if tracesExec : print("Tableau de communes : ", comm)
    if tracesExec : print("Tableau du score moyen des logements directement disponibles à la location : ", avgLgtScoreMoyen)
    
    #On génère notre graphique avec les listes comm et propHotesHabts
    plt.bar(comm, avgLgtScoreMoyen)
    plt.xlabel("Villes")
    plt.ylabel("Score moyen logements")
    plt.title("Score moyen des logements directement disponibles en fonction des villes")
    plt.ylim(0, 20)
    plt.show()


#%% S2.04 -- Programme principal


while(True):
    #On demande à l'utilisateur la requête qu'il souhaite exécuter
    choixRequete = input(""" \n \n 
Choisissez votre requête :
 1 - Pourcentage de logements secondaires dans une ville
 2 - Pourcentage de langues parlées dans les commentaires d'une ville
 3 - Score moyen d'évaluation d'une ville
 4 - Activer/ Désactiver les traces d'exécution
 5 - Quitter 
 Aide - Si certaines villes ne sont pas affichées, vérifiez s'il y a une erreur dans l'ortographe de la ville, ou si elle existe au Pays Basque \n 
Votre choix : """)
    
    #Appel des requêtes en fonction du choix de l'utilisateur
    match choixRequete:
        case "1":
            print(r1())
        case "2":
            print(r2())
        case "3":
            print(r3())
        case "4":
            if tracesExec:
                tracesExec = False
                print("Traces d'exécution désactivées")
            else:
                tracesExec = True
                print("Traces d'exécution activées")
        case "5":
            break
        case _:
            print("\n \n Erreur en entrée, reessayez : ")