import os
import streamlit as st
from streamlit_chat import message as st_message
from sqlalchemy import create_engine
from langchain.agents import Tool, initialize_agent
from langchain.chains.conversation.memory import ConversationBufferMemory

from llama_index import GPTSQLStructStoreIndex, LLMPredictor, ServiceContext
from llama_index import SQLDatabase as llama_SQLDatabase
from llama_index.indices.struct_store import SQLContextContainerBuilder
import matplotlib.pyplot as plt
import ast
import pandas as pd
import hmac

from constants import (
    DEFAULT_SQL_PATH,
    DEFAULT_GRANTS_TABLE_DESCRP,
    DEFAULT_LC_TOOL_DESCRP,
)
from utils import get_sql_index_tool, get_llm

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False


if not check_password():
    st.stop()  # Do not continue if check_password is not True.


@st.cache_resource
def initialize_index(
    llm_name, model_temperature, table_context_dict, api_key, sql_path=DEFAULT_SQL_PATH
):
    """Create the GPTSQLStructStoreIndex object."""
    llm = get_llm(llm_name, model_temperature, api_key)
    engine = create_engine(sql_path)
    sql_database = llama_SQLDatabase(engine)

    context_container = None
    if table_context_dict is not None:
        context_builder = SQLContextContainerBuilder(
            sql_database, context_dict=table_context_dict
        )
        context_container = context_builder.build_context_container()

    service_context = ServiceContext.from_defaults(llm_predictor=LLMPredictor(llm=llm))
    index = GPTSQLStructStoreIndex(
        [],
        sql_database=sql_database,
        sql_context_container=context_container,
        service_context=service_context,
    )

    return index


@st.cache_resource
def initialize_chain(llm_name, model_temperature, lc_descrp, api_key, _sql_index):
    """Create a custom agent and sql_index tool."""
    sql_tool = Tool(
        name="SQL Index",
        func=get_sql_index_tool(
            _sql_index, _sql_index.sql_context_container.context_dict
        ),
        description=lc_descrp,
    )
    llm = get_llm(llm_name, model_temperature, api_key=api_key)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    agent_chain = initialize_agent(
        [sql_tool],
        llm,
        agent="chat-conversational-react-description",
        verbose=True,
        memory=memory,
    )
    return agent_chain

st.title("Gates Foundation Grants")

llama_tab, lc_tab = st.tabs(["Table Agent", "Text Agent"])

api_key = st.secrets['OPENAI_API_KEY']
# llm_name = "gpt-3.5-turbo"
llm_name = "o1-preview"
model_temperature = 0.5
grants_table_descrp=DEFAULT_GRANTS_TABLE_DESCRP
table_context_dict = {"grants": grants_table_descrp}
use_table_descrp = True
lc_descrp=DEFAULT_LC_TOOL_DESCRP

with llama_tab:
    # st.subheader("Text2SQL with Llama Index")
    if st.button("Initialize Index", key="init_index_1"):
        st.session_state["llama_index"] = initialize_index(
            llm_name,
            model_temperature,
            table_context_dict if use_table_descrp else None,
            api_key,
        )

    if "llama_index" in st.session_state:
        query_text = st.text_input(
            "Query:", value="How much funding for Malaria by year?"
        )
        use_nl = False #st.checkbox("Return natural language response?")
        if st.button("Run Query") and query_text:
            with st.spinner("Getting response..."):
                try:
                    response = st.session_state["llama_index"].as_query_engine(synthesize_response=use_nl).query(query_text)
                    response_text = str(response)
                    response_sql = response.extra_info["sql_query"]
                    print(response_text) 
                except Exception as e:
                    response_text = "Error running SQL Query."
                    response_sql = str(e)

            try:
                fig, ax = plt.subplots()
                response_list = ast.literal_eval(response_text)
                print('response_list',response_list)
                
                df = pd.DataFrame()
                df['value']=[int(x[1]) for x in response_list]
                df['label']=[x[0] for x in response_list] 
                # df['value'] = pd.to_numeric(df['value'])
                print(df['value'])
                df = df.sort_values(by=['value'],ascending=False)
                print(df)
                st.bar_chart(df,x='label',y='value')
                st.dataframe(df)
            except:
                st.write('Sorry, cannot make a chart')

            # show_query = st.checkbox("Show SQL Query")
            # if show_query:            
            #     col1, col2 = st.columns(2)
            #     # with col1:
            #     st.text("SQL Result:")
            #     st.markdown(response_text)

            #     with col2:
            #     st.text("SQL Query:")
            #     st.markdown(response_sql)

with lc_tab:
    if st.button("Initialize Agent"):
        st.session_state["llama_index"] = initialize_index(
            llm_name,
            model_temperature,
            table_context_dict if use_table_descrp else None,
            api_key,
        )
        st.session_state["lc_agent"] = initialize_chain(
            llm_name,
            model_temperature,
            lc_descrp,
            api_key,
            st.session_state["llama_index"],
        )
        st.session_state["chat_history"] = []

    model_input = st.text_input(
        "Message:", value="What is the first grant funded?"
    )
    if "lc_agent" in st.session_state and st.button("Send"):
        model_input = "User: " + model_input
        st.session_state["chat_history"].append(model_input)
        with st.spinner("Getting response..."):
            try:
                response = st.session_state["lc_agent"].run(input=model_input)
            except Exception as e:
                print(e)
                response = "Error running query."
        st.session_state["chat_history"].append(response)

    if "chat_history" in st.session_state:
        for msg in st.session_state["chat_history"]:
            st_message(msg.split("User: ")[-1], is_user="User: " in msg)
