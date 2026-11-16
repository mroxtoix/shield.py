import os
import sys
import zlib
import hmac
import base64
import random
import string
import ctypes
import hashlib
import webbrowser
import threading
from tkinter import filedialog
import customtkinter as ctk
from tkinterdnd2 import TkinterDnD, DND_FILES

try:
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("ix.ixshield.protector.1.0")
except Exception:
    pass


def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


ICON_NAME = "icons8-star-100.ico"

ctk.set_appearance_mode("Dark")

BG_MAIN = "#0B0B0E"
BG_CARD = "#141419"
BG_INPUT = "#1C1C24"
RED_PRIMARY = "#E50914"
RED_HOVER = "#B80710"
RED_GLOW = "#FF2A35"
TEXT_WHITE = "#F5F5F7"
TEXT_MUTED = "#8E8E9A"


class TkDnDCTk(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)


class AboutWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("About - ixShield")
        self.geometry("380x290")
        self.resizable(False, False)
        self.configure(fg_color=BG_MAIN)
        self.transient(parent)
        self.grab_set()

        icon_file = resource_path(ICON_NAME)
        if os.path.exists(icon_file):
            self.after(200, lambda: self.iconbitmap(icon_file))

        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (380 // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (290 // 2)
        self.geometry(f"+{x}+{y}")

        card = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=14, border_width=1, border_color="#2A1519")
        card.pack(fill="both", expand=True, padx=16, pady=16)

        ctk.CTkLabel(
            card, text="ixShield Protector",
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
            text_color=RED_PRIMARY
        ).pack(pady=(18, 2))

        ctk.CTkLabel(
            card, text="Advanced Python Source Code Obfuscator",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=TEXT_MUTED
        ).pack(pady=(0, 14))

        info_frame = ctk.CTkFrame(card, fg_color=BG_INPUT, corner_radius=10)
        info_frame.pack(fill="x", padx=20, pady=4)

        ctk.CTkLabel(
            info_frame, text="Developer: ix   |   Team: wakeup",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=TEXT_WHITE
        ).pack(pady=10)

        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(pady=(16, 10))

        yt_btn = ctk.CTkButton(
            btn_frame, text="YouTube", width=130, height=34,
            fg_color=RED_PRIMARY, hover_color=RED_HOVER,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            corner_radius=8,
            command=lambda: webbrowser.open("https://youtube.com/@ixlol.1?si=BUEemo2y5XZXRixq")
        )
        yt_btn.grid(row=0, column=0, padx=6)

        dc_btn = ctk.CTkButton(
            btn_frame, text="Discord Server", width=130, height=34,
            fg_color=RED_PRIMARY, hover_color=RED_HOVER,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            corner_radius=8,
            command=lambda: webbrowser.open("https://discord.gg/WKB")
        )
        dc_btn.grid(row=0, column=1, padx=6)


class ixShieldApp(TkDnDCTk):
    def __init__(self):
        super().__init__()

        self.title("ixShield - Python Protector")
        self.geometry("560x340")
        self.resizable(False, False)
        self.configure(fg_color=BG_MAIN)

        icon_file = resource_path(ICON_NAME)
        if os.path.exists(icon_file):
            self.iconbitmap(icon_file)

        self.selected_file = ""
        self.mode_var = ctk.StringVar(value="sha256")
        self._reset_job = None

        self._build_ui()
        self._setup_drag_and_drop()

    def _build_ui(self):
        self.main_card = ctk.CTkFrame(
            self, fg_color=BG_CARD, corner_radius=16,
            border_width=1, border_color="#291418"
        )
        self.main_card.pack(fill="both", expand=True, padx=18, pady=18)

        header_frame = ctk.CTkFrame(self.main_card, fg_color="transparent")
        header_frame.pack(fill="x", padx=22, pady=(18, 12))

        title_box = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_box.pack(side="left")

        ctk.CTkLabel(
            title_box, text="ixShield",
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
            text_color=RED_PRIMARY
        ).pack(side="left")

        ctk.CTkLabel(
            title_box, text="  |  Python Source Protector",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=TEXT_WHITE
        ).pack(side="left", pady=(3, 0))

        dev_badge = ctk.CTkLabel(
            header_frame, text=" dev: ix ",
            fg_color="#261014", text_color=RED_GLOW,
            corner_radius=6, font=ctk.CTkFont(family="Consolas", size=12, weight="bold")
        )
        dev_badge.pack(side="right", pady=4)

        file_frame = ctk.CTkFrame(self.main_card, fg_color="transparent")
        file_frame.pack(fill="x", padx=22, pady=(6, 14))

        self.file_entry = ctk.CTkEntry(
            file_frame, placeholder_text="Drag & Drop .py file here or Select...",
            height=38, fg_color=BG_INPUT, border_color="#2E2E3A",
            text_color=TEXT_WHITE, placeholder_text_color=TEXT_MUTED,
            corner_radius=8, font=ctk.CTkFont(family="Consolas", size=12)
        )
        self.file_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.file_entry.configure(state="readonly")

        select_btn = ctk.CTkButton(
            file_frame, text="Select File", width=115, height=38,
            fg_color=RED_PRIMARY, hover_color=RED_HOVER,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            corner_radius=8, command=self.select_file
        )
        select_btn.pack(side="right")

        modes_frame = ctk.CTkFrame(self.main_card, fg_color=BG_INPUT, corner_radius=10)
        modes_frame.pack(fill="x", padx=22, pady=(0, 16))

        rb_b64 = ctk.CTkRadioButton(
            modes_frame, text="Base64",
            variable=self.mode_var, value="base64",
            fg_color=RED_PRIMARY, hover_color=RED_GLOW,
            border_color="#4A4A5A", text_color=TEXT_WHITE,
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold")
        )
        rb_b64.pack(side="left", padx=(24, 55), pady=12)

        rb_strong = ctk.CTkRadioButton(
            modes_frame, text="SHA256-Stream",
            variable=self.mode_var, value="sha256",
            fg_color=RED_PRIMARY, hover_color=RED_GLOW,
            border_color="#4A4A5A", text_color=TEXT_WHITE,
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold")
        )
        rb_strong.pack(side="left", pady=12)

        self.protect_btn = ctk.CTkButton(
            self.main_card, text="PROTECT SOURCE CODE", height=42,
            fg_color=RED_PRIMARY, hover_color=RED_HOVER,
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            corner_radius=9, command=self.start_protection
        )
        self.protect_btn.pack(fill="x", padx=22, pady=(0, 12))

        self.progress = ctk.CTkProgressBar(
            self.main_card, height=4, fg_color=BG_INPUT, progress_color=RED_PRIMARY
        )
        self.progress.pack(fill="x", padx=22, pady=(0, 12))
        self.progress.set(0)

        footer_frame = ctk.CTkFrame(self.main_card, fg_color="transparent")
        footer_frame.pack(fill="x", padx=22, pady=(0, 10))

        self.status_label = ctk.CTkLabel(
            footer_frame, text="Status: Ready (Drag & Drop enabled)",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=TEXT_MUTED
        )
        self.status_label.pack(side="left")

        about_btn = ctk.CTkButton(
            footer_frame, text="About", width=75, height=28,
            fg_color="transparent", hover_color="#241216",
            border_width=1, border_color="#3D1C22",
            text_color=TEXT_WHITE, corner_radius=6,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            command=self.open_about
        )
        about_btn.pack(side="right")

    def _setup_drag_and_drop(self):
        for widget in (self, self.main_card, self.file_entry):
            widget.drop_target_register(DND_FILES)
            widget.dnd_bind("<<Drop>>", self._on_file_drop)

    def _on_file_drop(self, event):
        files = self.tk.splitlist(event.data)
        if not files:
            return
        path = files[0].strip("{}").strip('"')

        if not path.lower().endswith(".py"):
            self.update_status("Invalid file! Drop a .py file only.", RED_GLOW)
            return

        self._load_file_path(path)

    def _load_file_path(self, path):
        if self._reset_job:
            self.after_cancel(self._reset_job)
            self._reset_job = None
        self.selected_file = path
        self.file_entry.configure(state="normal")
        self.file_entry.delete(0, "end")
        self.file_entry.insert(0, path)
        self.file_entry.configure(state="readonly")
        self.file_entry.configure(border_color=RED_PRIMARY)
        self.after(600, lambda: self.file_entry.configure(border_color="#2E2E3A"))
        self.update_status(f"Loaded: {os.path.basename(path)}", TEXT_WHITE)
        self.progress.set(0)

    def select_file(self):
        path = filedialog.askopenfilename(
            title="Select Python Script",
            filetypes=[("Python Files", "*.py")]
        )
        if path:
            self._load_file_path(path)

    def update_status(self, text, color=TEXT_MUTED):
        self.status_label.configure(text=f"Status: {text}", text_color=color)

    def open_about(self):
        AboutWindow(self)

    def _animate_progress(self, target, step=0.05, on_done=None):
        current = self.progress.get()
        if abs(current - target) <= abs(step):
            self.progress.set(target)
            if on_done:
                on_done()
            return
        next_val = current + step if target > current else current - abs(step)
        self.progress.set(max(0.0, min(1.0, next_val)))
        self.after(15, lambda: self._animate_progress(target, step, on_done))

    def start_protection(self):
        if not self.selected_file or not os.path.exists(self.selected_file):
            self.update_status("Please drop or select a .py file first!", RED_GLOW)
            return

        if self._reset_job:
            self.after_cancel(self._reset_job)
            self._reset_job = None

        self.progress.set(0)
        self.protect_btn.configure(state="disabled", text="ENCRYPTING...")
        self._animate_progress(0.45, step=0.04)
        threading.Thread(target=self._process_encryption, daemon=True).start()

    def _process_encryption(self):
        try:
            with open(self.selected_file, "r", encoding="utf-8") as f:
                source_code = f.read()

            mode = self.mode_var.get()
            if mode == "base64":
                protected_code = self._encrypt_base64(source_code)
            else:
                protected_code = self._encrypt_sha256_stream(source_code)

            base, ext = os.path.splitext(self.selected_file)
            out_path = f"{base}_protected{ext}"

            with open(out_path, "w", encoding="utf-8") as f:
                f.write(protected_code)

            self.after(0, lambda: self._on_success(out_path))
        except Exception as e:
            self.after(0, lambda: self._on_error(str(e)))

    def _rand_var(self, length=8):
        first = random.choice(string.ascii_letters)
        rest = "".join(random.choices(string.ascii_letters + string.digits, k=length - 1))
        return first + rest

    def _rand_junk(self, length=12):
        chars = string.ascii_letters + string.digits + "+/"
        return "".join(random.choices(chars, k=length))

    def _encrypt_base64(self, code: str) -> str:
        encoded = base64.b64encode(code.encode("utf-8")).decode("utf-8")
        return (
            "import base64\n"
            f'exec(base64.b64decode("{encoded}"))\n'
        )

    def _encrypt_sha256_stream(self, code: str) -> str:
        compressed = zlib.compress(code.encode("utf-8"), level=9)
        key = os.urandom(32)
        nonce = os.urandom(16)

        keystream = bytearray()
        counter = 0
        while len(keystream) < len(compressed):
            block = hashlib.sha256(key + nonce + counter.to_bytes(4, "big")).digest()
            keystream.extend(block)
            counter += 1

        cipher_bytes = bytes(a ^ b for a, b in zip(compressed, keystream[:len(compressed)]))
        mac = hmac.new(key, nonce + cipher_bytes, hashlib.sha256).digest()

        k_b64 = base64.b64encode(key).decode("utf-8")
        n_b64 = base64.b64encode(nonce).decode("utf-8")
        m_b64 = base64.b64encode(mac).decode("utf-8")
        c_b64 = base64.b64encode(cipher_bytes).decode("utf-8")

        chunk_size = max(12, len(c_b64) // 25)
        real_chunks = [c_b64[i:i + chunk_size] for i in range(0, len(c_b64), chunk_size)]

        used_names = set()

        def unique_name():
            while True:
                n = self._rand_var(8)
                if n not in used_names:
                    used_names.add(n)
                    return n

        v_key = unique_name()
        v_nonce = unique_name()
        v_mac = unique_name()

        statements = [
            f"{v_key}='{k_b64}'",
            f"{v_nonce}='{n_b64}'",
            f"{v_mac}='{m_b64}'"
        ]

        real_vars = []
        for chunk in real_chunks:
            vn = unique_name()
            real_vars.append(vn)
            statements.append(f"{vn}='{chunk}'")

        for _ in range(len(real_chunks) + 15):
            jn = unique_name()
            statements.append(f"{jn}='{self._rand_junk(random.randint(10, 16))}'")

        random.shuffle(statements)

        joined_data = "+".join(real_vars)
        exec_stmt = (
            f"exec((lambda b,h,z,m:("
            f"(lambda k,n,c,g:(z.decompress(bytes(x^y for x,y in zip(c,b''.join(h.sha256(k+n+i.to_bytes(4,'big')).digest() for i in range((len(c)+31)//32))))) if m.compare_digest(m.new(k,n+c,h.sha256).digest(),g) else b''))"
            f"(b.b64decode({v_key}),b.b64decode({v_nonce}),b.b64decode({joined_data}),b.b64decode({v_mac}))"
            f"))(__import__('base64'),__import__('hashlib'),__import__('zlib'),__import__('hmac')))"
        )

        statements.append(exec_stmt)
        return ";".join(statements) + "\n"

    def _on_success(self, out_path):
        def after_fill():
            self.protect_btn.configure(state="normal", text="PROTECT SOURCE CODE")
            self.update_status(f"Saved -> {os.path.basename(out_path)}", "#4ADE80")
            self._reset_job = self.after(1500, self._smooth_reset)

        self._animate_progress(1.0, step=0.05, on_done=after_fill)

    def _smooth_reset(self):
        self._animate_progress(0.0, step=0.04, on_done=lambda: self.update_status("Ready for next file", TEXT_MUTED))

    def _on_error(self, err_msg):
        self.progress.set(0)
        self.protect_btn.configure(state="normal", text="PROTECT SOURCE CODE")
        self.update_status(f"Error: {err_msg}", RED_GLOW)


if __name__ == "__main__":
    app = ixShieldApp()
    app.mainloop()