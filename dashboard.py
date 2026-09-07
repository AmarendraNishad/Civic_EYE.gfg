import streamlit as st
import cv2
import time
import numpy as np
import os
from ultralytics import YOLO

# =========================================================
# CIVICEYE CONFIGURATION
# =========================================================

MODEL_PATH = "models/yolov8n.pt"
VIDEO_PATH = "videos/traffic.mp4"
INCIDENT_DIR = "incidents"

THRESHOLD_SECONDS = 5.0

os.makedirs(INCIDENT_DIR, exist_ok=True)

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="CivicEye",
    page_icon="🚨",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main-title {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 0;
}

.subtitle {
    font-size: 18px;
    color: #777;
    margin-bottom: 25px;
}

.metric-card {
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #ddd;
    text-align: center;
}

.alert-box {
    padding: 18px;
    border-radius: 10px;
    background-color: #ffe5e5;
    border: 2px solid #ff3333;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🚨 CivicEye</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Emergency Corridor Obstruction Sentinel'
    '</div>',
    unsafe_allow_html=True
)

st.divider()

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("⚙️ Control Panel")

threshold = st.sidebar.slider(
    "Obstruction Threshold (seconds)",
    min_value=3,
    max_value=10,
    value=5
)

st.sidebar.info(
    "CivicEye monitors vehicles entering "
    "the emergency corridor and raises an "
    "alert when the obstruction exceeds "
    "the configured threshold."
)

start_button = st.sidebar.button(
    "▶ Start Monitoring",
    use_container_width=True
)

# =========================================================
# DASHBOARD METRICS
# =========================================================

metric1, metric2, metric3, metric4 = st.columns(4)

vehicle_metric = metric1.empty()
zone_metric = metric2.empty()
alert_metric = metric3.empty()
status_metric = metric4.empty()

vehicle_metric.metric(
    "🚗 Vehicles Detected",
    "0"
)

zone_metric.metric(
    "🟨 Vehicles in Zone",
    "0"
)

alert_metric.metric(
    "🚨 Critical Alerts",
    "0"
)

status_metric.metric(
    "🟢 System Status",
    "READY"
)

st.divider()

# =========================================================
# VIDEO AREA
# =========================================================