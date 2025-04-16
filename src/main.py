from textnode import TextNode, TextType
from htmlnode import HTMLNode
from markdown_blocks import markdown_to_html_node, extract_title
import os
import shutil
from pathlib import Path

def copy_static(source, destination):
    # Step 1: Delete the destination directory if it exists
    if os.path.exists(destination):
        shutil.rmtree(destination)

    # Step 2: Create the destination directory
    os.mkdir(destination)
    
    # Step 3: Loop through all files and directories in source
    for item in os.listdir(source):
        source_path = os.path.join(source, item)
        dest_path = os.path.join(destination, item)
        
        # Step 4: If it's a file, copy it
        if os.path.isfile(source_path):
            print(f"Copying file: {source_path} to {dest_path}")
            shutil.copy(source_path, dest_path)
        # Step 5: If it's a directory, recursively copy it
        else:
            # Create the corresponding subdirectory in destination
            os.mkdir(dest_path)
            # Recursively copy contents from source subdirectory to destination subdirectory
            copy_static(source_path, dest_path)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as markdown_file:
        markdown_content = markdown_file.read()
    
    with open(template_path, "r") as template_file:
        template_content = template_file.read()

    html_content = markdown_to_html_node(markdown_content).to_html()

    title = extract_title(markdown_content)

    template_with_content = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)


    with open(dest_path, "w") as output_file:
        output_file.write(template_with_content)

# def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
#      for item in os.listdir(dir_path_content):
#          source_path = os.path.join(dir_path_content, item)
#          dest_path = os.path.join(dest_dir_path, item)
         
#          if os.path.isfile(source_path):
#             if source_path.endswith(".md"):
#                 dest_path = dest_path.replace(".md", ".html")
#                 os.makedirs(os.path.dirname(dest_path), exist_ok=True)
#                 generate_page(source_path, template_path, dest_path)

#          elif os.path.isdir(source_path):
#             os.makedirs(dest_path, exist_ok=True)
#             generate_pages_recursive(source_path, template_path, dest_path)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
     for item in os.listdir(dir_path_content):
         source_path = os.path.join(dir_path_content, item)
         dest_path = os.path.join(dest_dir_path, item)
         
         if os.path.isfile(source_path):
            if source_path.endswith(".md"):
                dest_path = dest_path.replace(".md", ".html")
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                generate_page(source_path, template_path, dest_path)
            else:
                # Copy non-markdown files directly
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                shutil.copy(source_path, dest_path)
         elif os.path.isdir(source_path):
            os.makedirs(dest_path, exist_ok=True)
            generate_pages_recursive(source_path, template_path, dest_path)


def main():
    
    if os.path.exists("public"):
        shutil.rmtree("public")

    copy_static("static", "public")
    generate_pages_recursive("content", "template.html", "public")

if __name__ == "__main__":
    main()