import platform
import re
import statistics
import subprocess
import threading
import tkinter as tk
from tkinter import ttk

def ping(host, count=3):
    if not host:
        return None
    cmd = ["ping", "-n", str(count), "-w", "1000", host] if platform.system() == "Windows" else ["ping", "-c", str(count), "-W", "2", host]
    try:
        txt = subprocess.run(cmd, capture_output=True, text=True, timeout=count * 3 + 3).stdout
        vals = [float(x) for x in re.findall(r"time[=<](\d+(?:\.\d+)?) ?ms", txt, re.I)]
        return round(statistics.mean(vals), 1) if vals else None
    except Exception:
        return None

def gateway():
    try:
        if platform.system() == "Windows":
            txt = subprocess.run(["route", "print", "-4"], capture_output=True, text=True, timeout=6).stdout
            for line in txt.splitlines():
                parts = line.split()
                if len(parts) >= 3 and parts[0] == "0.0.0.0" and parts[1] == "0.0.0.0":
                    return parts[2]
        else:
            txt = subprocess.run(["ip", "route", "show", "default"], capture_output=True, text=True, timeout=4).stdout
            m = re.search(r"default via (\d+\.\d+\.\d+\.\d+)", txt)
            if m:
                return m.group(1)
    except Exception:
        return None
    return None

def run(cmd):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=12)
        return p.returncode == 0, (p.stdout or p.stderr).strip()
    except Exception as exc:
        return False, str(exc)

def help_home():
    notes = []
    if platform.system() != "Windows":
        return ["This installer helps on Windows. Other systems can only show the check."]
    ok, txt = run(["netsh", "int", "tcp", "show", "global"])
    if ok and "disabled" in txt.lower():
        good, _ = run(["netsh", "int", "tcp", "set", "global", "autotuninglevel=normal"])
        notes.append("Turned Windows download window back on." if good else "Could not change the Windows download window. Run the installer as administrator.")
    else:
        notes.append("Windows download window is already on.")
    good, _ = run(["ipconfig", "/flushdns"])
    notes.append("Cleared the old address book." if good else "Could not clear the address book.")
    good, jobs = run(["bitsadmin", "/list", "/allusers"])
    if good and "{" in jobs:
        notes.append("A Windows background transfer is present. Pause Windows Update if a big download is running.")
    else:
        notes.append("No Windows background transfer is filling the line.")
    return notes

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("NETBOOST")
        self.geometry("860x620")
        self.configure(bg="#070b14")
        self.plan = tk.StringVar(value="100")
        tk.Label(self, text="NETBOOST", font=("Segoe UI Semibold", 26), fg="#3ce7ff", bg="#070b14").pack(anchor="w", padx=28, pady=(22, 0))
        tk.Label(self, text="Installed on this PC. It checks both sides, then fixes only the house.", font=("Segoe UI", 11), fg="#93a4bc", bg="#070b14").pack(anchor="w", padx=28)
        card = tk.Frame(self, bg="#101826", highlightthickness=1, highlightbackground="#24344c")
        card.pack(fill="both", expand=True, padx=28, pady=16)
        self.title_lbl = tk.Label(card, text="Ready", font=("Segoe UI Semibold", 24), fg="white", bg="#101826")
        self.title_lbl.pack(anchor="w", padx=22, pady=(22, 6))
        self.body = tk.Label(card, text="One button. House fixes are applied. A busy provider is reported, not invented.", font=("Segoe UI", 12), fg="#c5d2e4", bg="#101826", wraplength=760, justify="left")
        self.body.pack(anchor="w", padx=22, pady=6)
        row = tk.Frame(card, bg="#101826")
        row.pack(anchor="w", padx=22, pady=10)
        tk.Label(row, text="Plan Mbps", fg="#93a4bc", bg="#101826").pack(side="left")
        ttk.Entry(row, textvariable=self.plan, width=8).pack(side="left", padx=8)
        self.check_btn = ttk.Button(card, text="Check and help", command=self.start)
        self.check_btn.pack(anchor="w", padx=22, pady=8)
        self.log = tk.Label(card, text="", font=("Consolas", 11), fg="#d5e6f7", bg="#101826", justify="left")
        self.log.pack(anchor="w", padx=22, pady=12)
    def start(self):
        self.check_btn.config(state="disabled")
        self.title_lbl.config(text="Checking this PC...")
        threading.Thread(target=self.work, daemon=True).start()
    def work(self):
        g = gateway()
        gms = ping(g)
        wms = ping("1.1.1.1")
        try:
            plan = float(self.plan.get())
        except ValueError:
            plan = None
        home_ok = gms is not None and gms < 25
        provider_busy = home_ok and (wms is None or wms > 80)
        notes = help_home()
        if provider_busy:
            title = "House helped. Provider is still busy."
            body = "Your router answered quickly. The slow part starts after it. Nothing installed on this PC can add speed on the provider network."
        elif not home_ok:
            title = "The slowdown is in the house."
            body = "The router itself is slow or not answering. Move closer, try 5 GHz, or use a cable."
        else:
            title = "No clear slowdown in this sample."
            body = "Run it again when the line feels slow."
        lines = [f"Router {gms if gms is not None else '-'} ms", f"Past the router {wms if wms is not None else '-'} ms"]
        if plan:
            lines.append(f"Plan {plan:.0f} Mbps")
        lines.extend(notes)
        self.after(0, lambda: self.show(title, body, "\n".join(lines)))
    def show(self, title, body, lines):
        self.title_lbl.config(text=title)
        self.body.config(text=body)
        self.log.config(text=lines)
        self.check_btn.config(state="normal")

if __name__ == "__main__":
    App().mainloop()
