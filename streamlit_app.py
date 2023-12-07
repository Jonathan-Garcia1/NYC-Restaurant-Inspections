import streamlit as st
import pandas as pd
import content as cn

# Set the page config to use wide format
st.set_page_config(layout="wide")

css = '''
<style>
    .block-container.st-emotion-cache-z5fcl4.ea3mdgi2 {
        width: 1400px;
    } 
    
    .stCodeBlock {
    max-height: 800px;
    overflow: auto;
    }

    div[data-testid="stExpanderDetails"].st-emotion-cache-1clstc5.eqpbllx1 {
        max-height: 900px;
        overflow: auto;
    }

    .custom-code-container {
        max-height: 300px;
        overflow: auto;
    }
</style>
'''
def display_dataframe(file_name, title='', description='', max_height=760):
    df = pd.read_csv(file_name)
    numRows = len(df)
    dynamic_height = min(max_height, (numRows + 1) * 35 + 3)
    
    if title:
        st.write(f"## {title}")
    
    if description:
        st.markdown(description)
        
    st.dataframe(df, height=dynamic_height)

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
        st.write("#### Acquired NYC Inspection DataFrame Preview:\n")
        st.dataframe(df)

# Second Accordion: Prepare
with st.expander("Prepare"):
    tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Dealing with Nulls", "tab3", "tab4"])

    with tab1:
        
        st.markdown('#### Preparation Intro')
        st.markdown(cn.prep_text)
        display_dataframe('inspections_df_status.csv', 'Dataset Overview', 'The table below displays all columns in the dataset, including their respective Null and Zero Counts and data types.')
        display_dataframe('inspections_prepare.csv', 'Columns with Nulls and Zeros', 'In the following table, we have applied a filter to focus solely on columns with Nulls or Zeros. These columns will be the primary focus of our cleaning and preparation efforts in this section.')

    with tab2:
        st.markdown('#### Dealing with Nulls')
        display_dataframe('inspections_df_isna.csv', 'Current Null Count')
        
        st.markdown('#### Grade & Grade Date')
        st.markdown(
            '''Let's begin the preparation section by addressing the columns with the highest number of null values, which are Grade and Grade Date.
            According to the Health Department, all inspections generate a score, but not all result in a letter grade. Letter grades are assigned only to Cycle initial-inspections and Cycle re-inspections. You can find more information on how these grades are determined in the [How We Score and Grade](https://www.nyc.gov/assets/doh/downloads/pdf/rii/restaurant-grading-faq.pdf) document.
            '''
        )
        st.code(
            '''
            # Dropping the 'grade' and 'grade_date' columns
            inspection_df = inspection_df.drop(['grade', 'grade_date'], axis=1)
            '''
        )
        
        st.markdown(
            '''
            <br>
            
            #### Inferring Missing Values

            Our next step is to strategize how to address these missing values by leveraging available data in other columns. The proposed hierarchy for inference is as follows:

            lat&long < building < bin < bbl < nta, zipcode* < community board < council district < census tract

            Given the relatively low count of missing values in the BBL column, it appears to be a promising candidate for inferring related data such as NTA (Neighborhood Tabulation Area), Community Board, Council District, and Census Tract.

            Let's examine the first few unique values in the BBL column to understand its content
            ''',
            unsafe_allow_html=True
        )
        st.code(
            '''
            # Let's take a look at the first few unique values in the BBL column
            sorted(inspection_df.bbl.unique())[:10]
            '''
        )
        st.markdown(
            '''
            ```python
            [1.0,
            2.0,
            3.0,
            4.0,
            5.0,
            1000010010.0,
            1000020001.0,
            1000047501.0,
            1000070028.0,
            1000070031.0]
            ```
            ''', 
        )

        
        st.markdown(
            '''
            The initial examination of the BBL column shows the presence of non-standard values such as 1.0, 2.0, 3.0, 4.0, etc., which do not conform to the expected 10-digit format.

            Now, let's find out the count of these non-standard values:
            '''
        )
        
        st.code(
            '''
            # Define non-standard BBL values
            bbl_values = [np.nan, 1.0, 2.0, 3.0, 4.0, 5.0]

            # Calculate the count of these non-standard values in the BBL column
            inspection_df['bbl'].isin(bbl_values).sum()
            '''
        )
        
        st.markdown(
            '''
            The count of non-standard BBL values is found to be relatively consistent with the number of NaN values in the BIN column, indicating a pattern of missing values across these key columns.

            - census_tract               3157
            - bin                        4144
            - bbl                        4144
            - nta                        3153
            - community_board            3153
            - council_district           3157

            We are unable to rely on bbl make inferences because the features were missing across the same. We must abandon the hierarchy inference plan. To proceed, we drop rows with NaN values in the BIN column.
            '''
        )

        st.code(
            '''
            # Dropping rows with null values in the 'bin' column
            inspection_df = inspection_df.dropna(subset=['bin'])
            '''
        )
        st.markdown('Reevaluating Null Counts After BIN Column Cleanup')
        
        st.code(
            '''
            # Calculate the count of missing values in each column
            null_counts_by_column = inspection_df.isnull().sum()

            # Filter and display columns with missing values
            null_counts_by_column[null_counts_by_column > 0]
            '''
        )
        
        st.code(
            '''
            zipcode                    30
            phone                       6
            score                    7440
            community_board            30
            council_district           34
            census_tract               34
            nta                        30
            violation_code           1076
            violation_description    1076
            
            ''', 
        )

        st.markdown(
            '''
            As expected, the remaining NaNs are mostly related or in common with the initial set. 

            #### Handling Remaining Zoning Nulls

            For the small number of remaining NaNs (e.g., 30 in ZIP code), we can safely drop them due to their limited impact on the dataset. I chose to drop 'council_district' to see if this also got rid of the other NaNs.
            '''
        )
        
        st.code(
            '''
            # Dropping rows with null values in the 'council_district' column
            inspection_df = inspection_df.dropna(subset=['council_district'])

            # Reassessing the null counts in the dataset
            null_counts_by_column = inspection_df.isnull().sum()
            null_counts_by_column[null_counts_by_column > 0]
            ''', 
        )

        st.code(
            '''
            phone                       6
            score                    7438
            violation_code           1076
            violation_description    1076
            
            ''', 
        )
        

        st.markdown(
            '''
            As expected, dropping council_district also removed the other zoning features with nulls.

            #### Identifying Relevant Inspection Types

            Before proceeding with the score nulls, let's identify and focus on inspection types related to food safety.
            '''
        )
        
        st.code(
            '''
            # Assuming 'inspection_df' is your DataFrame
            unique_inspection_types = inspection_df['inspection_type'].unique()

            # Convert the numpy array to a list and then sort it
            sorted_inspection_types = sorted(unique_inspection_types.tolist())
            sorted_inspection_types
            ''', 
        )
        
        
        
        # Create a markdown block with custom HTML for the code
        code_content = '''
        ['Administrative Miscellaneous / Compliance Inspection',
        'Administrative Miscellaneous / Initial Inspection',
        'Administrative Miscellaneous / Re-inspection',
        'Administrative Miscellaneous / Reopening Inspection',
        'Administrative Miscellaneous / Second Compliance Inspection',
        'Calorie Posting / Compliance Inspection',
        'Calorie Posting / Initial Inspection',
        'Calorie Posting / Re-inspection',
        'Cycle Inspection / Compliance Inspection',
        'Cycle Inspection / Initial Inspection',
        'Cycle Inspection / Re-inspection',
        'Cycle Inspection / Reopening Inspection',
        'Cycle Inspection / Second Compliance Inspection',
        'Inter-Agency Task Force / Initial Inspection',
        'Inter-Agency Task Force / Re-inspection',
        'Pre-permit (Non-operational) / Compliance Inspection',
        'Pre-permit (Non-operational) / Initial Inspection',
        'Pre-permit (Non-operational) / Re-inspection',
        'Pre-permit (Non-operational) / Second Compliance Inspection',
        'Pre-permit (Operational) / Compliance Inspection',
        'Pre-permit (Operational) / Initial Inspection',
        'Pre-permit (Operational) / Re-inspection',
        'Pre-permit (Operational) / Reopening Inspection',
        'Pre-permit (Operational) / Second Compliance Inspection',
        'Smoke-Free Air Act / Compliance Inspection',
        'Smoke-Free Air Act / Initial Inspection',
        'Smoke-Free Air Act / Limited Inspection',
        'Smoke-Free Air Act / Re-inspection',
        'Trans Fat / Compliance Inspection',
        'Trans Fat / Initial Inspection',
        'Trans Fat / Re-inspection']
        '''


        # Create a markdown block with your code inside a code block
        code_block = f'''
        <div class="custom-code-container">

        ```python
        {code_content}
        ```
        </div>
        '''
        st.markdown(code_block, unsafe_allow_html=True)
    
        
        st.markdown(
            '''
            We will exclude types such as "Calorie Posting," "Pre-permit," "Smoke-Free Air Act," and "Trans Fat," as they do not directly pertain to food safety
            '''
        )
        
        
        st.code(
            '''
            # List of inspection types to be removed
            remove_types = ["Calorie Posting", "Pre-permit", "Smoke-Free Air Act", "Trans Fat"]

            # Filter the DataFrame in a single step
            inspection_df = inspection_df[~inspection_df['inspection_type'].str.startswith(tuple(remove_types))]
            len(inspection_df)
            '''
        )
        
        st.code(
            '''
            155970
            '''
        )
        
        st.markdown('Reevaluating Null Counts After BIN Column Cleanup')
        
        st.code(
            '''
            # Calculate the count of missing values in each column
            null_counts_by_column = inspection_df.isnull().sum()

            # Filter and display columns with missing values
            null_counts_by_column[null_counts_by_column > 0]
            '''
        )
        
        st.code(
            '''
            score                    6024
            violation_code            797
            violation_description     797
            '''
        )
        
        st.markdown('''
                    Eliminating these rows led to a modest decrease in null values, due to the overlap in missing data among these rows. However, a detailed analysis of a few outstanding violation codes is still required.
                    
                    Now, let's examine the history of a restaurant with a null value in the violation code to understand the reasons behind this occurrence.
                    
                    ''')
        
        st.code(
            '''
            # Step 1: Group by 'camis' and 'inspection_date' and check for nulls in 'violation_code'
            grouped = inspection_df.groupby(['camis', 'inspection_date'])
            groups_with_nulls = grouped.apply(lambda x: x['score'].isna().any())

            # Step 2: Filter the DataFrame to include only those groups
            filtered_df = inspection_df[inspection_df.set_index(['camis', 'inspection_date']).index.isin(groups_with_nulls[groups_with_nulls].index)].reset_index(drop=True)

            # Now, 'filtered_df' contains only the groups where there are null values in 'violation_code'
            filtered_df.sort_values(by='camis').head(3)
            '''
        )
        
        display_dataframe('inspections_camisg.csv')
        
    with tab3:
        st.markdown('')


