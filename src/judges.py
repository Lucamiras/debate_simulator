import numpy as np
from langchain_community.llms import Ollama

class Panel:
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
    
    def create_panel(self):
        judges = []
        for i in range(self.number_of_judges):
            judges.append(Judge(i + 1, self.llm))
        
        return judges
    
    def get_judgement(self, debate, container):
        debate_topic = debate.topic
        favor_arguments = debate.debate_dictionary["favor"]
        opposition_arguments = debate.debate_dictionary["opposition"]

        for judge in self.judges:
            decision = judge.judge_debate(debate_topic, favor_arguments, opposition_arguments)
            
            self.decisions['judge_' + str(judge.index)] = {
                "personality" : judge.personality,
                "reason" : decision,
    
            }

            container.markdown(f"- **Judge {judge.index} ({judge.personality})**: {decision}")
        
class Judge:
    def __init__(self, index, llm):
        self.index = index
        self.llm = llm
        self.personality = self.generate_personality()

    def generate_personality(self):
        personalities = ["progressive", "conservative", "libertarian", "authoritarian", "centrist", "populist", "anarchist", "socialist", "environmentalist"]
        personality = np.random.choice(personalities)
        return personality
    
    def judge_debate(self, debate_topic, favor_arguments, opposition_arguments):
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
        
        decision = self.llm(prompt.format(personality = self.personality,
                                          debate_topic=debate_topic,
                                          favor_arguments=favor_arguments,
                                          opposition_arguments=opposition_arguments))

        return decision
