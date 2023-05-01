from jinja2 import Environment, FileSystemLoader
from catch_output import catch_warnigns
import os

class NavbarItem:
    def __init__(self, name, endpoint, isSelected) -> None:
        self.name = name
        self.endpoint = endpoint
        self.isSelected = isSelected

nav_bar = [
    NavbarItem('Home', 'index.html', True),
    NavbarItem('Warnings', 'warnings.html', False),
    NavbarItem('Vulnerabilities', '/vulnerabilities', False),
]

def get_navbar(item_name: str):
    for item in nav_bar:
        if item_name == item.name:
            item.isSelected = True
        else:
            item.isSelected = False
    return nav_bar


root = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(root, 'templates')
env = Environment(loader=FileSystemLoader(templates_dir))

# index.html
template = env.get_template('index.html')
filename = os.path.join(root, 'html', 'index.html')
with open(filename, 'w') as fh:
    fh.write(template.render(nav_bar=get_navbar('Home')))

# warnings
template_warnings = env.get_template('warnings.html')
filename = os.path.join(root, 'html', 'warnings.html')
warnings = catch_warnigns()
with open(filename, 'w') as fh:
    fh.write(template_warnings.render(nav_bar=get_navbar('Warnings'), warnings=warnings))