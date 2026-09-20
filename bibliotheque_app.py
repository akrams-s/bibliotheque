# bibliotheque_app.py

from view import BibliothequeView
from controller import BibliothequeController

if __name__ == "__main__":
    vue = BibliothequeView()
    controller = BibliothequeController(vue)
    vue.mainloop()