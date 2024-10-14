import tkinter as tk
import pyperclip
from pynput import mouse
import google.generativeai as genai
import threading
import tkinter.font as tkFont
from google.generativeai.types import HarmCategory, HarmBlockThreshold

API_KEY = "AIzaSyDbCxNdRAnwnk7hFnJarnURPW7hxrrVkDA"  # Replace with your actual API key

# Configure the API key
genai.configure(api_key=API_KEY)

class ClipboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Clipboard Viewer")
        self.root.geometry("500x300")
        # self.root.attributes('-topmost', True)  # Stay on top

        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()

        # Start the window in the top-right corner
        # self.position = "right"
        # self.root.geometry(f"+{self.screen_width - 500}+0")

        # Create a frame for the text widget and scrollbar
        frame = tk.Frame(root)
        frame.pack(expand=True, fill=tk.BOTH)

        self.font = tkFont.Font(size=18)  
        self.text_area = tk.Text(frame, wrap=tk.WORD, state=tk.DISABLED, font=self.font)
        self.text_area.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        # Create a Scrollbar and attach it to the Text widget
        self.scrollbar = tk.Scrollbar(frame, command=self.text_area.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area.config(yscrollcommand=self.scrollbar.set)

        # Create a label for the loading GIF
        self.loading_label = tk.Label(root)
        self.loading_label.pack(pady=20)

        # Load the GIF (make sure to have a 'loading.gif' in your directory)
        self.loading_gif = tk.PhotoImage(file="loading.gif")
        self.loading_label.config(image=self.loading_gif)
        self.loading_label.pack_forget()  # Initially hide the loading label

        # Bind event for mouse hover to switch the window's position
        # self.root.bind("<Enter>", self.switch_position)

        # Start the mouse listener
        self.listener = mouse.Listener(on_click=self.on_click)
        self.listener.start()

    def switch_position(self, event):
        """Switch between top-right and top-left corners."""
        if self.position == "right":
            # Move to top-left corner
            self.root.geometry(f"+0+0")
            self.position = "left"
        elif self.position == "left":
            # Move to top-right corner
            self.root.geometry(f"+{self.screen_width - 500}+0")
            self.position = "right"

    def on_click(self, x, y, button, pressed):
        if button == mouse.Button.x1 and pressed:  # Mouse button 4 (x1)
            self.root.after(100, self.show_clipboard_content)

    def summarize_content(self, content):
        # Show the loading label
        self.loading_label.pack()
        self.root.update_idletasks()  # Update the UI to show the loading icon

        # Generate summary using the AI API
        summary_response = genai.GenerativeModel(model_name="gemini-1.5-flash").generate_content(
            f"Summarize the following in 30% of what actually the content is:\n\n{content}",
            safety_settings={
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE
            }
        )

        # Hide the loading label
        self.loading_label.pack_forget()
        return summary_response.text

    def show_clipboard_content(self):
        try:
            clipboard_content = pyperclip.paste()
            summarized_content = self.summarize_content(clipboard_content)
            self.text_area.config(state=tk.NORMAL)
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, summarized_content)
            self.text_area.config(state=tk.DISABLED)
        except pyperclip.PyperclipException:
            self.text_area.config(state=tk.NORMAL)
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, "Failed to read clipboard.")
            self.text_area.config(state=tk.DISABLED)

    def run(self):
        self.root.mainloop()
        self.listener.stop()

if __name__ == "__main__":
    root = tk.Tk()
    app = ClipboardApp(root)
    app.run()
