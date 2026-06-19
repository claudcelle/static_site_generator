import pathlib as pl
import os 
import shutil
from block_markdown import markdown_to_html_node

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    c_file = open(from_path, "r")
    t_file = open(template_path,"r")
    content = c_file.read()
    template = t_file.read()
    html_content = markdown_to_html_node(content).to_html()
    title = extract_title(content)
    full_html = template.replace("{{ Title }}",title).replace("{{ Content }}", html_content)
    # Crea la directory padre se non esiste
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    dest_file = open(dest_path,'w')
    dest_file.write(full_html)

    c_file.close()
    t_file.close()
    dest_file.close()



def extract_title(markdown=''):
    if not markdown:
        raise Exception("Markdown is empty")
    if not isinstance(markdown,str):
        raise TypeError("Content must be text")
    
    for row in markdown.split('\n'):
        if row.startswith("# "):
            return (row.lstrip('#')).strip()
    raise Exception("No h1 header")

def copy_recursively(dest, source):    

    if not isinstance(dest,pl.Path):
        dest = pl.Path(dest)
    if not isinstance(source,pl.Path):
        source = pl.Path(source)

    if source.is_dir():
        dest.mkdir(exist_ok=True)
        for item in source.iterdir():
            print(f" * {item} -> {dest/item.name}")
            copy_recursively(dest/item.name, item)
    else:
        shutil.copy(source, dest)




def write(dest, source):
    if not os.path.isfile(source):
        for item in os.listdir(source):
            if os.path.isfile(source/item):
                if not os.path.exists(dest):
                    os.mkdir(dest)
                print(source/item, dest)
                shutil.copy(source/item, dest)
            if not os.path.exists(dest):    
                os.mkdir(dest)
            if not os.path.exists(dest/item):        
                os.mkdir(dest/item)    
            write(dest/item,source/item)       

def clear(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder)


def clear_copy(dest, source):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    # write(dest, source)
    copy_recursively(dest, source)