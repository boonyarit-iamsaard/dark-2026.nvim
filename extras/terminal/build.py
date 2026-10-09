#!/usr/bin/env python3
"""Generate dark-2026.terminal, the Dark 2026 profile for macOS Terminal.app.

Terminal.app stores each color as an NSKeyedArchiver-encoded NSColor, embedded
in the profile plist as base64 data. That cannot be written or reviewed by
hand, so the hexes live here, each with the VS Code key it comes from, and the
.terminal file is generated from them:

    python3 extras/terminal/build.py           # rewrite dark-2026.terminal
    python3 extras/terminal/build.py --check   # fail if it is out of date

Standard library only, so it runs anywhere, not just on macOS.
"""

import plistlib
import sys
from pathlib import Path

OUT = Path(__file__).with_name("dark-2026.terminal")

PROFILE_NAME = "Dark 2026"

# Terminal.app profile key -> hex. Same values as ghostty/dark-2026.
COLORS = {
    # --- surfaces -------------------------------------------------------------
    # editor.background, rather than terminal.background (#191a1b): a terminal
    # window is the whole surface here, not a panel docked below an editor.
    "BackgroundColor": "#121314",
    # terminal.foreground
    "TextColor": "#cccccc",
    # terminal.foreground; Terminal.app otherwise picks its own bold color.
    "BoldTextColor": "#cccccc",
    # editor.selectionBackground (#276782dd) blended over editor.background —
    # palette.lua's bg_visual, the color the editor actually renders.
    "SelectionColor": "#245c73",
    # terminalCursor.background. Terminal.app has no cursor-text color, so
    # terminalCursor.foreground has nowhere to go.
    "CursorColor": "#bfbfbf",
    # --- the 16 ANSI colors -----------------------------------------------------
    # dark-2026.jsonc leaves every terminal.ansi* key commented out, so VS Code
    # falls back to its built-in defaults — see `M.ansi` in
    # lua/dark-2026/palette.lua.
    "ANSIBlackColor": "#000000",
    "ANSIRedColor": "#cd3131",
    "ANSIGreenColor": "#0dbc79",
    "ANSIYellowColor": "#e5e510",
    "ANSIBlueColor": "#2472c8",
    "ANSIMagentaColor": "#bc3fbc",
    "ANSICyanColor": "#11a8cd",
    "ANSIWhiteColor": "#e5e5e5",
    "ANSIBrightBlackColor": "#666666",
    "ANSIBrightRedColor": "#f14c4c",
    "ANSIBrightGreenColor": "#23d18b",
    "ANSIBrightYellowColor": "#f5f543",
    "ANSIBrightBlueColor": "#3b8eea",
    "ANSIBrightMagentaColor": "#d670d6",
    "ANSIBrightCyanColor": "#29b8db",
    "ANSIBrightWhiteColor": "#e5e5e5",
}


def ns_color(hex_color):
    """Archive an opaque color the way NSKeyedArchiver writes NSColor.

    The shape mirrors catppuccin/Terminal.app's profiles, which import cleanly:
    calibrated RGB (NSColorSpace 1) with NSRGB only. An sRGB archive carrying
    NSCustomColorSpace/NSComponents was tried first and Terminal.app rejected
    the profile as corrupt.
    """
    r, g, b = (int(hex_color[i : i + 2], 16) / 255 for i in (1, 3, 5))
    archive = {
        "$archiver": "NSKeyedArchiver",
        "$version": 100000,
        "$top": {"root": plistlib.UID(1)},
        "$objects": [
            "$null",
            {
                "$class": plistlib.UID(2),
                "NSColorSpace": 1,
                "NSRGB": f"{r:.10g} {g:.10g} {b:.10g}".encode() + b"\0",
            },
            {"$classname": "NSColor", "$classes": ["NSColor", "NSObject"]},
        ],
    }
    return plistlib.dumps(archive, fmt=plistlib.FMT_BINARY, sort_keys=False)


def build():
    profile = {
        "name": PROFILE_NAME,
        "type": "Window Settings",
        "ProfileCurrentVersion": 2.04,
        **{key: ns_color(hex_color) for key, hex_color in COLORS.items()},
    }
    return plistlib.dumps(profile, fmt=plistlib.FMT_XML).decode()


def main():
    text = build()
    if "--check" in sys.argv[1:]:
        if not OUT.exists() or OUT.read_text() != text:
            sys.exit(f"{OUT.name} is out of date; run {Path(__file__).name}")
        return
    OUT.write_text(text)


if __name__ == "__main__":
    main()
