import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns

st.set_page_config(
    page_title="Scientific Visualization"
)

st.header("Genetic Algorithm", divider="gray")

# Define the URL for the CSV file
URL = 'https://raw.githubusercontent.com/nrhdyh/Student_data/refs/heads/main/arts_student_survey.csv'

# Set the title for the Streamlit app
st.title("Arts Student Survey Analysis Dashboard with Plotly 📊")

# --- 1. Data Loading Function (Cached for Performance) ---

# Use st.cache_data to load the DataFrame only once
@st.cache_data
def load_data(url):
    try:
        data = pd.read_csv(url)
        return data
    except Exception as e:
        # Return None and display an error message
        st.error(f"Error loading data: {e}")
        return None

arts_df = load_data(URL)

# --- 2. Data Display and Plotting ---

if arts_df is not None:
    st.success("CSV file loaded successfully! Plotly analysis beginning. 🎉")

    # Display the first few rows
    st.subheader("Raw Data Preview")
    st.dataframe(arts_df.head())

    # Ensure the 'Gender' column exists before proceeding
    if 'Gender' in arts_df.columns:
        # Calculate the gender counts for plotting
        gender_counts = arts_df['Gender'].value_counts().reset_index()
        gender_counts.columns = ['Gender', 'Count'] # Rename columns for clarity in Plotly

        st.header("Gender Distribution Analysis (Interactive Plots)")

        # --- 3. Plotly Pie Chart ---
        st.subheader("Interactive Pie Chart: Gender Distribution")

        # Create the Plotly Pie Chart using Plotly Express
        fig_pie = px.pie(
            gender_counts,
            values='Count',
            names='Gender',
            title='Distribution of Gender in Arts Faculty (Pie Chart)',
            hole=0.3,  # Optional: creates a donut chart
            color_discrete_sequence=px.colors.qualitative.Pastel
        )

        # Use st.plotly_chart() to display the Plotly figure
        st.plotly_chart(fig_pie, use_container_width=True)

        # --- 4. Plotly Bar Chart ---
        st.subheader("Interactive Bar Chart: Gender Distribution")

        # Create the Plotly Bar Chart using Plotly Express
        fig_bar = px.bar(
            gender_counts,
            x='Gender',
            y='Count',
            title='Distribution of Gender in Arts Faculty (Bar Chart)',
            color='Gender',
            color_discrete_map={ # Optional: custom colors
                'Female': 'lightcoral',
                'Male': 'cornflowerblue',
                'Other': 'gold'
            },
            labels={'Gender': 'Gender Category', 'Count': 'Number of Students'}
        )

        # Add tooltips and customize layout
        fig_bar.update_traces(hovertemplate='Gender: %{x}<br>Count: %{y}<extra></extra>')
        fig_bar.update_layout(xaxis={'categoryorder': 'total descending'}) # Order bars by count

        # Display the Plotly figure
        st.plotly_chart(fig_bar, use_container_width=True)

    else:
        st.warning("The 'Gender' column was not found in the loaded data. Cannot perform analysis.")
