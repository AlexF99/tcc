import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import threading
import os
from fdx_src import fdx

class CSVProcessor:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV File Processor")
        self.root.geometry("600x400")
        self.file_path = None
        
        # Create a frame for the content
        self.main_frame = tk.Frame(root, padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add a label with instructions
        self.label = tk.Label(
            self.main_frame, 
            text="Select a CSV file to process",
            font=("Arial", 12)
        )
        self.label.pack(pady=20)
        
        # Add a button to select the file
        self.select_button = tk.Button(
            self.main_frame,
            text="Choose CSV File",
            command=self.select_file,
            width=20,
            height=2,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold")
        )
        self.select_button.pack(pady=10)
        
        # Add a label to display the selected file path
        self.file_label = tk.Label(
            self.main_frame,
            text="No file selected",
            font=("Arial", 10),
            wraplength=400
        )
        self.file_label.pack(pady=10)
        
        # Create a frame for algorithm selection
        self.algo_frame = tk.Frame(self.main_frame)
        self.algo_frame.pack(pady=10, fill=tk.X)
        
        # Add algorithm selection dropdown
        self.algo_label = tk.Label(
            self.algo_frame,
            text="Select Algorithm:",
            font=("Arial", 10)
        )
        self.algo_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.algorithm = tk.StringVar()
        self.algorithm.set("Pyro")  # Default selection
        self.algorithms = ["Pyro", "FDX"]

        self.na_values = "empty"
        self.sparsity = 0.0

        self.algo_dropdown = ttk.Combobox(
            self.algo_frame,
            textvariable=self.algorithm,
            values=self.algorithms,
            state="readonly",
            width=20
        )
        self.algo_dropdown.pack(side=tk.LEFT)
        
        # Add a button to process the file (disabled initially)
        self.process_button = tk.Button(
            self.main_frame,
            text="Process CSV",
            command=self.process_file,
            width=20,
            height=2,
            state=tk.DISABLED,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10, "bold")
        )
        self.process_button.pack(pady=10)
        
        # Add a progress bar (hidden initially)
        self.progress = ttk.Progressbar(
            self.main_frame, 
            orient="horizontal", 
            length=400, 
            mode="indeterminate"
        )
        
        # Add a text area for output
        self.output_frame = tk.Frame(self.main_frame)
        self.output_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.output_label = tk.Label(
            self.output_frame,
            text="Process Output:",
            font=("Arial", 10)
        )
        self.output_label.pack(anchor=tk.W)
        
        self.output_text = tk.Text(
            self.output_frame,
            height=5,
            width=50,
            font=("Courier", 9),
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollbar to output text
        self.scrollbar = tk.Scrollbar(self.output_text)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_text.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.output_text.yview)
    
    def select_file(self):
        """Open a file dialog to select a CSV file"""
        file_path = filedialog.askopenfilename(
            title="Select dataset",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialdir="../datasets"
        )
        
        if file_path:
            self.file_path = file_path
            self.file_label.config(text=f"Selected: {os.path.basename(file_path)}")
            self.process_button.config(state=tk.NORMAL)
    
    def process_file(self):
        """Process the selected CSV file with the chosen algorithm"""
        if not self.file_path:
            messagebox.showerror("Error", "No file selected")
            return
        
        # Disable the process button during processing
        self.process_button.config(state=tk.DISABLED)
        
        # Show progress bar
        self.progress.pack(pady=10)
        self.progress.start()
        
        # Clear previous output
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state=tk.DISABLED)
        
        # Run the processing in a separate thread to keep UI responsive
        processing_thread = threading.Thread(
            target=self.run_algorithm,
            args=(self.algorithm.get(), self.file_path)
        )

        processing_thread.daemon = True
        processing_thread.start()
    
    def run_algorithm(self, algorithm, file_path):
        """Run the selected algorithm on the file"""
        try:
            self.update_output(f"Processing {os.path.basename(file_path)} with {algorithm}...\n")

            if algorithm == "FDX":
                fdx(file_path, na_values=self.na_values, sparsity=self.sparsity)
            elif algorithm == "Pyro":
                script_name = "run_pyro.sh"
                script_path = os.path.join("../metanome-cli", script_name)
                os.chmod(script_path, 0o755)
                
                script_dir = os.path.dirname(script_path)
                
                # Run the script and capture output
                process = subprocess.Popen(
                    [script_name, file_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    shell=False,
                    cwd=script_dir
                )
                
                stdout, stderr = process.communicate()
                self.update_output(f"Output:\n{stdout}")
                self.update_output(f"Error:\n{stderr}")
            else:
                # Placeholder for other algorithms
                self.update_output(f"Algorithm '{algorithm}' not implemented yet.")
                
        except Exception as e:
            self.update_output(f"Error: {str(e)}")
        finally:
            # Re-enable the process button and hide progress bar
            self.root.after(0, self.finish_processing)
    
    def update_output(self, text):
        """Update the output text area safely from any thread"""
        def update():
            self.output_text.config(state=tk.NORMAL)
            self.output_text.insert(tk.END, text + "\n")
            self.output_text.see(tk.END)
            self.output_text.config(state=tk.DISABLED)
        
        self.root.after(0, update)
    
    def finish_processing(self):
        """Clean up after processing is done"""
        self.progress.stop()
        self.progress.pack_forget()
        self.process_button.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = CSVProcessor(root)
    root.mainloop()
