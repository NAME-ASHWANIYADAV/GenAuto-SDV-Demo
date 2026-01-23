import streamlit as st
import plotly.graph_objects as go
import random
import time
from collections import deque
import datetime

# --- Configuration ---
st.set_page_config(
    page_title="GenAuto-SDV Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Dark Theme Styling (using markdown and st.markdown for CSS injection) ---
st.markdown(
    """
    <style>
    .reportview-container {
        background: #1e1e1e;
        color: #f0f2f6;
    }
    .sidebar .sidebar-content {
        background: #2f2f2f;
        color: #f0f2f6;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 10px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
    }
    .stTextArea, .stTextInput {
        background-color: #3e3e3e;
        color: #f0f2f6;
        border: 1px solid #555;
    }
    .stCode {
        background-color: #333;
        color: #00ff00;
        font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
        border-radius: 5px;
        padding: 10px;
    }
    .stProgress > div > div > div > div {
        background-color: #4CAF50;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #00ccff; /* A futuristic blue */
    }
    .metric-card {
        background-color: #2f2f2f;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
    }
    .metric-value {
        font-size: 3em;
        font-weight: bold;
        color: #fff;
    }
    .metric-label {
        font-size: 1em;
        color: #aaa;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Sidebar (The GenAI Engineer Interface) ---
st.sidebar.title("GenAuto-SDV | GenAI Engineer Interface")

with st.sidebar:
    st.markdown("### Task Definition")
    user_prompt = st.text_area(
        "Describe the automotive service/feature you want to generate:",
        "Create a Battery Health Monitor Service with predictive analytics for thermal runaway prevention.",
        height=150
    )

    simulation_mode = st.checkbox("Enable Simulation Mode", value=True)

    if st.button("Generate & Deploy Service", key="generate_deploy_btn"):
        st.subheader("Deployment Log")
        progress_bar = st.progress(0)
        status_text = st.empty()

        steps = [
            ("Parsing Requirements...", 25),
            ("Generating MISRA C++ Code...", 50),
            ("Validating with Physics Engine (ISO 26262 Compliant)...", 75),
            ("Deploying via OTA (SOME/IP Connected)...", 100)
        ]

        for i, (step_msg, progress_val) in enumerate(steps):
            status_text.info(step_msg)
            progress_bar.progress(progress_val)
            time.sleep(1) # Simulate work

        status_text.success("Deployment Complete: Service 'BatteryHealthMonitor' Deployed Successfully!")
        st.balloons()

        st.markdown("---")
        st.subheader("Generated C++ Code (Snippet)")
        # Placeholder for generated C++ code
        cpp_code_snippet = """
#include <iostream>
#include <string>
#include <vector>
#include <memory>
#include "someip_client.h" // Assume SOME/IP library

// MISRA C++ 2012 compliant code example
// Rule 8-5-1: All functions should have a single point of exit.
// Rule 7-1-1: Octal constants shall not be used.

class BatteryModule {
public:
    explicit BatteryModule(int id) : module_id_(id), temperature_(25.0f), voltage_(3.7f) {}

    void update_telemetry(float temp, float volt) {
        temperature_ = temp;
        voltage_ = volt;
        // Additional MISRA compliance checks and error handling
    }

    float get_temperature() const { return temperature_; }
    float get_voltage() const { return voltage_; }

private:
    int module_id_;
    float temperature_;
    float voltage_;
};

class BatteryHealthMonitor {
public:
    BatteryHealthMonitor(std::unique_ptr<SOMEIPClient> client)
        : someip_client_(std::move(client)), health_score_(100.0) {
        // Initialize connections, subscribe to SOME/IP events
        if (someip_client_) {
            someip_client_->connect("192.168.1.100", 30501);
            someip_client_->subscribe("BatteryTelemetryService", "BatteryUpdateEvent");
        }
    }

    void analyze_data(const std::vector<BatteryModule>& modules) {
        // Complex predictive analytics for thermal runaway
        float avg_temp = 0.0f;
        for (const auto& module : modules) {
            avg_temp += module.get_temperature();
        }
        avg_temp /= static_cast<float>(modules.size());

        if (avg_temp > 60.0f) {
            std::cout << "[WARNING] Anomaly Detected: High Battery Temperature!" << std::endl;
            health_score_ -= 0.5;
        } else {
            health_score_ = std::min(100.0, health_score_ + 0.1); // Gradual recovery
        }
        // Publish health score via SOME/IP
        if (someip_client_) {
            someip_client_->publish("BatteryHealthService", "HealthScoreEvent", std::to_string(health_score_));
        }
    }

    double get_health_score() const { return health_score_; }

private:
    std::unique_ptr<SOMEIPClient> someip_client_;
    double health_score_;
};

// Placeholder for SOME/IP Client
class SOMEIPClient {
public:
    void connect(const std::string& ip, int port) {
        std::cout << "SOME/IP Client connected to " << ip << ":" << port << std::endl;
    }
    void subscribe(const std::string& service, const std::string& event) {
        std::cout << "Subscribed to " << service << ":" << event << std::endl;
    }
    void publish(const std::string& service, const std::string& event, const std::string& payload) {
        std::cout << "Published to " << service << ":" << event << " with payload: " << payload << std::endl;
    }
};

int main() {
    // Example usage
    std::unique_ptr<SOMEIPClient> client = std::make_unique<SOMEIPClient>();
    BatteryHealthMonitor monitor(std::move(client));

    std::vector<BatteryModule> modules;
    modules.emplace_back(1);
    modules.emplace_back(2);

    // Simulate some updates
    modules[0].update_telemetry(random_float(20.0f, 30.0f), random_float(3.5f, 4.0f));
    modules[1].update_telemetry(random_float(20.0f, 30.0f), random_float(3.5f, 4.0f));

    monitor.analyze_data(modules);
    std::cout << "Current Battery Health Score: " << monitor.get_health_score() << std::endl;

    return 0; // Single point of exit
}
float random_float(float min, float max) {
    return min + static_cast<float>(rand()) / (static_cast<float>(RAND_MAX / (max - min)));
}
"""
        st.code(cpp_code_snippet, language="cpp")

# --- Main Dashboard (The Vehicle Visualization) ---
st.title("GenAuto-SDV | Live Telemetry & Health Monitoring")
st.markdown("Automotive Software Defined Vehicle (SDV) Platform - **SOME/IP Connected, ISO 26262 Compliant**")

# --- Top Row (Metrics) ---
st.markdown("## Real-time Vehicle Metrics")
col1, col2, col3, col4 = st.columns(4)

# Initial dummy data
if 'vehicle_speed' not in st.session_state:
    st.session_state.vehicle_speed = 0
if 'battery_soc' not in st.session_state:
    st.session_state.battery_soc = 85
if 'tire_pressure' not in st.session_state:
    st.session_state.tire_pressure = 35
if 'system_latency' not in st.session_state:
    st.session_state.system_latency = 15

with col1:
    st.markdown(f"<div class='metric-card'><div class='metric-label'>Vehicle Speed</div><div class='metric-value' style='color:#FF4B4B;'>{st.session_state.vehicle_speed} km/h</div></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='metric-card'><div class='metric-label'>Battery SoC</div><div class='metric-value' style='color:#6AFF6A;'>{st.session_state.battery_soc} %</div></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='metric-card'><div class='metric-label'>Tire Pressure</div><div class='metric-value' style='color:#FFD700;'>{st.session_state.tire_pressure} PSI</div></div>", unsafe_allow_html=True)
with col4:
    st.markdown(f"<div class='metric-card'><div class='metric-label'>System Latency</div><div class='metric-value' style='color:#ADD8E6;'>{st.session_state.system_latency} ms</div></div>", unsafe_allow_html=True)

# --- Middle Row (Live Graphs) ---
st.markdown("## Predictive Analytics & Performance")
col5, col6 = st.columns(2)

# Data for live graphs
if 'rpm_data' not in st.session_state:
    st.session_state.rpm_data = deque([random.uniform(500, 1500) for _ in range(30)], maxlen=60)
if 'torque_data' not in st.session_state:
    st.session_state.torque_data = deque([random.uniform(50, 150) for _ in range(30)], maxlen=60)
if 'time_data' not in st.session_state:
    st.session_state.time_data = deque([datetime.datetime.now() - datetime.timedelta(seconds=i) for i in range(30)], maxlen=60)
if 'battery_health_score' not in st.session_state:
    st.session_state.battery_health_score = 90

with col5:
    st.subheader("Motor Torque vs. RPM")
    fig_torque_rpm = go.Figure(
        data=[
            go.Scatter(y=list(st.session_state.torque_data), x=list(st.session_state.time_data), mode='lines', name='Torque (Nm)', line=dict(color='yellow')),
            go.Scatter(y=list(st.session_state.rpm_data), x=list(st.session_state.time_data), mode='lines', name='RPM', yaxis='y2', line=dict(color='cyan'))
        ],
        layout=go.Layout(
            height=400,
            template="plotly_dark",
            margin=dict(l=20, r=20, t=30, b=20),
            xaxis=dict(title='Time', showgrid=True, gridcolor='#333', gridwidth=0.5),
            yaxis=dict(title='Torque (Nm)', showgrid=True, gridcolor='#333', gridwidth=0.5, range=[0, 200]),
            yaxis2=dict(title='RPM', overlaying='y', side='right', showgrid=False, range=[0, 2500]),
            legend=dict(x=0, y=1.1, orientation="h")
        )
    )
    torque_rpm_chart = st.plotly_chart(fig_torque_rpm, use_container_width=True)

with col6:
    st.subheader("Battery Health Prediction")
    fig_battery_health = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=st.session_state.battery_health_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Battery Health Score (%)"},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "#6AFF6A"}, # Green for good health
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 40], 'color': '#FF4B4B'}, # Red for low
                    {'range': [40, 70], 'color': '#FFD700'}, # Yellow for medium
                    {'range': [70, 100], 'color': '#6AFF6A'} # Green for high
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 80 # Example threshold
                }
            }
        ),
        layout=go.Layout(
            height=400,
            template="plotly_dark",
            margin=dict(l=20, r=20, t=30, b=20)
        )
    )
    battery_health_gauge = st.plotly_chart(fig_battery_health, use_container_width=True)

# --- Bottom Row (Logs) ---
st.markdown("## System Logs")
log_container = st.empty()

if 'system_logs' not in st.session_state:
    st.session_state.system_logs = deque(maxlen=20)

def generate_log_message():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    log_types = ["INFO", "WARNING", "ERROR", "DEBUG"]
    services = ["TireMonitor", "ADAS_Controller", "PowerMgmt", "Infotainment", "OTA_Updater"]
    messages = [
        "Service: {} started successfully.".format(random.choice(services)),
        "Telemetry data received from sensor: {}".format(random.randint(1, 12)),
        "Alert: Prediction Model Confidence {}%".format(random.randint(90, 99)),
        "System check: All subsystems nominal.",
        "Anomaly Detected in {} module!".format(random.choice(["Battery", "Motor", "Brake"])),
        "Firmware update available for {}",
        "SOME/IP message handler processing event."
    ]
    log_type = random.choice(log_types)
    message = random.choice(messages)
    return f"[{current_time}] [{log_type}] {message}"

# --- Live Data Simulation Loop ---
if simulation_mode:
    # Update metrics
    st.session_state.vehicle_speed = int(random.uniform(0, 120))
    st.session_state.battery_soc = int(random.uniform(20, 100))
    st.session_state.tire_pressure = int(random.uniform(30, 40))
    st.session_state.system_latency = int(random.uniform(5, 50))

    # Update graph data
    new_rpm = random.uniform(500, 2000)
    new_torque = random.uniform(50, 180)
    new_time = datetime.datetime.now()
    st.session_state.rpm_data.append(new_rpm)
    st.session_state.torque_data.append(new_torque)
    st.session_state.time_data.append(new_time)

    # Update battery health (simulate fluctuation)
    current_health = st.session_state.battery_health_score
    change = random.uniform(-0.5, 0.5)
    st.session_state.battery_health_score = max(70, min(100, current_health + change)) # Keep it between 70-100 for PoC

    # Add a new log message
    st.session_state.system_logs.append(generate_log_message())

    # Display logs
    log_messages_str = "\n".join(st.session_state.system_logs)
    log_container.text_area("Live System Output", log_messages_str, height=200, key="system_logs_display")

    # Rerun the script every second to update live data
    time.sleep(1)
    st.rerun()
else:
    log_messages_str = "\n".join(st.session_state.system_logs)
    log_container.text_area("Live System Output", log_messages_str, height=200, key="system_logs_display")
    st.info("Simulation Mode is OFF. Data will not update.")
