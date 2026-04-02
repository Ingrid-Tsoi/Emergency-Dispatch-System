import time
from abc import ABC, abstractmethod


# --------------------------------------------------
# Abstract Base Class: EmergencyUnit
# --------------------------------------------------
class EmergencyUnit(ABC):
    """
    Abstract base class representing a generic emergency unit.

    Attributes:
    - unit_id: Unique identifier of the unit
    - unit_type: Type of unit (Ambulance, FireTruck, PoliceCar)
    - location: Current location of the unit
    - available: Availability status (True = available, False = busy)
    """

    def __init__(self, unit_id, unit_type, location):
        self.unit_id = unit_id
        self.unit_type = unit_type
        self.location = location
        self.available = True  # Units are available by default

    def set_available(self):
        """Mark the unit as available."""
        self.available = True

    def set_unavailable(self):
        """Mark the unit as unavailable (busy)."""
        self.available = False

    def is_available(self):
        """Check if the unit is available."""
        return self.available

    @abstractmethod
    def respond(self, incident):
        """
        Abstract method to define how a unit responds to an incident.
        Must be implemented by subclasses.
        """
        pass


# --------------------------------------------------
# Concrete Classes: Specific Emergency Units
# --------------------------------------------------
class Ambulance(EmergencyUnit):
    """Represents an ambulance unit."""

    def respond(self, incident):
        """Return response message when dispatched."""
        return f"Ambulance {self.unit_id} → Incident {incident.incident_id}"


class FireTruck(EmergencyUnit):
    """Represents a fire truck unit."""

    def respond(self, incident):
        """Return response message when dispatched."""
        return f"FireTruck {self.unit_id} → Incident {incident.incident_id}"


class PoliceCar(EmergencyUnit):
    """Represents a police car unit."""

    def respond(self, incident):
        """Return response message when dispatched."""
        return f"PoliceCar {self.unit_id} → Incident {incident.incident_id}"


# --------------------------------------------------
# Incident Class
# --------------------------------------------------
class Incident:
    """
    Represents an emergency incident.

    Attributes:
    - incident_id: Unique identifier
    - type: Type of incident (e.g., Fire, Accident)
    - location: Incident location
    - severity: Severity level (1–5)
    - status: Current status (Pending, Dispatched, Resolved)
    - assigned_unit: Unit assigned to handle the incident
    - timestamp: Time when incident was reported
    - priority: Computed priority score
    """

    def __init__(self, incident_id, incident_type, location, severity):
        self.incident_id = incident_id
        self.type = incident_type
        self.location = location
        self.severity = int(severity)
        self.status = "Pending"
        self.assigned_unit = None
        self.timestamp = time.time()  # Record creation time
        self.priority = 0

    def update_priority(self):
        """
        Update incident priority based on:
        - Severity (weighted heavily)
        - Waiting time (capped at 30 seconds)

        Formula:
        priority = severity * 10 + waiting_time
        """
        waiting = time.time() - self.timestamp
        self.priority = self.severity * 10 + int(min(waiting, 30))

    def assign_unit(self, unit):
        """
        Assign a unit to this incident and update status.
        """
        self.assigned_unit = unit
        self.status = "Dispatched"

    def mark_resolved(self):
        """
        Mark the incident as resolved.
        """
        self.status = "Resolved"