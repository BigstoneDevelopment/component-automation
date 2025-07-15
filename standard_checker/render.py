from PIL import Image, ImageDraw

from .online import load_block_texture
from .block import Structure, Block


# === CONFIGURATION ===

BLOCK_COLORS: dict[str, tuple[int, int, int] | None] = {
    "minecraft:stone": (120, 120, 120),
    "minecraft:grass": (100, 200, 100),
    "minecraft:dirt": (134, 96, 67),
    "minecraft:smooth_stone": (200, 200, 200),
    "minecraft:calcite": (255, 255, 255),
    "minecraft:polished_blackstone": (50, 50, 50),
    "minecraft:redstone_block": (255, 0, 0),
}


# === RENDERING ===

def iso_project(x: float, y: float, z: float) -> tuple[float, float]:
    return (x - z) * 8, (x + z) * 4 - y * 8


def draw_voxel(draw: ImageDraw.ImageDraw, x: float, y: float, color: tuple[int, int, int] | None) -> None:
    if color is None:
        return

    top = [(x, y), (x + 8, y + 4), (x, y + 8), (x - 8, y + 4)]
    left = [(x - 8, y + 4), (x, y + 8), (x, y + 16), (x - 8, y + 12)]
    right = [(x, y + 8), (x + 8, y + 4), (x + 8, y + 12), (x, y + 16)]

    draw.polygon(top, fill=tuple(min(int(c * 1.1), 255) for c in color))
    draw.polygon(left, fill=tuple(int(c * 0.9) for c in color))
    draw.polygon(right, fill=tuple(int(c * 0.7) for c in color))


def draw_voxel_texture(img: Image.Image, atlas: Image.Image, x: int, y: int) -> None:
    img = img.resize((16, 16), Image.Resampling.NEAREST)  # upscale for isometric
    img.paste(img, (x - 8, y), img.convert("RGBA"))


def render_structure(structure: Structure, output_path: str = "img.png", debug: bool = False) -> Image.Image:
    # w, h = 128, 128
    # Estimate size from structure dimensions
    size_x = len(structure[0][0])
    size_y = len(structure[0])
    size_z = len(structure)

    # Estimate projected bounds
    margin = 32  # extra padding
    w = (size_x + size_z) * 8 + margin
    h = (size_x + size_z) * 4 + size_y * 8 + margin
    img = Image.new("RGBA", (w, h), (255, 255, 255, 0))

    blocks: list[tuple[int, int, int, Block]] = []
    for z, layer in enumerate(structure):
        for y, row in enumerate(layer):
            for x, block in enumerate(row):
                if block is None:
                    continue
                blocks.append((x, y, z, block))

    blocks.sort(key=lambda b: b[0] + b[1] + b[2])  # back to front

    center_x = (size_x - 1) / 2
    center_y = (size_y - 1) / 2
    center_z = (size_z - 1) / 2
    proj_cx, proj_cy = iso_project(center_x, center_y, center_z)

    offset_x = w // 2 - int(proj_cx)
    offset_y = h // 2 - int(proj_cy)

    for x, y, z, block in blocks:
        sx, sy = iso_project(x, y, z)
        cx, cy = int(sx) + offset_x, int(sy) + offset_y

        texture = load_block_texture(block.id)
        draw_voxel_texture(img, texture, cx, cy)

    if debug:
        img.show()
    img.save(output_path)

    return img


__all__ = ["render_structure"]
