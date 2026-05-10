import tkinter as tk
from tkinter import scrolledtext
import re

class ExpIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("ExpStudio - .exp Language IDE")
        # Widened the window geometry to 1200px
        self.root.geometry("1200x750")
        self.root.configure(bg="#1e1e1e")

        # --- THE 10 EXPERT ERRORS ---
        self.errors = {
            "use": "ERROR_The resource file you are trying to link doesn't exist or isn't found. The expert can only be used to use valid resources or architecture",
            "access": "ERROR_The agent @access has encountered a denial of access of the file requested",
            "pen": "ERROR_The expert @pen failed to recognize the file type. Please choose a png or a visual object file...",
            "penWIN": "ERROR_The agent @penWIN couldn't find anything to display or has failed to read the file. Please check the code syntax or restart penWIN",
            "computer": "ERROR_The expert @computer is not allowed to do the following operation...",
            "math": "ERROR_Invalid operation!",
            "Inet": "ERROR_The expert @Inet couldn't find the following link. The following link doesn't exist, has been removed, is corrupted or experiencing a Cloudflare error",
            "imp": "ERROR_@exp codes don't have access to system files or control over hard disks. the expert @imp is used only to import SAFE TO ALTER AND EDIT files",
            "exp": "ERROR_Unrecognised code syntax",
            "IDE": "ERROR_@IDE isn't able to execute the following program. Check and correct syntax errors"
        }

        # --- UI LAYOUT (Original Base Design - Widened) ---
        tk.Label(root, text="EDITOR (.exp)", bg="#1e1e1e", fg="white", font=("Courier", 12)).pack()
        self.editor = scrolledtext.ScrolledText(root, width=130, height=12, bg="#2d2d2d", fg="#dcdcdc", font=("Courier", 11))
        self.editor.pack(pady=5)
        
        self.editor.insert(tk.INSERT, "@math(100+1)\n@Inet(random_text)\n@pen(video.mp4)\n@imp(kernel.sys)\n@access(C:/System32)")

        self.run_btn = tk.Button(root, text="RUN @exp PROGRAM", command=self.run_code, bg="#007acc", fg="white", font=("Arial", 10, "bold"))
        self.run_btn.pack(pady=5)

        self.bottom_frame = tk.Frame(root, bg="#1e1e1e")
        self.bottom_frame.pack(fill="both", expand=True, padx=20)

        # Widened console width from 50 to 80 to fit the long error strings
        self.console = scrolledtext.ScrolledText(self.bottom_frame, width=80, height=18, bg="black", fg="#00ff00", font=("Courier", 10))
        self.console.pack(side="left", padx=5, pady=5, fill="both", expand=True)

        self.display = tk.Canvas(self.bottom_frame, width=400, height=300, bg="#333333", highlightthickness=1, highlightbackground="white")
        self.display.pack(side="right", padx=5, pady=5)

    def run_code(self):
        self.console.delete(1.0, tk.END)
        self.display.delete("all")
        lines = self.editor.get("1.0", tk.END).splitlines()

        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line: continue

            if any(x in line.upper() for x in ["C:/", "D:/", "SYSTEM32"]):
                self.trigger_error("computer", i)
                continue

            match = re.fullmatch(r"@([a-zA-Z]+)\((.*)\)", line)
            if not match:
                self.trigger_error("exp", i)
                continue

            agent = match.group(1)
            content = match.group(2)

            # --- STRICT VALIDATION BRAINS ---
            if agent == "math":
                if re.match(r"^[0-9+\-*/().\s^]+$", content):
                    try:
                        res = eval(content.replace("^", "**"))
                        self.console.insert(tk.END, f"[@math] RESULT: {res}\n")
                    except: self.trigger_error("math", i)
                else: self.trigger_error("math", i)

            elif agent == "pen":
                if content.lower().endswith(('.png', '.jpg', '.obj')):
                    self.console.insert(tk.END, f"[@pen] File valid: {content}\n")
                else: self.trigger_error("pen", i)

            elif agent == "penWIN":
                if content.lower() in ["circle", "square"]:
                    self.console.insert(tk.END, f"[@penWIN] Executing: {content}\n")
                    if content == "circle": self.display.create_oval(150, 75, 250, 175, outline="cyan")
                else: self.trigger_error("penWIN", i)

            elif agent == "Inet":
                if "http" in content or ("." in content and len(content) > 4):
                    self.console.insert(tk.END, f"[@Inet] Link verified: {content}\n")
                else: self.trigger_error("Inet", i)

            elif agent == "imp":
                if any(ext in content.lower() for ext in [".exe", ".sys", ".dll"]):
                    self.trigger_error("imp", i)
                else: self.console.insert(tk.END, f"[@imp] Imported safe file: {content}\n")

            elif agent == "access":
                if any(sym in content for sym in ["/", "\\", ":"]):
                    self.trigger_error("access", i)
                else: self.console.insert(tk.END, f"[@access] Permission granted: {content}\n")

            elif agent == "use":
                if "arch" in content.lower():
                    self.console.insert(tk.END, f"[@use] Architecture linked: {content}\n")
                else: self.trigger_error("use", i)

            elif agent in ["IDE", "exp", "computer"]:
                self.console.insert(tk.END, f"[@{agent}] Command processed.\n")
            else:
                self.trigger_error("exp", f"Unknown Agent @{agent} Line {i}")

    def trigger_error(self, agent, details):
        msg = self.errors.get(agent, "Error")
        self.console.insert(tk.END, f"[@{agent}] {msg} (Line {details})\n", "err")
        self.console.tag_config("err", foreground="red")

if __name__ == "__main__":
    root = tk.Tk()
    ExpIDE(root)
    root.mainloop()
