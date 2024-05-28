import streamlit as st
from src.debate import Debate
from src.panel import Panel, Judge
from src.utils import generate_loading_statements

# Variables
debate_styles = ["heated", "calm", "formal", "casual", "aggressive", "friendly"]
max_rounds = 6
min_rounds = 1
default_rounds = 2
model = "llama3"

# Declare input interface elements
form = st.form("user_input_form")
debate_stage = st.container(border = False)
sidebar = st.sidebar

## Input form
form.header("Drama Llama Debate Bot")
user_input_debate_topic = form.text_input("Enter the topic of the debate: ")
col1, col2 = form.columns(2)

with col1:
    user_input_style = st.selectbox("Choose a debate style: ", debate_styles)

with col2:
    user_input_number_of_rounds = int(st.number_input("Number of rounds (excl. opening statements): ", max_value=max_rounds, min_value=min_rounds, value=default_rounds))

start_button = form.form_submit_button("Start debate")

## Sidebar to display arguments
with sidebar:
    key_points, panel, transcript = st.tabs(["Key points", "Panel vote", "Transcript"])

    # key_points
    pro_header = key_points.subheader("Pro arguments")
    pro_placeholder = key_points.markdown("*Waiting for debate to start*")
    con_header = key_points.subheader("Con arguments")
    con_placeholder = key_points.markdown("*Waiting for debate to start*")
    bullet_placeholder = key_points.container()

with panel:
    panel_decision_placeholder = st.container()
    panel_decision_placeholder.write("Panel will vote once the debate is over.")

## Main debate stage
if start_button and user_input_debate_topic and user_input_style:

    # Initialize debate class
    db = Debate(model, user_input_debate_topic, user_input_style, user_input_number_of_rounds)
    panel = Panel(model, 5)
    
    with debate_stage:
        debate_stage.empty()
        # Streamlit logic
        with st.spinner("Thinking about my opening statement ..."):
            db.opening_arguments("favor", pro_placeholder, con_placeholder)
        
        with st.spinner("Preparing my opening remarks ..."):
            db.opening_arguments("opposition", pro_placeholder, con_placeholder)
        
        for i in range(db.number_of_rounds):

            with st.spinner(generate_loading_statements()):
                db.debate("favor", pro_placeholder, con_placeholder)        
            
            with st.spinner(generate_loading_statements()):
                db.debate("opposition", pro_placeholder, con_placeholder)
        
        with st.spinner("Wrapping up the debate ..."):
            panel.get_judgement(debate = db, container = panel_decision_placeholder)
            db.wrap_up(panel.decisions)
        
        db.add_full_transcript_to_sidebar(transcript)
        db.bullet_points(bullet_placeholder)

