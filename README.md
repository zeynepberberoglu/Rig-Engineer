# 🛠️ Rig-Engineer: System Analyzer for Engineers

![Project Category](https://img.shields.io/badge/Category-System%20Tool-blue)
![Language](https://img.shields.io/badge/Language-Python%203.x-yellow)
![Status](https://img.shields.io/badge/Status-Hackathon%20Prototype-orange)

> **"Can I run this?" – An engineering-focused answer to a critical question.**

## 📖 Executive Summary
Today, engineering students and junior developers often struggle to understand why heavy tools like Docker, IDEs, or Simulators perform poorly on their systems.

**Rig-Engineer** goes beyond listing hardware specifications. It performs real-time benchmarking and active resource analysis to provide an **"engineering-focused"** system health report. Think of it as "Can I Run It," but specialized for engineering tools like Unreal Engine, MATLAB, and Android Studio.

---

## 🚩 Problem Definition
* **The Static Data Problem:** Existing tools like "Can I Run It" only check manufacturer data. They don't account for thermal throttling or RAM usage by background processes.
* **Lack of Focus:** While there are many tools for gaming performance, there is no comprehensive analyzer dedicated to engineering software.
* **Bottleneck Ambiguity:** Users cannot easily determine if their system lag is due to insufficient RAM, CPU bottlenecks, or other factors.

## 💡 Solution & Features

### A. Dynamic Hardware Scraper
* Utilizes `psutil` and `GPUtil` to fetch real-time CPU, RAM, and GPU data.
* Compares system specs against a dynamic JSON database containing Minimum/Recommended requirements for popular engineering tools.

### B. Synthetic Benchmarking Engine
* **CPU Stress Test:** Measures the processor's *actual* current speed using mathematical calculations (e.g., prime number generation).
* **RAM Latency Test:** Tests memory read/write speeds instantaneously.

### C. Intelligent Decision Logic
* **Bottleneck Detection:** Analyzes background loads even if hardware is sufficient and provides a list of "Processes to Kill".
* **Engineering Score:** Rates the system out of 100 for categories like Software Development, 3D Modeling, and Data Science.

---

## ⚙️ Tech Stack
The project is built entirely on **Python 3.x** and powers its analysis with the following libraries:

| Domain | Technology |
|---|---|
| **System Analysis** | `psutil`, `platform`, `GPUtil`, `subprocess` |
| **User Interface** | PyQt6 / CustomTkinter (Modern Desktop UI) |
| **Data Management** | JSON / SQLite |

---

## 🚀 Installation & Usage

To run the project locally:

1. **Clone the repository:**
   ```bash
   
   git clone [https://github.com/zeynepberberoglu/Rig-Engineer.git](https://github.com/zeynepberberoglu/Rig-Engineer.git)
   cd Rig-Engineer
   
   ```
2. **Install requirements:**

   ```bash

   pip install -r requirements.txt

   ```

3. **Run the application:**

   ```bash

   python main.py

   ```
