# **signalDUPLI**  
*A Signal Duplicator for ASK Modulated Signals*

## **Overview**  
**signalDUPLI** allows you to capture, analyze, and replicate ASK-modulated signals using RTL-SDR, Universal Radio Hacker (URH), and an ESP32-based transmitter setup.  

---

## **Requirements**  
1. **Software**  
   - [rtl-433](https://github.com/merbanan/rtl_433)  
   - [Universal Radio Hacker (URH)](https://github.com/jopohl/urh)  

2. **Hardware**  
   - ESP32 microcontroller  
   - ASK-compatible transmitter module (connected to GPIO 4 on the ESP32)  

---

## **Setup Guide**

### **Step 1: Install Dependencies**
1. **Download and install rtl-433**  
   Follow the instructions from the [rtl-433 repository](https://github.com/merbanan/rtl_433).  

2. **Download and install Universal Radio Hacker (URH)**  
   Follow the instructions from the [URH repository](https://github.com/jopohl/urh).  

---

### **Step 2: Upload Firmware**  
1. Flash the provided firmware to your ESP32 microcontroller.  

---

### **Step 3: Connect the Transmitter**  
1. Connect your ASK transmitter to the **GPIO 4** pin on the ESP32.  

---

### **Step 4: Capture Signals**  
1. Run **rtl-433** with the following command:  
   ```bash
   rtl_433 -S all
   ```  

2. Wait for the signal file to appear.  

---

### **Step 5: Analyze Signals**  
1. Open the signal file in **Universal Radio Hacker (URH)**.  

2. Set the following parameters in URH:  
   - **Samples/Symbol:** `1`  
   - **Error Tolerance:** `5`  
   - **Modulation:** `ASK`  
   - **Bit/Symbol:** `1`  
   - **Show Data As:** `Hex`  

3. Your URH interface should look similar to this:  
   ![URH Example](https://github.com/kototronik/signalDUPLI/blob/main/1.png?raw=true)  

4. Copy the resulting **data array**.  

---

### **Step 6: Prepare Data**  
1. Paste the copied data into `input.txt`.  

---

### **Step 7: Replicate Signals**  
1. Run the provided Python script to transmit the signal.  
