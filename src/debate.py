import numpy as np
import streamlit as st
from langchain_community.llms import Ollama

class Debate:
    def __init__(self, model, topic, style, number_of_rounds):
        self.llm = self.load_model(model)
        self.topic = topic
        self.style = style
        self.number_of_rounds = number_of_rounds
        self.prompts = self.load_prompts()
        self.debate_dictionary = self.initialize_debate_dictionaries(topic)[0]
        self.full_transcript = self.initialize_debate_dictionaries(topic)[1]
        self.arg_counter = [1, 1]

    def load_model(self, model) -> Ollama:
        """
        Load a model.

        Args:
            model (type): The type of the model to load.

        Returns:
            Ollama: An instance of the loaded model.
        """
        return Ollama(model=model)
    
    def load_prompts(self):
        debater_one_start_prompt = """
            You are a debater having a {style} debate. 
            The topic of the debate is: {topic}. You will go first.
            Please provide a starting argument in {side} of the topic. 
            Keep it short and simple. 
            Do not add stage directions. This is a dialogue.
            Be {style}.
        """

        debater_two_start_prompt = """
            You are a debater having a {style} debate. 
            The topic of the debate is: {topic}. You will go second. 
            Please provide a starting argument in {side} of the topic. 
            Keep it short and simple. 
            Do not add stage directions. This is a dialogue.
            Be {style}.
        """

        summarize_prompt = """
            You are summarizing arguments from a debate. The topic of the debate is: {topic}. You just heard the following argument: {argument}.
            Please summarize the argument in one sentence. Return only the sentence.
        """

        summarize_into_bullet_list = """
            Please summarize this paragraph's main points as brief bullet points: {paragraph}.
            Return the bullet points as markdown unordered lists. Each bullet needs to be written in a new line.
            Do not add anything before or after.
        """

        debater_follow_up_prompt = """
            You are still a debater having a {style} debate. 
            The topic of the debate is still {topic}. 
            The previous debater so far argued the following: {counter_args}.
            You already made the following points: {history}.
            Please provide a follow-up argument in {side} of the topic. Keep it short and simple.
            Do not add stage directions. This is a dialogue.
            Be {style}.
        """

        host_end_prompt = """
            You are the host of the debate. Please look at these python lists of arguments that were made in the debate about the following topic: {topic}.
            Arguments in favor of the position: {arguments_pro}.
            Arguments against the position: {arguments_con}.
            Please summarize each position in one paragraph, thank the audience and end the debate.
            Also declare a winner and explain which argument convinced you.
        """
        
        prompt_dictionary = {
            "debater_one_start_prompt": debater_one_start_prompt,
            "debater_two_start_prompt": debater_two_start_prompt,
            "summarize_prompt": summarize_prompt,
            "summarize_into_bullet_list": summarize_into_bullet_list,
            "debater_follow_up_prompt": debater_follow_up_prompt,
            "host_end_prompt": host_end_prompt
        }

        return prompt_dictionary

    def initialize_debate_dictionaries(self, topic: str) -> dict:
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
        transcript_dictionary = {
            "topic": topic,
            "number_of_rounds": self.number_of_rounds,
        }
        return debate_dictionary, transcript_dictionary

    def summarize_arguments(self, 
                            argument: str, 
                            side: str,
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
        summary = self.llm(self.prompts["summarize_prompt"].format(topic=self.topic, argument=argument))
        self.debate_dictionary[side] += (" " + summary)
        
        if side == "favor":      
            pro_placeholder.markdown(self.debate_dictionary["favor"])

        if side == "opposition":
            con_placeholder.markdown(self.debate_dictionary["opposition"])
    
    def opening_arguments(self,
                          side: str, 
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

        if side == "favor":
            debate_prompt = self.prompts["debater_one_start_prompt"]
        
        if side == "opposition":
            debate_prompt = self.prompts["debater_two_start_prompt"]

        arg = self.llm(debate_prompt.format(topic=self.topic, side=side, style=self.style))
        self.full_transcript["opening_arguments_" + side] = arg
        self.summarize_arguments(arg, side, pro_placeholder, con_placeholder)
        return (
            st.subheader(f"Debater in {side} starts:"),
            st.write(arg)
        )

    def debate(self,
               side: str, 
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
        if side == "favor":
            debate_prompt = self.prompts["debater_follow_up_prompt"]
            last_summary = self.debate_dictionary["opposition"]
            history = self.debate_dictionary["favor"]
            counter = self.arg_counter[0]
            self.arg_counter[0] += 1
        if side == "opposition":
            debate_prompt = self.prompts["debater_follow_up_prompt"]
            last_summary = self.debate_dictionary["favor"]
            history = self.debate_dictionary["opposition"]
            counter = self.arg_counter[1]
            self.arg_counter[1] += 1

        arg = self.llm(debate_prompt.format(topic=self.topic, counter_args=last_summary, history=history, side=side, style=self.style))
        self.full_transcript["argument_" + side + '_' + str(counter)] = arg
        self.summarize_arguments(arg, side, pro_placeholder, con_placeholder)
        return (
            st.subheader(f"Debater {side} responds:"),
            st.write(arg)
        )
    
    def wrap_up(self) -> str:
        """Wrap up the debate and return a summary.

        Returns:
            str: A summary of the debate, including the topic, arguments in favor, and arguments in opposition.
        """
        final_statement = self.llm(self.prompts["host_end_prompt"].format(topic=self.topic,
                                                                          arguments_pro=self.debate_dictionary["favor"],
                                                                          arguments_con=self.debate_dictionary["opposition"]))    
        return (
            st.header("Host summary:"),
            st.write(final_statement)
        )
    
    def bullet_points(self, container: st.container) -> str:
        """Generate bullet points for pro and con arguments.

        Args:
            container (st.container): The container to display the bullet points.

        Returns:
            str: The generated bullet points as a string.
        """
        pro_bullets = self.llm(self.prompts["summarize_into_bullet_list"].format(paragraph=self.debate_dictionary["favor"]))
        con_bullets = self.llm(self.prompts["summarize_into_bullet_list"].format(paragraph=self.debate_dictionary["opposition"]))

        container.subheader("Pro bullets")
        container.markdown(pro_bullets)
        container.subheader("Con bullets")
        container.markdown(con_bullets)
    
    def add_full_transcript_to_sidebar(self, container: st.container) -> None:
            """Add the full transcript to the sidebar container.

            This method clears the container and writes the full transcript to it.

            Args:
                container (st.container): The container to which the full transcript will be added.
            """
            container.empty()
            container.write(self.full_transcript)
    
    