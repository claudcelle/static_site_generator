import os
import pathlib as pl
from copystatic import generate_page, clear_copy

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for p in os.listdir(dir_path_content):
        full_p = dir_path_content/p
        if os.path.isfile(full_p):
            if p.endswith('.md'):
                relative = full_p.relative_to(dir_path_content)
                destination = dest_dir_path/relative.with_suffix('.html')
                generate_page(full_p,template_path,destination)

        else:

            dest_path = dest_dir_path/p
            
            generate_pages_recursive(full_p,template_path,dest_path)

