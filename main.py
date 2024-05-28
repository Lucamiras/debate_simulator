import streamlit as st
from src.debate import Debate
from src.utils import generate_loading_statements

# Input interface
st.header("Drama Llama Debate Bot")
user_input_debate_topic = st.text_input("Enter the topic of the debate: ")
col1, col2 = st.columns(2)

with col1:
    user_input_style = st.selectbox("Choose a debate style:", ["heated", "calm", "formal", "casual", "aggressive", "friendly"])

with col2:
    user_input_number_of_rounds = int(st.number_input("Enter the number of rounds: ", max_value=10, min_value=1, value=3))

start_button = st.button("Start debate")
divider = st.divider()

# Sidebar to display arguments
pro_header = st.sidebar.subheader("Pro arguments:")
pro_placeholder = st.sidebar.empty()
con_header = st.sidebar.subheader("Con arguments:")
con_placeholder = st.sidebar.empty()

# Main debate stage
if start_button and user_input_debate_topic and user_input_style:

    # Initialize debate class
    Debate = Debate("llama3", user_input_debate_topic, user_input_style)
    
    # Streamlit logic
    with st.spinner("Thinking about my opening statement ..."):
        Debate.opening_arguments("favor", pro_placeholder, con_placeholder)
    
    with st.spinner("Preparing my opening remarks ..."):
        Debate.opening_arguments("opposition", pro_placeholder, con_placeholder)
    
    for i in range(user_input_number_of_rounds):

        with st.spinner(generate_loading_statements()):
            Debate.debate("favor", pro_placeholder, con_placeholder)        
        
        with st.spinner(generate_loading_statements()):
            Debate.debate("opposition", pro_placeholder, con_placeholder)
    
    with st.spinner("Wrapping up the debate ..."):
        Debate.wrap_up()


