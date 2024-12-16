"""
@author : Latxague Thibault / Rafael Masson
"""

#importations de bibliotheques
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
import geopandas as gpd

#choix du repertoire par defaut
os.chdir('C:\\Users\\rafae\\OneDrive\\Desktop\\IUT\\sae-s2-04-bdd\\csv')

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

#%%

communes['pb']='pb'
hotes = pd.merge(hotes, communes,left_on='host_ville',right_on='Commune',how="left")
hotes['origine']='Etranger'
hotes['host_pays']=hotes['host_pays'].replace(np.nan, False)
hotes.loc[hotes['host_pays']=='France', 'origine'] = 'France'
hotes.loc[hotes['host_pays']==False, 'origine'] = 'None'

hotes.loc[hotes['pb']=='pb', 'origine'] = 'Pays Basque'
hotes['host_pays']=hotes['host_pays'].replace(False, None)

# Fusionner les DataFrames communes et hotes sur la colonne Commune

merged_df = pd.merge(communes, hotes, on='Commune', how='left')

logements = pd.merge(logements, hotes[['host_id', 'origine']], on='host_id', how='left')

logements['Hote_PaysBasque'] = np.nan
logements['Hote_France'] = np.nan
logements['Hote_Etranger'] = np.nan
logements['Hote_Aucune_Donnee'] = np.nan


logements.loc[logements['origine'] == 'Pays Basque', 'Hote_PaysBasque'] = 1
logements.loc[logements['origine'] == 'France', 'Hote_France'] = 1
logements.loc[logements['origine'] == 'Etranger', 'Hote_Etranger'] = 1
logements.loc[logements['origine'] == 'None', 'Hote_Aucune_Donnee'] = 1


logements['Hote_PaysBasque'].count()
logements['Hote_France'].count()
logements['Hote_Etranger'].count()
logements['Hote_Aucune_Donnee'].count()

logements.dtypes
org_paysbasque = logements['Hote_PaysBasque'].groupby(logements['logt_codeINSEE']).count()
org_france = logements['Hote_France'].groupby(logements['logt_codeINSEE']).count()
org_etranger = logements['Hote_Etranger'].groupby(logements['logt_codeINSEE']).count()
org_inconnu = logements['Hote_Aucune_Donnee'].groupby(logements['logt_codeINSEE']).count()

#jointure de xxx dans la table communes

communes = pd.merge(communes, org_paysbasque, left_index=True,right_index=True,how="left")
communes = pd.merge(communes, org_france, left_index=True,right_index=True,how="left")
communes = pd.merge(communes, org_etranger, left_index=True,right_index=True,how="left")
communes = pd.merge(communes, org_inconnu, left_index=True,right_index=True,how="left")

logements['origine'].unique()
logements.dtypes

communes['Hote_PaysBasque']=communes['Hote_PaysBasque'].replace(np.nan, 0)
communes['Hote_France']=communes['Hote_France'].replace(np.nan, 0)
communes['Hote_Etranger']=communes['Hote_Etranger'].replace(np.nan, 0)
communes['Hote_Aucune_Donnee']=communes['Hote_Aucune_Donnee'].replace(np.nan, 0)


communes['nbr_ttl_donnees_valides']=0
communes['nbr_ttl_donnees_valides']=communes['Hote_PaysBasque'] + communes['Hote_France'] + communes['Hote_Etranger']
communes['%age_pb']=0
communes['%age_pb']=(communes['Hote_PaysBasque']/communes['nbr_ttl_donnees_valides'])*100
communes['%age_pb']=communes['%age_pb'].replace(np.nan,0)

#%% analyses

#%% bivariee entre 2 quanti : communes['moy_prixNuit'] et communes['nb_logements']
sns.scatterplot(x=communes['moy_prixNuit'],y=communes['nb_logements'],hue=communes['Poles1'])
plt.title('Prix moyen par nuit, nombre de logements AirB&B des poles de communes')
plt.xlabel('Prix moyen par nuit')
plt.ylabel('Nombre de logements')
plt.legend(title='Pole',bbox_to_anchor=(1.05,1.0), loc = 'upper left')
plt.ylim(-10,1900)


#%% bivariee entre 1 quali et 1 quanti : communes['moy_prixNuit'] et communes['Poles1']
communes.boxplot(by = 'Poles1', column = 'moy_prixNuit', grid = False, showmeans=True)
plt.title('Répartition des prix moyen des AirB&Bs par pole de communes')
plt.suptitle("")
plt.xlabel('Pole')
plt.ylabel('Prix moyen')

#pour obtenir un affichage correct, on cree une nouvelle varible contenant une mise en page de poles1
corresp = {'Garazi Baigorri - Iholdi Oztibarre - Soule Xiberoa' : 'Garazi\nIholdi\nSoule',
           'Sud Pays Basque - int' : 'SudPaysBsq',
           'Amikuze - Bidache - Hasparren - Nive Adour' : 'Amikuze\nBidache\nHasparren\nNive Adour',
           'Cote Basque Adour' : 'CoteBasque',
           'Errobi' : 'Errobi',
           'Hendaye - Urugne - Biriatou' : 'Hendaye\nUrugne\nBiriatou',
           'Stj luz - Guétary - Ciboure' : 'Stj luz\nGuetary\nCiboure',}

communes['PolesAbr']=communes['Poles1'].replace(corresp)

#on affiche le boxplot avec comme axe x la nouvelle variable
communes.boxplot(by = 'PolesAbr', column = 'moy_prixNuit', grid = False, showmeans=True)
plt.title('Répartition des prix moyen des AirB&Bs par pole de communes')
plt.suptitle("")
plt.xlabel('Pole')
plt.ylabel('Prix moyen')

#on aimerait bien que les moyennes des boites sur le graphique soient ordonnees...
#on regarde les triangles (moyennes) et on ordonne les poles:
communes['PolesAbr']=pd.Categorical(communes['PolesAbr'],
                                   ordered=True,
                                   categories=['SudPaysBsq',
                                               'Stj luz\nGuetary\nCiboure',
                                               'CoteBasque',
                                               'Errobi',
                                               'Hendaye\nUrugne\nBiriatou',
                                               'Amikuze\nBidache\nHasparren\nNive Adour',
                                               'Garazi\nIholdi\nSoule'
                                               ])

#les poles sont maintenant ordonnees
communes['PolesAbr'].unique()

#on affiche le boxplot avec les poles ordonnees par moyennes
communes.boxplot(by = 'PolesAbr', column = 'moy_prixNuit', grid = False, showmeans=True)
plt.title('Répartition des prix moyen des AirB&Bs par pole de communes')
plt.suptitle("")
plt.xlabel('Pole')
plt.ylabel('Prix moyen')

#%% bivariee entre 2 quanti : communes['Hote_PaysBasque'], et communes['Population_2021']
sns.scatterplot(x=communes['Hote_PaysBasque'],y=communes['Population_2021'],hue=communes['Poles1'])
plt.title('Prix moyen par nuit, nombre de logements AirB&B des poles de communes')
plt.xlabel('Pourcentage d\'hotes originaire du pays basque')
plt.ylabel('Nombre de logements')
plt.legend(title='Pole',bbox_to_anchor=(1.05,1.0), loc = 'upper left')

#on ajoute des limites afin de mieux voir la partie interessante du nuage de points
#remarque : on ne voit plus les 3 points isolés de Cote Basque Adour
sns.scatterplot(x=communes['Hote_PaysBasque'],y=communes['Population_2021'],hue=communes['Poles1'])
plt.title('Prix moyen par nuit, nombre de logements AirB&B des poles de communes')
plt.xlabel('Pourcentage d\'hotes originaire du pays basque')
plt.ylabel('Nombre de logements')
plt.legend(title='Pole',bbox_to_anchor=(1.05,1.0), loc = 'upper left')
plt.xlim(-10,500)
plt.ylim(-10,20000)

#%% cartographie
# importation du geodataframe
contours = gpd.read_file('capb-communes-poles.geojson')
contours['insee'] = contours['insee'].astype(int)
contours.set_index('insee',inplace= True )


# Jointure du dataframe communes et du geodataframe contours
communesgpd = contours.merge(communes,left_index=True, right_index = True)

#on set les contours de la carte sur la variable geometry
communesgpd.set_geometry('geometry', inplace = True)

#visualisation des poles sur la carte
gf = communesgpd.plot(column = "Poles1", legend = False)
gf.set_axis_off()

#----------------
gf = communesgpd.plot(column = "%age_pb", legend = True, cmap ='RdYlGn',
legend_kwds={"label": 'Proportion d\'hotes originaires du Pays Basque',"orientation": "horizontal"})
gf.set_axis_off()

#----------------
gf = communesgpd.plot(column = "moy_prixNuit", legend = True, cmap ='RdYlGn',
legend_kwds={"label": 'Repartition du prix/nuit par commune',"orientation": "horizontal"})
gf.set_axis_off()