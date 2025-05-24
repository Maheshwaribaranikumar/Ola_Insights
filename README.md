# 🚕 OLA Data Insights Dashboard

An interactive dashboard built with Streamlit to analyze and visualize ride booking data from OLA Cabs. This project provides insights into booking patterns, cancellations, payment methods, and customer behavior using SQL queries, visual charts, and metrics.

---

## 📚 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [Use Cases](#-use-cases-included)
- [Screenshots](#-screenshots)
- [Author](#-author)
- [License](#-license)

---

## 📝 Overview

This project uses data from the OLA ride-hailing platform to explore a variety of business and operational insights. The data comes from an Excel sheet and is converted into a SQLite database. The dashboard allows users to interactively explore predefined queries like cancellations, ratings, payment methods, and booking statuses.

It is a great tool for data-driven decision-making, performance tracking, and user behavior analysis.

---

## ✨ Features

- Load and convert Excel data into SQLite
- Interactive Streamlit interface with sidebar navigation
- 10 use case queries with dynamic visualizations
- Visual summaries using bar charts, pie charts, and metrics
- SQL-powered queries behind the scenes
- Analyze ride patterns by vehicle type, status, and customer feedback

---

## 🛠 Tech Stack

| Component     | Purpose                              |
|---------------|--------------------------------------|
| Python        | Core language                        |
| Streamlit     | UI and interactivity                 |
| SQLite        | Lightweight database                 |
| pandas        | Data manipulation                    |
| plotly.express| Data visualizations                  |
| openpyxl      | Excel file support                   |

---

## 🗂 Project Structure

ola-insights-project/
├── load_ola_data.py # Main Streamlit app with SQL logic
├── olaeda.ipynb # Jupyter Notebook for EDA (optional)
├── OLA_DataSet.xlsx # Raw data source (Excel)
├── ola_data.db # Generated SQLite database
├── requirements.txt # Python dependencies
├── README.md # Project documentation
├── .gitignore # Files to exclude from Git
└── images/ # Screenshots for documentation
