import pathlib as pl
import os 
import shutil

REPO = pl.Path().absolute().parent
DEST = REPO / "public"
SOURCE = REPO / "static"

def write(dest = DEST, source = SOURCE):
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


def clear_copy(dest = DEST, source = SOURCE):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    write(dest, source)