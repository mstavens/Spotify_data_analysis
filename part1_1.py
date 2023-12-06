import pandas as pd
import fonctions1 as f 
#from new import artists

def top_artists(artists):


    '''
    Calcule les 10 artistes les plus populaires avec le graphique
    '''


    #trier par la popularité descendante les artistes, parmi les top 10, trier par la popularité
    top_artists_table = (
    artists.sort_values("popularity", ascending=False).head(10).sort_values("followers", ascending=False)


    )

    #afficher en millions de followers 
    top_artists_table["followers_M"] = round(top_artists_table["followers"] / 1000000, 2)
    #afficher le graphique
    f.bar_plot(top_artists_table, "name", "followers_M")


def chansons_par_annee(adj_tracks): 
    
    ''' 
    Calcule le nombre de chansons sorties chaque année avec le graphique
    '''   
    #grouper par l'année et calculer le distinct count sur les id des chansons, trier 

    chansons_par_annee_table = f.calculate(
        adj_tracks, ["min_release_date"], ["adj_id_track"], ["nunique"], ["nb of tracks"]
    ).sort_values("min_release_date", ascending=False)

    #afficher le graphique
    f.bar_plot(chansons_par_annee_table, "min_release_date", "nb of tracks") 

    
    
def artistes_top_200(top):    
    '''  
    Calcule les artistes ont le plus de chansons distinctes dans le top 200 Global avec le graphique
    '''
    #  #creer un id 
    #  top["adj_id_track"] = top["Artist"] + "_" + top["Title"]
    
    #grouper par l'artiste et titre de la chanson, sommer pour chaque groupe les streams et obtenir la valeur cumulée 
    first = f.calculate(top,
                      ["Artist", "Title"],
                      ["Streams"],
                      [lambda x: round(x.sum())])
     #une fois on a obtenu UNE valeur de stream pour chaque chanson et artiste,
     # on calcule pour chaque artiste le distinct count des chansons et la somme des streams , ensuite on trie 
    artistes_top_200_table=f.calculate(
         first,
         ["Artist"],  
         ["Title", "Streams"],
         ["nunique", "sum"],
         ["nb of tracks", "streams"],
     ).sort_values(["nb of tracks", "streams"], ascending=False).head(35)

     #afficher le graphique
    f.bar_plot(artistes_top_200_table, "Artist", "nb of tracks")
    
    
def correlation_popularite(adj_tracks):
    '''  
    calcule la correlation entre la popularité et les autres variables avec un graphique
    '''
    
    #calcule la correlation, on supprime les variables inutiles et on utilise que la popularité vs autres variables
    cor=pd.DataFrame( adj_tracks.drop(
    ["adj_id_track","is_duplicated"], axis=1
    ).corr(numeric_only=True)["max_popularity"]).T
    
    
    #on definit le graphique et ces éléments
    f.plt.figure(figsize=(15, 1))
    f.sns.heatmap(cor, annot=True, cmap='coolwarm', fmt=".1f", linewidths=.1)
    f.plt.title(f'Pearson Correlation Coefficients with Popularity ')
    f.plt.xticks(rotation=45, ha='right')
    f.plt.show()