from pathlib import Path
import json
import pandas as pd
import streamlit as st
import plotly.express as px
from agro_engine import load_crops, load_disease_rules, diagnose, recommend_crops, analyze_sensors, search_knowledge

st.set_page_config(page_title="AgroAI Pro", page_icon="🌱", layout="wide", initial_sidebar_state="expanded")
BASE_DIR = Path(__file__).resolve().parent
st.markdown("""<style>
.main {background-color:#f7faf7;} .block-container {padding-top:1.6rem; padding-bottom:2rem;}
.hero {padding:1.3rem 1.5rem; border-radius:16px; background:linear-gradient(120deg,#164e3b,#2d7b53); color:white; margin-bottom:1rem;}
.hero h1 {color:white; margin:0;} .hero p {color:#e8f5ec; margin:.35rem 0 0 0;}
.note {padding:.8rem 1rem; border-left:4px solid #d6a542; background:#fff8e7; border-radius:6px;}
</style>""", unsafe_allow_html=True)

@st.cache_data
def get_crops(): return load_crops()
@st.cache_data
def get_rules(): return load_disease_rules()

crops=get_crops(); rules=get_rules()
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=900&q=80", use_container_width=True)
    st.title("🌱 AgroAI Pro")
    st.caption("Smart Farming Advisor · Educational prototype")
    page=st.radio("Navigation", ["Dashboard", "Disease Diagnosis", "Crop Recommendation", "IoT Monitor", "Knowledge Hub", "Dataset Explorer"])
    st.divider()
    st.caption(f"Crop records: {len(crops)} · Demo rules: {len(rules)}")

if page == "Dashboard":
    st.markdown('<div class="hero"><h1>🌿 AgroAI Pro</h1><p>Practical decision-support prototype for crop planning, symptom scouting, and sensor readings.</p></div>',unsafe_allow_html=True)
    a,b,c,d=st.columns(4)
    a.metric("Crop records",len(crops)); b.metric("Symptom rules",len(rules)); c.metric("Knowledge notes",len(list((BASE_DIR/'data/knowledge').glob('*.txt')))); d.metric("Interface","Streamlit")
    st.subheader("Explore the project")
    c1,c2,c3=st.columns(3)
    with c1:
        st.markdown("### 🩺 Disease Diagnosis")
        st.write("Compare selected symptoms with illustrative rules and review possible next steps.")
    with c2:
        st.markdown("### 🌾 Crop Recommendation")
        st.write("Shortlist crops using season, soil type, pH, and water preference.")
    with c3:
        st.markdown("### 📡 IoT Monitor")
        st.write("Enter sensor values and receive simple threshold alerts.")
    st.subheader("Crop records by season")
    season_counts=crops['season'].value_counts().rename_axis('Season').reset_index(name='Count')
    fig=px.bar(season_counts,x='Season',y='Count',color='Season',title='Educational crop catalog')
    st.plotly_chart(fig,use_container_width=True)
    st.markdown('<div class="note"><b>Prototype notice:</b> Data and rules included with this project are educational examples. They are not a verified regional agronomy dataset, live weather feed, or substitute for a local agricultural specialist.</div>',unsafe_allow_html=True)

elif page == "Disease Diagnosis":
    st.title("🩺 Plant Symptom Assistant")
    st.write("Select a crop and the symptoms you can observe. The tool ranks matching demo rules; it does not confirm disease.")
    crops_list=sorted(set(crops['crop'].astype(str)))
    crop=st.selectbox("Crop",crops_list)
    all_symptoms=sorted({s for r in rules if r.get('crop') in (crop,'Any') for s in r.get('symptoms',[])})
    chosen=st.multiselect("Observed symptoms",all_symptoms,help="Choose only symptoms you actually observe.")
    extra=st.text_input("Optional note",placeholder="For example: symptoms began after heavy rain")
    if st.button("Analyze symptoms",type="primary"):
        if not chosen: st.warning("Select at least one symptom first.")
        else:
            matches=diagnose(crop,chosen,rules)
            if not matches: st.info("No matching demo rule found. This does not mean the plant is healthy; seek local advice.")
            else:
                for idx,item in enumerate(matches[:5],1):
                    with st.container(border=True):
                        st.subheader(f"{idx}. {item['disease']}")
                        st.progress(min(item['score']/100,1.0),text=f"Symptom overlap score: {item['score']:.1f}%")
                        st.caption("This percentage is a simple rule overlap score, not a probability of disease.")
                        st.write("**Matched symptoms:** "+", ".join(item['matched_symptoms']))
                        st.write("**Suggested checks:**")
                        for tip in item.get('advice',[]): st.markdown(f"- {tip}")
                        st.caption(item.get('note',''))
            if extra: st.caption("Your note: "+extra)
    st.warning("Do not use this output alone to select or apply pesticides. Confirm the cause with a qualified local agricultural specialist and follow local regulations.")

elif page == "Crop Recommendation":
    st.title("🌾 Crop Recommendation")
    st.write("Generate a transparent shortlist using the included educational catalog.")
    left,right=st.columns(2)
    with left:
        season=st.selectbox("Planting season",["Summer","Winter"])
        soil=st.selectbox("Soil type",sorted(crops['soil_type'].unique()))
        ph=st.slider("Measured soil pH",3.5,9.0,6.5,0.1)
    with right:
        water=st.selectbox("Water availability / preferred crop need",["Any","Low","Medium","High"])
        st.info("Use a recent soil test for pH. ‘Water need’ is a broad catalog label, not a precise irrigation schedule.")
    if st.button("Recommend crops",type="primary"):
        recs=recommend_crops(season,soil,ph,None if water=="Any" else water,crops)
        for rec in recs[:8]:
            with st.container(border=True):
                top1,top2=st.columns([3,1]); top1.subheader(rec['crop']); top2.metric("Heuristic score",f"{rec['score']}/100")
                st.progress(rec['score']/100)
                st.write("**Why it appears:** "+"; ".join(rec['reasons']))
                st.caption(f"Catalog pH range: {rec['ideal_ph']} · Water need label: {rec['water_need']}")
                st.write(rec['notes'])
        st.caption("Scores are simple heuristic matches, not yield estimates or guarantees of suitability.")

elif page == "IoT Monitor":
    st.title("📡 IoT Sensor Monitor")
    st.write("Enter current readings from your sensors. Values are not connected to live hardware in this version.")
    c1,c2,c3=st.columns(3)
    with c1: moisture=st.slider("Soil moisture (%)",0,100,42)
    with c2: temp=st.slider("Temperature (°C)",-5,55,28)
    with c3: humidity=st.slider("Relative humidity (%)",0,100,60)
    st.subheader("Current readings")
    m1,m2,m3=st.columns(3); m1.metric("Soil moisture",f"{moisture}%"); m2.metric("Temperature",f"{temp} °C"); m3.metric("Humidity",f"{humidity}%")
    if st.button("Check readings",type="primary"):
        alerts=analyze_sensors(moisture,temp,humidity)
        for alert in alerts:
            (st.warning if alert['level']=='Warning' else st.info)(alert['message'])
        st.caption("Thresholds are demo values. Calibrate sensors and configure crop-specific thresholds before field use.")
    chart_df=pd.DataFrame({'Metric':['Soil moisture','Temperature','Humidity'],'Reading':[moisture,temp,humidity],'Scale':['Percent','Celsius','Percent']})
    st.dataframe(chart_df,use_container_width=True,hide_index=True)

elif page == "Knowledge Hub":
    st.title("📚 Agricultural Knowledge Hub")
    st.write("Search the short local notes bundled with the project.")
    query=st.text_input("Search topics",placeholder="soil pH, irrigation, disease scouting, sensors...")
    if query:
        results=search_knowledge(query)
        if not results: st.info("No matching note. Try a broader keyword such as soil, water, crop, disease, or sensor.")
        for result in results:
            with st.expander(f"{result['title']} · keyword score {result['score']}"):
                st.write(result['content'])
                st.caption(f"Local file: data/knowledge/{result['file']}")
    else:
        st.caption("Available topics")
        for path in sorted((BASE_DIR/'data/knowledge').glob('*.txt')):
            with st.expander(path.stem.replace('_',' ').title()): st.write(path.read_text(encoding='utf-8'))

elif page == "Dataset Explorer":
    st.title("🗂️ Dataset Explorer")
    st.write("Inspect and filter the crop catalog included with this prototype.")
    f1,f2=st.columns(2)
    with f1: season_filter=st.multiselect("Season",sorted(crops['season'].unique()),default=sorted(crops['season'].unique()))
    with f2: soil_filter=st.multiselect("Soil type",sorted(crops['soil_type'].unique()),default=sorted(crops['soil_type'].unique()))
    filtered=crops[crops['season'].isin(season_filter)&crops['soil_type'].isin(soil_filter)]
    st.metric("Filtered records",len(filtered))
    st.dataframe(filtered,use_container_width=True,hide_index=True)
    st.download_button("Download filtered CSV",filtered.to_csv(index=False).encode('utf-8'),file_name='agroai_crops_filtered.csv',mime='text/csv')
    st.caption("The included catalog is manually assembled demo content; verify agronomic values for the target region before real use.")

st.divider()
st.caption("AgroAI Pro · Streamlit educational prototype · No live sensor, weather, or expert-service integration")
