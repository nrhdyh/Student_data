import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import plotly.figure_factory as ff

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

if arts_df_url.empty:
    st.warning("Data not available for analysis.")
else:
    # --- 1. Data Preparation and Correlation Calculation ---
    st.header("1. 📊 Correlation Analysis of Student Expectations and Satisfaction")
    correlation_cols = [
        'Q3 [What was your expectation about the University as related to quality of resources?]',
        'Q4 [What was your expectation about the University as related to quality of learning environment?]',
        'Q5 [To what extent your expectation was met?]',
        'Q6 [What are the best aspects of the program?]'
    ]

    # Convert columns to numeric, coercing errors to NaN
    df_corr = arts_df_url.copy()
    for col in correlation_cols:
        if col in df_corr.columns:
            df_corr[col] = pd.to_numeric(df_corr[col], errors='coerce')
        else:
            st.error(f"Column '{col}' not found in the dataset. Please check the column names.")
            st.stop() # Stop execution if critical columns are missing

    # Calculate the correlation matrix, dropping rows with NaN
    # Check if there's enough data left after dropping NaNs
    if df_corr[correlation_cols].dropna().shape[0] < 2:
        st.warning("Not enough complete data points to calculate correlation. Check for non-numeric values in the selected columns.")
    else:
        correlation_matrix = df_corr[correlation_cols].dropna().corr()
        
        st.subheader("Correlation Matrix")
        st.dataframe(correlation_matrix.style.background_gradient(cmap='coolwarm').format("{:.2f}"))

        # --- 2. Plotly Heatmap Generation ---
        
        # Extract data for the heatmap
        z = correlation_matrix.values
        x = correlation_matrix.columns.tolist()
        y = correlation_matrix.index.tolist()

        # Create the Plotly Heatmap using figure_factory for annotation support
        fig = ff.create_annotated_heatmap(
            z, 
            x=x, 
            y=y, 
            annotation_text=z.round(2), # Display the correlation values on the map
            colorscale='Coolwarm',
            showscale=True
        )

        # Update layout for better readability
        fig.update_layout(
            title='Correlation Heatmap of Expectations and Satisfaction',
            xaxis={'tickangle': 45, 'dtick': 1},
            yaxis={'dtick': 1},
            height=600
        )
        
        # Display the Plotly figure in Streamlit
        st.subheader("Interactive Correlation Heatmap")
        st.plotly_chart(fig, use_container_width=True)

    # --- 2. Satisfaction Levels Analysis (Q5 & Q6) ---
    st.header("2. Program Satisfaction Levels")
    satisfaction_cols = [
        'Q5 [To what extent your expectation was met?]',
        'Q6 [What are the best aspects of the program?]'
    ]

    col1, col2 = st.columns(2)

    for i, col in enumerate(satisfaction_cols):
        if col in arts_df.columns:
            # Prepare data for Plotly Bar Chart (Equivalent to Count Plot)
            counts = arts_df[col].value_counts().reset_index()
            counts.columns = [col, 'Number of Students']

            fig = px.bar(
                counts,
                x=col,
                y='Number of Students',
                color=col,
                title=f'Distribution of Responses: {col}',
                labels={'x': 'Rating/Aspect', 'y': 'Number of Students'}
            )
            fig.update_layout(xaxis={'categoryorder': 'total descending'})

            # Display plot in the respective column
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

    # --- 3. Academic Performance by Gender ---
    st.header("3. Academic Performance Distributions by Gender")

    # Box Plot for S.S.C (GPA) by Gender
    st.subheader("S.S.C (GPA) by Gender (Box Plot)")
    if 'Gender' in arts_df.columns and 'S.S.C (GPA)' in arts_df.columns:
        fig_box = px.box(
            arts_df,
            x='Gender',
            y='S.S.C (GPA)',
            color='Gender',
            title='Distribution of S.S.C (GPA) by Gender',
            labels={'S.S.C (GPA)': 'S.S.C (CGPA)'}
        )
        st.plotly_chart(fig_box, use_container_width=True)

    # Violin Plot for H.S.C (GPA) by Gender
    st.subheader("H.S.C (GPA) by Gender (Violin Plot)")
    if 'Gender' in arts_df.columns and 'H.S.C (GPA)' in arts_df.columns:
        fig_violin = px.violin(
            arts_df,
            x='Gender',
            y='H.S.C (GPA)',
            color='Gender',
            box=True,
            title='Distribution of H.S.C (GPA) by Gender'
        )
        st.plotly_chart(fig_violin, use_container_width=True)
    else:
        st.error("Required columns for GPA plots not found.")

    st.markdown("---")

    # --- 4. Core Survey Questions (Indices 13-20) ---
    st.header("4. Core Survey Question Distributions")

    # Get columns by index (13 to 20 are indices 13, 14, ..., 20)
    columns_to_visualize = arts_df.columns[13:21]
    st.write(f"Columns analyzed: {list(columns_to_visualize)}")

    for i, col in enumerate(columns_to_visualize):
        st.subheader(f"Distribution: {col}")

        # Check for numerical data (int64, float64)
        if arts_df[col].dtype in ['int64', 'float64']:
            # Numerical Visualization (Histogram)
            fig_hist = px.histogram(
                arts_df,
                x=col,
                marginal="box",
                title=f'Distribution of {col}',
                labels={col: col, 'count': 'Frequency'}
            )
            st.plotly_chart(fig_hist, use_container_width=True)

        # Assuming other types (object/categorical) should be treated as categories
        elif arts_df[col].dtype == 'object' or arts_df[col].nunique() < 20:
            # Categorical/Ordinal Visualization (Bar Chart)
            counts = arts_df[col].value_counts().reset_index()
            counts.columns = [col, 'Number of Students']

            fig_bar = px.bar(
                counts,
                x='Number of Students',
                y=col,
                color=col,
                orientation='h',
                title=f'Distribution of Responses for: {col}'
            )
            fig_bar.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info(f"Skipping visualization for column '{col}' (unsuitable data type or too many unique values).")

    st.markdown("---")

    # --- 5. Program Improvement Aspects ---
    st.header("5. Program Improvement Aspects")
    improvement_col = 'What aspects of the program could be improved?'

    if improvement_col in arts_df.columns:
        st.subheader(f"Frequency of Responses for: {improvement_col}")

        # Create a horizontal bar chart
        counts_imp = arts_df[improvement_col].value_counts().reset_index()
        counts_imp.columns = [improvement_col, 'Number of Students']

        fig_imp = px.bar(
            counts_imp,
            x='Number of Students',
            y=improvement_col,
            color=improvement_col,
            orientation='h',
            title='Most Frequently Mentioned Aspects for Program Improvement'
        )
        fig_imp.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_imp, use_container_width=True)
    else:
        st.error(f"Column '{improvement_col}' not found.")
