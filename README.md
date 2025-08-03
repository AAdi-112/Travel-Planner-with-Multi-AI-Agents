# Travel-Planner-with-Multi-AI-Agents
A personalized travel itinerary planner built using LangGraph, leveraging multiple collaborative AI agents to generate customized trip recommendations based on user preferences, constraints, and real-time data.
##  Features

-  **Multi-agent conversational flow** using `LangGraph` for state-based planning
-  **Custom itinerary generation** using LLaMA 3.3 (70B Versatile) from GROQ
-  Real-time user input and conversational UX using `Streamlit`
-  Secure API handling via `Streamlit Secrets Manager`
-  Fully deployed and accessible on **Streamlit Cloud**
-  ## 🛠 Tech Stack

| Category        | Tools/Tech Used                     |
|----------------|-------------------------------------|
| Language        | Python                              |
| LLM             | [LLaMA 3.3 70B Versatile](https://groq.com/) via [GROQ API](https://console.groq.com/) |
| UI Framework    | Streamlit                           |
| Agent Logic     | LangGraph, LangChain                |
| State Handling  | `session_state` in Streamlit        |
| Deployment      | Streamlit Community Cloud           |
| Version Control | Git, GitHub                         |






## How It Works
LangGraph Multi-Agent Design:
input_city → Prompts user to enter the destination city.

input_interest → Collects user interests related to the trip.

create_itinerary → Calls LLaMA 3 via GROQ API to generate a personalized day-trip itinerary.

Each node updates the internal PlannerState and transitions using a directed state graph (StateGraph).



##Example Prompt Flow
User: "I want to plan a day trip"

App: "Which city do you want to visit?"

User: "Bangalore"

App: "What are your interests for this trip?"

User: "nature, food, museums"

App:  Generates a bulleted itinerary with LLaMA 3 via GROQ



