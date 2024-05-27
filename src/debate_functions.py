import numpy as np
import streamlit as st
from langchain_community.llms import Ollama

def load_model(model) -> Ollama:
    """
    Load a model.

    Args:
        model (type): The type of the model to load.

    Returns:
        Ollama: An instance of the loaded model.
    """
    return Ollama(model=model)

def initialize_debate_dictionary(topic: str) -> dict:
    """Initialize a debate dictionary with the given topic.

    Args:
        topic (str): The topic of the debate.

    Returns:
        dict: A dictionary representing the debate with the following keys:
            - "topic": The topic of the debate.
            - "favor": An empty string representing the favor side of the debate.
            - "opposition": An empty string representing the opposition side of the debate.
    """
    debate_dictionary = {
        "topic": topic,
        "favor": "",
        "opposition": ""
    }
    return debate_dictionary

def summarize_arguments(llm: Ollama, 
                        topic: str, 
                        prompt: str, 
                        argument: str, 
                        side: str, 
                        debate_dictionary: dict, 
                        pro_placeholder, 
                        con_placeholder) -> None:
    """Summarizes the arguments for a given side in a debate.

    Args:
        llm (Ollama): The language model used for summarization.
        topic (str): The topic of the debate.
        prompt (str): The prompt template for generating summaries.
        argument (str): The argument to be summarized.
        side (str): The side of the debate (either "favor" or "opposition").
        debate_dictionary (dict): The dictionary storing the debate summaries.
        pro_placeholder (_type_): The placeholder for displaying the pro side summary.
        con_placeholder (_type_): The placeholder for displaying the con side summary.
    """
    summary = llm(prompt.format(topic=topic, argument=argument))
    debate_dictionary[side] += (" " + summary)
    
    if side == "favor":      
        pro_placeholder.markdown(debate_dictionary["favor"])

    if side == "opposition":
        con_placeholder.markdown(debate_dictionary["opposition"])
    
def opening_arguments(llm: Ollama, 
                      topic: str, 
                      debate_prompt: str,
                      summary_prompt: str,
                      debate_dictionary: dict,
                      side: str, 
                      style: str,
                      pro_placeholder,
                      con_placeholder) -> tuple:
    """Generate opening arguments for a debate.

    This function takes in various parameters and generates opening arguments for a debate based on the given topic,
    debate prompt, side, and style.

    Args:
        llm (Ollama): The language model used to generate the opening arguments.
        topic (str): The topic of the debate.
        debate_prompt (str): The prompt for the debate.
        side (str): The side of the debater (e.g., "Pro" or "Con").
        style (str): The style of the debate (e.g., "Formal" or "Informal").

    Returns:
        tuple: A tuple containing the subheader indicating the debater's side and the generated opening arguments.
    """
    arg = llm(debate_prompt.format(topic=topic, side=side, style=style))
    summarize_arguments(llm, topic, summary_prompt, arg, side, debate_dictionary, pro_placeholder, con_placeholder)
    return (
        st.subheader(f"Debater {side} starts:"),
        st.write(arg)
    )

def debate(llm: Ollama, 
           topic: str, 
           debate_prompt: str,
           summary_prompt: str,
           debate_dictionary: dict,
           last_summary: str, 
           history: str, 
           side: str, 
           style: str,
           pro_placeholder,
           con_placeholder) -> tuple:
    """Simulates a debate between two sides.

    Args:
        llm (Ollama): The language model used for generating responses.
        topic (str): The topic of the debate.
        debate_prompt (str): The prompt for the debate.
        last_summary (str): The summary of the previous arguments.
        history (str): The history of the debate.
        side (str): The side of the debater.
        style (str): The style of the debate.

    Returns:
        tuple: A tuple containing the subheader and the generated response.
    """
    arg = llm(debate_prompt.format(topic=topic, counter_args=last_summary, history=history, side=side, style=style))
    summarize_arguments(llm, topic, summary_prompt, arg, side, debate_dictionary, pro_placeholder, con_placeholder)
    return (
        st.subheader(f"Debater {side} responds:"),
        st.write(arg)
    )

def generate_loading_statements(custom_loading_texts: list = None) -> str:
    """Generate a random loading statement.

    This function generates a random loading statement while the debate bot is processing.

    Args:
        custom_loading_texts (list, optional): A list of custom loading texts to include. Defaults to None. If provided, the custom loading texts will be included in the list of loading statements.

    Returns:
        str: A randomly selected loading statement.

    Examples:
        >>> generate_loading_statements()
        'Thinking about my opening statement ...'

        >>> generate_loading_statements(["Loading data ...", "Preparing the model ..."])
        'Preparing the model ...'
    """
    loading_texts = [
        "Thinking about my opening statement ...",
        "Thinking about my next point ...",
        "Preparing my opening remarks ...",
        "Generating a follow-up argument ...",
        "Analyzing the counter-arguments ...",
        "Rebutting the opponent's points ...",
        "Crafting a response ...",
    ]

    if custom_loading_texts:
        loading_texts += custom_loading_texts

    choice = np.random.choice(
        loading_texts,
        1
    )

    return choice[0]
