
class beamer_writer:
    def __init__(self,
                 file_name: str,
                 title: str,
                 author: str,
                 date: str):
        assert isinstance(file_name, str) and len(file_name) != 0

        self.__file_name: str = file_name
        self.__title: str = title
        self.__author: str = author
        self.__date: str = date
        self.__data_group: tuple[tuple] = []
        
    @property
    def file_name(self) -> str:
        return self.__file_name

    @property
    def title(self) -> str:
        return self.__title

    @property
    def author(self) -> str:
        return self.__author

    @property
    def date(self) -> str:
        return self.__date
    
    def add_data_group(self,
                       title: str,
                       subtitle: str,
                       collection: tuple,
                       n: int = 7,
                       section_page: bool = False,
                       comment: str = ""):
        self.__data_group.append([title, subtitle, collection, n, section_page, comment])

    def write(self) -> None:
        with open(self.file_name, "w") as outFile:
            self.write_metadata(outFile)
            self.write_begin_document(outFile)

            for (title, subtitle, collection, n, section_page, comment) in self.__data_group:
                if section_page:
                    self.write_title_page(title, comment, outFile)
                self.write_collection(title, subtitle, collection, n, outFile)
            
            self.write_end_document(outFile)

    def write_collection(self,
                         title: str,
                         subtitle: str,
                         collection: tuple,
                         N: int,
                         outFile) -> None:
        print(f"Writing collection on frame with title: {title} : {subtitle}")
        while (len(collection) > 0):
            to_be_printed = collection[:N] if len(collection) > N else collection
            self.write_frame(title=title,
                             subtitle=subtitle,
                             collection=to_be_printed,
                             outFile=outFile)
            collection = collection[N:] if len(collection) > N else []
        
            
    def write_metadata(self,
                       outFile) -> None:
        outFile.write("\\documentclass[10pt]{beamer}\n")
        outFile.write("\\usepackage[utf8]{inputenc}\n\n")
        outFile.write(f"\\title{{{self.title}}}\n")
        outFile.write(f"\\author{{{self.author}}}\n")
        outFile.write(f"\\date{{{self.date}}}\n\n")
        outFile.write("\\setbeamertemplate{footline}[frame number]\n")
        outFile.write("\\setbeamertemplate{headline}{}\n\n")
        outFile.write("\\usepackage{xcolor}\n")
        outFile.write("\\usepackage{hyperref}\n")
        outFile.write("\\hypersetup{\n  colorlinks=true,\n  linkbordercolor=blue,\n  urlbordercolor=blue \n}\n\n")
        
    def write_begin_document(self,
                             outFile) -> None:
        outFile.write("\\begin{document}\n\n")
        outFile.write("\\frame{\\titlepage}\n\n")

    def write_title_page(self,
                         title: str,
                         comment: str,
                         outFile) -> None:
        outFile.write("\\begin{frame}\n")
        outFile.write(f"\\centering \\huge {title}\n\n")
        outFile.write(f"\\footnotesize {comment}\n")
        outFile.write("\\end{frame}\n\n")
        
    def write_frame(self,
                    title: str,
                    subtitle: str,
                    collection: tuple,
                    outFile) -> None:
        outFile.write(f"\\begin{{frame}}{{{title}}}{{{subtitle}}}\n")
        outFile.write("\\footnotesize\n")
        for el in collection:
            outFile.write(el.dump_latex().replace("_", "\_"))
        outFile.write("\\end{frame}\n\n")

    def write_end_document(self,
                           outFile) -> None:
        outFile.write("\\end{document}")
