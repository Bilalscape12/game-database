import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

class DBApplication:
    def __init__(self, root):
        self.root = root
        # Program title
        self.root.title("Video Game Searcher")
        self.connection = openConnection("Checkpoint3-dbase.sqlite3")
        
        # Create notebook for multiple tabs/searches
        self.notebook = ttk.Notebook(root)
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create and add tabs
        self.game_search_tab = ttk.Frame(self.notebook)
        self.console_search_tab = ttk.Frame(self.notebook)
        self.developer_search_tab = ttk.Frame(self.notebook)
        self.manage_data_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.game_search_tab, text='Game Search')
        self.notebook.add(self.console_search_tab, text='Console Search')
        self.notebook.add(self.developer_search_tab, text='Developer Search')
        self.notebook.add(self.manage_data_tab, text='Manage Data')
        
        self.gameSearchTab()
        self.consoleSearchTab()
        self.developerSearchTab()
        self.manageDataTab()
        
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

    def gameSearchTab(self):
        # Search frame
        search_frame = ttk.Frame(self.game_search_tab, padding="10")
        search_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        search_frame.columnconfigure(1, weight=1)
        search_frame.columnconfigure(3, weight=1)
        
        # Game name textbox
        ttk.Label(search_frame, text="Game:").grid(row=0, column=0, padx=5)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=25)
        self.search_entry.grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E))
        
        # Console name textbox
        ttk.Label(search_frame, text="Console:").grid(row=0, column=2, padx=5)
        self.consolegame_search_var = tk.StringVar()
        self.consolegame_search_entry = ttk.Entry(search_frame, textvariable=self.consolegame_search_var, width=25)
        self.consolegame_search_entry.grid(row=0, column=3, padx=5, sticky=(tk.W, tk.E))
        
        # Leftside panel
        filter_frame = ttk.LabelFrame(self.game_search_tab, text="Filters", padding="10")
        filter_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=5)
        
        # Sales slider
        ttk.Label(filter_frame, text="Sales Range:").pack(anchor=tk.W, pady=(0, 5))
        self.sales_var = tk.IntVar(value=0)
        self.sales_slider = ttk.Scale(
            filter_frame,
            from_=0, # Min value
            to=50000000, # Max value
            orient=tk.HORIZONTAL,
            variable=self.sales_var,
            command=self.updateSales
        )
        self.sales_slider.pack(fill=tk.X, pady=(0, 5))
        self.sales_label = ttk.Label(filter_frame, text="0")
        self.sales_label.pack(anchor=tk.W)
        
        # Sorting options
        sort_frame = ttk.LabelFrame(filter_frame, text="Sort By", padding="5")
        sort_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.sort_var = tk.StringVar(value="none")
        ttk.Radiobutton(sort_frame, text="None", variable=self.sort_var, value="none").pack(anchor=tk.W)
        ttk.Radiobutton(sort_frame, text="Name (A-Z)", variable=self.sort_var, value="name_asc").pack(anchor=tk.W)
        ttk.Radiobutton(sort_frame, text="Name (Z-A)", variable=self.sort_var, value="name_desc").pack(anchor=tk.W)
        ttk.Radiobutton(sort_frame, text="Date (Oldest)", variable=self.sort_var, value="date_asc").pack(anchor=tk.W)
        ttk.Radiobutton(sort_frame, text="Date (Newest)", variable=self.sort_var, value="date_desc").pack(anchor=tk.W)
        
        # Results tree
        self.game_tree = ttk.Treeview(self.game_search_tab, columns=(), show='headings')
        self.game_tree.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=5)
        
        # Scrollbar for results
        scrollbar = ttk.Scrollbar(self.game_search_tab, orient=tk.VERTICAL, command=self.game_tree.yview)
        scrollbar.grid(row=1, column=2, sticky=(tk.N, tk.S))
        self.game_tree.configure(yscrollcommand=scrollbar.set)
        
        # Search button
        ttk.Button(search_frame, text="Search", command=self.performGameSearch).grid(row=0, column=4, padx=5)
        
        self.game_search_tab.columnconfigure(1, weight=4)
        self.game_search_tab.rowconfigure(1, weight=1)

    def consoleSearchTab(self):
        # Search frame
        search_frame = ttk.Frame(self.console_search_tab, padding="10")
        search_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        search_frame.columnconfigure(1, weight=1)
        
        # Console name textbox
        ttk.Label(search_frame, text="Console:").grid(row=0, column=0, padx=5)
        self.console_search_var = tk.StringVar()
        self.console_search_entry = ttk.Entry(search_frame, textvariable=self.console_search_var, width=50)
        self.console_search_entry.grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E))
        
        # Leftside panel
        filter_frame = ttk.LabelFrame(self.console_search_tab, text="Filters", padding="10")
        filter_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=5)
        
        # Sales slider
        ttk.Label(filter_frame, text="Sales Range:").pack(anchor=tk.W, pady=(0, 5))
        self.console_sales_var = tk.IntVar(value=0)
        self.console_sales_slider = ttk.Scale(
            filter_frame,
            from_=0, # Min value
            to=500000000, # Max value
            orient=tk.HORIZONTAL,
            variable=self.console_sales_var,
            command=self.updateConsoleSales
        )
        self.console_sales_slider.pack(fill=tk.X, pady=(0, 5))
        self.console_sales_label = ttk.Label(filter_frame, text="0")
        self.console_sales_label.pack(anchor=tk.W)
        
        # Sorting options
        sort_frame = ttk.LabelFrame(filter_frame, text="Sort By", padding="5")
        sort_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.console_sort_var = tk.StringVar(value="none")
        ttk.Radiobutton(sort_frame, text="None", variable=self.console_sort_var, value="none").pack(anchor=tk.W)
        ttk.Radiobutton(sort_frame, text="Name (A-Z)", variable=self.console_sort_var, value="name_asc").pack(anchor=tk.W)
        ttk.Radiobutton(sort_frame, text="Name (Z-A)", variable=self.console_sort_var, value="name_desc").pack(anchor=tk.W)
        ttk.Radiobutton(sort_frame, text="Date (Oldest)", variable=self.console_sort_var, value="date_asc").pack(anchor=tk.W)
        ttk.Radiobutton(sort_frame, text="Date (Newest)", variable=self.console_sort_var, value="date_desc").pack(anchor=tk.W)
        
        # Results tree
        self.console_tree = ttk.Treeview(self.console_search_tab, columns=(), show='headings')
        self.console_tree.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=5)
        
        # Scrollbar for results
        scrollbar = ttk.Scrollbar(self.console_search_tab, orient=tk.VERTICAL, command=self.console_tree.yview)
        scrollbar.grid(row=1, column=2, sticky=(tk.N, tk.S))
        self.console_tree.configure(yscrollcommand=scrollbar.set)
        
        # Search button
        ttk.Button(search_frame, text="Search", command=self.performConsoleSearch).grid(row=0, column=2, padx=5)
        
        self.console_search_tab.columnconfigure(1, weight=4)
        self.console_search_tab.rowconfigure(1, weight=1)
        
    def developerSearchTab(self):
        # Search frame
        search_frame = ttk.Frame(self.developer_search_tab, padding="10")
        search_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        search_frame.columnconfigure(1, weight=1)
        search_frame.columnconfigure(3, weight=1)
        
        # Developer name textbox
        ttk.Label(search_frame, text="Developer:").grid(row=0, column=0, padx=5)
        self.dev_search_var = tk.StringVar()
        self.dev_search_entry = ttk.Entry(search_frame, textvariable=self.dev_search_var, width=25)
        self.dev_search_entry.grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E))
        
        # Game name textbox
        ttk.Label(search_frame, text="Game:").grid(row=0, column=2, padx=5)
        self.dev_game_search_var = tk.StringVar()
        self.dev_game_search_entry = ttk.Entry(search_frame, textvariable=self.dev_game_search_var, width=25)
        self.dev_game_search_entry.grid(row=0, column=3, padx=5, sticky=(tk.W, tk.E))
        
        # Leftside panel
        filter_frame = ttk.LabelFrame(self.developer_search_tab, text="Filters", padding="10")
        filter_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=5)
        
        # Sorting options
        sort_frame = ttk.LabelFrame(filter_frame, text="Sort By", padding="5")
        sort_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.dev_sort_var = tk.StringVar(value="none")
        ttk.Radiobutton(sort_frame, text="None", variable=self.dev_sort_var, value="none").pack(anchor=tk.W)
        ttk.Radiobutton(sort_frame, text="Developer Name (A-Z)", variable=self.dev_sort_var, value="dev_asc").pack(anchor=tk.W)
        ttk.Radiobutton(sort_frame, text="Developer Name (Z-A)", variable=self.dev_sort_var, value="dev_desc").pack(anchor=tk.W)
        ttk.Radiobutton(sort_frame, text="Game Name (A-Z)", variable=self.dev_sort_var, value="game_asc").pack(anchor=tk.W)
        ttk.Radiobutton(sort_frame, text="Game Name (Z-A)", variable=self.dev_sort_var, value="game_desc").pack(anchor=tk.W)
        
        # Results tree
        self.dev_tree = ttk.Treeview(self.developer_search_tab, columns=(), show='headings')
        self.dev_tree.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=5)
        
        # Scrollbar for results
        scrollbar = ttk.Scrollbar(self.developer_search_tab, orient=tk.VERTICAL, command=self.dev_tree.yview)
        scrollbar.grid(row=1, column=2, sticky=(tk.N, tk.S))
        self.dev_tree.configure(yscrollcommand=scrollbar.set)
        
        # Search button
        ttk.Button(search_frame, text="Search", command=self.performDeveloperSearch).grid(row=0, column=4, padx=5)
        
        self.developer_search_tab.columnconfigure(1, weight=4)
        self.developer_search_tab.rowconfigure(1, weight=1)

    def manageDataTab(self):
        # Create a nested notebook for different tables
        manage_notebook = ttk.Notebook(self.manage_data_tab)
        manage_notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=5)
        
        # Create tabs for each table
        game_frame = ttk.Frame(manage_notebook)
        console_frame = ttk.Frame(manage_notebook)
        publisher_frame = ttk.Frame(manage_notebook)
        developer_frame = ttk.Frame(manage_notebook)
        franchise_frame = ttk.Frame(manage_notebook)
        accessory_frame = ttk.Frame(manage_notebook)
        console_accessories_frame = ttk.Frame(manage_notebook)
        game_accessories_frame = ttk.Frame(manage_notebook)
        developer_games_frame = ttk.Frame(manage_notebook)
        publisher_games_frame = ttk.Frame(manage_notebook)
        franchise_games_frame = ttk.Frame(manage_notebook)
        game_languages_frame = ttk.Frame(manage_notebook)
        region_games_frame = ttk.Frame(manage_notebook)
        
        # Add frames to notebook
        manage_notebook.add(game_frame, text='Games')
        manage_notebook.add(console_frame, text='Consoles')
        manage_notebook.add(publisher_frame, text='Publishers')
        manage_notebook.add(developer_frame, text='Developers')
        manage_notebook.add(franchise_frame, text='Franchises')
        manage_notebook.add(accessory_frame, text='Accessories')
        manage_notebook.add(console_accessories_frame, text='Console Accessories')
        manage_notebook.add(game_accessories_frame, text='Game Accessories')
        manage_notebook.add(developer_games_frame, text='Developer Games')
        manage_notebook.add(publisher_games_frame, text='Publisher Games')
        manage_notebook.add(franchise_games_frame, text='Franchise Games')
        manage_notebook.add(game_languages_frame, text='Game Languages')
        manage_notebook.add(region_games_frame, text='Region Games')
        
        # Create entry widgets for each table tab
        self.entry_widgets = {
            'Game': self.createTableSection(game_frame, 'Game'),
            'Console': self.createTableSection(console_frame, 'Console'),
            'Publisher': self.createTableSection(publisher_frame, 'Publisher'),
            'Developer': self.createTableSection(developer_frame, 'Developer'),
            'Franchise': self.createTableSection(franchise_frame, 'Franchise'),
            'Accessory': self.createTableSection(accessory_frame, 'Accessory'),
            'ConsoleAccessories': self.createTableSection(console_accessories_frame, 'ConsoleAccessories'),
            'GameAccessories': self.createTableSection(game_accessories_frame, 'GameAccessories'),
            'DeveloperGames': self.createTableSection(developer_games_frame, 'DeveloperGames'),
            'PublisherGames': self.createTableSection(publisher_games_frame, 'PublisherGames'),
            'FranchiseGames': self.createTableSection(franchise_games_frame, 'FranchiseGames'),
            'GameLanguages': self.createTableSection(game_languages_frame, 'GameLanguages'),
            'RegionGames': self.createTableSection(region_games_frame, 'RegionGames')
        }
        
        self.manage_data_tab.columnconfigure(0, weight=1)
        self.manage_data_tab.rowconfigure(0, weight=1)

    def createTableSection(self, parent, table_name):
        # Data entry frame
        entry_frame = ttk.LabelFrame(parent, text="Data Entry", padding="10")
        entry_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=10, pady=5)
        
        # Get table structure using PRAGMA
        cursor = self.connection.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        entry_widgets = {}
        
        # Create entry fields for each column
        for i, col in enumerate(columns):
            name = col[1]
            ttk.Label(entry_frame, text=f"{name}:").grid(row=i, column=0, padx=5, pady=2, sticky=tk.W)
            entry = ttk.Entry(entry_frame)
            entry.grid(row=i, column=1, padx=5, pady=2, sticky=(tk.W, tk.E))
            entry_widgets[name] = entry
        
        # Buttons frame
        button_frame = ttk.Frame(parent, padding="10")
        button_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=10, pady=5)
        
        ttk.Button(
            button_frame, 
            text="Insert", 
            command=lambda t=table_name, e=entry_widgets: self.insertRecord(t, e)
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="Update", 
            command=lambda t=table_name, e=entry_widgets: self.updateRecord(t, e)
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="Delete", 
            command=lambda t=table_name, e=entry_widgets: self.deleteRecord(t, e)
        ).pack(side=tk.LEFT, padx=5)
        
        # Clears text from boxes
        ttk.Button(
            button_frame, 
            text="Clear", 
            command=lambda e=entry_widgets: self.clearEntries(e)
        ).pack(side=tk.LEFT, padx=5)
        
        return entry_widgets

    # Tab for searching Games
    def performGameSearch(self):
        search_term = self.search_var.get()
        console_term = self.consolegame_search_var.get()
        sales_limit = self.sales_var.get()
        sort_option = self.sort_var.get()
        
        query = """
            SELECT * FROM Game 
            WHERE (game_name LIKE ? OR ? = '')
            AND (console_name LIKE ? OR ? = '')
            AND (sales <= ? OR sales IS NULL OR sales = '' OR ? = 0)
        """
        
        # Add ORDER BY based on sort option
        if sort_option == "name_asc":
            query += " ORDER BY game_name ASC"
        elif sort_option == "name_desc":
            query += " ORDER BY game_name DESC"
        elif sort_option == "date_asc":
            query += " ORDER BY release_date ASC"
        elif sort_option == "date_desc":
            query += " ORDER BY release_date DESC"
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (
                f'%{search_term}%', search_term,
                f'%{console_term}%', console_term,
                sales_limit, sales_limit
            ))
            results = cursor.fetchall()
            columns = ["Game", "Console", "Release Date", "Genre", "Sales", "Sequel Game", "Sequel Console"]
            self.updateResults(self.game_tree, columns, results)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {str(e)}")

    # Tab for searching Consoles
    def performConsoleSearch(self):
        search_term = self.console_search_var.get()
        sales_limit = self.console_sales_var.get()
        sort_option = self.console_sort_var.get()
        
        query = """
            SELECT * FROM Console 
            WHERE (console_name LIKE ? OR ? = '')
            AND (sales <= ? OR sales IS NULL OR sales = '' OR ? = 0)
        """
        
        # Add ORDER BY based on sort option
        if sort_option == "name_asc":
            query += " ORDER BY console_name ASC"
        elif sort_option == "name_desc":
            query += " ORDER BY console_name DESC"
        elif sort_option == "date_asc":
            query += " ORDER BY release_date ASC"
        elif sort_option == "date_desc":
            query += " ORDER BY release_date DESC"
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (f'%{search_term}%', search_term, sales_limit, sales_limit))
            results = cursor.fetchall()
            columns = ["Console", "Developer", "Release Date", "Handheld (1 = True, 0 = False)", "Bit-size", "Sales"]
            self.updateResults(self.console_tree, columns, results)
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")

    # Tab for searching Developers and the games they developed
    def performDeveloperSearch(self):
        dev_term = self.dev_search_var.get()
        game_term = self.dev_game_search_var.get()
        sort_option = self.dev_sort_var.get()
        
        query = """
            SELECT DISTINCT 
                dg.developer_name,
                d.date_founded,
                dg.game_name,
                dg.console_name,
                g.release_date,
                g.genre,
                g.sales
            FROM Developer d
            JOIN DeveloperGames dg ON d.developer_name = dg.developer_name
            JOIN Game g ON dg.game_name = g.game_name AND dg.console_name = g.console_name
            WHERE (d.developer_name LIKE ? OR ? = '')
            AND (g.game_name LIKE ? OR ? = '')
        """
        
        # Add ORDER BY based on sort option
        if sort_option == "dev_asc":
            query += " ORDER BY dg.developer_name ASC"
        elif sort_option == "dev_desc":
            query += " ORDER BY dg.developer_name DESC"
        elif sort_option == "game_asc":
            query += " ORDER BY dg.game_name ASC"
        elif sort_option == "game_desc":
            query += " ORDER BY dg.game_name DESC"
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (
                f'%{dev_term}%', dev_term,
                f'%{game_term}%', game_term
            ))
            results = cursor.fetchall()
            columns = ["Developer", "Date Founded", "Game", "Console", "Release Date", "Genre", "Sales"]
            self.updateResults(self.dev_tree, columns, results)
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")

    # Updates the results tree
    def updateResults(self, tree, columns, results):
        for item in tree.get_children():
            tree.delete(item)
        
        if not columns or not results:
            messagebox.showinfo("Info", "No results found")
            return
        
        tree['columns'] = columns
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
            
        for row in results:
            tree.insert('', tk.END, values=row)
    
    # Updates the sales label in increments of 10,000
    def updateSales(self, *args):
        value = self.sales_var.get()
        rounded_value = round(value / 10000) * 10000 # Increments of 10,000
        self.sales_var.set(rounded_value)
        self.sales_label.config(text=f"{rounded_value:,}")
    # TODO: redundant code
    def updateConsoleSales(self, *args):
        value = self.console_sales_var.get()
        rounded_value = round(value / 100000) * 100000 # Increments of 100,000
        self.console_sales_var.set(rounded_value)
        self.console_sales_label.config(text=f"{rounded_value:,}")
        
    # Row insertion
    def insertRecord(self, table, entry_widgets):
        values = {name: widget.get() for name, widget in entry_widgets.items()}
        
        columns = ", ".join(values.keys())
        placeholders = ", ".join(["?" for _ in values])
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, list(values.values()))
            self.connection.commit()
            messagebox.showinfo("Success", "Record inserted successfully")
            self.clearEntries(entry_widgets)
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")

    # Row update
    def updateRecord(self, table, entry_widgets):
        values = {name: widget.get() for name, widget in entry_widgets.items()}
        id_column = list(values.keys())[0] # First column
        id_value = values[id_column]
        
        # Remove ID from update values
        del values[id_column]
        
        set_clause = ", ".join([f"{name} = ?" for name in values.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {id_column} = ?"
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, list(values.values()) + [id_value])
            self.connection.commit()
            if cursor.rowcount > 0:
                messagebox.showinfo("Success", "Record updated successfully")
            else:
                messagebox.showwarning("Warning", "Record not found")
            self.clearEntries(entry_widgets)
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")

    # Row deletion
    def deleteRecord(self, table, entry_widgets):
        id_column = list(entry_widgets.keys())[0]  # First column
        id_value = entry_widgets[id_column].get()
        # If ID is empty
        if not id_value:
            messagebox.showwarning("Warning", f"Please enter {id_column} to delete")
            return
        
        if messagebox.askyesno("Confirm Delete", "Confirm deletion?"):
            try:
                cursor = self.connection.cursor()
                cursor.execute(f"DELETE FROM {table} WHERE {id_column} = ?", [id_value])
                self.connection.commit()
                if cursor.rowcount > 0:
                    messagebox.showinfo("Success", "Record deleted successfully")
                else:
                    messagebox.showwarning("Warning", "No matching record found")
                self.clearEntries(entry_widgets)
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Database error: {e}")

    # Clears all entries
    def clearEntries(self, entry_widgets):
        for entry in entry_widgets.values():
            entry.delete(0, tk.END)

# Opens connection to database
def openConnection(db_name):
    try:
        connection = sqlite3.connect(db_name)
        print(f"Successfully connected to database {db_name}")
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
