try:
    from markdown2 import MarkdownWithExtras as Markdown
except ImportError:
    from markdown import Markdown 
md = Markdown()

def markdown(data):
    return md.convert(data)
