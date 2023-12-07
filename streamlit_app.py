import streamlit as st
import pandas as pd
import content as cn

# Set the page config to use wide format
st.set_page_config(layout="wide")

css = '''
<style>
    .block-container.st-emotion-cache-z5fcl4.ea3mdgi2 {
        width: 1200px;
    } 
    .stCodeBlock {
    max-height: 800px;
    overflow: auto;

    }
</style>
'''

st.markdown(css, unsafe_allow_html=True)


# Project Title, Description, and Objectives
st.title("New York Health Inspection Prediction")

st.header("Project Description")
st.write("In today’s culinary landscape, making informed decisions about dining out is challenging with the multitude of options available. Our project leverages New York Open data to integrate health inspection results and restaurant reviews from Google Maps. By analyzing this information, we predict restaurant health inspection outcomes and report sentiment based on posted reviews, offering valuable insights for safety and informed choices. Whether you’re a foodie, a concerned parent, or a health-conscious individual, our platform assists in making better decisions about where to dine in New York City.")

st.header("Project Objectives")
st.markdown("""
- Merge NYC health inspection data with customer reviews from Google Maps.
- Utilize sentiment analysis on customer reviews for a qualitative understanding of dining experiences.
- Predict the outcomes of restaurant health inspections for informed decision-making.
- Assist various stakeholders, including food enthusiasts, parents, and health-conscious individuals, in making safer and better-informed dining choices in New York City.
""")

# Section: NYC DATASET
st.header("NYC DATASET")
# First Accordion: NYC DATASET
with st.expander("Acquire"):
    # Tabs within the accordion
    tab1, tab2, tab3, tab4 = st.tabs(["Overview", "API Functions", "API Call", "Dataframe"], )

    with tab1:
        # Embed iframe
        st.markdown("""
        <div style="width: 960px; height: 720px; margin: 10px; position: relative;">
            <iframe allowfullscreen frameborder="0" style="width:960px; height:720px" 
            src="https://lucid.app/documents/embedded/a0dcf6a9-1c35-4805-bd9b-749fcbbbf9f8?ui=off" 
            id="~BGT2pp0eyZo">
            </iframe>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        st.code(cn.api_code)

    with tab3:
        st.code(cn.api_call)

    with tab4:
        df = pd.read_csv('inspections_df_head.csv')

        # Display the DataFrame in the app
        st.write("### Displaying the DataFrame:")
        st.dataframe(df)
        # st.markdown(cn.nyc_acquired_df)

# Second Accordion: Prepare
with st.expander("Prepare"):
    tab1, tab2 = st.tabs(["Overview", "Dataframe Nulls"])

    with tab1:
        st.markdown("## Title")

    with tab2:
        st.markdown("## Title")

# Add additional components as needed
