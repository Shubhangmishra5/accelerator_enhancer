## 🚀 Accelerator Enhancer System

This project is a **smart motor control system** designed to optimize **acceleration**, **torque**, and **speed** using a cluster of **6 motors**. It features a real-time Pygame-based GUI to control and monitor the motors, interfaced with an **STM32 microcontroller** over serial communication.

### 🔧 Features

- **Manual Mode**: Individually control each motor (M1–M6).
- **Auto Modes**: Choose from *Sports*, *Normal*, or *Eco* to automate motor behavior.
- **Live Monitoring**: Real-time feedback of **Current (A)** and **RPM** through analog-style meters.
- **Bidirectional Communication**: Sends commands and receives live data from STM32.
- **Dynamic State Management**: All motor and mode states tracked via a single array `systemSTATE`.

### 📦 Tech Stack

- **Python** (Pygame, PySerial)
- **STM32 Microcontroller**
- **Serial UART Communication**

### 🧠 Future Scope

- Add logic for automatic motor activation based on load (Current).
- Implement logging and real-time graphing.
- Define dynamic behavior profiles for each auto mode.
- Introduce fault detection for overcurrent/low RPM.
