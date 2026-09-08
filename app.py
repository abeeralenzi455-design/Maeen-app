import streamlit as st

st.set_page_config(page_title="MAEEN Engine Dashboard", page_icon="🌊", layout="wide")

st.title("🌊 MAEEN Engine - Decision & Predictive Control")
st.caption("Turbidity Calculations, Sediment Accumulation & Dam Risk Assessment")

st.sidebar.header("⚙️ Simulation Inputs")
water_level = st.sidebar.slider("Water Level (%)", 0.0, 100.0, 65.0)
rainfall = st.sidebar.slider("Rainfall Rate (mm)", 0.0, 300.0, 35.0)
inflow = st.sidebar.slider("Inflow Rate (m³/s)", 0.0, 1200.0, 260.0)
sediment_volume = st.sidebar.number_input("Current Sediment Volume (m³)", min_value=0.0, value=1240000.0, step=50000.0)

design_capacity = 10_000_000.0
turbidity = min(500.0, max(5.0, rainfall * 1.6 + inflow * 0.12))
sed_conc = min(100.0, max(0.0, turbidity * 0.16 + inflow * 0.012))
sed_inflow = max(0.0, (inflow * 0.85 + sed_conc * 175))
capacity_loss_pct = min(100.0, max(0.0, (sediment_volume / design_capacity) * 100))

risk_score = min(100.0, max(0.0, 
    water_level * 0.12 + 
    (rainfall / 200 * 100) * 0.18 + 
    (inflow / 1000 * 100) * 0.18 + 
    min(100.0, sed_inflow / 25000 * 100) * 0.27 + 
    capacity_loss_pct * 0.25
))

if risk_score < 40:
    risk_status = "SAFE"
elif risk_score < 70:
    risk_status = "WATCH"
elif risk_score < 85:
    risk_status = "HIGH"
else:
    risk_status = "CRITICAL"

col1, col2, col3, col4 = st.columns(4)
col1.metric("Risk Score", f"{risk_score:.1f}%", delta=risk_status)
col2.metric("Turbidity", f"{turbidity:.1f} NTU")
col3.metric("Sediment Inflow", f"{sed_inflow:,.0f} m³/mo")
col4.metric("Capacity Loss", f"{capacity_loss_pct:.1f}%")

st.divider()

st.subheader("💡 Recommended Structural Intervention")
if risk_score > 70:
    st.error("⚠️ High Risk: Deploy **Sediment Trap** and perform controlled sediment release.")
elif risk_score > 40:
    st.warning("⚡ Moderate Risk: Activate **Vegetation Zone** to attenuate flow velocity.")
else:
    st.success("✅ System Status Nominal. Routine monitoring active.")

st.divider()

st.subheader("🔬 Sediment Sample Analysis & Circular Economy")
if st.button("Run Sample Analysis"):
    sand = min(60.0, max(15.0, 45.0 - sed_conc * 0.2))
    clay = min(40.0, max(8.0, 12.0 + sed_conc * 0.25))
    silt = max(5.0, 100.0 - sand - clay)
    recovered_vol = sediment_volume * 0.06
    circular_val = recovered_vol * 15.0
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.write(f"- **Sand:** {sand:.1f}% | **Silt:** {silt:.1f}% | **Clay:** {clay:.1f}%")
    with col_b:
        st.write(f"- **Recovered Volume:** {recovered_vol:,.0f} m³")
        st.write(f"- **Estimated Circular Value:** {circular_val:,.2f} SAR")
