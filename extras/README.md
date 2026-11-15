# Extras

Ports of the Dark 2026 palette to the other tools that surround the editor, so a
tmux session or a lazygit popup does not break the illusion.

These are plain config fragments — nothing here is loaded by the Neovim plugin,
and none of it is required. Copy what you want.

| File | Tool | How to use |
| --- | --- | --- |
| [`ghostty/dark-2026`](ghostty/dark-2026) | Ghostty | copy into `~/.config/ghostty/themes/`, then `theme = dark-2026` |
| [`terminal/dark-2026.terminal`](terminal/dark-2026.terminal) | macOS Terminal.app | double-click to import, then make it the default profile |
| [`tmux/dark-2026.conf`](tmux/dark-2026.conf) | tmux | `source-file` it from `tmux.conf` |
| [`lazygit/dark-2026.yml`](lazygit/dark-2026.yml) | lazygit (shell) | merge into `~/.config/lazygit/config.yml` |
| [`lazyvim/lazygit.lua`](lazyvim/lazygit.lua) | lazygit (Neovim float) | drop into `~/.config/nvim/lua/plugins/` |
| [`lazydocker/dark-2026.yml`](lazydocker/dark-2026.yml) | lazydocker | merge into `~/.config/lazydocker/config.yml` |
| [`opencode/dark-2026.json`](opencode/dark-2026.json) | OpenCode | copy into `~/.config/opencode/themes/`, then `"theme": "dark-2026"` in `tui.json` |
| [`claude-code/dark-2026.json`](claude-code/dark-2026.json) | Claude Code | copy into `~/.claude/themes/`, then pick it in `/theme` |
| [`windows-terminal/dark-2026.json`](windows-terminal/dark-2026.json) | Windows Terminal | paste the scheme into `schemes` in `settings.json`, then `"colorScheme": "Dark 2026"` in a profile |
| [`oh-my-posh/dark-2026.omp.json`](oh-my-posh/dark-2026.omp.json) | Oh My Posh | `oh-my-posh init pwsh --config <path> \| Invoke-Expression` |

## lazygit needs both files

Themed twice on purpose. lazygit opened from a shell reads
`~/.config/lazygit/config.yml`. lazygit opened from Neovim — LazyVim's
`<leader>gg` — goes through snacks.nvim, which writes its own
`~/.cache/nvim/lazygit-theme.yml` on every `ColorScheme` event and appends it to
`$LG_CONFIG_FILE`. Later files win, so that generated theme overrides your
config and the two views drift apart.

snacks derives that theme from highlight groups, and its defaults pick ones that
do not carry the right colors here: `activeBorderColor` comes from
`MatchParen.fg`, which Dark 2026 leaves unset (VS Code draws a bracket match as
a background only), so the focused panel border loses its accent entirely;
`optionsTextColor` comes from `Function.fg`, the syntax purple. The Lua spec
pins every key to the same hexes as the YAML instead. Keep the two in sync.

## Colors

Every value carries a comment naming the VS Code key it came from, matching the
convention in [`lua/dark-2026/palette.lua`](../lua/dark-2026/palette.lua). If a
color here looks wrong next to the editor, the palette is the source of truth —
fix it there first, then propagate.

The OpenCode file is an exception: OpenCode reads themes with a strict JSON
parser, so it cannot carry comments. Instead its `defs` block names each hex
after the `palette.lua` field it was copied from (`bg`, `accent`, `git_add`,
...), and the `theme` block only ever references those names. Provenance is one
lookup away in the palette rather than beside the value. A few of those names
(`accent`, `text`, `error`, `info`) coincide with OpenCode's own theme keys;
OpenCode resolves `defs` before theme keys, so `"text": "fg_term"` and
`"markdownStrong": "text"` both mean what they look like they mean.

The Claude Code file has neither comments nor a `defs` block — its `overrides`
are bare hexes — so its provenance lives here instead. Every value is a
`palette.lua` field; the two `*Dimmed` diff backgrounds are `diff_add` /
`diff_delete` recomputed at half their upstream alpha, since Claude Code fades a
rejected diff and the palette has no key for that. Tokens not listed fall
through to Claude Code's built-in `dark` preset (the `rainbow_*` gradient is
left alone on purpose).

| Token(s) | Palette field |
| --- | --- |
| `claude`, `permissionShimmer`, `rate_limit_fill`, `briefLabelClaude` | `accent` |
| `claudeShimmer` | `link_active` |
| `permission` | `accent_dim` |
| `ide` | `accent_badge` |
| `suggestion` | `link` |
| `text` | `fg_term` |
| `inverseText` | `on_accent` |
| `inactive`, `promptBorderShimmer` | `fg_dim` |
| `inactiveShimmer`, `briefLabelYou` | `fg_ui` |
| `subtle`, `promptBorder` | `fg_disabled` |
| `remember`, `merged`, `effortUltra`, `purple_FOR_SUBAGENTS_ONLY` | `purple` |
| `success` | `ok` |
| `error` | `error` |
| `warning` | `warn` |
| `warningShimmer`, `fastMode`, `yellow_FOR_SUBAGENTS_ONLY` | `yellow` |
| `autoAccept`, `fastModeShimmer` | `git_change` |
| `planMode`, `green_FOR_SUBAGENTS_ONLY` | `green` |
| `bashBorder`, `orange_FOR_SUBAGENTS_ONLY` | `orange` |
| `diffAdded` / `diffRemoved` | `diff_add` / `diff_delete` |
| `diffAddedWord` / `diffRemovedWord` | `diff_text_add` / `diff_text_del` |
| `diffAddedDimmed` / `diffRemovedDimmed` | `diff_add` / `diff_delete` at half alpha |
| `userMessageBackground` | `bg_panel` |
| `userMessageBackgroundHover` | `bg_line` |
| `bashMessageBackgroundColor` | `bg_float` |
| `memoryBackgroundColor` | `hint_bg` |
| `selectionBg` | `bg_visual` |
| `rate_limit_empty` | `bg_inactive` |
| `red_FOR_SUBAGENTS_ONLY` | `red` |
| `blue_FOR_SUBAGENTS_ONLY` | `blue` |
| `pink_FOR_SUBAGENTS_ONLY` | `ansi.bright_magenta` |
| `cyan_FOR_SUBAGENTS_ONLY` | `ansi.bright_cyan` |

The Oh My Posh file is strict JSON too, so it follows the OpenCode rule: its
`palette` block names each hex after its `palette.lua` field, and the segments
reference only those names (`p:link`, `p:purple`, ...). The prompt layout itself
is one owner's choice, not part of the theme; keep the `palette` block and
restyle the segments freely.

The tmux file exposes its palette as `@custom_*` user options rather than baking
hexes into status-line formats, so you can write your own status line against
role names:

```tmux
set -ga status-left "#[fg=#{@custom_cyan}] #{pane_current_command} "
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

[`ghostty/dark-2026`](ghostty/dark-2026) is exactly that pairing, written in
Ghostty's config syntax. Port it to another emulator by keeping the same 16
slots — the surface and cursor colors around them are the only part that needs
translating.

[`terminal/dark-2026.terminal`](terminal/dark-2026.terminal) is the same port for
macOS Terminal.app, with two differences: it has no cursor-text color, and its
selection is `bg_visual` — the upstream selection blended over the background —
because the profile stores opaque colors. Terminal.app archives each color as a
binary `NSColor`, so the profile is generated rather than hand-written: edit
the hexes in [`terminal/build.py`](terminal/build.py), each commented with its
VS Code key, and rerun it. `build.py --check` fails if the two have drifted.
The colors are stored the way catppuccin's Terminal.app profiles store them, in
generic ("calibrated") RGB rather than sRGB, so they can render a shade off the
hexes; an sRGB-tagged profile was rejected by Terminal.app as corrupt.

[`windows-terminal/dark-2026.json`](windows-terminal/dark-2026.json) is the
Ghostty pairing as a Windows Terminal scheme: the same surfaces, cursor and 16
slots, with `selectionBackground` the opaque base of
`editor.selectionBackground`, as in Ghostty. Windows Terminal has no
cursor-text color. The file is a `{ "schemes": [...] }` object, so it can also
be dropped in a [JSON fragment extension](https://learn.microsoft.com/windows/terminal/json-fragment-extensions)
directory as is.

Terminal.app only renders 24-bit color from macOS 26 Tahoe. On earlier releases
the profile still themes the shell, but Neovim needs `termguicolors`, so the
colorscheme itself will not render correctly there — use Ghostty or another
truecolor terminal.
