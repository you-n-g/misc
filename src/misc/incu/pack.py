import importlib
import site
import sys
from pathlib import Path


def locate_pack(module: str) -> None:
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
    for pa in list(Path(site_packages[0]).glob("*.pth")):
        print(f"- {pa}")
    # TODO:
    # - know how path is constructed
    # - read the content of the files and give more accurate results
