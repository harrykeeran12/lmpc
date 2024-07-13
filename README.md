# chiron
A repository housing a mock paper creator program powered by an LLM. (used to be called LLM mock paper creator). The LLM uses *few shot learning*- more information about this learning style can be found [here.](https://www.promptingguide.ai/techniques/fewshot). 
The LLM used in development was `phi-3:mini` due to its small size. My personal opinion is that small language models could be very useful. 

The aim of this project is to generate mock papers from notes, and render them as a PDF for printing. 
The idea for this project came about whilst I was studying for my exams, and grew tired of the papers that were provided to me. I did not feel as if I understood the material from these short papers. 
Ollama is used in order to host a local LLM on the development machine.



## For development:

- You will need to set up a LaTeX distribution for this. 
  The paper generated uses commands from the  [`exam.cls`](https://ctan.org/pkg/exam) class file. I was able to set this up with assistance from the MIT document on rendering exams with LaTeX [here.](https://math.mit.edu/~psh/exam/examdoc.pdf)
  You can install this class file using:
  ```sh 
  sudo tlmgr install exam
  ```
  which uses `tlmgr` (the TUG package manager) to install `exam.cls`. 
  To compile the document, `pdflatex` is used, but this can be changed + extended. 

- The Python packages required can be installed using conda. You will need to have `ollama` on your system, and up and running using the `ollama serve` command. 
- For the web interface, `streamlit` is required. The web application can be run using `streamlit run main.py`. 


## Tests:

You can run the tests for the program using `pytest tests -q`. Note that pytest must be installed.
## TODO: 

- [ ] Generate clear options for multiple choice questions. 

- [ ] Add subdivision support(a,b,c) for questions with some sort of link.

- [ ] Add support for example questions to be added.



