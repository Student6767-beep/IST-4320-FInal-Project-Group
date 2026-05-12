# Project Feedback
Group Members- Skylar Fenn and Coraima Ruiz
## Purpose of the app

A Cyber Attack Encyclopedia — a desktop reference tool where you can look up common cyber
attacks (phishing, ransomware, DDoS, man-in-the-middle, etc.), read what they are, see how
they work step by step, get a virus/malware risk score specific to that attack, and get
actionable protection tips. The goal was to make something genuinely informative and
visually clear, not just a toy demo.

---

## What I attempted

- A dark-themed tkinter app with two tabs: a "Lookup" tab where you pick an attack and get
  the full breakdown, and a "Browse All" tab with a colour-coded table of every attack.
- A menu bar with a "Filter by category" submenu that dynamically builds items from the
  data (Network Attack, Social Engineering, etc.) — so adding a new attack category
  automatically shows up in the menu with no extra code.
- An `AttackDatabase` class to hold all the attack data and expose clean methods:
  `get_attack_info(**kwargs)` for flexible lookups, `risk_assessment()` for the risk
  calculation, `by_category()` for filtering, and `session_history()` to track what the
  user has looked up this session.
- A `format_risk_bar()` standalone function that generates an ASCII progress bar from a
  0–100 score, so the risk level is visual and immediately readable.
- A `@log_lookup` decorator that prints each lookup to the terminal (useful for debugging
  and audit trail without cluttering the UI).
- A scrollable results panel built on `tk.Canvas` so long results don't get cut off.

---

## What worked

- Everything runs and all 10 attacks display correctly with their descriptions, step-by-step
  explanations, risk scores, and tips.
- The `**kwargs` pattern in `get_attack_info()` is used in two real ways: the Browse tab
  passes `record=False` so browsing doesn't pollute the session history, and the `fields`
  kwarg lets you request only specific keys — both practical uses, not just for show.
- The `risk_assessment()` function centralises all the tier logic in one place, so the
  lookup tab and browse table both get consistent risk labels.
- Clicking a row in the Browse tab switches to the Lookup tab and runs the lookup
  automatically — the two tabs communicate cleanly.
- The dark theme with `ttk.Style` came out well; colour-coding risk levels (green → red)
  makes the table scannable at a glance.

---

## What didn't work / challenges

- `ttk.Combobox` dropdown list background ignores `fieldbackground` on some OS/themes
  (the list items show in OS default white even though the selected-state is styled).
  This is a known tkinter limitation with no clean fix short of a custom dropdown widget.
- `canvas.bind_all("<MouseWheel>")` for scrolling works on Windows/macOS but on Linux the
  event is `<Button-4>` / `<Button-5>` — would need an OS check for full cross-platform
  scrolling.
- The `dict | None` union type hint syntax requires Python 3.10+. For 3.9 compatibility
  you'd use `Optional[dict]` from `typing`.

---

## What I'd still like to do

- **Search bar**: live-filter the attack list as you type, rather than just a dropdown.
- **Quiz mode**: flash an attack name, ask the user to guess the risk level or category —
  good for studying.
- **Real SQLite backend**: persist the attack data in a database so new attacks can be
  added without editing the Python file, using a simple admin form.
- **Export**: "Save to PDF" or "Copy to clipboard" button on any attack's result page.
- **Severity chart**: a small bar chart (matplotlib embedded in tkinter) comparing all
  attack risk scores visually.

---

## What I learned

- How `tk.Canvas` + `create_window` builds a scrollable area for arbitrary tkinter widgets
  — this is the standard pattern since tkinter has no built-in scrollable frame.
- How `ttk.Style` theming works: you set named element properties and map state-specific
  overrides (e.g. selected vs. normal combobox colour), but some widgets have OS-level
  paint that ignores these.
- How `**kwargs` enables genuinely flexible APIs — the same `get_attack_info()` method
  handles full lookups, history-silent browses, and field-subset requests cleanly.
- How decorators work in practice: `@log_lookup` is just a function that intercepts the
  call, does something extra (prints to console), then calls the original function. Once
  you understand that, you can use them anywhere for logging, timing, auth checks, etc.
- How to build a `tk.Menu` with submenus dynamically generated from data — the category
  submenu populates itself from whatever categories exist in the attack dictionary.
