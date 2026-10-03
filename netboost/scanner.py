from .models import Metrics
from .scan import wifi, path, dns, load, host

def full_scan(with_load=True):
    m = Metrics()
    w = wifi.scan()
    m.ssid = w["ssid"]
    m.band = w["band"]
    m.signal_pct = w["signal_pct"]
    m.link_mbps = w["link_mbps"]
    g, lan, wan = path.scan()
    m.gateway = g
    m.gateway_ms = lan["latency"]
    m.gateway_loss = lan["loss"]
    m.wan_ms = wan["latency"]
    m.wan_jitter = wan["jitter"]
    m.wan_loss = wan["loss"]
    m.idle_ms = m.wan_ms
    cur, ref = dns.scan()
    m.dns_current_ms = cur
    m.dns_reference_ms = ref
    h = host.scan()
    m.top_process = h["top_process"]
    m.top_process_bps = h["top_process_bps"]
    m.iface_bps = h["iface_bps"]
    m.tcp_autotune = h["tcp_autotune"]
    m.bits_active = h["bits_active"]
    if with_load:
        sample = load.scan()
        m.down_mbps = sample["down_mbps"]
        m.up_mbps = sample["up_mbps"]
        m.loaded_ms = sample["loaded_ms"]
        if sample.get("idle_ms") is not None:
            m.idle_ms = sample["idle_ms"]
    return m
