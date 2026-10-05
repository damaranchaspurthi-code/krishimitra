import streamlit as st
import requests
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

# Gemini
key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=key) if key else None

st.set_page_config(page_title="KrishiMitra", page_icon="🌾")

st.title("🌾 KrishiMitra")
st.write("AI-Powered Farmer Assistance Platform")

choice = st.selectbox(
    "Choose an option",
    ["🤖 AI Advice", "🌦️ Weather", "📊 Farm Data"]
)

# -------- AI ADVICE --------
if choice == "🤖 AI Advice":

    crop = st.selectbox(
        "Select Crop",
        ["Rice", "Wheat", "Cotton", "Tomato", "Chilli", "Other"]
    )

    problem = st.selectbox(
        "Select Problem",
        ["Disease", "Water", "Fertilizer", "Pests", "General Advice"]
    )

    question = st.text_area("Describe your problem")

    image = st.file_uploader(
        "Upload crop image (optional)",
        type=["jpg", "jpeg", "png"]
    )

    if st.button("🌱 Get AI Advice"):

        if not key:
            st.error("GEMINI_API_KEY is missing in .env")

        elif not question:
            st.warning("Please describe your problem.")

        else:
            prompt = f"""
            You are KrishiMitra, an agriculture assistant.

            Crop: {crop}
            Problem: {problem}
            Farmer question: {question}

            Give simple and practical farming advice.
            Explain possible causes and safe next steps.
            """

            try:
                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=prompt
                )

                st.success("🌾 AI Advice")
                st.write(response.text)

            except Exception as e:
                st.error("Gemini error: " + str(e))

# -------- WEATHER --------
elif choice == "🌦️ Weather":

    city = st.text_input("Enter your city", "Hyderabad")

    if st.button("Check Weather"):

        geo = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1}
        ).json()

        if "results" in geo:

            lat = geo["results"][0]["latitude"]
            lon = geo["results"][0]["longitude"]

            weather = requests.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": lat,
                    "longitude": lon,
                    "current":
                    "temperature_2m,relative_humidity_2m,precipitation"
                }
            ).json()

            w = weather["current"]

            st.metric("🌡️ Temperature",
                      f'{w["temperature_2m"]} °C')

            st.metric("💧 Humidity",
                      f'{w["relative_humidity_2m"]}%')

            st.metric("🌧️ Rain",
                      f'{w["precipitation"]} mm')

        else:
            st.error("City not found")

# -------- FARM DATA --------
else:

    st.subheader("📊 Farm Dashboard")

    c1, c2, c3 = st.columns(3)

    c1.metric("👨‍🌾 Farmers", "1,250")
    c2.metric("🌾 Crops", "8,420")
    c3.metric("💧 Water Saved", "18%")

    st.subheader("🌾 Crop Production")

    st.bar_chart({
        "Rice": [80],
        "Wheat": [60],
        "Cotton": [45],
        "Tomato": [70]
    })

    st.subheader("🌧️ Rainfall")

    st.line_chart({
        "Rainfall": [20, 35, 25, 50, 40, 65]
    })

st.sidebar.success("🌾 KrishiMitra")
st.sidebar.write("Better Data → Better Decisions")