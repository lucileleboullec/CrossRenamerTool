# Design Choices

This page explains the UX and architectural decision made during development, and the reasoning behind each one.

## UI - QStackedWidget over collapsible sections
**Decisions**: Use a tab-based navigation (`QStackedWidget` + custom nav buttons) instead of collapsible sections.  
**Why**:  
A renaming tool has many features - Rename, Prefix/Suffix, Search/Replace, Insert/Remove, Convert Case, Utils. Whit collapsible sections, all of them would be visible at once, requiring the artist to scroll and mentally parse what is expanded and what is not.  
With `QStackedWidget`, only one page is visible at a time. The UI stays compact and the artist focuses on one task. The window height stays fixed regardless of which page is open.  
**Trade-off**: Features are not immediately all visible - the artist needs to know which tab to click. This is acceptable because the tab labels are explicit and the features are logically grouped.

## UI - GLobal mode selector always visible
**Decision**: The Apply on selector (Selected/Hierarchy/Scene) is fixed at the top of the window, outside the tab pages.  
**Why**:  
The mode applies to every operation - Rename, Prefix/Suffix, etc. If it lived inside each page, the artist would to set it repeatedly. Keeping it global means setting it once and forgetting it.  
**Trade-off**: The mode is shared across all operations - changing it affects the next action regardless of which page is active. This is documented in the tooltips.

## UI -  Preset Manager as dialog, not inline
**Decision**: Preset management (add, remove, reorder, rename) lives in a dedicated `PresetDialog`, not inline in the `PrefixSuffixPage`.  
**Why**:  
Managing presets is a rare action - it happens once when setting up the tool, not on every rename. Inline management (a list with add/remove buttons next to the combobox) would clutter the daily-use UI with controls that are almost never needed.  
The dialog keeps the main UI clean. The right-click context menu on the combobox provides a fast path for the most common actions (save/remove) without opening the dialog.

## Architecture - Pure functions in `renamer.py`
**Decision**: All renaming logic lives in `renamer.py` as pure Python functions with no DCC dependency.  
**Why**:  
- **Testability** - unit tests run without a DCC session. This is critical for CI/CD.
- **Reusability** - the same logic could be reused in an other DCC adapter or a standalone CLI tool.
- **Clarity** -  a function that takes a string and returns a string is easy to reason about and debug.  

**Trade-off**: An extra layer of indirection - `maya_api.py` calls `renamer.py` which does the work. Accepted because the separation pays off in testability and futur portability.

## Architecture - `_process_nodes` helper
**Decision**: All node-level operations in `maya_api.py` go through a single `_process_nodes(mode, transform_fn)` helper instead of each function having its own loop.  
**Why**:  
Without `_process_nodes`, every function (`add_prefix`, `add_suffix`, `text_to_lowercase`...) would repeat the same pattern:
```python
nodes = get_nodes(mode)
for node in nodes:
    if not cmds.objExists(node):
        log.error(...)
        continue
    new_name = some_function(node)
    _apply_rename(node, new_name)
```
With `_process_nodes`, each operation becomes a one-liner:
```python
def add_prefix(mode: str, prefix: str) -> dict[str, str]:
    return _process_nodes(mode, lambda node: renamer.add_prefix(node, prefix))
```
**Trade-off**: Operations that need special handling (batch rename with step, fix duplicates) cannot use `_process_nodes` and implement their own loop. This is intentional - `_process_nodes` is for the simple case.

## Architecture - QtSignals between UI and controller
**Decision**: UI widgets communicate with `MainWindow` exclusively via Qt Signals. No widget holds a reference to the controller.  
**Why**:  
- **Decoupling** - a widget can be tested in isolation without a controller or DCC.
- **Clarity** - all connections are defined in one place (`MainWindow.create_gui`), making the data flow easy to trace.
- **Extensibility** - swapping a widget for a new version only requires reconnecting its signals.  
```python
# All connections is one place - easy to audit
self.rename_page. request_rename.connect(self.rename_nodes)
self.prefix_suffix_page.request_prefix.connect(self.add_prefix)
```

## Architecture - JSON presets over Maya `optionVar`
**Decision**: Presets are stored as JSON files in `resources/presets/`, not in Maya `optionVar` system.  
**Why**:  
- **Portability** -  JSON files can be committed to Git and shared across a team. `optionVar` is per-machine and per-Maya installation.
- **Readability** - a JSON file is human-readable and editable outside Maya.
- **Version control** - the default presets ship with the tool in `constants.py` and can be restored at any time.  

**Trade-off**: The JSON files live inside the package - on a shared installation, all users share the same presets file. For multi-user studio deployment, the presets path should be moved to a user-specific location (e.g. `~/maya/scripts/crossrenamertool/presets/`)

## UX - Two buttons for Fix Duplicates
**Decision**: Fix Duplicates has two buttons - `Auto Rename Duplicates` and `Rename Selected` - plus an editable table.  
**Why**:  
A fully automatic fix is fast but dumb - it cannot know the intent behind the name. `arm` duplicated in `GRP_arm_L` and `GRP_arm_R` should become `arm_L` and `arm_R`, not `arm_001` and `arm_002`.  
The editable table lets the artist review and correct every proposed name before applying. `Auto Rename` fills the table with a sensible default; `Rename Selected` applies exactly what the artist has written.

## UX - Tooltips with HTML
**Decision**: All widgets tooltips use HTML formatting (`<b>`, `<i>`, `<code>`, `<p>`).  
**Why**:  
Plain text tooltips are hard to scan. HTML allows separating the description from the example, bolding key terms, and using monospace for node names - making tooltips readable at a glance.
```python
self.step.setToolTip(
    "<p>Increment between each number.</p>"
    "<p><i>Example: Start=<b>1</b>, Step=<b>2</b> -> "
    "<span style='color:#5285a6;'>arm_001, arm_003, arm_005</span></i></p>"
)
```