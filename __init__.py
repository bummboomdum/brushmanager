from .brushmanager import *

# And add the extension to Krita's list of extensions:
app = Krita.instance()

# Instantiate your class:
extension = brushmanager(parent=app)
app.addExtension(extension)
