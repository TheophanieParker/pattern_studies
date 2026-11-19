
import argparse
import math
import random
from pathlib import Path


def generate_pattern(size=800, grid=16, seed=42):
    """Generate a geometric SVG pattern using symmetry and rotation."""
    rng = random.Random(seed)
    cell = size / grid
    elements = []

    for row in range(grid):
        for col in range(grid):
            x = col * cell + cell / 2
            y = row * cell + cell / 2

            # Mirror the pattern across its vertical axis.
            mirror_col = min(col, grid - 1 - col)
            local_rng = random.Random(seed + row * grid + mirror_col)

            rotation = local_rng.choice([0, 45, 90, 135])
            radius = cell * local_rng.uniform(0.20, 0.42)
            stroke_width = max(1, cell * 0.025)

            elements.append(
                f'<rect x="{x - radius:.2f}" y="{y - radius:.2f}" '
                f'width="{2 * radius:.2f}" height="{2 * radius:.2f}" '
                f'fill="none" stroke="#171717" '
                f'stroke-width="{stroke_width:.2f}" '
                f'transform="rotate({rotation} {x:.2f} {y:.2f})"/>'
            )

            if local_rng.random() > 0.55:
                elements.append(
                    f'<circle cx="{x:.2f}" cy="{y:.2f}" '
                    f'r="{radius * 0.35:.2f}" fill="#BC3B2D"/>'
                )

    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{size}" height="{size}" viewBox="0 0 {size} {size}">'
        f'<rect width="100%" height="100%" fill="#F2EFE8"/>'
        + "".join(elements)
        + '</svg>'
    )

    return svg


def main():
    parser = argparse.ArgumentParser(
        description="Generate geometric SVG pattern studies."
    )
    parser.add_argument("--size", type=int, default=800)
    parser.add_argument("--grid", type=int, default=16)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", default="pattern.svg")
    args = parser.parse_args()

    if args.size <= 0 or args.grid <= 0:
        parser.error("--size and --grid must be positive integers")

    svg = generate_pattern(args.size, args.grid, args.seed)
    Path(args.output).write_text(svg, encoding="utf-8")

    print(f"Pattern saved to {args.output}")


if __name__ == "__main__":
    main()
