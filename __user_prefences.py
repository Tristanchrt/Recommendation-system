import random
import json
import numpy as np

with open("images/metadata/metadata.json", 'r') as images_infos:
    images_infos = json.load(images_infos)
    print(images_infos[0])
users_preferences = []

number_of_users = 10
for user_id in range(number_of_users):
    favorites_index = random.sample(range(1,len(images_infos)), 8)
    dislike_index = random.choices([i for i in range(1, len(images_infos)) if i not in favorites_index], k=8)

    favorites_colors = [images_infos[index]["closest_colors"] for index in favorites_index if len(images_infos[index]["closest_colors"])]

    favorites_types = [[images_infos[index]["properties"]["type1"], images_infos[index]["properties"]["type2"]] for index in favorites_index]
    disliked_types = [[images_infos[index]["properties"]["type1"], images_infos[index]["properties"]["type2"]] for index in dislike_index]
    user_metadata = {
        "id" : user_id +1,
        "favorites" : favorites_index,
        "dislikes" : dislike_index,
        "favorites_types" : list(set(tuple(el) for el in favorites_types)),
        "disliked_types" : list(set(tuple(el) for el in disliked_types)),
        "colors" : list(set(np.array(favorites_colors).ravel()))
    }
    users_preferences.append(user_metadata)
with open("images/metadata/users_preferences.json", 'w+') as outfile:
    outfile.write(json.dumps(users_preferences))