# IPv6 tcpdump → Oracle REST

A small Python script for reading IPv6 packets from a network interface (tcpdump) and sending parsed data to a REST service (Oracle REST/ORDS).

Features:

- Listens on the `eth0` interface via `tcpdump` (requires root or sudo privileges).
- Extracts timestamp, source MAC address and VLAN (if present) and sends JSON to the specified URL.
- Simple modular structure: `ipv6.py` (main reader/parser) and `oracle_rest.py` (HTTP client).

Requirements
-----------

- Python 3.7+
- Libraries: `requests`

Installation
---------

1. Create a virtual environment (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

Running
------

The `ipv6.py` file is executed as a script. By default it uses tcpdump on `eth0` and posts data to the URL set in `service_url`.

Examples:

```bash
# run directly (sudo required for tcpdump)
sudo python3 ipv6.py

# or if you want to run without sudo, grant tcpdump capabilities (not recommended) or use CAP_NET_RAW
```

Configuration
-------------

- `service_url` — REST service URL (in `ipv6.py`).
- `vlan_native` — default VLAN value when tcpdump output does not contain VLAN info.
- If your server uses a different interface name (not `eth0`), edit the `cmd` list in `ipv6.py` or use the CLI options.

Security
--------

The script runs `tcpdump` with elevated privileges. Ensure you understand the risks and follow security best practices (limited access, use of a service account, auditing).

License
--------

This project is licensed under the MIT License — see the `LICENSE` file.

Contributing
------------

PRs and improvements are welcome. Open an issue to propose a feature or report a bug.
