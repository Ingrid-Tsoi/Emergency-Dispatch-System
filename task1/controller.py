# controller.py
from models import *
from heap_structure import MaxHeap, heap_sort


class Dispatcher:
    def __init__(self):
        self.units = []
        self.incidents = []
        self.history = []
        self.heap = MaxHeap()
        self._load_units()

    # Load default units
    def _load_units(self):
        self.units.append(Ambulance("A1", "Ambulance", "Central"))
        self.units.append(Ambulance("A2", "Ambulance", "Kowloon"))
        self.units.append(FireTruck("F1", "FireTruck", "Central"))
        self.units.append(PoliceCar("P1", "PoliceCar", "Mongkok"))

    # Report incident
    def report_incident(self, incident_type, location, severity):
        incident_id = len(self.incidents) + len(self.history) + 1
        incident = Incident(incident_id, incident_type, location, severity)

        self.incidents.append(incident)
        self.heap.push(incident)

        return incident

    # Priority Dispatch using Heap
    def dispatch_unit(self):
        self.heap = MaxHeap()
        # Update priority before choosing
        for inc in self.incidents:
            if inc.status == "Pending":
                inc.update_priority()
                self.heap.push(inc)

        incident = self.heap.pop()

        if not incident:
            return "No pending incidents."

        # choose an available unit
        for unit in self.units:
            if unit.is_available():
                msg = unit.respond(incident)
                incident.assign_unit(unit)
                unit.set_unavailable()
                return msg

        return "No available units."

    # Resolve incident
    def resolve_incident(self, incident_id):
        for inc in self.incidents:
            if inc.incident_id == incident_id:
                inc.mark_resolved()
                if inc.assigned_unit:
                    inc.assigned_unit.set_available()

                self.history.append(inc)
                self.incidents.remove(inc)
                return f"Incident {incident_id} resolved."
        return "Incident not found"