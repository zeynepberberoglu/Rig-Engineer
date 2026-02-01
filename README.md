# 🛠️ Rig-Engineer: System Analyzer for Engineers

![Project Category](https://img.shields.io/badge/Category-System%20Tool-blue)
![Language](https://img.shields.io/badge/Language-Python%203.x-yellow)
![Status](https://img.shields.io/badge/Status-Hackathon%20Prototype-orange)

> **"Can I run this?" – An engineering-focused answer to a critical question.**

## 📖 Executive Summary
Today, engineering students and junior developers often struggle to understand why heavy tools like Docker, IDEs, or Simulators perform poorly on their systems.

**Rig-Engineer** goes beyond listing hardware specifications. It performs real-time benchmarking and active resource analysis to provide an **"engineering-focused"** system health report. [cite_start]Think of it as "Can I Run It," but specialized for engineering tools like Unreal Engine, MATLAB, and Android Studio[cite: 5, 6, 7].

---

## 🚩 Problem Definition
* **The Static Data Problem:** Existing tools like "Can I Run It" only check manufacturer data. [cite_start]They don't account for thermal throttling or RAM usage by background processes[cite: 9, 10].
* [cite_start]**Lack of Focus:** While there are many tools for gaming performance, there is no comprehensive analyzer dedicated to engineering software[cite: 11].
* [cite_start]**Bottleneck Ambiguity:** Users cannot easily determine if their system lag is due to insufficient RAM, CPU bottlenecks, or other factors[cite: 12].

## 💡 Solution & Features

### A. Dynamic Hardware Scraper
* [cite_start]Utilizes `psutil` and `GPUtil` to fetch real-time CPU, RAM, and GPU data[cite: 16].
* [cite_start]Compares system specs against a dynamic JSON database containing Minimum/Recommended requirements for popular engineering tools[cite: 17].

### B. Synthetic Benchmarking Engine
* [cite_start]**CPU Stress Test:** Measures the processor's *actual* current speed using mathematical calculations (e.g., prime number generation)[cite: 19, 20].
* [cite_start]**RAM Latency Test:** Tests memory read/write speeds instantaneously[cite: 21].

### C. Intelligent Decision Logic
* [cite_start]**Bottleneck Detection:** Analyzes background loads even if hardware is sufficient and provides a list of "Processes to Kill"[cite: 23].
* [cite_start]**Engineering Score:** Rates the system out of 100 for categories like Software Development, 3D Modeling, and Data Science[cite: 24].

---

## ⚙️ Tech Stack
[cite_start]The project is built entirely on **Python 3.x** and powers its analysis with the following libraries[cite: 26]:

| Domain | Technology |
|---|---|
| **System Analysis** | [cite_start]`psutil`, `platform`, `GPUtil`, `subprocess` [cite: 27] |
| **User Interface** | [cite_start]PyQt6 / CustomTkinter (Modern Desktop UI) [cite: 29] |
| **Data Management** | [cite_start]JSON / SQLite [cite: 28] |

---

## 🚀 Installation & Usage

To run the project locally:

1. **Clone the repository:**
   ```bash  
   git clone [https://github.com/zeynepberberoglu/Rig-Engineer.git](https://github.com/zeynepberberoglu/Rig-Engineer.git)
   cd Rig-Engineer
2. **Install requirements:**
   ```bash
   pip install -r requirements.txt
3. **Run the application:**
   ```bash
   python main.py
