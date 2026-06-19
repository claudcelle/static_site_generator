import os
from textnode import *
from htmlnode import *
from copystatic import clear_copy,generate_page
from generatepage import generate_pages_recursive
import pathlib as pl
import shutil
  
REPO = pl.Path().absolute()
PUBLIC = REPO / "public"
STATIC = REPO / "static"
CONTENT = REPO / "content"
TEMPLATE = REPO / "template.html"

def main() -> None:
    print("Deleting public directory...")
    if os.path.exists(PUBLIC):
        shutil.rmtree(PUBLIC)
    print("Done")

    print("Copying static files to public directory...")
    clear_copy(PUBLIC,STATIC)

    print("Generating content...")
    generate_pages_recursive(CONTENT,TEMPLATE,PUBLIC)

if __name__ == "__main__":
    main()
