"""
This type stub file was generated by pyright.
"""

def nbt_data(literal): # -> Compound:
    ...

parser = ...
inputs = ...
outputs = ...
def main(): # -> None:
    ...

def read(filename, gzipped, byteorder, snbt, path, find): # -> Generator[Any | list[Any] | File, Any, None]:
    ...

def display(tag, compact, pretty, unpack, json): # -> None:
    ...

def write(nbt_data, filename, gzipped, byteorder): # -> None:
    ...

def merge(nbt_data, filename, gzipped, byteorder): # -> None:
    ...

