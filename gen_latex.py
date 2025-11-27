import subprocess
from pathlib import Path

def create_latex_document(file_names: list[str]):
    latex_body = ""

    for i in range(0, len(file_names), 2):
        latex_body += f"\\TwoPerPage{{{file_names[i]}}}{{{file_names[i + 1]}}}\n"

    start = r"""\documentclass{article}
\usepackage[margin=0.25in]{geometry}
\usepackage{graphicx}
\pagestyle{empty}

\newcommand{\TwoPerPage}[2]{%
  \centering

  \includegraphics[angle=90,keepaspectratio,
                   width=\textwidth,height=.46\textheight]{#1}\par
  \vspace{0.5in}

  \includegraphics[angle=90,keepaspectratio,
                   width=\textwidth,height=.46\textheight]{#2}%
  \clearpage
}

\begin{document}
"""
    end = r"\end{document}"

    full = "\n".join([start, latex_body, end])

    with open("output.tex", "w") as f:
        f.write(full)

    subprocess.run(["pdflatex", "output.tex"], cwd=".")


create_latex_document(list(map(str, Path("output").glob("*.png"))))