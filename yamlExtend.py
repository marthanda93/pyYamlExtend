import yaml
import os
import argparse

class Loader(yaml.SafeLoader):
    def __init__(self, stream):
        self._root = os.path.split(stream.name)[0]

        super(Loader, self).__init__(stream)

    def join(self, node):
        seq = self.construct_sequence(node)
        return ''.join([str(i) for i in seq])

    def ignore_unknown(self, node):
        return None 

    def path(self, node):
        yaml_data = False
        filename = [os.path.join(dp, f) for dp, dn, filenames in os.walk(self.construct_scalar(node)) for f in filenames if os.path.splitext(f)[1] in ['.yaml', '.yml']]
        
        for path in filename:
            if os.path.exists(path) and os.stat(path).st_size > 0:

                with open(path, 'r') as f:
                    data = yaml.load(f, Loader)   
                    
                    if len(data) > 0:
                        if yaml_data == False:
                            yaml_data = data
                        else:
                            yaml_data = yaml_data + data

            else:
                print(f"Error: file {path} doesn't exists! \n Or doesn't contain any data.")

        return yaml_data

    def include(self, node):
        yaml_data = False
        filename = os.path.join(self._root, self.construct_scalar(node))

        i = False
        
        for path in filename.split(" !include "):
            with open(path, 'r') as f:
                data = yaml.load(f, Loader)   
                
                if len(data) > 0:
                    if yaml_data == False:
                        yaml_data = data
                    else:
                        yaml_data = yaml_data + data

        return yaml_data

if __name__ == "__main__":
    Loader.add_constructor('!include', Loader.include)
    Loader.add_constructor('!path', Loader.path)
    Loader.add_constructor('!join', Loader.join)
    Loader.add_constructor(None, Loader.ignore_unknown)
