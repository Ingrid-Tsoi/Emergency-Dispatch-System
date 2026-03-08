# models.py
import time
from abc import ABC, abstractmethod

# ============================================================
# Abstract Class: EmergencyUnit
# ============================================================
class EmergencyUnit(ABC):
    def __init__(self, unit_id, unit_type, location):
        self.unit_id = unit_id
        self.unit_type = unit_type
        self.location = location
        self.available = True

    def set_available(self):
        self.available = True

    def set_unavailable(self):
        self.available = False

    def is_available(self):
        return self.available

    @abstractmethod
    def respond(self, incident):
        pass


# ============================================================
# Subclasses: Ambulance / FireTruck / PoliceCar
# ============================================================
class Ambulance(EmergencyUnit):
    def respond(self, incident):
        return f"🚑 Ambulance {self.unit_id} responding to incident {incident.incident_id}"


class FireTruck(EmergencyUnit):
    def respond(self, incident):
        return f"🔥 FireTruck {self.unit_id} responding to incident {incident.incident_id}"


class PoliceCar(EmergencyUnit):
    def respond(self, incident):
        return f"🚓 PoliceCar {self.unit_id} responding to incident {incident.incident_id}"


# ============================================================
# Incident Class
# ============================================================
class Incident:
    def __init__(self, incident_id, incident_type, location, severity):
        self.incident_id = incident_id
        self.type = incident_type
        self.location = location
        self.severity = int(severity)
        self.status = "Pending"
        self.assigned_unit = None
        self.timestamp = time.time()
        self.priority = self.calculate_priority()

    def calculate_priority(self):
        waiting_time = time.time() - self.timestamp
        return self.severity * 2 + waiting_time * 1.5

    def update_priority(self):
        self.priority = self.calculate_priority()

    def assign_unit(self, unit):
        self.assigned_unit = unit
        self.status = "Dispatched"

    def mark_resolved(self):
        self.status = "Resolved"