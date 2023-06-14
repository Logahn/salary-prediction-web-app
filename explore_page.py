import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def shorten_categories(categories: pd.Series, cutoff: int) -> dict:
    """
    Shortens categories based on a cutoff value.

    Args:
        categories: A pandas Series containing the categories.
        cutoff: An integer representing the cutoff value.

    Returns:
        A dictionary where the keys are the original categories and the values
        are either the same as the key or 'Other' if the value is less than
        the cutoff.
    """
    categorical_map = {}
    # Iterate over the categories and assign either the category or 'Other'
    # based on the cutoff value.
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map


def clean_experience(experience: str) -> float:
    """
    Cleans the experience string and returns it as a float.

    Args:
    experience (str): a string indicating the years of experience.

    Returns:
    A float indicating the years of experience.
    """
    if experience == 'More than 50 years':
        return 50.0
    elif experience == 'Less than 1 year':
        return 0.5
    else:
        return float(experience)


def clean_education(x):
    """
    Cleans the education level string by returning one of four possible categories: 
    'Bachelor’s degree', 'Master’s degree', 'Post grad', or 'Less than a Bachelors'.

    Args:
        x (str): the education level string to be cleaned
    
    Returns:
        str: the cleaned education level string
    """
    if 'Bachelor’s degree' in x:
        # If the string contains 'Bachelor’s degree', return 'Bachelor’s degree'
        return 'Bachelor’s degree'
    elif 'Master’s degree' in x:
        # If the string contains 'Master’s degree', return 'Master’s degree'
        return 'Master’s degree'
    elif 'Professional degree' in x or 'Other doctoral' in x:
        # If the string contains 'Professional degree' or 'Other doctoral', return 'Post grad'
        return 'Post grad'
    else:
        # If the string doesn't contain any of the above, return 'Less than a Bachelors'
        return 'Less than a Bachelors'

import pandas as pd
import streamlit as st

def shorten_categories(value_counts, max_categories):
    """
    A function to shorten categories in a pandas Series to the top n categories.

    Parameters:
    value_counts (pandas.Series): A pandas Series containing the value counts of each category.
    max_categories (int): The maximum number of categories to keep.

    Returns:
    A pandas Series with the top n categories and their value counts.
    """
    shortened_categories = value_counts[:max_categories]
    if value_counts.sum() > shortened_categories.sum():
        shortened_categories["Other"] = value_counts.sum() - shortened_categories.sum()
    return shortened_categories

def clean_experience(years):
    """
    A function to clean the 'YearsCodePro' column of the dataframe.

    Parameters:
    years (str): A string containing the number of years of professional coding experience.

    Returns:
    An integer value representing the cleaned years of coding experience.
    """
    if years == "Less than 1 year":
        return 0.5
    elif years == "More than 50 years":
        return 50
    else:
        return int(years.split()[0])

def clean_education(education):
    """
    A function to clean the 'EdLevel' column of the dataframe.

    Parameters:
    education (str): A string representing the level of education.

    Returns:
    A string representing the cleaned level of education.
    """
    if "Bachelor’s degree" in education:
        return "Bachelor's degree"
    elif "Master’s degree" in education:
        return "Master's degree"
    elif "Doctoral degree" in education:
        return "Doctoral degree"
    elif "Some college/university study without earning a degree" in education:
        return "Some college without degree"
    elif "Professional degree" in education:
        return "Professional degree"
    elif "I never completed any formal education" in education:
        return "No formal education"
    else:
        return education

@st.cache_data 
def load_data():
    """
    A function to load and clean the 'survey_results_public.csv' file.

    Returns:
    A pandas dataframe containing the cleaned data.
    """
    df = pd.read_csv("survey_results_public.csv")
    df = df[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedComp"]]
    df = df.dropna(subset=["ConvertedComp", "Employment"])
    df = df[df["Employment"] == "Employed full-time"]
    df = df.drop("Employment", axis=1)

    country_map = shorten_categories(df.Country.value_counts(), 400)
    df["Country"] = df["Country"].map(country_map)
    df = df[(df["ConvertedComp"] >= 10000) & (df["ConvertedComp"] <= 250000) & (df["Country"] != "Other")]

    df["YearsCodePro"] = df["YearsCodePro"].apply(clean_experience)
    df["EdLevel"] = df["EdLevel"].apply(clean_education)
    df = df.rename(columns={"ConvertedComp": "Salary"})

    return df

df = load_data()

def show_explore_page():
    st.title("Explore Software Engineer Salaries")

    st.write(
        """
    ### Stack Overflow Developer Survey 2020
    """
    )

    data = df["Country"].value_counts()

    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels=data.index, autopct="%1.1f%%", shadow=False, startangle=90)
    ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.

    st.write("""#### Number of Data from different countries""")

    st.pyplot(fig1)
    
    st.write(
        """
    #### Mean Salary Based On Country
    """
    )

    data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(data)

    st.write(
        """
    #### Mean Salary Based On Experience
    """
    )

    data = df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data)
