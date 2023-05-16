from generate_templates import generate_templates
import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        generate_templates(file_name=sys.argv[1])
    else:
        generate_templates()