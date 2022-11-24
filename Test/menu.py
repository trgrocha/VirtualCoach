from cursesmenu import CursesMenu
from cursesmenu.items import MenuItem
from curses import panel

def fEnsinar():
    print ("Ensinar um exercício ")
    exec(open("Personal.py").read())

def main():
    menu1 = CursesMenu("Treinador Virtual")
    item1 = MenuItem("Ensinar um exercício", menu1, should_exit=True)
    menu1.items.append(item1)
    menu1.show()
    fEnsinar()
    
if __name__ == "__main__":
    main()

