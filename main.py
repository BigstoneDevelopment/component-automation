from errno import EACCES
from standard_checker import load, render
import sys
import os


# TODO: load from env.GITHUB_TOKEN into a git lib or something to upload the new wiki file to the pr
WIKI_EXTENSIONS = [".md", ".txt"]
WIKI_FOLDER = os.path.join(os.path.dirname(__file__), "..", "??????")  # TODO: set the wiki folder path


if __name__ == "__main__":
    sys.argv = sys.argv[1:]
    if len(sys.argv) < 1:
        print("Usage: automation <nbt_file> [<wiki_file>]", file=sys.stderr)
        sys.exit(1)

    nbt_path = list(filter(lambda x: x.endswith(".nbt"), sys.argv))
    wiki_path = list(filter(lambda x: any(x.endswith(ext) for ext in WIKI_EXTENSIONS), sys.argv))

    if len(nbt_path) != 1 or len(wiki_path) > 1 or len(wiki_path) + len(nbt_path) != len(sys.argv):
        print("Usage: automation <nbt_file> [<wiki_file>]", file=sys.stderr)
        sys.exit(EACCES)

    structure = load(nbt_path[0])
    if not structure:
        print(f"Failed to load structure from {nbt_path[0]}", file=sys.stderr)
        sys.exit(EACCES)

    old_wiki_path = wiki_path[0] if wiki_path else None
    if wiki_path:
        wiki_path = wiki_path[0]
    else:
        wiki_path = nbt_path[0].removesuffix(".nbt") + ".ext"
    wiki_path = os.path.join(WIKI_FOLDER, os.path.splitext(os.path.basename(wiki_path))[0])  # Remove the extension

    image = render(structure, output_path=wiki_path + ".png")
