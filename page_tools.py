from jinja2 import Template
import config
import os

navbar_path = os.path.join(config.path_to_resources, "navbar.html")
def create_navbar(data):
    with open(navbar_path, encoding='utf-8') as file:
        navbar_text = file.read()
        template = Template(navbar_text)
    return template.render(data)

def page_from_template(path, data):
    data['navbar'] = create_navbar(data)
    with open(path, encoding='utf-8') as file:
        page_text = file.read()
        template = Template(page_text)
    return template.render(data)