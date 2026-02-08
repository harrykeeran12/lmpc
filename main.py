# import subprocess
import time

import ollama
import streamlit as st

# from httpx import ConnectError
from questionType import QuestionType
from src.longMockPaperGenerator import LongMockPaperGenerator
from src.shortMockPaperGenerator import ShortMockPaperGenerator

short = QuestionType(
    "short", "You must generate short questions that are clear to understand."
)
long = QuestionType(
    "long", "You must generate long answer questions. Examples include essay questions."
)
mcq = QuestionType(
    "mcq",
    "You must generate short multiple choice questions that can be answered using one sentence. Do not return the answers or options.",
)
ALLQUESTIONTYPES: dict[str, QuestionType] = {}

ALLQUESTIONTYPES[short.name] = short
ALLQUESTIONTYPES[long.name] = long

INSTALLEDMODELS: list[str] = []
for modelName in ollama.list()["models"]:
    # print(modelName)
    INSTALLEDMODELS.append(modelName["model"])


def createPaper(questionType: str, questionNo: int, totalMarks: int, modelName: str):
    """Creates a new instance of the mock paper generator class."""
    with st.status("Generating a mock paper...") as status:
        newPaper = ShortMockPaperGenerator(
            QUESTIONNUMBER=questionNo,
            TOTALMARKS=totalMarks,
            MODELNAME=modelName,
        )
        if questionType == "long":
            newPaper = LongMockPaperGenerator(
                QUESTIONNUMBER=questionNo,
                TOTALMARKS=totalMarks,
                MODELNAME=modelName,
            )
        # newPaper = MockPaperGenerator(
        #     QUESTIONTYPE=questionType, QUESTIONNUMBER=questionNo, TOTALMARKS=totalMarks)
        ticOne = time.perf_counter()
        newPaper.prompt()
        newPaper.generate()
        ticTwo = time.perf_counter()
        status.update(label="Prompt generated.", state="running", expanded=False)
        newPaper.texTemplate()
        status.update(label="Compiling .pdf.", state="running", expanded=False)
        newPaper.compileTeX("exam_1.tex")
        ticThree = time.perf_counter()
        status.update(
            label=f"Generated prompt in {ticTwo - ticOne:0.4f} seconds. Compiled .pdf in {ticThree - ticTwo:0.4f} seconds. ",
            state="complete",
            expanded=True,
        )


if __name__ == "__main__":
    st.title("Chiron: an automated, paper generation tool, displayed in $ \\LaTeX $")
    st.markdown("##### Installed models: ")
    selectedModel = st.selectbox(
        "Select the model.", INSTALLEDMODELS, key="modelSelected"
    )
    # st.markdown(f"{''.join(INSTALLEDMODELS)}")
    st.divider()
    col1, col2 = st.columns([1, 1.5])
    questionTypeOption = st.selectbox(
        "Select the **type of question** from the dropdown menu.",
        ALLQUESTIONTYPES.keys(),
        key="questionType",
    )

    with col1:
        questionNumber = st.number_input(
            "How many **questions** should there be?",
            min_value=2,
            max_value=10,
            key="questionNumber",
        )
    with col2:
        markNumber = st.number_input(
            "Select the total number of marks.",
            min_value=2,
            max_value=100,
            step=10,
            key="markNumber",
        )
    with st.form("my_form"):
        # st.write(st.session_state)
        notefile = st.file_uploader(label="Upload notes here.", disabled=True)

        submitted = st.form_submit_button("Submit")
    if submitted:
        createPaper(
            st.session_state.questionType,
            st.session_state.questionNumber,
            st.session_state.markNumber,
            st.session_state.modelSelected,
        )
        st.download_button(
            label="Download PDF.",
            data=open("exam_1.pdf", "rb"),
            mime="text/pdf",
            file_name="exam_1.pdf",
        )
