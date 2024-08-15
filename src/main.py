import os, shutil
from markdown_converter import extract_title, markdown_to_html_node


def main():
    public_dir = "./public/"
    static_dir = "./static/"
    template_file_path = "./template.html"
    content_dir = "./content/"
    if not os.path.exists(static_dir):
        print("!! run markdown-to-html first")
        return
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
        print(f"-> {public_dir} deleted")
    os.mkdir(public_dir)
    print(f"-> {public_dir} created")
    copy_static(static_dir, public_dir)
    generate_pages_recursively(content_dir, template_file_path, public_dir)


def copy_static(src, dest):
    for i in os.listdir(src):
        if i.startswith("."):
            continue
        elif os.path.isfile(f"{src}{i}"):
            shutil.copy(f"{src}{i}", f"{dest}{i}")
        elif os.path.isdir(f"{src}{i}"):
            os.mkdir(f"{dest}{i}")
            copy_static(f"{src}{i}/", f"{dest}{i}/")


def generate_page(src, template, dest):
    dest = dest.replace(".md", ".html")
    print(f"Generating page from {src} to {dest} using {template}")
    markdown_file = open(src, "r")
    markdown = markdown_file.read()
    markdown_file.close()
    template_file = open(template, "r")
    template = template_file.read()
    template_file.close()
    title = extract_title(markdown)
    content = markdown_to_html_node(markdown)
    index_html_file = open(dest, "x")
    index_html_file.write(template.replace("{{ Title }}", title).replace("{{ Content }}", content.to_html()))
    index_html_file.close()

def generate_pages_recursively(src, template_path, dest):
    for i in os.listdir(src):
        if i.startswith("."):
            continue
        elif os.path.isfile(f"{src}{i}"):
            generate_page(f"{src}{i}", template_path, f"{dest}{i}")
        elif os.path.isdir(f"{src}{i}"):
            os.mkdir(f"{dest}{i}")
            generate_pages_recursively(f"{src}{i}/", template_path, f"{dest}{i}/")


main()
