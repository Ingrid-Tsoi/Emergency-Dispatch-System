# gui.py
import tkinter as tk
from tkinter import ttk, messagebox
from controller import Dispatcher


class EmergencyGUI:
    """
    Graphical User Interface for the Emergency Dispatch System.

    This class provides:
    - Incident reporting interface
    - Incident management (dispatch & resolve)
    - History tracking
    - Unit status monitoring
    """

    def __init__(self, root):
        """
        Initialize the GUI window and core system components.
        """
        self.root = root
        self.root.title("Emergency Dispatch System")

        # Core dispatcher logic handler
        self.dispatcher = Dispatcher()

        # Initialize GUI layout
        self.setup_notebook()
        self.setup_incident_tab()
        self.setup_history_tab()
        self.setup_units_tab()

    # ------------------------------------------------------------
    # Tabs (Notebook)
    # ------------------------------------------------------------
    def setup_notebook(self):
        """
        Create tabbed interface using ttk Notebook.
        """
        self.notebook = ttk.Notebook(self.root)

        # Create tabs
        self.tab_active = ttk.Frame(self.notebook)
        self.tab_history = ttk.Frame(self.notebook)
        self.tab_units = ttk.Frame(self.notebook)

        # Add tabs to notebook
        self.notebook.add(self.tab_active, text="Active Incidents")
        self.notebook.add(self.tab_history, text="Resolved Incidents")
        self.notebook.add(self.tab_units, text="Units Status")

        self.notebook.pack(expand=True, fill="both")

    # ------------------------------------------------------------
    # ACTIVE INCIDENT TAB
    # ------------------------------------------------------------
    def setup_incident_tab(self):
        """
        Build the Active Incidents tab UI:
        - Input fields
        - Incident table
        - Action buttons
        """
        frame = self.tab_active

        # -------------------------
        # Input Section
        # -------------------------

        # Incident Type dropdown
        tk.Label(frame, text="Incident Type").grid(row=0, column=0)
        self.type_combobox = ttk.Combobox(frame, values=[
            "Car Accident", "Fire", "Drowning", "Fall", "Stealing / Theft",
            "Medical Emergency", "Assault", "Gas Leak", "Electrical Hazard"
        ])
        self.type_combobox.grid(row=0, column=1)

        # Location dropdown
        tk.Label(frame, text="Location").grid(row=1, column=0)
        self.loc_combobox = ttk.Combobox(frame, values=[
            "Road", "Building", "Mall", "River", "Stair",
            "Park", "School", "Parking Lot"
        ])
        self.loc_combobox.grid(row=1, column=1)

        # Severity input (1–5)
        tk.Label(frame, text="Severity (1-5)").grid(row=2, column=0)
        self.sev_entry = tk.Entry(frame)
        self.sev_entry.grid(row=2, column=1)

        # Report button
        tk.Button(
            frame,
            text="Report Incident",
            command=self.report_incident
        ).grid(row=3, column=0, columnspan=2)

        # -------------------------
        # Incident Table (TreeView)
        # -------------------------
        columns = ("id", "type", "location", "severity", "status", "unit")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings")

        # Configure table columns
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, anchor="center")

        self.tree.grid(row=4, column=0, columnspan=3)

        # Color tags for severity levels
        self.tree.tag_configure("high", background="#ffb3b3")     # High severity
        self.tree.tag_configure("medium", background="#ffd9b3")   # Medium severity
        self.tree.tag_configure("low", background="#c6f5c6")      # Low severity

        # -------------------------
        # Action Buttons
        # -------------------------
        tk.Button(frame, text="Dispatch Unit",
                  command=self.dispatch_unit).grid(row=5, column=0)

        tk.Button(frame, text="Resolve Incident",
                  command=self.resolve_incident).grid(row=5, column=1)

        tk.Button(frame, text="Sort by Priority",
                  command=self.refresh_incidents).grid(row=5, column=2)

    # ------------------------------------------------------------
    # HISTORY TAB
    # ------------------------------------------------------------
    def setup_history_tab(self):
        """
        Build the Resolved Incidents tab.
        Displays completed incidents.
        """
        frame = self.tab_history

        columns = ("id", "type", "location", "severity", "unit")
        self.tree_history = ttk.Treeview(frame, columns=columns, show="headings")

        for col in columns:
            self.tree_history.heading(col, text=col.capitalize())
            self.tree_history.column(col, anchor="center")

        self.tree_history.pack(fill="both", expand=True)

    # ------------------------------------------------------------
    # UNITS TAB
    # ------------------------------------------------------------
    def setup_units_tab(self):
        """
        Build the Units Status tab.
        Displays all emergency units and their availability.
        """
        frame = self.tab_units

        columns = ("unit", "type", "location", "status")
        self.tree_units = ttk.Treeview(frame, columns=columns, show="headings")

        for col in columns:
            self.tree_units.heading(col, text=col.capitalize())
            self.tree_units.column(col, anchor="center")

        self.tree_units.pack(fill="both", expand=True)

        # Load initial unit data
        self.refresh_units()

    # ------------------------------------------------------------
    # CORE FUNCTIONS
    # ------------------------------------------------------------
    def report_incident(self):
        """
        Handle incident reporting from user input.
        Validates input and updates the UI.
        """
        t = self.type_combobox.get()
        l = self.loc_combobox.get()
        s = self.sev_entry.get()

        try:
            # Convert severity to integer
            s = int(s)

            inc = self.dispatcher.report_incident(t, l, s)

            # If error returned as string
            if isinstance(inc, str):
                messagebox.showerror("Error", inc)
                return

            self.refresh_incidents()

        except:
            messagebox.showerror("Error", "Invalid input (Severity must be 1–5)")

    def dispatch_unit(self):
        """
        Dispatch a unit to the highest priority incident.
        """
        msg = self.dispatcher.dispatch_unit()
        messagebox.showinfo("Dispatch", msg)

        self.refresh_incidents()
        self.refresh_units()

    def resolve_incident(self):
        """
        Resolve the selected incident from the table.
        """
        selected = self.tree.selection()

        # Ensure an item is selected
        if not selected:
            return

        # Extract incident ID from selected row
        inc_id = int(self.tree.item(selected)['values'][0])

        msg = self.dispatcher.resolve_incident(inc_id)

        messagebox.showinfo("Resolved", msg)

        self.refresh_incidents()
        self.refresh_history()
        self.refresh_units()

    # ------------------------------------------------------------
    # REFRESH FUNCTIONS
    # ------------------------------------------------------------
    def refresh_incidents(self):
        """
        Refresh the Active Incidents table.
        Applies color coding based on severity.
        """
        # Clear existing rows
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insert updated incident data
        for inc in self.dispatcher.get_sorted_incidents():

            # Assign color tag based on severity
            tag = "low"
            if inc.severity >= 4:
                tag = "high"
            elif inc.severity >= 2:
                tag = "medium"

            # Get assigned unit (if any)
            unit = inc.assigned_unit.unit_id if inc.assigned_unit else "None"

            self.tree.insert(
                "", "end",
                values=(inc.incident_id, inc.type, inc.location,
                        inc.severity, inc.status, unit),
                tags=(tag,)
            )

    def refresh_history(self):
        """
        Refresh the Resolved Incidents table.
        """
        for item in self.tree_history.get_children():
            self.tree_history.delete(item)

        for inc in self.dispatcher.history:
            unit = inc.assigned_unit.unit_id if inc.assigned_unit else "None"

            self.tree_history.insert(
                "", "end",
                values=(inc.incident_id, inc.type,
                        inc.location, inc.severity, unit)
            )

    def refresh_units(self):
        """
        Refresh the Units Status table.
        Displays availability of each unit.
        """
        for item in self.tree_units.get_children():
            self.tree_units.delete(item)

        for u in self.dispatcher.units:
            status = "Available" if u.available else "Busy"

            self.tree_units.insert(
                "", "end",
                values=(u.unit_id, u.unit_type, u.location, status)
            )