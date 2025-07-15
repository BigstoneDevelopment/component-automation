from functools import cache
import sys
import traceback
from typing import Any, cast
import requests
from PIL import Image
from io import BytesIO


GITHUB_RAW_BASE = "https://raw.githubusercontent.com/BigstoneDevelopment/Minecraft-Assets/main"


def fetch_json(url: str) -> dict[Any, Any]:
    res = requests.get(url)
    if res.status_code != 200:
        raise ValueError(f"Failed to fetch JSON: {url}")
    return res.json()


def resolve_model_from_blockstate(block_id: str) -> str:
    """Fetch model path from blockstate, fallback to direct model if needed."""
    namespace, name = block_id.split(":")
    blockstate_url = f"{GITHUB_RAW_BASE}/assets/{namespace}/blockstates/{name}.json"

    try:
        blockstate = fetch_json(blockstate_url)
    except ValueError as e:
        traceback.print_exception(e)
        # No blockstate file? Assume direct model path.
        return f"assets/{namespace}/models/block/{name}.json"

    if "variants" in blockstate:
        # Use first variant
        first_variant = next(iter(blockstate["variants"].values()))
        if isinstance(first_variant, list):
            model_name: str = cast(str, first_variant[0]["model"])
        else:
            model_name: str = first_variant["model"]
    elif "multipart" in blockstate:
        # Use first multipart condition
        model_name: str = blockstate["multipart"][0]["apply"]["model"]
    else:
        raise ValueError(f"Unsupported blockstate structure for {block_id}")

    if ':' in model_name:
        model_namespace, model_name = model_name.split(":")
    else:
        model_namespace = namespace
    return f"{GITHUB_RAW_BASE}/assets/{model_namespace}/models/{model_name}.json"


def get_texture_path_from_model(block_id: str) -> str:
    model_url = resolve_model_from_blockstate(block_id)
    model_namespace = model_url.split("/")[GITHUB_RAW_BASE.count("/") + 2]
    model_json = fetch_json(model_url)

    # Support 'all', 'side', 'top', etc.
    textures: dict[str, str] | None = model_json.get("textures")
    if not textures:
        raise ValueError(f"No textures defined in model for {block_id}")

    texture_ref = textures.get("all") or textures.get("side") or next(iter(textures.values()))
    texture_path = texture_ref.replace(":", "/").replace("block/", "textures/block/") + ".png"
    texture_path = texture_path.removeprefix(model_namespace + "/")
    return f"{GITHUB_RAW_BASE}/assets/{model_namespace}/{texture_path}"


@cache
def load_block_texture(block_id: str) -> Image.Image:
    try:
        texture_url = get_texture_path_from_model(block_id)
        res = requests.get(texture_url)
        res.raise_for_status()
        return Image.open(BytesIO(res.content)).convert("RGBA")
    except Exception as e:
        print(f"[WARN] Could not load texture for {block_id}\n{e}", file=sys.stderr)
        # Return a fallback magenta
        return Image.new("RGBA", (16, 16), (255, 0, 255, 255))


__all__ = ["load_block_texture"]


if __name__ == "__main__":
    # Example usage
    block_id = "minecraft:stone"
    texture_image = load_block_texture(block_id)
    texture_image.show()  # Display the texture image
