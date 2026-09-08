import streamlit as st
import plotly.graph_objects as go

# ============================================================
# 1. إعدادات الصفحة والهوية البصرية (Custom CSS)
# ============================================================
st.set_page_config(
    page_title="مَعِين | MAEEN — Circular Dam Management",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تطبيق التنسيقات الخاصة بمنظومة مَعِين (الألوان الغامقة والخطوط)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Tajawal', sans-serif;
        background-color: #081917;
        color: #EAF4F0;
    }
    .stApp {
        background-color: #081917;
    }
    /* الهيدر والتعريف بالمنصة */
    .header-box {
        background: linear-gradient(135deg, #0E2622 0%, #04100E 100%);
        border: 1px solid rgba(232,244,240,0.18);
        border-radius: 8px;
        padding: 24px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    .brand-title {
        font-size: 42px;
        font-weight: 900;
        color: #EAF4F0;
        margin-bottom: 0px;
        letter-spacing: 1px;
    }
    .brand-sub {
        font-size: 13px;
        letter-spacing: 6px;
        color: #63D4C8;
        font-weight: 500;
        margin-bottom: 12px;
    }
    .brand-slogan {
        font-size: 18px;
        color: #D9C79E;
        font-weight: 700;
        margin-bottom: 8px;
    }
    .brand-desc {
        font-size: 14px;
        color: #9CB6B0;
        max-width: 680px;
        margin: 0 auto;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# 2. الواجهة الرئيسية: اسم المنصة والتعريف بها
# ============================================================
st.markdown("""
<div class="header-box">
    <div class="brand-title">مَعِين</div>
    <div class="brand-sub">M A E E N</div>
    <div class="brand-slogan">نحمي الماء، ونحوّل ما يهدد كفاءته إلى مورد.</div>
    <div class="brand-desc">
        منظومة ذكية تستبق تراكم المواد المحمولة مع مياه الأمطار والسيول، 
        وتحوّل بيانات السد إلى تنبؤات وقرارات وقيمة مستدامة.
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# 3. القائمة الجانبية: التحكم والسيناريوهات
# ============================================================
st.sidebar.header("⚙️ محاكاة مدخلات السد")

preset = st.sidebar.radio(
    "اختر السيناريو (Preset):",
    ["مخصص (Custom)", "يوم طبيعي (Normal Day)", "أمطار غزيرة (Heavy Rain)", "تراكم حرج (Critical Event)"]
)

# تعيين قيم المحاكاة المسبقة
if preset == "يوم طبيعي (Normal Day)":
    init_wl, init_rf, init_inf, init_sed = 60.0, 15.0, 140.0, 420000.0
elif preset == "أمطار غزيرة (Heavy Rain)":
    init_wl, init_rf, init_inf, init_sed = 74.0, 120.0, 600.0, 900000.0
elif preset == "تراكم حرج (Critical Event)":
    init_wl, init_rf, init_inf, init_sed = 88.0, 180.0, 900.0, 1650000.0
else:
    init_wl, init_rf, init_inf, init_sed = 65.0, 35.0, 260.0, 1240000.0

water_level = st.sidebar.slider("مستوى المياه (Water Level %)", 0.0, 100.0, init_wl)
rainfall = st.sidebar.slider("معدل الأمطار (Rainfall mm)", 0.0, 200.0, init_rf)
inflow = st.sidebar.slider("معدل التدفق (Inflow m³/s)", 0.0, 1000.0, init_inf)
sediment_volume = st.sidebar.number_input("حجم الرواسب الحالية (m³)", min_value=0.0, max_value=2000000.0, value=init_sed, step=50000.0)
intervention_eff = st.sidebar.slider("كفاءة التدخل (Intervention Efficiency %)", 0.0, 100.0, 0.0)

# ============================================================
# 4. محرك الحسابات الهندسي (MAEEN Engine Calculations)
# ============================================================
design_capacity = 10_000_000.0
turbidity = min(500.0, max(5.0, rainfall * 1.6 + inflow * 0.12))
sed_conc = min(100.0, max(0.0, turbidity * 0.16 + inflow * 0.012))
sed_inflow = max(0.0, (inflow * 0.85 + sed_conc * 175) * (1 - intervention_eff / 100.0))
capacity_loss_pct = min(100.0, max(0.0, (sediment_volume / design_capacity) * 100))
effective_capacity = design_capacity - sediment_volume

risk_score = min(100.0, max(0.0, 
    water_level * 0.12 + 
    (rainfall / 200 * 100) * 0.18 + 
    (inflow / 1000 * 100) * 0.18 + 
    min(100.0, sed_inflow / 25000 * 100) * 0.27 + 
    capacity_loss_pct * 0.25
))

if risk_score < 40:
    risk_level, risk_color = "SAFE", "#4FAE7A"
elif risk_score < 70:
    risk_level, risk_color = "WATCH", "#E0A83E"
elif risk_score < 85:
    risk_level, risk_color = "HIGH", "#E0813F"
else:
    risk_level, risk_color = "CRITICAL", "#DB4C4C"

# ============================================================
# 5. التبويبات التفاعلية للمنظومة
# ============================================================
tab_overview, tab_prediction, tab_prevention, tab_reuse = st.tabs([
    "📊 مركز الذكاء والنظرة العامة", 
    "🔮 التنبؤ الذكي والتحقيق", 
    "🛡️ تقليل التراكم والتوصيات", 
    "♻️ الاسترداد والقيمة الدائرية"
])

# --- TAB 1: OVERVIEW ---
with tab_overview:
    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("مستوى المياه", f"{water_level:.1f}%")
    k2.metric("السعة الفعالة", f"{effective_capacity/1e6:.2f}M m³")
    k3.metric("الرواسب المتراكمة", f"{sediment_volume/1e6:.2f}M m³")
    k4.metric("فقدان السعة", f"{capacity_loss_pct:.1f}%")
    k5.metric("مستوى الخطر", risk_level)

    st.divider()

    col_chart1, col_chart2 = st.columns([1, 1])

    with col_chart1:
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=risk_score,
            title={'text': "مؤشر الخطر اللحظي (Risk Gauge)"},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "#EAF4F0"},
                'steps': [
                    {'range': [0, 40], 'color': "#4FAE7A"},
                    {'range': [40, 70], 'color': "#E0A83E"},
                    {'range': [70, 85], 'color': "#E0813F"},
                    {'range': [85, 100], 'color': "#DB4C4C"}
                ],
            }
        ))
        fig_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color': '#EAF4F0'}, height=280)
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col_chart2:
        st.subheader("🗺️ خريطة قرار مَعِين (MAEEN Decision Map)")
        st.info(f"📍 **المنطقة الأكثر تأثراً:** المنطقة A (قريبة من مدخل الخزان)")
        st.warning(f"🌊 **معدل تدفق الرواسب:** {sed_inflow:,.0f} m³/شهر")
        st.error(f"⚡ **مستوى الخطورة الحالي:** {risk_level}")

# --- TAB 2: PREDICTION ---
with tab_prediction:
    st.subheader("🔮 التحقيق والتنبؤ الذكي (AI Investigation)")
    
    pred_36h = sed_inflow * 0.05
    col_p1, col_p2 = st.columns(2)
    col_p1.metric("التراكم المتوقع خلال 36 ساعة", f"+{pred_36h:,.0f} m³")
    col_p2.metric("الزيادة المتوقعة في فقدان السعة", f"+{(pred_36h/design_capacity)*100:.2f}%")

    st.markdown("### 🔍 نتائج التحقيق الذكي (AI Investigation)")
    cause_text = "ارتفاع معدل الجريان الناتج عن زيادة الأمطار المحلية." if rainfall > inflow * 0.15 else "ارتفاع تدفق المياه القادم من أعلى الحوض دون هطول محلي كبير."
    
    st.write(f"**أين المشكلة؟** ارتفاع تركيز المواد المحمولة في المنطقة A.")
    st.write(f"**ما السبب المحتمل؟** {cause_text}")
    st.write(f"**لماذا يعتقد النظام ذلك؟** لأن التدفق ارتفع إلى {inflow:.0f} م³/ثا بينما بلغت العكارة {turbidity:.1f} NTU وتركيز الرواسب {sed_conc:.1f}.")

# --- TAB 3: PREVENTION ---
with tab_prevention:
    st.subheader("🛡️ التوصيات وتكتيكات الدفاع (MAEEN Defense)")
    
    if risk_score > 70:
        action = "مصيدة رواسب (Sediment Trap) + تصريف متحكم به"
        reduction = 45
    elif risk_score > 40:
        action = "نطاق نباتي (Vegetation Zone) لتقليل السرعة"
        reduction = 25
    else:
        action = "مراقبة دورية وقائية (Routine Monitoring)"
        reduction = 10

    st.success(f"🎯 **الإجراء الموصى به:** {action}")
    st.info(f"📉 **الخفض المتوقع في الرواسب:** {reduction}%")

# --- TAB 4: REUSE & RECOVERY ---
with tab_reuse:
    st.subheader("♻️ تحليل العينات والاسترداد والاقتصاد الدائري")
    
    recovered_vol = sediment_volume * 0.06 * (1 + intervention_eff / 200)
    
    sand = min(60.0, max(15.0, 45.0 - sed_conc * 0.2))
    clay = min(40.0, max(8.0, 12.0 + sed_conc * 0.25))
    silt = max(5.0, 100.0 - sand - clay)
    
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        st.write("#### 🧪 تركيبة العينة المستردة")
        st.write(f"- **رمال (Sand):** {sand:.1f}%")
        st.write(f"- **طمي (Silt):** {silt:.1f}%")
        st.write(f"- **طين (Clay):** {clay:.1f}%")
    
    with col_r2:
        processing_cost = recovered_vol * 15
        material_val = recovered_vol * 35
        circular_val = max(0.0, material_val - processing_cost)
        
        st.write("#### 💰 القيمة الاقتصادية الدائرية المقدرة")
        st.write(f"- **حجم المواد المستردة:** {recovered_vol:,.0f} m³")
        st.metric("صافي القيمة الدائرية (Estimated Circular Value)", f"{circular_val:,.0f} SAR")

# Footer
st.caption("MAEEN is a prototype decision-support simulation. — بيانات اصطناعية بالكامل، لا تمثل أي سد حقيقي.")
