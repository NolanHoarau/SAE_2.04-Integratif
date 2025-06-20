## Config Routeur




## Config Switch-rt12

Mot de passe enable : **conomejo**

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