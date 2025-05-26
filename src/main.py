import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import threading
import os
from metrics.main import run_metrics
from pandastable import Table
import pandas as pd
try:
    from fdx_src import fdx
except:
    print("Warning: Could not import fdx_src module. FDX functionality will not be available.")
    fdx = None


class CSVProcessor:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV File Processor")
        
        # self.root.state('zoomed')  # For Windows
        self.root.attributes('-zoomed', True) # For Linux/Mac
        
        self.file_path = None
        self.metrics_csv_path = None
        self.metrics_fds_path = None
        
        # Create a notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.create_processing_tab()
        self.create_metrics_tab()
        self.create_views_tab()

    def create_views_tab(self):
        """Create the views tab"""
        self.views_frame = tk.Frame(self.notebook)
        self.notebook.add(self.views_frame, text="Views")
        
        # Create a frame for the content
        views_content = tk.Frame(self.views_frame, padx=20, pady=20)
        views_content.pack(fill=tk.BOTH, expand=True)
        
        # Add a label with instructions
        self.views_label = tk.Label(
            views_content, 
            text="Select a CSV file to view",
            font=("Arial", 12)
        )
        self.views_label.pack(pady=10)
        
        # Add a button to select the file
        self.view_select_button = tk.Button(
            views_content,
            text="Choose CSV File",
            command=self.select_view_file,
            width=20,
            height=2,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold")
        )
        self.view_select_button.pack(pady=10)
        
        # Add a label to display the selected file path
        self.view_file_label = tk.Label(
            views_content,
            text="No file selected",
            font=("Arial", 10),
            wraplength=400
        )
        self.view_file_label.pack(pady=10)
        
        # Create a frame for the table
        self.table_frame = tk.Frame(views_content)
        self.table_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create a placeholder for the table
        self.placeholder_label = tk.Label(
            self.table_frame,
            text="Select a CSV file to display data",
            font=("Arial", 10),
            fg="gray"
        )
        self.placeholder_label.pack(pady=20)
    
    def create_processing_tab(self):
        """Create the main processing tab"""
        # Create a frame for the processing tab
        self.processing_frame = tk.Frame(self.notebook)
        self.notebook.add(self.processing_frame, text="Processing")
        
        # Create a frame for the content
        self.main_frame = tk.Frame(self.processing_frame, padx=20, pady=20)
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
    
    def create_metrics_tab(self):
        """Create the metrics tab"""
        # Create a frame for the metrics tab
        self.metrics_frame = tk.Frame(self.notebook)
        self.notebook.add(self.metrics_frame, text="Metrics")
        
        # Create a frame for the content
        metrics_content = tk.Frame(self.metrics_frame, padx=20, pady=20)
        metrics_content.pack(fill=tk.BOTH, expand=True)
        
        # Add a label for the metrics tab
        metrics_label = tk.Label(
            metrics_content,
            text="Algorithm Performance Metrics",
            font=("Arial", 14, "bold")
        )
        metrics_label.pack(pady=20)
        
        # CSV file selection section
        csv_frame = tk.Frame(metrics_content)
        csv_frame.pack(fill=tk.X, pady=10)
        
        self.csv_select_button = tk.Button(
            csv_frame,
            text="Select CSV File",
            command=self.select_metrics_csv,
            width=20,
            height=2,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold")
        )
        self.csv_select_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.csv_file_label = tk.Label(
            csv_frame,
            text="No CSV file selected",
            font=("Arial", 10),
            wraplength=300
        )
        self.csv_file_label.pack(side=tk.LEFT)
        
        # FDS file selection section
        fds_frame = tk.Frame(metrics_content)
        fds_frame.pack(fill=tk.X, pady=10)
        
        self.fds_select_button = tk.Button(
            fds_frame,
            text="Select FDS File",
            command=self.select_metrics_fds,
            width=20,
            height=2,
            bg="#FF9800",
            fg="white",
            font=("Arial", 10, "bold")
        )
        self.fds_select_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.fds_file_label = tk.Label(
            fds_frame,
            text="No FDS file selected",
            font=("Arial", 10),
            wraplength=300
        )
        self.fds_file_label.pack(side=tk.LEFT)
        
        # Add observation about file relationship
        observation_label = tk.Label(
            metrics_content,
            text="Note: The FDS file must be related to the selected CSV dataset",
            font=("Arial", 9, "italic"),
            fg="orange"
        )
        observation_label.pack(pady=(10, 0))
        
        # Add run metrics button (disabled initially)
        self.run_metrics_button = tk.Button(
            metrics_content,
            text="Run Metrics Analysis",
            command=self.run_metrics_analysis,
            width=20,
            height=2,
            state=tk.DISABLED,
            bg="#9C27B0",
            fg="white",
            font=("Arial", 10, "bold")
        )
        self.run_metrics_button.pack(pady=20)
        
        # Add a progress bar for metrics (hidden initially)
        self.metrics_progress = ttk.Progressbar(
            metrics_content, 
            orient="horizontal", 
            length=400, 
            mode="indeterminate"
        )
        
        # Add metrics output text area
        self.metrics_output_frame = tk.Frame(metrics_content)
        self.metrics_output_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.metrics_output_label = tk.Label(
            self.metrics_output_frame,
            text="Metrics Analysis Output:",
            font=("Arial", 10)
        )
        self.metrics_output_label.pack(anchor=tk.W)
        
        self.metrics_output_text = tk.Text(
            self.metrics_output_frame,
            height=8,
            width=50,
            font=("Courier", 9),
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.metrics_output_text.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollbar to metrics output text
        self.metrics_scrollbar = tk.Scrollbar(self.metrics_output_text)
        self.metrics_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.metrics_output_text.config(yscrollcommand=self.metrics_scrollbar.set)
        self.metrics_scrollbar.config(command=self.metrics_output_text.yview)
        
        # Placeholder content for metrics display
        placeholder_label = tk.Label(
            metrics_content,
            text="Select files and run analysis to display metrics results",
            font=("Arial", 10),
            fg="gray"
        )
        placeholder_label.pack(pady=10)
    
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
    
    def select_metrics_csv(self):
        """Open a file dialog to select a CSV file for metrics"""
        file_path = filedialog.askopenfilename(
            title="Select CSV dataset for metrics",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialdir="../datasets"
        )
        
        if file_path:
            self.metrics_csv_path = file_path
            self.csv_file_label.config(text=f"CSV: {os.path.basename(file_path)}")
            self.check_metrics_files_selected()
    
    def select_metrics_fds(self):
        """Open a file dialog to select an FDS file for metrics"""
        file_path = filedialog.askopenfilename(
            title="Select FDS file for metrics",
            filetypes=[("FDS files", "*_fds"), ("All files", "*.*")],
            initialdir="./results"
        )
        
        if file_path:
            self.metrics_fds_path = file_path
            self.fds_file_label.config(text=f"FDS: {os.path.basename(file_path)}")
            self.check_metrics_files_selected()
    
    def check_metrics_files_selected(self):
        """Enable run metrics button if both files are selected"""
        if hasattr(self, 'metrics_csv_path') and hasattr(self, 'metrics_fds_path'):
            if self.metrics_csv_path and self.metrics_fds_path:
                self.run_metrics_button.config(state=tk.NORMAL)
    
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
                script_path = os.path.join("./", script_name)
                os.chmod(script_path, 0o755)
                
                script_dir = os.path.dirname(script_path)
                
                # Run the script and capture output
                process = subprocess.Popen(
                    [script_path, file_path],
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
    
    def run_metrics_analysis(self):
        """Run the metrics analysis on the selected files"""
        if not self.metrics_csv_path or not self.metrics_fds_path:
            messagebox.showerror("Error", "Please select both CSV and FDS files")
            return
        
        # Disable the button during processing
        self.run_metrics_button.config(state=tk.DISABLED)
        
        # Show progress bar
        self.metrics_progress.pack(pady=10)
        self.metrics_progress.start()
        
        # Clear previous output
        self.metrics_output_text.config(state=tk.NORMAL)
        self.metrics_output_text.delete(1.0, tk.END)
        self.metrics_output_text.config(state=tk.DISABLED)
        
        # Run the metrics analysis in a separate thread
        metrics_thread = threading.Thread(
            target=self.execute_metrics_analysis
        )
        metrics_thread.daemon = True
        metrics_thread.start()
    
    def execute_metrics_analysis(self):
        """Execute the metrics analysis"""
        try:
            # Determine source_type based on filename
            source_type = "metanome" if "_fds" in os.path.basename(self.metrics_fds_path) else "fdx"
            has_header = True  # Always true as specified
            
            self.update_metrics_output(f"Starting metrics analysis...\n")
            self.update_metrics_output(f"CSV: {os.path.basename(self.metrics_csv_path)}\n")
            self.update_metrics_output(f"FDS: {os.path.basename(self.metrics_fds_path)}\n")
            self.update_metrics_output(f"Source type: {source_type}\n")
            self.update_metrics_output(f"Has header: {has_header}\n\n")
            
            # Call the run_metrics function
            results = run_metrics(
                dataset_csv_file=self.metrics_csv_path,
                fds_input_file=self.metrics_fds_path,
                source_type=source_type,
                hasHeader=has_header
            )
            
            self.update_metrics_output("Metrics analysis completed successfully!\n\n")
            self.update_metrics_output(f"Results saved to: {results['output_folder']}\n")
            self.update_metrics_output(f"FDs CSV: {results['fds_csv_file']}\n")
            self.update_metrics_output(f"Runtime CSV: {results['metrics_csv_file']}\n")
            self.update_metrics_output(f"Total time: {results['total_time']:.2f} seconds\n")
            self.update_metrics_output(f"Number of FDs processed: {results['num_fds']}\n")
            
        except Exception as e:
            self.update_metrics_output(f"Error during metrics analysis: {str(e)}\n")
        finally:
            # Re-enable the button and hide progress bar
            self.root.after(0, self.finish_metrics_processing)
    
    def update_metrics_output(self, text):
        """Update the metrics output text area safely from any thread"""
        def update():
            self.metrics_output_text.config(state=tk.NORMAL)
            self.metrics_output_text.insert(tk.END, text)
            self.metrics_output_text.see(tk.END)
            self.metrics_output_text.config(state=tk.DISABLED)
        
        self.root.after(0, update)
    
    def finish_metrics_processing(self):
        """Clean up after metrics processing is done"""
        self.metrics_progress.stop()
        self.metrics_progress.pack_forget()
        self.run_metrics_button.config(state=tk.NORMAL)

    def select_view_file(self):
        """Open file dialogs to select multiple CSV files to view, possibly from different directories"""
        all_files = []
        
        while True:
            file_paths = filedialog.askopenfilenames(
                title="Select CSV file(s) to view (Cancel when done)",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                initialdir="./metrics_results"
            )
            
            if not file_paths:  # User clicked Cancel
                break
            
            all_files.extend(file_paths)
            
            continue_selecting = messagebox.askyesno(
                "Continue Selection?", 
                f"Added {len(file_paths)} file(s). Select more files from another directory?"
            )
            
            if not continue_selecting:
                break
        
        if all_files:
            self.process_selected_files(all_files)

    def process_selected_files(self, file_paths):
        """Process the selected CSV files"""
        try:
            # Update the label with selected files
            if len(file_paths) == 1:
                self.view_file_label.config(text=f"Selected: {os.path.basename(file_paths[0])}")
            else:
                self.view_file_label.config(text=f"Selected: {len(file_paths)} files")
            
            # Clear the table frame
            for widget in self.table_frame.winfo_children():
                widget.destroy()
            
            # Load and merge the CSV files into a pandas DataFrame
            dfs = []
            for file_path in file_paths:
                df = pd.read_csv(file_path)
                # Add filename as a column to identify source
                df['source_file'] = os.path.basename(file_path)
                dfs.append(df)
            
            # Combine all dataframes
            if len(dfs) > 1:
                df = pd.concat(dfs, ignore_index=True)
            else:
                df = dfs[0]
            
            # Create a container frame to hold table and plot side by side
            container_frame = tk.Frame(self.table_frame)
            container_frame.pack(fill=tk.BOTH, expand=True)
            
            # Create left frame for table (65% width)
            table_frame = tk.Frame(container_frame)
            table_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
            
            # Create the pandastable in the table frame
            self.pt = Table(table_frame, dataframe=df, showtoolbar=True, showstatusbar=True)
            self.pt.show()
            self.pt.showIndex()
            self.pt.redraw()
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not load the CSV file(s): {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CSVProcessor(root)
    root.mainloop()
