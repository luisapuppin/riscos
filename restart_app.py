import os
import sys
from shutil import rmtree

def limpar_dados_aplicacao():
    print("[DELETE-DATABASE] Initializing...")
    origin = "\\".join(os.path.realpath(__file__).split("\\")[:-1])
    if os.path.exists(os.path.join(origin, "db.sqlite3")):
        os.remove(os.path.join(origin, "db.sqlite3"))
        print("[DATABASE] Deleted!")
    for folders in os.walk(origin):
        if "__pycache__" in folders[0]:
            rmtree(folders[0])
            print("[%s/__pycache__] Deleted!" % folders[0].split("\\")[-2])
        if folders[0].endswith("migrations"):
            folders[2].remove("__init__.py")
            for migrations_files in folders[2]:
                os.remove(os.path.join(folders[0], migrations_files))
            print("[%s/MIGRATIONS] Deleted!" % folders[0].split("\\")[-2])
    print("[DELETE-DATABASE] Done!")

def redo_data_base():
    print("[CREATE-DATABASE] Initializing...")
    os.system("python manage.py makemigrations")
    os.system("python manage.py migrate")
    os.system("python create_admin.py")
    os.system("python create_db.py")
    print("[CREATE-DATABASE] Done!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        limpar_dados_aplicacao()
        redo_data_base()
    elif sys.argv[1] == "del":
        limpar_dados_aplicacao()
    elif sys.argv[1] == "create":
        redo_data_base()
