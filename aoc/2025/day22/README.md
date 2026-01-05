# C2 Detection

https://tryhackme.com/room/detecting-c2-with-rita-aoc2025-m9n2b5v8c1

Convert PCAP to Zeek logs
Use RITA to analyze zeek logs



zeek readpcap pcaps/AsyncRAT.pcap zeek_logs/asyncrat

rita import --logs ~/zeek_logs/asyncrat/ --database foobar

rita view asyncrat


Common threats

- MIME type/URI mismatch: Flags connections where the MIME type reported in the HTTP header doesn't match the URI. This can indicate an attacker is trying to trick the browser or a security tool.

- Rare signature: Points to unusual patterns that attackers might overlook, such as a unique user agent string that is not seen in any other connections on the network.

- Prevalence: Analyzes the number of internal hosts communicating with a specific external host. A low percentage of internal hosts communicating with an external one can be suspicious.

- First Seen: Checks the date an external host was first observed on the network. A new host on the network is more likely to be a potential threat.

- Missing host header: Identifies HTTP connections that are missing the host header, which is often an oversight by attackers or a sign of a misconfigured system.

- Large amount of outgoing data: Flags connections that send a very large amount of data out from the network.

- No direct connections: Flags connections that don't have any direct connections, which can be a sign of a more complex or hidden command and control communication.
