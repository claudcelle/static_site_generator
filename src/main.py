from textnode import *
from htmlnode import *
from copystatic import clear_copy,generate_page
import pathlib as pl
  
REPO = pl.Path().absolute()
DEST = REPO / "public"
SOURCE = REPO / "static"

def main() -> None:
    clear_copy(DEST,SOURCE)
    generate_page(REPO/"content/index.md",REPO/"template.html",DEST/"index.html")

if __name__ == "__main__":
    main()
