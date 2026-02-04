
import notebooklm
print([x for x in dir(notebooklm) if 'list' in x.lower() or 'get' in x.lower() or 'notebook' in x.lower()])
