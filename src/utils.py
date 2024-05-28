
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
