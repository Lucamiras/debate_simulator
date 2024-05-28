def load_prompts():
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

    debater_one_follow_up_prompt = """
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
        "debater_one_follow_up_prompt": debater_one_follow_up_prompt,
        "host_end_prompt": host_end_prompt
    }

    return prompt_dictionary