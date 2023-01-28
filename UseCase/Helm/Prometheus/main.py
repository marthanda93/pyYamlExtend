import yaml
import sys

sys.path.append("../../../")

from yamlExtend import Loader

if __name__ == "__main__":
    Loader.add_constructor('!include', Loader.include)
    Loader.add_constructor('!path', Loader.path)
    Loader.add_constructor('!join', Loader.join)
    Loader.add_constructor(None, Loader.ignore_unknown)

    with open('helm_value.yaml', 'r') as f:
        data = yaml.load(f, Loader)

    # Clean tags:
    for key in data.copy().keys():
        if key.startswith('tmp_'):
            del data[key]

    with open('tmp_helm_value.yaml', 'w') as outfile:
        yaml.safe_dump(data, outfile, width=float("inf"), default_flow_style=False)
