from mockPaperGenerator import MockPaperGenerator


class MCQMockPaperGenerator(MockPaperGenerator):
  def __init__(self, QUESTIONTYPE: str = "short", MODELNAME: str = "phi3:mini", NOTEFILE: str = "notes.txt", QUESTIONNUMBER: int = 5, TOTALMARKS: int = 10) -> None:
    super().__init__(QUESTIONTYPE, MODELNAME, NOTEFILE, QUESTIONNUMBER, TOTALMARKS)
  def generate(self):
    super().generate()
    
  def texTemplate(self):
    MARK = self.TOTALMARKS // self.QUESTIONNUMBER
    with open("questions.tex", "w") as questionTemplate:
      for question in self.generated_questions:
          questionTemplate.write(
              f"\\question[{MARK}] {question} \n")
          questionTemplate.write("\\begin{checkboxes} \n")
          # [my_file.write("\\choice {choices}") for choice in choices]
          questionTemplate.write("\\end{checkboxes} \n")
          # my_file.write(f"\n")
          # my_file.write("\\end{parts}")
