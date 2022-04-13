from sklearn import tree
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import json
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.image as mpimg

with open('images/metadata/metadata.json') as meta:
    meta_data = json.load(meta)
    colors_closet1 = [val['closest_colors'][0] if len(val['closest_colors']) > 1 else None for val in meta_data]
    colors_closet2 = [val['closest_colors'][1] if len(val['closest_colors']) > 1 else None for val in meta_data]

    colors1 = [val['colors'][0] if len(val['colors']) > 1 else None for val in meta_data]
    colors2 = [val['colors'][1] if len(val['colors']) > 1 else None for val in meta_data]

    df_images = pd.json_normalize(
    meta_data,  
        meta=[
            'class',
            ['properties', 'type1', 'types2'], 
        ]
    )   
    df_test = pd.json_normalize(
    meta_data,  
        meta=[
            'class',
            ['properties', 'type1', 'types2'], 
        ]
    )   
    df_images = df_images[df_images.columns[~df_images.columns.isin(['size', 'id','properties.name', 'tags', 'path', 'colors', 'closest_colors'])]]
    df_images['colors1'] = colors1
    df_images['colors2'] = colors2
    df_images['colors_closet1'] = colors_closet1
    df_images['colors_closet2'] = colors_closet2

with open('images/metadata/users_preferences.json') as user_metadata:
    user_data = json.load(user_metadata)
    df_u = pd.json_normalize(user_data)

le1 = LabelEncoder()
df_images['colors1'] = le1.fit_transform(df_images['colors1'])
df_images['colors2'] = le1.fit_transform(df_images['colors2'])

le2 = LabelEncoder()
df_images['colors_closet1'] = le2.fit_transform(df_images['colors_closet1'])
df_images['colors_closet2'] = le2.fit_transform(df_images['colors_closet2'])

le3 = LabelEncoder()
df_images['properties.type2'] = le3.fit_transform(df_images['properties.type2'])
df_images['properties.type1'] = le3.fit_transform(df_images['properties.type1'])


"""Separate data for train set and test set"""
train = df_images[:650]
test = df_images[650:]

dtc = tree.DecisionTreeClassifier()

fitted_models = []

def randomDf():
    df = pd.DataFrame()
    for i in range(8):
        df = pd.concat([df, train.sample()], ignore_index = True, axis = 0)
    return df

label_likes = LabelEncoder()
users_preferences = {}
for index, row in df_u.iterrows():
    fits = dtc.fit(randomDf(), label_likes.fit_transform(row['favorites']))
    prediction = fits.predict(test)
    users_preferences[index] = df_test.iloc[label_likes.inverse_transform(prediction.reshape(-1, 1))]


users_ids = []
def users_images():
    for index in range(8):
        # ax.set_title(f"User {index} and image favorites id :{list(users_preferences[index].sample()['id'].items())[0][1]}")
        random_favorite = np.random.choice(df_u.iloc[index]['favorites'], size=1)
        favorite = random_favorite.tolist().pop(0)
        recommanded =  list(users_preferences[index].sample()['id']).pop(0)
        users_ids.append(favorite)
        users_ids.append(recommanded)

users_images()

fig , axs = plt.subplots(8,2, figsize=(8, 8))
fig.suptitle("Each row is a user and left image is favorite and right is a recommanded")
axs = axs.flatten()
def plot_users(plot):
    for index, ax in enumerate(plot):
        ax.set_title(f"Image number : {users_ids[index]}")
        img = mpimg.imread(df_test.iloc[users_ids[index]]['path'])
        ax.imshow(img)
    plt.show()
plot_users(axs)

for i in range(8):
    print("User number :",i," with a random recommanded image : \n")
    print(users_preferences[i].sample())
    print('\nFavorites types, color and image for this user : \n')
    print(df_u.iloc[i]['favorites_types'])
    print(df_u.iloc[i]['colors'])
    print(df_u.iloc[i]['favorites'])
    print('\n\n')