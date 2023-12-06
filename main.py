import pandas as pd

import fonctions1 as f
import load_data1 as l
import part2_1 as p2
import cleaning1 as cl
import userface1 as us

#importer les fichiers
my_tables=l.load_tables(["artists","spotify_top200_global","tracks"])
#stocker  les tables 
artists=my_tables["artists"]
top=my_tables["spotify_top200_global"]
tracks=my_tables["tracks"]

#clean la table chansons
adj_tracks=cl.clean_tracks(tracks)

#modifier la table des chansons
new_adj_tracks=p2.create_exploded_table(adj_tracks)
#modifier la table des top chansons
aggregate_top_table=p2.aggregate_top(top)


#afficher le userface
if __name__=="__main__":
    us.creer_interface()