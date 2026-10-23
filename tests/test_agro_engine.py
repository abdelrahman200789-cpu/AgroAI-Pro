from agro_engine import analyze_sensors, diagnose, recommend_crops, search_knowledge


def test_diagnose_matches_selected_symptoms():
    rules = [{"disease":"Demo disease", "crop":"Tomato", "symptoms":["brown spots", "yellow leaves"], "advice":[]}]
    results = diagnose("Tomato", ["brown spots"], rules)
    assert results
    assert results[0]["disease"] == "Demo disease"
    assert results[0]["score"] == 50.0


def test_diagnose_filters_crop():
    rules = [{"disease":"Demo disease", "crop":"Wheat", "symptoms":["white powder"]}]
    assert diagnose("Tomato", ["white powder"], rules) == []


def test_sensor_alerts_low_moisture():
    alerts = analyze_sensors(10, 25, 50)
    assert any("moisture is low" in item["message"] for item in alerts)


def test_recommendation_returns_sorted_results():
    rows = [
        {"crop":"A", "season":"Summer", "soil_type":"Loamy", "ideal_ph":"6.0-7.0", "water_need":"Medium", "notes":""},
        {"crop":"B", "season":"Winter", "soil_type":"Clay", "ideal_ph":"5.0-6.0", "water_need":"Low", "notes":""},
    ]
    import pandas as pd
    result = recommend_crops("Summer", "Loamy", 6.5, "Medium", pd.DataFrame(rows))
    assert result[0]["crop"] == "A"
    assert result[0]["score"] >= result[1]["score"]


def test_knowledge_search_uses_tfidf_and_ranks_relevant_note(tmp_path):
    (tmp_path / "irrigation.txt").write_text(
        "soil moisture irrigation root zone water scheduling", encoding="utf-8"
    )
    (tmp_path / "disease.txt").write_text(
        "plant disease scouting leaf symptoms fungal infection", encoding="utf-8"
    )
    result = search_knowledge("irrigation soil moisture", tmp_path)
    assert result and result[0]["file"] == "irrigation.txt"
    assert 0 < result[0]["score"] <= 1
    assert result[0]["score_percent"] > 0
    assert "irrigation" in result[0]["matched_terms"]


def test_knowledge_search_returns_empty_for_unrelated_query(tmp_path):
    (tmp_path / "irrigation.txt").write_text("soil moisture irrigation", encoding="utf-8")
    assert search_knowledge("spacecraft nebula", tmp_path) == []


def test_knowledge_search_returns_empty_for_blank_query(tmp_path):
    (tmp_path / "irrigation.txt").write_text("soil moisture irrigation", encoding="utf-8")
    assert search_knowledge("   ", tmp_path) == []
