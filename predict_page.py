import streamlit as st
import pickle
import numpy as np


# Create a function for loading model
import pickle

def load_model() -> object:
    """
    Loads a saved machine learning model from a pickle file.
    
    :return: the loaded model object
    """
    with open('saved_steps.pkl', 'rb') as file:
        model = pickle.load(file)
    return model

data = load_model()

regressor = data['model']
le_country = data['le_country']
le_education = data['le_education']

import numpy as np

def show_predict_page():
    """
    Displays a streamlit page where the user can select a country, education level, and years of experience to predict
    their salary as a software developer.
    """

    # Set page title
    st.title("Software Developer Salary Predictions")

    # Set options for country and education level
    countries = (
        "United States",
        "India",
        "United Kingdom",
        "Germany",
        "Canada",
        "Brazil",
        "France",
        "Spain",
        "Netherlands",
        "Australia",
        "Italy",
        "Poland",
    )
    education_levels = (
        'Bachelor’s degree',
        'Master’s degree',
        'Less than a Bachelors',
        'Post grad'
    )

    # Display dropdowns for country and education level
    country = st.selectbox("Country", countries)
    education_level = st.selectbox("Education Level", education_levels)

    # Display slider for years of experience
    years_of_experience = st.slider("Years of Experience", 1, 50, 3)

    # Display button to predict salary
    predict_salary_button = st.button("Predict Salary")

    if predict_salary_button:
        # Prepare input data for salary prediction
        input_data = np.array([[country, education_level, years_of_experience]])
        input_data[:, 0] = le_country.transform(input_data[:, 0])
        input_data[:, 1] = le_education.transform(input_data[:, 1])
        input_data = input_data.astype(float)

        # Predict salary and display result
        salary_prediction = regressor.predict(input_data)
        st.subheader("Predicted Salary: ${:,.2f}".format(salary_prediction[0]))
