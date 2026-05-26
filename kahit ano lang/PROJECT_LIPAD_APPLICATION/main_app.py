import customtkinter as ctk
import pandas as pd
from tkinter import filedialog
from PIL import Image, ImageTk
import os

# Application Global Settings
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class LipadApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Project LiPAD - Structural Health Analytics Engine")
        self.geometry("1200x800")
        
        # State variables for nested options
        self.selected_inspection = ctk.StringVar(value="None")
        self.selected_corrosion_type = ctk.StringVar(value="None")
        self.uploaded_video_path = None

        # Grid Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 1. PERSISTENT SIDEBAR
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo = ctk.CTkLabel(self.sidebar, text="LiPAD AI", font=ctk.CTkFont(size=22, weight="bold"))
        self.logo.pack(pady=(30, 20))

        # Main Navigation Buttons [Message 23, 28]
        tabs = [("Me", "me"), ("Inspection Options", "options"), ("Media Hub", "media"), 
                ("Analysis", "analysis"), ("Epair", "epair"), ("Reports", "reports")]
        
        for text, name in tabs:
            btn = ctk.CTkButton(self.sidebar, text=text, fg_color="transparent", anchor="w",
                                 command=lambda n=name: self.select_tab(n))
            btn.pack(fill="x", padx=20, pady=5)

        # 2. MAIN CONTENT AREA
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=0, column=1, sticky="nsew", padx=30, pady=30)
        
        self.select_tab("home")

    def select_tab(self, name):
        for widget in self.container.winfo_children(): widget.destroy()

        # TAB 1: HOME PAGE (Totally Separate Introduction) [Message 29]
        if name == "home":
            ctk.CTkLabel(self.container, text="Welcome to Project LiPAD", font=("Arial", 32, "bold")).pack(pady=(0, 20))
            intro_text = (
                "Project LiPAD (Light-based Inspection and Precision Analytics Drone) is an advanced computer vision "
                "platform designed to automate structural health monitoring [2]. By integrating YOLOv12-seg VIS "
                "and deterministic prediction models, LiPAD enables civil engineers to identify, track, and predict "
                "the progression of structural defects such as concrete cracks and steel corrosion [3, 4]."
            )
            lbl = ctk.CTkLabel(self.container, text=intro_text, wraplength=800, justify="left", font=("Arial", 16))
            lbl.pack(pady=10)

        # TAB 2: INSPECTION OPTIONS (Nested Buttons) [Message 29]
        elif name == "options":
            ctk.CTkLabel(self.container, text="Select Inspection Target", font=("Arial", 24, "bold")).pack(pady=20)
            
            btn_frame = ctk.CTkFrame(self.container, fg_color="transparent")
            btn_frame.pack(pady=10)

            ctk.CTkButton(btn_frame, text="Crack Detection", width=200, height=50, 
                          command=lambda: self.set_inspection("Crack")).grid(row=0, column=0, padx=10)
            
            ctk.CTkButton(btn_frame, text="Corrosion Detection", width=200, height=50, 
                          command=lambda: self.set_inspection("Corrosion")).grid(row=0, column=1, padx=10)

            self.sub_options_frame = ctk.CTkFrame(self.container, fg_color="transparent")
            self.sub_options_frame.pack(pady=20)

        # TAB 3: MEDIA HUB (Desktop Upload) [Message 29]
        elif name == "media":
            ctk.CTkLabel(self.container, text="Media Telemetry Hub", font=("Arial", 24, "bold")).pack(pady=20)
            
            self.upload_btn = ctk.CTkButton(self.container, text="Upload MP4 from Desktop", 
                                            command=self.upload_video)
            self.upload_btn.pack(pady=10)
            
            self.status_lbl = ctk.CTkLabel(self.container, text="No video selected.")
            self.status_lbl.pack()

        # TAB 4: ANALYSIS (Connect to results.csv) [306, Message 29]
        elif name == "analysis":
            ctk.CTkLabel(self.container, text="Defect Analytics Engine", font=("Arial", 24, "bold")).pack(pady=20)
            try:
                df = pd.read_csv("data/results.csv")
                # Simplified table display logic
                table_text = df.to_string()
                textbox = ctk.CTkTextbox(self.container, width=800, height=400)
                textbox.insert("0.0", table_text)
                textbox.pack()
            except Exception as e:
                ctk.CTkLabel(self.container, text="results.csv not found. Run the engine first.").pack()

        # TAB 5: REPAIR (Literature-Based Suggestions) [55, Message 29]
        elif name == "repair":
            ctk.CTkLabel(self.container, text="Suggested Engineering Repairs", font=("Arial", 24, "bold")).pack(pady=20)
            self.show_repair_logic()

    def set_inspection(self, target):
        self.selected_inspection.set(target)
        for widget in self.sub_options_frame.winfo_children(): widget.destroy()
        
        if target == "Corrosion":
            ctk.CTkLabel(self.sub_options_frame, text="Select Corrosion Environment:").pack(pady=5)
            ctk.CTkButton(self.sub_options_frame, text="Wet Corrosion (Marine)", 
                          command=lambda: self.selected_corrosion_type.set("Wet")).pack(side="left", padx=10)
            ctk.CTkButton(self.sub_options_frame, text="Dry Corrosion (Oxidation)", 
                          command=lambda: self.selected_corrosion_type.set("Dry")).pack(side="left", padx=10)
        else:
            ctk.CTkLabel(self.sub_options_frame, text="Scanning for concrete fractures selected.").pack()

    def upload_video(self):
        file_path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
        if file_path:
            self.uploaded_video_path = file_path
            self.status_lbl.configure(text=f"Loaded: {os.path.basename(file_path)}")

    def show_repair_logic(self):
        """Rule-based suggestion logic connected to Analysis data [1, 5]"""
        try:
            df = pd.read_csv("data/results.csv")
            latest_defect = df.iloc[-1] # Grabs most recent detection
            
            defect_type = latest_defect['Type']
            severity = latest_defect['Severity']
            
            suggestion = "No action required."
            if defect_type == "Crack" and severity == "Structural":
                suggestion = "LITERATURE REF [6]: Immediate epoxy injection and structural bracing required."
            elif defect_type == "Corrosion" and severity == "Severe":
                suggestion = "LITERATURE REF [7]: Immediate abrasive blasting and cathodic protection required [3]."
                
            ctk.CTkLabel(self.container, text=f"Last Detected: {defect_type} ({severity})", font=("Arial", 16, "bold")).pack()
            ctk.CTkLabel(self.container, text=suggestion, wraplength=600, text_color="orange").pack(pady=20)
        except:
            ctk.CTkLabel(self.container, text="Awaiting data from Analysis tab...").pack()

if __name__ == "__main__":
    app = LipadApp()
    app.mainloop()