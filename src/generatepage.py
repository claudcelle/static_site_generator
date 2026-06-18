import os
import pathlib as pl
from copystatic import generate_page

def generate_pages_recursive(
        dir_path_content=pl.Path("/home/claudio/boot_dot_dev/static_site_generator/content"), 
        template_path=pl.Path("/home/claudio/boot_dot_dev/static_site_generator/template.html"), 
        dest_dir_path=pl.Path('/home/claudio/boot_dot_dev/static_site_generator/public')):
    
    for p in os.listdir(dir_path_content):
        full_p = dir_path_content/p
        if os.path.isfile(full_p):
            print(f"{full_p} is file\n")            
            if p.endswith('.md'):
            #     parent = full_p.removeprefix("/home/claudio/boot_dot_dev/static_site_generator/content/")
            #     # print(parent)
                destination = pl.Path(str(full_p).removesuffix(".md")+".html")
                # print(f"{p} is markdown")                
                print(f"generating html to {destination}")  
                print("--------\n")
                # generate_page(full_p,template_path,destination)

        else:
            # print(f"{full_p} is folder")
            new_content_path = full_p            
            generate_pages_recursive(dir_path_content=new_content_path)
    # return 

generate_pages_recursive()
