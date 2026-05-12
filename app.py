"""
Cyber Attack Encyclopedia
==========================
A tkinter desktop app for learning about common cyber attacks.

Run:
    python app.py   (no pip installs needed — all standard library)

Criteria:
    1. App UI       — tkinter with menu bar, notebook tabs, combobox, labels, buttons
    2. Custom funcs — AttackDatabase class, get_attack_info(**kwargs), risk_assessment(),
                      format_risk_bar() — plus a @log_lookup decorator
    3. Does something — user picks an attack → gets definition + risk score + tips
    4. GitHub       — push this file + README.md
"""

import tkinter as tk
from tkinter import ttk, messagebox
from functools import wraps
from datetime import datetime


# ─────────────────────────────────────────────────────────────────────────────
# Criterion 2 ▸ Attack data & class
# ─────────────────────────────────────────────────────────────────────────────

ATTACKS = {
    "Phishing": {
        "category": "Social Engineering",
        "description": (
            "Phishing is a fraudulent attempt to steal sensitive information — "
            "passwords, credit card numbers, or personal data — by disguising a "
            "malicious message as a trustworthy one. Attackers typically send "
            "fake emails or texts that mimic banks, tech companies, or colleagues, "
            "tricking victims into clicking a link and entering credentials on a "
            "spoofed website."
        ),
        "how_it_works": (
            "1. Attacker crafts a convincing email with a malicious link.\n"
            "2. Victim clicks the link and lands on a fake login page.\n"
            "3. Victim enters credentials — attacker captures them.\n"
            "4. Attacker uses stolen credentials for account takeover."
        ),
        "virus_risk": 55,
        "risk_label": "Moderate",
        "risk_color": "#e0a020",
        "tips": [
            "Check the sender's actual email address, not just the display name.",
            "Hover over links before clicking to preview the real URL.",
            "Enable multi-factor authentication (MFA) on all accounts.",
            "Never enter credentials on a page you reached via an email link.",
        ],
    },
    "Malware": {
        "category": "Software Attack",
        "description": (
            "Malware (malicious software) is an umbrella term for any program "
            "intentionally designed to harm a device, steal data, or gain "
            "unauthorized access. It includes viruses, trojans, spyware, ransomware, "
            "and adware. Malware is typically delivered through infected downloads, "
            "email attachments, or compromised websites."
        ),
        "how_it_works": (
            "1. User downloads or opens an infected file.\n"
            "2. Malware executes and installs itself on the system.\n"
            "3. Depending on type: encrypts files, logs keystrokes, or opens backdoor.\n"
            "4. Attacker gains control, steals data, or demands ransom."
        ),
        "virus_risk": 95,
        "risk_label": "Critical",
        "risk_color": "#cc2200",
        "tips": [
            "Keep your OS and applications fully up to date.",
            "Use reputable antivirus / endpoint protection software.",
            "Never open email attachments from unknown senders.",
            "Download software only from official, trusted sources.",
        ],
    },
    "Ransomware": {
        "category": "Software Attack",
        "description": (
            "Ransomware is a type of malware that encrypts the victim's files and "
            "demands payment (usually in cryptocurrency) for the decryption key. "
            "It can spread through phishing emails, unpatched software, or exposed "
            "Remote Desktop Protocol (RDP) ports. Both individuals and large "
            "organizations are common targets."
        ),
        "how_it_works": (
            "1. Ransomware enters via phishing, drive-by download, or RDP exploit.\n"
            "2. It silently maps and encrypts files across the system.\n"
            "3. A ransom note appears demanding payment for the key.\n"
            "4. Paying does not guarantee recovery; backups are the real safeguard."
        ),
        "virus_risk": 98,
        "risk_label": "Critical",
        "risk_color": "#cc2200",
        "tips": [
            "Maintain offline, tested backups (3-2-1 backup rule).",
            "Patch all software promptly — especially OS and browsers.",
            "Disable RDP if not needed; use a VPN if it is.",
            "Segment your network so ransomware cannot spread laterally.",
        ],
    },
    "DDoS": {
        "category": "Network Attack",
        "description": (
            "A Distributed Denial-of-Service (DDoS) attack floods a server, "
            "service, or network with massive amounts of traffic from thousands "
            "of compromised machines (a botnet), making it unavailable to "
            "legitimate users. DDoS attacks target availability rather than "
            "data theft, and are common against gaming servers, banks, and "
            "e-commerce sites."
        ),
        "how_it_works": (
            "1. Attacker builds or rents a botnet of infected machines.\n"
            "2. Botnet simultaneously floods the target with requests.\n"
            "3. Server resources are exhausted — legitimate traffic is dropped.\n"
            "4. Service goes offline until traffic is filtered or attack stops."
        ),
        "virus_risk": 10,
        "risk_label": "Low (for individuals)",
        "risk_color": "#1d9e75",
        "tips": [
            "Individuals are rarely DDoS targets — organizations are.",
            "Use a CDN (e.g. Cloudflare) to absorb volumetric attacks.",
            "Configure rate limiting and firewall rules on servers.",
            "Have an incident response plan and ISP contact ready.",
        ],
    },
    "Man-in-the-Middle (MitM)": {
        "category": "Network Attack",
        "description": (
            "A Man-in-the-Middle attack occurs when an attacker secretly intercepts "
            "and potentially alters communication between two parties who believe "
            "they are communicating directly with each other. Common vectors include "
            "unsecured Wi-Fi networks, ARP spoofing, and DNS spoofing. MitM attacks "
            "allow eavesdropping, credential theft, and session hijacking."
        ),
        "how_it_works": (
            "1. Attacker positions themselves between victim and server.\n"
            "2. All traffic is routed through the attacker (ARP/DNS spoofing).\n"
            "3. Attacker reads, captures, or modifies data in transit.\n"
            "4. Victim and server remain unaware of the interception."
        ),
        "virus_risk": 40,
        "risk_label": "Moderate",
        "risk_color": "#e0a020",
        "tips": [
            "Always use HTTPS — look for the padlock in your browser.",
            "Avoid entering sensitive info on public / open Wi-Fi.",
            "Use a trusted VPN on untrusted networks.",
            "Enable HSTS in browsers and verify SSL certificates.",
        ],
    },
    "SQL Injection": {
        "category": "Application Attack",
        "description": (
            "SQL Injection (SQLi) is an attack where malicious SQL code is inserted "
            "into an input field, tricking the application's database into executing "
            "unintended commands. It can expose entire databases, allow authentication "
            "bypass, and in some configurations enable remote code execution. SQLi is "
            "one of the most prevalent web application vulnerabilities (OWASP Top 10)."
        ),
        "how_it_works": (
            "1. Attacker finds an input field (login, search) not properly sanitized.\n"
            "2. Injects SQL syntax: e.g.  ' OR '1'='1\n"
            "3. Database executes injected code, returning or deleting data.\n"
            "4. Attacker dumps user tables, credentials, or drops the database."
        ),
        "virus_risk": 20,
        "risk_label": "Low–Moderate",
        "risk_color": "#5a9e1d",
        "tips": [
            "Use parameterized queries / prepared statements — never string concat.",
            "Validate and sanitize all user input server-side.",
            "Apply the principle of least privilege to DB accounts.",
            "Use a Web Application Firewall (WAF) as a secondary layer.",
        ],
    },
    "Brute Force": {
        "category": "Credential Attack",
        "description": (
            "A brute force attack systematically tries every possible password "
            "or encryption key until the correct one is found. Dictionary attacks "
            "are a faster variant that tries common words and known passwords first. "
            "Credential stuffing reuses username/password pairs leaked from other "
            "breaches. Automated tools can test millions of combinations per second."
        ),
        "how_it_works": (
            "1. Attacker obtains or guesses a username / email.\n"
            "2. Tool submits thousands of password guesses per second.\n"
            "3. On success, attacker gains account access.\n"
            "4. Accounts without MFA or lockout policies are most vulnerable."
        ),
        "virus_risk": 30,
        "risk_label": "Low–Moderate",
        "risk_color": "#5a9e1d",
        "tips": [
            "Use long, unique passwords (passphrase style) for every account.",
            "Enable MFA — a breached password alone won't be enough.",
            "Use a password manager so you never reuse credentials.",
            "Enable account lockout after N failed attempts.",
        ],
    },
    "Social Engineering": {
        "category": "Social Engineering",
        "description": (
            "Social engineering is the psychological manipulation of people into "
            "performing actions or divulging confidential information. Rather than "
            "hacking systems, attackers hack humans — exploiting trust, urgency, "
            "fear, or authority. Tactics include pretexting (fabricating a scenario), "
            "baiting (offering something enticing), and vishing (voice phishing)."
        ),
        "how_it_works": (
            "1. Attacker researches the target to build a convincing pretext.\n"
            "2. Contact is made (call, email, in-person) with a fabricated scenario.\n"
            "3. Victim is manipulated into revealing info or granting access.\n"
            "4. Attacker uses obtained info for further attacks."
        ),
        "virus_risk": 45,
        "risk_label": "Moderate",
        "risk_color": "#e0a020",
        "tips": [
            "Verify identities through a known, separate channel before acting.",
            "Be skeptical of unsolicited urgency ('act now or your account is closed').",
            "Never share passwords, even with IT — they shouldn't need them.",
            "Security awareness training significantly reduces susceptibility.",
        ],
    },
    "Zero-Day Exploit": {
        "category": "Software Attack",
        "description": (
            "A zero-day exploit targets a software vulnerability that is unknown "
            "to the vendor — meaning there are zero days of protection since no "
            "patch exists yet. These are highly prized by both cybercriminals and "
            "nation-state actors. Once a zero-day is discovered and reported, "
            "the vendor races to issue a patch before it is widely exploited."
        ),
        "how_it_works": (
            "1. Researcher or attacker discovers an unknown flaw in software.\n"
            "2. Exploit code is written to take advantage of the flaw.\n"
            "3. Attack is launched before the vendor knows the bug exists.\n"
            "4. Patch is issued only after discovery — victims have no prior defense."
        ),
        "virus_risk": 85,
        "risk_label": "High",
        "risk_color": "#c05000",
        "tips": [
            "Apply patches and updates the moment they are released.",
            "Use defense-in-depth — no single layer should be your only protection.",
            "Network segmentation limits blast radius of a zero-day compromise.",
            "Endpoint Detection & Response (EDR) tools can catch unusual behavior.",
        ],
    },
    "DNS Spoofing": {
        "category": "Network Attack",
        "description": (
            "DNS Spoofing (also called DNS cache poisoning) tricks a DNS resolver "
            "into caching a fraudulent record, redirecting users to a malicious IP "
            "address instead of the legitimate website. Victims type a real URL but "
            "land on a fake site, often used to steal credentials or serve malware — "
            "without the user knowing anything is wrong."
        ),
        "how_it_works": (
            "1. Attacker injects forged DNS responses into a resolver's cache.\n"
            "2. When victim queries the poisoned domain, resolver returns fake IP.\n"
            "3. Victim's browser connects to attacker's server, not the real site.\n"
            "4. Attacker serves a phishing page or malware download."
        ),
        "virus_risk": 65,
        "risk_label": "High",
        "risk_color": "#c05000",
        "tips": [
            "Use DNSSEC-enabled resolvers (Cloudflare 1.1.1.1, Google 8.8.8.8).",
            "Check that sites use HTTPS — a fake site often can't get a valid cert.",
            "Flush your DNS cache if you suspect redirection issues.",
            "Use a reputable VPN which routes DNS through encrypted tunnels.",
        ],
    },
}


class AttackDatabase:
    """
    Criterion 2 ▸ class that manages all attack data and lookup logic.
    """

    def __init__(self, data: dict):
        self._data = data
        self._history: list[dict] = []   # tracks every lookup this session

    # ── Criterion 2 ▸ **kwargs for flexible querying ──────────────────────

    def get_attack_info(self, name: str, **kwargs) -> dict | None:
        """
        Return attack dict for *name*.

        Optional kwargs:
            fields (list[str]) — return only those keys
            record  (bool)     — if True (default), save to session history
        """
        entry = self._data.get(name)
        if entry is None:
            return None

        if kwargs.get("record", True):
            self._history.append({"name": name, "time": datetime.now().strftime("%H:%M:%S")})

        if "fields" in kwargs:
            return {k: entry[k] for k in kwargs["fields"] if k in entry}

        return dict(entry)

    def all_names(self) -> list[str]:
        return sorted(self._data.keys())

    def by_category(self, category: str) -> list[str]:
        return [k for k, v in self._data.items() if v["category"] == category]

    def session_history(self) -> list[dict]:
        return list(self._history)

    # ── Criterion 2 ▸ custom calculation function ─────────────────────────

    def risk_assessment(self, name: str) -> dict:
        """
        Return a structured risk report for the named attack.
        Computes risk tier and personalised advice string.
        """
        entry = self._data.get(name)
        if not entry:
            return {}
        score = entry["virus_risk"]
        if score >= 90:
            tier, icon = "Critical",    "🔴"
        elif score >= 70:
            tier, icon = "High",        "🟠"
        elif score >= 45:
            tier, icon = "Moderate",    "🟡"
        elif score >= 20:
            tier, icon = "Low–Moderate","🟢"
        else:
            tier, icon = "Low",         "✅"

        advice = (
            "Immediate action required — treat any exposure as a confirmed incident."
            if score >= 90 else
            "Strong precautions needed — this attack frequently results in damage."
            if score >= 70 else
            "Take this seriously — common targets include everyday users."
            if score >= 45 else
            "Lower direct risk — follow best practices and stay alert."
        )
        return {"score": score, "tier": tier, "icon": icon, "advice": advice}


# ── Criterion 2 ▸ custom standalone function ──────────────────────────────────

def format_risk_bar(score: int, width: int = 30) -> str:
    """Return an ASCII progress bar representing the risk score (0–100)."""
    filled = round(score / 100 * width)
    return "█" * filled + "░" * (width - filled) + f"  {score}/100"


# ── Criterion 2 ▸ decorator ───────────────────────────────────────────────────

def log_lookup(f):
    """Decorator: prints each lookup to stdout for debugging / audit trail."""
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        if args:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Lookup → {args[0]}")
        return f(self, *args, **kwargs)
    return wrapper


# ─────────────────────────────────────────────────────────────────────────────
# Criterion 1 ▸ tkinter GUI
# ─────────────────────────────────────────────────────────────────────────────

class CyberApp(tk.Tk):

    # ── colours ───────────────────────────────────────────────────────────
    BG       = "#0d1117"   # dark background
    SURFACE  = "#161b22"   # card / panel
    BORDER   = "#30363d"   # borders
    TEXT     = "#e6edf3"   # primary text
    MUTED    = "#8b949e"   # secondary text
    GREEN    = "#1d9e75"
    RED      = "#cc2200"
    ORANGE   = "#c05000"
    YELLOW   = "#e0a020"
    ACCENT   = "#58a6ff"   # blue accent

    def __init__(self):
        super().__init__()
        self.db = AttackDatabase(ATTACKS)

        self.title("🛡 Cyber Attack Encyclopedia")
        self.geometry("900x680")
        self.minsize(750, 560)
        self.configure(bg=self.BG)

        self._style_ttk()
        self._build_menu()
        self._build_ui()

    # ── ttk styling ───────────────────────────────────────────────────────

    def _style_ttk(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("TNotebook",
                        background=self.BG, borderwidth=0)
        style.configure("TNotebook.Tab",
                        background=self.SURFACE, foreground=self.MUTED,
                        padding=[14, 6], font=("Helvetica", 10, "bold"))
        style.map("TNotebook.Tab",
                  background=[("selected", self.BG)],
                  foreground=[("selected", self.ACCENT)])

        style.configure("TCombobox",
                        fieldbackground=self.SURFACE,
                        background=self.SURFACE,
                        foreground=self.TEXT,
                        selectbackground=self.SURFACE,
                        selectforeground=self.ACCENT,
                        arrowcolor=self.ACCENT)
        style.map("TCombobox", fieldbackground=[("readonly", self.SURFACE)])

        style.configure("Treeview",
                        background=self.SURFACE,
                        foreground=self.TEXT,
                        fieldbackground=self.SURFACE,
                        rowheight=24,
                        borderwidth=0)
        style.configure("Treeview.Heading",
                        background=self.BG,
                        foreground=self.MUTED,
                        font=("Helvetica", 9, "bold"))
        style.map("Treeview",
                  background=[("selected", "#1f3050")],
                  foreground=[("selected", self.ACCENT)])

        style.configure("Vertical.TScrollbar",
                        background=self.BORDER,
                        troughcolor=self.SURFACE,
                        bordercolor=self.BG,
                        arrowcolor=self.MUTED)

    # ── menu bar ──────────────────────────────────────────────────────────

    def _build_menu(self):
        menubar  = tk.Menu(self, bg=self.SURFACE, fg=self.TEXT,
                           activebackground=self.BORDER,
                           activeforeground=self.ACCENT, bd=0)

        file_m = tk.Menu(menubar, tearoff=0, bg=self.SURFACE, fg=self.TEXT,
                         activebackground=self.BORDER,
                         activeforeground=self.ACCENT)
        file_m.add_command(label="Clear results",    command=self._clear_results)
        file_m.add_command(label="View session log", command=self._show_session_log)
        file_m.add_separator()
        file_m.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_m)

        filter_m = tk.Menu(menubar, tearoff=0, bg=self.SURFACE, fg=self.TEXT,
                           activebackground=self.BORDER,
                           activeforeground=self.ACCENT)
        cats = sorted({v["category"] for v in ATTACKS.values()})
        for cat in cats:
            filter_m.add_command(
                label=cat,
                command=lambda c=cat: self._filter_by_category(c)
            )
        filter_m.add_separator()
        filter_m.add_command(label="Show all", command=self._reset_filter)
        menubar.add_cascade(label="Filter by category", menu=filter_m)

        help_m = tk.Menu(menubar, tearoff=0, bg=self.SURFACE, fg=self.TEXT,
                         activebackground=self.BORDER,
                         activeforeground=self.ACCENT)
        help_m.add_command(label="About", command=lambda: messagebox.showinfo(
            "About",
            "Cyber Attack Encyclopedia\n\n"
            "Learn about common cyber attacks,\n"
            "how they work, and how to stay safe.\n\n"
            "Built with Python + tkinter + SQLite"))
        menubar.add_cascade(label="Help", menu=help_m)

        self.config(menu=menubar)

    # ── main UI ───────────────────────────────────────────────────────────

    def _build_ui(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self._build_lookup_tab(notebook)
        self._build_browse_tab(notebook)

    # ── TAB 1: Lookup ─────────────────────────────────────────────────────

    def _build_lookup_tab(self, nb):
        frame = tk.Frame(nb, bg=self.BG)
        nb.add(frame, text="  🔍 Attack Lookup  ")

        # ── selector row
        top = tk.Frame(frame, bg=self.BG)
        top.pack(fill="x", padx=16, pady=(14, 6))

        tk.Label(top, text="Select an attack type:",
                 bg=self.BG, fg=self.MUTED,
                 font=("Helvetica", 10, "bold")).pack(side="left")

        self.combo = ttk.Combobox(top, state="readonly", width=30,
                                  values=self.db.all_names(),
                                  font=("Helvetica", 11))
        self.combo.pack(side="left", padx=10)
        self.combo.bind("<<ComboboxSelected>>", lambda _: self._lookup())

        btn = tk.Button(top, text="Look up →",
                        bg=self.ACCENT, fg="#000000",
                        activebackground="#79bfff", activeforeground="#000000",
                        font=("Helvetica", 10, "bold"),
                        relief="flat", cursor="hand2", padx=12, pady=4,
                        command=self._lookup)
        btn.pack(side="left")

        # ── scrollable results area
        canvas = tk.Canvas(frame, bg=self.BG, highlightthickness=0)
        vsb    = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y", pady=4)
        canvas.pack(side="left", fill="both", expand=True, padx=(12, 0), pady=4)

        self.results_frame = tk.Frame(canvas, bg=self.BG)
        self.canvas_window = canvas.create_window(
            (0, 0), window=self.results_frame, anchor="nw")

        def _on_resize(e):
            canvas.itemconfig(self.canvas_window, width=e.width)
        def _on_frame_configure(_):
            canvas.configure(scrollregion=canvas.bbox("all"))

        canvas.bind("<Configure>", _on_resize)
        self.results_frame.bind("<Configure>", _on_frame_configure)
        canvas.bind_all("<MouseWheel>",
                        lambda e: canvas.yview_scroll(-1 * (e.delta // 120), "units"))

        self._show_placeholder()

    def _show_placeholder(self):
        for w in self.results_frame.winfo_children():
            w.destroy()
        tk.Label(self.results_frame,
                 text="☝  Choose an attack from the dropdown above",
                 bg=self.BG, fg=self.MUTED,
                 font=("Helvetica", 13)).pack(pady=60)

    # ── Criterion 3 ▸ app reacts to user input ────────────────────────────

    @log_lookup
    def _lookup(self, name: str = None):
        name = name or self.combo.get()
        if not name:
            messagebox.showwarning("Nothing selected", "Please choose an attack first.")
            return

        info   = self.db.get_attack_info(name)
        risk   = self.db.risk_assessment(name)
        bar    = format_risk_bar(risk["score"])

        # ── clear and repopulate results frame
        for w in self.results_frame.winfo_children():
            w.destroy()

        pad = {"padx": 18, "pady": 4}

        # name + category badge
        header = tk.Frame(self.results_frame, bg=self.BG)
        header.pack(fill="x", **pad)

        tk.Label(header, text=name,
                 bg=self.BG, fg=self.TEXT,
                 font=("Helvetica", 20, "bold")).pack(side="left")
        tk.Label(header, text=f"  [{info['category']}]",
                 bg=self.BG, fg=self.ACCENT,
                 font=("Helvetica", 11)).pack(side="left", pady=6)

        self._divider()

        # description card
        self._section_label("📖  What is it?")
        self._card(info["description"])

        # how it works
        self._section_label("⚙️  How it works")
        self._card(info["how_it_works"])

        # risk meter
        self._section_label("⚠️  Virus / malware risk to you")
        risk_card = tk.Frame(self.results_frame, bg=self.SURFACE,
                             highlightbackground=info["risk_color"],
                             highlightthickness=2)
        risk_card.pack(fill="x", padx=18, pady=6)

        tk.Label(risk_card,
                 text=f"  {risk['icon']}  {risk['risk_label'].upper()}",
                 bg=self.SURFACE, fg=info["risk_color"],
                 font=("Courier", 14, "bold"), anchor="w").pack(
            fill="x", padx=12, pady=(10, 2))

        tk.Label(risk_card,
                 text=f"  {bar}",
                 bg=self.SURFACE, fg=info["risk_color"],
                 font=("Courier", 12), anchor="w").pack(
            fill="x", padx=12, pady=(0, 4))

        tk.Label(risk_card,
                 text=f"  {risk['advice']}",
                 bg=self.SURFACE, fg=self.MUTED,
                 font=("Helvetica", 10), wraplength=700, justify="left",
                 anchor="w").pack(fill="x", padx=12, pady=(2, 10))

        # protection tips
        self._section_label("🛡️  How to protect yourself")
        tips_card = tk.Frame(self.results_frame, bg=self.SURFACE,
                             highlightbackground=self.BORDER,
                             highlightthickness=1)
        tips_card.pack(fill="x", padx=18, pady=6)

        for tip in info["tips"]:
            row = tk.Frame(tips_card, bg=self.SURFACE)
            row.pack(fill="x", padx=12, pady=3)
            tk.Label(row, text="✔", bg=self.SURFACE, fg=self.GREEN,
                     font=("Helvetica", 11, "bold"), width=2).pack(side="left")
            tk.Label(row, text=tip, bg=self.SURFACE, fg=self.TEXT,
                     font=("Helvetica", 10), wraplength=680, justify="left").pack(
                side="left", pady=2)

        tk.Frame(self.results_frame, bg=self.BG, height=20).pack()  # bottom padding

    def _divider(self):
        tk.Frame(self.results_frame, bg=self.BORDER, height=1).pack(
            fill="x", padx=18, pady=6)

    def _section_label(self, text):
        tk.Label(self.results_frame, text=text,
                 bg=self.BG, fg=self.MUTED,
                 font=("Helvetica", 10, "bold")).pack(
            anchor="w", padx=18, pady=(8, 0))

    def _card(self, text):
        f = tk.Frame(self.results_frame, bg=self.SURFACE,
                     highlightbackground=self.BORDER, highlightthickness=1)
        f.pack(fill="x", padx=18, pady=4)
        tk.Label(f, text=text, bg=self.SURFACE, fg=self.TEXT,
                 font=("Helvetica", 10), wraplength=720,
                 justify="left", anchor="nw").pack(
            padx=14, pady=10, fill="x")

    # ── TAB 2: Browse all ─────────────────────────────────────────────────

    def _build_browse_tab(self, nb):
        frame = tk.Frame(nb, bg=self.BG)
        nb.add(frame, text="  📋 Browse All  ")

        tk.Label(frame,
                 text="Click any row to view details in the Lookup tab",
                 bg=self.BG, fg=self.MUTED,
                 font=("Helvetica", 9)).pack(anchor="w", padx=12, pady=(10, 4))

        cols = ("Attack", "Category", "Risk Level", "Score")
        tree = ttk.Treeview(frame, columns=cols, show="headings", selectmode="browse")

        for col, w in zip(cols, [220, 160, 130, 80]):
            tree.heading(col, text=col)
            tree.column(col, width=w, anchor="w" if col != "Score" else "center")

        tree.tag_configure("Critical", foreground="#cc2200")
        tree.tag_configure("High",     foreground="#c05000")
        tree.tag_configure("Moderate", foreground="#e0a020")
        tree.tag_configure("Low",      foreground="#1d9e75")

        for name in self.db.all_names():
            info = self.db.get_attack_info(name, record=False)
            risk = self.db.risk_assessment(name)
            tag  = (risk["tier"].split("–")[0],)   # "Low–Moderate" → "Low"
            tree.insert("", "end",
                        values=(name, info["category"],
                                risk["icon"] + " " + risk["tier"],
                                risk["score"]),
                        iid=name, tags=tag)

        sb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y", pady=4, padx=(0, 10))
        tree.pack(fill="both", expand=True, padx=(10, 0), pady=(0, 10))

        def on_select(e):
            sel = tree.selection()
            if sel:
                name = sel[0]
                self.combo.set(name)
                self._lookup(name)
                # switch to lookup tab
                self.nametowidget(self.winfo_children()[0]).select(0)

        tree.bind("<<TreeviewSelect>>", on_select)

    # ── helpers for menu actions ──────────────────────────────────────────

    def _clear_results(self):
        self.combo.set("")
        self._show_placeholder()

    def _show_session_log(self):
        history = self.db.session_history()
        if not history:
            messagebox.showinfo("Session log", "No lookups yet this session.")
            return
        lines = [f"{h['time']}  →  {h['name']}" for h in history]
        messagebox.showinfo("Session log", "\n".join(lines))

    def _filter_by_category(self, category: str):
        names = self.db.by_category(category)
        self.combo["values"] = names
        self.combo.set("")
        self._show_placeholder()
        messagebox.showinfo("Filter applied",
                            f"Showing {len(names)} attacks in: {category}\n\n"
                            + "\n".join(f"• {n}" for n in names))

    def _reset_filter(self):
        self.combo["values"] = self.db.all_names()
        self.combo.set("")
        self._show_placeholder()


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = CyberApp()
    app.mainloop()
