import argparse
from .nbt_reader import read_nbt_file as load
from .render import render_structure as render


parser = argparse.ArgumentParser()
parser.add_argument("--debug", action="store_true")
parser.add_argument("--output", type=str, default="head_render.png")
args = parser.parse_args()
structure = load("./pressure_plate.nbt")
print(structure)
image = render(structure, output_path=args.output, debug=args.debug)
