"""
@author : Latxague Thibault / Rafael Masson
"""

#importations de bibliotheques
import pandas as pd
import numpy as np
import os

#choix du repertoire par defaut
os.chdir('F:\Desktop\S2\S2.04')

#importation des dataframes
communes=pd.read_table('capb-communes-poles.csv',index_col=0,sep=",")
hotes=pd.read_table('hotes.csv',sep=";",decimal=',')
logements=pd.read_table('logements.csv',index_col=0,sep=';',decimal=',')
reviews=pd.read_table('reviews.csv',index_col='id',sep=",")


#%% idees

#1. le pourcentage de logements par region

#2. densite de la commune en terme de logements AirBnB

#3. analyse bivariee entre prix/nuit monnaie locale et emplacement logement

#4. moyenne des scores des logement en fonction de la region

# localisations, notes, lien entre la taille/localisation, notes/taille, localisation/taille, capacite/notes...
# mapping des score moyen par communes... ; par region, typeLogement
# carte representant les logements airbnb colores en fonction de nbTaille/nbLit/score/prix/rapportQualPrix/txAcceptationHote/

#%% Objectif : alimenter la table communes

logements.dtypes #variables de la table logements


#%% jointure des effectifs de la colonne logt_codeINSEE dans la table communes
nb_logements = logements['logt_codeINSEE'].value_counts() #nombre de logements par communes (codeINSEE)

#jointure du nombre de logements par communes dans la table communes
communes=pd.merge(communes,nb_logements,left_index=True,right_index=True,how="left")

#renommer la colonne logt_codeINSEE en nb_logements
listetmp=list(communes.columns)
listetmp[8]='nb_logements'
communes.columns=listetmp

#remplacer les nan de la variable nb_logements par des 0
communes['nb_logements']=communes['nb_logements'].replace(np.nan, 0)

#%% jointure des effectifs des modalites de logt_room_type dans la table communes
logements['logt_room_type'].unique() #modalites de la variable logt_room_type

# tableau de contingence entre les types de logements et le codeINSEE
nb_roomType_commune = pd.crosstab(logements['logt_codeINSEE'],logements['logt_room_type'])

#jointure du nombre de types de logements par communes dans la table communes
communes=pd.merge(communes,nb_roomType_commune,left_index=True,right_index=True,how="left")

#renommer les colonne pour avoir des noms pas separes par des espaces
listetmp=list(communes.columns)
listetmp[9]='Entire_home/apt'
listetmp[10]='Hotel_room'
listetmp[11]='Private_room'
listetmp[12]='Shared_room'
communes.columns=listetmp

#remplacer les nan par des 0 des variables representant les types de logements tires des modalites de logt_room_type
communes['Entire_home/apt']=communes['Entire_home/apt'].replace(np.nan, 0)
communes['Hotel_room']=communes['Hotel_room'].replace(np.nan, 0)
communes['Private_room']=communes['Private_room'].replace(np.nan, 0)
communes['Shared_room']=communes['Shared_room'].replace(np.nan, 0)

#%% jointure de la moyenne de la colonne logt_accommodates dans la table communes
#moyenne de la colonne logt_accommodates par communes (codeINSEE)
moy_nbPersonneMax = logements['logt_accommodates'].groupby(logements['logt_codeINSEE']).mean()

#jointure de la moyenne de la colonne logt_accommodates par communes dans la table communes
communes=pd.merge(communes,moy_nbPersonneMax,left_index=True,right_index=True,how="left")

#renommer la colonne logt_accommodates en moy_nbPersonneMax
listetmp=list(communes.columns)
listetmp[13]='moy_nbPersonneMax'
communes.columns=listetmp

#remplacer les nan de la variable moy_nbPersonneMax par des 0
communes['moy_nbPersonneMax']=communes['moy_nbPersonneMax'].replace(np.nan, 0)

#%% jointure de la moyenne de la colonne logt_beds dans la table communes
#moyenne de la colonne logt_beds par communes (codeINSEE)
moy_nbLits = logements['logt_beds'].groupby(logements['logt_codeINSEE']).mean()

#jointure de la moyenne de la colonne logt_beds par communes dans la table communes
communes=pd.merge(communes,moy_nbLits,left_index=True,right_index=True,how="left")

#renommer la colonne logt_beds en moy_nbLits
listetmp=list(communes.columns)
listetmp[14]='moy_nbLits'
communes.columns=listetmp

#remplacer les nan de la variable moy_nbLits par des 0
communes['moy_nbLits']=communes['moy_nbLits'].replace(np.nan, 0)

#%% jointure de la moyenne de la colonne logt_prix dans la table communes
#moyenne de la colonne logt_prix par communes (codeINSEE)
moy_prixNuit = logements['logt_prix'].groupby(logements['logt_codeINSEE']).mean()

#jointure de la moyenne de la colonne logt_prix par communes dans la table communes
communes=pd.merge(communes,moy_prixNuit,left_index=True,right_index=True,how="left")

#renommer la colonne logt_prix en moy_prixNuit
listetmp=list(communes.columns)
listetmp[15]='moy_prixNuit'
communes.columns=listetmp

#remplacer les nan de la variable moy_prixNuit par des 0
communes['moy_prixNuit']=communes['moy_prixNuit'].replace(np.nan, 0)

communes.boxplot(by= 'Poles1', column=['moy_prixNuit'])

#%% jointure de la moyenne de la colonne logt_review_scores_rating dans la table communes
#moyenne de la colonne logt_review_scores_rating par communes (codeINSEE)
moy_notes = logements['logt_review_scores_rating'].groupby(logements['logt_codeINSEE']).mean()

#jointure de la moyenne de la colonne logt_review_scores_rating par communes dans la table communes
communes=pd.merge(communes,moy_notes,left_index=True,right_index=True,how="left")

#renommer la colonne logt_review_scores_rating en moy_notes
listetmp=list(communes.columns)
listetmp[16]='moy_notes'
communes.columns=listetmp

#remplacer les nan de la variable moy_notes par des 0
communes['moy_notes']=communes['moy_notes'].replace(np.nan, 0)

#%% jointure de la moyenne de la colonne logt_review_scores_value dans la table communes
#moyenne de la colonne logt_review_scores_value par communes (codeINSEE)
moy_qualite_prix = logements['logt_review_scores_value'].groupby(logements['logt_codeINSEE']).mean()

#jointure de la moyenne de la colonne logt_review_scores_value par communes dans la table communes
communes=pd.merge(communes,moy_qualite_prix,left_index=True,right_index=True,how="left")

#renommer la colonne logt_review_scores_value en moy_qualite_prix
listetmp=list(communes.columns)
listetmp[17]='moy_qualite_prix'
communes.columns=listetmp

#remplacer les nan de la variable moy_qualite_prix par des 0
communes['moy_qualite_prix']=communes['moy_qualite_prix'].replace(np.nan, 0)

#%% jointure de la moyenne de la colonne logt_price_per_bed dans la table communes

#Calcul du prix/lits pour chaque enregistrement de la table logements et création de cette variable
logements['logt_price_per_bed'] = logements['logt_prix'] / logements['logt_beds']

#moyenne de la colonne logt_price_per_bed par communes (codeINSEE)
moy_prix_par_lit = logements['logt_price_per_bed'].groupby(logements['logt_codeINSEE']).mean()

#jointure de la moyenne de la colonne logt_price_per_bed par communes dans la table communes
communes=pd.merge(communes,moy_prix_par_lit,left_index=True,right_index=True,how="left")

#renommer la colonne logt_price_per_bed en moy_prix_par_lit
listetmp=list(communes.columns)
listetmp[18]='moy_prix_par_lit'
communes.columns=listetmp

#remplacer les nan de la variable moy_prix_par_lit par des 0
communes['moy_prix_par_lit']=communes['moy_prix_par_lit'].replace(np.nan, 0)

