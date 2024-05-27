import streamlit as st
from src.debate_functions import load_model, initialize_debate_dictionary, summarize_arguments, opening_arguments, debate, generate_loading_statements
from src.prompts import load_prompts

# Load language model
llm = load_model("llama3")

# Load prompts
debater_one_start_prompt, debater_two_start_prompt, summarize_prompt, debater_one_follow_up_prompt, host_end_prompt = load_prompts()

# Construct user interface
st.header("Drama Llama Debate Bot")
user_input_debate_topic = st.text_input("Enter the topic of the debate: ")
debate_dictionary = initialize_debate_dictionary(user_input_debate_topic)

col1, col2 = st.columns(2)

with col1:
    user_input_style = st.selectbox("Choose a debate style:", ["heated", "calm", "formal", "casual", "aggressive", "friendly"])

with col2:
    user_input_number_of_rounds = int(st.number_input("Enter the number of rounds: ", max_value=10, min_value=1, value=3))

# Sidebar to display arguments
pro_header = st.sidebar.subheader("Pro arguments:")
pro_placeholder = st.sidebar.empty()
con_header = st.sidebar.subheader("Con arguments:")
con_placeholder = st.sidebar.empty()

# Main debate stage
if st.button("Start debate") and user_input_debate_topic and user_input_style:
    
    with st.spinner("Thinking about my opening statement ..."):
        opening_arguments(llm, user_input_debate_topic, debater_one_start_prompt, summarize_prompt, debate_dictionary, "favor", user_input_style, pro_placeholder, con_placeholder)
    
    with st.spinner("Preparing my opening remarks ..."):
        opening_arguments(llm, user_input_debate_topic, debater_two_start_prompt, summarize_prompt, debate_dictionary, "opposition", user_input_style, pro_placeholder, con_placeholder)
    
    for i in range(user_input_number_of_rounds):

        with st.spinner(generate_loading_statements()):
            debate(llm, user_input_debate_topic, debater_one_follow_up_prompt, summarize_prompt, debate_dictionary, debate_dictionary["opposition"], debate_dictionary["favor"], "favor", user_input_style, pro_placeholder, con_placeholder)        
        
        with st.spinner(generate_loading_statements()):
            debate(llm, user_input_debate_topic, debater_one_follow_up_prompt, summarize_prompt, debate_dictionary, debate_dictionary["favor"], debate_dictionary["opposition"], "opposition", user_input_style, pro_placeholder, con_placeholder)

    with st.spinner("Wrapping up the debate ..."):
        st.header("Host summary:")
        final_statement = llm(host_end_prompt.format(
            topic=user_input_debate_topic,
            arguments_pro=debate_dictionary["favor"],
            arguments_con=debate_dictionary["opposition"]))
        st.write(final_statement)