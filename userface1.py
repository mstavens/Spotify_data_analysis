#################################
"""
TKINTER
"""

import pandas as pd
import webbrowser
import cleaning1 as cl
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
#################################

import time
import fonctions1 as f
import load_data1 as l
import part1_1 as p1
import cleaning1 as cl
import part2_1 as p2
#################################

from main import adj_tracks,artists,aggregate_top_table,new_adj_tracks


def creer_interface():
    
 '''  
    On crée un userface graphique pour afficher les résultats
 '''
 ig = tk.Tk() #fenêtre vide

    #définition: titre, taille, fond, ...:
 ig.title("Spotify Search")
 ig.minsize(480, 320) 
 ig.configure(bg="#1DB954") #RGB Spotify: green

 saisir_chanson = tk.Label(ig, text="Entrez le titre de la chanson :", 
                      bg='#1DB954', 
                      fg='white',
                      highlightbackground='#191414',
                      font=('Arial', 16))
 saisir_chanson.grid(row=0, column=0, padx=10, pady=10, sticky='w')

 entry_chanson = tk.Entry(ig,  highlightbackground='#191414',#RGB Spotify: black
                              font=('Arial', 16))
 entry_chanson.grid(row=0, column=1, padx=10, pady=10)

 columns_chanson = ['Name', 
                        'Popularity', 
                        'Artist(s)', 
                        'Release Date', 
                        'Duration(in Min)', 'URL']
    #seulement quelques colonnes("pertinentes") sont séléctionnées

 tab_chanson = ttk.Treeview(ig, columns=columns_chanson, show='headings')
    #show=headings => on définit les en-têtes

 for col in columns_chanson:
        tab_chanson.heading(col, text=col) #on attribue un nom à chaque colonne
        tab_chanson.column(col, width=200, anchor='center') 
 tab_chanson.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky='w')


 def ma_chancon():
         ''' 
        Afficher les informations pertinentes pour chaque chanson trouvée ou non 
        '''
 chanson_titre = entry_chanson.get() #extrait le texte saisi

 recherche=p2.chanson_results(adj_tracks,chanson_titre)


 for i in tab_chanson.get_children():  #parcourt les éléments de tab et les 
            tab_chanson.delete(i)             #supprime

 if not recherche.empty: #si pas vide (=si condition verifiée)
            true_recherche = recherche.head(20).copy()
            access_token = f.get_access_token('e4966233faa14ead9b584b63f3eb57df','779a9a68fb9f4b3484a6f903f9d90c66')
              #creation de la vriable link qui recevra les url des chansons dans le dataframe
            true_recherche.loc[:, 'link'] = None
            for j in true_recherche.index.tolist():
                 #Obtention de l'ID de la chanson
                 track_id = f.get_track_id(true_recherche.loc[j, 'name_track'], true_recherche.loc[j, 'name_artist'], access_token)
                 #Obtention de l'adresse url
                 track_url = f.get_track_url(track_id)
                 
                 #Enregistrement de l'url dans la colonne lien web du dataframe
                 if track_url != 'https://open.spotify.com/track/None' :
                     true_recherche.loc[j, 'link'] = track_url
            
            for col, row in  true_recherche.head(20).iterrows():#afficher les resultat
                tab_chanson.insert("", "end", values=(row['name_track'], 
                                           row['max_popularity'],
                                           row['name_artist'], 
                                           row['min_release_date_concrete_str'], 
                                           row['duration_ms'], row['link'] ))
 else:#sinon afficher rien 
            tab_chanson.insert("", "end", values=("Aucun résultat", "", "", "", "", ""))
            #"end" <=> tk.End
    #appliquer la fonction 
 button_chanson = tk.Button(ig, text="Rechercher", command=ma_chancon, 
                                  bg='#191414', 
                                  fg='#191414',
                                  highlightbackground='#191414',
                                  font=('Arial', 16))
    #command executée sera la fonction précédemment définie, en cliquant sur le 
    #bouton, chaque colonne de l'objet 'tab_chanson' prendra une valeur

 button_chanson.grid(row=0, column=2, padx=10, pady=10, sticky='e')

 saisir_artiste = tk.Label(ig, text="Entrez le nom de l'artiste :", 
                      bg='#1DB954', 
                      fg='white',
                      highlightbackground='#191414',
                      font=('Arial', 16))
 saisir_artiste.grid(row=2, column=0, padx=10, pady=10, sticky='w')

 entry_artiste = tk.Entry(ig,  highlightbackground='#191414', font=('Arial', 16))
 entry_artiste.grid(row=2, column=1, padx=10, pady=10)
    #on definit l ordre d'affichage des colonnes
 columns_artist = ['ID', 
                       'Name', 
                       'Followers', 
                       'Nb of Top 200 tracks',
                       'Most Popular songs', 
                       'Most Recent Songs']

 tab_artist = ttk.Treeview(ig, columns=columns_artist, show='headings')
 tab_artist.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky='w')

 for col in columns_artist:
        tab_artist.heading(col, text=col.capitalize())
        tab_artist.column(col, width=200)

 def info_artiste():
         '''  
         Afficher les chansons les plus populaires/recentes

         '''
 nom_artiste = entry_artiste.get() #on récupére le nom
 df = p2.les_chansons_populaires(artists,aggregate_top_table,nom_artiste) #df, sous forme d'un DataFrame
        #récupère les informations relatives à l'artiste en question
        #et execute la fonction définie en dehors de cette fenêtre, plus précisem-
        #ment la fonction "partie_2_question_1" qui prend en paramètre le nom de 
        #l'artiste

 for i in tab_artist.get_children():
            tab_artist.delete(i) #permet de supprimer les éléments saisis pour 
             #éviter que les lignes s'enchainent une après l'autre 
             #(on efface de la mémoire ce qui a été saisi)


 if df is not None:#si le df is None alors afficher rien car on a pas trouvé cet artiste
             #sinon: afficher les resultats:
            for col, row in df.iterrows():
                tab_artist.insert("", "end", values=list(row))

 else: #si pas vide (=si condition verifiée)


            tab_artist.insert("", "end", values=("Aucun résultat", "", "", "", "", ""))
             #"end" <=> tk.End




 button_artiste = tk.Button(ig, text="Rechercher", command=info_artiste, 
                                  bg='#191414', 
                                  fg='#191414',
                                  highlightbackground='#191414',
                                  font=('Arial', 16))
    #au bouton est associé une nouvelle commande: 'info_artiste'

 button_artiste.grid(row=2, column=2, padx=10, pady=10, sticky='e')

 saisir_genre = tk.Label(ig, text="Genre :", 
                      bg='#1DB954', 
                      fg='white',
                      highlightbackground='#191414',
                      font=('Arial', 16))
 saisir_genre.grid(row=4, column=0, padx=10, pady=10, sticky='w')
 saisir_genre.place(x=325,y=600)

 saisir_annee = tk.Label(ig, text="Année :", 
                      bg='#1DB954', 
                      fg='white',
                      highlightbackground='#191414',
                      font=('Arial', 16))
    #la méthode appliquée est la même dans les trois cas 

 saisir_annee.grid(row=5, column=0, padx=10, pady=10, sticky='w') 
 saisir_annee.place(x=325,y=700) 

 entry_genre = tk.Entry(ig,  
                            highlightbackground='#191414', 
                            font=('Arial', 16))
 entry_genre.grid(row=4, column=1, padx=10, pady=10, sticky='w')  
 entry_genre.place(x=400,y=600) 

 entry_annee=tk.Entry(ig,  
                          highlightbackground='#191414', 
                          font=('Arial', 16))
 entry_annee.grid(row=5, column=1, padx=10, pady=10, sticky='w') 
 entry_annee.place(x=400,y=700)  

 columns = ["Artist(s)", 'Song', 'Release date','URL']

 tab_genre_annee = ttk.Treeview(ig, columns=columns, show='headings')

 for col in columns:
        tab_genre_annee.heading(col, text=col)
        tab_genre_annee.column(col, width=130, anchor='center')
 tab_genre_annee.grid(row=4, column=2, columnspan=4, padx=10, pady=10)  

 def genre_an():

        genre = entry_genre.get()
        annee = entry_annee.get()

        df_merge_sort=p2.chanson_genre(artists,genre,annee)
        for i in tab_genre_annee.get_children():
            tab_genre_annee.delete(i)

        if not df_merge_sort.empty: #si pas vide
            true_df_merge_sort = df_merge_sort.head(20).copy()
            access_token = f.get_access_token('e4966233faa14ead9b584b63f3eb57df','779a9a68fb9f4b3484a6f903f9d90c66')
              #creation de la vriable link qui recevra les url des chansons dans le dataframe
            true_df_merge_sort.loc[:, 'link'] = None
            for j in true_df_merge_sort.index.tolist():
                 #Obtention de l'ID de la chanson
                 track_id = f.get_track_id(true_df_merge_sort.loc[j, 'name_track'], true_df_merge_sort.loc[j, 'name_artist'], access_token)
                 #Obtention de l'adresse url
                 track_url = f.get_track_url(track_id)
                 
                 #Enregistrement de l'url dans la colonne lien web du dataframe
                 if track_url != 'https://open.spotify.com/track/None' :
                     true_df_merge_sort.loc[j, 'link'] = track_url
            print(true_df_merge_sort)
            for col, row in true_df_merge_sort.head(20).iterrows():
                tab_genre_annee.insert("", "end", values=(row['name_artist'], 
                                           row['name_track'], 
                                           row['min_release_date_concrete_str'], row['link']))
        else: #si vide
            tab_genre_annee.insert("", "end", values=("Aucun résultat", "", ""))

 button_recherche = tk.Button(ig, text="Rechercher", command=genre_an, 
                                  bg='#191414', 
                                  fg='#191414',
                                  highlightbackground='#191414',
                                  font=('Arial', 16))
 button_recherche.place(x=435,y=650)

    #lien spotify ==> espace compte 

 def spotify_link():
        lien_spotify = "https://accounts.spotify.com/fr/login?continue=https%3A%2F%2Fopen.spotify.com%2Fintl-fr"
        webbrowser.open(lien_spotify)
        #ouvre l'URL dans le navigateur
        #comme avant, on stocke la fonction dans un bouton cliquable

 bouton_link = tk.Button(ig, text="Se Connecter", command=spotify_link,
                                     bg='#191414', fg='#191414', padx=10, pady=10, 
                                     font=('Arial', 20),
                                     highlightbackground='#191414')
 bouton_link.grid(row=4, column=0, padx=10, pady=10, sticky='w') 
 bouton_link.place(x=10,y=720)

 phrase = tk.Label(ig, text="(Pour plus de contenus \n connectez-vous) ", 
                     bg='#1DB954', 
                      fg='white',
                      highlightbackground='#191414',
                      font=('Arial', 11))
 phrase.place(x=35, y=685)

 ig.mainloop()

#################################
###############FIN###############