from mockPaperGenerator import MockPaperGenerator


class ShortMockPaperGenerator(MockPaperGenerator):
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
        """A modified form of the texTemplate."""
        MARK = self.TOTALMARKS // self.QUESTIONNUMBER
        with open("questions.tex", "w") as questionTemplate:
            for question in self.generated_questions:
                questionTemplate.write(f"\\question[{MARK}] {question} \n")
                questionTemplate.write("\\fillwithlines{0.75in}")
                # for i in range(5):
                #   my_file.write(f"\\newline")
                #   my_file.write(f"{{\\rule{{\\linewidth}}{{0.5pt}}}} \n")
                #   my_file.write(f"\\newline")
                questionTemplate.write(f"\\vspace{{0.5in}}")
