import importlib
from pathlib import Path
import site
import sys

def locate_pack(module: str):
    print("Check your sys.path first")
    orig_path = sys.path
    sys.path = []
    for p in orig_path:
        try:
            importlib.import_module(module)
        except ModuleNotFoundError:
            pass
        else:
            print(f"The module is loaded form {p}")
            break
        sys.path.append(p)
    # get the absolute path of site-packages
    site_packages = site.getsitepackages()
    print("You may check following paths")
    for p in list(Path(site_packages[0]).glob("*.pth")):
        print(f"- {p}")
    # TODO:
    # - know how path is constructed
    # - read the content of the files and give more accurate results
