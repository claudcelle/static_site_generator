from textnode import *
from htmlnode import *
from copystatic import clear_copy
import pathlib as pl
  
REPO = pl.Path().absolute()
DEST = REPO / "public"
SOURCE = REPO / "static"

def main() -> None:
    clear_copy(DEST,SOURCE)

if __name__ == "__main__":
    main()
