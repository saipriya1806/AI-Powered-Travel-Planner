 
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
import os

# ✅ Fetch API Key
API_KEY = os.getenv("GOOGLE_API_KEY")

# ✅ Validate API Key
if not API_KEY:
    st.error("API key is missing! Please set GOOGLE_API_KEY.")

# Streamlit UI
st.title("AI-Powered Travel Planner")
st.write("Enter your travel details to get estimated travel costs for various travel modes including cab, train, bus, and flights.")

# User input fields
source = st.text_input("Source:")
destination = st.text_input("Destination:")

if st.button("Get Travel plan"):
    if source and destination:
        with st.spinner("Fetching travel options..."):
            # LangChain components
            chat_template = ChatPromptTemplate.from_messages([
                ("system", '''You are an AI-powered travel assistant that provides users with the best travel options.
                Given a source and destination, provide the distance, estimated travel costs, time, and different transport modes.'''),
                ("human", "Find travel options from {source} to {destination}.")
            ])

            chat_model = ChatGoogleGenerativeAI(api_key=API_KEY, model="gemini-2.0-flash-exp")
            parser = StrOutputParser()
            chain = chat_template | chat_model | parser
            response = chain.invoke({"source": source, "destination": destination})

            st.success("Estimated Travel Options and Costs:")
            for mode in response.split("\n"):
                st.write(mode)
    else:
        st.error("Please enter both source and destination.")
