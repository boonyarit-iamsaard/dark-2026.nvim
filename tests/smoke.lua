-- Headless smoke test. Run via `make test`, which isolates the runtimepath so
-- this exercises the repo rather than whatever is in the user's config.
--
-- Deliberately dependency-free: a colorscheme has little behaviour to unit
-- test, and what can actually break is (a) a Lua error at load, (b) a color
-- that Neovim will not accept, and (c) an option that stops taking effect.

local failures = {}
local checked = 0

local function check(ok, msg)
  checked = checked + 1
  if not ok then
    table.insert(failures, msg)
  end
end

local function is_color(v)
  return type(v) == "string" and (v == "NONE" or v:match("^#%x%x%x%x%x%x$") ~= nil)
end

-- (a) The colorscheme loads, and loading it twice is safe.
vim.cmd.colorscheme("dark-2026")
vim.cmd.colorscheme("dark-2026")
check(vim.g.colors_name == "dark-2026", "colors_name is " .. tostring(vim.g.colors_name))
check(vim.o.termguicolors, "termguicolors was not set")
check(vim.o.background == "dark", "background is " .. vim.o.background)

-- (b) Every color Neovim was handed is a value it accepts.
local hl, p = require("dark-2026").highlights()
local count = 0
for group, spec in pairs(hl) do
  count = count + 1
  for _, key in ipairs({ "fg", "bg", "sp" }) do
    if spec[key] ~= nil then
      check(is_color(spec[key]), ("%s.%s = %s"):format(group, key, vim.inspect(spec[key])))
    end
  end
end
check(count > 500, "only " .. count .. " highlight groups were built")

-- The palette itself, including values only reachable through blend().
for name, value in pairs(p) do
  if type(value) == "string" then
    check(is_color(value), ("palette.%s = %q"):format(name, value))
  end
end
for name, value in pairs(p.ansi) do
  check(is_color(value), ("palette.ansi.%s = %q"):format(name, value))
end

-- The 16 terminal slots are populated.
for i = 0, 15 do
  check(is_color(vim.g["terminal_color_" .. i]), "terminal_color_" .. i .. " is unset or malformed")
end

-- (c) Options still reach the highlight table.
local dark2026 = require("dark-2026")

dark2026.setup({ transparent = true })
check(dark2026.highlights().Normal.bg == "NONE", "transparent did not clear Normal.bg")
check(dark2026.highlights().NormalFloat.bg ~= "NONE", "transparent should not clear float backgrounds")

dark2026.setup({ transparent = false, italic_comments = false })
check(dark2026.highlights().Comment.italic == false, "italic_comments = false did not take effect")

dark2026.setup({
  italic_comments = true,
  on_highlights = function(h, palette)
    h.Normal = { fg = palette.error }
  end,
})
check(dark2026.highlights().Normal.fg == p.error, "on_highlights hook did not run last")

-- The lualine theme resolves and is shaped the way lualine expects.
local lualine = require("lualine.themes.dark-2026")
for _, mode in ipairs({ "normal", "insert", "visual", "replace", "command", "inactive" }) do
  check(type(lualine[mode]) == "table", "lualine theme is missing " .. mode)
  for _, section in ipairs({ "a", "b", "c" }) do
    check(is_color(lualine[mode][section].bg), ("lualine.%s.%s.bg"):format(mode, section))
    check(is_color(lualine[mode][section].fg), ("lualine.%s.%s.fg"):format(mode, section))
  end
end

if #failures > 0 then
  io.stderr:write(("FAIL — %d problem(s):\n"):format(#failures))
  for _, f in ipairs(failures) do
    io.stderr:write("  " .. f .. "\n")
  end
  vim.cmd("cquit 1")
end

print(("ok — %d highlight groups, %d checks passed"):format(count, checked))
vim.cmd("quit")
