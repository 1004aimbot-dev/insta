
from notebooklm import Notebook
print([x for x in dir(Notebook) if not x.startswith('_')])
