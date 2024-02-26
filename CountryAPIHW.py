import requests
import pandas as pd
import os

country_name = input("Enter country Name: ")
filename = "myOutput.json"

def get_country_info(name):
    url = f"https://restcountries.com/v3.1/name/{name}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return None


country_info = get_country_info(country_name)
file_exists = os.path.exists(filename)
if(file_exists):
    df = pd.read_json('myOutput.json')
else:
    df = pd.DataFrame({'name':[], 'capital':[], 'population':[]})


if country_info:
    if len(country_info) == 1:
        print("There is 1 result:")
    elif len(country_info) > 1:
        print("There are", len(country_info), "results:")
    for i in range(0, len(country_info)):
        if 'capital' in country_info[i]:
            print(country_info[i]['name']['common'], "with a capital city of", country_info[i]['capital'][0], "has a population of", country_info[i]['population'])
            exists = False
            for index, row in df.iterrows():
                if(row['name'] == country_info[i]['name']['common']):
                    exists = True
            if(not exists):
                df.loc[len(df.index)] = [country_info[i]['name']['common'], country_info[i]['capital'][0], country_info[i]['population']]
        else:
            print(country_info[i]['name']['common'], "(No capital city)", "has a population of", country_info[i]['population'])
            exists = False
            for index, row in df.iterrows():
                if(row['name'] == country_info[i]['name']['common']):
                    exists = True
            if(not exists):
                df.loc[len(df.index)] = [country_info[i]['name']['common'], None, country_info[i]['population']]
    df.to_json(filename, orient='records', indent=4)
else:
    print("Failed to fetch country information. Please enter a valid country")
