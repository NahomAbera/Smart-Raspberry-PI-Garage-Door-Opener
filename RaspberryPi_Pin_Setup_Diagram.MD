Raspberry Pi              Relay Module
+-----------------+       +---------------+
| Physical Pin 2  |------>| VCC           |
| Physical Pin 7  |------>| IN1 (Door 1)  |
| Physical Pin 11 |------>| IN2           |
| Physical Pin 13 |------>| IN3 (Door 2)  |
| Physical Pin 15 |------>| IN4           |
| Physical Pin 9  |------>| GND           |
+-----------------+       +---------------+

Raspberry Pi              Magnetic Switches (Door 1)
+-----------------+       +---=-------------+
| Physical Pin 29 |------>|NO (open Switch) |
| Physical Pin 31 |------>|NO (close Switch)|
| Any Ground Pin  |------>| COM             |
+-----------------+       +-----------------+

Raspberry Pi              Magnetic Switches (Door 2)
+-----------------+       +-----------------+
| Physical Pin 33 |------>|NO (open Switch) |
| Physical Pin 37 |------>|NO (close Switch)|
| Any Ground Pin  |------>|COM              |
+-----------------+       +-----------------+