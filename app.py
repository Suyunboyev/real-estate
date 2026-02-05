import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json

# Sahifa konfiguratsiyasi
st.set_page_config(
    page_title="Ko'chmas Mulk Baholash AI",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# YANGILANGAN CSS - KATTA VA YORQIN! 
st.markdown("""
<style>
    /* Asosiy fon - qora-ko'k */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }
    
    /* BARCHA SARLAVHALAR - JUDA KATTA! */
    h1 {
        color: #00ffff !important;
        font-size: 4rem !important;
        font-weight: 900 !important;
        text-shadow: 0 0 20px rgba(0,255,255,0.5);
        margin-bottom: 1.5rem !important;
    }
    
    h2 {
        color: #00ff88 !important;
        font-size: 2.8rem !important;
        font-weight: 800 !important;
        margin-top: 2rem !important;
    }
    
    h3 {
        color: #fbbf24 !important;
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        margin-bottom: 1rem !important;
    }
    
    /* ODDIY MATN - KATTA */
    p, div, span, label, li {
        color: #f1f5f9 !important;
        font-size: 1.4rem !important;
        line-height: 1.8 !important;
        font-weight: 500 !important;
    }
    
    /* METRIKLAR - SUPER KATTA! */
    .stMetric {
        background: linear-gradient(135deg, #7c3aed 0%, #2563eb 100%);
        padding: 30px !important;
        border-radius: 20px !important;
        border: 3px solid #00ffff !important;
        box-shadow: 0 0 30px rgba(0,255,255,0.4);
        transition: all 0.3s ease;
    }
    
    .stMetric:hover {
        transform: translateY(-8px);
        box-shadow: 0 0 50px rgba(0,255,255,0.7);
    }
    
    .stMetric label {
        color: #fbbf24 !important;
        font-size: 1.6rem !important;
        font-weight: 700 !important;
        margin-bottom: 10px !important;
    }
    
    [data-testid="stMetricValue"] {
        color: #00ff88 !important;
        font-size: 3.5rem !important;
        font-weight: 900 !important;
        text-shadow: 0 0 15px rgba(0,255,136,0.6);
    }
    
    [data-testid="stMetricDelta"] {
        color: #fbbf24 !important;
        font-size: 1.5rem !important;
        font-weight: 700 !important;
    }
    
    /* INPUT MAYDONLAR - KATTA VA YORQIN */
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > div,
    .stTextInput > div > div > input {
        background: rgba(30, 41, 59, 0.9) !important;
        border: 3px solid #00ffff !important;
        color: #ffffff !important;
        font-size: 1.5rem !important;
        padding: 18px !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
    }
    
    .stNumberInput label,
    .stSelectbox label,
    .stTextInput label {
        color: #00ffff !important;
        font-size: 1.6rem !important;
        font-weight: 800 !important;
        margin-bottom: 12px !important;
    }
    
    /* SELECT OPTION - oq rangda */
    option {
        background: #1e293b !important;
        color: #ffffff !important;
        font-size: 1.4rem !important;
        font-weight: 600 !important;
    }
    
    /* TUGMALAR - KATTA VA RANGDOR */
    .stButton > button {
        background: linear-gradient(135deg, #ec4899 0%, #8b5cf6 100%) !important;
        color: white !important;
        font-size: 1.8rem !important;
        font-weight: 900 !important;
        padding: 25px 50px !important;
        border: none !important;
        border-radius: 20px !important;
        box-shadow: 0 0 40px rgba(236,72,153,0.6) !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-8px) scale(1.05) !important;
        box-shadow: 0 0 60px rgba(236,72,153,0.9) !important;
    }
    
    /* CHECKBOX - KATTA */
    .stCheckbox {
        font-size: 1.5rem !important;
    }
    
    .stCheckbox label {
        color: #f1f5f9 !important;
        font-size: 1.5rem !important;
        font-weight: 700 !important;
    }
    
    .stCheckbox input {
        width: 30px !important;
        height: 30px !important;
    }
    
    /* SIDEBAR - YORQIN */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%) !important;
        border-right: 4px solid #00ffff !important;
    }
    
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #00ffff !important;
    }
    
    /* TABS - KATTA VA YORQIN */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        background: rgba(30, 41, 59, 0.8);
        padding: 20px;
        border-radius: 20px;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-size: 1.6rem !important;
        font-weight: 800 !important;
        padding: 20px 40px !important;
        background: rgba(124, 58, 237, 0.3) !important;
        border-radius: 15px !important;
        color: #f1f5f9 !important;
        border: 2px solid transparent !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #ec4899 0%, #8b5cf6 100%) !important;
        color: #ffffff !important;
        border-color: #00ffff !important;
        box-shadow: 0 0 30px rgba(236,72,153,0.5) !important;
    }
    
    /* DATAFRAME - YORQIN */
    .dataframe {
        font-size: 1.3rem !important;
        font-weight: 600 !important;
    }
    
    .dataframe thead tr th {
        background: linear-gradient(135deg, #7c3aed 0%, #2563eb 100%) !important;
        color: #ffffff !important;
        font-size: 1.5rem !important;
        font-weight: 800 !important;
        padding: 18px !important;
        border: 2px solid #00ffff !important;
    }
    
    .dataframe tbody tr td {
        background: rgba(30, 41, 59, 0.9) !important;
        color: #f1f5f9 !important;
        font-size: 1.3rem !important;
        padding: 15px !important;
        border: 1px solid rgba(0,255,255,0.2) !important;
    }
    
    /* INFO, SUCCESS, WARNING - KATTA */
    .stAlert {
        font-size: 1.5rem !important;
        padding: 25px !important;
        border-radius: 15px !important;
        font-weight: 700 !important;
        border: 2px solid !important;
    }
    
    div[data-baseweb="notification"] {
        background: rgba(30, 41, 59, 0.95) !important;
        border-radius: 15px !important;
    }
    
    /* EXPANDER - KATTA */
    .streamlit-expanderHeader {
        font-size: 1.7rem !important;
        font-weight: 800 !important;
        background: rgba(124, 58, 237, 0.4) !important;
        border-radius: 12px !important;
        padding: 20px !important;
        color: #00ffff !important;
        border: 2px solid #00ffff !important;
    }
    
    .streamlit-expanderContent {
        background: rgba(30, 41, 59, 0.6) !important;
        border-radius: 12px !important;
        padding: 20px !important;
    }
    
    /* CAPTION - Ko'rinadigan */
    .caption, small {
        color: #fbbf24 !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
    }
    
    /* MARKDOWN TEXT */
    .stMarkdown p {
        font-size: 1.4rem !important;
        color: #f1f5f9 !important;
    }
    
    .stMarkdown strong {
        color: #00ffff !important;
        font-weight: 900 !important;
    }
    
    /* PROGRESS BAR */
    .stProgress > div > div {
        background: linear-gradient(90deg, #ec4899 0%, #8b5cf6 100%) !important;
        height: 20px !important;
    }
    
    /* HR - rangdor chiziq */
    hr {
        border: 2px solid rgba(0,255,255,0.3) !important;
        margin: 30px 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# Tumanlar ma'lumotlari
DISTRICTS = {
    'yunusobod': {'name': 'Yunusobod', 'basePrice': 1200, 'coords': [41.35, 69.29], 'growth': 8.5},
    'mirzo_ulugbek': {'name': "Mirzo Ulug'bek", 'basePrice': 1100, 'coords': [41.32, 69.33], 'growth': 7.2},
    'yakkasaroy': {'name': 'Yakkasaroy', 'basePrice': 1400, 'coords': [41.30, 69.27], 'growth': 9.1},
    'mirobod': {'name': 'Mirobod', 'basePrice': 1300, 'coords': [41.31, 69.28], 'growth': 8.8},
    'shayxontohur': {'name': 'Shayxontohur', 'basePrice': 1000, 'coords': [41.33, 69.24], 'growth': 6.5},
    'uchtepa': {'name': 'Uchtepa', 'basePrice': 900, 'coords': [41.29, 69.20], 'growth': 5.8},
    'sergeli': {'name': 'Sergeli', 'basePrice': 850, 'coords': [41.22, 69.22], 'growth': 6.2},
    'chilonzor': {'name': 'Chilonzor', 'basePrice': 1050, 'coords': [41.31, 69.22], 'growth': 7.0},
    'bektemir': {'name': 'Bektemir', 'basePrice': 800, 'coords': [41.21, 69.34], 'growth': 5.5},
    'yashnobod': {'name': 'Yashnobod', 'basePrice': 950, 'coords': [41.28, 69.32], 'growth': 6.8},
    'olmazor': {'name': 'Olmazor', 'basePrice': 1000, 'coords': [41.34, 69.21], 'growth': 6.9}
}

def calculate_price(area, rooms, year, floor, total_floors, district_key, 
                   has_parking, has_elevator, has_renovation, condition):
    """Narxni hisoblash funksiyasi"""
    
    district = DISTRICTS[district_key]
    price_per_sqm = district['basePrice']
    
    # Yosh koeffitsienti
    current_year = 2026
    age = current_year - year
    if age < 5:
        age_coef = 1.20
    elif age < 10:
        age_coef = 1.10
    elif age < 20:
        age_coef = 0.95
    elif age < 30:
        age_coef = 0.85
    else:
        age_coef = 0.75
    
    # Qavat koeffitsienti
    if floor == 1:
        floor_coef = 0.88
    elif floor == total_floors:
        floor_coef = 0.93
    elif 2 <= floor <= 5:
        floor_coef = 1.08
    else:
        floor_coef = 1.02
    
    # Qo'shimcha imkoniyatlar
    amenities_coef = 1.0
    if has_parking:
        amenities_coef += 0.07
    if has_elevator:
        amenities_coef += 0.04
    if has_renovation:
        amenities_coef += 0.12
    
    # Xonalar koeffitsienti
    if rooms == 1:
        room_coef = 0.92
    elif rooms == 2:
        room_coef = 1.0
    elif rooms == 3:
        room_coef = 1.05
    elif rooms == 4:
        room_coef = 1.08
    else:
        room_coef = 1.10
    
    # Holat koeffitsienti
    condition_coefs = {
        "A'lo": 1.15,
        "Yaxshi": 1.0,
        "O'rtacha": 0.90,
        "Zaif": 0.75
    }
    condition_coef = condition_coefs[condition]
    
    # Yakuniy narx
    final_price_per_sqm = price_per_sqm * age_coef * floor_coef * amenities_coef * room_coef * condition_coef
    total_price = final_price_per_sqm * area
    
    return {
        'price_per_sqm': round(final_price_per_sqm),
        'total_price': round(total_price),
        'min_price': round(total_price * 0.92),
        'max_price': round(total_price * 1.08),
        'yearly_growth': district['growth'],
        'investment_return': round(total_price * district['growth'] / 100),
        'coefficients': {
            'age': age_coef,
            'floor': floor_coef,
            'amenities': amenities_coef,
            'rooms': room_coef,
            'condition': condition_coef
        }
    }

def generate_price_history(total_price, growth_rate):
    """Narx tarixini yaratish"""
    years = []
    prices = []
    
    # O'tmish 5 yil
    for i in range(5, -1, -1):
        year = 2026 - i
        price = total_price / ((1 + growth_rate/100) ** i)
        years.append(year)
        prices.append(round(price))
    
    # Kelajak 3 yil (prognoz)
    for i in range(1, 4):
        year = 2026 + i
        price = total_price * ((1 + growth_rate/100) ** i)
        years.append(year)
        prices.append(round(price))
    
    return pd.DataFrame({'Yil': years, 'Narx': prices})

def create_comparison_data(area, rooms, year, floor, total_floors, 
                          has_parking, has_elevator, has_renovation, condition):
    """Boshqa tumanlar bilan taqqoslash ma'lumotlari"""
    comparisons = []
    
    for key, district in list(DISTRICTS.items())[:6]:
        result = calculate_price(area, rooms, year, floor, total_floors, key,
                                has_parking, has_elevator, has_renovation, condition)
        comparisons.append({
            'Tuman': district['name'],
            'Narx': result['total_price'],
            'M² Narxi': result['price_per_sqm']
        })
    
    return pd.DataFrame(comparisons).sort_values('Narx', ascending=False)

# SARLAVHA - JUDA KATTA!
st.markdown("<h1 style='text-align: center;'>🏠 Ko'chmas Mulk Baholash AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #00ff88; font-size: 1.8rem; font-weight: 700;'>Toshkent shahri uchun professional narx tahlili va prognozi</p>", unsafe_allow_html=True)

st.markdown("---")

# Yon panel - Parametrlar
with st.sidebar:
    st.markdown("## 📋 Kvartira Parametrlari")
    st.markdown("---")
    
    area = st.number_input("🏠 Maydoni (m²)", min_value=20, max_value=500, value=80, step=5)
    
    rooms = st.selectbox("🚪 Xonalar soni", [1, 2, 3, 4, 5], index=2)
    
    year = st.number_input("📅 Qurilish yili", min_value=1950, max_value=2026, value=2015, step=1)
    
    col1, col2 = st.columns(2)
    with col1:
        floor = st.number_input("⬆️ Qavat", min_value=1, max_value=30, value=5)
    with col2:
        total_floors = st.number_input("🏢 Jami", min_value=1, max_value=30, value=9)
    
    st.markdown("---")
    
    district_key = st.selectbox(
        "📍 Tuman",
        options=list(DISTRICTS.keys()),
        format_func=lambda x: DISTRICTS[x]['name'],
        index=0
    )
    
    condition = st.selectbox("✨ Holati", ["A'lo", "Yaxshi", "O'rtacha", "Zaif"], index=1)
    
    st.markdown("---")
    st.markdown("### ➕ Qo'shimcha Imkoniyatlar")
    
    has_parking = st.checkbox("🚗 Avtoturargoh (+7%)")
    has_elevator = st.checkbox("🛗 Lift (+4%)", value=True)
    has_renovation = st.checkbox("🔨 Ta'mirlangan (+12%)")
    
    st.markdown("---")
    calculate_btn = st.button("💰 NARXNI HISOBLASH", use_container_width=True, type="primary")

# Asosiy sahifa
if calculate_btn or 'calculated' not in st.session_state:
    st.session_state.calculated = True
    
    # Progress bar
    with st.spinner("⏳ Tahlil qilinmoqda..."):
        import time
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress_bar.progress(i + 1)
        progress_bar.empty()
    
    # Narxni hisoblash
    result = calculate_price(area, rooms, year, floor, total_floors, district_key,
                           has_parking, has_elevator, has_renovation, condition)
    
    district = DISTRICTS[district_key]
    
    # Asosiy natijalar
    st.markdown("## 🎯 Baholash Natijalari")
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📍 Tuman", district['name'])
    
    with col2:
        st.metric("💵 1 m² narxi", f"${result['price_per_sqm']:,}")
    
    with col3:
        st.metric("💰 Umumiy narx", f"${result['total_price']:,}")
    
    with col4:
        st.metric("📈 Yillik o'sish", f"{result['yearly_growth']}%")
    
    st.markdown("---")
    
    # Narx diapazoni
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info(f"**💵 Minimal narx:** ${result['min_price']:,}")
    with col2:
        st.success(f"**💰 O'rtacha narx:** ${result['total_price']:,}")
    with col3:
        st.warning(f"**📈 Maksimal narx:** ${result['max_price']:,}")
    
    st.markdown("---")
    
    # Investitsiya ma'lumoti
    st.markdown("## 💼 Investitsiya Prognozi")
    inv_col1, inv_col2 = st.columns(2)
    
    with inv_col1:
        st.info(f"""
        **💵 Yillik daromad:** ${result['investment_return']:,}
        
        **📊 ROI:** {result['yearly_growth']}% per annum
        """)
    
    with inv_col2:
        future_3y = round(result['total_price'] * ((1 + result['yearly_growth']/100) ** 3))
        st.success(f"""
        **🚀 3 yillik prognoz:** ${future_3y:,}
        
        **💰 Potensial foyda:** ${future_3y - result['total_price']:,}
        """)
    
    st.markdown("---")
    
    # Grafiklar
    tab1, tab2, tab3 = st.tabs(["📈 NARX TARIXI", "📊 TUMANLAR TAQQOSLASH", "🎯 KOEFFITSIENTLAR"])
    
    with tab1:
        st.markdown("### 📈 Narx Tarixi va Kelajak Prognozi")
        price_history = generate_price_history(result['total_price'], result['yearly_growth'])
        
        fig = px.line(price_history, x='Yil', y='Narx', 
                     markers=True,
                     line_shape='spline')
        fig.update_traces(line_color='#00ff88', line_width=5, marker=dict(size=14, color='#fbbf24'))
        fig.update_layout(
            plot_bgcolor='rgba(15,23,42,0.9)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#f1f5f9', size=16, family='Arial Black'),
            xaxis=dict(
                showgrid=True, 
                gridcolor='rgba(0,255,255,0.2)',
                title=dict(text='Yil', font=dict(size=20, color='#00ffff'))
            ),
            yaxis=dict(
                showgrid=True, 
                gridcolor='rgba(0,255,255,0.2)',
                title=dict(text='Narx (USD)', font=dict(size=20, color='#00ffff'))
            ),
            height=550
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.caption("* 2025-2027 yillar uchun prognoz ma'lumotlar")
    
    with tab2:
        st.markdown("### 📊 Boshqa Tumanlar bilan Taqqoslash")
        comparison_df = create_comparison_data(area, rooms, year, floor, total_floors,
                                              has_parking, has_elevator, has_renovation, condition)
        
        fig = px.bar(comparison_df, x='Tuman', y='Narx',
                    color='Narx',
                    color_continuous_scale='turbo',
                    text='Narx')
        fig.update_traces(texttemplate='$%{text:,.0f}', textposition='outside', textfont_size=16)
        fig.update_layout(
            plot_bgcolor='rgba(15,23,42,0.9)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#f1f5f9', size=16, family='Arial Black'),
            xaxis=dict(title='', tickangle=-30),
            yaxis=dict(title=dict(text='Narx (USD)', font=dict(size=20, color='#00ffff'))),
            showlegend=False,
            height=550
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(comparison_df, use_container_width=True, height=350)
    
    with tab3:
        st.markdown("### 🎯 Narx Koeffitsientlari Tahlili")
        
        coef_data = {
            'Omil': ['Yangilik', 'Qavat', 'Xonalar', 'Holat', 'Imkoniyatlar'],
            'Koeffitsient': [
                result['coefficients']['age'],
                result['coefficients']['floor'],
                result['coefficients']['rooms'],
                result['coefficients']['condition'],
                result['coefficients']['amenities']
            ]
        }
        coef_df = pd.DataFrame(coef_data)
        
        fig = px.bar(coef_df, x='Omil', y='Koeffitsient',
                    color='Koeffitsient',
                    color_continuous_scale='RdYlGn',
                    text='Koeffitsient')
        fig.update_traces(texttemplate='%{text:.2f}', textposition='outside', textfont_size=18)
        fig.add_hline(y=1.0, line_dash="dash", line_color="#00ffff", line_width=3,
                     annotation_text="Bazaviy (1.0)", annotation_font_size=16, annotation_font_color="#00ffff")
        fig.update_layout(
            plot_bgcolor='rgba(15,23,42,0.9)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#f1f5f9', size=16, family='Arial Black'),
            height=550
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(coef_df, use_container_width=True, height=300)
    
    st.markdown("---")
    
    # Xarita
    st.markdown("## 🗺️ Toshkent Tumanlari Narxlar Xaritasi")
    
    map_data = []
    for key, dist in DISTRICTS.items():
        map_data.append({
            'Tuman': dist['name'],
            'lat': dist['coords'][0],
            'lon': dist['coords'][1],
            'Narx': dist['basePrice'],
            'O\'sish': dist['growth']
        })
    
    map_df = pd.DataFrame(map_data)
    
    fig = px.scatter_mapbox(map_df, 
                           lat='lat', 
                           lon='lon',
                           hover_name='Tuman',
                           hover_data={'Narx': ':$,.0f', "O'sish": ':.1f%', 'lat': False, 'lon': False},
                           color='Narx',
                           size='Narx',
                           color_continuous_scale='turbo',
                           zoom=10,
                           height=650,
                           size_max=40)
    
    fig.update_layout(
        mapbox_style='carto-darkmatter',
        margin={"r":0,"t":0,"l":0,"b":0},
        font=dict(size=16)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Ma'lumot
    with st.expander("ℹ️ NARXGA TA'SIR QILUVCHI OMILLAR", expanded=False):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            ### 🏙️ Joylashuv
            
            **Premium tumanlar:**
            - Yakkasaroy (+40%)
            - Mirobod (+30%)
            - Yunusobod (+20%)
            
            **O'rtacha:**
            - Chilonzor
            - Olmazor
            
            **Arzon:**
            - Sergeli
            - Bektemir
            """)
        
        with col2:
            st.markdown("""
            ### 🏗️ Yangilik va Holat
            
            **Yangi (0-5 yil):**
            - +20% premium
            - Kafolat mavjud
            
            **O'rtacha (10-20):**
            - Standart narx
            
            **Eski (30+):**
            - -25% chegirma
            - Ta'mir talab
            """)
        
        with col3:
            st.markdown("""
            ### 💡 Investitsiya Maslahatlari
            
        **Qisqa muddat (1-3 y):**
        - Markaziy tumanlar
        - Metro yaqini

        **Uzoq muddat (5-10 y):**
        - Rivojlanayotgan
        - Yangi loyihalar
        
        **Ijara uchun:**
        - Universitet yaqini
        - Transport qulayligi
        """)