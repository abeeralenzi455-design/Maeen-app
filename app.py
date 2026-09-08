import streamlit as st
import plotly.graph_objects as go
import time

# ============================================================
# 1. إعدادات الصفحة والهوية البصرية (RTL & Clean UI)
# ============================================================
st.set_page_config(
    page_title="مَعِين | MAEEN — Circular Dam Management",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تحسين المحاذاة والاتجاه العربي وتنسيق البطاقات
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;900&display=swap');

    html, body, [class*="css"], div, p, span, h1, h2, h3, h4 {
        font-family: 'Tajawal', sans-serif !important;
        direction: rtl;
        text-align: right;
        color: #EAF4F0;
    }
    .stApp {
        background-color: #081917;
    }
    /* الهيدر الرئيسي */
    .header-box {
        background: linear-gradient(135deg, #0E2622 0%, #04100E 100%);
        border: 1px solid rgba(232,244,240,0.18);
        border-radius: 12px;
        padding: 20px;
        text-align: right;
        margin-bottom: 15px;
    }
    .brand-title {
        font-size: 36px;
        font-weight: 900;
        color: #EAF4F0;
        margin: 0;
    }
    .brand-slogan {
        font-size: 15px;
        color: #D9C79E;
        font-weight: 700;
        margin-top: 5px;
    }
    /* بطاقة خطوات الديمو */
    .demo-step-card {
        background: linear-gradient(135deg, #0E2622 0%, #153B35 100%);
        border-right: 5px solid #63D4C8;
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .demo-step-title {
        font-size: 17px;
        font-weight: 700;
        color: #63D4C8;
        margin-bottom: 6px;
    }
    .demo-step-desc {
        font-size: 14px;
        color: #EAF4F0;
        margin: 0;
    }
    /* بطاقات العرض المقروءة */
    .info-card {
        background-color: #0E2622;
        border-right: 4px solid #63D4C8;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .info-card h4 {
        margin: 0 0 6px 0;
        color: #63D4C8;
        font-size: 16px;
    }
    .info-card p {
        margin: 0;
        color: #EAF4F0;
        font-size: 14px;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# 2. الهيدر وزر المحاكاة الحية (Live Demo Mode)
# ============================================================
col_header, col_demo = st.columns([3, 1])

with col_demo:
    st.write("") 
    st.write("")
    run_demo = st.button("▶️ تشغيل الديمو التفاعلي", type="primary", use_container_width=True)

with col_header:
    st.markdown("""
    <div class="header-box">
        <div class="brand-title">مَعِين <span style="font-size:14px; color:#63D4C8; letter-spacing:3px;">| MAEEN</span></div>
        <div class="brand-slogan">نحمي الماء، ونحوّل ما يهدد كفاءته إلى مورد.</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# 3. مساحة عرض خطوات الديمو التفاعلية أعلى الصفحة
# ============================================================
demo_placeholder = st.empty()

# ============================================================
# 4. القائمة الجانبية: التحكم والسيناريوهات
# ============================================================
st.sidebar.header("⚙️ محاكاة مدخلات السد")

preset = st.sidebar.radio(
    "اختر السيناريو (Preset):",
    ["مخصص (Custom)", "يوم طبيعي (Normal Day)", "أمطار غزيرة (Heavy Rain)", "تراكم حرج (Critical Event)"]
)

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
# 5. محرك الحسابات الهندسي
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
    risk_level = "آمن (SAFE)"
elif risk_score < 70:
    risk_level = "مراقبة (WATCH)"
elif risk_score < 85:
    risk_level = "مرتفع (HIGH)"
else:
    risk_level = "حرج (CRITICAL)"

# ============================================================
# 6. منطق تشغيل الديمو وعرض الخطوات أعلى الصفحة
# ============================================================
if run_demo:
    demo_steps = [
        {
            "step": "الخطوة 1: قراءة الحساسات والبيانات الهيدرولوجية 📡",
            "desc": f"جاري سحب القراءات اللحظية: التدفق ({inflow:.0f} m³/s) | معدل الهطول ({rainfall:.0f} mm) | مستوى المياه ({water_level:.1f}%)."
        },
        {
            "step": "الخطوة 2: تحليل مستويات العكارة والتراكم عبر الذكاء الاصطناعي 🧠",
            "desc": f"معالجة عكارة المياه ({turbidity:.1f} NTU) وحساب حجم الترسبات المتراكمة ({sediment_volume/1e6:.2f} مليون m³)."
        },
        {
            "step": "الخطوة 3: التنبؤ والتحقيق في المخاطر المستقبليّة 🔮",
            "desc": f"معدل خطورة النظام الحالي هو [{risk_level}]. التراكم المتوقع خلال 36 ساعة القادمة هو +{(sed_inflow * 0.05):,.0f} m³."
        },
        {
            "step": "الخطوة 4: تشغيل خوارزميات التوصية والاقتصاد الدائري 🛡️♻️",
            "desc": "تم تحديد الإجراء الوقائي المناسب واحتساب القيمة الاستردادية للرواسب بنجاح."
        }
    ]

    for idx, item in enumerate(demo_steps):
        demo_placeholder.markdown(f"""
        <div class="demo-step-card">
            <div class="demo-step-title">{item['step']}</div>
            <div class="demo-step-desc">{item['desc']}</div>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(2)
    
    # بعد انتهاء الديمو يتم عرض إشعار النجاح
    demo_placeholder.success("✅ اكتملت دورة التحليل والمحاكاة بنجاح!")

# ============================================================
# 7. التبويبات التفاعلية
# ============================================================
tab_overview, tab_prediction, tab_prevention, tab_reuse = st.tabs([
    "📊 مركز الذكاء والنظرة العامة", 
    "🔮 التنبؤ الذكي والتحقيق", 
    "🛡️ تقليل التراكم والتوصيات", 
    "♻️ الاسترداد والقيمة الدائرية"
])

# --- TAB 1 ---
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
        fig_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color': '#EAF4F0'}, height=260)
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col_chart2:
        st.subheader("🗺️ خريطة قرار مَعِين (Decision Map)")
        st.markdown(f"""
        <div class="info-card">
            <h4>📍 المنطقة الأكثر تأثراً</h4>
            <p>المنطقة A (قريبة من مدخل الخزان الرئيسي)</p>
        </div>
        <div class="info-card">
            <h4>🌊 معدل تدفق الرواسب</h4>
            <p>{sed_inflow:,.0f} متر مكعب / شهر</p>
        </div>
        <div class="info-card">
            <h4>⚡ حالة النظام</h4>
            <p>المستوى الحالي: <b>{risk_level}</b></p>
        </div>
        """, unsafe_allow_html=True)

# --- TAB 2 ---
with tab_prediction:
    st.subheader("🔮 التحقيق والتنبؤ الذكي (AI Investigation)")
    
    pred_36h = sed_inflow * 0.05
    p1, p2 = st.columns(2)
    p1.metric("التراكم المتوقع (36 ساعة)", f"+{pred_36h:,.0f} m³")
    p2.metric("الزيادة المتوقعة في فقدان السعة", f"+{(pred_36h/design_capacity)*100:.2f}%")

    st.divider()
    
    cause_text = "ارتفاع معدل الجريان الناتج عن زيادة الأمطار المحلية." if rainfall > inflow * 0.15 else "ارتفاع تدفق المياه القادم من أعلى الحوض دون هطول محلي كبير."

    st.markdown(f"""
    <div class="info-card">
        <h4>📍 أين المشكلة؟</h4>
        <p>ارتفاع تركيز المواد المحمولة والترسبات في المنطقة A.</p>
    </div>
    <div class="info-card">
        <h4>❓ ما السبب المحتمل؟</h4>
        <p>{cause_text}</p>
    </div>
    <div class="info-card">
        <h4>💡 لماذا يعتقد النظام ذلك؟</h4>
        <p>لأن التدفق ارتفع إلى <b>{inflow:.0f} م³/ثا</b>، بينما بلغت نسبة العكارة <b>{turbidity:.1f} NTU</b> وتركيز الرواسب <b>{sed_conc:.1f}</b>.</p>
    </div>
    """, unsafe_allow_html=True)

# --- TAB 3 ---
with tab_prevention:
    st.subheader("🛡️ التوصيات وتكتيكات الدفاع (MAEEN Defense)")
    
    if risk_score > 70:
        action = "تفعيل مصيدة الرواسب (Sediment Trap) + إجراء تصريف متحكم به"
        reduction = 45
    elif risk_score > 40:
        action = "إنشاء نطاق نباتي (Vegetation Zone) لتقليل سرعة الجريان"
        reduction = 25
    else:
        action = "استمرار المراقبة الدورية الوقائية (Routine Monitoring)"
        reduction = 10

    st.markdown(f"""
    <div class="info-card" style="border-right-color: #4FAE7A;">
        <h4>🎯 الإجراء الموصى به</h4>
        <p>{action}</p>
    </div>
    <div class="info-card" style="border-right-color: #E0A83E;">
        <h4>📉 الخفض المتوقع في نسبة الرواسب</h4>
        <p>{reduction}% عند تطبيق التوصية</p>
    </div>
    """, unsafe_allow_html=True)

# --- TAB 4 ---
with tab_reuse:
    st.subheader("♻️ تحليل العينات والاسترداد والاقتصاد الدائري")
    
    recovered_vol = sediment_volume * 0.06 * (1 + intervention_eff / 200)
    sand = min(60.0, max(15.0, 45.0 - sed_conc * 0.2))
    clay = min(40.0, max(8.0, 12.0 + sed_conc * 0.25))
    silt = max(5.0, 100.0 - sand - clay)
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="info-card">
            <h4>🧪 تركيبة العينة المستردة</h4>
            <p>• <b>رمال (Sand):</b> {sand:.1f}%</p>
            <p>• <b>طمي (Silt):</b> {silt:.1f}%</p>
            <p>• <b>طين (Clay):</b> {clay:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with c2:
        processing_cost = recovered_vol * 15
        material_val = recovered_vol * 35
        circular_val = max(0.0, material_val - processing_cost)
        
        st.markdown(f"""
        <div class="info-card" style="border-right-color: #D9C79E;">
            <h4>💰 القيمة الاقتصادية الدائرية</h4>
            <p>• <b>حجم المواد المستردة:</b> {recovered_vol:,.0f} m³</p>
            <p>• <b>صافي القيمة التقديرية:</b> {circular_val:,.0f} ريال سعودي</p>
        </div>
        """, unsafe_allow_html=True)

st.caption("MAEEN is a prototype decision-support simulation.")
