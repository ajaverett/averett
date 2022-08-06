#%%
import pandas as pd
import zipfile
import kaggle
from kaggle.api.kaggle_api_extended import KaggleApi

#%%
api = KaggleApi()
api.authenticate() 

#%%
api.dataset_download_file('andreuvallhernndez/myanimelist-jikan','characters.csv')
with zipfile.ZipFile('characters.csv.zip','r') as zipref:\
    zipref.extractall()

#%%
api.dataset_download_file('andreuvallhernndez/myanimelist','anime.csv')
with zipfile.ZipFile('anime.csv.zip','r') as zipref:\
    zipref.extractall()

#%%
anime = pd.read_csv('anime.csv')
anime.query('scored_by >= 1000 and episodes > 2').sort_values(by=['score'], ascending=True)
anime['start'] = pd.to_datetime(anime['airing_from'], infer_datetime_format=True)
new_best_anime = (anime
    .query('scored_by >= 1000 and episodes > 2 and start > "2019-01-01 00:00:00"')
    .sort_values(by=['score'], ascending=False)
    .head(12)
)

#%%
new_best_anime 
char = pd.read_csv('characters.csv')
test = char['about'].head(20).reset_index()
pattern = '|'.join(['January', 'February', 'March', 'April', 'May', 'June', 'July','August', 'September', 'October', 'November', 'December'])

test['about'].str.findall(r'({}).[0-9]+'.format(pattern))
list = test['about'].str.findall(r'(January|February|March|April|May|June|July|August|September|October|November|December).([0-9][0-9])?').reset_index()

list2 = pd.DataFrame(list['about'].to_list())[0]

#%%
list_of_lists = [['aa', 'bb', 'cc'], ['dd', 'ee', 'ff'], ['gg', 'hh', 'ii']]

flatten_list = []
for s in list_of_lists:
    for i in s:
        flatten_list.append(i)

#%%
def flatten(list):
    for s in list:
        for i in s:
            list.append(i)
    return(list)

test4 = [[1,"n",3],[4,5,6]]

import itertools
flat_list = list(np.concatenate(regular_list).flat)



print(flatten_list)










# %%
