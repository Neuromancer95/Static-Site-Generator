import os
import shutil
from gencontent import generate_page, generate_pages_recursive
import sys

def copy_static(source_dir, dest_dir):   
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.mkdir(dest_dir)
    copy_directory_contents(source_dir, dest_dir)    



def copy_directory_contents(source_dir, dest_dir):
    for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)
        if os.path.isfile(source_path):
            print(f"Copying {source_path} to {dest_path}")
            shutil.copy2(source_path, dest_path)
        elif os.path.isdir(source_path):
            os.makedirs(dest_path, exist_ok=True)
            copy_directory_contents(source_path, dest_path)


           

def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]    
    source_dir_stat ="static"
    source_dir = "content"
    template_path = "template.html"
    dest_dir = "docs"
    copy_static(source_dir_stat, dest_dir)
    generate_pages_recursive(source_dir, template_path, dest_dir, basepath)
    

    
if __name__ == "__main__":
    main()    