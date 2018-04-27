""" Rotina para deletar e criar o banco de dados.
    Chamadas:
        python restart_app.py
        python restart_app.py del
        python restart_app.py create
"""

import os
import sys
from shutil import rmtree

def limpar_dados_aplicacao():
    """ Rotina que deleta o arquivo de banco db.sqlite3, as pastas
        __pycache__, e todos os arquivos da pasta migrations
        (exceto __init__.py)
    """
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
    """ Rotina para recriar o banco de dados. É composta de 4 etapas:
        I) makemigrations; II) migrate; III) create_admin.py, e;
        IV) create_db.py.
    """
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
