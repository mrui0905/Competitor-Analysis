import streamlit as st
from sec_api import FormAdvApi
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

form_adv_api = FormAdvApi(api_key=st.secrets['SEC_API_KEY'])
client = Anthropic(api_key=st.secrets['ANTHROPIC_API_KEY'])
# client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

st.title("📝 File Q&A")

uploaded_file = st.file_uploader("Upload A File", type=("txt", "md", "csv"))

competitor_list = [
    'CRESTONE ASSET MANAGEMENT LLC',
    'CRESSET PARTNERS LLC',
    'PROVENIO CAPITAL',
    'JOHNSON FINANCIAL GROUP LLC',
    'SEVEN POST INVESTMENT OFFICE LP',
    'BBR PARTNERS, LLC',
    'GRESHAM INVESTMENT MANAGEMENT LLC',
    'HIRTLE, CALLAGHAN & CO., LLC'
]

select_IA = st.selectbox(label='Select Investment Adviser', options=competitor_list, index=1)

if select_IA == competitor_list[1]:

    st.markdown(
        """
        [Cresset Form ADV](https://reports.adviserinfo.sec.gov/reports/ADV/288566/PDF/288566.pdf)
        \n
        [Cresset Brochure](https://files.adviserinfo.sec.gov/IAPD/Content/Common/crd_iapd_Brochure.aspx?BRCHR_VRSN_ID=850944)
        """
    )

question = st.text_input(
    "Ask something about the file",
    placeholder="Can you give me a short summary?",
    disabled=not uploaded_file,
)


if st.button('Run Query'):
    if uploaded_file and question:
        article = uploaded_file.read().decode()
        prompt = f"""{HUMAN_PROMPT} Here's an article that I will ask you a question about:\n\n<article>
        {article}\n\n</article>\n\n Here is the question: {question}{AI_PROMPT}"""

        response = client.completions.create(
            model="claude-2",
            max_tokens_to_sample=500,
            prompt=f"{HUMAN_PROMPT} {prompt} {AI_PROMPT}",
            timeout=30,
            # temperature=0.70,
        )

        st.write("### Answer")
        st.write(response.completion)


# if st.button('Run Query'):
#     if uploaded_file and question:
#         article_lines = []
#         for line in uploaded_file:
#             article_lines.append(line.decode())
#         article = ''.join(article_lines)

#         prompt = f"""{HUMAN_PROMPT} Here's an article:\n\n<article>
#         {article}\n\n</article>\n\n{question}{AI_PROMPT}"""

#         response = client.completions.create(
#             model="claude-2",
#             max_tokens_to_sample=500,
#             prompt=f"{HUMAN_PROMPT} {prompt} {AI_PROMPT}",
#             timeout=30,
#         )

#         st.write("### Answer")
#         st.write(response.completion)


# def process_chunk(chunk, question):
#     prompt = f"""{HUMAN_PROMPT} Here's an article:\n\n<article>
#     {chunk}\n\n</article>\n\n{question}{AI_PROMPT}"""
#     response = client.completions.create(
#         model="claude-2",
#         max_tokens_to_sample=500,
#         prompt=f"{HUMAN_PROMPT} {prompt} {AI_PROMPT}",
#         timeout=30,
#     )
#     return response.completion

# if st.button('Run Query'):
#     if uploaded_file and question:
#         article = uploaded_file.read().decode()
#         chunks = [article[i:i+5000] for i in range(0, len(article), 5000)]  # Break the article into chunks of 5000 characters each

#         st.write("### Answer")
#         st.write(f"This Document is broken up into {len(chunks)} chunks.")
#         for chunk in chunks:
#             response = process_chunk(chunk, question)
#             st.write(response)
