"""Tkinter GUI for TikTok Account Creator Pro"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import json
from pathlib import Path

from src.core import AccountManager, ColoredLogger
from src.core.config import EngineConfig


class TikTokGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("TikTok Account Creator Pro v3.0")
        self.root.geometry("900x700")
        self.root.configure(bg="#1a1a2e")
        
        self.manager = None
        self.logger = ColoredLogger("gui")
        
        self._build_ui()
    
    def _build_ui(self):
        # Header
        header = tk.Label(
            self.root,
            text="🎵 TikTok Account Creator Pro",
            font=("Helvetica", 20, "bold"),
            bg="#1a1a2e",
            fg="#e94560"
        )
        header.pack(pady=10)
        
        # Controls Frame
        controls = tk.Frame(self.root, bg="#16213e", padx=20, pady=20)
        controls.pack(fill="x", padx=20)
        
        # Region
        tk.Label(controls, text="Region:", bg="#16213e", fg="white").grid(row=0, column=0, sticky="w")
        self.region_var = tk.StringVar(value="US")
        ttk.Combobox(controls, textvariable=self.region_var, values=["US", "GB", "DE", "FR", "JP"]).grid(row=0, column=1, padx=5)
        
        # Count
        tk.Label(controls, text="Accounts:", bg="#16213e", fg="white").grid(row=0, column=2, sticky="w", padx=(20,0))
        self.count_var = tk.IntVar(value=5)
        tk.Spinbox(controls, from_=1, to=100, textvariable=self.count_var, width=8).grid(row=0, column=3, padx=5)
        
        # Threads
        tk.Label(controls, text="Threads:", bg="#16213e", fg="white").grid(row=0, column=4, sticky="w", padx=(20,0))
        self.threads_var = tk.IntVar(value=3)
        tk.Spinbox(controls, from_=1, to=20, textvariable=self.threads_var, width=8).grid(row=0, column=5, padx=5)
        
        # Buttons
        btn_frame = tk.Frame(self.root, bg="#1a1a2e")
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="▶ START", bg="#0f3460", fg="white", 
                 font=("Helvetica", 12, "bold"), command=self.start).pack(side="left", padx=5)
        tk.Button(btn_frame, text="⏸ PAUSE", bg="#533483", fg="white",
                 font=("Helvetica", 12), command=self.pause).pack(side="left", padx=5)
        tk.Button(btn_frame, text="⏹ STOP", bg="#e94560", fg="white",
                 font=("Helvetica", 12), command=self.stop).pack(side="left", padx=5)
        
        # Log Area
        tk.Label(self.root, text="Activity Log:", bg="#1a1a2e", fg="white", 
                font=("Helvetica", 12)).pack(anchor="w", padx=20, pady=(10,0))
        
        self.log_area = scrolledtext.ScrolledText(
            self.root, height=20, bg="#0f3460", fg="#00ff88",
            font=("Consolas", 10), insertbackground="white"
        )
        self.log_area.pack(fill="both", expand=True, padx=20, pady=5)
        
        # Status Bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = tk.Label(self.root, textvariable=self.status_var, 
                             bg="#16213e", fg="#00ff88", anchor="w")
        status_bar.pack(fill="x", side="bottom")
    
    def log(self, message: str):
        self.log_area.insert("end", f"{message}\n")
        self.log_area.see("end")
    
    def start(self):
        self.log("[*] Initializing engine...")
        try:
            self.manager = AccountManager()
            self.status_var.set("Running...")
            
            thread = threading.Thread(
                target=self._run_batch,
                daemon=True
            )
            thread.start()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def _run_batch(self):
        try:
            results = self.manager.run_batch(
                count=self.count_var.get(),
                region=self.region_var.get()
            )
            self.log(f"[+] Complete: {len([r for r in results if r.status == 'success'])} accounts")
            self.status_var.set("Complete")
        except Exception as e:
            self.log(f"[-] Error: {e}")
            self.status_var.set("Error")
    
    def pause(self):
        if self.manager:
            self.manager.pause()
            self.status_var.set("Paused")
            self.log("[!] Paused")
    
    def stop(self):
        if self.manager:
            self.manager.stop()
            self.status_var.set("Stopped")
            self.log("[!] Stopped")
    
    def run(self):
        self.root.mainloop()


def launch_gui():
    app = TikTokGUI()
    app.run()

