# 🚗 GenAuto-SDV Studio v2.0
> **Build Safe, Compliant Automotive SoA Services in Minutes — Not Weeks.**  
> *Built for Tata Elxsi TELIPORT Season 3 (Round 2)*

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://genauto-sdv.streamlit.app)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Standard](https://img.shields.io/badge/Compliance-MISRA%20C%2B%2B%3A2023-orange)

---

## 🌟 The Problem
Vehicle software development today is **slow, manual, and error-prone**.
- **4-8 Weeks** to develop a single Service-Oriented Architecture (SoA) service.
- **Manual Compliance Reviews** (MISRA/AUTOSAR) take days.
- **Integration Chaos** between different vehicle domains.

## 💡 The Solution: GenAuto-SDV
**GenAuto-SDV Studio** is a Generative AI-powered DevOps platform that automates the entire lifecycle of automotive software:
1.  **Requirement** (Natural Language)
2.  **Architecture** (COVESA VSS & SOME/IP)
3.  **Code Generation** (C++14, Franca IDL, Docker)
4.  **Validation** (MISRA C++:2023)
5.  **Deployment** (CI/CD simulation & OTA)

...all in **under 2 minutes**.

---

## 🚀 Key Features (The "Wow" Factors)

### 1. 🧠 AI Development Studio
- **Multi-LLM Engine:** Auto-switches between **Claude 3 Haiku** (Anthropic), **Llama 3** (Groq), and **Gemini 2.0** for enterprise-grade resilience.
- **Compliance-First:** Safety isn't an afterthought. We inject **MISRA C++:2023** rules directly into the generation prompt.
- **Automated Artifacts:** Generates C++ Source, CMakeLists, Dockerfiles, and Franca IDL interfaces automatically.

### 2. 📊 Connected Vehicle Dashboard (Digital Twin)
- **3D Digital Twin:** Real-time 3D point cloud visualization of the vehicle state.
- **Live Telemetry:** Gauges react in real-time to the generated service (e.g., Tire Pressure, Battery SOH).
- **Edge AI Predictions:** Integrated ML models predict failures (e.g., "Tire Blowout Risk: High").

### 3. 🛡️ Resilience & "Demo Guard"
- **Zero-Fail Guarantee:** Built-in fallback mechanisms ensure the demo *never* crashes. If APIs fail, the system switches to high-fidelity simulation.

### 4. 🔄 OTA & Subscription Store
- **Simulated Updates:** Deploy new services or unlock features (e.g., "Premium Analytics") over-the-air.
- **Dynamic Docker Management:** View running containers on the simulated vehicle HPC.

---

## 📖 Demo Walkthrough (For Judges)
Since we cannot present live, we have documented our **Winning Demo Script** step-by-step.
👉 **[Click here to read the Full Demo Script](./DEMO_WALKTHROUGH.md)**

---

## 🛠️ Tech Stack
- **Frontend:** Streamlit, Plotly (3D & 2D Charts)
- **AI Core:** LangChain, Anthropic API, Groq API (Llama 3)
- **Standards:** COVESA VSS, SOME/IP, MISRA C++
- **Simulation:** Hash-based deterministic signal generation

---

## 💻 Installation & Setup

1.  **Clone the Repo:**
    ```bash
    git clone https://github.com/NAME-ASHWANIYADAV/GenAuto-SDV-Demo.git
    cd GenAuto-SDV-Demo
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the App:**
    ```bash
    streamlit run app.py
    ```

---

*© 2026 Team Greenbytes — DTU Delhi*
