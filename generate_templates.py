from jinja2 import Environment, FileSystemLoader
from catch_output import catch_output
import os

class NavbarItem:
    def __init__(self, name, endpoint, isSelected) -> None:
        self.name = name
        self.endpoint = endpoint
        self.isSelected = isSelected

nav_bar = [
    NavbarItem('Home', 'index.html', True),
    NavbarItem('Warnings', 'warnings.html', False),
    NavbarItem('Vulnerabilities', 'vulnerabilities.html', False),
]

def get_navbar(item_name: str):
    for item in nav_bar:
        if item_name == item.name:
            item.isSelected = True
        else:
            item.isSelected = False
    return nav_bar

def generate_templates(file_name= r'./example_contracts/lock.sol'):
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
    warnings, vulnerabilities = catch_output(file_name)

    with open(filename, 'w') as fh:
        fh.write(template_warnings.render(nav_bar=get_navbar('Warnings'), warnings=warnings))

    # vulnerabilities
    template_vulnerabilities = env.get_template('vulnerabilities.html')
    filename = os.path.join(root, 'html', 'vulnerabilities.html')
    with open(filename, 'w') as fh:
        fh.write(template_vulnerabilities.render(nav_bar=get_navbar('vulnerabilities'), vulnerabilities=vulnerabilities))