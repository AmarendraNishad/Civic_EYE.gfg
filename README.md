# 🚨 CivicEye — Emergency Corridor Obstruction Sentinel

### Career Catalyst × GeeksforGeeks Hackathon

CivicEye is an AI-powered intelligent traffic surveillance system designed to detect and monitor vehicles obstructing designated emergency corridors.

The system transforms conventional CCTV footage into an intelligent monitoring layer using computer vision, object detection, object tracking, zone analysis, and incident evidence capture.

---

## 🎯 Problem Statement

Emergency vehicles such as ambulances, fire engines, and police vehicles can lose critical time when designated emergency corridors are blocked by traffic.

Traditional CCTV surveillance depends heavily on continuous human monitoring, making it difficult to detect every obstruction quickly and consistently.

CivicEye addresses this problem by automatically analysing CCTV video and identifying vehicles present inside a predefined emergency corridor.

---

## 💡 Our Solution

CivicEye introduces an AI-driven surveillance pipeline that:

- Detects vehicles from CCTV footage.
- Tracks individual vehicles using persistent tracking IDs.
- Defines a configurable emergency corridor using a polygonal zone.
- Monitors vehicle presence inside the designated zone.
- Calculates vehicle dwell time.
- Generates an obstruction alert when the configured threshold is exceeded.
- Captures visual evidence of detected incidents.
- Maintains structured incident records for further analysis.

The goal is to convert passive CCTV infrastructure into a proactive emergency-corridor monitoring system.

---

## 🧠 How CivicEye Works

```text
CCTV / Traffic Video
        ↓
YOLOv8 Vehicle Detection
        ↓
ByteTrack Object Tracking
        ↓
Vehicle ID Assignment
        ↓
Emergency Corridor Zone Analysis
        ↓
Vehicle Dwell-Time Monitoring
        ↓
Obstruction Detection
        ↓
🚨 Alert Generation
        ↓
📸 Incident Snapshot
        ↓
📋 Incident Logging