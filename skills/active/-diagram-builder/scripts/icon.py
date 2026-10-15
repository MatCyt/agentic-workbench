"""Print a draw.io image style for a Material Symbol recolored to a hex color.

Usage: python icon.py <Material_Symbol_Name> <#RRGGBB>
Example: python icon.py Lock '#004791'
"""

import base64
import sys
import urllib.request

ICON_URL = "https://icons.diagrams.net/assets/material-symbols/1/{}.svg"


def icon_style(name: str, color: str) -> str:
    """Return `shape=image;...;image=data:image/svg+xml,<b64>;` with the icon's fill set to `color`."""
    # icons.diagrams.net returns 403 without a User-Agent.
    req = urllib.request.Request(ICON_URL.format(name), headers={"User-Agent": "curl/8"})
    svg = urllib.request.urlopen(req).read().decode().replace("#000000", color)
    b64 = base64.b64encode(svg.encode()).decode()
    # draw.io's data-URI form has no ";base64" marker.
    return f"shape=image;html=1;imageAspect=0;aspect=fixed;image=data:image/svg+xml,{b64};"


if __name__ == "__main__":
    sys.stdout.write(icon_style(sys.argv[1], sys.argv[2]) + "\n")
