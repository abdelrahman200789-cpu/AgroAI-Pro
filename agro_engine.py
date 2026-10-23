"""Core educational logic for AgroAI Pro. Rules are illustrative, not expert diagnoses."""
from pathlib import Path
import json, re, math
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


def load_crops(path=None):
    path = Path(path) if path else DATA_DIR / "crops.csv"
    return pd.read_csv(path).fillna("")


def load_disease_rules(path=None):
    path = Path(path) if path else DATA_DIR / "disease_rules.json"
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def normalize(text):
    return re.sub(r"[^a-z0-9 ]+", " ", str(text).lower()).strip()


def diagnose(crop, symptoms, rules=None):
    """Rank illustrative rules by symptom overlap. Returns candidates, never a definitive diagnosis."""
    rules = rules if rules is not None else load_disease_rules()
    selected = {normalize(s) for s in symptoms if normalize(s)}
    results = []
    for rule in rules:
        if rule.get("crop", "Any").lower() not in (crop.lower(), "any"):
            continue
        rule_symptoms = {normalize(s) for s in rule.get("symptoms", [])}
        overlap = selected & rule_symptoms
        if not overlap:
            continue
        score = len(overlap) / max(len(rule_symptoms), 1)
        results.append({**rule, "matched_symptoms": sorted(overlap), "score": round(score * 100, 1)})
    return sorted(results, key=lambda x: (x["score"], len(x["matched_symptoms"])), reverse=True)


def recommend_crops(season, soil_type, ph=None, water=None, crops=None):
    """Transparent shortlist based on demo metadata; score is a heuristic, not a yield prediction."""
    df = crops if crops is not None else load_crops()
    out=[]
    for _, row in df.iterrows():
        score=0; reasons=[]
        if season and str(row.get('season','')).lower() == season.lower(): score += 40; reasons.append('season matches')
        if soil_type and str(row.get('soil_type','')).lower() == soil_type.lower(): score += 35; reasons.append('soil type matches')
        ph_text=str(row.get('ideal_ph',''))
        match=re.search(r"([0-9.]+)\s*[-–]\s*([0-9.]+)", ph_text)
        if ph is not None and match:
            lo,hi=float(match.group(1)),float(match.group(2))
            if lo <= float(ph) <= hi: score += 20; reasons.append('pH falls in listed range')
            elif lo-0.5 <= float(ph) <= hi+0.5: score += 8; reasons.append('pH is near listed range')
        if water:
            need=str(row.get('water_need','')).lower()
            if water.lower() == need: score += 5; reasons.append('water need matches preference')
        out.append({'crop':row.get('crop',''), 'score':min(score,100), 'ideal_ph':ph_text,
                    'water_need':row.get('water_need',''), 'notes':row.get('notes',''),
                    'reasons':reasons or ['No strong match from the selected inputs']})
    return sorted(out,key=lambda x:x['score'],reverse=True)


def analyze_sensors(soil_moisture, temperature, humidity):
    """Simple configurable demo thresholds; units are percent, °C, percent."""
    alerts=[]
    if soil_moisture < 25: alerts.append({'level':'Warning','message':'Soil moisture is low in this demo threshold. Check the root zone before irrigating.'})
    elif soil_moisture > 85: alerts.append({'level':'Warning','message':'Soil moisture is high. Check drainage and sensor placement.'})
    else: alerts.append({'level':'Info','message':'Soil moisture is within the demo range.'})
    if temperature > 35: alerts.append({'level':'Warning','message':'High temperature reading. Check crop conditions and sensor shade/placement.'})
    elif temperature < 5: alerts.append({'level':'Warning','message':'Low temperature reading. Check local crop sensitivity and forecast.'})
    else: alerts.append({'level':'Info','message':'Temperature is within the demo range.'})
    if humidity > 90: alerts.append({'level':'Info','message':'High relative humidity may increase some disease risks; scout the crop.'})
    return alerts


def search_knowledge(query, folder=None):
    """Rank local knowledge notes with TF-IDF vectors and cosine similarity.

    TF-IDF gives more weight to terms that are informative in a document and
    less weight to terms that occur in many documents. Cosine similarity then
    ranks each document against the user's query. Scores are relevance signals,
    not probabilities or factual-confidence values.
    """
    folder = Path(folder) if folder else DATA_DIR / 'knowledge'
    query = str(query).strip()
    if not query:
        return []

    paths = sorted(folder.glob('*.txt'))
    if not paths:
        return []

    documents = [path.read_text(encoding='utf-8').strip() for path in paths]
    if not any(documents):
        return []

    # Fit IDF on the available note collection, then vectorize the query.
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
    try:
        document_vectors = vectorizer.fit_transform(documents)
        query_vector = vectorizer.transform([query])
    except ValueError:
        # Happens when the notes contain no usable vocabulary.
        return []

    if query_vector.nnz == 0:
        return []

    similarities = cosine_similarity(query_vector, document_vectors).ravel()
    query_terms = set(vectorizer.build_analyzer()(query))
    results = []
    for index, score in enumerate(similarities):
        if score <= 0:
            continue
        doc_terms = set(vectorizer.build_analyzer()(documents[index]))
        matched_terms = sorted(query_terms & doc_terms)
        results.append({
            'title': paths[index].stem.replace('_', ' ').title(),
            'file': paths[index].name,
            'score': round(float(score), 4),
            'score_percent': round(float(score) * 100, 1),
            'matched_terms': matched_terms,
            'content': documents[index],
        })
    return sorted(results, key=lambda item: item['score'], reverse=True)
