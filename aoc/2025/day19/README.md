# Modbus

Runs on port 502 with no auth

https://tryhackme.com/room/ICS-modbus-aoc2025-g3m6n9b1v4



```
TBFC DRONE CONTROL - REGISTER MAP
(For maintenance use only)

HOLDING REGISTERS:
HR0: Package Type Selection
     0 = Christmas Gifts
     1 = Chocolate Eggs
     2 = Easter Baskets

HR1: Delivery Zone (1-9 normal, 10 = ocean dump!)

HR4: System Signature/Version
     Default: 100
     Current: ??? (check this!)

COILS (Boolean Flags):
C10: Inventory Verification
     True = System checks actual stock
     False = Blind operation

C11: Protection/Override
     True = Changes locked/monitored
     False = Normal operation

C12: Emergency Dump Protocol
     True = DUMP ALL INVENTORY
     False = Normal

C13: Audit Logging
     True = All changes logged
     False = No logging

C14: Christmas Restored Flag
     (Auto-set when system correct)

C15: Self-Destruct Status
     (Auto-armed on breach)

CRITICAL: Never change HR0 while C11=True!
Will trigger countdown!

- Maintenance Tech, Dec 19
```


```
Holding Registers storing configuration values:
HR0: Package type selection (0=Gifts, 1=Eggs, 2=Baskets)
HR1: Delivery zone (1-9 for normal zones, 10 for emergency disposal)
HR4: System signature (a version identifier or, in this case, an attacker's calling card)
Coils controlling system behaviour:
C10: Inventory verification enabled/disabled
C11: Protection mechanism enabled/disabled
C12: Emergency dump protocol active/inactive
C13: Audit logging enabled/disabled
C14: Christmas restoration status flag
C15: Self-destruct mechanism armed/disarmed
```

## Tools

pymodbus

nmap -sV -p 22,80,502 10.66.188.65


### Connect Modbus
```
python3
Python 3.10.12 (main, Nov 20 2023, 15:14:05)
Type "help", "copyright", "credits" or "license" for more information.
>>> from pymodbus.client import ModbusTcpClient
>>> 
>>> # Connect to the PLC on port 502
>>> client = ModbusTcpClient('10.66.188.65', port=502)
>>> 
>>> # Establish connection
>>> if client.connect():
...     print("Connected to PLC successfully")
... else:
...     print("Connection failed")
... 
Connected to PLC successfully
>>>
```

### Read Registers

Abreviated
`client.read_holding_registers(address=10, count=1, slave=1).registers[0]`

full
```
>>> # Read holding register 0 (Package Type)
>>> result = client.read_holding_registers(address=0, count=1, slave=1)
>>> 
>>> if not result.isError():
...     package_type = result.registers[0]
...     print(f"HR0 (Package Type): {package_type}")
...     if package_type == 0:
...         print("  Christmas Presents")
...     elif package_type == 1:
...         print("  Chocolate Eggs")
...     elif package_type == 2:
...         print("  Easter Baskets")
... 
HR0 (Package Type): 1
  Chocolate Eggs
>>>
```


### Read Coils

Abreviated
`client.read_coils(address=14, count=1, slave=1).bits[0]`


```
>>> result = client.read_coils(address=10, count=1, slave=1)
>>> 
>>> if not result.isError():
...     verification = result.bits[0]
...     print(f"C10 (Inventory Verification): {verification}")
...     if not verification:
...         print("  DISABLED - System not checking stock")
... 
C10 (Inventory Verification): False
  DISABLED - System not checking stock
>>>
```