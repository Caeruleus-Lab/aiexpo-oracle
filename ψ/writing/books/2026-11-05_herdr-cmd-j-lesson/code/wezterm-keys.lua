    key = 'k',
    mods = 'CMD',
    action = act.SendKey { key = 'F12' },
  },
  -- CMD+J → F11 for the herdr-ask input box (herdr side: keys.command f11).
  -- Same reason as CMD+K above: a real Cmd chord cannot reach herdr, so send a
  -- plain key it parses. F11 is free; f7-f10 are LinearMouse, f12 is goto.
  -- `herdr --remote <ssh-target> --session <s>` tabs: herdr 0.9.1 runs no
  -- keys.command popups for remote clients (measured 2026-10-05, F11 reached
  -- white and nothing ran on either side). So for those tabs CMD+J opens a
  -- short split that ssh's to the target and runs herdr-ask-remote there,
  -- which finds the session's focused pane and hands over to herdr-ask.
  {
    key = 'j',
    mods = 'CMD',
    action = wezterm.action_callback(function(window, pane)
      local ok, info = pcall(function() return pane:get_foreground_process_info() end)
      local argv = (ok and info and info.argv) or {}
      local target, session
      for i, a in ipairs(argv) do
        if a == '--remote' then target = argv[i + 1] end
        if a == '--session' then session = argv[i + 1] end
      end
      if not target then
        window:perform_action(act.SendKey { key = 'F11' }, pane)
        return
      end
      window:perform_action(act.SplitPane {
        direction = 'Down',
        size = { Cells = 12 },
        command = { args = { 'ssh', '-t', target,
          '~/.local/bin/herdr-ask-remote ' .. (session or 'default') } },
      }, pane)
    end),
  },
  -- CMD+\\ → F6 for `maw arrange organize` (herdr side: keys.command f6).
  -- Deliberately NOT a global skhd hotkey: a bare Cmd chord bound system-wide
  -- steals it from every app, and arranging is a herdr-time action. F6 because
  -- f7-f10 are LinearMouse, f11 is ⌘J and f12 is ⌘K.
  {
    key = '\\',
    mods = 'CMD',
    action = act.SendKey { key = 'F6' },
  },
  -- CMD+G → F5 for the herdr "go" popup (herdr side: keys.command f5). Same
  -- reason as CMD+K/J: a real Cmd chord cannot reach herdr, so send a plain key.
  -- F5 was free; f6 is arrange, f7-f10 LinearMouse, f11 is ⌘J, f12 is ⌘K.
  -- Right now f5 is only the mouse probe; the real popup replaces it later.
  {
    key = 'g',
    mods = 'CMD',
    action = act.SendKey { key = 'F5' },
  },
  -- CMD+S -> F4 for herdr-soulcast: broadcast one line to every body of this
  -- oracle across herdr sessions (herdr side: keys.command f4). Same reason as
  -- CMD+K/J: a real Cmd chord cannot reach herdr. F4 was free.
  {
    key = 's',
    mods = 'CMD',
    action = act.SendKey { key = 'F4' },
  },
  -- CMD+L -> F3 for herdr-wtcast: one line to every agent of this repo (main + its worktrees)
  -- (herdr side: keys.command f3). LarisCo's learning copy of CMD+J, 2026-10-31.
  -- F3 was free (f4 soulcast, f5 go, f6 arrange, f7-f10 LinearMouse, f11 ask, f12 goto).
  {
    key = 'l',
    mods = 'CMD',
    action = act.SendKey { key = 'F3' },
  },
  -- CMD+I -> F2 for herdr-status: is every agent of this session online, on every machine (pid, bot, plugin, token,
  -- usage, ctx). herdr side: keys.command f2. Nat 2026-11-04. F2 was free (f3 wtcast, f4 soulcast … f12 goto).
  {
    key = 'i',
    mods = 'CMD',
    action = act.SendKey { key = 'F2' },
  },
  -- CMD+X types "exit" + Enter into the focused pane. \r not \n: terminals
  -- send CR for Enter. Plain text passes through Herdr to the active pane
  -- untouched, so no Herdr bind needed.
  {
    key = 'x',
