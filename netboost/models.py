from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Metrics:
    ssid: str = "Unknown"
    band: str = "Unknown"
    signal_pct: Optional[int] = None
    link_mbps: Optional[float] = None
    gateway: Optional[str] = None
    gateway_ms: Optional[float] = None
    gateway_loss: Optional[float] = None
    wan_ms: Optional[float] = None
    wan_jitter: Optional[float] = None
    wan_loss: Optional[float] = None
    dns_current_ms: Optional[float] = None
    dns_reference_ms: Optional[float] = None
    down_mbps: Optional[float] = None
    up_mbps: Optional[float] = None
    idle_ms: Optional[float] = None
    loaded_ms: Optional[float] = None
    top_process: Optional[str] = None
    top_process_bps: Optional[float] = None
    iface_bps: Optional[float] = None
    tcp_autotune: Optional[str] = None
    bits_active: bool = False

@dataclass
class Finding:
    cause: str
    confidence: str
    evidence: list[str] = field(default_factory=list)
    action: str = ""
    fix_id: Optional[str] = None
    before: dict = field(default_factory=dict)
    after: Optional[dict] = None
    undo_id: Optional[str] = None
    improved: Optional[bool] = None
    note: str = ""
