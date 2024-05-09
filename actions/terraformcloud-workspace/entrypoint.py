import os

from main import Context

if __name__ == '__main__':
    context = Context(os.environ)
    context.load_from_env()
    context.workspace_create()
