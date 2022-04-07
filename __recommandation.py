from sklearn import tree
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import json

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

    # favorites_types1 = [val['favorites_types'][0][0] if len(val['favorites_types']) > 1 else None for val in user_data]
    # favorites_types2 = [val['favorites_types'][1][0] if len(val['favorites_types']) > 1 else None for val in user_data]
    
    # dislikes_types1 = [val['disliked_types'][0] if len(val['disliked_types']) > 1 else None for val in user_data]
    # dislikes_types2 = [val['dislikes_types'][1] if len(val['dislikes_types']) > 1 else None for val in user_data]

    # df_u = df_u[df_u.columns[~df_u.columns.isin(['favorites_types', 'disliked_types'])]]
    # df_u['favorites_type1'] = favorites_types1
    # df_u['favorites_type2'] = favorites_types2
    # df_u['dislikes_types1'] = dislikes_types1 
    # df_u['dislikes_types2'] = dislikes_types2



le1 = LabelEncoder()
df_images['colors1'] = le1.fit_transform(df_images['colors1'])
df_images['colors2'] = le1.fit_transform(df_images['colors2'])

le2 = LabelEncoder()
df_images['colors_closet1'] = le2.fit_transform(df_images['colors_closet1'])
df_images['colors_closet2'] = le2.fit_transform(df_images['colors_closet2'])

le3 = LabelEncoder()
df_images['properties.type2'] = le3.fit_transform(df_images['properties.type2'])
df_images['properties.type1'] = le3.fit_transform(df_images['properties.type1'])

train = df_images[:650]
test = df_images[650:]
# print(len(train) , len(test))

dtc = tree.DecisionTreeClassifier()

fitted_models = []

def randomDf():
    df = pd.DataFrame()
    for i in range(8):
        df = pd.concat([df, df_images.sample()], ignore_index = True, axis = 0)
    return df

label_likes = LabelEncoder()
for index, row in df_u.iterrows():
    fits = dtc.fit(randomDf(), label_likes.fit_transform(row['favorites']))
    prediction = fits.predict(test)
    print(df_test.iloc[label_likes.inverse_transform(prediction.reshape(-1, 1))])