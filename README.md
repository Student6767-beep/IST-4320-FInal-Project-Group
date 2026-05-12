# 🛡 Cyber Attack Encyclopedia
Group Project Members-Skylar Fenn and Coraima Ruiz
A desktop reference app built with **Python + tkinter** for learning about common cyber attacks — what they are, how they work, how likely they are to give you a virus, and how to protect yourself.

**No pip installs required** — only the Python standard library is used.

---

## How to run

```bash
python app.py
```

Python 3.10 or later recommended (uses `dict | None` type hint syntax).  
For Python 3.9 and earlier, change `dict | None` to `Optional[dict]` on line ~95.

---

## Attacks covered

| Attack | Category | Risk |
|---|---|---|
| Phishing | Social Engineering | 🟡 Moderate |
| Malware | Software Attack | 🔴 Critical |
| Ransomware | Software Attack | 🔴 Critical |
| DDoS | Network Attack | ✅ Low |
| Man-in-the-Middle | Network Attack | 🟡 Moderate |
| SQL Injection | Application Attack | 🟢 Low–Moderate |
| Brute Force | Credential Attack | 🟢 Low–Moderate |
| Social Engineering | Social Engineering | 🟡 Moderate |
| Zero-Day Exploit | Software Attack | 🟠 High |
| DNS Spoofing | Network Attack | 🟠 High |

---

## Features

- **Lookup tab** — choose any attack from the dropdown, get a full breakdown
- **Browse all tab** — colour-coded table of all attacks; click any row to look it up
- **Menu bar** — filter by category (Network / Social Engineering / etc.), view session log, clear results
- **Risk meter** — ASCII bar graph showing virus/malware risk score 0–100
- **Protection tips** — actionable steps specific to each attack type

---

## Assignment criteria

| # | Criterion | How it's met |
|---|---|---|
| 1 | **App UI** | tkinter with `ttk.Notebook` tabs, `ttk.Combobox`, `ttk.Treeview`, `tk.Menu` menu bar, scrollable canvas panel |
| 2 | **Custom functions** | `AttackDatabase` class; `get_attack_info(**kwargs)` uses `**kwargs`; `risk_assessment()` calculates risk tier; `format_risk_bar()` is a standalone custom function; `@log_lookup` is a decorator |
| 3 | **Does something with input** | User picks attack → `get_attack_info()` + `risk_assessment()` called → full definition, risk score, bar graph, and tips rendered live |
| 4 | **GitHub** | ✅ this repo |
