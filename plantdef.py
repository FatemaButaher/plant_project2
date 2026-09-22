import pandas as pd 
import datetime
from openai import OpenAI
import requests
import streamlit as st

def load_data(path):
    df = pd.read_csv(path)
    return df

#---------------------------------------------------------

def get_plant_names(df):
    return df["Plant Name"].tolist()

#---------------------------------------------------------

def add_plant_data(df, plant_name, location, date_acquired, watering_frequency, sunlight_needs, Weather):
    dataframe = pd.DataFrame([{'Plant Name': plant_name, 'Location': location, 'Date Acquired': date_acquired, "Watering Frequency (days)":watering_frequency, "Sunlight Needs" : sunlight_needs, "Weather": Weather}])

    df = pd.concat([df, dataframe], ignore_index=True)
    return df

#---------------------------------------------------------
        
def get_record_care_data(df, selected_plant, activity_performed, date_acquired, height_plant):
    
    new_activity = pd.DataFrame([{ "Plant Name": selected_plant, "Activity": activity_performed, "Date": date_acquired, "Height" : height_plant}])
    
    df = pd.concat([df, new_activity], ignore_index=True)

    return df
    

#---------------------------------------------------------

def get_plant_due_care(df, care_data):
    today_date = pd.to_datetime(datetime.date.today())

    care_data = care_data[care_data["Activity"] == "Watering"].copy()
    care_data["Date"] = pd.to_datetime(care_data["Date"], format="mixed")

    care_data = care_data.sort_values("Date")
    last_care = care_data.drop_duplicates("Plant Name", keep="last")

    due_care_table = pd.merge(df, last_care[["Plant Name", "Date"]], on="Plant Name")

    difference = (today_date - due_care_table["Date"]).dt.days

    return due_care_table[ difference >= due_care_table["Watering Frequency (days)"]]
    
#---------------------------------------------------------

def get_plant_search(df, care_data, search_term): 
    due_care_table = pd.merge(df , care_data, on="Plant Name")
    name_search = due_care_table["Plant Name"].str.lower().str.contains(search_term.lower())
    location_search = due_care_table["Location"].str.lower().str.contains(search_term.lower())

    return due_care_table[name_search | location_search]

#---------------------------------------------------------

def get_plant_growth(PlantGrowth, selected_plant):
    PlantGrowth = PlantGrowth[PlantGrowth["Plant Name"] == selected_plant].copy()
    PlantGrowth["Date"] = pd.to_datetime(PlantGrowth["Date"],format="mixed")
    PlantGrowth = PlantGrowth.sort_values("Date")

    return PlantGrowth

#---------------------------------------------------------

client = OpenAI(
    base_url= "https://openrouter.ai/api/v1",
    api_key= st.secrets["API_KEY"]
)

def get_LLM(prompt): 
    completion = client.chat.completions.create(
        model= "dots-studio/dots-3-note-preview:free",
        messages=[
            {
                "role": "system",
                "content": "You are a Ai plant doctor care assistant. Give simple, practical, and helpful plant care advice.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.0,
    )

    response = completion.choices[0].message.content
    return response

#---------------------------------------------------------

def get_season_advice(plant_name, weather):
    prompt = f"The plant is {plant_name}, The season is {weather}. Give practical plant care advice for this season. Include advice about watering, sunlight, fertilizing, and general plant care. Keep the advice short and easy to understand and make small care 'schedules'."

    return get_LLM(prompt)


#---------------------------------------------------------

def get_Doctor_photo(photo, plant_name):
    prompt = f"The plant is {plant_name}, and photo is{photo} say if sick or its going good, be the doctor and say what should do to recover her health if its needed, and ask for new photo after fue days to To check on her."

    return get_LLM(prompt)

#---------------------------------------------------------

# def get_plant_api(plant_name):
# url = "https://house-plants2.p.rapidapi.com/search"

# querystring = {"query":"Fern"}

# headers = {
# 	"x-rapidapi-key": "e131f86474msh8c07893796cfc8bp16c838jsn677236a27381",
# 	"x-rapidapi-host": "house-plants2.p.rapidapi.com",
# 	"Content-Type": "application/json"
# }

# response = requests.get(url, headers=headers, params=querystring)

# print(response.json())
