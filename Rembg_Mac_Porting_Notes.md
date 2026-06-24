# Rembg Fuse — macOS Porting Notes

> These notes document every issue encountered running the Rembg Fuse on macOS (DaVinci Resolve Lite, App Store version, Apple Silicon). The original project was built primarily for Windows. This is intended as a guide for contributing Mac support upstream.

---

## Environment

- **Machine**: Apple Silicon Mac (arm64)
- **DaVinci Resolve**: Lite (free, App Store version — fully sandboxed)
- **macOS**: 15.x (Sequoia)
- **Python used**: python.org Python 3.14 at `/Library/Frameworks/Python.framework/Versions/3.14/`

---

## Issues & Fixes

### 1. `python-tk` not installed by default on Homebrew Python
The `rembg_manager.py` GUI uses `tkinter`, which is not bundled with Homebrew Python by default.

**Fix**: `brew install python-tk@3.14`

---

### 2. Homebrew Python blocks system-wide `pip install` (PEP 668)
Running `pip install rembg` with Homebrew Python fails with an "externally managed environment" error.

**Fix**: Use a virtual environment (`python3 -m venv ~/.rembg_venv`) or pass `--break-system-packages`. For DaVinci Resolve use, a venv is cleaner but see issue #3.

---

### 3. DaVinci Resolve Lite (App Store sandbox) blocks Python from `~/` and `/opt/homebrew/`
The App Sandbox in the Mac App Store version of Resolve **cannot execute binaries** from:
- `~/.rembg_venv/bin/python3` (home directory — blocked)
- `/opt/homebrew/bin/python3` (Homebrew — blocked)

**Only python.org Python is permitted**, as it installs to `/Library/Frameworks/Python.framework/` which is outside the user home and is a whitelisted system path.

**Fix**: Install Python from python.org. Install rembg into it:
```bash
/Library/Frameworks/Python.framework/Versions/3.14/bin/python3 -m pip install "rembg[cpu]" pillow
```

**Note for contributors**: The Fuse should detect the OS and on macOS suggest python.org Python specifically, not just "python3".

---

### 4. `scipy` installs to user site-packages, not framework site-packages
When pip installs `scipy` without sudo, it goes to `~/Library/Python/3.14/lib/python/site-packages/`. The sandboxed subprocess cannot access `~/Library/` (it resolves to the container's home, not the real one).

**Fix**: Force install to the framework's system site-packages:
```bash
/Library/Frameworks/Python.framework/Versions/3.14/bin/python3 -m pip install scipy \
  --target /Library/Frameworks/Python.framework/Versions/3.14/lib/python3.14/site-packages/
```

---

### 5. `handle:close()` unreliable in LuaJIT on macOS (success detection bug)
The Fuse uses `executionSuccess = handle:close()` after `io.popen()` to detect if Python ran successfully. On macOS with LuaJIT (used by Resolve), `handle:close()` returns `nil` even when the process exits with code 0. This causes the Fuse to always think Python failed, skip loading the output PNG, and pass through the original image — even though Python ran correctly.

**Symptom**: Status shows `[COMPLETE] Frame N` but background is never removed.

**Fix**: Detect success from the Python script's stdout instead of the exit code:
```lua
result = handle:read("*a")
handle:close()
-- io.popen:close() is unreliable on macOS — check output text instead
executionSuccess = result and result:find("%[COMPLETE%]") ~= nil
```

---

### 6. FileControl in Inspector truncates long paths when typed manually
Typing `/Library/Frameworks/Python.framework/Versions/3.14/bin/python3` into the Python Path field truncates it (e.g. to `...bin/pyt`), producing a "no such file" error.

**Fix**: Always use the **Browse** button to select the Python binary rather than typing the path. Consider shortening the default path or adding input validation in the Fuse.

---

### 7. `NotifyChanged` crashes on startup when `param` is nil
When DaVinci Resolve loads a project, it calls `NotifyChanged` for all inputs during initialisation with `param = nil`. The function immediately accesses `param.Value` without a nil check, causing a Lua error that prevents models from loading and may break other startup behaviour.

**Fix**: Add a nil guard at the top of `NotifyChanged`:
```lua
function NotifyChanged(inp, param, time)
    if not param then return end
    ...
```

---

### 8. Model dropdown empty after restart
`CCS_AddString` dynamically adds items to the `InModel` combo box, but these additions are **not persisted** across sessions. On restart, `GetData("models")` returns the saved list but the combo box is visually empty. The early-return guard (`if #available_models > 0 then return end`) prevents the combo box from being repopulated.

**Fix**: Remove the early-return guard so `GetModels()` and `CCS_AddString` always run when `param.Value == 0`:
```lua
if inp == InSetup then
    if param.Value == 0 then
        local check_models = GetModels()
        if #check_models > 0 then
            for _, model in ipairs(check_models) do
                InModel:SetAttrs({ CCS_AddString = model })
            end
        end
        self:SetData("models", check_models)
    end
end
```

---

### 9. Python path not persisted across restarts without user re-entry
`GetData("python_path")` is only set when the user interacts with the Python Path field in the Inspector. On a fresh project or after restart without interaction, it falls back to `python3` (which is Homebrew/system Python — blocked by sandbox).

**Fix**: In `ProcessWithPython`, always fall back to reading `python_path.txt` if `GetData` is empty or default:
```lua
local pythonpath = self:GetData("python_path")
if not pythonpath or pythonpath == "python3" or pythonpath == "pythonw" then
    local python_location = self.Comp:MapPath('Fuses:/Rembg/python_path.txt')
    local pfile = io.open(python_location, "r")
    if pfile then
        pythonpath = pfile:read("*a"):match("^%s*(.-)%s*$")
        pfile:close()
        self:SetData("python_path", pythonpath)
    end
end
```

---

### 10. Default Python path in Inspector shows `python3` instead of the correct path
The `INPS_DefaultText` for the Python Path control defaults to `python3`, which does not work on Mac (sandbox blocks it, and it's Homebrew anyway).

**Fix**: Change the default to the python.org path:
```lua
local defaultPython = '/Library/Frameworks/Python.framework/Versions/3.14/bin/python3.14'
```

Ideally this should be detected dynamically rather than hardcoded.

---

### 11. "Open Rembg Setup" button does not work from Inspector (Resolve Lite)
The setup button runs the `rembg_manager.py` GUI via `os.execute()`. In DaVinci Resolve Lite (sandboxed), this is blocked entirely — the button does nothing.

**Workaround**: Run the manager manually from Terminal:
```bash
/Library/Frameworks/Python.framework/Versions/3.14/bin/python3 \
  "/path/to/Fuses/Rembg/rembg_manager.py"
```

**For contributors**: On Mac, `os.execute()` from a sandboxed Fuse is unreliable. Consider an alternative launch mechanism or document this limitation clearly.

---

## Suggested Contributions

- Auto-detect python.org Python on macOS and pre-fill the path
- Add macOS-specific install instructions to the README
- Fix the nil `param` crash in `NotifyChanged`
- Fix the model dropdown repopulation bug
- Fix `handle:close()` success detection (use stdout text instead)
- Fix `python_path.txt` fallback so path persists without user interaction
- Note in README that Resolve Lite (App Store) requires python.org Python specifically
- Note that `scipy` and other packages must be installed to the framework site-packages, not user site-packages

---

## Repo

https://github.com/Akascape/Rembg-Fuse
