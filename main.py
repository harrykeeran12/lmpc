from httpx import ConnectError
import ollama
import typing
import subprocess
import streamlit as st
from pypdf import PdfReader
# Check if models are installed or not.
try:
    # print("Installed models on local ollama instance:")
    # print(ollama.list())
    INSTALLEDMODELS: list[str] = []
    for modelName in ollama.list()["models"]:
        # print(modelName["name"])
        INSTALLEDMODELS.append(modelName["name"])
except ConnectError:
    raise Exception(
        "ollama server is not online. \nUse ollama serve to run the ollama daemon.")


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


short = QuestionType(
    "short", "You must generate short questions that are clear to understand.")
long = QuestionType(
    "long", "You must generate long answer questions. Examples include essay questions.")
mcq = QuestionType(
    "mcq", "You must generate short multiple choice questions that can be answered using one sentence. Do not return the answers or options.", )
ALLQUESTIONTYPES: dict[str, QuestionType] = {}

ALLQUESTIONTYPES[short.name] = short
ALLQUESTIONTYPES[long.name] = long
ALLQUESTIONTYPES[mcq.name] = mcq


class MockPaperGenerator():
    """This class encapsulates all the mock paper items that need to be included. Checks are run to make sure the data can be validated.
    Parameters: 
    QUESTIONTYPE: str - a string(default is short)
    MODELNAME: str - A model name supported by Ollama.
    NOTEFILE: str - A path to where the notes are stored, so that they can all be read beforehand.  
    QUESTIONNUMBER: int - The number of questions.
    TOTALMARKS: int - The number of marks."""

    def __init__(self, QUESTIONTYPE: str = "short", MODELNAME: str = "phi3:mini", NOTEFILE: str = "notes.txt", QUESTIONNUMBER: int = 5, TOTALMARKS: int = 10) -> None:
        self.QUESTIONTYPE = QUESTIONTYPE
        self.MODELNAME = MODELNAME
        self.NOTEFILE = NOTEFILE
        self.QUESTIONNUMBER = QUESTIONNUMBER
        self.TOTALMARKS = TOTALMARKS

        if MODELNAME not in INSTALLEDMODELS:
            raise Exception(f"Model name {MODELNAME} not in installed models.")
        else:
            ollama.pull(MODELNAME)
        try:
            with open(NOTEFILE, "r") as questionTemplate:
                self.NOTES: str = "".join(questionTemplate.readlines())
        except FileNotFoundError:
            raise Exception(f"Could not find {NOTEFILE}.")

        if QUESTIONNUMBER > 5 or QUESTIONNUMBER < 2:
            raise Exception("Question amount not suitable.")

        if TOTALMARKS // QUESTIONNUMBER < 1:
            raise Exception("Number of marks is too low.")

        if QUESTIONTYPE not in ALLQUESTIONTYPES.keys():
            raise Exception("Invalid question type.")

        self.prompt()
        self.generate()
        self.texTemplate()
        self.compileTeX("exam_1.tex")

    def rewrite(self) -> str:
        """Rewrite the notes."""
        NOTESREWRITE = f"Instruct: Rewrite, reorganise and summmarise these notes below into one simple clear paragraph. Make sentences simple. Do not add any other information. Do not write the questions. Write each note in a definition-example-explanation structure. Make sure that the data is all in plain-text. \n \n {
            self.NOTES
        }"
        print(NOTESREWRITE)

        rewriteNotes = ollama.generate(
            model=self.MODELNAME, prompt=self.NOTESREWRITE)

        print(rewriteNotes["response"])

        self.NOTES = rewriteNotes["response"]

    def prompt(self):
        """ The system prompt should be designed to use few-shot learning in order to generate the most accurate questions for the source material. """

        self.SYSTEMPROMPT = f"Instruct: Generate {self.QUESTIONNUMBER} questions, in a list. Each question should be written as a string, and should be separated by one new line character \\n each. Questions should not be numbered. \nFor example, for 4 questions about famous authors would be generated as\n \"Which author beginning with the letter M contributed the most to American literary fiction?\"\\n\"When was this author born?\"\\n\"Which famous comet was associated with this author?\"\\n\"Did this author have a pen-name?\"\n "

        if ALLQUESTIONTYPES[self.QUESTIONTYPE].examplePrompt != None:
            self.SYSTEMPROMPT += ALLQUESTIONTYPES[self.QUESTIONTYPE].systemPrompt + \
                ALLQUESTIONTYPES[self.QUESTIONTYPE].examplePrompt
        else:
            self.SYSTEMPROMPT += ALLQUESTIONTYPES[self.QUESTIONTYPE].systemPrompt

        self.SYSTEMPROMPT += f"\nPlease generate the questions from these notes: \n {
            self.NOTES} \n Output: "
        # print(self.SYSTEMPROMPT)

    def generate(self):
        """Uses the specified MODELNAME to generate the questions. """
        generation = ollama.generate(
            model=self.MODELNAME, prompt=self.SYSTEMPROMPT)
        # print(generation["response"])
        self.generated_questions = [question.replace(
            "\"", "") for question in generation["response"].split("\\n")]
        # Filter out the blank spaces.
        self.generated_questions = [
            question.strip() for question in self.generated_questions if question != ""]

        # print(generated_questions)
        for q in range(len(self.generated_questions)):
            print(f"Question [{q+1}] {self.generated_questions[q]}")

        if len(self.generated_questions) != self.QUESTIONNUMBER:
            raise Exception(f"Problem with generated question amount: expected {
                            self.QUESTIONNUMBER}, got {len(self.generated_questions)}")

        if self.QUESTIONTYPE == 'mcq':
            """ Generate choices for each question."""
            MCQOPTIONS = 4
            QUESTIONDICT = {}
            for question in self.generated_questions:
                CHOICEPROMPT = f"Generate a short correct answer, that is less than 10 words, to the question {
                    question}. This answer should be summarised and should not include any notes or formatting. \nFor example: for the question \"What is the capital of England?\" the output would be \"London\". \nFor example: for the question \"How many seas are there in the world\" the output would be \"7\". \nFor example: for the question \"What is an example of a JavaScript framework?\" the output would be \"React.js\" "
                correctChoiceGeneration = ollama.generate(
                    model=self.MODELNAME, prompt=self.CHOICEPROMPT)
                """Output Parser"""
                choiceList = [choice.replace(
                    "\"", "") for choice in correctChoiceGeneration["response"].split("\\n") if choice != ""]
                QUESTIONDICT[str(question)] = choiceList
                print(question)
                print(choiceList)
                incorrectPrompt = f"Generate {MCQOPTIONS - 1} options, that are similar but not the same as {
                    choiceList[0]}. \nFor example: for an option London, the output would be \"Edinburgh\\nGlasgow\\nAberdeen\\Leeds\". \nFor example: for an option \"7\" the output would be \"4\\n6\\n2\\n9\". \n"
                incorrectChoiceGeneration = ollama.generate(
                    model=self.MODELNAME, prompt=incorrectPrompt)
                print(incorrectChoiceGeneration["response"].split("\\n"))

    def texTemplate(self):
        """ Add generated questions to a tex file."""
        MARK = self.TOTALMARKS // self.QUESTIONNUMBER
        try:
            with open("questions.tex", "w") as questionTemplate:
                if self.QUESTIONTYPE == "short":
                    # my_file.write("\\begin{parts}\n")
                    for question in self.generated_questions:
                        questionTemplate.write(
                            f"\\question[{MARK}] {question} \n")
                        questionTemplate.write("\\fillwithlines{0.75in}")
                        # for i in range(5):
                        #   my_file.write(f"\\newline")
                        #   my_file.write(f"{{\\rule{{\\linewidth}}{{0.5pt}}}} \n")
                        #   my_file.write(f"\\newline")
                        questionTemplate.write(f"\\vspace{{0.5in}}")
                        # [my_file.write("\\choice {choices}") for choice in choices]
                        # my_file.write(f"\n")
                    # my_file.write("\\end{parts}")
                elif self.QUESTIONTYPE == "mcq":
                    # my_file.write("\\begin{parts}\n")
                    for question in self.generated_questions:
                        questionTemplate.write(
                            f"\\question[{MARK}] {question} \n")
                        questionTemplate.write("\\begin{checkboxes} \n")
                        # [my_file.write("\\choice {choices}") for choice in choices]
                        questionTemplate.write("\\end{checkboxes} \n")
                        # my_file.write(f"\n")
                    # my_file.write("\\end{parts}")
                elif self.QUESTIONTYPE == "long":
                    # my_file.write("\\begin{parts}\n")
                    for question in self.generated_questions:
                        questionTemplate.write(
                            f"\\question[{MARK}] {question} \n")
                        # for i in range(10):
                        #   my_file.write(f"\\newline")
                        #   my_file.write(f"{{\\rule{{\\linewidth}}{{0.5pt}}}} \n")
                        #   my_file.write(f"\\newline")
                        questionTemplate.write("\\fillwithlines{2in}")
                        questionTemplate.write(f"\\vspace{{0.5in}}")

                else:
                    raise Exception("Behavior for questions not implemented.")
        except OSError:
            raise Exception(
                "questions.tex does not exist and cannot be written to.")

    def compileTeX(self, texFile: str):
        """Uses pdflatex to compile the file."""
        if texFile[-3:] == "tex":
            subprocess.run(
                ["pdflatex", "-interaction", "nonstopmode", "-v", texFile])
        else:
            raise Exception("This is not a tex file and cannot be compiled.")


# compileTeX("exam_1.tex")

def createPaper(questionType:str, questionNo:int, totalMarks: int):
    """Create a new paper."""
    with st.status("Generating a mock paper..."):
        newPaper = MockPaperGenerator(
            questionType, QUESTIONNUMBER=questionNo, TOTALMARKS=totalMarks)
if __name__ == "__main__":
    st.title("Magister: an automated, paper generation tool.")
    st.subheader("Installed models: ")
    for i in INSTALLEDMODELS:
        st.markdown(f"- {i}")
    with st.form("my_form"):
        questionTypeOption = st.selectbox(
            "Select the type of question from the dropdown.", ALLQUESTIONTYPES.keys())
        questionNumber = st.number_input(
            "How many questions should there be?", min_value = 2, max_value = 10)
        markNumber = st.number_input(
            "Select the total number of marks that the questions should come up to.", min_value = 3, max_value = 100)
        submitted = st.form_submit_button("Submit")
    if submitted:
        createPaper(questionTypeOption, questionNumber, markNumber)
        pdf = PdfReader("exam_1.pdf")

        st.download_button(label="Download PDF.", data=open("exam_1.pdf", "rb"),
                           mime="text/pdf", file_name="exam_1.pdf")


    
        
