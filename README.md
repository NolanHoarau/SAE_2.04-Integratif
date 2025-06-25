## Config Routeur
Router-rt12(config)# hostname Router2800
Router2800(config)# no ip domain-lookup
Router2800(config)# ip domain-name sae24.rt
Router2800(config)# enable secret 0 MonSuperSecret
Router2800(config)# ip name-server 10.252.4.42
Router2800(config)# ip dns server

Router2800(config)# interface g0/0
 description Trunk vers SW (802.1Q)
 no ip address
 no shutdown

Router2800(config)# interface g0/1
 shutdown

Router2800(config)# interface s0/3/0
 description WAN / Fournisseur
 ip address 201.100.11.1 255.255.255.252
 ip nat outside
 clock rate 2000000
 no shutdown

Router2800(config)# interface g0/0.100
 encapsulation dot1Q 100
 ip address 10.252.10.1 255.255.255.192
 ip helper-address 10.252.10.1
 ip nat inside

Router2800(config)# interface g0/0.200
 encapsulation dot1Q 200
 ip address 10.252.10.65 255.255.255.192
 ip helper-address 10.252.10.65
 ip access-group ICMPBLOCK in
 ip nat inside

Router2800(config)# interface g0/0.300
 encapsulation dot1Q 300
 ip address 10.252.10.129 255.255.255.192
 ip helper-address 10.252.10.129
 ip nat inside

Router2800(config)# interface g0/0.400
 encapsulation dot1Q 400
 ip address 10.252.10.193 255.255.255.192
 ip helper-address 10.252.10.193
 ip nat inside

Router2800(config)# ip route 0.0.0.0 0.0.0.0 201.100.11.2

Router2800(config)# ip dhcp excluded-address 10.252.10.1 10.252.10.10
Router2800(config)# ip dhcp excluded-address 10.252.10.65 10.252.10.74
Router2800(config)# ip dhcp excluded-address 10.252.10.129 10.252.10.138
Router2800(config)# ip dhcp excluded-address 10.252.10.193 10.252.10.202

Router2800(config)# ip dhcp pool VLAN100-VOIX
 network 10.252.10.0 255.255.255.192
 default-router 10.252.10.1
 dns-server 10.252.4.42
 domain-name sae24.rt

Router2800(config)# ip dhcp pool VLAN200-USERS
 network 10.252.10.64 255.255.255.192
 default-router 10.252.10.65
 dns-server 10.252.4.42
 domain-name sae24.rt

Router2800(config)# ip dhcp pool VLAN300-SERVEUR
 network 10.252.10.128 255.255.255.192
 default-router 10.252.10.129
 dns-server 10.252.4.42
 domain-name sae24.rt

Router2800(config)# ip dhcp pool VLAN400-ADMIN
 network 10.252.10.192 255.255.255.192
 default-router 10.252.10.193
 dns-server 10.252.4.42
 domain-name sae24.rt

Router2800(config)# access-list 1 permit 10.252.10.0 0.0.0.63
Router2800(config)# access-list 1 permit 10.252.10.64 0.0.0.63
Router2800(config)# access-list 1 permit 10.252.10.128 0.0.0.63
Router2800(config)# access-list 1 permit 10.252.10.192 0.0.0.63

Router2800(config)# ip nat inside source list 1 interface s0/3/0 overload

Router2800(config)# ip access-list extended ICMPBLOCK
 deny icmp 10.252.10.64 0.0.0.63 10.252.10.192 0.0.0.63 echo
 permit ip any any

Router2800(config)# clock timezone CET 1
Router2800(config)# clock summer-time CEST recurring
Router2800(config)# ntp server fr.pool.ntp.org
Router2800(config)# logging host 10.252.10.130
Router2800(config)# service timestamps debug datetime msec
Router2800(config)# service timestamps log datetime msec

Router2800(config)# no ip http server
Router2800(config)# crypto key generate rsa modulus 2048

Router2800# write memory



---
## Config Switch-rt12

```
Switch-rt12(config) # vlan 100
	name Voix
	no shut
	
Switch-rt12(config) # vlan 200
	name Users
	no shut
	
Switch-rt12(config) # vlan 300
	name Serveur
	no shut
	
Switch-rt12(config) # vlan 400
	name Administrateurs
	no shut
```

```
Switch-rt12(config) # int range f0/1-4
	switchport mode access
	switchport access vlan 100

Switch-rt12(config) # int range f0/5-8
	switchport mode access
	switchport access vlan 200

Switch-rt12(config) # int range f0/9-12
	switchport mode access
	switchport access vlan 300

Switch-rt12(config) # int range f0/13-16
	switchport mode access
	switchport access vlan 400
```

### Mise en place des ports mirroring

Le mirroring permet a pour objectif de faire de la surveillance du trafic d'un port ou d'un vlan via une config **SPAN (Switched Port Analyser)**

```
Switch(config)# monitor session 1 source interface g0/1 both
	monitor session 1 destnation interface f0/24

Switch(config)# monitor session 2 source vlan 100
	monitor session 2 destination interface f0/23
```

- `source` : spécifie le port a surveiller
- `both` : capture le trafic dans les deux sens (entrant et sortant)
- `destination` : c'est le port où est branché l'outil de capture

`sh monitor session all`

---

## Récupération des informations mqtt dans une base de donnée avec python

```bash
sudo apt install libmariadb-dev
sudo apt install mariadb-server
sudo systemctl start mariadb
sudo systemctl enable mariadb
sudo apt install python3-pip
sudo apt install python3.11-venv
```

Creation d'un environnement virtuel pour le script python permettant de récupérer les informations et les mettres dans une base de données mariadb.

```bash
python3 -m venv monenv
```
activation de l'environnement virtuel :

```bash
source monenv/bin/activate
```
Installation des paquets python :

```bash
(monenv) pip install paho-mqtt mariadb
```
mettre le programme python dans un fichier .py dans l'environnement puis lancer Mariadb :

```bash
sudo mariadb
```
Dans mariadb on créer la database

```sql
CREATE DATABASE IF NOT EXISTS sae204;
```

Et créer un user pour la database

```sql
CREATE USER 'toto'@'localhost' IDENTIFIED BY 'toto';
GRANT ALL PRIVILEGES ON sae204.* TO 'toto'@'localhost';
FLUSH PRIVILEGES;
```
Dans le script python :

....

Enfin lancer le script

```bash
python3 ./script.py
```

---

