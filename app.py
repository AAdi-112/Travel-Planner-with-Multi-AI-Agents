import streamlit as st
from typing import TypedDict, Annotated, List
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import os

# Define the PlannerState (copy from your notebook)
class PlannerState(TypedDict):
  messages : Annotated[List[HumanMessage | AIMessage], "the messages in the conversation"]
  city: str
  interests: List[str]
  itinerary: str

# Initialize the LLM (copy from your notebook, ensure GROQ_API_KEY is set in Streamlit secrets)
# Make sure to set up your GROQ_API_KEY in Streamlit secrets
 
if "GROQ_API_KEY" not in st.secrets:
    st.error("GROQ_API_KEY not found. Please set it in Streamlit secrets.")
    st.stop()

groq_api_key = st.secrets["GROQ_API_KEY"]


llm = ChatGroq(
   temperature = 0,
   groq_api_key = groq_api_key,
   model_name = "llama-3.3-70b-versatile"
)

# Define the prompt template (copy from your notebook)
itinerary_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful travel assistant. Create a day trip itinerary for {city} based on the user's interests: {interests}. Provide a brief, bulleted itinerary."),
    ("human", "Create an itinerary for my day trip."),
])


# Define the agent functions (copy from your notebook)
def input_city(state: PlannerState) -> PlannerState:
         st.write("Please enter the city you want to visit for your day trip: ")
         user_message = st.text_input("Your Input (City):", key="city_input")
         if user_message:
             return {
                  **state,
                  "city": user_message,
                  "messages": state['messages'] + [HumanMessage(content=user_message)]
              }
         return state # Return current state if no input

def input_interest(state: PlannerState) -> PlannerState:
          st.write(f"Please enter your interest for the trip to : {state['city']} (comma-separted): ")
          user_message = st.text_input(f"Your Input (Interests for {state['city']}):", key="interests_input")
          if user_message:
              return {
                  **state,
                  "interests": [interest.strip() for interest in user_message.split(",")],
                  "messages": state['messages'] + [HumanMessage(content=user_message)]
              }
          return state # Return current state if no input

def create_itinerary(state: PlannerState) -> PlannerState:
          st.write(f"Creating an itinerary for {state['city']} based on interests : {', '.join(state['interests'])}")
          response = llm.invoke(itinerary_prompt.format_messages(city = state['city'], interests = ','.join(state['interests'])))
          st.write("Final Itinerary: ")
          st.markdown(response.content) # Use markdown to display the bulleted list
          return {
              **state,
              "messages": state['messages'] + [AIMessage(content=response.content)],
              "itinerary" : response.content,
          }

# Create and compile the graph (copy from your notebook)
workflow = StateGraph(PlannerState)

workflow.add_node("input_city", input_city)
workflow.add_node("input_interest", input_interest)
workflow.add_node("create_itinerary", create_itinerary)

workflow.set_entry_point("input_city")

workflow.add_edge("input_city", "input_interest")
workflow.add_edge("input_interest", "create_itinerary")
workflow.add_edge("create_itinerary", END)

app = workflow.compile()

# Streamlit App
st.title("Day Trip Planner")

if 'state' not in st.session_state:
    st.session_state.state = {
        "messages": [],
        "city": "",
        "interests": [],
        "itinerary": "",
    }

user_request = st.text_input("Enter your request (e.g., 'I want to plan a day trip'):")

if user_request and not st.session_state.state["city"]:
    st.session_state.state["messages"].append(HumanMessage(content=user_request))
    for output in app.stream(st.session_state.state, {'recursion_limit': 50}):
        for key, value in output.items():
            st.session_state.state.update(value)
            # Streamlit reruns the script on every interaction, so we need to handle state changes carefully.
            # The input_city and input_interest nodes will update the state and trigger reruns.
            # The create_itinerary node will display the final result and end the graph.

# Display the itinerary if available
if st.session_state.state["itinerary"]:
    st.subheader("Your Itinerary:")
    st.markdown(st.session_state.state["itinerary"])