from email.mime import base
import os
from textnode import *
from htmlnode import *
from copystatic import clear_copy
from generatepage import generate_pages_recursive
import pathlib as pl
import shutil
import sys
  
BASE = pl.Path().absolute()
PUBLIC = BASE / "public"
DOCS  = BASE / "docs"
STATIC = BASE / "static"
CONTENT = BASE / "content"
TEMPLATE = BASE / "template.html"

def main() -> None:

    try:
        basepath = sys.argv[1]
    except Exception:
        basepath = '/'

    print("Deleting public directory...")
    if os.path.exists(DOCS):
        shutil.rmtree(DOCS)
    print("Done")

    print("Copying static files to public directory...")
    clear_copy(DOCS,STATIC)

    print("Generating content...")
    print(basepath)
    generate_pages_recursive(CONTENT,TEMPLATE,DOCS,basepath)

if __name__ == "__main__":
    main()
