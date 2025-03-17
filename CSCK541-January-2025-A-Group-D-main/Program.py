"""
Main module for the Travel Record Management System with a Tkinter-based user interface.
This application provides functionality to manage client, airline, and flight records.
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime

# Adjust system path to include the parent directory for imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from src.data_manager import DataManager
from src.models import ClientRecord, AirlineRecord, FlightRecord, RecordType


class RecordManagementApp:
    """A Tkinter application for managing travel-related records."""

    def __init__(self, root):
        """
        Initialises the RecordManagementApp with a Tkinter root window.

        Args:
            root (tk.Tk): The main Tkinter window instance.
        """
        self.root = root
        self.root.title("Travel Record Management System - CSK541-JANUARY-2025-A-GROUP-D")
        self.data_manager = DataManager()

        # Attempt to load existing data; warn if unsuccessful
        if not self.data_manager.load_data():
            messagebox.showwarning("Warning", "Failed to load data. Starting with an empty database.")

        # Set up the notebook (tabbed interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, expand=True, fill="both")

        # Define tabs
        self.instruction_tab = ttk.Frame(self.notebook)
        self.view_tab = ttk.Frame(self.notebook)
        self.add_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.instruction_tab, text="Instructions")
        self.notebook.add(self.view_tab, text="View Records")
        self.notebook.add(self.add_tab, text="Add Record")

        # Initialise tab contents
        self.setup_instruction_tab()
        self.setup_view_tab()
        self.setup_add_tab()

    def setup_instruction_tab(self):
        """Configures the Instructions tab with usage information."""
        frame = ttk.Frame(self.instruction_tab)
        frame.pack(padx=10, pady=10, fill="both", expand=True)

        instruction_text = (
            "Welcome to the Travel Record Management System!\n\n"
            "How to Use:\n"
            "1. Add Record Tab:\n"
            "   - Select 'Client', 'Airline', or 'Flight' from the left panel.\n"
            "   - Complete the form on the right and click 'Add' to create a new record.\n"
            "   - Client and Airline names must be unique; IDs are assigned automatically.\n\n"
            "2. View Records Tab:\n"
            "   - Click 'View Clients', 'View Airlines', or 'View Flights' on the left.\n"
            "   - Records are displayed in a table on the right.\n"
            "   - Use the search field to filter by ID or Name.\n"
            "   - Double-click a record to view its details.\n"
            "   - In the details window:\n"
            "     - Click 'Edit' to amend fields (ID cannot be changed).\n"
            "     - Click 'Save' to update the record.\n"
            "     - Click 'Delete' to remove the record (requires confirmation; Clients/Airlines cannot be deleted if linked to a Flight).\n\n"
            "Notes:\n"
            "- All fields are mandatory when adding records.\n"
            "- Flight records use dropdown menus to select existing Clients and Airlines.\n"
            "- Data is stored in 'record.json' within the 'src/record' directory."
        )

        ttk.Label(frame, text=instruction_text, justify="left", wraplength=680, anchor="nw").pack(
            side="top", fill="both", expand=True
        )

    def setup_view_tab(self):
        """Sets up the View Records tab with buttons and a table frame."""
        frame = ttk.Frame(self.view_tab)
        frame.pack(padx=10, pady=10, fill="both", expand=True)

        paned_window = ttk.PanedWindow(frame, orient=tk.HORIZONTAL)
        paned_window.pack(fill="both", expand=True)

        left_panel = ttk.Frame(paned_window)
        paned_window.add(left_panel, weight=1)

        ttk.Label(left_panel, text="Select Record Type:").pack(pady=5)
        ttk.Button(left_panel, text="View Clients", command=lambda: self.show_records(RecordType.CLIENT)).pack(
            pady=5, fill="x"
        )
        ttk.Button(left_panel, text="View Airlines", command=lambda: self.show_records(RecordType.AIRLINE)).pack(
            pady=5, fill="x"
        )
        ttk.Button(left_panel, text="View Flights", command=lambda: self.show_records(RecordType.FLIGHT)).pack(
            pady=5, fill="x"
        )

        self.table_frame = ttk.Frame(paned_window)
        paned_window.add(self.table_frame, weight=3)

    def setup_add_tab(self):
        """Configures the Add Record tab with buttons and a form frame."""
        frame = ttk.Frame(self.add_tab)
        frame.pack(padx=10, pady=10, fill="both", expand=True)

        paned_window = ttk.PanedWindow(frame, orient=tk.HORIZONTAL)
        paned_window.pack(fill="both", expand=True)

        left_panel = ttk.Frame(paned_window)
        paned_window.add(left_panel, weight=1)

        ttk.Label(left_panel, text="Select Record Type to Add:").pack(pady=5)
        ttk.Button(left_panel, text="Add Client", command=lambda: self.show_add_form("client")).pack(pady=5, fill="x")
        ttk.Button(left_panel, text="Add Airline", command=lambda: self.show_add_form("airline")).pack(pady=5, fill="x")
        ttk.Button(left_panel, text="Add Flight", command=lambda: self.show_add_form("flight")).pack(pady=5, fill="x")

        self.add_form_frame = ttk.Frame(paned_window)
        paned_window.add(self.add_form_frame, weight=3)

    def show_add_form(self, form_type):
        """
        Displays the appropriate form for adding a record based on type.

        Args:
            form_type (str): The type of record form to display ('client', 'airline', 'flight').
        """
        for widget in self.add_form_frame.winfo_children():
            widget.destroy()

        if form_type == "client":
            self.setup_client_form(self.add_form_frame)
        elif form_type == "airline":
            self.setup_airline_form(self.add_form_frame)
        elif form_type == "flight":
            self.setup_flight_form(self.add_form_frame)

    def setup_client_form(self, frame):
        """Sets up the form for adding a new client record."""
        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        form_frame = ttk.Frame(canvas)

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        canvas.create_window((0, 0), window=form_frame, anchor="nw")
        form_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        ttk.Label(form_frame, text="Name:").grid(row=0, column=0, padx=5, pady=2, sticky="e")
        self.client_name = ttk.Entry(form_frame, width=30)
        self.client_name.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(form_frame, text="Address Line 1:").grid(row=1, column=0, padx=5, pady=2, sticky="e")
        self.client_addr1 = ttk.Entry(form_frame, width=30)
        self.client_addr1.grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(form_frame, text="Address Line 2:").grid(row=2, column=0, padx=5, pady=2, sticky="e")
        self.client_addr2 = ttk.Entry(form_frame, width=30)
        self.client_addr2.grid(row=2, column=1, padx=5, pady=2)

        ttk.Label(form_frame, text="Address Line 3:").grid(row=3, column=0, padx=5, pady=2, sticky="e")
        self.client_addr3 = ttk.Entry(form_frame, width=30)
        self.client_addr3.grid(row=3, column=1, padx=5, pady=2)

        ttk.Label(form_frame, text="City:").grid(row=4, column=0, padx=5, pady=2, sticky="e")
        self.client_city = ttk.Entry(form_frame, width=30)
        self.client_city.grid(row=4, column=1, padx=5, pady=2)

        ttk.Label(form_frame, text="County/State:").grid(row=5, column=0, padx=5, pady=2, sticky="e")
        self.client_state = ttk.Entry(form_frame, width=30)
        self.client_state.grid(row=5, column=1, padx=5, pady=2)

        ttk.Label(form_frame, text="Postcode:").grid(row=6, column=0, padx=5, pady=2, sticky="e")
        self.client_zip = ttk.Entry(form_frame, width=30)
        self.client_zip.grid(row=6, column=1, padx=5, pady=2)

        ttk.Label(form_frame, text="Country:").grid(row=7, column=0, padx=5, pady=2, sticky="e")
        self.client_country = ttk.Entry(form_frame, width=30)
        self.client_country.grid(row=7, column=1, padx=5, pady=2)

        ttk.Label(form_frame, text="Telephone Number:").grid(row=8, column=0, padx=5, pady=2, sticky="e")
        self.client_phone = ttk.Entry(form_frame, width=30)
        self.client_phone.grid(row=8, column=1, padx=5, pady=2)

        ttk.Button(form_frame, text="Add", command=self.add_client).grid(row=9, column=1, pady=5)

    def setup_airline_form(self, frame):
        """Sets up the form for adding a new airline record."""
        form_frame = ttk.Frame(frame)
        form_frame.pack(padx=10, pady=10, fill="both", expand=True)

        ttk.Label(form_frame, text="Company Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.airline_name = ttk.Entry(form_frame, width=30)
        self.airline_name.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(form_frame, text="Add", command=self.add_airline).grid(row=1, column=1, pady=10)

    def setup_flight_form(self, frame):
        """Sets up the form for adding a new flight record."""
        form_frame = ttk.Frame(frame)
        form_frame.pack(padx=10, pady=10, fill="both", expand=True)

        input_width = 30

        # Client dropdown
        ttk.Label(form_frame, text="Client:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        clients = self.data_manager.get_all_records(RecordType.CLIENT)
        self.client_name_to_id = {f"{record.name}": record.id for record in clients}
        client_names = list(self.client_name_to_id.keys())
        client_names.sort()
        self.flight_client_combo = ttk.Combobox(form_frame, values=client_names, state="readonly", width=input_width - 2)
        self.flight_client_combo.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        if client_names:
            self.flight_client_combo.set(client_names[0])

        # Airline dropdown
        ttk.Label(form_frame, text="Airline:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        airlines = self.data_manager.get_all_records(RecordType.AIRLINE)
        self.airline_name_to_id = {f"{record.company_name}": record.id for record in airlines}
        airline_names = list(self.airline_name_to_id.keys())
        airline_names.sort()
        self.flight_airline_combo = ttk.Combobox(form_frame, values=airline_names, state="readonly", width=input_width - 2)
        self.flight_airline_combo.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        if airline_names:
            self.flight_airline_combo.set(airline_names[0])

        # Date picker
        ttk.Label(form_frame, text="Date:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.flight_date = DateEntry(form_frame, width=input_width - 2, date_pattern="yyyy-mm-dd")
        self.flight_date.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.flight_date.set_date(datetime.now())

        # Time selector
        ttk.Label(form_frame, text="Time:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        time_frame = ttk.Frame(form_frame)
        time_frame.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        self.flight_hour = ttk.Combobox(time_frame, width=5, values=[f"{h:02d}" for h in range(24)], state="readonly")
        self.flight_hour.pack(side="left")
        self.flight_hour.set("12")
        ttk.Label(time_frame, text=":").pack(side="left", padx=2)
        self.flight_minute = ttk.Combobox(time_frame, width=5, values=[f"{m:02d}" for m in range(0, 60, 5)], state="readonly")
        self.flight_minute.pack(side="left")
        self.flight_minute.set("00")

        # Start City
        ttk.Label(form_frame, text="Departure City:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.flight_start = ttk.Entry(form_frame, width=input_width)
        self.flight_start.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        # End City
        ttk.Label(form_frame, text="Destination City:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.flight_end = ttk.Entry(form_frame, width=input_width)
        self.flight_end.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        ttk.Button(form_frame, text="Add", command=self.add_flight).grid(row=6, column=1, pady=10, sticky="w")

    def show_records(self, record_type):
        """
        Displays records of the specified type in a table with search functionality.

        Args:
            record_type (RecordType): The type of records to display (CLIENT, AIRLINE, FLIGHT).
        """
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        search_frame = ttk.Frame(self.table_frame)
        search_frame.pack(fill="x", pady=5)
        ttk.Label(search_frame, text="Search by ID/Name:").pack(side="left", padx=5)
        search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=search_var)
        search_entry.pack(side="left", fill="x", expand=True, padx=5)

        tree_frame = ttk.Frame(self.table_frame)
        tree_frame.pack(fill="both", expand=True)
        tree_scroll = ttk.Scrollbar(tree_frame, orient="vertical")

        if record_type == RecordType.CLIENT:
            columns = ("ID", "Name", "Country", "Telephone")
            self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", yscrollcommand=tree_scroll.set)
            self.tree.heading("ID", text="ID")
            self.tree.column("ID", width=50, stretch=True)
            self.tree.heading("Name", text="Name")
            self.tree.column("Name", width=150, stretch=True)
            self.tree.heading("Country", text="Country")
            self.tree.column("Country", width=100, stretch=True)
            self.tree.heading("Telephone", text="Telephone")
            self.tree.column("Telephone", width=120, stretch=True)
        elif record_type == RecordType.AIRLINE:
            columns = ("ID", "Company Name")
            self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", yscrollcommand=tree_scroll.set)
            self.tree.heading("ID", text="ID")
            self.tree.column("ID", width=50, stretch=True)
            self.tree.heading("Company Name", text="Company Name")
            self.tree.column("Company Name", width=250, stretch=True)
        else:  # FLIGHT
            columns = ("ID", "Client Name", "Airline Name", "Departure City", "Destination City", "Departure Time")
            self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", yscrollcommand=tree_scroll.set)
            self.tree.heading("ID", text="ID")
            self.tree.column("ID", width=50, stretch=True)
            self.tree.heading("Client Name", text="Client Name")
            self.tree.column("Client Name", width=150, stretch=True)
            self.tree.heading("Airline Name", text="Airline Name")
            self.tree.column("Airline Name", width=150, stretch=True)
            self.tree.heading("Departure City", text="Departure City")
            self.tree.column("Departure City", width=100, stretch=True)
            self.tree.heading("Destination City", text="Destination City")
            self.tree.column("Destination City", width=100, stretch=True)
            self.tree.heading("Departure Time", text="Departure Time")
            self.tree.column("Departure Time", width=150, stretch=True)

        tree_scroll.config(command=self.tree.yview)
        tree_scroll.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        self.tree.bind("<Double-1>", lambda event: self.show_details(record_type))

        def filter_records(*args):
            """Filters displayed records based on the search input."""
            search_text = search_var.get().lower()
            for item in self.tree.get_children():
                self.tree.delete(item)

            clients = {rec.id: rec.name for rec in self.data_manager.get_all_records(RecordType.CLIENT)}
            airlines = {rec.id: rec.company_name for rec in self.data_manager.get_all_records(RecordType.AIRLINE)}

            for record in self.data_manager.get_all_records(record_type):
                if record_type == RecordType.CLIENT:
                    if search_text in str(record.id) or search_text in record.name.lower():
                        self.tree.insert("", "end", values=(record.id, record.name, record.country, record.phone_number))
                elif record_type == RecordType.AIRLINE:
                    if search_text in str(record.id) or search_text in record.company_name.lower():
                        self.tree.insert("", "end", values=(record.id, record.company_name))
                else:  # FLIGHT
                    client_name = clients.get(record.client_id, f"Unknown (ID: {record.client_id})")
                    airline_name = airlines.get(record.airline_id, f"Unknown (ID: {record.airline_id})")
                    departure_time = record.date.strftime("%Y-%m-%d %H:%M")
                    if (search_text in str(record.id) or
                            search_text in client_name.lower() or
                            search_text in airline_name.lower() or
                            search_text in record.start_city.lower() or
                            search_text in record.end_city.lower()):
                        self.tree.insert("", "end", values=(
                            record.id,
                            client_name,
                            airline_name,
                            record.start_city,
                            record.end_city,
                            departure_time
                        ))

        search_var.trace("w", filter_records)
        filter_records()

    def show_details(self, record_type):
        """
        Displays detailed information about a selected record in a new window.

        Args:
            record_type (RecordType): The type of record to display details for.
        """
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        record_id = int(item["values"][0])
        record = self.data_manager.get_record(record_id, record_type)
        if not record:
            return

        details_window = tk.Toplevel(self.root)
        details_window.title(f"{record_type.capitalize()} Details - ID: {record_id}")
        details_window.geometry("400x500")

        canvas = tk.Canvas(details_window)
        scrollbar = ttk.Scrollbar(details_window, orient="vertical", command=canvas.yview)
        frame = ttk.Frame(canvas)

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        canvas.create_window((0, 0), window=frame, anchor="nw")
        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        entries = {}
        input_width = 30

        if record_type == RecordType.CLIENT:
            fields = [
                ("ID", record.id),
                ("Name", record.name),
                ("Address Line 1", record.address_line_1),
                ("Address Line 2", record.address_line_2),
                ("Address Line 3", record.address_line_3),
                ("City", record.city),
                ("County/State", record.state),
                ("Postcode", record.zip_code),
                ("Country", record.country),
                ("Telephone Number", record.phone_number)
            ]
            for i, (label, value) in enumerate(fields):
                ttk.Label(frame, text=f"{label}:").grid(row=i, column=0, padx=5, pady=2, sticky="e")
                entry = ttk.Entry(frame, width=input_width)
                entry.insert(0, value)
                entry.config(state="disabled")
                entry.grid(row=i, column=1, padx=5, pady=2)
                entries[label] = entry
        elif record_type == RecordType.AIRLINE:
            fields = [("ID", record.id), ("Company Name", record.company_name)]
            for i, (label, value) in enumerate(fields):
                ttk.Label(frame, text=f"{label}:").grid(row=i, column=0, padx=5, pady=2, sticky="e")
                entry = ttk.Entry(frame, width=input_width)
                entry.insert(0, value)
                entry.config(state="disabled")
                entry.grid(row=i, column=1, padx=5, pady=2)
                entries[label] = entry
        else:  # FLIGHT
            ttk.Label(frame, text="Client:").grid(row=0, column=0, padx=5, pady=2, sticky="e")
            clients = self.data_manager.get_all_records(RecordType.CLIENT)
            self.client_name_to_id = {f"{record.name}": record.id for record in clients}
            client_names = list(self.client_name_to_id.keys())
            client_names.sort()
            self.flight_client_combo = ttk.Combobox(frame, values=client_names, state="disabled", width=input_width - 2)
            current_client = next((name for name, id_ in self.client_name_to_id.items() if id_ == record.client_id),
                                  client_names[0] if client_names else "")
            self.flight_client_combo.set(current_client)
            self.flight_client_combo.grid(row=0, column=1, padx=5, pady=2, sticky="w")
            entries["Client"] = self.flight_client_combo

            ttk.Label(frame, text="Airline:").grid(row=1, column=0, padx=5, pady=2, sticky="e")
            airlines = self.data_manager.get_all_records(RecordType.AIRLINE)
            self.airline_name_to_id = {f"{record.company_name}": record.id for record in airlines}
            airline_names = list(self.airline_name_to_id.keys())
            airline_names.sort()
            self.flight_airline_combo = ttk.Combobox(frame, values=airline_names, state="disabled", width=input_width - 2)
            current_airline = next((name for name, id_ in self.airline_name_to_id.items() if id_ == record.airline_id),
                                   airline_names[0] if airline_names else "")
            self.flight_airline_combo.set(current_airline)
            self.flight_airline_combo.grid(row=1, column=1, padx=5, pady=2, sticky="w")
            entries["Airline"] = self.flight_airline_combo

            ttk.Label(frame, text="Date:").grid(row=2, column=0, padx=5, pady=2, sticky="e")
            self.flight_date_entry = DateEntry(frame, width=input_width - 2, date_pattern="yyyy-mm-dd")
            self.flight_date_entry.set_date(record.date)
            self.flight_date_entry.config(state="disabled")
            self.flight_date_entry.grid(row=2, column=1, padx=5, pady=2, sticky="w")
            entries["Date"] = self.flight_date_entry

            ttk.Label(frame, text="Time:").grid(row=3, column=0, padx=5, pady=2, sticky="e")
            time_frame = ttk.Frame(frame)
            time_frame.grid(row=3, column=1, padx=5, pady=2, sticky="w")
            self.flight_hour_entry = ttk.Combobox(time_frame, width=5, values=[f"{h:02d}" for h in range(24)],
                                                  state="disabled")
            self.flight_hour_entry.set(f"{record.date.hour:02d}")
            self.flight_hour_entry.pack(side="left")
            ttk.Label(time_frame, text=":").pack(side="left", padx=2)
            self.flight_minute_entry = ttk.Combobox(time_frame, width=5, values=[f"{m:02d}" for m in range(0, 60, 5)],
                                                    state="disabled")
            self.flight_minute_entry.set(f"{record.date.minute:02d}")
            self.flight_minute_entry.pack(side="left")
            entries["Time"] = (self.flight_hour_entry, self.flight_minute_entry)

            ttk.Label(frame, text="Departure City:").grid(row=4, column=0, padx=5, pady=2, sticky="e")
            self.flight_start_entry = ttk.Entry(frame, width=input_width)
            self.flight_start_entry.insert(0, record.start_city)
            self.flight_start_entry.config(state="disabled")
            self.flight_start_entry.grid(row=4, column=1, padx=5, pady=2, sticky="w")
            entries["Departure City"] = self.flight_start_entry

            ttk.Label(frame, text="Destination City:").grid(row=5, column=0, padx=5, pady=2, sticky="e")
            self.flight_end_entry = ttk.Entry(frame, width=input_width)
            self.flight_end_entry.insert(0, record.end_city)
            self.flight_end_entry.config(state="disabled")
            self.flight_end_entry.grid(row=5, column=1, padx=5, pady=2, sticky="w")
            entries["Destination City"] = self.flight_end_entry

        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=6 if record_type == RecordType.FLIGHT else len(fields), column=0, columnspan=2, pady=10)

        edit_btn = ttk.Button(btn_frame, text="Edit", command=lambda: self.enable_edit(entries, save_btn))
        edit_btn.pack(side="left", padx=5)
        save_btn = ttk.Button(btn_frame, text="Save",
                              command=lambda: self.save_record(record_type, record_id, entries, details_window),
                              state="disabled")
        save_btn.pack(side="left", padx=5)
        delete_btn = ttk.Button(btn_frame, text="Delete",
                                command=lambda: self.delete_record(record_type, record_id, details_window))
        delete_btn.pack(side="left", padx=5)

    def enable_edit(self, entries, save_btn):
        """
        Enables editing of record fields in the details window.

        Args:
            entries (dict): Dictionary of field labels to entry widgets.
            save_btn (ttk.Button): The Save button to enable.
        """
        for label, entry in entries.items():
            if label != "ID":  # ID remains uneditable
                if label == "Time":
                    entry[0].config(state="readonly")  # Hour Combobox
                    entry[1].config(state="readonly")  # Minute Combobox
                elif label in ("Client", "Airline"):
                    entry.config(state="readonly")
                else:
                    entry.config(state="normal" if label != "Date" else "readonly")
        save_btn.config(state="normal")

    def save_record(self, record_type, record_id, entries, window):
        """
        Saves changes to a record and updates the data store.

        Args:
            record_type (RecordType): The type of record being saved.
            record_id (int): The ID of the record to update.
            entries (dict): Dictionary of field labels to entry widgets.
            window (tk.Toplevel): The details window to close on success.
        """
        try:
            if record_type == RecordType.CLIENT:
                updated_record = ClientRecord(
                    id=record_id,
                    name=entries["Name"].get(),
                    address_line_1=entries["Address Line 1"].get(),
                    address_line_2=entries["Address Line 2"].get(),
                    address_line_3=entries["Address Line 3"].get(),
                    city=entries["City"].get(),
                    state=entries["County/State"].get(),
                    zip_code=entries["Postcode"].get(),
                    country=entries["Country"].get(),
                    phone_number=entries["Telephone Number"].get()
                )
            elif record_type == RecordType.AIRLINE:
                updated_record = AirlineRecord(id=record_id, company_name=entries["Company Name"].get())
            else:  # FLIGHT
                client_name = entries["Client"].get()
                airline_name = entries["Airline"].get()
                date_str = entries["Date"].get()
                hour = entries["Time"][0].get()
                minute = entries["Time"][1].get()
                start_city = entries["Departure City"].get()
                end_city = entries["Destination City"].get()

                if not all([client_name, airline_name, date_str, hour, minute, start_city, end_city]):
                    messagebox.showerror("Error", "All fields are mandatory")
                    return

                client_id = self.client_name_to_id[client_name]
                airline_id = self.airline_name_to_id[airline_name]
                date_time_str = f"{date_str} {hour}:{minute}:00"
                try:
                    date = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD HH:MM:SS")
                    return
                updated_record = FlightRecord(
                    id=record_id,
                    client_id=client_id,
                    airline_id=airline_id,
                    date=date,
                    start_city=start_city,
                    end_city=end_city
                )

            if self.data_manager.update_record(updated_record):
                self.data_manager.save_data()
                messagebox.showinfo("Success", "Record updated successfully")
                window.destroy()
                self.show_records(record_type)
            else:
                messagebox.showerror("Error", "Failed to update record")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def delete_record(self, record_type, record_id, window):
        """
        Deletes a record after user confirmation.

        Args:
            record_type (RecordType): The type of record to delete.
            record_id (int): The ID of the record to delete.
            window (tk.Toplevel): The details window to close on success.
        """
        if record_type in (RecordType.CLIENT, RecordType.AIRLINE):
            flights = self.data_manager.get_all_records(RecordType.FLIGHT)
            if record_type == RecordType.CLIENT and any(f.client_id == record_id for f in flights):
                messagebox.showerror("Error", f"Cannot delete Client ID {record_id} as it is linked to a Flight record")
                return
            if record_type == RecordType.AIRLINE and any(f.airline_id == record_id for f in flights):
                messagebox.showerror("Error", f"Cannot delete Airline ID {record_id} as it is linked to a Flight record")
                return

        if messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this record? This action is irreversible."):
            if self.data_manager.delete_record(record_id, record_type):
                self.data_manager.save_data()
                messagebox.showinfo("Success", "Record deleted successfully")
                window.destroy()
                self.show_records(record_type)
            else:
                messagebox.showerror("Error", "Failed to delete record")

    def add_client(self):
        """Adds a new client record based on form input."""
        name = self.client_name.get()
        addr1 = self.client_addr1.get()
        addr2 = self.client_addr2.get()
        addr3 = self.client_addr3.get()
        city = self.client_city.get()
        state = self.client_state.get()
        zip_code = self.client_zip.get()
        country = self.client_country.get()
        phone = self.client_phone.get()

        if name and country:
            try:
                client = ClientRecord(0, name, addr1, addr2, addr3, city, state, zip_code, country, phone)
                client_id = self.data_manager.add_record(client)
                self.data_manager.save_data()
                messagebox.showinfo("Success", f"Client added with ID: {client_id}")
                for entry in [self.client_name, self.client_addr1, self.client_addr2, self.client_addr3,
                              self.client_city, self.client_state, self.client_zip, self.client_country,
                              self.client_phone]:
                    entry.delete(0, tk.END)
            except ValueError as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "Name and Country are mandatory")

    def add_airline(self):
        """Adds a new airline record based on form input."""
        name = self.airline_name.get()

        if name:
            try:
                airline = AirlineRecord(0, name)
                airline_id = self.data_manager.add_record(airline)
                self.data_manager.save_data()
                messagebox.showinfo("Success", f"Airline added with ID: {airline_id}")
                self.airline_name.delete(0, tk.END)
            except ValueError as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "Company Name is mandatory")

    def add_flight(self):
        """Adds a new flight record based on form input."""
        try:
            client_name = self.flight_client_combo.get()
            airline_name = self.flight_airline_combo.get()
            date_str = self.flight_date.get()
            hour = self.flight_hour.get()
            minute = self.flight_minute.get()
            start_city = self.flight_start.get()
            end_city = self.flight_end.get()

            if not all([client_name, airline_name, date_str, hour, minute, start_city, end_city]):
                messagebox.showerror("Error", "All fields are mandatory")
                return

            date_time_str = f"{date_str} {hour}:{minute}:00"
            flight_date = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")

            client_id = self.client_name_to_id[client_name]
            airline_id = self.airline_name_to_id[airline_name]

            flight = FlightRecord(0, client_id, airline_id, flight_date, start_city, end_city)
            flight_id = self.data_manager.add_record(flight)
            self.data_manager.save_data()
            messagebox.showinfo("Success", f"Flight added with ID: {flight_id}")
            self.flight_client_combo.set("")
            self.flight_airline_combo.set("")
            self.flight_date.set_date(datetime.now())
            self.flight_hour.set("12")
            self.flight_minute.set("00")
            self.flight_start.delete(0, tk.END)
            self.flight_end.delete(0, tk.END)
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid date/time format: {str(e)}")


def main():
    """Launches the Travel Record Management System application."""
    root = tk.Tk()
    root.geometry("1080x720")
    app = RecordManagementApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()