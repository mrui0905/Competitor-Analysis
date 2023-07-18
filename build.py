import os
import json
import openai
import anthropic
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from sec_api import FormAdvApi, ExtractorApi

load_dotenv()
pd.set_option('display.max_columns', None)

openai.api_key = st.secrets['OPENAI_API_KEY']
form_adv_api = FormAdvApi(api_key=st.secrets['SEC_API_KEY'])
extractor_api = ExtractorApi(api_key=st.secrets['SEC_API_KEY'])
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


class Source_Form_ADV_Data:
    """
    A class used to source Form ADV data.
    ...
    Methods
    -------
    get_filings():
        Retrieves filings within a specified date range from the Form ADV API.
    extract_values(data):
        Extracts the dictionary from a list if the list contains a dictionary.
    transform_columns(df, columns):
        Transforms specified columns in a DataFrame by extracting dictionaries and normalizing JSON.
    run():
        Executes the process of retrieving, transforming, and saving Form ADV data.
    """

    def __init__(self):
        """
        Constructs all the necessary attributes for the Source_Form_ADV_Data object.
        """
        self.filings_df = r"data\clean\form_adv_filings_df.csv"
        self.filings_json = r"data\json\form_adv_filings.json"
        self.filings_json_unicode = r"data\json\form_adv_filings_unicode.json"


    def get_filings(self):
        """
        Retrieves filings within a specified date range from the Form ADV API.
        Returns
        -------
        tuple
            A tuple containing a list of all filings and a DataFrame of normalized filings.
        """
        query = {
            "query": {"query_string": {"query": "Filing.Dt:[2022-12-31 TO 2023-04-30]"}},
            "from": "0",
            "size": "50",
            "sort": [{"Filing.Dt": {"order": "desc"}}]
        }
        from_param = 0
        size_param = 50
        all_filings = []
        while True:
            query['from'] = from_param
            query['size'] = size_param
            response = form_adv_api.get_firms(query)
            filings = response['filings']
            if len(filings) == 0:
                break
            all_filings.extend(filings)
            from_param += size_param

        with open(self.filings_json, 'w') as file:
            json.dump(all_filings, file)

        with open(self.filings_json_unicode, 'w', encoding='utf-8') as file:
            json.dump(all_filings, file, ensure_ascii=False)

        filings_raw_df = pd.json_normalize(all_filings).sort_values('Info.FirmCrdNb').fillna('NA')
        filings_df = self.transform_columns(filings_raw_df.copy(), ['NoticeFiled.States', 'Rgstn', 'Filing'])

        return all_filings, filings_df


    def extract_values(self, data):
        """
        Extracts the dictionary from a list if the list contains a dictionary.
        Parameters
        ----------
        data : list
            A list potentially containing a dictionary.
        Returns
        -------
        dict
            The extracted dictionary if it exists, otherwise an empty dictionary.
        """
        if data and isinstance(data, list) and isinstance(data[0], dict):
            return data[0]
        else:
            return {}


    def transform_columns(self, df, columns):
        """
        Transforms specified columns in a DataFrame by extracting dictionaries and normalizing JSON.
        Parameters
        ----------
        df : DataFrame
            The DataFrame to transform.
        columns : list
            The columns to transform.

        Returns
        -------
        DataFrame
            The transformed DataFrame.
        """
        for col in columns:
            df[col] = df[col].apply(self.extract_values)
            new_data = pd.json_normalize(df[col])
            new_data.columns = [f"{col}_{c}" for c in new_data.columns]
            df = pd.concat([new_data, df], axis=1)
            df = df.drop(columns=col)
        df.columns = [col.split('.')[-1] for col in df.columns]
        df = df.sort_values('BusNm').set_index('BusNm').fillna('NA')
        df.to_csv(self.filings_df)
        return df


    def run(self):
        """
        Executes the process of retrieving, transforming, and saving Form ADV data.
        Returns
        -------
        tuple
            A tuple containing the raw JSON data and the transformed DataFrame.
        """
        form_adv_filings_json, form_adv_filings_df = self.get_filings()
        return form_adv_filings_json, form_adv_filings_df


form_adv_filings_json, form_adv_filings_df = Source_Form_ADV_Data().run()
print(form_adv_filings_df.head())
