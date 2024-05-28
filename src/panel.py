import numpy as np
from langchain_community.llms import Ollama
from debate import Debate
import streamlit as st

class Panel:
    """Represents a panel of judges for a debate simulator.

    Attributes:
        llm (Ollama): The loaded model for the debate simulator.
        number_of_judges (int): The number of judges in the panel.
        judges (list): A list of Judge objects representing the panel of judges.
        decisions (dict): A dictionary to store the decisions of each judge.
    """
    def __init__(self, model, number_of_judges):
        self.llm = self.load_model(model)
        self.number_of_judges = number_of_judges
        self.judges = self.create_panel()
        self.decisions = {}
        
    def load_model(self, model) -> Ollama:
        """
        Load a model.

        Args:
            model (type): The type of the model to load.

        Returns:
            Ollama: An instance of the loaded model.
        """
        return Ollama(model=model)
    
    def create_panel(self) -> list:
        """Create a panel of judges.

        This method creates a panel of judges based on the specified number of judges.
        Each judge is assigned a unique identifier and a reference to the debate simulator.

        Returns:
            list: A list of Judge objects representing the panel of judges.
        """
        judges = []
        for i in range(self.number_of_judges):
            judges.append(Judge(i + 1, self.llm))
        
        return judges
    
    def get_judgement(self, debate: Debate, container: st.container) -> None:
        """Get the judgement of each judge for the given debate.

        Args:
            debate (Debate): The debate object containing the debate topic and arguments.
            container (st.container): The Streamlit container to display the judge's decisions.
        """
        debate_topic = debate.topic
        favor_arguments = debate.debate_dictionary["favor"]
        opposition_arguments = debate.debate_dictionary["opposition"]

        for judge in self.judges:
            decision = judge.judge_debate(debate_topic, favor_arguments, opposition_arguments)
            
            self.decisions['judge_' + str(judge.index)] = {
                "personality" : judge.personality,
                "reason" : decision,
            }

            container.empty()
            container.markdown(f"- **Judge {judge.index} ({judge.personality})**: {decision}")
        
class Judge:
    """Represents a judge in a debate.

    Attributes:
        index (int): The index of the judge.
        llm (function): The function used for making decisions.
        personality (str): The personality of the judge.

    Methods:
        __init__(self, index, llm): Initializes a Judge object.
        generate_personality(self): Generates a random personality for the judge.
        judge_debate(self, debate_topic, favor_arguments, opposition_arguments): Judges a debate and makes a decision.

    """

    def __init__(self, index: int, llm: Ollama):
        self.index = index
        self.llm = llm
        self.personality = self.generate_personality()

    def generate_personality(self):
        """Generates a random personality for the judge.

        Returns:
            str: The generated personality.

        """
        personalities = ["progressive", "conservative", "libertarian", "authoritarian", "centrist", "populist", "anarchist", "socialist", "environmentalist"]
        personality = np.random.choice(personalities)
        return personality
    
    def judge_debate(self, debate_topic: str, favor_arguments: str, opposition_arguments: str):
        """Judges a debate and makes a decision.

        Args:
            debate_topic (str): The topic of the debate.
            favor_arguments (str): The arguments in favor of the resolution.
            opposition_arguments (str): The arguments against the resolution.

        Returns:
            str: The decision made by the judge.

        """
        prompt = """
            You are a judge in a debate. \n
            The debate topic is: {debate_topic} \n
            Your personality is {personality}. This personality should influence your decision. \n
            Arguments in favor: {favor_arguments} \n
            Arguments in opposition: {opposition_arguments} \n
            Decide a winner. \n
            Respond in the following format: ONE sentence describing your position and if you vote for or against the resolution. \n
            DO NOT add any other information.
            """
        
        decision = self.llm(prompt.format(personality=self.personality,
                                          debate_topic=debate_topic,
                                          favor_arguments=favor_arguments,
                                          opposition_arguments=opposition_arguments))

        return decision
