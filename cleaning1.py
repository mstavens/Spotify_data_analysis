import fonctions1 as f
import pandas as pd 

def clean_tracks(tracks):
    
  '''  
    We work on  the most unclean table : tracks, a lot of dupliccates, investigation and correction 
    
    
  '''
  
    #creer les champs sans [  , ] , ' pour les utiliser après 

  tracks["new_artist"] = tracks["artists"].str.replace("[\[\]']", "", regex=True)

  tracks["new_ids"] = tracks["id_artists"].str.replace("[\[\]']", "", regex=True)



      # create real track id to deduplicate on it afterwards
  tracks["adj_id_track"] = tracks["name"] + "_" + tracks["new_artist"] 


      # delete empty values as otherwise they will create a lot of variance when aggregating ->bias in figures
  tracks["adj_id_track"].fillna("unknown", inplace=True)
  tracks = tracks[tracks["adj_id_track"] != "unknown"].copy()


      # extract year
  tracks["release_date"] = pd.to_datetime(tracks["release_date"], format="%Y-%m-%d")
  tracks["year"] = tracks["release_date"].dt.year
  
  #delete columns that "hide" duplicate values, then->deduplicate
  new_tracks = tracks.drop(
      [
          "id",
          "name",
          "artists",
          "id_artists",
          "release_date",
          "new_artist",
          "year",
          "popularity",
          "new_ids"
      ],
      axis=1,
  ).drop_duplicates()
  
    # delete columns that "hide" duplicate values-> deduplicate one more time
  new_tracks["is_duplicated"] = new_tracks["adj_id_track"].duplicated()
  new_tracks = new_tracks[new_tracks["is_duplicated"] == False].copy()
    # from one side: calculate mean popularity and min date for every id
    # from another side: merge these aggregated results with unique and only unique results
  adj_tracks = f.calculate(
          tracks,
          ["adj_id_track","new_ids"],
          ["popularity", "year","release_date"],
          ["max", "min","min"],
          ["max_popularity", "min_release_date","min_release_date_concrete"],
      ).merge(new_tracks, on="adj_id_track", how="inner")


    #name track= first obs from list

  adj_tracks["name_track"] = adj_tracks["adj_id_track"].str.split("_").str[0]


    #name artist= second obs from list

  adj_tracks["name_artist"] = adj_tracks["adj_id_track"].str.split("_").str[1]




    #convert duration in minutes  
  adj_tracks['duration_ms'] = (adj_tracks['duration_ms']/60000).round(2)
    #convert to string for results
  adj_tracks['min_release_date_concrete_str'] = adj_tracks['min_release_date_concrete'].dt.strftime('%Y-%m-%d')


    # get final deduplicated and aggragated by id table, that will be used futher
  return(adj_tracks)
