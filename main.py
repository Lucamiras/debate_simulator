import streamlit as st
from src.functions import load_model, initialize_debate_dictionary, summarize_arguments, opening_arguments, debate, generate_loading_statements

llm = load_model("llama3")

debater_one_start_prompt = """
    You are a debater having a {style} debate. The topic of the debate is: {topic}. You will go first.
    Please provide a starting argument in {side} of the topic. Keep it short and simple. Be {style}.
"""

debater_two_start_prompt = """
    You are a debater having a {style}. The topic of the debate is: {topic}. You will go second. 
    Please provide a starting argument in {side} of the topic. Keep it short and simple. Be {style}.
"""

summarize_prompt = """
    You are summarizing arguments from a debate. The topic of the debate is: {topic}. You just heard the following argument: {argument}.
    Please summarize the argument in one sentence. Return only the sentence.
"""

debater_one_follow_up_prompt = """
    You are still a debater having a {style} debate. The topic of the debate is still {topic}. The previous debater so far argued the following: {counter_args}.
    You already made the following points: {history}.
    Please provide a follow-up argument in {side} of the topic. Keep it short and simple.
    Be {style}.
"""

host_end_prompt = """
    You are the host of the debate. Please look at these python lists of arguments that were made in the debate about the following topic: {topic}.
    Arguments in favor of the position: {arguments_pro}.
    Arguments against the position: {arguments_con}.
    Please summarize each position in one paragraph, thank the audience and end the debate.
    Also declare a winner and explain which argument convinced you.
"""

# User interface
st.header("Drama Llama Debate Bot")
user_input_debate_topic = st.text_input("Enter the topic of the debate: ")
col1, col2 = st.columns(2)

with col1:
    user_input_style = st.selectbox("Choose a debate style:", ["heated", "calm", "formal", "casual", "aggressive", "friendly"])

with col2:
    user_input_number_of_rounds = int(st.number_input("Enter the number of rounds: ", max_value=10, min_value=1, value=3))

# Initialize dictionary to store debate arguments
debate_dictionary = initialize_debate_dictionary(user_input_debate_topic)

# Sidebar to display arguments
pro_header = st.sidebar.subheader("Pro arguments:")
pro_placeholder = st.sidebar.empty()
con_header = st.sidebar.subheader("Con arguments:")
con_placeholder = st.sidebar.empty()

if st.button("Start debate") and user_input_debate_topic and user_input_style:
    
    with st.spinner("Thinking about my opening statement ..."):
        opening_arguments(llm, user_input_debate_topic, debater_one_start_prompt, "favor", user_input_style)
    
    with st.spinner("Preparing my opening remarks ..."):
        opening_arguments(llm, user_input_style, debater_two_start_prompt, "opposition", user_input_style)
    
    for i in range(user_input_number_of_rounds):

        with st.spinner(generate_loading_statements()):
            debate(llm, user_input_debate_topic, debater_one_follow_up_prompt, debate_dictionary["opposition"], debate_dictionary["favor"], "favor", style=user_input_style)
            st.text(debate_dictionary)
        
        with st.spinner(generate_loading_statements()):
            debate(llm, user_input_debate_topic, debater_one_follow_up_prompt, debate_dictionary["favor"], debate_dictionary["opposition"], "opposition", style=user_input_style)
            st.text(debate_dictionary)

    st.write(debate_dictionary)

    with st.spinner("Wrapping up the debate ..."):
        st.header("Host summary:")
        final_statement = llm(host_end_prompt.format(
            topic=user_input_debate_topic, 
            arguments_pro=debate_dictionary["favor"], 
            arguments_con=debate_dictionary["opposition"]))
        st.write(final_statement)