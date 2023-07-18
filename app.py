import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Form·ADV · Chatbot",
    page_icon="chart_with_upwards_trend",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "# · Form·ADV · Chatbot · "
        },
    )
st.markdown(
    """
    <style>
    MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    footer:after {
        content:" · Crestone Capital LLC · ";
        visibility: visible;
        display: block;
        position: 'fixed';
        #background-color: red;
        padding: 10px;
        top: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
    )
st.markdown(
    "<div id='linkto_top'></div>",
    unsafe_allow_html=True
    )


@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')


@st.cache_data
def parse_data_file():
    file_location = "./data/labeled/form_adv_labeled_PROPERLY.csv"
    raw_data = pd.read_csv(file_location).sort_values('Business Name')
    company_list = ['All'] + sorted(list(raw_data['Business Name']))
    columns_query_list = sorted(list(raw_data.columns))
    return raw_data, company_list, columns_query_list


st.title(" · Form-ADV · Chatbot · ")
st.divider()

with st.expander("**Project Documentation**"):
    tab1, tab2, tab3, tab4 = st.tabs(["**About**", "**Instructions**", "**Outline**", "**Help**"])

    with tab1:
        st.markdown("**About The App:**")
        st.markdown("""
            - Competitor Profile / Comparative Analysis On Crestone's Peer Group (8)
            - Perform Q&A Via Custom FormADV Data Selection/Focus
            - Compare/ Contrast 1-8 Investment Advisors Specific Data Points
            - Review The Full Form-ADV For Any of The 8 IAs
            - Interact With Data, Create Custom Tables, Sort/Filter, & Download Data
        """)

    with tab2:
        st.markdown("**Instructions:**")
        st.markdown("""
            - Scroll Down The Page To Interact With Each Section
            - All Tables are interactive & User has the ability to sort each row/column within any table.
            - Additionally, All Tables are downloadable to users.
            - To download a table, locate & click the '**Press to Download**' button below the table
        """)

    with tab3:
        st.markdown("**App Sections:**")
        st.markdown("""
            - **Peer Group Form-ADV Data**
                - All 8 IA's FormADV Data
            - **Query Inputs**
                - Custom Selected FormADV Tables [1-8 Investment Advisor(s)]
                - Complete FormADV Data [1-8 Investment Advisor(s)]
            """)

    with tab4:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Help:**")
            st.markdown("""
                        - Help On how to use a Section:
                            - For directions/helpful-hints, Hover over the ? icon on the Right-Hand Side of the Page
                        - Help Reset/Reboot Webpage Cache
                            - For Help on if app is not loading correctly or is loading slowly.
                            - hit button below to reset/reboot webpage Cache.
                """)
            st.button(label="**Clear Cache**", help="", on_click=st.cache_data.clear())

        with col2:
            st.markdown("**IN CASE OF EMERGENCY:**")
            st.markdown("""
                    - Press the following keys: **F5**
                        - [This will Reload The Webpage]
                    - If nothing is happening try pressing the following keys: **fn + F5**
                """)
st.divider()


# SOURCE, WRANGLE, CLEAN, & PREPARE DATA
raw_data, company_list, columns_query_list = parse_data_file()


st.header("Peer Group Form-ADV Data")
st.markdown("- Most Recent Filings [2023]")
st.dataframe(raw_data.set_index('Business Name'), use_container_width=True)
st.download_button(
    label="**Press to Download**",
    data=convert_df(raw_data),
    file_name="Competitor Profile - Peer Group 8 - Complete Form ADV Data.csv",
    mime="text/csv",
    key='Download - Peer Group 8 - Complete Form ADV Data - csv'
    )
st.divider()


st.header("Query Inputs")
query_company = st.multiselect(
    label='**Select Company(s)**',
    options=company_list,
    default=company_list[0],
    help="\
        - This is a Multi-Select Box. \n\
        - Select 'All' For All 8 IAs. If 'All' is selected NO other option needs to be selected.\n\
        - Additionally User Can Manually Select 1-8 IAs.\n\
        - To begin, click into the box start typing. The available options will filter per your input.\n\
        - Clicking into the box will also pull up dropdown menu of pre-built options.\n\
        - To Remove A single Selected Option from The Box, Click on the 'x' icon that Option's Name.\n\
        - To Clear all Inputs in Box Click the 'X' on the Far-Right-Hand side of the Box."
    )
query = st.multiselect(
    label="**Select Field(s)**",
    options=columns_query_list,
    default=[
        'Address', 'Web Address', 'Total Number Of Offices',
        'Total Employees',
        'Total Number Of Employees - Performing Investment Advisory Functions Including Research',
        'Total Number Of Employees - Registered With 1+ State Securities Authorities As IAR',
        'Total Number Of Clients - Approximate Number Of Client With funds And Securities',
        'Approximate Total Number Of Clients - For Which Related Persons Have Custody',
        'Non-Discretionary Total Number Of Accounts',
        'Discretionary Total Number Of Accounts', 'Total Number Of Accounts',
        'Non-Discretionary Aum',
        'Discretionary Aum', 'Total Aum',
        ],
    help="\
        - This is a Multi-Select Box. \n\
        - The Options in This Multi-Select-Box are Various Fields From the FormADV.\n\
        - Be Advised, there are 140+ FormADV Fields Included\n\
        - To begin, click into the box start typing. The available options will filter per your input.\n\
        - Clicking into the box will also pull up dropdown menu of pre-built options.\n\
        - To Remove A single Selected Option from The Box, Click on the 'x' icon that Option's Name.\n\
        - To Clear all Inputs in Box Click the 'X' on the Far-Right-Hand side of the Box."
    )

col1, col2, col3, col4, col5 = st.columns(5)
with col3:
    run_query_button = st.button(label="Run Query", key='run_button', use_container_width=True)
st.divider()


if run_query_button:
    if query:
        with st.spinner(f"Generating Answer to your Query {query} for {query_company}"):
            if 'All' in query_company:
                company_list.remove('All')
                formatted_string = ", ".join([x.split()[0] for x in company_list])
                data = raw_data.copy().set_index('Business Name')[query]
                st.subheader(f"Peer Group - Select FormADV Data: {formatted_string}")
                st.dataframe(data, use_container_width=True)
                st.download_button(
                    label="**Press to Download**",
                    data=convert_df(data),
                    file_name="Competitor_Profile_PeerGroup8_Select_FormADV_Fields.csv",
                    mime="text/csv",
                    key='Download - Peer Group 8 - Select Form ADV Data - csv'
                    )
            else:
                try:
                    data_2 = raw_data[raw_data['Business Name'].isin(query_company)].set_index('Business Name')
                except Exception as e:
                    data_2 = raw_data[raw_data['Business Name'] == query_company].set_index('Business Name')
                    print(e)
                formatted_string = ", ".join([x.split()[0] for x in query_company])
                data_1 = data_2[query]

                st.subheader(f"{formatted_string} - Select FormADV Fields")
                st.dataframe(data_1, use_container_width=True)
                st.download_button(
                    label="**Press to Download**",
                    data=convert_df(data_1),
                    file_name=f"Competitor_Profile_{formatted_string}_Select_FormADV_Fields.csv",
                    mime="text/csv",
                    key=f'Download - {formatted_string} - Select Form ADV Fields - csv'
                    )
                st.divider()

                st.subheader(f"{formatted_string} - Complete Form ADV")
                st.dataframe(data_2.T, use_container_width=True)
                st.download_button(
                    label="**Press to Download**",
                    data=convert_df(data_2.T),
                    file_name=f"Competitor_Profile_{formatted_string}_Complete_FormADV.csv",
                    mime="text/csv",
                    key=f'Download - {formatted_string} - Complete Form ADV Data - csv'
                    )
                st.divider()
