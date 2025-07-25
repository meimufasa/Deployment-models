import streamlit as st
import pandas as pd
import pickle

with open('pipe.pkl', 'rb') as f:
    pipe = pickle.load(f)

st.set_page_config(page_title="EV Range Estimator", layout="wide")

# Custom styling (Dark theme with neon blue highlights)
st.markdown("""
    <style>
        html, body, [class*="css"] {
            background-color: #121212 !important;
            color: #f0f0f0;
            font-family: 'Segoe UI', sans-serif;
        }
        .main-title {
            font-size: 3em;
            color: #00e6e6;
            text-align: center;
            margin-bottom: 0.3em;
            font-weight: bold;
        }
        .sub-title {
            text-align: center;
            font-size: 1.2em;
            color: #aaaaaa;
            margin-bottom: 2em;
        }
        .custom-card {
            background: linear-gradient(145deg, #1e1e1e, #292929);
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0 0 12px rgba(0, 230, 230, 0.15);
            transition: all 0.3s ease-in-out;
        }
        .custom-card:hover {
            box-shadow: 0 0 25px rgba(0, 230, 230, 0.4);
            transform: translateY(-5px);
        }
        .car-header {
            font-size: 1.1em;
            font-weight: 600;
            color: #00e6e6;
            margin-bottom: 0.5em;
        }
        .car-spec {
            font-size: 0.9em;
            color: #cccccc;
        }
        .range-value {
            font-size: 1.4em;
            color: #03fc8c;
            font-weight: bold;
            margin-top: 10px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-title">EV Range Estimator</div>
<div class="sub-title">Precision Meets Performance in Every Drive.</div>
""", unsafe_allow_html=True)

# Display Samples
sample_cars = pd.DataFrame([
    {'model': 'Mazda MX-30','brand': 'Mazda','car_body_type': 'SUV','drivetrain': 'FWD','segment': 'C - Medium','top_speed_kmh': 140,'battery_capacity_kWh': 35.5,'torque_nm': 270,'efficiency_wh_per_km': 160,'acceleration_0_100_s': 9.7,'seats': 5,'length_mm': 4395,'width_mm': 1795,'height_mm': 1555},
    {'model': 'Mini Cooper SE','brand': 'Mini','car_body_type': 'Hatchback','drivetrain': 'FWD','segment': 'B - Compact','top_speed_kmh': 150,'battery_capacity_kWh': 32.6,'torque_nm': 270,'efficiency_wh_per_km': 145,'acceleration_0_100_s': 7.3,'seats': 4,'length_mm': 3850,'width_mm': 1727,'height_mm': 1432},
    {'model': 'Honda e','brand': 'Honda','car_body_type': 'Hatchback','drivetrain': 'RWD','segment': 'A - Mini','top_speed_kmh': 145,'battery_capacity_kWh': 35.5,'torque_nm': 315,'efficiency_wh_per_km': 180,'acceleration_0_100_s': 8.3,'seats': 4,'length_mm': 3895,'width_mm': 1750,'height_mm': 1495}
])

st.markdown("""<h4 style='margin-top: 30px;'>🚗 Explore Sample EV Predictions</h4>""", unsafe_allow_html=True)
cols = st.columns(3)
for idx, row in sample_cars.iterrows():
    prediction = pipe.predict(pd.DataFrame([row]))[0]
    with cols[idx % 3]:
        st.markdown(f"""
            <div class='custom-card'>
                <div class='car-header'>{row['model']}</div>
                <div class='car-spec'>Body: {row['car_body_type']} | {row['segment']}</div>
                <div class='car-spec'>Battery: {row['battery_capacity_kWh']} kWh | Efficiency: {row['efficiency_wh_per_km']} Wh/km</div>
                <div class='car-spec'>0–100 km/h: {row['acceleration_0_100_s']}s | Seats: {row['seats']}</div>
                <div class='range-value'>{prediction:.0f} km</div>
            </div>
        """, unsafe_allow_html=True)

st.markdown("""<h4 style='margin-top: 40px;'>🛠 Customize Your EV</h4>""", unsafe_allow_html=True)
with st.form("predict_form"):
    col1, col2 = st.columns(2)
    with col1:
        brand = st.text_input("Brand", "Audi")
        model = st.text_input("Model", "e-tron GT")
        car_body_type = st.selectbox("Car Body Type", ["SUV", "Hatchback", "Sedan"])
        drivetrain = st.selectbox("Drivetrain", ["FWD", "RWD", "AWD"])
        segment = st.selectbox("Segment", ['A - Mini', 'B - Compact', 'C - Medium'])
    with col2:
        top_speed_kmh = st.number_input("Top Speed (km/h)", 100, 350, 200)
        battery_capacity_kWh = st.number_input("Battery Capacity (kWh)", 10.0, 150.0, 60.0)
        torque_nm = st.number_input("Torque (Nm)", 50, 1200, 400)
        efficiency_wh_per_km = st.number_input("Efficiency (Wh/km)", 100, 250, 140)
        acceleration_0_100_s = st.number_input("0–100 km/h (s)", 2.0, 20.0, 4.0)
        seats = st.slider("Seats", 2, 7, 2)
        length_mm = st.number_input("Length (mm)", 3000, 5500, 4600)
        width_mm = st.number_input("Width (mm)", 1500, 2500, 2000)
        height_mm = st.number_input("Height (mm)", 1200, 2000, 1300)

    submitted = st.form_submit_button("Predict Range")
    if submitted:
        new_data = pd.DataFrame([{
            'model': model,
            'brand': brand,
            'car_body_type': car_body_type,
            'drivetrain': drivetrain,
            'segment': segment,
            'top_speed_kmh': top_speed_kmh,
            'battery_capacity_kWh': battery_capacity_kWh,
            'torque_nm': torque_nm,
            'efficiency_wh_per_km': efficiency_wh_per_km,
            'acceleration_0_100_s': acceleration_0_100_s,
            'seats': seats,
            'length_mm': length_mm,
            'width_mm': width_mm,
            'height_mm': height_mm
        }])

        try:
            pred = pipe.predict(new_data)[0]
            st.success(f"🏁 Estimated Range: {pred:.2f} km")
        except Exception as e:
            st.error(f"Prediction failed: {e}")
