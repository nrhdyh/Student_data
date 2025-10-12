import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


st.set_page_config(
    page_title="Scientific Visualization"
)

st.header("Genetic Algorithm", divider="gray")

# Define the URL for the CSV file
# URL = 'https://raw.githubusercontent.com/nrhdyh/Student_data/refs/heads/main/arts_student_survey.csv'

# Set the title for the Streamlit app
st.title("Arts Student Survey Analysis Dashboard 📊")

# --- 1. Data Loading Function (Cached for Performance) ---

@st.cache_data # Recommended to cache data loading to prevent re-running on every interaction
def load_data(url):
    try:
        data = pd.read_csv(url)
        return data
    except Exception as e:
        # Return None or handle the error appropriately
        st.error(f"Error loading data: {e}")
        return None

arts_df = load_data(URL)

# --- 2. Data Display and Analysis ---

if arts_df is not None:
    st.success("CSV file loaded successfully! Data analysis beginning. 🎉")

    # Display the first few rows (as in the original script's 'display(arts_df_url.head())')
    st.subheader("Raw Data Preview")
    st.dataframe(arts_df.head())

    # Ensure the 'Gender' column exists before proceeding with analysis
    if 'Gender' in arts_df.columns:
        st.header("Gender Distribution Analysis")
        gender_counts = arts_df['Gender'].value_counts()

        # Display the counts
        st.text("Gender Counts:")
        st.dataframe(gender_counts)

        # --- 3. Pie Chart (Matplotlib) ---
        st.subheader("Pie Chart: Gender Distribution")

        fig_pie, ax_pie = plt.subplots(figsize=(6, 6))
        ax_pie.pie(
            gender_counts,
            labels=gender_counts.index,
            autopct='%1.1f%%',
            startangle=140
        )
        ax_pie.set_title('Distribution of Gender in Arts Faculty (Pie Chart)')
        ax_pie.axis('equal') # Ensures the pie is circular

        # Use st.pyplot() to display the Matplotlib figure
        st.pyplot(fig_pie)
        plt.close(fig_pie) # Good practice to close the figure

        # --- 4. Bar Chart (Seaborn/Matplotlib) ---
        st.subheader("Bar Chart: Gender Distribution")

        fig_bar, ax_bar = plt.subplots(figsize=(7, 5))
        sns.barplot(
            x=gender_counts.index,
            y=gender_counts.values,
            ax=ax_bar,
            palette="viridis"
        )
        ax_bar.set_title('Distribution of Gender in Arts Faculty (Bar Chart)')
        ax_bar.set_xlabel('Gender')
        ax_bar.set_ylabel('Count')
        ax_bar.grid(axis='y', linestyle='--')

        # Use st.pyplot() to display the Matplotlib figure
        st.pyplot(fig_bar)
        plt.close(fig_bar) # Good practice to close the figure

    else:
        st.warning("The 'Gender' column was not found in the loaded data.")

# Note: The original code used a variable named 'arts_df' for plotting, but defined 
# 'arts_df_url' for loading. The Streamlit code standardizes on 'arts_df'.
