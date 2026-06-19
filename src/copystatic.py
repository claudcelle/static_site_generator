import pathlib as pl
import os 
import shutil





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