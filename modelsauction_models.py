"""
Data models for the micro-auction system.
"""
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from enum import Enum
import uuid

class AuctionStatus(Enum):
    """Auction lifecycle states."""
    PENDING = "pending"  # Telemetry collecting, not yet biddable
    ACTIVE = "active"    # Open for bidding
    TIME_LOCKED = "time_locked"  # Bidding closed, waiting for restoration
    COMPLETED = "completed"  # Winner determined, data delivered
    CANCELLED = "cancelled"  # System restored before time lock
    FAILED = "failed"  # Critical error in auction process

class SystemFailureType(Enum):
    """Catalog of known failure types for categorization."""
    RAM_EXHAUSTION = "ram_exhaustion"
    API_CASCADE_COLLAPSE = "api_cascade_collapse"
    DISK_FULL = "disk_full"
    NETWORK_PARTITION = "network_partition"
    DATABASE_DEADLOCK = "database_deadlock"
    UNKNOWN = "unknown"

@dataclass
class TelemetryData:
    """Real-time system telemetry at failure moment."""
    timestamp: datetime
    failure_type: SystemFailureType
    metrics: Dict[str, Any]  # e.g., {"ram_usage_percent": 99.8, "api_error_rate": 0.95}
    system_context: Dict[str, Any]  # e.g., {"node_id": "server-1", "service_version": "2.4.1"}
    stack_trace: Optional[str] = None
    logs_excerpt: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to Firestore