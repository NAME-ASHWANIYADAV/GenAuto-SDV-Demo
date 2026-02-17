import streamlit as st
import time
import plotly.graph_objects as go

# ============================================================
# SERVICE-AWARE SIGNAL DEFINITIONS
# ============================================================

SERVICE_SIGNAL_PROFILES = {
    "tire": {
        "name": "Tire Pressure Monitoring",
        "icon": "🛞",
        "primary_signals": [
            {"name": "FL Tire", "vss": "Vehicle.Chassis.Axle.Row1.Wheel.Left.Tire.Pressure", "unit": "PSI", "min": 28, "max": 36, "normal_min": 30, "normal_max": 35},
            {"name": "FR Tire", "vss": "Vehicle.Chassis.Axle.Row1.Wheel.Right.Tire.Pressure", "unit": "PSI", "min": 28, "max": 36, "normal_min": 30, "normal_max": 35},
            {"name": "RL Tire", "vss": "Vehicle.Chassis.Axle.Row2.Wheel.Left.Tire.Pressure", "unit": "PSI", "min": 28, "max": 36, "normal_min": 30, "normal_max": 35},
            {"name": "RR Tire", "vss": "Vehicle.Chassis.Axle.Row2.Wheel.Right.Tire.Pressure", "unit": "PSI", "min": 28, "max": 36, "normal_min": 30, "normal_max": 35},
        ],
        "predictions": [
            {"name": "Tire Failure Risk", "model": "tire_failure_rf.pkl", "unit": "%", "base": 3.5, "good_below": 10},
            {"name": "Tire Wear", "model": "tire_wear_cnn.pkl", "unit": "%", "base": 12.0, "good_below": 50},
            {"name": "Next Replace", "model": "tire_life_lstm.pkl", "unit": "km", "base": 18500, "good_below": None},
        ],
        "tips": [
            "Maintain pressure between 32-35 PSI for optimal tread life",
            "Check pressure when tires are cold (not driven >3km)",
            "Rotate tires every 8,000 km for even wear",
        ],
    },
    "battery": {
        "name": "Battery SOH Analyzer",
        "icon": "🔋",
        "primary_signals": [
            {"name": "Voltage", "vss": "Vehicle.Powertrain.TractionBattery.Voltage", "unit": "V", "min": 340, "max": 420, "normal_min": 360, "normal_max": 410},
            {"name": "Current", "vss": "Vehicle.Powertrain.TractionBattery.Current", "unit": "A", "min": -150, "max": 150, "normal_min": -100, "normal_max": 100},
            {"name": "Temperature", "vss": "Vehicle.Powertrain.TractionBattery.Temperature", "unit": "°C", "min": 15, "max": 55, "normal_min": 20, "normal_max": 45},
            {"name": "SoC", "vss": "Vehicle.Powertrain.TractionBattery.StateOfCharge", "unit": "%", "min": 5, "max": 100, "normal_min": 20, "normal_max": 100},
        ],
        "predictions": [
            {"name": "State of Health", "model": "battery_soh_xgb.pkl", "unit": "%", "base": 94.2, "good_below": None},
            {"name": "Lifespan", "model": "battery_life_lstm.pkl", "unit": "years", "base": 6.3, "good_below": None},
            {"name": "Degradation", "model": "battery_deg_rf.pkl", "unit": "%/yr", "base": 2.1, "good_below": 3},
        ],
        "tips": [
            "Avoid charging above 80% for daily use (extends life 20%)",
            "Keep battery between 20-35°C for optimal SOH",
            "Minimize fast charging (>50kW) to reduce degradation",
        ],
    },
    "motor": {
        "name": "Motor Health Monitor",
        "icon": "⚙️",
        "primary_signals": [
            {"name": "Motor Temp", "vss": "Vehicle.Powertrain.ElectricMotor.Temperature", "unit": "°C", "min": 30, "max": 120, "normal_min": 40, "normal_max": 90},
            {"name": "RPM", "vss": "Vehicle.Powertrain.ElectricMotor.Speed", "unit": "RPM", "min": 0, "max": 12000, "normal_min": 0, "normal_max": 10000},
            {"name": "Vibration", "vss": "Vehicle.Powertrain.ElectricMotor.Vibration", "unit": "mm/s", "min": 0, "max": 10, "normal_min": 0, "normal_max": 4.5},
            {"name": "Efficiency", "vss": "Vehicle.Powertrain.ElectricMotor.TorqueEfficiency", "unit": "%", "min": 80, "max": 99, "normal_min": 90, "normal_max": 99},
        ],
        "predictions": [
            {"name": "Motor Health", "model": "motor_health_rf.pkl", "unit": "%", "base": 96.1, "good_below": None},
            {"name": "Bearing Wear", "model": "bearing_cnn.pkl", "unit": "%", "base": 4.2, "good_below": 20},
            {"name": "Failure Risk", "model": "motor_fail_lstm.pkl", "unit": "%", "base": 0.8, "good_below": 5},
        ],
        "tips": [
            "Motor temp above 100°C indicates thermal stress",
            "Vibration >4.5 mm/s suggests bearing inspection",
            "Torque efficiency drop >5% = winding degradation",
        ],
    },
    "default": {
        "name": "Vehicle Service Monitor",
        "icon": "🚗",
        "primary_signals": [
            {"name": "Speed", "vss": "Vehicle.Speed", "unit": "km/h", "min": 0, "max": 240, "normal_min": 0, "normal_max": 180},
            {"name": "Throttle", "vss": "Vehicle.Powertrain.CombustionEngine.Throttle", "unit": "%", "min": 0, "max": 100, "normal_min": 0, "normal_max": 80},
            {"name": "Brake", "vss": "Vehicle.Chassis.Brake.PedalPosition", "unit": "%", "min": 0, "max": 100, "normal_min": 0, "normal_max": 100},
            {"name": "Steering", "vss": "Vehicle.Chassis.SteeringWheel.Angle", "unit": "°", "min": -540, "max": 540, "normal_min": -180, "normal_max": 180},
        ],
        "predictions": [
            {"name": "Health Score", "model": "service_health.pkl", "unit": "%", "base": 92.0, "good_below": None},
            {"name": "Anomaly", "model": "anomaly_det.pkl", "unit": "%", "base": 2.5, "good_below": 10},
            {"name": "Maintenance", "model": "maint_pred.pkl", "unit": "km", "base": 14000, "good_below": None},
        ],
        "tips": [
            "Monitor signal thresholds for optimal performance",
            "Schedule diagnostics based on AI predictions",
        ],
    },
}


def detect_service_type(description):
    """Detect service type from description keywords."""
    desc = description.lower()
    if any(w in desc for w in ["tire", "tyre", "pressure", "tpms", "wheel"]):
        return "tire"
    elif any(w in desc for w in ["battery", "soh", "charge", "voltage", "soc"]):
        return "battery"
    elif any(w in desc for w in ["motor", "vibration", "bearing", "torque", "rpm"]):
        return "motor"
    return "default"


def init_simulation_data(profile, variant):
    """Initialize stable simulation values in session_state (NOT random on every render)."""
    import hashlib, struct
    
    key = f"sim_data_{profile['name']}_{variant}"
    if key not in st.session_state:
        # Generate deterministic but realistic values using hash
        seed_str = f"{profile['name']}_{variant}_{time.strftime('%Y%m%d%H')}"
        h = hashlib.md5(seed_str.encode()).digest()
        
        signal_values = []
        for i, sig in enumerate(profile["primary_signals"]):
            # Deterministic value within normal range
            frac = struct.unpack('B', h[i:i+1])[0] / 255.0
            center = (sig["normal_min"] + sig["normal_max"]) / 2
            spread = (sig["normal_max"] - sig["normal_min"]) / 2
            value = center + (frac - 0.5) * spread * 1.2
            value = max(sig["min"], min(sig["max"], round(value, 1)))
            signal_values.append(value)
        
        pred_values = []
        for i, pred in enumerate(profile["predictions"]):
            # Use base value with slight deterministic offset
            frac = struct.unpack('B', h[8+i:9+i])[0] / 255.0
            offset = (frac - 0.5) * pred["base"] * 0.1
            pred_values.append(round(pred["base"] + offset, 1))
        
        # Generate trend data (deterministic)
        trend = []
        base_val = signal_values[0] if signal_values else 32
        for j in range(50):
            frac = struct.unpack('B', h[(j % 16):(j % 16)+1])[0] / 255.0
            trend.append(round(base_val + (frac - 0.5) * 3, 1))
        
        st.session_state[key] = {
            "signal_values": signal_values,
            "pred_values": pred_values,
            "trend": trend,
            "speed": int(struct.unpack('B', h[12:13])[0] / 255.0 * 80 + 40),
            "steering": round((struct.unpack('B', h[13:14])[0] / 255.0 - 0.5) * 60, 1),
            "ev_range": int(struct.unpack('B', h[14:15])[0] / 255.0 * 140 + 180),
            "fuel": int(struct.unpack('B', h[15:16])[0] / 255.0 * 55 + 30),
        }
    
    return st.session_state[key]


def create_gauge(value, min_val, max_val, color, suffix=""):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number={"suffix": suffix, "font": {"size": 22, "color": "white"}},
        gauge={
            "axis": {"range": [min_val, max_val], "tickcolor": "#8b949e", "tickfont": {"color": "#8b949e", "size": 10}},
            "bar": {"color": color},
            "bgcolor": "#21262d",
            "borderwidth": 0,
        },
    ))
    fig.update_layout(
        height=150, margin=dict(l=20, r=20, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)", font={"color": "#c9d1d9"},
    )
    return fig


def create_3d_digital_twin(highlight_part):
    """Generate a high-tech 3D point cloud of the vehicle with active subsystem highlighted."""
    import numpy as np
    
    # Generate vehicle shape (simplified coupe)
    x, y, z = [], [], []
    colors = []
    sizes = []
    
    # Grid/Road (Base holographic plane)
    for i in range(-25, 25, 5):
        for j in range(-15, 15, 5):
             x.append(i); y.append(j); z.append(-2); colors.append('#1a202c'); sizes.append(2)

    # Chassis points (BRIGHT GREY for visibility)
    for i in range(-20, 20, 2):
        for j in range(-8, 8, 2):
            # Floor
            x.append(i); y.append(j); z.append(0); colors.append('#a0aec0'); sizes.append(4)
            # Roof
            if -10 < i < 10 and -6 < j < 6:
                x.append(i); y.append(j); z.append(10); colors.append('#a0aec0'); sizes.append(4)
    
    # Wheels (Very bright)
    wheels = [(-15, -8, 2), (-15, 8, 2), (15, -8, 2), (15, 8, 2)]
    for wx, wy, wz in wheels:
        is_highlight = highlight_part == 'tire'
        c = '#00ffff' if is_highlight else '#e2e8f0' # Cyan or White
        s = 15 if is_highlight else 8
        
        # Draw wheel clusters
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                 x.append(wx+dx); y.append(wy+dy); z.append(wz); colors.append(c); sizes.append(s)
        
        # Add glow if highlighted (Huge glow points)
        if is_highlight:
             x.append(wx); y.append(wy); z.append(wz); colors.append('#e0f2fe'); sizes.append(35) 

    # Battery Pack (Bright Green)
    if highlight_part == 'battery':
        for i in range(-6, 6, 2):
            for j in range(-4, 4, 2):
                x.append(i); y.append(j); z.append(1); colors.append('#00ff00'); sizes.append(10)
        # Core glow
        x.append(0); y.append(0); z.append(1); colors.append('#ccffdd'); sizes.append(40)
    
    # Motor (Bright Orange)
    if highlight_part == 'motor':
        for j in range(-4, 4, 2):
            x.append(14); y.append(j); z.append(2); colors.append('#ff9900'); sizes.append(12)
        # Core glow
        x.append(14); y.append(0); z.append(2); colors.append('#ffeebb'); sizes.append(40)

    fig = go.Figure(data=[go.Scatter3d(
        x=x, y=y, z=z,
        mode='markers',
        marker=dict(size=sizes, color=colors, opacity=1.0, line=dict(width=0))
    )])
    
    fig.update_layout(
        scene=dict(
            xaxis=dict(visible=False, showbackground=False),
            yaxis=dict(visible=False, showbackground=False),
            zaxis=dict(visible=False, showbackground=False),
            bgcolor='rgba(0,0,0,0)',
            aspectmode='data',
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.5)) # Better angle
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=350,
        showlegend=False
    )
    return fig


# ============================================================
# MAIN RENDER
# ============================================================

def render():
    service_ctx = st.session_state.get('generated_service', None)
    
    if service_ctx:
        service_type = detect_service_type(service_ctx['description'])
        profile = SERVICE_SIGNAL_PROFILES[service_type]
        st.success(f"🔗 **Live runtime of:** {service_ctx['name']} | Engine: {service_ctx['llm_engine']} | {service_ctx['compliance']}")
    else:
        service_type = "default"
        profile = SERVICE_SIGNAL_PROFILES["default"]
        st.info("💡 **Generate a service in AI Studio first** — this dashboard will show its live runtime data!")
    
    variant = st.selectbox("🚗 Vehicle Variant", ["EV", "Hybrid", "ICE"], index=0, key="dash_variant")
    
    # Initialize stable simulation data
    sim = init_simulation_data(profile, variant)
    
    # --- Top metrics ---
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Connection", "Active ✅")
    m2.metric("SOME/IP", "Port 30490")
    latency = 8 + (len(profile["primary_signals"]))
    m3.metric("Data Latency", f"{latency} ms")
    m4.metric("Service", f"{profile['icon']} {profile['name'][:20]}")
    
    st.divider()

    # --- DIGITAL TWIN & SIGNALS ---
    col_twin, col_sigs = st.columns([1, 2])
    
    with col_twin:
        st.markdown("##### 🧬 Digital Twin State")
        st.plotly_chart(create_3d_digital_twin(service_type), use_container_width=True)
        st.caption("Real-time VSS state synchronization")
    
    with col_sigs:
        st.markdown(f"##### 📡 {profile['icon']} Live Telemetry")
        if service_ctx:
            st.caption(f"Source: **{service_ctx['name']}** (Container ID: a1b2c3d4)")
        
        # Grid of signals
        sig_cols = st.columns(2)
        for i, sig in enumerate(profile["primary_signals"]):
            value = sim["signal_values"][i]
            
            if sig["normal_min"] <= value <= sig["normal_max"]:
                color = "#00ff88"
            elif value < sig["normal_min"]:
                color = "#ffaa00"
            else:
                color = "#ff4444"
            
            with sig_cols[i % 2]:
                st.plotly_chart(create_gauge(value, sig["min"], sig["max"], color, f" {sig['unit']}"), use_container_width=True)

    
    # --- CORE VEHICLE SIGNALS ---
    st.markdown("### 🚗 Core Vehicle Signals")
    
    vc1, vc2, vc3, vc4 = st.columns(4)
    vc1.metric("Speed", f"{sim['speed']} km/h", "VSS: Vehicle.Speed")
    vc2.metric("Gear", "D", "VSS: Vehicle.Powertrain.Transmission")
    vc3.metric("Steering", f"{sim['steering']}°", "← Left" if sim['steering'] < 0 else "→ Right")
    
    if variant == "EV":
        vc4.metric("EV Range", f"{sim['ev_range']} km", "VSS: Vehicle.Powertrain.Range")
    elif variant == "Hybrid":
        vc4.metric("Battery SoC", f"{min(85, sim['fuel'] + 20)}%", "VSS: Vehicle.Powertrain.Battery.SoC")
    else:
        vc4.metric("Fuel Level", f"{sim['fuel']}%", "VSS: Vehicle.Powertrain.FuelSystem")
    
    st.divider()
    
    # --- AI PREDICTIONS ---
    st.markdown(f"### 🤖 AI Predictions — {profile['name']}")
    
    pred_cols = st.columns(len(profile["predictions"]))
    for i, pred in enumerate(profile["predictions"]):
        val = sim["pred_values"][i]
        
        if pred["good_below"] is not None:
            status_icon = "🟢" if val < pred["good_below"] else "🔴"
        else:
            status_icon = "🟢"
        
        with pred_cols[i]:
            st.metric(f"{status_icon} {pred['name']}", f"{val} {pred['unit']}")
            st.caption(f"Model: `{pred['model']}` | Inference: {5 + i * 3}ms")
    
    st.divider()
    
    # --- SIGNAL TREND ---
    st.markdown(f"### 📈 Signal Trend — {profile['primary_signals'][0]['name']} (Last 50 readings)")
    
    sig = profile["primary_signals"][0]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y=sim["trend"], mode="lines", name=sig["name"],
        line=dict(color="#00e5ff", width=2),
        fill="tozeroy", fillcolor="rgba(0,229,255,0.1)"
    ))
    fig.add_hline(y=sig["normal_max"], line_dash="dash", line_color="#ffaa00",
                  annotation_text=f"Upper ({sig['normal_max']} {sig['unit']})")
    fig.add_hline(y=sig["normal_min"], line_dash="dash", line_color="#ff4444",
                  annotation_text=f"Lower ({sig['normal_min']} {sig['unit']})")
    
    fig.update_layout(
        height=280, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#8b949e"}, xaxis=dict(gridcolor="#21262d", title="Reading"),
        yaxis=dict(gridcolor="#21262d", title=f"{sig['unit']}"),
        margin=dict(l=50, r=20, t=20, b=50), showlegend=False
    )
    st.plotly_chart(fig)
    
    st.divider()
    
    # --- DRIVING ANALYTICS ---
    st.markdown("### 🏎️ Driving Analytics")
    
    an1, an2 = st.columns(2)
    
    with an1:
        # Score based on actual signal health
        healthy = sum(1 for i, s in enumerate(profile["primary_signals"]) 
                      if s["normal_min"] <= sim["signal_values"][i] <= s["normal_max"])
        score = int(healthy / len(profile["primary_signals"]) * 100)
        
        st.metric("Efficiency Score", f"{score} / 100")
        st.progress(score / 100)
        
        if score >= 75:
            st.success("✅ All signals within normal range")
        else:
            st.warning("⚠️ Some signals need attention")
    
    with an2:
        st.markdown(f"##### 💡 {profile['name']} Tips:")
        for tip in profile["tips"]:
            st.markdown(f"• {tip}")
    
    st.divider()
    
    # --- SUBSCRIPTION STORE ---
    st.markdown("### 🛒 Feature Subscription Store (OTA)")
    
    subs = [
        {"name": f"{profile['icon']} Basic Diagnostics", "active": True, "price": "Included"},
        {"name": "📊 Premium Analytics", "active": False, "price": "₹299/mo"},
        {"name": "🤖 Predictive Maintenance", "active": False, "price": "₹499/mo"},
    ]
    
    sub_cols = st.columns(3)
    for i, sub in enumerate(subs):
        with sub_cols[i]:
            if sub["active"]:
                st.markdown(f"""
<div style="background:linear-gradient(135deg,#1a2e1a,#1a3a1a);border:1px solid #238636;
border-radius:10px;padding:15px;text-align:center;">
    <h4 style="color:#00ff88;">{sub['name']}</h4>
    <p style="color:#8b949e;">✅ Active — {sub['price']}</p>
</div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
<div style="background:linear-gradient(135deg,#1a1f2e,#21262d);border:1px solid #30363d;
border-radius:10px;padding:15px;text-align:center;">
    <h4 style="color:#8b949e;">{sub['name']}</h4>
    <p style="color:#8b949e;">🔒 {sub['price']}</p>
</div>""", unsafe_allow_html=True)
                if st.button(f"🔓 Unlock", key=f"dash_unlock_{i}"):
                    st.balloons()
                    st.success(f"✅ {sub['name']} unlocked via OTA!")
    
    # --- DATA PIPELINE ---
    st.divider()
    with st.expander("🔄 Data Transformation Pipeline", expanded=False):
        c1, c2, c3, c4 = st.columns(4)
        sig0 = profile['primary_signals'][0]
        with c1:
            st.markdown(f"**📡 Raw CAN**\n```\nID: 0x185\nBytes: [48 00 1C A0]\n```")
        with c2:
            st.markdown(f"**🔢 DBC Decode**\n```\nFactor: 0.01\nOffset: 0\nParsed: Float\n```")
        with c3:
            st.markdown(f"**🌐 VSS Signal**\n```\n{sig0['vss'][-30:]}\nValue: {sim['signal_values'][0]} {sig0['unit']}\n```")
        with c4:
            st.markdown("**📊 SOME/IP**\n```\nService: 0x1234\nMethod: 0x0001\nPublished ✅\n```")
