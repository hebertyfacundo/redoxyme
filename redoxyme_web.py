"""
REDOXYME WEB - A Calculator for Antioxidant Enzyme Activity
Web version of the original Redoxyme desktop application
"""

import streamlit as st
import math

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Redoxyme Web - Antioxidant Enzyme Calculator",
    page_icon="🧪",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E86AB;
        padding-bottom: 1rem;
        border-bottom: 2px solid #f0f0f0;
        margin-bottom: 2rem;
    }
    .enzyme-section {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid;
        margin-bottom: 1.5rem;
    }
    .cat-section { border-left-color: #2E86AB; }
    .gpx-section { border-left-color: #d17486; }
    .sod-section { border-left-color: #4CAF50; }
    .result-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 8px;
        padding: 1.2rem;
        margin-top: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# CALCULATION FUNCTIONS
# ============================================================================
def calculate_catalase(abs0, abs60, reaction_vol, sample_vol, protein_conc):
    """Catalase Activity Calculation"""
    try:
        R_abs = float(abs0) / float(abs60)
        Ln = math.log(R_abs)
        U = Ln / 60.0
        U_total = U * (float(reaction_vol) / float(sample_vol))
        result = U_total / float(protein_conc)
        return round(result, 4)
    except:
        return "Error: Check input values"

def calculate_gpx(abs0_sample, abs60_sample, abs0_blank, abs60_blank,
                  reaction_vol, sample_vol, dilution, extinction_coef, protein_conc):
    """Glutathione Peroxidase Activity Calculation"""
    try:
        delta_sample = float(abs0_sample) - float(abs60_sample)
        delta_blank = float(abs0_blank) - float(abs60_blank)
        delta_delta = delta_sample - delta_blank

        GPX1 = delta_delta / float(extinction_coef)
        volume_factor = (float(reaction_vol) / float(sample_vol)) * float(dilution) * 2
        GPX2 = GPX1 * volume_factor

        result = GPX2 / float(protein_conc)
        return round(result, 4)
    except:
        return "Error: Check input values"

def calculate_sod(abs_blank, abs_sample, reaction_vol, sample_vol, protein_conc):
    """Superoxide Dismutase Activity Calculation"""
    try:
        R_abs = (float(abs_blank) - float(abs_sample)) / float(abs_blank)
        unit_calc = R_abs / 0.5
        U = unit_calc * (float(reaction_vol) / float(sample_vol))
        result = U / float(protein_conc)
        return round(result, 4)
    except:
        return "Error: Check input values"

# ============================================================================
# MAIN INTERFACE
# ============================================================================
st.markdown('<h1 class="main-header">🧪 Redoxyme Web - A Calculator for Antioxidant Enzyme Activity</h1>',
            unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; margin-bottom: 2rem; color: #555;'>
    <p>Web-based calculator for antioxidant enzyme activity analysis</p>
    <p><small>Compatible with the original Redoxyme desktop application • Use decimal point (.) for numbers</small></p>
</div>
""", unsafe_allow_html=True)

calculator = st.selectbox(
    "**Select Enzyme Calculator**",
    ["Catalase (CAT)", "Glutathione Peroxidase (GPX)", "Superoxide Dismutase (SOD)"]
)

st.markdown("---")

# ============================================================================
# CATALASE CALCULATOR
# ============================================================================
if calculator == "Catalase (CAT)":
    st.markdown('<div class="enzyme-section cat-section">', unsafe_allow_html=True)
    st.subheader("🔬 Catalase Activity Calculator")
    st.caption("Method: H₂O₂ decomposition at 240 nm")

    col1, col2 = st.columns(2)

    with col1:
        cat_abs0 = st.number_input(
            "Absorbance at 0 seconds (A₀)",
            min_value=0.001,
            value=0.5,
            step=0.001,
            format="%.3f",
            help="Use decimal point: 0.5 not 0,5"
        )
        cat_abs60 = st.number_input(
            "Absorbance at 60 seconds (A₆₀)",
            min_value=0.001,
            value=0.3,
            step=0.001,
            format="%.3f"
        )
        cat_react_vol = st.number_input(
            "Total reaction volume (mL)",
            min_value=0.1,
            value=3.0,
            step=0.1,
            format="%.1f"
        )

    with col2:
        cat_sample_vol = st.number_input(
            "Sample volume (mL)",
            min_value=0.01,
            value=0.1,
            step=0.01,
            format="%.2f"
        )
        cat_protein = st.number_input(
            "Protein concentration (mg/mL)",
            min_value=0.001,
            value=1.0,
            step=0.001,
            format="%.3f",
            help="Use decimal point: 1.0 not 1,0"
        )

    if st.button("Calculate Catalase Activity", type="primary", key="cat_calc"):
        result = calculate_catalase(cat_abs0, cat_abs60, cat_react_vol, cat_sample_vol, cat_protein)

        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        st.markdown(f"### 🎯 **Catalase Activity:** {result} U/mg protein")
        st.markdown("""
        **Formula:** U/mg = [(ln(A₀/A₆₀)/60) × (V_reaction/V_sample)] ÷ [Protein]
        
        **Note:** One unit decomposes 1.0 μmol of H₂O₂ per minute at pH 7.0, 25°C
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# GPX CALCULATOR
# ============================================================================
elif calculator == "Glutathione Peroxidase (GPX)":
    st.markdown('<div class="enzyme-section gpx-section">', unsafe_allow_html=True)
    st.subheader("⚗️ Glutathione Peroxidase Calculator")
    st.caption("Method: NADPH oxidation at 340 nm")

    col1, col2 = st.columns(2)

    with col1:
        gpx_abs0_sample = st.number_input(
            "Sample - Initial absorbance",
            min_value=0.001,
            value=0.8,
            step=0.001,
            format="%.3f",
            help="Use decimal point: 0.8 not 0,8"
        )
        gpx_abs60_sample = st.number_input(
            "Sample - Final absorbance",
            min_value=0.001,
            value=0.4,
            step=0.001,
            format="%.3f"
        )
        gpx_abs0_blank = st.number_input(
            "Blank - Initial absorbance",
            min_value=0.001,
            value=0.8,
            step=0.001,
            format="%.3f"
        )
        gpx_abs60_blank = st.number_input(
            "Blank - Final absorbance",
            min_value=0.001,
            value=0.7,
            step=0.001,
            format="%.3f"
        )

    with col2:
        gpx_react_vol = st.number_input(
            "Total reaction volume (mL)",
            min_value=0.1,
            value=1.0,
            step=0.1,
            format="%.1f"
        )
        gpx_sample_vol = st.number_input(
            "Sample volume (mL)",
            min_value=0.01,
            value=0.1,
            step=0.01,
            format="%.2f"
        )
        gpx_dilution = st.number_input(
            "Dilution factor",
            min_value=1.0,
            value=1.0,
            step=0.1,
            format="%.1f"
        )
        gpx_coef = st.number_input(
            "Extinction coefficient (mM⁻¹cm⁻¹)",
            min_value=0.1,
            value=6.22,
            step=0.01,
            format="%.2f",
            help="For NADPH at 340 nm: 6.22 mM⁻¹cm⁻¹"
        )
        gpx_protein = st.number_input(
            "Protein concentration (mg/mL)",
            min_value=0.001,
            value=1.0,
            step=0.001,
            format="%.3f"
        )

    if st.button("Calculate GPX Activity", type="primary", key="gpx_calc"):
        result = calculate_gpx(gpx_abs0_sample, gpx_abs60_sample, gpx_abs0_blank,
                              gpx_abs60_blank, gpx_react_vol, gpx_sample_vol,
                              gpx_dilution, gpx_coef, gpx_protein)

        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        st.markdown(f"### 🎯 **GPX Activity:** {result} U/mg protein")
        st.markdown("""
        **Formula:** U/mg = [ΔΔA/ε × (V_reaction/V_sample) × Dilution × 2] ÷ [Protein]
        
        **Note:** One unit oxidizes 1.0 μmol of NADPH per minute at 25°C
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# SOD CALCULATOR
# ============================================================================
else:
    st.markdown('<div class="enzyme-section sod-section">', unsafe_allow_html=True)
    st.subheader("🧪 Superoxide Dismutase Calculator")
    st.caption("Method: NBT reduction inhibition at 560 nm")

    col1, col2 = st.columns(2)

    with col1:
        sod_abs_blank = st.number_input(
            "Blank tube absorbance",
            min_value=0.001,
            value=0.25,
            step=0.001,
            format="%.3f",
            help="Use decimal point: 0.25 not 0,25"
        )
        sod_abs_sample = st.number_input(
            "Sample tube absorbance",
            min_value=0.001,
            value=0.15,
            step=0.001,
            format="%.3f"
        )
        sod_react_vol = st.number_input(
            "Total reaction volume (mL)",
            min_value=0.1,
            value=3.0,
            step=0.1,
            format="%.1f"
        )

    with col2:
        sod_sample_vol = st.number_input(
            "Sample volume (mL)",
            min_value=0.01,
            value=0.1,
            step=0.01,
            format="%.2f"
        )
        sod_protein = st.number_input(
            "Protein concentration (mg/mL)",
            min_value=0.001,
            value=1.0,
            step=0.001,
            format="%.3f"
        )

    if st.button("Calculate SOD Activity", type="primary", key="sod_calc"):
        result = calculate_sod(sod_abs_blank, sod_abs_sample, sod_react_vol,
                              sod_sample_vol, sod_protein)

        inhibition = ((sod_abs_blank - sod_abs_sample) / sod_abs_blank) * 100

        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        st.markdown(f"### 🎯 **SOD Activity:** {result} U/mg protein")
        st.markdown(f"**Inhibition:** {inhibition:.2f}%")
        st.markdown("""
        **Formula:** U/mg = [((A_blank - A_sample)/A_blank)/0.5 × (V_reaction/V_sample)] ÷ [Protein]
        
        **Note:** One unit causes 50% inhibition of NBT reduction
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9rem; padding: 1rem;'>
    <p>🧪 <strong>Redoxyme Web - A Calculator for Antioxidant Enzyme Activity</strong></p>
    <p>📌 Web version based on original Redoxyme formulas • Use decimal point (.) for numbers</p>
    <p>🔗 <a href='https://github.com/hebertyfacundo/redoxyme' target='_blank'>View original project on GitHub</a></p>
</div>
""", unsafe_allow_html=True)