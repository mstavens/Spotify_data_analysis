import zipfile
import pandas as pd
import os 

def load_tables(list_tables):
 '''  
    Téléchargements des données 
    
    Args:
        list_tables(list) : liste des strings des fichiesr
    Returns:
        le dictionnaire qui contient ces fichiers 
    
 '''#remonter d'un cran pour accéder au dossier data
    
 os.chdir("../")
 os.chdir("data")
 my_tables={}
 #dézipper chaque fichier et le sauvegarder en csv   
 for el in list_tables:
        zip_file_path = f'{el}.csv.zip'
        csv_file_name = f'{el}.csv'
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extract(csv_file_name, path='csv_unzip')
        csv_file_path = 'csv_unzip/' + csv_file_name
        my_tables[el]=pd.read_csv(csv_file_path,sep=",")

 return my_tables
  