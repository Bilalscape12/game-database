import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

class DBApplication:
    def __init__(self, root):
        self.root = root
        # Program title
        self.root.title("Video Game Searcher")
        self.connection = openConnection("Checkpoint3-dbase.sqlite3")
        
        # Text box for searching
        search_frame = ttk.Frame(root, padding="10")
        search_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        # Center the contents of search_frame
        search_frame.columnconfigure(1, weight=1)
        
        ttk.Label(search_frame, text="Search:").grid(row=0, column=0, padx=5)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=50)
        self.search_entry.grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E))
        
        # Left side panel for filters
        filter_frame = ttk.LabelFrame(root, text="Filters", padding="10")
        filter_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=5)
        
        # Sales range slider from 0 to 50 million
        ttk.Label(filter_frame, text="Sales Range:").pack(anchor=tk.W, pady=(0, 5))
        self.sales_var = tk.IntVar(value=0)
        self.sales_slider = ttk.Scale(
            filter_frame,
            from_=0,
            to=50000000,
            orient=tk.HORIZONTAL,
            variable=self.sales_var,
            command=self.updateSales
        )
        self.sales_slider.pack(fill=tk.X, pady=(0, 5))
        
        # Currently selected sales
        self.sales_label = ttk.Label(filter_frame, text="$0")
        self.sales_label.pack(anchor=tk.W)
        
        # Results box
        self.tree = ttk.Treeview(root, columns=(), show='headings')
        self.tree.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=5)
        
        # Scroll bar for results
        scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.grid(row=1, column=2, sticky=(tk.N, tk.S))
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Search button
        ttk.Button(search_frame, text="Search", command=self.performSearch).grid(row=0, column=2, padx=5)
        
        # GUI sizing
        root.columnconfigure(0, weight = 1)  # Filter panel
        root.columnconfigure(1, weight = 4)  # Results box - 80% of screen
        root.rowconfigure(1, weight = 1)

    # Passes query through to database
    def performSearch(self):
        search_term = self.search_var.get()
        sales_limit = self.sales_var.get()
        
        query = """
            SELECT * FROM Game 
            WHERE game_name LIKE ? 
            AND sales <= ?
        """
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (f'%{search_term}%', sales_limit))
            results = cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            self.updateResults(columns, results)
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")

    # Show results as table after query execution
    def updateResults(self, columns, results):
        # Empties results box
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Warning message if no results found
        if not columns or not results:
            messagebox.showinfo("Info", "No results found")
            return
        
        # Create columns
        self.tree['columns'] = columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)  # Sets column width
            
        # Adds data to results box
        for row in results:
            self.tree.insert('', tk.END, values=row)
    
    # Gets sales value from slider
    # Also used for limiting increments
    def updateSales(self, *args):
        # Round for increments of 10000
        value = self.sales_var.get()
        rounded_value = round(value / 10000) * 10000
        self.sales_var.set(rounded_value)
        self.sales_label.config(text=f"${rounded_value:,}")
        # Update results automatically when slider changes
        self.performSearch()

# Opens connection to database
def openConnection(db_name):
    try:
        connection = sqlite3.connect(db_name)
        print("Connected to database successfully.")
        return connection
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def main():
    root = tk.Tk()
    app = DBApplication(root)
    root.mainloop()

if __name__ == "__main__":
    main()
