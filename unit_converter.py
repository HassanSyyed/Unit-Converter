# type: ignore
import streamlit as st
import pandas as pd
from typing import Dict, List

# Page configuration
st.set_page_config(
    page_title="Professional Unit Converter",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #2c3e50;
        transform: translateY(-2px);
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    .title-text {
        font-size: 2.5rem;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .category-text {
        font-size: 1.5rem;
        color: #34495e;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Conversion dictionaries
CONVERSIONS = {
    "Length": {
        "Meters": 1,
        "Kilometers": 1000,
        "Centimeters": 0.01,
        "Millimeters": 0.001,
        "Miles": 1609.34,
        "Yards": 0.9144,
        "Feet": 0.3048,
        "Inches": 0.0254,
        "Nautical Miles": 1852
    },
    "Weight/Mass": {
        "Kilograms": 1,
        "Grams": 0.001,
        "Milligrams": 0.000001,
        "Metric Tons": 1000,
        "Pounds": 0.453592,
        "Ounces": 0.0283495,
        "Stone": 6.35029
    },
    "Temperature": {
        "Celsius": "C",
        "Fahrenheit": "F",
        "Kelvin": "K"
    },
    "Area": {
        "Square Meters": 1,
        "Square Kilometers": 1000000,
        "Square Miles": 2589988.11,
        "Square Yards": 0.836127,
        "Square Feet": 0.092903,
        "Acres": 4046.86,
        "Hectares": 10000
    },
    "Volume": {
        "Cubic Meters": 1,
        "Liters": 0.001,
        "Milliliters": 0.000001,
        "Cubic Feet": 0.0283168,
        "Cubic Inches": 0.0000163871,
        "Gallons (US)": 0.00378541,
        "Quarts (US)": 0.000946353,
        "Pints (US)": 0.000473176,
        "Fluid Ounces (US)": 0.0000295735
    },
    "Speed": {
        "Meters per Second": 1,
        "Kilometers per Hour": 0.277778,
        "Miles per Hour": 0.44704,
        "Knots": 0.514444,
        "Feet per Second": 0.3048
    },
    "Time": {
        "Seconds": 1,
        "Minutes": 60,
        "Hours": 3600,
        "Days": 86400,
        "Weeks": 604800,
        "Months": 2592000,
        "Years": 31536000
    },
    "Digital Storage": {
        "Bytes": 1,
        "Kilobytes": 1024,
        "Megabytes": 1048576,
        "Gigabytes": 1073741824,
        "Terabytes": 1099511627776
    },
    "Energy": {
        "Joules": 1,
        "Kilojoules": 1000,
        "Calories": 4.184,
        "Kilocalories": 4184,
        "Watt-hours": 3600,
        "Kilowatt-hours": 3600000,
        "Electron-volts": 1.602177e-19
    },
    "Pressure": {
        "Pascal": 1,
        "Kilopascal": 1000,
        "Bar": 100000,
        "PSI": 6894.76,
        "Atmosphere": 101325,
        "Millimeter of Mercury": 133.322
    }
}

def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    """Special conversion for temperature units."""
    # Convert to Celsius first
    if from_unit == "Fahrenheit":
        celsius = (value - 32) * 5/9
    elif from_unit == "Kelvin":
        celsius = value - 273.15
    else:
        celsius = value
        
    # Convert from Celsius to target unit
    if to_unit == "Fahrenheit":
        return (celsius * 9/5) + 32
    elif to_unit == "Kelvin":
        return celsius + 273.15
    return celsius

def create_visualization(value: float, result: float, from_unit: str, to_unit: str, category: str):
    """Create a simple bar chart visualization for the conversion."""
    df = pd.DataFrame({
        'Unit': [from_unit, to_unit],
        'Value': [value, result]
    })
    return df

# Main app
st.markdown('<p class="title-text">Professional Unit Converter</p>', unsafe_allow_html=True)

# Sidebar for category selection
category = st.sidebar.selectbox(
    "Select Conversion Category",
    list(CONVERSIONS.keys())
)

# Main conversion interface
col1, col2 = st.columns(2)

with col1:
    st.markdown(f'<p class="category-text">{category} Converter</p>', unsafe_allow_html=True)
    
    # Input value
    value = st.number_input("Enter Value", value=1.0)
    
    # Unit selection
    from_unit = st.selectbox("From Unit", list(CONVERSIONS[category].keys()))
    to_unit = st.selectbox("To Unit", list(CONVERSIONS[category].keys()))
    
    # Convert button
    if st.button("Convert"):
        if category == "Temperature":
            result = convert_temperature(value, from_unit, to_unit)
        else:
            # For other conversions
            result = value * CONVERSIONS[category][from_unit] / CONVERSIONS[category][to_unit]
        
        # Display result
        st.success(f"{value:,.4f} {from_unit} = {result:,.4f} {to_unit}")
        
        # Create and display visualization
        with col2:
            st.markdown(f'<p class="category-text">Visualization</p>', unsafe_allow_html=True)
            df = create_visualization(value, result, from_unit, to_unit, category)
            st.bar_chart(df.set_index('Unit'))

# Additional information
with st.expander("ℹ️ About this Converter"):
    st.markdown("""
    This professional unit converter supports multiple categories of conversion:
    - Length (9 units)
    - Weight/Mass (7 units)
    - Temperature (3 units)
    - Area (7 units)
    - Volume (9 units)
    - Speed (5 units)
    - Time (7 units)
    - Digital Storage (5 units)
    - Energy (7 units)
    - Pressure (6 units)
    
    Features:
    - Real-time conversion
    - Interactive visualizations
    - Support for scientific notation
    - High precision calculations
    - User-friendly interface
    """)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>Made with ❤️❤️ using Streamlit</p>
        <p style='font-size: 0.8rem'>© 2025 Professional Unit Converter</p>
    </div>
    """,
    unsafe_allow_html=True
) 