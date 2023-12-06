#from new import artists

import fonctions1 as f 
import pandas as pd 

def aggregate_top(top):
    ''' 
    grouper par l'artiste et titre de la chanson, sommer pour chaque groupe les streams et obtenir la valeur cumulée 
    
    '''
    aggregate_top_table = f.calculate(top,
                      ["Artist", "Title"],
                      ["Streams"],
                      [lambda x: round(x.sum())])
    return(aggregate_top_table)

def create_exploded_table(adj_tracks):
    
 '''
 Calcule la table avec la transformation de la liste des aartistes en lignes pour avoir pour chaqun une ligne individuelle
 '''
 #cette table sera utilisée après dans d'autres fonctions de ce fichier, sans l'appeler dans les arguments
 global new_adj_tracks

     #on passe de string en liste 
 adj_tracks["new_ids_splitted"]=adj_tracks["new_ids"].str.split(",")
     #on crée une autre table  pour faire en sorte que même s'il y a plusieurs artistes qui ont contribué à la chanson,
     # il y aura une ligne par artiste (table new_adj_tracks)
 new_adj_tracks=adj_tracks.explode("new_ids_splitted").reset_index(drop=True)
     # on supprime les espaces à gauche et à droite qui ont été créés lors de cleaning 
 new_adj_tracks["new_ids_splitted"]=new_adj_tracks["new_ids_splitted"].apply(lambda x : x.strip())

 
 return(new_adj_tracks)
 

def les_chansons_populaires(artists,aggregate_top_table,artist_name_input):
    '''  
    Presente de manière universelle les données pertinentes pour chaque auteur
    Fonction permettant de récupérer un certain nombre d'informations sur un 
    artiste que l'on souhaite rechercher:
    
    
    Args:
        artist_name_input (str) : l'auteur de la chanson 

    Returns:
        la table pour chaque artiste trouvé  avec:
            les chansons les plus populaires
            les chansons les plus recentes
            le nb de chansons dans top 200 2020
            
    
    '''
    
    def repeat_info(el):
        
        '''  
        Execute le tri selon le critère défini 
        
        Args: 
            el (str): soit la date de sortie, soit le score de popularité
        Returns:
            La table triée selon le critère
        
        '''
        #pour chaque artiste trouvé, trier dans l'ordre descendant la popularité/la date de sortie
        df_songs_by_criterion = chansons_Beyonce.groupby(["id"], group_keys=True).apply(
            lambda x: x.sort_values(el, ascending=False).head(3)
        )
        #on d2finit le nom de la colonne de la table finale 
        name = "most popular songs"
        #s"il s'agit de trier par date, alors , convertir la date en string et définir un autre nom
        if el == "min_release_date_concrete":
            df_songs_by_criterion["min_release_date_concrete"] = pd.to_datetime(
                df_songs_by_criterion["min_release_date_concrete"]
            ).dt.strftime("%Y-%m-%d")
            name = "most recent songs"
        #Concatenate le nom de la chanson et sa popularité/date
        df_songs_by_criterion[name] = df_songs_by_criterion.apply(
            lambda x: x["name_track"] + ": " + str(x[el]), axis=1
        )
        #Supprimer les variables inutiles
        result = df_songs_by_criterion.drop(
            [
                "name_track",
                "max_popularity",
                "min_release_date",
                "min_release_date_concrete",
                el,
            ],
            axis=1,
        ).reset_index(drop=True)
        
        return result
    #Début de la fonction les_chansons_populaires
    
    #tant qu'il n'y a pas d'erreur on fait:
    try:
        #trouver l'artiste dans la table des artistes avec le nb de followers
        Beyonce = artists[(artists["name"].str.lower()).str.contains(artist_name_input.lower())]
        
        #SI les résultats existent dans la table top 200 , trouver les:
        #grouper par chaque artiste trouvé et calculer le distinct count sur les chansons trouvées dans top 200 
        nb_200top = f.calculate(
              Beyonce.drop_duplicates("name").merge(
                  aggregate_top_table, left_on="name", right_on="Artist"
              ),
              ["name"],
              ["Title"],
              ["nunique"],
              ["nb of top 200 chansons"],
        )
        #ajouter au résultat
        Beyonce = Beyonce.merge(nb_200top, on="name", how="left")
        
        #essayer de trouver aussi les chansons pour cet artiste dans la table des chansons:
        #attention, on utilise la table définie dans la fonction create_exploded_table de ce fichier
        #on selectionne certaines vqriqbles 
        chansons_Beyonce = Beyonce.merge(
            new_adj_tracks, left_on="id", right_on="new_ids_splitted"
        )[
            [
                "id",
                "name",
                "followers",
                "name_track",
                "max_popularity",
                "min_release_date",
                "min_release_date_concrete",
                "nb of top 200 chansons"
            ]
        ]
        #on définit 2 tables avec la fonction  définie avant:
        #les chansons les plus populaires 
        popularity = repeat_info("max_popularity")
        #les chansons les plus recentes
        recent = repeat_info("min_release_date_concrete")
        #on concatenate les 2 tables ensembles
        #puisque on aura toujours le nombre de lignes identiques dans 2 tables avec le même ordre des auteurs,
        #on peut les concatenate simplement
        result = pd.concat(
            [popularity, recent.drop(["id", "name", "followers","nb of top 200 chansons"], axis=1)], axis=1
        )
        result['nb of top 200 chansons']=result['nb of top 200 chansons'].fillna('no data')
        result['followers'] = result['followers'].fillna(0)
       
        result['followers'] = result['followers'].astype(int)
        
        
    #si on a des erreurs , alors il y a 2 raisons
    except:
        #la table de l'artiste est vide 
        if Beyonce.empty:
            result = None
        #la table des chansons est vide
        elif chansons_Beyonce.empty:
            Beyonce = Beyonce[["id",	"name",	"followers","nb of top 200 chansons"]]
            #on crée une colonne "no data" qui signifie que cet auteur n'a pas les chansons trouvées
            series_with_f = pd.Series(["no data"]* Beyonce.shape[0])
            #on les concatenate
            result = pd.concat([Beyonce, series_with_f,series_with_f], axis=1).reset_index(drop=True)
            result = result.rename(columns={0: 'most popular songs',1: 'most recent songs'})
            result['followers'] = result['followers'].fillna(0)
      
            
            result['followers'] = result['followers'].astype(int)
            
    #fin de la fonction les_chansons_populaires
    
    
    
  
    return result


def chanson_genre(artists,genre,annee):
     '''  
     Trouve à partir de l'année de sortie et de genre la chanson dans la base
     
     Args:
        artist (df) table des artistes
        artiste_genre(str) genre de l artiste
        annee (str) de l artiste
     
     '''
     
     df_art_genre=artists[artists['genres'].str.lower().str.contains(genre.lower()) ] 
     
     df_genre=df_art_genre[["id","popularity", "genres"]]
     df_genre=df_genre.rename(columns={"id":"id_1art", "popularity": "pop_a"}) 
   
     df_year = new_adj_tracks[new_adj_tracks["min_release_date_concrete_str"].
                              astype(str).str.contains(str(annee))]
     df_year=df_year.rename(columns={"new_ids_splitted":"id_1art"})
   
     df_merge=pd.merge(df_genre, df_year, how="inner", on=["id_1art"])
     df_merge_sort=df_merge.sort_values(["pop_a","max_popularity"],
                                        ascending=False)
     return df_merge_sort






def chanson_results(adj_tracks,chanson_titre):
    
   '''  
   Retourne les résultats pértinents des chansons
   
   Args:
        adj_tracks (df) tables des chansons corrigée
        chanson_titre (str) nom de la chanson
   '''
   
   #filtrer sur lower les chansons
   recherche = adj_tracks[(adj_tracks['name_track'].str.lower()).str.contains(chanson_titre.lower(), 
                                                    case=False, 
                                                    na=False)]
   #trier
   recherche = recherche.sort_values(by='max_popularity', ascending=False)
   #select some columns
   recherche = recherche[['name_track', 
                            'max_popularity', 
                            'name_artist', 
                            'min_release_date_concrete_str', 
                            'duration_ms']]
   
   return recherche


