import streamlit as st   # type: ignore
import pandas as pd
import plotly.express as px
import sqlite3
import os

# Load Excel
df = pd.read_excel("C:/Users/mahes/OneDrive/Desktop/OLA2/env/Scripts/OLA_DataSet.xlsx", sheet_name="July")

# Connect to DB
conn = sqlite3.connect("ola_data.db")

# Write DataFrame to SQLite DB
df.to_sql("July", conn, if_exists="replace", index=False)
print("Current working directory:", os.getcwd())

# Sidebar
menu = st.sidebar.radio("Navigation", ['About', 'Use Cases'])

if menu == 'About':
    st.markdown("## <span style='color:green;'>OLA</span>", unsafe_allow_html=True)
    st.markdown(""" 
    Ola Cabs is India’s leading mobility platform and one of the world’s largest ride-hailing companies.  
    The platform offers services ranging from daily ride bookings to luxury travel options through its diverse fleet of vehicles.
    """, unsafe_allow_html=True)

elif menu == 'Use Cases':
    st.markdown("## <span style='color:green;'>Use Cases</span>", unsafe_allow_html=True)
    use_case = st.selectbox("Select a Use Case Query", [
        "1. Retrieve all successful bookings",
        "2. Find the average ride distance for each vehicle type",
        "3. Get the total number of cancelled rides by customers",
        "4. List the top 5 customers who booked the highest number of rides",
        "5. Get the number of rides cancelled by drivers due to personal and car-related issues",
        "6. Find the maximum and minimum driver ratings for Prime Sedan bookings",
        "7. Retrieve all rides where payment was made using UPI",
        "8. Find the average customer rating per vehicle type",
        "9. Calculate the total booking value of rides completed successfully",
        "10. List all incomplete rides along with the reason"
    ])

    use_case_queries = {
        "1. Retrieve all successful bookings": "SELECT * FROM July WHERE Booking_Status = 'Success';",
        "2. Find the average ride distance for each vehicle type": "SELECT Vehicle_Type, AVG(Ride_Distance) AS Avg_Ride_Distance FROM July GROUP BY Vehicle_Type;",
        "3. Get the total number of cancelled rides by customers": "SELECT COUNT(*) AS Total_Cancelled_By_Customers FROM July WHERE Canceled_Rides_by_Customer IS NOT NULL AND Canceled_Rides_by_Customer != '';",
        "4. List the top 5 customers who booked the highest number of rides": "SELECT Customer_ID, COUNT(*) AS Total_Rides FROM July GROUP BY Customer_ID ORDER BY Total_Rides DESC LIMIT 5;",
        "5. Get the number of rides cancelled by drivers due to personal and car-related issues": "SELECT COUNT(*) AS Cancelled_By_Drivers FROM July WHERE Canceled_Rides_by_Driver IS NOT NULL AND Canceled_Rides_by_Driver != '';",
        "6. Find the maximum and minimum driver ratings for Prime Sedan bookings": "SELECT MAX(Driver_Ratings) AS Max_Driver_Rating, MIN(Driver_Ratings) AS Min_Driver_Rating FROM July WHERE Vehicle_Type = 'Prime Sedan';",
        "7. Retrieve all rides where payment was made using UPI": "SELECT * FROM July WHERE Payment_Method = 'UPI';",
        "8. Find the average customer rating per vehicle type": "SELECT Vehicle_Type, AVG(Customer_Rating) AS Avg_Customer_Rating FROM July WHERE Customer_Rating IS NOT NULL GROUP BY Vehicle_Type;",
        "9. Calculate the total booking value of rides completed successfully": "SELECT SUM(Booking_Value) AS Total_Successful_Booking_Value FROM July WHERE Booking_Status = 'Success';",
        "10. List all incomplete rides along with the reason": "SELECT Booking_ID, Incomplete_Rides, Incomplete_Rides_Reason FROM July WHERE Incomplete_Rides = 'Yes' AND Incomplete_Rides_Reason IS NOT NULL;"
    }

    query = use_case_queries[use_case]

    if use_case == "1. Retrieve all successful bookings":
        df = pd.read_sql_query(query, conn)
        fig = px.histogram(df, x='Vehicle_Type', title='Successful Bookings by Vehicle Type')
        st.plotly_chart(fig)

    elif use_case == "2. Find the average ride distance for each vehicle type":
        df = pd.read_sql_query(query, conn)
        fig = px.bar(df, x='Vehicle_Type', y='Avg_Ride_Distance', 
                     title='Average Ride Distance per Vehicle Type', labels={'Avg_Ride_Distance': 'Avg Ride Distance (km)'})
        st.plotly_chart(fig)

    elif use_case == "3. Get the total number of cancelled rides by customers":
        df = pd.read_sql_query(query, conn)
        cancelled = int(df["Total_Cancelled_By_Customers"][0])
        total_query = "SELECT COUNT(*) AS Total_Rides FROM July;"
        df_total = pd.read_sql_query(total_query, conn)
        total = int(df_total["Total_Rides"][0])
        data = {
            "Status": ["Cancelled by Customers", "Other Rides"],
            "Count": [cancelled, total - cancelled]
        }
        df_pie = pd.DataFrame(data)
        fig = px.pie(df_pie, values='Count', names='Status', 
                     title='Cancelled Rides by Customers vs Other Rides', hole=0.4)
        st.plotly_chart(fig)

    elif use_case == "4. List the top 5 customers who booked the highest number of rides":
        df = pd.read_sql_query(query, conn)
        fig = px.bar(df, x='Customer_ID', y='Total_Rides', 
                     title='Top 5 Customers by Number of Rides Booked')
        st.plotly_chart(fig)

    elif use_case == "5. Get the number of rides cancelled by drivers due to personal and car-related issues":
        df = pd.read_sql_query(query, conn)
        cancelled = int(df["Cancelled_By_Drivers"][0])
        total_query = "SELECT COUNT(*) AS Total_Rides FROM July;"
        df_total = pd.read_sql_query(total_query, conn)
        total = int(df_total["Total_Rides"][0])
        data = {
            "Status": ["Cancelled by Drivers", "Other Rides"],
            "Count": [cancelled, total - cancelled]
        }
        df_pie = pd.DataFrame(data)
        fig = px.pie(df_pie, values='Count', names='Status', 
                     title='Driver Cancelled Rides vs Other Rides', hole=0.4)
        st.plotly_chart(fig)

    elif use_case == "6. Find the maximum and minimum driver ratings for Prime Sedan bookings":
        df = pd.read_sql_query(query, conn)
        col1, col2 = st.columns(2)
        col1.metric("Max Driver Rating", df["Max_Driver_Rating"][0])
        col2.metric("Min Driver Rating", df["Min_Driver_Rating"][0])
        rating_df = pd.DataFrame({
           "Rating Type": ["Max", "Min"],
            "Value": [df["Max_Driver_Rating"][0], df["Min_Driver_Rating"][0]]
        })
        fig = px.bar(rating_df, x="Rating Type", y="Value", 
                     title="Max and Min Driver Ratings for Prime Sedan")
        st.plotly_chart(fig)

    elif use_case == "7. Retrieve all rides where payment was made using UPI":
        df = pd.read_sql_query(query, conn)
        fig = px.histogram(df, x='Vehicle_Type', title='UPI Payments by Vehicle Type')
        st.plotly_chart(fig)

    elif use_case == "8. Find the average customer rating per vehicle type":
        df = pd.read_sql_query(query, conn)
        fig = px.bar(df, x='Vehicle_Type', y='Avg_Customer_Rating', 
                     title='Average Customer Rating per Vehicle Type')
        st.plotly_chart(fig)

    elif use_case == "9. Calculate the total booking value of rides completed successfully":
        df = pd.read_sql_query(query, conn)
        total_value = float(df["Total_Successful_Booking_Value"][0])
        st.metric(label="Total Successful Booking Value", value=f"₹ {total_value:,.2f}")

        # Visualize total successful booking value as a single bar
        fig = px.bar(
            x=["Total Successful Booking Value"],
            y=[total_value],
            labels={"x": "Category", "y": "Booking Value (₹)"},
            title="Total Booking Value of Successfully Completed Rides",
            text=[f"₹ {total_value:,.2f}"]
        )
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig)

    elif use_case == "10. List all incomplete rides along with the reason":
        df = pd.read_sql_query(query, conn)
        reason_counts = df['Incomplete_Rides_Reason'].value_counts().reset_index()
        reason_counts.columns = ['Reason', 'Count']
        fig = px.bar(reason_counts, x='Reason', y='Count', title='Incomplete Rides by Reason')
        st.plotly_chart(fig)
