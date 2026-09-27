import streamlit as st
from streamlit_geolocation import streamlit_geolocation
import math


BUILDING_LAT = 34.0965
BUILDING_LON = 74.8237
RADIUS = 100

 # before salifs function of check-in is called this will be called first
def check_location():

    location = streamlit_geolocation()

    if not location:
        return False

    latitude = location.get("latitude")
    longitude = location.get("longitude")

    if latitude is None or longitude is None:

        st.warning("Unable to get your location.")

        return False


    # Calculate distance

    R = 6371000

    lat1 = math.radians(BUILDING_LAT)
    lat2 = math.radians(latitude)

    dlat = math.radians(latitude - BUILDING_LAT)
    dlon = math.radians(longitude - BUILDING_LON)

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(dlon / 2) ** 2
    )

    distance = (
        R
        * 2
        * math.atan2(
            math.sqrt(a),
            math.sqrt(1 - a)
        )
    )


    if distance <= RADIUS:

        st.success(
            f"Location verified. "
            f"Distance: {distance:.1f} meters."
        )

        return True

    else:

        st.error(
            f"Check-in denied. "
            f"You are {distance:.1f} meters away."
        )

        return False
check_location()    