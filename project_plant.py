import streamlit as st
import plantdef as pf
import pandas as pd

#--------------------------------------------------------------------

def add_plant():
    st.title("Add a new plant to the collection")
    plant_name = st.text_input("Plant name/species: ")
    location = st.text_input("Location in home: ")
    date_acquired = st.date_input("Date acquired: ")
    watering_frequency = st.number_input( "Watering frequency (in days)", min_value=1, step=1, value=1 )
    sunlight_needs = st.selectbox( "Sunlight needs", ["🌥️ Low", "⛅ Medium", "🌤️High"] )
    Weather = st.selectbox( "Weather", ["🌞 Sunny ", "☁️ Cloudy", "🌧️ Rainy" , "🍃 windy"])


    data= pf.load_data("file.csv")
    
    if st.button("Add"):
        if plant_name and location:
            df = pf.add_plant_data(data, plant_name,location, date_acquired, watering_frequency, sunlight_needs, Weather)
            
            df.to_csv("file.csv", index=False)
            st.success(f"'{plant_name}' has been added to your collection.")
        else:
            st.error("Please Fill the Information Above.")
    
#--------------------------------------------------------------------

def record_care():
    st.title("Record a Plant Care Activity")
    data = pf.load_data("file.csv")
    selected_plant = st.selectbox("Select plant", pf.get_plant_names(data))
    activity_performed = st.selectbox( "Activity Performed", ["Watering", "Fertilizing", "Repotting" , "Pruning"] )
    date_acquired = st.date_input("Date acquired: ")
    height_plant = st.number_input( "Enter New Plant Height: ", value=1.0 )
    uploaded_file = st.file_uploader("Upload plant photo", type=["jpg", "png"])

    if st.button("Add Activity"):
        
        care_data = pf.load_data("plantCare.csv")
        
        df = pf.get_record_care_data(care_data, selected_plant, activity_performed, date_acquired, height_plant)
        
        if uploaded_file:
            df.loc[df.index[-1], "Photo"] = uploaded_file.name

        df.to_csv("plantCare.csv", index=False)
        
        st.success(f"Recorded {activity_performed} for {selected_plant}.")

#--------------------------------------------------------------------

def due_for_care():
    st.title("View Plants Due for Care")
    data = pf.load_data("file.csv")
    care_data = pf.load_data("plantCare.csv")
    due_care = pf.get_plant_due_care(data, care_data)
    
    if due_care.empty:
        st.success("No plants are due for care.")
    else:
        st.write(due_care)

#---------------------------------------------------------

def search_plants():
    st.title("Search plants by name or location")
    search_term = st.text_input("Plant name or Location: ")
    data= pf.load_data("file.csv")
    care_data = pf.load_data("plantCare.csv")
    result_search = pf.get_plant_search(data, care_data, search_term)

    if result_search.empty:
        st.error("Not Found.")
    else:
        st.write(result_search)

#---------------------------------------------------------
   
def view_all():
    st.title("All Plants")
    data = pf.load_data("file.csv")
    st.write(data) 
    
#---------------------------------------------------------

def plant_growth():
    st.title("The plant growth")

    data = pf.load_data("file.csv")
    growth_data = pf.load_data("plantCare.csv")

    selected_plant = st.selectbox("Select plant", pf.get_plant_names(data))

    Fillter = growth_data[growth_data["Plant Name"] == selected_plant
    result = Fillter[["Date" , "Height]]

    if result.empty:
        st.error("No growth measurements found for this plant.")
    else:
        st.line_chart(result, x = "Date" , y="Height")

#---------------------------------------------------------

def plant_Weather():
    st.title("Seasonal Plant Care")
    data = pf.load_data("file.csv")
    selected_plant = st.selectbox("Select plant", pf.get_plant_names(data))
    weather = st.selectbox( "Weather", ["🌞 Sunny ", "☁️ Cloudy", "🌧️ Rainy" , "🍃 windy"])

    if st.button("Get Advice"):
        advice = pf.get_season_advice(selected_plant, weather)
        st.write(advice)

        
#---------------------------------------------------------

def Upload_Photo():
    st.title("Dr. Plant is here!")
    uploaded_file = st.file_uploader("Upload images", type=["jpg", "png"])
    
    if uploaded_file:
        st.image(uploaded_file)
        
    data = pf.load_data("file.csv")
    selected_plant = st.selectbox("Select plant", pf.get_plant_names(data))

    if st.button("Ask Dr. Plant for Help"):
        advice = pf.get_Doctor_photo(uploaded_file, selected_plant)
        st.write(advice)

#---------------------------------------------------------

# def plant_api():
#     st.title("Learn About Your Current or Next Plant")

#     plant_name = st.text_input("Enter plant name")

#     if st.button("Search"):
#         result = pf.get_plant_api(plant_name)


#---------------------------------------------------------

add = st.Page(add_plant, title="Add a new plant", icon=":material/add_circle:")
recored = st.Page(record_care, title="Record care activity", icon=":material/content_paste:")
care = st.Page(due_for_care, title="Plants due for care", icon=":material/history:")
search = st.Page(search_plants, title="Search plants", icon=":material/search:")
view = st.Page(view_all, title="View all plants", icon=":material/visibility:")
growth = st.Page(plant_growth, title="Plant Growth", icon=":material/show_chart:")
Weather  = st.Page(plant_Weather, title="Information about Seasons", icon=":material/partly_cloudy_day:")
Dr = st.Page(Upload_Photo, title="Cheak Your Plant", icon=":material/health_and_safety:")
# plant_api = st.Page(plant_api, title="Learn About Your Plant", icon=":material/book:")



pg = st.navigation([add, recored, care, search, view, growth, Weather, Dr], position="sidebar")
pg.run()
