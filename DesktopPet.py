"""Building something fun for myself =  A little desktop buddy to keep me 
entertained while I work on my computer. Roams the taskbar.
 """

import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import random
import time
import os
import sys

# New: directory where you should put your pet images (create 'pet_images' next to this file)
PET_ASSETS_DIR = os.path.join(os.path.dirname(__file__), "pet_images")
SUPPORTED_EXTS = (".png", ".gif", ".jpg", ".jpeg")

# New: lock vertical movement to taskbar (True = pet only moves horizontally at bottom)
LOCK_TO_TASKBAR = True

class DesktopPet:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)  # Remove window decorations
        self.root.attributes("-topmost", True)  # Keep on top of other windows

        # Transparent background color (choose a color unlikely used in images)
        self.transparent_color = "#123456"
        self.root.config(bg=self.transparent_color)
        # Enable Tk transparent color (Windows, some X11 managers)
        try:
            self.root.wm_attributes("-transparentcolor", self.transparent_color)
        except Exception:
            pass

        # Try to make window click-through on Windows so it doesn't steal clicks
        if sys.platform.startswith("win"):
            try:
                import ctypes
                GWL_EXSTYLE = -20
                WS_EX_LAYERED = 0x00080000
                WS_EX_TRANSPARENT = 0x00000020
                WS_EX_TOOLWINDOW = 0x00000080
                hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
                prev_style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
                ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, prev_style | WS_EX_LAYERED | WS_EX_TRANSPARENT | WS_EX_TOOLWINDOW)
            except Exception:
                pass

        # Initial position
        self.root.geometry("+100+100")

        # Load pet images (with fallback if missing)
        self.images = []
        # Try to load from PET_ASSETS_DIR first (sorted for consistent animation order)
        try:
            if not os.path.isdir(PET_ASSETS_DIR):
                print(f"[DesktopPet] image folder not found; create and add frames here: {PET_ASSETS_DIR}")
            else:
                print(f"[DesktopPet] loading images from: {PET_ASSETS_DIR} (supported: {', '.join(SUPPORTED_EXTS)})")
                files = sorted(os.listdir(PET_ASSETS_DIR))
                for fname in files:
                    if fname.lower().endswith(SUPPORTED_EXTS):
                        path = os.path.join(PET_ASSETS_DIR, fname)
                        try:
                            img = Image.open(path).convert("RGBA").resize((80, 80), Image.ANTIALIAS)
                            self.images.append(ImageTk.PhotoImage(img))
                        except Exception as e:
                            print(f"[DesktopPet] failed to load {path}: {e}")
        except Exception as e:
            print(f"[DesktopPet] error accessing assets dir: {e}")

        # Fallback if no images found in folder: try original naming convention in script folder
        if not self.images:
            for i in range(1, 5):
                path = os.path.join(os.path.dirname(__file__), f"pet_frame_{i}.png")
                if os.path.exists(path):
                    try:
                        img = Image.open(path).convert("RGBA").resize((80, 80), Image.ANTIALIAS)
                        self.images.append(ImageTk.PhotoImage(img))
                    except Exception as e:
                        print(f"[DesktopPet] failed to load {path}: {e}")

        # Final fallback: create a simple placeholder pet programmatically (embedded image)
        if not self.images:
            print(f"[DesktopPet] no pet images found; using drawn placeholder pet.")
            # Draw a cute circular pet with eyes and a small smile
            size = (80, 80)
            base = Image.new("RGBA", size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(base)
            # body
            draw.ellipse((4, 8, 76, 72), fill=(255, 167, 167, 255), outline=(200,80,80,255))
            # left eye
            draw.ellipse((24, 28, 32, 36), fill=(0,0,0,255))
            # right eye
            draw.ellipse((48, 28, 56, 36), fill=(0,0,0,255))
            # smile
            draw.arc((28, 36, 52, 56), start=10, end=170, fill=(0,0,0,255), width=2)
            self.images.append(ImageTk.PhotoImage(base))

        self.current_image = 0

        # Create label to hold the pet image; use transparent bg
        self.label = tk.Label(root, image=self.images[self.current_image], bg=self.transparent_color, bd=0)
        self.label.pack()

        # Right-click menu to quit
        self.menu = tk.Menu(root, tearoff=0)
        self.menu.add_command(label="Quit", command=self.root.destroy)
        self.label.bind("<Button-3>", self.show_menu)

        # Movement state
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        self.pet_w = self.images[0].width()
        self.pet_h = self.images[0].height()

        # Taskbar area: keep y near bottom (adjust offset if taskbar height differs)
        self.taskbar_offset = 40  # distance above bottom of screen
        # if LOCK_TO_TASKBAR is True we don't use vertical jitter
        self.taskbar_range = 0 if LOCK_TO_TASKBAR else 20   # vertical jitter range

        # Movement targets and speed
        self.target_x = 100
        # Ensure initial target_y is snapped to bottom/taskbar area
        self.target_y = self.screen_height - self.pet_h - self.taskbar_offset
        self.speed = 8  # pixels per frame

        # Start animation and movement
        self.animate()
        self.schedule_new_target()

    def show_menu(self, event):
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()

    def animate(self):
        """Cycle through pet images to create animation effect."""
        self.current_image = (self.current_image + 1) % len(self.images)
        self.label.config(image=self.images[self.current_image])
        self.smooth_move_step()
        self.root.after(120, self.animate)  # Change frame every 120 ms

    def schedule_new_target(self):
        """Pick a new X target across the screen while keeping Y near the taskbar."""
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        new_x = random.randint(0, max(0, self.screen_width - self.pet_w))
        base_y = self.screen_height - self.pet_h - self.taskbar_offset
        if LOCK_TO_TASKBAR:
            new_y = base_y  # lock vertically to taskbar line
        else:
            new_y = base_y + random.randint(-self.taskbar_range, self.taskbar_range)
        self.target_x = new_x
        self.target_y = max(0, min(self.screen_height - self.pet_h, new_y))
        # choose next target in a bit (move while animating)
        delay = random.randint(3000, 8000)  # pick next target every 3-8s
        self.root.after(delay, self.schedule_new_target)

    def smooth_move_step(self):
        """Move a small step toward the current target (create smooth motion)."""
        try:
            geom = self.root.geometry().split('+')
            if len(geom) >= 3:
                cur_x = int(geom[1])
                cur_y = int(geom[2])
            else:
                cur_x, cur_y = 0, 0
        except Exception:
            cur_x, cur_y = 0, 0

        dx = self.target_x - cur_x
        # If locked to taskbar, force current Y -> target_y so movement stays on the bar
        if LOCK_TO_TASKBAR:
            dy = 0
            cur_y = self.target_y
        else:
            dy = self.target_y - cur_y

        dist = max(1, (dx*dx + dy*dy) ** 0.5)
        if dist < 2:
            # close enough; snap to target (ensuring Y is bottom if locked)
            final_y = self.target_y if not LOCK_TO_TASKBAR else self.target_y
            self.root.geometry(f"+{self.target_x}+{final_y}")
            return

        step_x = int(self.speed * dx / dist)
        step_y = int(self.speed * dy / dist) if not LOCK_TO_TASKBAR else 0
        new_x = cur_x + step_x
        new_y = cur_y + step_y
        # if locked, force new_y to target_y exactly
        if LOCK_TO_TASKBAR:
            new_y = self.target_y
        self.root.geometry(f"+{new_x}+{new_y}")

if __name__ == "__main__":
    root = tk.Tk()
    pet = DesktopPet(root)
    root.mainloop()