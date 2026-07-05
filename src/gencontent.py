from markdown_blocks import markdown_to_html_node
import os

def extract_title(markdown):
    lines = markdown.splitlines()
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No title found in the markdown content.")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
   
      
    with open(from_path, "r") as file:
        markdown = file.read()
    with open(template_path, "r") as file:
        template = file.read()
    
   
    dest_dir = os.path.dirname(dest_path)
    os.makedirs(dest_dir, exist_ok=True)
         
    html = markdown_to_html_node(markdown).to_html()
    #print("HTML HAS SPACE?", "understand its" in html)
    #print("HTML HAS GLUED?", "understandits" in html)
    title = extract_title(markdown)

    final_html = template.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html)
    final_html = final_html.replace("href=\"/", "href=\"" + basepath)
    final_html = final_html.replace("src=\"/", "src=\"" + basepath)

    #print("FINAL HAS SPACE?", "understand its" in final_html)
    #print("FINAL HAS GLUED?", "understandits" in final_html)
        
    with open(dest_path, "w") as file:
        file.write(final_html)
    
    #with open(dest_path, "r") as file:
        #written = file.read()
    
    #print("WRITTEN HAS SPACE?", "understand its" in written)
    #print("WRITTEN HAS GLUED?", "understandits" in written)
   # print("WROTE TO:", os.path.abspath(dest_path))

def generate_pages_recursive(from_dir, template_path, dest_dir, basepath):
    
    
    for item in os.listdir(from_dir):
        source_path = os.path.join(from_dir, item)
        dest_path = os.path.join(dest_dir, item)
        if os.path.isfile(source_path) and source_path.endswith(".md"):
            dest_path = dest_path.replace(".md", ".html")
            generate_page(source_path, template_path, dest_path, basepath)
        elif os.path.isdir(source_path):
            os.makedirs(dest_path, exist_ok=True)
            generate_pages_recursive(source_path, template_path, dest_path, basepath)
            
