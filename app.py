import streamlit as st
import pandas as pd
from model import detect_attacks
from utils import get_location
import folium
from streamlit_folium import st_folium


st.set_page_config(
    page_title="Firewall Attack Location Tracker",
    layout="wide"
)

st.title("🛡️ Firewall Attack Location Tracker")
st.write(
    "This project detects suspicious firewall activity "
    "and shows approximate attacker location using IP information."
)


uploaded_file = st.file_uploader(
    "Upload Firewall Log CSV",
    type=["csv"]
)


if uploaded_file:

    data = pd.read_csv(uploaded_file)

    st.subheader("Firewall Logs")
    st.dataframe(data)


    suspicious = detect_attacks(data)


    st.subheader("🚨 Suspicious Activities")

    if len(suspicious) == 0:
        st.success("No suspicious activity detected")

    else:
        st.dataframe(suspicious)


        locations = []

        for ip in suspicious["ip"].unique():

            info = get_location(ip)

            locations.append(info)


        location_df = pd.DataFrame(locations)


        st.subheader("🌍 IP Location Details")
        st.dataframe(location_df)


        if not location_df.empty:

            map_center = [
                location_df["lat"].mean(),
                location_df["lon"].mean()
            ]


            firewall_map = folium.Map(
                location=map_center,
                zoom_start=3
            )


            for _, row in location_df.iterrows():

                folium.Marker(
                    [
                        row["lat"],
                        row["lon"]
                    ],
                    popup=(
                        f"IP: {row['ip']}<br>"
                        f"Country: {row['country']}<br>"
                        f"City: {row['city']}"
                    )
                ).add_to(firewall_map)


            st.subheader("📍 Attack Location Map")

            st_folium(
                firewall_map,
                width=900,
                height=500
            )

else:
    st.info("Upload firewall log CSV file to start detection.")
