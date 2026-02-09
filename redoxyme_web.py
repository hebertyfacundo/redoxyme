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
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 8px;
        padding: 1rem;
        margin-top: 1rem;
        color: #721c24;
    }
    .reference-box {
        background-color: #e9ecef;
        border-left: 4px solid #6c757d;
        padding: 1rem;
        margin-top: 2rem;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================
def validate_number_input(value, field_name):
    """Validate if input is a valid number with decimal point"""
    if value is None or value == "":
        return False, f"{field_name}: Field cannot be empty"

    try:
        # Convert string to float, handling comma as decimal separator
        str_value = str(value).strip()
        if ',' in str_value:
            str_value = str_value.replace(',', '.')

        float_value = float(str_value)

        if float_value <= 0:
            return False, f"{field_name}: Value must be greater than 0"

        return True, float_value
    except ValueError:
        return False, f"{field_name}: Must be a valid number (use decimal point '.')"

def validate_all_inputs(inputs_dict):
    """Validate all inputs in a dictionary"""
    errors = []
    validated_values = {}

    for field_name, value in inputs_dict.items():
        is_valid, result = validate_number_input(value, field_name)
        if not is_valid:
            errors.append(result)
        else:
            validated_values[field_name] = result

    return len(errors) == 0, errors, validated_values

# ============================================================================
# CALCULATION FUNCTIONS
# ============================================================================
def calculate_catalase(abs0, abs60, reaction_vol, sample_vol, protein_conc):
    """Catalase Activity Calculation"""
    try:
        R_abs = abs0 / abs60
        Ln = math.log(R_abs)
        U = Ln / 60.0
        U_total = U * (reaction_vol / sample_vol)
        result = U_total / protein_conc
        return round(result, 4), None
    except Exception as e:
        return None, f"Calculation error: {str(e)}"

def calculate_gpx(abs0_sample, abs60_sample, abs0_blank, abs60_blank,
                  reaction_vol, sample_vol, dilution, extinction_coef, protein_conc):
    """Glutathione Peroxidase Activity Calculation"""
    try:
        delta_sample = abs0_sample - abs60_sample
        delta_blank = abs0_blank - abs60_blank
        delta_delta = delta_sample - delta_blank

        GPX1 = delta_delta / extinction_coef
        volume_factor = (reaction_vol / sample_vol) * dilution * 2
        GPX2 = GPX1 * volume_factor

        result = GPX2 / protein_conc
        return round(result, 4), None
    except Exception as e:
        return None, f"Calculation error: {str(e)}"

def calculate_sod(abs_blank, abs_sample, reaction_vol, sample_vol, protein_conc):
    """Superoxide Dismutase Activity Calculation"""
    try:
        R_abs = (abs_blank - abs_sample) / abs_blank
        unit_calc = R_abs / 0.5
        U = unit_calc * (reaction_vol / sample_vol)
        result = U / protein_conc
        return round(result, 4), None
    except Exception as e:
        return None, f"Calculation error: {str(e)}"

# ============================================================================
# MAIN INTERFACE
# ============================================================================
st.markdown('<h1 class="main-header">🧪 Redoxyme Web - A Calculator for Antioxidant Enzyme Activity</h1>',
            unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; margin-bottom: 2rem; color: #555;'>
    <p>Web-based calculator for antioxidant enzyme activity analysis</p>
    <p><small>Compatible with the original Redoxyme desktop application • All fields must be filled with numbers</small></p>
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
        cat_abs0 = st.text_input(
            "Absorbance at 0 seconds (A₀)",
            value="",
            help="Enter a number using decimal point (e.g., 0.5)"
        )
        cat_abs60 = st.text_input(
            "Absorbance at 60 seconds (A₆₀)",
            value="",
            help="Enter a number using decimal point (e.g., 0.3)"
        )
        cat_react_vol = st.text_input(
            "Total reaction volume (mL)",
            value="",
            help="Enter a number using decimal point (e.g., 3.0)"
        )

    with col2:
        cat_sample_vol = st.text_input(
            "Sample volume (mL)",
            value="",
            help="Enter a number using decimal point (e.g., 0.1)"
        )
        cat_protein = st.text_input(
            "Protein concentration (mg/mL)",
            value="",
            help="Enter a number using decimal point (e.g., 1.0)"
        )

    if st.button("Calculate Catalase Activity", type="primary", key="cat_calc"):
        # Validate inputs
        inputs = {
            "Absorbance at 0 seconds": cat_abs0,
            "Absorbance at 60 seconds": cat_abs60,
            "Total reaction volume": cat_react_vol,
            "Sample volume": cat_sample_vol,
            "Protein concentration": cat_protein
        }

        is_valid, errors, validated = validate_all_inputs(inputs)

        if not is_valid:
            st.markdown('<div class="error-box">', unsafe_allow_html=True)
            st.markdown("### ❌ Validation Errors:")
            for error in errors:
                st.markdown(f"- {error}")
            st.markdown("**Please correct the errors and try again.**")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            # Perform calculation
            result, calc_error = calculate_catalase(
                validated["Absorbance at 0 seconds"],
                validated["Absorbance at 60 seconds"],
                validated["Total reaction volume"],
                validated["Sample volume"],
                validated["Protein concentration"]
            )

            if calc_error:
                st.markdown('<div class="error-box">', unsafe_allow_html=True)
                st.markdown(f"### ❌ {calc_error}")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
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
        gpx_abs0_sample = st.text_input(
            "Sample - Initial absorbance",
            value="",
            help="Enter a number using decimal point (e.g., 0.8)"
        )
        gpx_abs60_sample = st.text_input(
            "Sample - Final absorbance",
            value="",
            help="Enter a number using decimal point (e.g., 0.4)"
        )
        gpx_abs0_blank = st.text_input(
            "Blank - Initial absorbance",
            value="",
            help="Enter a number using decimal point (e.g., 0.8)"
        )
        gpx_abs60_blank = st.text_input(
            "Blank - Final absorbance",
            value="",
            help="Enter a number using decimal point (e.g., 0.7)"
        )

    with col2:
        gpx_react_vol = st.text_input(
            "Total reaction volume (mL)",
            value="",
            help="Enter a number using decimal point (e.g., 1.0)"
        )
        gpx_sample_vol = st.text_input(
            "Sample volume (mL)",
            value="",
            help="Enter a number using decimal point (e.g., 0.1)"
        )
        gpx_dilution = st.text_input(
            "Dilution factor",
            value="",
            help="Enter a number using decimal point (e.g., 1.0)"
        )
        gpx_coef = st.text_input(
            "Extinction coefficient (mM⁻¹cm⁻¹)",
            value="",
            help="For NADPH at 340 nm: 6.22 mM⁻¹cm⁻¹ (use decimal point)"
        )
        gpx_protein = st.text_input(
            "Protein concentration (mg/mL)",
            value="",
            help="Enter a number using decimal point (e.g., 1.0)"
        )

    if st.button("Calculate GPX Activity", type="primary", key="gpx_calc"):
        # Validate inputs
        inputs = {
            "Sample initial absorbance": gpx_abs0_sample,
            "Sample final absorbance": gpx_abs60_sample,
            "Blank initial absorbance": gpx_abs0_blank,
            "Blank final absorbance": gpx_abs60_blank,
            "Total reaction volume": gpx_react_vol,
            "Sample volume": gpx_sample_vol,
            "Dilution factor": gpx_dilution,
            "Extinction coefficient": gpx_coef,
            "Protein concentration": gpx_protein
        }

        is_valid, errors, validated = validate_all_inputs(inputs)

        if not is_valid:
            st.markdown('<div class="error-box">', unsafe_allow_html=True)
            st.markdown("### ❌ Validation Errors:")
            for error in errors:
                st.markdown(f"- {error}")
            st.markdown("**Please correct the errors and try again.**")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            # Perform calculation
            result, calc_error = calculate_gpx(
                validated["Sample initial absorbance"],
                validated["Sample final absorbance"],
                validated["Blank initial absorbance"],
                validated["Blank final absorbance"],
                validated["Total reaction volume"],
                validated["Sample volume"],
                validated["Dilution factor"],
                validated["Extinction coefficient"],
                validated["Protein concentration"]
            )

            if calc_error:
                st.markdown('<div class="error-box">', unsafe_allow_html=True)
                st.markdown(f"### ❌ {calc_error}")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
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
        sod_abs_blank = st.text_input(
            "Blank tube absorbance",
            value="",
            help="Enter a number using decimal point (e.g., 0.25)"
        )
        sod_abs_sample = st.text_input(
            "Sample tube absorbance",
            value="",
            help="Enter a number using decimal point (e.g., 0.15)"
        )
        sod_react_vol = st.text_input(
            "Total reaction volume (mL)",
            value="",
            help="Enter a number using decimal point (e.g., 3.0)"
        )

    with col2:
        sod_sample_vol = st.text_input(
            "Sample volume (mL)",
            value="",
            help="Enter a number using decimal point (e.g., 0.1)"
        )
        sod_protein = st.text_input(
            "Protein concentration (mg/mL)",
            value="",
            help="Enter a number using decimal point (e.g., 1.0)"
        )

    if st.button("Calculate SOD Activity", type="primary", key="sod_calc"):
        # Validate inputs
        inputs = {
            "Blank tube absorbance": sod_abs_blank,
            "Sample tube absorbance": sod_abs_sample,
            "Total reaction volume": sod_react_vol,
            "Sample volume": sod_sample_vol,
            "Protein concentration": sod_protein
        }

        is_valid, errors, validated = validate_all_inputs(inputs)

        if not is_valid:
            st.markdown('<div class="error-box">', unsafe_allow_html=True)
            st.markdown("### ❌ Validation Errors:")
            for error in errors:
                st.markdown(f"- {error}")
            st.markdown("**Please correct the errors and try again.**")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            # Perform calculation
            result, calc_error = calculate_sod(
                validated["Blank tube absorbance"],
                validated["Sample tube absorbance"],
                validated["Total reaction volume"],
                validated["Sample volume"],
                validated["Protein concentration"]
            )

            if calc_error:
                st.markdown('<div class="error-box">', unsafe_allow_html=True)
                st.markdown(f"### ❌ {calc_error}")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                # Calculate inhibition percentage
                inhibition = ((validated["Blank tube absorbance"] - validated["Sample tube absorbance"]) /
                            validated["Blank tube absorbance"]) * 100

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
# FOOTER WITH REFERENCE
# ============================================================================
st.markdown("---")

st.markdown("""
<div class="reference-box">
<h4>📚 Citation & References</h4>

<p><strong>Preprint (biorxiv):</strong><br>
Redoxyme: A Calculator for Antioxidant Enzyme Activity<br>
<em>Available at:</em> https://www.biorxiv.org/content/10.64898/2026.02.05.703993v1</p>

<p><strong>How to cite this web tool:</strong><br>
Facundo, H.T. (2026). Redoxyme Web: A Calculator for Antioxidant Enzyme Activity [Web application]. Retrieved from https://redoxyme.streamlit.app</p>

<p><strong>Peer-reviewed publication:</strong><br>
<em>[To be updated upon publication in a peer-reviewed journal]</em></p>

<p><strong>Source Code:</strong><br>
GitHub: https://github.com/hebertyfacundo/redoxyme</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9rem; padding: 1rem;'>
    <p>🧪 <strong>Redoxyme Web - A Calculator for Antioxidant Enzyme Activity</strong></p>
    <p>📌 Web version based on original Redoxyme formulas • All fields must be filled with valid numbers</p>
    <p>🔗 <a href='https://github.com/hebertyfacundo/redoxyme' target='_blank'>View source code on GitHub</a></p>
</div>
""", unsafe_allow_html=True)
