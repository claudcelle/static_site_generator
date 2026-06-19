import os
import pathlib as pl
from copystatic import clear_copy
from block_markdown import markdown_to_html_node,extract_title


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for p in os.listdir(dir_path_content):
        full_p = dir_path_content/p
        if os.path.isfile(full_p):
            if p.endswith('.md'):
                relative = full_p.relative_to(dir_path_content)
                destination = dest_dir_path/relative.with_suffix('.html')
                generate_page(full_p,template_path,destination,basepath)

        else:

            dest_path = dest_dir_path/p
            
            generate_pages_recursive(full_p,template_path,dest_path,basepath)

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    c_file = open(from_path, "r")
    t_file = open(template_path,"r")
    content = c_file.read()
    template = t_file.read()
    html_content = markdown_to_html_node(content).to_html()
    title = extract_title(content)
    full_html = (template.replace("{{ Title }}",title)
                         .replace("{{ Content }}", html_content)
                         .replace('href="/',f'href="{basepath}')
                         .replace('src="/', f'src="{basepath}')
    )
    

    # Crea la directory padre se non esiste
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    dest_file = open(dest_path,'w')
    dest_file.write(full_html)

    c_file.close()
    t_file.close()
    dest_file.close()

