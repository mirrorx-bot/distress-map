import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap, MarkerCluster
from streamlit_folium import folium_static

# Load the CSV file
csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRYSUOh5kElFlNoJb7j8f1gNMBs6m76JSj0nAknc6vomY5JkCBsVVLPr4kBu6J03__pH0rJsuVkoYOO/pub?output=csv"
df = pd.read_csv(csv_url)

# Set up page configuration for a fullscreen experience
st.set_page_config(layout="wide")

# Layout split into two columns: 1 for sidebar, 1 for map
col1, col2 = st.columns([1, 4])  # Left (col1) is 1 part, right (col2) is 4 parts

with col1:
    # Sidebar section for layers and title
    st.title('Distress Points Map')
    layer = st.selectbox(
        'Select layer',
        ['All Distresses', 'By Severity', 'Distress Heatmap', 'Distress Type Clustering']
    )

    # Footer with copyright text at the bottom of the sidebar
    st.markdown("<br><br><br><br><br><br><br>", unsafe_allow_html=True)  # Spacer for alignment
    st.markdown("---")
    st.markdown("© **Bipul Dey**, Department of Urban & Regional Planning, RUET, 2024.",)

# Initialize the map at the center of the coordinates
center_lat = df['latitude_y'].mean()
center_lon = df['longitude_'].mean()
m = folium.Map(location=[center_lat, center_lon], zoom_start=10)

# Function to create popups with image and distress information
def create_popup(row):
    html = f"""
    <b>Distress Type:</b> {row['Distress_Type']}<br>
    <b>Distress Level:</b> {row['Distress_Level']}<br>
    <b>Severity:</b> {row['Severity']}<br>
    <iframe src="{row['File_URL']}" width="200px"></iframe><br>
    <b>Date and Time:</b> {row['DateTime_1']}
    """
    return folium.Popup(folium.IFrame(html, width=300, height=300))

# Layer: All Distresses
if layer == 'All Distresses':
    for _, row in df.iterrows():
        folium.Marker(
            location=[row['latitude_y'], row['longitude_']],
            popup=create_popup(row),
            icon=folium.Icon(color='red' if row['Severity'] == 'High' else 
                            ('orange' if row['Severity'] == 'Medium' else 'green'))
        ).add_to(m)

# Layer: By Severity
elif layer == 'By Severity':
    severity = st.selectbox('Select severity', df['Severity'].unique())
    filtered_df = df[df['Severity'] == severity]
    
    for _, row in filtered_df.iterrows():
        folium.Marker(
            location=[row['latitude_y'], row['longitude_']],
            popup=create_popup(row),
            icon=folium.Icon(color='red' if row['Severity'] == 'High' else 
                            ('orange' if row['Severity'] == 'Medium' else 'green'))
        ).add_to(m)

# Layer: Distress Heatmap
elif layer == 'Distress Heatmap':
    heat_data = [[row['latitude_y'], row['longitude_']] for index, row in df.iterrows()]
    HeatMap(heat_data).add_to(m)

# Layer: Distress Type Clustering
elif layer == 'Distress Type Clustering':
    marker_cluster = MarkerCluster().add_to(m)
    for _, row in df.iterrows():
        folium.Marker(
            location=[row['latitude_y'], row['longitude_']],
            popup=create_popup(row),
            icon=folium.Icon(color='red' if row['Severity'] == 'High' else 
                            ('orange' if row['Severity'] == 'Medium' else 'green'))
        ).add_to(marker_cluster)

# Display the map in Streamlit (using the second column for the map)
with col2:
    folium_static(m, width=1400, height=700)  # Make map large within the second column
