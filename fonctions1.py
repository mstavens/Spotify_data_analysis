import pandas as pd
import matplotlib.pyplot as plt
from typing import List
import seaborn as sns
import requests
import base64



def calculate(
    df: pd.DataFrame,
    group: List[str],
    fields: List[str],
    stats: str = "sum",
    names: List[str] = None,
) -> pd.DataFrame:
    """
    "Group by" operation on multiple fields and aggregate functions, the code becomes easier than standard pandas writing

    Args:
        df (DataFrame): DataFrame
        group : Aggregation column/columns
        fields: Calculation column/columns, on which aggregation function will be applied
        stats: Function/functions applied on fields
        names: Column name/names of new calculated columns

    Returns:
        DataFrame: Aggregated DataFrame by columns "group", with functions defined in "stats" on columns defined in "fields"

    Example:
        'Calculate number of clients by boutique
        calculate(my_dataframe,group=["boutique_name"],fields=["individuid"],stats=["nunique"],names=["nb_of_clients"])

        'Calculate number of clients by boutique, TO, nb of visits
        calculate(my_dataframe,group=["boutique_name","fsh_advisor"],fields=["individuid","price","purchase_date"],stats=["nunique","sum","nunique"],names=["nb_of_clients","Turnover","nb_of_visits])
    """
    # set default names
    if names is None:
        names = fields
    
    table = None
    #calculer pour chaque couple des variables et statistiques 
    #une des limites: ne pas utiliser les mêmes variabels dans groupe et field
    for field, stat in zip(fields, stats):
        v = (
            df.groupby(group)[field]
            .agg(stat)
            .reset_index()
            .rename(columns={field: f"{names[fields.index(field)]}"})
        )

        if table is None:
            table = v
        else:
            table = table.merge(v, on=group, how="left")

    return table


def bar_plot(dataset, by, y):
    
    ''' 
    Affiche les bar plots pour les questions d'analyse des données exploratoire
    
    Args:
        dataset(df): la table à utiliser
        by (str) : l'axe des x
        y (str) : l'axe des y 
    
    '''
    
    
    #on Définit le graphique
    d = plt.figure()
    plt.bar(dataset[by], dataset[y], color="skyblue")

    plt.xlabel(by)
    plt.ylabel(y)
    plt.title(f"{y} by {by}")
    plt.xticks(rotation=90)
    
    

    return d

#définition de la fontion qui nous permet d'obtenir un token d'accès afin de nous connecter à l'API de Spotify

def get_access_token(client_id, client_secret):
    # Encodage le client_id et le client_secret en base64
    client_creds = f"{client_id}:{client_secret}"
    client_creds_b64 = base64.b64encode(client_creds.encode())
    
    # Définition de l'URL du token et des headers
    token_url = "https://accounts.spotify.com/api/token"
    token_headers = {
        "Authorization": f"Basic {client_creds_b64.decode()}"
    }
    
    # Définition des données du corps de la requête
    token_data = {
        "grant_type": "client_credentials"
    }
    
    # Faisons la requête POST pour obtenir le token
    r = requests.post(token_url, headers=token_headers, data=token_data)
    
    # Vérification du succès de la requête
    if r.status_code not in range(200, 299):
        raise Exception("On n'arrive pas à authentifier le client.")
    
    # Récupération du token d'accès à partir de la réponse
    token_response_data = r.json()
    access_token = token_response_data['access_token']
    
    return access_token






#definition de la fonction qui nous permettra d'obtenir l'id de la chanson sur la plateforme
def get_track_id(track_name, artist_name, token):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
    }

    params = (
        ('q', f'track:{track_name} artist:{artist_name}'),
        ('type', 'track'),
    )

    response = requests.get('https://api.spotify.com/v1/search', headers=headers, params=params)
    response_json = response.json()
    
    tracksi = response_json['tracks']['items']
    
    if tracksi:
        # Retour de l'ID de la première piste trouvée
        return tracksi[0]['id']
    else:
        return None

#definition de la fonction qui retourne le lien web de la chanson sur spotify
def get_track_url(track_id):
    return f"https://open.spotify.com/track/{track_id}"