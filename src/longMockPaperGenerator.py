from mockPaperGenerator import MockPaperGenerator


class LongMockPaperGenerator(MockPaperGenerator):
    def __init__(
        self,
        QUESTIONTYPE: str = "short",
        MODELNAME: str = "phi3:mini",
        NOTEFILE: str = "notes.txt",
        QUESTIONNUMBER: int = 5,
        TOTALMARKS: int = 10,
    ) -> None:
        super().__init__(QUESTIONTYPE, MODELNAME, NOTEFILE, QUESTIONNUMBER, TOTALMARKS)

    def texTemplate(self):
        MARK = self.TOTALMARKS // self.QUESTIONNUMBER
        with open("questions.tex", "w") as questionTemplate:
            for question in self.generated_questions:
                questionTemplate.write(f"\\question[{MARK}] {question} \n")
                # for i in range(10):
                #   my_file.write(f"\\newline")
                #   my_file.write(f"{{\\rule{{\\linewidth}}{{0.5pt}}}} \n")
                #   my_file.write(f"\\newline")
                questionTemplate.write("\\fillwithlines{2in}")
                questionTemplate.write(f"\\vspace{{0.5in}}")
