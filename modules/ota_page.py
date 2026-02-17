import streamlit as st
import time

# ============================================================
# OTA & DEPLOYMENT PAGE — Connected to AI Studio
# ============================================================

def render():
    
    service_ctx = st.session_state.get('generated_service', None)
    
    # --- Deployed Services Catalog ---
    st.markdown("### 📦 Deployed Service Catalog")
    st.caption("Services running on vehicle HPC — managed via SOME/IP Service Discovery")
    
    # Build service list from generated service
    services = []
    
    if service_ctx:
        svc_name = service_ctx['name'].replace(" ", "")[:25]
        loc_cpp = len(st.session_state.get('cpp_output', '').split('\n')) if st.session_state.get('cpp_output') else 0
        loc_total = service_ctx.get('total_loc', loc_cpp * 3)
        mem_est = max(8, loc_total // 30)
        cpu_est = round(max(0.5, loc_total / 500), 1)
        
        services.append({
            "name": svc_name,
            "version": "1.0.0",
            "status": "Running",
            "port": 30490,
            "protocol": "SOME/IP",
            "container": f"soa-{svc_name.lower()[:15]}",
            "cpu": f"{cpu_est}%",
            "mem": f"{mem_est} MB",
            "generated": True,
            "compliance": service_ctx['compliance'],
            "engine": service_ctx['llm_engine'],
        })
        
        st.success(f"🔗 **Your generated service is deployed:** {service_ctx['name']} | {service_ctx['compliance']}")
    else:
        st.info("💡 **Generate a service in AI Studio first** — it will appear here as a deployed container!")
    
    # Always show core infrastructure services
    infra_services = [
        {"name": "DiagnosticAggregator", "version": "2.0.1", "status": "Running", "port": 30493,
         "protocol": "SOME/IP + REST", "container": "soa-diagnostics", "cpu": "4.2%", "mem": "34 MB", "generated": False},
        {"name": "HMIDashboard", "version": "1.2.0", "status": "Running", "port": 8080,
         "protocol": "HTTP", "container": "soa-hmi", "cpu": "5.1%", "mem": "45 MB", "generated": False},
    ]
    services.extend(infra_services)
    
    for svc in services:
        badge = "🟢 **[AI Generated]**" if svc.get('generated') else "⚙️ Infrastructure"
        with st.expander(f"✅ **{svc['name']}** v{svc['version']} — {svc['status']} | {badge}"):
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Port", svc['port'])
            c2.metric("Protocol", svc['protocol'])
            c3.metric("CPU", svc['cpu'])
            c4.metric("Memory", svc['mem'])
            
            if svc.get('generated'):
                st.caption(f"Compliance: **{svc['compliance']}** | Engine: **{svc['engine']}**")
            
            st.code(f"docker ps --filter name={svc['container']}", language="bash")
    
    st.divider()
    
    # --- OTA Update Simulator ---
    st.markdown("### ☁️ OTA Update Simulator")
    st.caption("Deploy or update services via Over-The-Air")
    
    ota_col1, ota_col2 = st.columns([1, 1])
    
    with ota_col1:
        update_type = st.radio("Update Type", [
            "🆕 Deploy New Service",
            "🔄 Update Existing Service",
            "🔓 Unlock Subscription Feature"
        ])
        
        if update_type == "🆕 Deploy New Service":
            deploy_options = ["DrivingPatternAnalyzer v1.0.0 (12 MB)", "RangeOptimizer v1.0.0 (8 MB)"]
            if service_ctx:
                svc_name = service_ctx['name']
                deploy_options.insert(0, f"{svc_name} v1.0.0 (AI Generated)")
            st.selectbox("Select Package", deploy_options)
            
        elif update_type == "🔄 Update Existing Service":
            update_options = []
            if service_ctx:
                svc_name = service_ctx['name']
                update_options.append(f"{svc_name} v1.0.0 → v1.1.0 (patch: improved ML model)")
            update_options.append("DiagnosticAggregator v2.0.1 → v2.1.0")
            st.selectbox("Select Service", update_options)
        else:
            st.selectbox("Select Feature", [
                "Premium Range Analytics (₹299/mo)",
                "Predictive Maintenance Pro (₹499/mo)",
                "Advanced Driving Insights (₹199/mo)"
            ])
    
    with ota_col2:
        if st.button("🚀 Execute OTA Deployment", type="primary"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            log_area = st.empty()
            
            svc_display = service_ctx['name'] if service_ctx else "Service"
            
            steps = [
                (10, "📡 Connecting to OTA server..."),
                (20, "🔐 Verifying vehicle identity (X.509 cert)..."),
                (35, f"📥 Downloading {svc_display} package..."),
                (50, "🔍 Verifying integrity (SHA-256)..."),
                (60, "🛡️ Safety pre-checks (ISO 26262)..."),
                (70, f"🐳 Pulling container image..."),
                (80, "⚙️ Starting service container..."),
                (85, "🔌 SOME/IP Service Discovery registration..."),
                (90, "🧪 Post-deployment health check..."),
                (95, "📊 Updating service catalog..."),
                (100, "✅ OTA deployment complete!"),
            ]
            
            log_lines = []
            for progress, msg in steps:
                progress_bar.progress(progress)
                status_text.markdown(f"**{msg}**")
                log_lines.append(f"[{time.strftime('%H:%M:%S')}] {msg}")
                log_area.code("\n".join(log_lines), language="bash")
                time.sleep(0.4)
            
            st.success(f"🎉 **OTA Complete!** {svc_display} is live on vehicle HPC.")
            st.balloons()
    
    st.divider()
    
    # --- Feature Subscriptions ---
    st.markdown("### 🛒 Feature Subscription Management")
    
    features = [
        {"name": "Basic Diagnostics", "price": "Included", "status": True,
         "desc": f"{'Monitoring for ' + service_ctx['name'] if service_ctx else 'Basic vehicle monitoring'}"},
        {"name": "Premium Analytics", "price": "₹299/mo", "status": st.session_state.get('premium_unlocked', False),
         "desc": "AI-powered pattern analysis + optimization"},
        {"name": "Predictive Maintenance", "price": "₹499/mo", "status": st.session_state.get('predictive_unlocked', False),
         "desc": "Advanced failure prediction with 30-day forecast"},
        {"name": "Fleet Manager", "price": "₹799/mo", "status": False,
         "desc": "Multi-vehicle fleet health overview"},
    ]
    
    for feat in features:
        f1, f2, f3, f4 = st.columns([3, 1, 1, 2])
        with f1:
            st.markdown(f"**{feat['name']}**")
            st.caption(feat['desc'])
        with f2:
            st.markdown(f"**{feat['price']}**")
        with f3:
            if feat['status']:
                st.markdown("✅ Active")
            else:
                st.markdown("🔒 Locked")
        with f4:
            if not feat['status']:
                if st.button("Unlock", key=f"ota_unlock_{feat['name']}"):
                    st.info(f"Subscribing to {feat['name']}... Use OTA above to deploy!")
        st.divider()
    
    # --- Docker Orchestration ---
    st.markdown("### 🐙 Container Orchestration")
    st.caption("All SoA services running as Docker containers on vehicle HPC")
    
    # Build docker ps output from actual services
    docker_lines = "$ docker ps\nCONTAINER ID   IMAGE                    STATUS         PORTS        NAMES\n"
    total_cpu = 0.0
    total_mem = 0
    
    for i, svc in enumerate(services):
        container_id = f"{'abcdef'[i:i+1] * 4}{i+1}{'ghijk'[i:i+1] * 4}{i+2}"[:12]
        cpu_val = float(svc['cpu'].replace('%', ''))
        mem_val = int(svc['mem'].replace(' MB', ''))
        total_cpu += cpu_val
        total_mem += mem_val
        
        port_str = f"{svc['port']}/{'udp' if 'SOME' in svc['protocol'] else 'tcp'}"
        docker_lines += f"{container_id}   {svc['container']}:{svc['version']}{'  ':<3}Up 2 hours     {port_str:<12}{svc['container']}\n"
    
    st.code(docker_lines, language="bash")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Containers", str(len(services)))
    c2.metric("Total CPU Usage", f"{total_cpu:.1f}%")
    c3.metric("Total Memory", f"{total_mem} MB")
