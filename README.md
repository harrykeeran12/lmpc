# lmpc
A repository housing a mock paper creator program powered by an LLM. (LLM mock paper creator).

The aim of this project is to generate mock papers from notes. 


For development:

- You will need to set up a LaTeX distribution for this. 
  The paper generated uses commands from the  [`exam.cls`](https://ctan.org/pkg/exam) class file. 
  You can install this class file using:
  ```sh 
  sudo tlmgr install exam
  ```

- The Python packages required can be installed using conda. You will need to have `ollama` on your system, and up and running using the `ollama serve` command. 


# Development: 

__A mock paper can be generated by__
- supplying notes(required), 
- supplying an LLM model name(default will be `phi3:mini` ), 
- providing the number of questions(between 2 and 5), 
- the total number of marks that the questions should total up to(default will be 100), 
- the question type(short-form questions, multiple choice questions(default), essay based questions), 
- any example questions given. 

# TODO: 

- [ ] Generate an answer key for multiple choice questions. 

- [ ] Add subdivision support.



