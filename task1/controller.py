from models import *
from heap_structure import MaxHeap, heap_sort


class Dispatcher:
    """
    Dispatcher class manages emergency units and incidents.
    Responsibilities include:
    - Reporting incidents
    - Dispatching appropriate units
    - Resolving incidents
    - Maintaining incident history
    """

    def __init__(self):
        """Initialize dispatcher with empty lists and load default units."""
        self.units = []           # List of all available units
        self.incidents = []       # Active incidents
        self.history = []         # Resolved incidents
        self.id_counter = 1       # Unique incident ID generator
        self._load_units()        # Load predefined units

    def _load_units(self):
        """Load initial emergency units into the system."""
        self.units = [
            Ambulance("A1", "Ambulance", "Central"),
            Ambulance("A2", "Ambulance", "Kowloon"),
            FireTruck("F1", "FireTruck", "Central"),
            PoliceCar("P1", "PoliceCar", "Mongkok")
        ]

    # -------------------------
    # Validation
    # -------------------------
    def _validate(self, t, l, s):
        """
        Validate incident input data.

        Parameters:
        t (str): Incident type
        l (str): Location
        s (int): Severity (1–5)

        Raises:
        ValueError if any field is invalid
        """
        if not t or not l:
            raise ValueError("Missing fields")

        if not isinstance(s, int) or s < 1 or s > 5:
            raise ValueError("Severity must be 1–5")

    # -------------------------
    # Report
    # -------------------------
    def report_incident(self, t, l, s):
        """
        Create and store a new incident.

        Returns:
        Incident object if successful
        Error message string if validation fails
        """
        try:
            self._validate(t, l, s)

            # Create new incident with unique ID
            inc = Incident(self.id_counter, t, l, s)
            self.id_counter += 1

            self.incidents.append(inc)
            return inc

        except Exception as e:
            return str(e)

    # -------------------------
    # Matching Logic
    # -------------------------
    def _match_unit(self, incident):
        """
        Match the most suitable available unit for a given incident.

        Priority:
        1. Best match based on incident type
        2. Fallback to any available unit

        Returns:
        Unit object or None if no unit is available
        """

        # Mapping of incident types to preferred unit types
        mapping = {
            "Fire": ["FireTruck"],
            "Medical Emergency": ["Ambulance"],
            "Car Accident": ["Ambulance", "PoliceCar"],
            "Drowning": ["Ambulance"],
            "Fall": ["Ambulance", "PoliceCar"],
            "Assault": ["PoliceCar"],
            "Stealing / Theft": ["PoliceCar"],
            "Gas Leak": ["FireTruck"],
            "Electrical Hazard": ["FireTruck", "Ambulance"],
        }

        # Get preferred unit types for this incident
        types = mapping.get(incident.type, [])

        # First pass: find best matching available unit
        for t in types:
            for u in self.units:
                if u.is_available() and u.unit_type == t:
                    return u

        # Fallback: return any available unit
        for u in self.units:
            if u.is_available():
                return u

        # No units available
        return None

    # -------------------------
    # Dispatch
    # -------------------------
    def dispatch_unit(self):
        """
        Dispatch the most appropriate unit to the highest priority incident.

        Uses a MaxHeap to prioritize incidents dynamically.

        Returns:
        Dispatch message or error message
        """
        try:
            heap = MaxHeap()
            valid_incidents = []

            # Rebuild heap with updated priorities
            for inc in self.incidents:
                if inc.status == "Pending":
                    inc.update_priority()
                    valid_incidents.append(inc)

            # Build max heap from valid incidents
            heap.build(valid_incidents)

            if not valid_incidents:
                return "No pending incidents."

            unit = None
            incident = None
            attempts = len(valid_incidents)
            skipped = []  # Store skipped incidents temporarily

            # Try to find a suitable unit
            while attempts > 0:
                incident = heap.pop()
                unit = self._match_unit(incident)

                if unit:
                    break

                skipped.append(incident)
                attempts -= 1

            # Push skipped incidents back into heap
            for i in skipped:
                heap.push(i)

            if not unit:
                return "No suitable unit available."

            # Assign unit to incident
            msg = unit.respond(incident)
            incident.assign_unit(unit)
            unit.set_unavailable()

            return msg

        except Exception as e:
            return f"Error: {str(e)}"

    # -------------------------
    # Resolve
    # -------------------------
    def resolve_incident(self, inc_id):
        """
        Resolve a dispatched incident.

        Steps:
        - Verify incident exists
        - Ensure it has been dispatched
        - Mark as resolved
        - Free assigned unit
        - Move to history

        Returns:
        Status message
        """
        try:
            for inc in self.incidents:
                if inc.incident_id == inc_id:

                    # Prevent resolving non-dispatched incidents
                    if inc.status != "Dispatched":
                        return "Cannot resolve: Incident not dispatched."

                    # Mark incident as resolved
                    inc.mark_resolved()

                    # Make unit available again
                    if inc.assigned_unit:
                        inc.assigned_unit.set_available()

                    # Move incident to history
                    self.history.append(inc)
                    self.incidents.remove(inc)

                    return f"Incident {inc_id} resolved."

            return "Incident not found."

        except Exception as e:
            return f"Error: {str(e)}"

    # -------------------------
    # Sorting
    # -------------------------
    def get_sorted_incidents(self):
        """
        Return all active incidents sorted by priority.

        Uses heap_sort after updating priorities.

        Returns:
        Sorted list of incidents
        """
        for inc in self.incidents:
            inc.update_priority()

        return heap_sort(self.incidents)