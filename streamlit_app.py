import streamlit as st
import pandas as pd
import content as cn
import uuid

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
    
    div[data-baseweb="tab-panel"][id^="tabs-bui4-tabpanel-"][class^="st-"] {
        max-height: 800px; /* Adjust the max height as needed */
        overflow-y: auto;
        overflow-x: hidden; 
        
    }
    /* Style the scrollbar corner to be transparent */
    div[data-baseweb="tab-panel"][id^="tabs-bui4-tabpanel-"][class^="st-"]::-webkit-scrollbar-corner {
        background-color: transparent;
    }
    
    .st-emotion-cache-q8sbsg p {
        font-size: x-large;
    }
    
    .footer {
        visibility: hidden;
        }

</style>
'''
def display_dataframe(file_name, title='', description='', max_height=720):
    df = pd.read_csv(file_name)
    numRows = len(df)
    dynamic_height = min(max_height, (numRows + 1) * 35 + 3)
    
    if title:
        st.write(title)
    
    if description:
        st.markdown(description)
        
    st.dataframe(df, height=dynamic_height)

st.markdown(css, unsafe_allow_html=True)

def display_styled_code_block(code_content, max_height=300):
    unique_class_name = f"custom-code-container-{uuid.uuid4().hex[:6]}"

    # CSS to be added to the app
    css_styled_code = f'''
    <style>
        .{unique_class_name} pre {{
            max-height: {max_height}px;
            overflow: auto;
            margin-bottom: 1em;
        }}
        .{unique_class_name} pre::-webkit-scrollbar-corner {{
            background-color: transparent;
        }}
    </style>
    '''
    
    # The code block with custom styling using HTML tags
    code_block = f'''
    <div class="{unique_class_name}">
        <pre><code>{code_content}</code></pre>
    </div>
    '''
    
    # Adding CSS and the code block to the Streamlit app
    st.markdown(css_styled_code, unsafe_allow_html=True)
    st.markdown(code_block, unsafe_allow_html=True)
    
    
def v_spacer(height, sb=False) -> None:
    for _ in range(height):
        if sb:
            st.sidebar.write('\n')
        else:
            st.write('\n')


# Project Title, Description, and Objectives
st.title("New York Health Inspection Prediction")

st.image('Title.jpg')

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
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Overview", "Nulls: Zoning", "Nulls: By Inspection Type", "Nulls: By Action", "Remaining Nulls & Zeros", "Data Types"])

    with tab1:
        
        st.markdown('#### Preparation Intro')
        st.markdown(cn.prep_text)
        display_dataframe('inspections_df_status.csv', '#### Dataset Overview', 'The table below displays all columns in the dataset, including their respective Null and Zero Counts and data types.')
        
        v_spacer(height=2, sb=False)
        
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
        
        
    with tab2:
        
        with st.container(border=False):
            
            st.markdown('''
                        ### Dealing with Nulls in the Zoning Columns
                        In this section you will see how we attempted to infer zoning data using the known hierarchy of zoning labels in NYC.  
                        # ''')
            display_dataframe('inspections_df_isna.csv', '##### Current Null Count', max_height= 400)
            

            
            v_spacer(height=2, sb=False)
            
            st.markdown(
                '''
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
                The BBL column shows the presence of non-standard values, which do not conform to the expected 10-digit format (1.0, 2.0, 3.0, 4.0, etc)

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
            
            st.code(
                '''
                4144
                '''
            )
            
            st.markdown(
                '''
                Non-standard BBL values are exactly the same as NaN values in the BIN column, indicating a pattern of missing values across these key columns.

                - census_tract               3157
                - bin                        4144
                - bbl                        4144
                - nta                        3153
                - community_board            3153
                - council_district           3157
                '''
            )
            
            v_spacer(height=2, sb=False)
            
            st.markdown('#### Drop BBL Nulls')
            
            st.markdown(
                '''
                We are unable to rely on bbl make inferences because the features were missing across the same rows. We must abandon the hierarchy inference plan. To proceed, we drop rows with NaN values in the BIN column.
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
                There was a significant overlap in missing data among these rows, very few nulls remain in relation to zoning columns.
                '''
            )
            
            v_spacer(height=2, sb=False)
            
            st.markdown(
                '''
                #### Handling Remaining Zoning Nulls

                For the small number of remaining NaNs (e.g., 34 census_track), we can safely drop them due to their limited impact on the dataset. I chose to drop 'council_district'. With some luck, these will overlap with the other zoning nulls.
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
                '''
            )
            
            v_spacer(height=2, sb=False)
            
        with tab3:
            st.markdown('''
                        ### Dealing with Nulls by Inspection Type
                        
                        In this section you will see how we dealt with the nulls in columns related to inspection scores by dropping rows of inspection types that were not relevant to this project. 
                        ''')
            
            st.markdown(
                '''#### Identifying Relevant Inspection Types

                Before proceeding with the score nulls, let's identify and focus on inspection types related to food safety.
                '''
            )
            
            st.code(
                '''
                # Creating an array of unique inspection_type values
                unique_inspection_types = inspection_df['inspection_type'].unique()

                # Convert the numpy array to a list and then sort it
                sorted_inspection_types = sorted(unique_inspection_types.tolist())
                sorted_inspection_types
                ''' 
            )
            
            
            
            # Create a markdown block with custom HTML for the code
            display_styled_code_block(cn.inspection_type, max_height=300)
            
            v_spacer(height=2, sb=False)

            st.markdown('#### Dropping Irrelevant Inspection Types')
            st.markdown(
                '''
                We will exclude types such as "Calorie Posting," "Pre-permit," "Smoke-Free Air Act," and "Trans Fat," as they do not directly pertain to food safety
                '''
            )
            
            
            st.code(
                '''
                original_length = len(inspection_df)
                # List of inspection types to be removed
                remove_types = ["Calorie Posting", "Pre-permit", "Smoke-Free Air Act", "Trans Fat"]

                # Filter the DataFrame in a single step
                inspection_df = inspection_df[~inspection_df['inspection_type'].str.startswith(tuple(remove_types))]
                new_length = len(inspection_df)
                print(f' {original_length} - {new_length} = {(original_length - new_length)}')
                '''
            )
            
            st.code(
                '''
                203187 - 155970 = 47217
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
                        Eliminating these 47k irrelevant rows led to a modest decrease in null values, due to the overlap in missing data among these rows. However, a detailed analysis of a few outstanding violation codes is still required.
                        ''')
            
            v_spacer(height=2, sb=False)
            
            st.markdown('#### Continue Identifying Relevant Inspection Types')
            
            st.markdown('''
                        Now, let's examine the history of a restaurant with a null value in the violation code to understand the reasons behind this occurrence.
                        
                        ''')
            
            st.code(
                '''
                # Group by 'camis' and 'inspection_date' and check for nulls in 'violation_code'
                grouped = inspection_df.groupby(['camis', 'inspection_date'])
                groups_with_nulls = grouped.apply(lambda x: x['violation_code'].isna().any())

                # Count the number of rows in each group
                group_sizes = grouped.size()

                # Filter the DataFrame to include only those groups with nulls in 'violation_code' and at least 2 rows
                filtered_groups = groups_with_nulls[groups_with_nulls].index.intersection(group_sizes[group_sizes >= 2].index)
                filtered_df = inspection_df[inspection_df.set_index(['camis', 'inspection_date']).index.isin(filtered_groups)].reset_index(drop=True)

                # Now, 'filtered_df' contains only the groups where there are null values in 'violation_code' and at least 2 rows in the group
                filtered_df.sort_values(by='camis').head()
                '''
            )
            
            display_dataframe('inspections_camisg.csv')
            
            st.markdown(
                '''
                The data format clearly shows that individual violations from an inspection are recorded on separate rows. However, it's unusual to observe different types of inspections, such as 'Administrative Miscellaneous', occurring concurrently within a single visit. Notably, rows categorized under 'Administrative Miscellaneous' frequently present missing data in the 'score, 'violation_code' and 'violation_description' fields. The next step in our analysis involves determining the frequency of NaN values within the 'Administrative Miscellaneous' inspection category
                '''
            )
            
            st.code(
                '''
                # Group by 'inspection_type' and count null 'violation_code' entries
                null_score_count = inspection_df.groupby('inspection_type').apply(lambda x: x['score'].isnull().sum())

                # The result is a Series where the index is 'inspection_type' and the values are the counts of null 'violation_code'
                print(null_score_count)

                '''
            )
            
            st.code(
                '''
                inspection_type
                Administrative Miscellaneous / Compliance Inspection             99
                Administrative Miscellaneous / Initial Inspection              4899
                Administrative Miscellaneous / Re-inspection                    975
                Administrative Miscellaneous / Reopening Inspection              43
                Administrative Miscellaneous / Second Compliance Inspection       8
                Cycle Inspection / Compliance Inspection                          0
                Cycle Inspection / Initial Inspection                             0
                Cycle Inspection / Re-inspection                                  0
                Cycle Inspection / Reopening Inspection                           0
                Cycle Inspection / Second Compliance Inspection                   0
                Inter-Agency Task Force / Initial Inspection                      0
                Inter-Agency Task Force / Re-inspection                           0
                '''
            )
            
            st.markdown(
                '''
                The analysis reveals that all the missing 'score' rows are tied to various "Administrative" inspection types. This pattern suggests that "Administrative" inspections might be documenting a distinct category of violations, particularly given the occurrence of both "Administrative" and "Cycle" inspections within the same visit. This finding indicates a potential strategy to either deduce the score for these cases or consider the removal of "Administrative" inspection types from our dataset.
                '''
            )
            
            v_spacer(height=2, sb=False)
            
            st.markdown('#### Administrative inspections')
            
            st.markdown(
                '''
                To proceed effectively, it's important to closely examine the specific types of violations recorded under "Administrative" inspections. Understanding the nuances of these violations will assist in determining their relevance to our overall data analysis and their impact on the comprehensive scoring system.

                We filter the dataset to only include rows where 'inspection_type' starts with "Administrative" and then identified the unique 'violation_description' values to understand the nature of violations in "Administrative" inspections.
                '''
            )
            
            st.code(
                '''
                # Filter for rows where 'inspection_type' starts with "Administrative"
                administrative_rows = inspection_df[inspection_df['inspection_type'].str.startswith("Administrative")]

                # Get a count of each unique 'violation_description' in these rows
                violation_description_counts = administrative_rows['violation_description'].value_counts()

                # Display the counts
                violation_description_counts
                '''
            )
            
            

            display_styled_code_block(cn.violation_description, max_height=300)
            
            st.markdown(
                '''
                The analysis of "Administrative" inspections revealed that these primarily involve non-food safety violations, such as missing posters, signage, or documentation, rather than critical food safety issues. Common violations in "Administrative" inspections include:

                - Missing "Choking first aid" and "Alcohol and pregnancy" posters.
                - Failure to post or conspicuously post current letter grades or Grade Pending cards.
                - Providing certain items without customer request, such as plastic straws.
                '''
            )
            
            v_spacer(height=2, sb=False)
            
            st.markdown('#### Dropping Administrative inspections')
            
            st.markdown(
                '''
                Given that "Administrative" inspections do not contribute to our food safety analysis and mainly involve non-critical violations, we made the decision to drop rows where the 'inspection_type' starts with "Administrative." This step helps streamline the dataset and focuses our analysis on relevant food safety factors.
                '''
            )
            
            st.code(
                '''
                # Drop rows where 'inspection_type' starts with "Administrative"
                inspection_df = inspection_df[~inspection_df['inspection_type'].str.startswith("Administrative")]
                null_counts_by_column = inspection_df.isnull().sum()
                null_counts_by_column[null_counts_by_column > 0]
                '''
            )
            
            st.code(
                '''
                violation_code           438
                violation_description    438
                '''
            )
            
        with tab4:
            st.markdown('''
            ### Dealing with Nulls by Inspection Action
            
            In this section you will see how we dealt with the nulls in columns related to violation codes and descriptions by identifying data that could be inferred using the a combination of the Action and inspection type columns.
            ''')
            
            v_spacer(height=2, sb=False)
            
            st.markdown('#### Investigating remaining violation code nulls')
            st.markdown(
                '''
                As a result, the null values in the 'score' column have been successfully addressed, leaving no NaNs in this column. Moving forward, we will further investigate the remaining null values in the 'violation_code' and 'violation_description' columns to gain insights into their presence, even though their frequency is relatively low.
                
                Reevaluating Null Counts in inspection_type
                '''
            )
            
            st.code(
                '''
                # Group by 'inspection_type' and count null 'violation_code' entries
                null_violation_count = inspection_df.groupby('inspection_type').apply(lambda x: x['violation_code'].isnull().sum())
                null_violation_count
                '''
            )
            
            st.code(
                '''
                inspection_type
                Cycle Inspection / Compliance Inspection             2
                Cycle Inspection / Initial Inspection              256
                Cycle Inspection / Re-inspection                    40
                Cycle Inspection / Reopening Inspection             70
                Cycle Inspection / Second Compliance Inspection      0
                Inter-Agency Task Force / Initial Inspection        69
                Inter-Agency Task Force / Re-inspection              1
                dtype: int64
                '''
            )
            
            v_spacer(height=2, sb=False)
            
            st.markdown('#### Investigating nulls by "action"')
            st.markdown(
                '''
                As observed, the presence of null values in the 'violation_code' and 'violation_description' columns varies depending on the inspection type. While this insight doesn't directly explain why these nulls exist, it's a useful observation. To further investigate the underlying reasons behind these null values, we can analyze the 'action' column, which may provide more context.
                '''
            )
            
            st.code(
                '''
                violation_code_null = inspection_df[inspection_df['violation_code'].isna()]
                # Group by 'inspection_type' and count null 'violation_code' entries
                null_violation_count = violation_code_null.groupby('action').apply(lambda x: x['violation_code'].isnull().sum())
                null_violation_count
                '''
            )
            
            
            st.code(
                '''
                action
                Establishment re-opened by DOHMH.                               70
                No violations were recorded at the time of this inspection.    364
                Violations were cited in the following area(s).                  4
                
                Null count: 438
                '''
            )
            
            v_spacer(height=2, sb=False)
            
            st.markdown('#### Filling nulls indicating No Violations')
            st.markdown(
                '''
                Our analysis has revealed that a significant portion of the null values in the 'violation_code' and 'violation_description' columns are associated with inspections where no violations were recorded. To address this, we plan to replace these null values for the 'violation_code' column with "none" and for the 'violation_description' column with "No violations were recorded." 
                '''
            )
            
            st.code(
                '''
                # Identify rows where 'action' starts with the specified strings and 'violation_code' is null
                condition = inspection_df['violation_code'].isna() & inspection_df['action'].str.startswith("No violations were recorded at the time of this inspection.")

                # Update 'violation_code' and 'violation_description' for these rows
                inspection_df.loc[condition, ['violation_code', 'violation_description']] = ['none', 'No violations were recorded']

                violation_code_null = inspection_df[inspection_df['violation_code'].isna()]
                # Group by 'inspection_type' and count null 'violation_code' entries
                null_violation_count = violation_code_null.groupby('action').apply(lambda x: x['violation_code'].isnull().sum())
                null_violation_count
                '''
            )
            
            st.code(
                '''
                action
                Establishment re-opened by DOHMH.                  70
                Violations were cited in the following area(s).     4
                '''
            )
            
            st.markdown(
                '''
                To gain further clarity and address the remaining null values in the 'violation_code' and 'violation_description' columns, we will focus on a subset of rows related to reopening inspections. Specifically, we will examine these rows to understand why some of them have null values in these columns.
                '''
            )
            
            st.code(
                '''
                # Filter rows where 'inspection_type' starts with "Administrative"
                action_reopened = inspection_df[inspection_df['action'].str.startswith("Establishment re-opened by DOHMH")]
                action_reopened.head(5)
                '''
            )
            
            display_dataframe('action_reopened.csv')
            
            st.markdown(
                '''
                In the case of reopening inspections, we observed that some rows had NaN values in the violation code/description, while others had codes and descriptions, suggesting the absence of violations. Additionally, the "critical_flag" column contained 'Not Applicable' when no violations were present. We can reasonably assume that this indicates no violations were found during those inspections. Therefore, we will be replacing violation_code and violation_description NaNs with 'none' and 'No violations were recorded', respectively.
                '''
            )
            
            st.code(
                '''
                # Identify rows where 'action' starts with the specified strings and 'violation_code' is null
                condition = (inspection_df['violation_code'].isna() & 
                            inspection_df['action'].str.startswith("Establishment re-opened") &
                        ( inspection_df['critical_flag'] == 'Not Applicable'))

                # Update 'violation_code' and 'violation_description' for these rows
                inspection_df.loc[condition, ['violation_code', 'violation_description']] = ['none', 'No violations were recorded']
                '''
            )
            
            st.markdown('Reevaluating Null Counts After BIN Column Cleanup')
            
            st.code(
                '''
                # Create a DataFrame containing rows where 'violation_code' is null
                violation_code_null = inspection_df[inspection_df['violation_code'].isna()]

                # Group the DataFrame by 'action' and count null 'violation_code' entries for each group
                null_violation_count = violation_code_null.groupby('action').apply(lambda x: x['violation_code'].isnull().sum())

                # Display the count of null 'violation_code' entries for each 'action'
                null_violation_count
                '''
            )
            
            st.code(
                '''
                action
                Violations were cited in the following area(s).    4
                '''
            )
            
            display_dataframe('action_violationcited.csv')
            
            v_spacer(height=2, sb=False)
            
            st.markdown('#### Dropping remaining violations with nulls')
            
            st.markdown(
                '''
                We examined inspections with the action "Violations were cited in the following area(s)" which had a mix of nulls and codes in the violation_code column. Since we cannot determine what the code should be for these cases, we have made the decision to drop these rows.
                '''
            )
            
            st.code(
                '''
                inspection_df = inspection_df.drop(inspection_df[(inspection_df['violation_code'].isna()) &
                                                                (inspection_df['action'].str.startswith("Violations were cited in the following area(s)"))].index)
                '''
            )
            
            v_spacer(height=2, sb=False)
            

            
        with tab5:
            st.markdown('''
            ### Dealing Remaining Nulls and Zeros
            
            There are only a couple of nulls and zeros that need to be handled.
            ''')

            st.markdown(
                '''
                ### Phone

                There are only a few rows with nulls in this column. We can fill these remaining nulls with a common placeholder, such as '0000000000,':
                '''
            )
            
            st.code(
                '''
                # Fill remaining nulls in numerical columns with '0000000000'
                inspection_df['phone'].fillna('0000000000', inplace=True)

                # Reassessing the null counts in the dataset
                null_counts_by_column = inspection_df.isnull().sum()
                null_counts_by_column[null_counts_by_column > 0]
                '''
            )
            st.markdown('Reevaluating Null Counts After BIN Column Cleanup')
            st.code(
                '''
                
                '''
            )
            
            st.markdown(
                '''
                #### We have successfully addressed all the nulls in the DataFrame. 
                '''
            )
            
            st.code(
            '''    
            pd.DataFrame({
            'Numeric_Zero_Count': (inspection_df == 0).sum(),
            'String_Zero_Count': (inspection_df == '0').sum(),
            'Null_Count': (inspection_df.isna().sum()).sum()
            })
            '''
            )
            
            display_dataframe('null_zero_counts.csv', '##### Current Null & Zero Count', max_height= 200)
            
            
            st.markdown(
            '''
            #### Dealing with 0s

            ##### Building

            For the 'building' column, it appears to have some 0 values, but there's not much we can do about that, so we will leave it as is.

            ##### Score
            Regarding the 'score' column, we can infer that a score of 0 indicates no violations.
            '''
            )
            
        with tab6:
            
            st.markdown('''
            ### Dealing with Data Types'
            
            Here we will asses which data types need to be changed, and address formatting. 
            ''')
            
            v_spacer(2,False)
            
            st.markdown('''
            #### Initial Assessment
            
            Lets begin by taking an assessment of our dataframe. 
            ''')
            
            st.code('''
            null_zero_counts = pd.DataFrame({
                'Numeric_Zero_Count': (inspection_df == 0).sum(),
                'String_Zero_Count': (inspection_df == '0').sum(),
                'Null_Count': (inspection_df.isna().sum()).sum(),
                'Blank Count': (inspection_df == '').sum(),
                'Space Count': (inspection_df == ' ').sum(),
                'Data Types': inspection_df.dtypes
            })

            null_zero_counts
                    ''')
            
            display_dataframe('null_zero_counts.csv', '##### Current Null & Zero Count')
            
            v_spacer(height=2, sb=False)
            
            st.markdown('''
            For the most part, the dataframe is free of zeros, nulls and blanks. Most of datatypes are assigned properly. 
            
            We will be reviewing:
            
            Zeros:
            - Score
            - Building
            
            Floats:
            - 'zipcode', 
            - 'score', 
            - 'community_board', 
            - 'council_district', 
            - 'census_tract', 
            - 'bin', 
            - 'bbl'
            
            Formatting:
            - Phone
            - Inspection Date
            ''')
            
            v_spacer(height=2, sb=False)
            
            st.markdown(
            '''
            ### Score Column

            Prepare the 'score' column for numerical analysis, the following action has been taken.
            '''
            )
            
            st.code(
            '''    
            inspection_df['score'] = inspection_df['score'].astype(int)
            '''
            )
            
            v_spacer(height=2, sb=False)
            
            st.markdown(
            '''
            #### Building Column
            First, lets address the building column.
            '''
            )
            
            st.code(
            '''    
            inspection_df['building'].str.isalpha().any()
            '''
            )
            
            st.code(
            '''    
            True
            ''')
            
            v_spacer(height=2, sb=False)
            
            st.markdown(
            '''
            ### Float data type columns

            The following columns should exclusively contain whole numbers. Currently, they are in float type. To ensure their integrity:

            1. Verify if they consist of whole numbers.
            2. Convert them to integers to confirm the absence of special characters.
            3. Convert them back to strings, as these columns are categorical features.
            '''
            )
            
            st.code(
            '''    
            columns_to_check = ['zipcode', 'score', 'community_board', 'council_district', 'census_tract', 'bin', 'bbl']

            for column in columns_to_check:
                is_integer = (inspection_df[column] % 1 == 0).all()
                print(f"{column} Column: {is_integer}")
            '''
            )
            
            st.code(
            '''    
            zip code Column: True
            score Column: True
            community_board Column: True
            council_district Column: True
            census_tract Column: True
            bin Column: True
            bbl Column: True    
            '''
            )
            
            st.code(
            '''    
            for column in columns_to_check:
                inspection_df[column] = inspection_df[column].astype(int)
                inspection_df[column] = inspection_df[column].astype(str)
            '''
            )
            
            v_spacer(height=2, sb=False)
            
            st.markdown(
            '''
            ### Phone Column

            Lets work on the 'phone' column, we will perform the following steps:

            1. Remove all non-numerical characters from the 'phone' column.
            2. Replace missing or empty values with '1000000000' to avoid having all zeros.
            '''
            )
            
            st.code(
            '''    
            # Use regex to extract digits from the "phone" column
            inspection_df['phone'] = inspection_df['phone'].str.replace(r'\D', '', regex=True)
            # Remove blank or 0s placeholder with '1000000000'.
            inspection_df['phone'] = inspection_df['phone'].str.strip().replace(['', '0000000000'], '1000000000')
            '''
            )
            
            st.markdown(
            '''
            ## Inspection Date Column

            To standardize the 'inspection_date' column, we will follow these steps:

            1. Begin by printing the 'inspection_date' from the first row of the DataFrame to verify the initial format.
            2. Next, convert the 'inspection_date' column to datetime format and format it to display only the date in 'YYYY-MM-DD' format.
            3. Finally, print the 'inspection_date' from the first row of the DataFrame again to confirm that it has been standardized to 'YYYY-MM-DD'.
            '''
            )
            
            st.code(
            '''    
            # Print the 'inspection_date' from the first row of the DataFrame
            inspection_df.loc[0, 'inspection_date']
            '''
            )
            
            st.code(
            '''    
            '2021-09-12T00:00:00.000'
            '''
            )
            
            st.code(
            '''    
            # Convert the 'inspection_date' column to datetime and format it to display only the date (YYYY-MM-DD)
            inspection_df['inspection_date'] = pd.to_datetime(inspection_df['inspection_date']).dt.strftime('%Y-%m-%d')
            
            # Print the 'inspection_date' from the first row of the DataFrame
            inspection_df.loc[0, 'inspection_date']
            '''
            )
            
            st.code(
            '''    
            '2021-09-12'
            '''
            )
            
            st.markdown(
            '''
            The DataFrame 'inspection_df' has been thoroughly checked and cleaned, resulting in the following characteristics:

            - No null values exist in any of the columns.
            - The data types of the columns are appropriate.

            The data is now ready for further analysis and exploration. If you have any additional tasks or questions related to this DataFrame or any other topic, please feel free to ask.
            '''
            )
#the end