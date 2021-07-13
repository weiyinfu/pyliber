import importlib
import pkgutil
import re
from collections import Counter
from os.path import dirname, basename
from types import ModuleType

import uvicorn
from fastapi import FastAPI
from pip._internal.cli import main as pip_main

from pyliber import util

app = FastAPI()


@app.get("/api/piplist")
def piplist():
    def f():
        pip_main.main(["list"])

    a = util.get_content(f)
    a = a.split()
    a = a[4:]
    name_list = a[::2]
    version_list = a[1::2]
    return {name: version for name, version in zip(name_list, version_list)}


def typeof(x):
    name = type(x)
    return re.search("<class '(.+)'>", str(name)).group(1)


@app.get("/api/get_module_info")
def module_desc(path: str):
    def _module_desc(mod: ModuleType):
        attr_type_list = []
        for i in dir(mod):
            if i.startswith("_"):
                continue
            ty = type(getattr(mod, i))
            ty_name = typeof(getattr(mod, i))
            if ty == ModuleType:
                # 去掉module类型的变量
                continue
            if ty_name.startswith("typing."):
                # 去掉typing包下的变量
                continue
            attr_type_list.append((ty_name, i))
        c = Counter([i[0] for i in attr_type_list])
        name_count = []
        for name, count in c.items():
            name_count.append({'name': name, 'count': count})
        attr_list = []
        for type_name, i in attr_type_list:
            v = getattr(mod, i)
            obj = {'name': i, 'type': type_name, 'doc': v.__doc__}
            attr_list.append(obj)
        name_count.sort(key=lambda x: x['count'], reverse=True)
        return name_count, attr_list

    def sub_module_list(folder: str):
        sub_modules = pkgutil.iter_modules([folder])
        sub_modules = [{'name': i.name, 'module_path': f"{path}.{i.name}"} for i in sub_modules]
        return sub_modules

    a = importlib.import_module(path)
    type_count, attr_list = _module_desc(a)
    subs = [] if basename(a.__file__) == "__init__.py" else sub_module_list(dirname(a.__file__))
    ans = {
        'desc': type_count,
        'doc': a.__doc__,
        'file': a.__file__,
        'members': attr_list,
        'sub_modules': subs,
    }
    return ans


if __name__ == '__main__':
    uvicorn.run(app, debug=True)
