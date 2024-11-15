# signalDUPLI
ASK signal duplicator

## How to use:

**Download and install** [rtl-433](https://github.com/merbanan/rtl_433)

**Download and install** [universal radio hacker](https://github.com/jopohl/urh)


**Upload firmware** to esp32

**Connect transmitter** to GIPO 4


**Run rtl-433 as**: rtl_433 -S all -p -47

**Wait** for the **file** to appear **and open it in URH**.


**Set the following parameters:** 

samples/symbol 1

error tolerance 5

modulation ASK

bit/symbol 1

show date as hex

![ ](https://github.com/kototronik/signalDUPLI/blob/main/1.png?raw=true)


**Copy the resulting array
paste it into input.txt
run the Python file**
