# Extras

Ports of the Dark 2026 palette to the other tools that surround the editor, so a
tmux session or a lazygit popup does not break the illusion.

These are plain config fragments — nothing here is loaded by the Neovim plugin,
and none of it is required. Copy what you want.

| File | Tool | How to use |
| --- | --- | --- |
| [`tmux/dark-2026.conf`](tmux/dark-2026.conf) | tmux | `source-file` it from `tmux.conf` |
| [`lazygit/dark-2026.yml`](lazygit/dark-2026.yml) | lazygit | merge into `~/.config/lazygit/config.yml` |
| [`lazydocker/dark-2026.yml`](lazydocker/dark-2026.yml) | lazydocker | merge into `~/.config/lazydocker/config.yml` |

## Colors

Every value carries a comment naming the VS Code key it came from, matching the
convention in [`lua/dark-2026/palette.lua`](../lua/dark-2026/palette.lua). If a
color here looks wrong next to the editor, the palette is the source of truth —
fix it there first, then propagate.

The tmux file exposes its palette as `@custom_*` user options rather than baking
hexes into status-line formats, so you can write your own status line against
role names:

```tmux
set -ga status-left "#[bg=#{@custom_bg},fg=#{@custom_cyan}] #{pane_current_command} "
```

It deliberately styles only chrome that every tmux has — status, panes, windows,
copy mode. Status-line *content* is personal, and anything referencing battery or
online-status needs plugins you may not run, so none of that is included.

## Terminal

The 16 ANSI slots the theme uses are in
[`lua/dark-2026/palette.lua`](../lua/dark-2026/palette.lua) under `M.ansi`. They
are VS Code's built-in defaults, since the theme leaves every `terminal.ansi*`
key unset. Pair them with `#121314` background and `#cccccc` foreground for a
terminal scheme that matches the editor.
