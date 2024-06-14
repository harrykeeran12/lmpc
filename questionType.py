class QuestionType:
    """This class houses the different types of questions, and the prompts, that can be created by the program for each paper.
    Parameters:
    name: str - the name of the question type.
    systemPrompt: str - the initial prompt that should be added to generate the questions.
    examplePrompt: str - any example questions that would aid in generation.
    """

    def __init__(self, name: str, systemPrompt: str, examplePrompt: str = None) -> None:
        self.name = name
        self.systemPrompt = systemPrompt
        self.examplePrompt = examplePrompt
