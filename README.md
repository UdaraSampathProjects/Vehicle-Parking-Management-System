# VAUED_Assignment2

# 🚗 Vehicle Parking Management System - VAUED Assignment 2
 
This project is a containerized Vehicle Parking Management System built for the VAUED module. It demonstrates how modern web applications can integrate observability using Prometheus and Grafana, while also being fully portable through Docker-based deployments.
 
---
 
## 📌 Overview
 
The system allows users to:

- Register, update, and delete vehicles

- Assign and release parking slots

- Log entry/exit times and durations

- Monitor application metrics in real time

- Visualize performance through Grafana dashboards

- Set up alerting rules for key metrics
 
---
 
## 🛠️ Technologies Used
 
- **Flask** – Web service framework

- **Prometheus** – Metrics collection and alerting

- **Grafana** – Dashboard visualization

- **Docker** – Containerization and deployment

- **Python** – Core programming language
 
---
 
## 🧪 Key Features
 
- RESTful API for vehicle and parking slot management

- Prometheus metrics for entries, exits, parking durations, and slot usage

- Grafana dashboard with real-time data visualizations

- Alerts for specific conditions (e.g., full occupancy)

- Dockerized setup for easy deployment and scalability
 
---
 
## 📦 Deployment
 
All services are containerized with Docker:
 
1. **Flask API** – Exposes endpoints and metrics on port `8000`

2. **Prometheus** – Scrapes metrics and runs on port `9090`

3. **Grafana** – Displays dashboards on port `3000`
 
---
 
## 📊 Observability
 
- Metrics are exposed via `/metrics` endpoint

- Prometheus scrapes data periodically

- Grafana displays metrics such as:

  - Total vehicle entries and exits

  - Occupied and free parking slots

  - Time series of parking trends

  - Distribution of parking durations
 
---
 
## 📁 Repository Contents
 
- `app.py` – Flask application with metrics

- `Dockerfile` – Builds the Flask app image

- `prometheus.yml` – Scrape configuration for Prometheus

- `requirements.txt` – Python dependencies

- `README.md` – Project documentation
 
---
 
## 📈 Dashboard Visuals (Examples)
 
- Total Vehicle Entries (Stat)

- Slot Occupancy (Bar Gauge)

- Parking Duration (Histogram)

- Entry/Exit Rates (Time Series)

- Free vs Occupied Slots (Donut/Stat)
 
---
 
## ✅ Assignment Tasks Covered
 
- [x] Implement web service and Prometheus exporter

- [x] Deploy services using Docker

- [x] Set up and configure Prometheus

- [x] Build Grafana dashboard with 5+ visualizations

- [x] Set up alerting for critical metrics
 
---



 
