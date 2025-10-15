import streamlit as st
import pandas as pd
import plotly.express as px
#import plotly.figure_factory as ff
# Note: seaborn import is unnecessary since you only use Plotly

st.set_page_config(
    page_title="Scientific Visualization",
    layout="wide" # Added wide layout for better dashboard view
)

st.header("Genetic Algorithm", divider="gray")

# Define the URL for the CSV file
URL = 'https://raw.githubusercontent.com/nrhdyh/Student_data/refs/heads/main/arts_student_survey.csv'

st.title("Arts Student Survey Analysis Dashboard with Plotly 📊")

# --- 1. Data Loading Function (Cached for Performance) ---
@st.cache_data
def load_data(url):
    try:
        data = pd.read_csv(url)
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Load the data into the correctly named variable
arts_df = load_data(URL)

# --- 2. Unified Data Display and Plotting ---

if arts_df is not None:
    st.success("CSV file loaded successfully! Plotly analysis beginning. 🎉")

    # Display the first few rows
    st.subheader("Raw Data Preview")
    st.dataframe(arts_df.head())

    # --- Gender Distribution Section (Already Correctly uses arts_df) ---
    if 'Gender' in arts_df.columns:
        gender_counts = arts_df['Gender'].value_counts().reset_index()
        gender_counts.columns = ['Gender', 'Count']

        st.header("Gender Distribution Analysis (Interactive Plots)")

        # Pie Chart
        st.subheader("Interactive Pie Chart: Gender Distribution")
        fig_pie = px.pie(gender_counts, values='Count', names='Gender',
                         title='Distribution of Gender in Arts Faculty (Pie Chart)', hole=0.3, 
                         color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_pie, use_container_width=True)

        # Bar Chart
        st.subheader("Interactive Bar Chart: Gender Distribution")
        fig_bar = px.bar(gender_counts, x='Gender', y='Count',
                         title='Distribution of Gender in Arts Faculty (Bar Chart)', color='Gender',
                         color_discrete_map={'Female': 'lightcoral', 'Male': 'cornflowerblue', 'Other': 'gold'},
                         labels={'Gender': 'Gender Category', 'Count': 'Number of Students'})
        fig_bar.update_traces(hovertemplate='Gender: %{x}<br>Count: %{y}<extra></extra>')
        fig_bar.update_layout(xaxis={'categoryorder': 'total descending'})
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.warning("The 'Gender' column was not found in the loaded data. Cannot perform analysis.")

    st.markdown("---")

    # --- START OF PREVIOUSLY FAILED/INCORRECTLY REFERENCED SECTION ---
    # The 'if arts_df_url.empty' block is removed, and all subsequent code uses arts_df.

    # 1. Satisfaction Levels Analysis (Q5 & Q6)
    st.header("1. Program Satisfaction Levels")
    satisfaction_cols = ['Q5 [To what extent your expectation was met?]', 'Q6 [What are the best aspects of the program?]']
    col1, col2 = st.columns(2)

    for i, col in enumerate(satisfaction_cols):
        if col in arts_df.columns: # CORRECT: Use arts_df
            counts = arts_df[col].value_counts().reset_index()
            counts.columns = [col, 'Number of Students']

            fig = px.bar(counts, x=col, y='Number of Students', color=col,
                         title=f'Distribution of Responses: {col}', labels={'x': 'Rating/Aspect', 'y': 'Number of Students'})
            fig.update_layout(xaxis={'categoryorder': 'total descending'})

            if i % 2 == 0:
                with col1:
                    st.subheader("Expectation Met (Q5)")
                    st.plotly_chart(fig, use_container_width=True)
            else:
                with col2:
                    st.subheader("Best Aspects (Q6)")
                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.error(f"Column '{col}' not found.")

    st.markdown("---")

    # 3. Academic Performance by Gender
    st.header("Academic Performance Distributions by Gender")

    # Box Plot for S.S.C (GPA) by Gender
    st.subheader("2. S.S.C (GPA) by Gender (Box Plot)")
    if 'Gender' in arts_df.columns and 'S.S.C (GPA)' in arts_df.columns: # CORRECT: Use arts_df
        fig_box = px.box(arts_df, x='Gender', y='S.S.C (GPA)', color='Gender',
                         title='Distribution of S.S.C (GPA) by Gender', labels={'S.S.C (GPA)': 'S.S.C (CGPA)'})
        st.plotly_chart(fig_box, use_container_width=True)

    # Violin Plot for H.S.C (GPA) by Gender
    st.subheader("3. H.S.C (GPA) by Gender (Violin Plot)")
    if 'Gender' in arts_df.columns and 'H.S.C (GPA)' in arts_df.columns: # CORRECT: Use arts_df
        fig_violin = px.violin(arts_df, x='Gender', y='H.S.C (GPA)', color='Gender', box=True,
                               title='Distribution of H.S.C (GPA) by Gender')
        st.plotly_chart(fig_violin, use_container_width=True)
    else:
        st.error("Required columns for GPA plots not found.")

    st.markdown("---")

    # 4. Core Survey Questions (Indices 13-20)
    st.header("4. Core Survey Question Distributions")

    columns_to_visualize = arts_df.columns[13:21] # CORRECT: Use arts_df
    st.write(f"Columns analyzed: {list(columns_to_visualize)}")

    for i, col in enumerate(columns_to_visualize):
        st.subheader(f"Distribution: {col}")

        if arts_df[col].dtype in ['int64', 'float64']: # CORRECT: Use arts_df
            fig_hist = px.histogram(arts_df, x=col, marginal="box",
                                   title=f'Distribution of {col}', labels={col: col, 'count': 'Frequency'})
            st.plotly_chart(fig_hist, use_container_width=True)

        elif arts_df[col].dtype == 'object' or arts_df[col].nunique() < 20: # CORRECT: Use arts_df
            counts = arts_df[col].value_counts().reset_index()
            counts.columns = [col, 'Number of Students']

            fig_bar = px.bar(counts, x='Number of Students', y=col, color=col, orientation='h',
                             title=f'Distribution of Responses for: {col}')
            fig_bar.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info(f"Skipping visualization for column '{col}' (unsuitable data type or too many unique values).")

    st.markdown("---")

    # 5. Program Improvement Aspects
    st.header("5. Program Improvement Aspects")
    improvement_col = 'What aspects of the program could be improved?'

    if improvement_col in arts_df.columns: # CORRECT: Use arts_df
        st.subheader(f"Frequency of Responses for: {improvement_col}")

        counts_imp = arts_df[improvement_col].value_counts().reset_index()
        counts_imp.columns = [improvement_col, 'Number of Students']

        fig_imp = px.bar(counts_imp, x='Number of Students', y=improvement_col, color=improvement_col,
                         orientation='h', title='Most Frequently Mentioned Aspects for Program Improvement')
        fig_imp.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_imp, use_container_width=True)
    else:
        st.error(f"Column '{improvement_col}' not found.")

st.markdown("---")

    # --- FINAL INTERPRETATION SECTION (Based on User's Request) ---

    
    st.markdown("""
    
    ### Gender Distribution and Academic Performance
    The analysis clearly shows the **student population's gender split**, and the **Box and Violin Plots** reveal the distribution of **SSC and HSC GPAs** for both groups. This comparison helps identify any significant differences in academic entry levels between genders, though the plots themselves would determine if one group tends to have a higher median or wider variance in scores.

    ### Expectation vs. Satisfaction
    The bar chart for **'Q5 [To what extent your expectation was met?]'** is the most critical metric, showing the overall level of student satisfaction. If most responses fall under **'Very Satisfied' or 'Satisfied,'** the program is generally meeting student expectations, while the **'Q6 [What are the best aspects of the program?]'** bar chart points to the specific factors (e.g., faculty, resources) driving this positive experience.

    ### Areas for Improvement
    The visualization of **'What aspects of the program could be improved?'** provides actionable insights. The top-ranked items in this horizontal bar chart represent the areas where the university should allocate resources, as they are the most frequently cited pain points by the student body.
    """)
    # --- END OF FINAL INTERPRETATION SECTION ---
