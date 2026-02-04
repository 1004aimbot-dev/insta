
from notebooklm import Notebook
print("Imported Notebook successfully")
try:
   # Try to see if it has a listing method
   print(dir(Notebook))
except:
   pass
