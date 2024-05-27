from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import SequentialChain, SimpleSequentialChain
from langchain_community.llms import Ollama
import numpy as np

import streamlit as st
import toml

# set up model
llm = Ollama(model="llama3")

debater_one_start_prompt = """
    You are a debater having a {style} debate. The topic of the debate is: {topic}. You will go first.
    Please provide a starting argument in {side} of the topic. Keep it short and simple. Be {style}.
""" # in favor

debater_two_start_prompt = """
    You are a debater having a {style}. The topic of the debate is: {topic}. You will go second. 
    Please provide a starting argument in {side} of the topic. Keep it short and simple. Be {style}.
""" # opposing

summarize_prompt = """
    You are summarizing arguments from a debate. The topic of the debate is: {topic}. You just heard the following argument: {argument}.
    Please summarize the argument in one sentence. Return only the sentence.
"""

#summarize_bullets = """
#    Summarize this paragraph into two to five word bullet points. The paragraph is: {paragraph}. Return only the bullet points. Return them as markdown.
#"""

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
debate_dictionary = {
    "topic": user_input_debate_topic,
    "favor": "",
    "opposition": ""
}

# Sidebar to display arguments
pro_header = st.sidebar.subheader("Pro arguments:")
pro_placeholder = st.sidebar.empty()
con_header = st.sidebar.subheader("Con arguments:")
con_placeholder = st.sidebar.empty()

# Functions
def summarize_arguments(argument, side):
    summary = llm(summarize_prompt.format(topic=user_input_debate_topic, argument=argument))
    debate_dictionary[side] += (" " + summary)
    # summary_bullets = llm(summarize_bullets.format(paragraph=summary))
    
    if side == "favor":      
        pro_placeholder.markdown(debate_dictionary["favor"])

    elif side == "opposition":
        con_placeholder.markdown(debate_dictionary["opposition"])
    
def opening_arguments(debate_prompt, side, style=user_input_style):
    arg = llm(debate_prompt.format(topic=user_input_debate_topic, side=side, style=user_input_style))
    summarize_arguments(arg, side)
    return (
        st.subheader(f"Debater {side} starts:"),
        st.write(arg)
    )

def debate(debate_prompt, last_summary, history, side, style=user_input_style):
    arg = llm(debate_prompt.format(topic=user_input_debate_topic, counter_args=last_summary, history=history, side=side, style=user_input_style))
    summarize_arguments(arg, side)
    return (
        st.subheader(f"Debater {side} responds:"),
        st.write(arg)
    )

def generate_loading_statements():
    choice = np.random.choice(
        [
            "Thinking about my next argument ...",
            "Preparing my next argument ...",
            "Let me think about this ...",
            "I'm thinking ...",
            "Let me think ...",
            "Let me think about this ...",
            "Let me think about my next argument ...",
            "What could I respond to this?"
         ],
         1
    )
    return choice[0]

if st.button("Start debate") and user_input_debate_topic and user_input_style:
    
    with st.spinner("Thinking about my opening statement ..."):
        opening_arguments(debater_one_start_prompt, "favor")
    
    with st.spinner("Preparing my opening remarks ..."):
        opening_arguments(debater_two_start_prompt, "opposition")
    
    for i in range(user_input_number_of_rounds):

        with st.spinner(generate_loading_statements()):
            debate(debater_one_follow_up_prompt, debate_dictionary["opposition"], debate_dictionary["favor"], "favor", style=user_input_style)
            st.text(debate_dictionary)
        
        with st.spinner(generate_loading_statements()):
            debate(debater_one_follow_up_prompt, debate_dictionary["favor"], debate_dictionary["opposition"], "opposition", style=user_input_style)
            st.text(debate_dictionary)

    st.write(debate_dictionary)

    with st.spinner("Wrapping up the debate ..."):
        st.header("Host summary:")
        final_statement = llm(host_end_prompt.format(
            topic=user_input_debate_topic, 
            arguments_pro=debate_dictionary["favor"], 
            arguments_con=debate_dictionary["opposition"]))
        st.write(final_statement)