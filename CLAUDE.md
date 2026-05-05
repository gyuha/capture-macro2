# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run all tests
python -m pytest tests/ -v

# Run a single test
python -m pytest tests/test_input_press_delay.py::test_config_defaults -v

# Recompile UI files after editing .ui XML
./ui-compile.sh

# Bump version (updates both version.py and .version atomically)
python tools/update_version.py X.Y.Z

# Build macOS DMG
./build-mac.sh
```

## Architecture

**Threading model:** `ActionController` runs macros in a daemon thread and emits Qt signals (`signal_mouse_event`, `signal_key_event`) back to the main thread. `AppCore` receives those signals and dispatches to `InputController`. Never call pynput directly from any thread other than via this signal path.

**Singletons:** `Config` (QSettings-backed settings) and `AppCore` both use `SingletonMeta`. In tests, clear between cases with `SingletonMeta._instances.clear()`.

**Config → InputController flow:** `InputController.click_mouse()` and `press_key()` read `Config()` singleton at call time for `click_press_min/max` and `key_press_min/max` (ms). No constructor injection needed — Config is always available.

**macOS requirement:** pynput requires Accessibility permission. The `PYNPUT_BACKEND` env var must be set to `"darwin"` *before* any pynput import. This is done in `app/app_core.py` with a platform guard at the top of the file.

## UI Files

`.ui` files (Qt Designer XML) are compiled to `*_ui.py` via `pyside6-uic` by `./ui-compile.sh`. When adding new widgets programmatically (e.g., adding rows to a form layout), edit the `*_ui.py` file directly rather than modifying the `.ui` XML — recompiling would overwrite hand-written additions.

## Version Management

`.version` is the source of truth for the build script (`build-mac.sh` reads it). `app/config/version.py` hardcodes the same value. Always use `python tools/update_version.py X.Y.Z` to keep both in sync — never edit them separately.

## Testing

Tests use `pytest`. Singleton state leaks between tests — always clear with `SingletonMeta._instances.clear()` in a fixture before instantiating `Config` or `AppCore`. See `tests/test_input_press_delay.py` for the pattern.
