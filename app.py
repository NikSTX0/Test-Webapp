import json
import os
import random as r
from flask import Flask, render_template, request, jsonify, session

app = Flask(__name__)
app.secret_key = "dein-geheimer-schluessel-hier-aendern"  # Bitte ändern!

# ─────────────────────────────────────────────────────────────────
# DATEN LADEN
# ─────────────────────────────────────────────────────────────────

with open("exercises.json", "r", encoding="utf-8") as f:
    Exercises = json.load(f)

assessment_questions = {
    "func_concept": [
        {"difficulty": 0.2, "step_complexity": 0.2, "qtype": "abstract",
         "question": "Welche Aussage beschreibt eine Funktion korrekt?",
         "choices": ["Jedem x-Wert wird genau ein y-Wert zugeordnet", "Ein x-Wert kann mehrere y-Werte haben", "Jeder y-Wert muss positiv sein", "Eine Funktion ist immer eine Gerade"],
         "correct": 0},
        {"difficulty": 0.3, "step_complexity": 0.4, "qtype": "example",
         "question": "Ein Taxi kostet 4€ Grundgebühr + 2€ pro km. Welche Aussage stimmt?",
         "choices": ["Zu jeder gefahrenen Strecke gehört genau ein Preis", "Eine Strecke kann mehrere Preise haben", "Der Preis ist unabhängig von der Strecke", "Der Preis sinkt mit der Strecke"],
         "correct": 0},
        {"difficulty": 0.5, "step_complexity": 0.5, "qtype": "abstract",
         "question": "Welche Zuordnung ist KEINE Funktion?",
         "choices": ["x → 2x", "x → x²", "x → ±x", "x → x + 5"],
         "correct": 2},
        {"difficulty": 0.7, "step_complexity": 0.6, "qtype": "abstract",
         "question": "Eine Relation ordnet x = 2 die Werte y = 3 und y = 5 zu. Was gilt?",
         "choices": ["Es handelt sich um keine Funktion", "Es handelt sich um eine Funktion", "Es handelt sich um eine lineare Funktion", "Der Definitionsbereich ist leer"],
         "correct": 0},
    ],
    "eq_reading": [
        {"difficulty": 0.2, "step_complexity": 0.2, "qtype": "abstract",
         "question": "Was beschreibt b in y = mx + b?",
         "choices": ["Die Steigung", "Den y-Achsenabschnitt", "Den Definitionsbereich", "Die Nullstelle"],
         "correct": 1},
        {"difficulty": 0.3, "step_complexity": 0.4, "qtype": "abstract",
         "question": "Was bedeutet m = -2 für den Graphen?",
         "choices": ["Die Funktion steigt", "Die Funktion fällt", "Die Funktion ist konstant", "Die Funktion ist quadratisch"],
         "correct": 1},
        {"difficulty": 0.5, "step_complexity": 0.7, "qtype": "abstract",
         "question": "Welche Funktion hat die größte Steigung?",
         "choices": ["y = 3x + 1", "y = -5x + 2", "y = x - 4", "y = 2x + 7"],
         "correct": 1},
        {"difficulty": 0.6, "step_complexity": 0.6, "qtype": "example",
         "question": "y = -3x + 6: Was lässt sich direkt ablesen?",
         "choices": ["Die Funktion fällt und schneidet die y-Achse bei 6", "Die Funktion steigt und schneidet die y-Achse bei -3", "Die Funktion ist konstant bei 6", "Die Nullstelle liegt bei x = 6"],
         "correct": 0},
    ],
    "slope": [
        {"difficulty": 0.2, "step_complexity": 0.2, "qtype": "example",
         "question": "Wenn m = 4, was bedeutet das?",
         "choices": ["y steigt um 4 wenn x um 1 steigt", "y steigt um 1 wenn x um 4 steigt", "y bleibt konstant", "x sinkt"],
         "correct": 0},
        {"difficulty": 0.5, "step_complexity": 0.5, "qtype": "abstract",
         "question": "Berechne die Steigung durch (1, 2) und (3, 6).",
         "choices": ["1", "2", "3", "4"],
         "correct": 1},
        {"difficulty": 0.4, "step_complexity": 0.7, "qtype": "abstract",
         "question": "Welche Gerade ist am steilsten?",
         "choices": ["m = 5", "m = -7", "m = 3", "m = -2"],
         "correct": 1},
        {"difficulty": 0.6, "step_complexity": 0.6, "qtype": "example",
         "question": "Ein Graph geht durch (0, 1) und (2, 5). Wie groß ist die Steigung?",
         "choices": ["1", "2", "3", "4"],
         "correct": 1},
    ],
    "graph_interp": [
        {"difficulty": 0.2, "step_complexity": 0.2, "qtype": "abstract",
         "question": "Wenn der Graph die y-Achse bei 3 schneidet, dann ist b = ?",
         "choices": ["0", "3", "-3", "1"],
         "correct": 1},
        {"difficulty": 0.3, "step_complexity": 0.4, "qtype": "abstract",
         "question": "Ein Graph fällt nach rechts. Was gilt?",
         "choices": ["m > 0", "m < 0", "m = 0", "b > 0"],
         "correct": 1},
        {"difficulty": 0.6, "step_complexity": 0.6, "qtype": "abstract",
         "question": "Wo liegt die Nullstelle von y = 2x - 4?",
         "choices": ["0", "1", "2", "4"],
         "correct": 2},
        {"difficulty": 0.8, "step_complexity": 0.6, "qtype": "abstract",
         "question": "Wann schneiden sich y = x + 1 und y = 2x - 1?",
         "choices": ["x = 1", "x = 2", "x = 3", "x = 0"],
         "correct": 1},
    ],
    "modelling": [
        {"difficulty": 0.3, "step_complexity": 0.4, "qtype": "example",
         "question": "3€ pro Stunde, 5€ Startgebühr. Welche Funktion beschreibt den Preis?",
         "choices": ["y = 3x + 5", "y = 5x + 3", "y = 3 + 5", "y = 5x - 3"],
         "correct": 0},
        {"difficulty": 0.4, "step_complexity": 0.6, "qtype": "example",
         "question": "Ein Tank hat 100 Liter. Pro Stunde fließen 8 Liter ab. Welche Funktion?",
         "choices": ["y = 100 - 8x", "y = 8x + 100", "y = 100 + 8x", "y = -100x + 8"],
         "correct": 0},
        {"difficulty": 0.6, "step_complexity": 0.6, "qtype": "example",
         "question": "Ein Handwerker berechnet 50€ Anfahrt + 40€ pro Stunde. Was kostet ein 3h-Einsatz?",
         "choices": ["150€", "170€", "190€", "210€"],
         "correct": 1},
        {"difficulty": 0.7, "step_complexity": 0.8, "qtype": "abstract",
         "question": "Bestimme die Gleichung der Geraden durch (0, 4) und (2, 8).",
         "choices": ["y = 2x + 4", "y = 4x + 2", "y = x + 4", "y = 2x - 4"],
         "correct": 0},
    ],
    "eq_manip": [
        {"difficulty": 0.3, "step_complexity": 0.2, "qtype": "abstract",
         "question": "Welche Operation isoliert x in 2x + 3 = 7?",
         "choices": ["Subtrahiere 3, dann dividiere durch 2", "Addiere 3, dann multipliziere mit 2", "Dividiere durch 2, dann subtrahiere 3", "Multipliziere mit 2, dann subtrahiere 3"],
         "correct": 0},
        {"difficulty": 0.5, "step_complexity": 0.4, "qtype": "example",
         "question": "Löse 3x - 5 = 10.",
         "choices": ["x = 5", "x = 3", "x = 15", "x = -5"],
         "correct": 0},
        {"difficulty": 0.7, "step_complexity": 0.6, "qtype": "abstract",
         "question": "Löse 2(x + 3) - 4 = 10.",
         "choices": ["x = 4", "x = 3", "x = 5", "x = 6"],
         "correct": 0},
        {"difficulty": 0.8, "step_complexity": 0.7, "qtype": "abstract",
         "question": "Löse 3(x - 2) = 2x + 1.",
         "choices": ["x = 5", "x = 7", "x = 3", "x = 1"],
         "correct": 1},
    ],
    "application": [
        {"difficulty": 0.2, "step_complexity": 0.2, "qtype": "example",
         "question": "Wenn m negativ ist, bedeutet das für eine reale Größe?",
         "choices": ["Die Größe nimmt ab", "Die Größe nimmt zu", "Die Größe bleibt konstant", "Keine Aussage möglich"],
         "correct": 0},
        {"difficulty": 0.3, "step_complexity": 0.4, "qtype": "example",
         "question": "Was bedeutet b = 100 in y = 20x + 100 als Kostenmodell?",
         "choices": ["Fixkosten von 100€", "Variable Kosten pro Einheit", "Gesamtgewinn", "Anzahl der Einheiten"],
         "correct": 0},
        {"difficulty": 0.6, "step_complexity": 0.7, "qtype": "abstract",
         "question": "y = 3x + 1 und y = 3x - 4: Was gilt für diese Geraden?",
         "choices": ["Sie sind parallel", "Sie schneiden sich genau einmal", "Sie sind identisch", "Sie stehen senkrecht aufeinander"],
         "correct": 0},
        {"difficulty": 0.8, "step_complexity": 0.6, "qtype": "example",
         "question": "Anbieter A: y = 10x + 50, Anbieter B: y = 15x + 20. Ab welchem x ist A günstiger?",
         "choices": ["ab x = 4", "ab x = 6", "ab x = 8", "ab x = 10"],
         "correct": 1},
    ],
}

# ─────────────────────────────────────────────────────────────────
# NUTZER SPEICHERN / LADEN  (als JSON-Datei)
# ─────────────────────────────────────────────────────────────────

USERS_FILE = "users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

def get_user(name):
    users = load_users()
    if name not in users:
        users[name] = {
            "name": name,
            "psychometrics": {
                "complexity": 0.0,
                "abstract_pref": 0.5,
                "meta_accuracy": {"false_pos": 0.2, "false_neg": 0.2}
            },
            "subject_skills": {
                "func_concept": 0.0, "eq_reading": 0.0, "slope": 0.0,
                "graph_interp": 0.0, "modelling": 0.0, "eq_manip": 0.0, "application": 0.0
            },
            "solved": [],
            "_cat_solved": {k: [] for k in assessment_questions},
            "assessment_done": False
        }
        save_users(users)
    return users[name]

def save_user(user_data):
    users = load_users()
    users[user_data["name"]] = user_data
    save_users(users)

# ─────────────────────────────────────────────────────────────────
# ASSESSMENT LOGIK
# ─────────────────────────────────────────────────────────────────

def get_assessment_state(user_data):
    """Gibt die nächste Assessment-Frage zurück, oder None wenn fertig."""
    if user_data.get("assessment_done"):
        return None

    # Tracking welche Fragen schon gespielt wurden
    played = set(tuple(x) for x in user_data.get("assessment_played", []))
    banned = set(tuple(x) for x in user_data.get("assessment_banned", []))

    order = [1, 2, 3, 0]
    for category in assessment_questions:
        for i in order:
            key = (category, i)
            if key not in played and key not in banned:
                q = assessment_questions[category][i]
                return {
                    "category": category,
                    "index": i,
                    "question": q["question"],
                    "choices": q["choices"],
                    "phase": "assessment"
                }
    return None  # Alles gespielt

def process_assessment_answer(user_data, category, index, choice, confidence):
    q = assessment_questions[category][index]
    is_correct = (choice == q["correct"])

    played = user_data.setdefault("assessment_played", [])
    played.append([category, index])

    # Ban-Logik
    banned = user_data.setdefault("assessment_banned", [])
    banned_set = set(tuple(x) for x in banned)
    questions = assessment_questions[category]
    current_diff = q["difficulty"]
    current_step = q["step_complexity"]

    if is_correct and confidence > 0.7:
        for j, aq in enumerate(questions):
            if aq["difficulty"] < current_diff:
                banned_set.add((category, j))
    elif not is_correct and confidence >= 0.7:
        for j, aq in enumerate(questions):
            if aq["step_complexity"] > current_step:
                banned_set.add((category, j))
    elif not is_correct and confidence < 0.7:
        for j, aq in enumerate(questions):
            if aq["difficulty"] > current_diff:
                banned_set.add((category, j))

    user_data["assessment_banned"] = [list(x) for x in banned_set]

    # Meta-accuracy update
    meta = user_data["psychometrics"]["meta_accuracy"]
    if is_correct:
        if confidence <= 0.7:
            meta["false_neg"] = min(meta["false_neg"] + 0.1, 1.0)
        else:
            meta["false_neg"] = max(meta["false_neg"] - 0.05, 0.0)
    else:
        if confidence >= 0.7:
            meta["false_pos"] = min(meta["false_pos"] + 0.1, 1.0)
        else:
            meta["false_pos"] = max(meta["false_pos"] - 0.05, 0.0)

    # Subject skill update
    if is_correct:
        conf_solved = user_data.setdefault("_conf_solved", [])
        unconf_solved = user_data.setdefault("_unconf_solved", [])
        if confidence > 0.7:
            conf_solved.append(q["step_complexity"])
        else:
            unconf_solved.append(q["step_complexity"])

        cat_solved = user_data["_cat_solved"][category]
        cat_solved.append({"difficulty": q["difficulty"], "confidence": confidence})
        sorted_cat = sorted(cat_solved, key=lambda x: x["difficulty"])
        hardest = sorted_cat[-1]
        if hardest["confidence"] > 0.7:
            user_data["subject_skills"][category] = min(hardest["difficulty"], 1.0)
        elif len(sorted_cat) >= 2:
            second = sorted_cat[-2]["difficulty"]
            user_data["subject_skills"][category] = min((hardest["difficulty"] + second) / 2, 1.0)
        else:
            user_data["subject_skills"][category] = min(hardest["difficulty"] * 0.75, 1.0)

    # Abstract pref update
    if is_correct:
        if q["qtype"] == "abstract":
            user_data["psychometrics"]["abstract_pref"] = min(
                user_data["psychometrics"]["abstract_pref"] + 0.05, 1.0)
        else:
            user_data["psychometrics"]["abstract_pref"] = max(
                user_data["psychometrics"]["abstract_pref"] - 0.05, 0.0)

    return is_correct

# ─────────────────────────────────────────────────────────────────
# ÜBUNGS-LOGIK
# ─────────────────────────────────────────────────────────────────

def choose_subject(user_data):
    skills = user_data["subject_skills"]
    weak   = [k for k, v in skills.items() if v < 0.4]
    mid    = [k for k, v in skills.items() if 0.4 <= v < 0.7]
    strong = [k for k, v in skills.items() if v >= 0.7]
    roll = r.randint(1, 10)
    if roll <= 5 and weak:   return r.choice(weak)
    if roll <= 8 and mid:    return r.choice(mid)
    if strong:               return r.choice(strong)
    return r.choice(list(skills.keys()))

def choose_exercise(user_data):
    subject = choose_subject(user_data)
    exercises = Exercises[subject]
    solved = [tuple(x) for x in user_data["solved"]]
    skills = user_data["subject_skills"]

    diffs = [abs(ex["difficulty"] - skills[subject]) for ex in exercises]
    sorted_ids = sorted(range(len(diffs)), key=lambda i: diffs[i])

    for candidate in sorted_ids:
        if (subject, candidate) not in solved:
            return subject, candidate

    # Alles in diesem Thema gelöst — anderes Thema
    remaining = [k for k in skills if
                 any((k, i) not in solved for i in range(len(Exercises[k])))]
    if not remaining:
        return subject, sorted_ids[0]

    # Temp. ausschließen und neu wählen
    original = skills[subject]
    skills[subject] = -1
    result = choose_exercise(user_data)
    skills[subject] = original
    return result

def get_representation(user_data, subject, ex_id):
    ex = Exercises[subject][ex_id]
    pref = user_data["psychometrics"]["abstract_pref"]
    roll = r.random()
    if roll > 0.8:
        return ex["representations"]["mixed"]
    elif roll < pref:
        return ex["representations"]["abstract"]
    else:
        return ex["representations"]["example"]

def get_support_type(user_data):
    if user_data["psychometrics"]["meta_accuracy"]["false_pos"] > 0.4:
        return "strategy"
    return "scaffold"

def get_scaffold_level(user_data, subject, ex_id):
    ex = Exercises[subject][ex_id]
    diff = ex["step_complexity"] - user_data["psychometrics"]["complexity"]
    if diff > 0.3:
        return "full"
    elif diff > 0.1:
        return "light"
    return None

def update_skill(user_data, subject, ex_id, support):
    difficulty = Exercises[subject][ex_id]["difficulty"]
    skills = user_data["subject_skills"]
    if support is None:
        if difficulty > skills[subject]:
            skills[subject] = round(skills[subject] + 0.15 * difficulty, 10)
    else:
        if difficulty < skills[subject]:
            skills[subject] = round(skills[subject] - 0.15 * difficulty, 10)
    skills[subject] = max(0.0, min(1.0, skills[subject]))
    user_data["solved"].append([subject, ex_id])

def update_psychometrics(user_data, support, errors):
    if errors == 0:
        if support == "strategy":
            user_data["psychometrics"]["meta_accuracy"]["false_pos"] = max(
                0, user_data["psychometrics"]["meta_accuracy"]["false_pos"] - 0.1)
        if support == "scaffold":
            user_data["psychometrics"]["complexity"] = min(
                1, user_data["psychometrics"]["complexity"] + 0.1)
    elif errors > 1:
        if support == "strategy":
            user_data["psychometrics"]["meta_accuracy"]["false_pos"] = min(
                1, user_data["psychometrics"]["meta_accuracy"]["false_pos"] + 0.1)
        if support == "scaffold":
            user_data["psychometrics"]["complexity"] = max(
                0, user_data["psychometrics"]["complexity"] - 0.1)

# ─────────────────────────────────────────────────────────────────
# ROUTEN
# ─────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/start", methods=["POST"])
def start():
    data = request.json
    name = data.get("name", "").strip()
    if not name:
        return jsonify({"error": "Bitte gib deinen Namen ein."}), 400

    user_data = get_user(name)
    session["user"] = name

    if not user_data.get("assessment_done"):
        next_q = get_assessment_state(user_data)
        if next_q:
            save_user(user_data)
            return jsonify({"phase": "assessment", "question": next_q})

    # Assessment fertig → Übung starten
    subject, ex_id = choose_exercise(user_data)
    rep = get_representation(user_data, subject, ex_id)
    support_type = get_support_type(user_data)
    ex = Exercises[subject][ex_id]

    session_data = {
        "subject": subject, "ex_id": ex_id,
        "support_type": support_type, "errors": 0,
        "scaffold_step": 0, "strategy_step": 0
    }
    user_data["current_exercise"] = session_data
    save_user(user_data)

    response = {"phase": "exercise", "representation": rep, "subject": subject}

    if support_type == "strategy":
        fp = user_data["psychometrics"]["meta_accuracy"]["false_pos"]
        level = "full" if fp > 0.6 else "light"
        steps = ex["strategy"][level]
        if steps:
            step = steps[0]
            response["support"] = {
                "type": "strategy", "step_index": 0,
                "question": step["question"], "choices": step["choices"]
            }
            return jsonify(response)
    else:
        level = get_scaffold_level(user_data, subject, ex_id)
        if level:
            steps = ex["scaffolding"][level]
            if steps:
                step = steps[0]
                response["support"] = {
                    "type": "scaffold", "level": level,
                    "step_index": 0, "prompt": step["prompt"]
                }
                return jsonify(response)

    response["support"] = None
    response["final_question"] = ex.get("question", "Löse die Aufgabe.")
    return jsonify(response)

@app.route("/api/assessment-answer", methods=["POST"])
def assessment_answer():
    data = request.json
    name = session.get("user") or data.get("name")
    user_data = get_user(name)

    category = data["category"]
    index = data["index"]
    choice = data["choice"]
    confidence = data["confidence"]

    is_correct = process_assessment_answer(user_data, category, index, choice, confidence)

    next_q = get_assessment_state(user_data)
    if next_q is None:
        # Assessment abgeschlossen
        user_data["assessment_done"] = True
        # Complexity finalisieren
        conf_solved = user_data.get("_conf_solved", [])
        unconf_solved = user_data.get("_unconf_solved", [])
        if conf_solved and unconf_solved:
            user_data["psychometrics"]["complexity"] = (
                sum(conf_solved)/len(conf_solved) + min(unconf_solved)) / 2
        elif conf_solved:
            user_data["psychometrics"]["complexity"] = sum(conf_solved)/len(conf_solved)
        elif unconf_solved:
            user_data["psychometrics"]["complexity"] = min(unconf_solved) * 0.75

        save_user(user_data)
        return jsonify({"phase": "assessment_done", "correct": is_correct,
                        "skills": user_data["subject_skills"]})

    save_user(user_data)
    return jsonify({"phase": "assessment", "correct": is_correct, "question": next_q})

@app.route("/api/support-answer", methods=["POST"])
def support_answer():
    data = request.json
    name = session.get("user") or data.get("name")
    user_data = get_user(name)
    ex_session = user_data["current_exercise"]
    subject = ex_session["subject"]
    ex_id = ex_session["ex_id"]
    ex = Exercises[subject][ex_id]
    support_type = ex_session["support_type"]

    answer = data["answer"]
    step_index = data["step_index"]

    if support_type == "strategy":
        fp = user_data["psychometrics"]["meta_accuracy"]["false_pos"]
        level = "full" if fp > 0.6 else "light"
        steps = ex["strategy"][level]
        step = steps[step_index]
        correct = answer.isdigit() and int(answer) == step["correct"]
        if not correct:
            ex_session["errors"] += 1
            save_user(user_data)
            return jsonify({"correct": False, "hint": step["explanation"],
                            "step_index": step_index})
        next_index = step_index + 1
        if next_index < len(steps):
            next_step = steps[next_index]
            ex_session["strategy_step"] = next_index
            save_user(user_data)
            return jsonify({"correct": True, "next_support": {
                "type": "strategy", "step_index": next_index,
                "question": next_step["question"], "choices": next_step["choices"]
            }})
    else:
        level = get_scaffold_level(user_data, subject, ex_id)
        if level:
            steps = ex["scaffolding"][level]
            step = steps[step_index]
            correct = answer == step["answer"]
            if not correct:
                ex_session["errors"] += 1
                save_user(user_data)
                return jsonify({"correct": False, "hint": step["hint"],
                                "step_index": step_index})
            next_index = step_index + 1
            if next_index < len(steps):
                next_step = steps[next_index]
                ex_session["scaffold_step"] = next_index
                save_user(user_data)
                return jsonify({"correct": True, "next_support": {
                    "type": "scaffold", "level": level,
                    "step_index": next_index, "prompt": next_step["prompt"]
                }})

    # Support fertig → Hauptfrage
    save_user(user_data)
    return jsonify({"correct": True, "next_support": None,
                    "final_question": ex.get("question", "Löse die Aufgabe.")})

@app.route("/api/final-answer", methods=["POST"])
def final_answer():
    data = request.json
    name = session.get("user") or data.get("name")
    user_data = get_user(name)
    ex_session = user_data["current_exercise"]
    subject = ex_session["subject"]
    ex_id = ex_session["ex_id"]
    ex = Exercises[subject][ex_id]

    answer = data["answer"]
    if answer == ex["final_answer"]:
        support = ex_session["support_type"] if ex_session.get("errors", 0) > 0 else None
        update_skill(user_data, subject, ex_id, support)
        update_psychometrics(user_data, support, ex_session.get("errors", 0))
        save_user(user_data)
        return jsonify({"correct": True, "feedback": "Hervorragend! ✓",
                        "skills": user_data["subject_skills"]})
    else:
        ex_session["errors"] = ex_session.get("errors", 0) + 1
        save_user(user_data)
        hint = ex.get("error_feedback", {}).get("concept_hint", "Versuche es nochmal.")
        return jsonify({"correct": False, "hint": hint})

@app.route("/api/next-exercise", methods=["POST"])
def next_exercise():
    data = request.json
    name = session.get("user") or data.get("name")
    user_data = get_user(name)

    subject, ex_id = choose_exercise(user_data)
    rep = get_representation(user_data, subject, ex_id)
    support_type = get_support_type(user_data)
    ex = Exercises[subject][ex_id]

    session_data = {
        "subject": subject, "ex_id": ex_id,
        "support_type": support_type, "errors": 0,
        "scaffold_step": 0, "strategy_step": 0
    }
    user_data["current_exercise"] = session_data
    save_user(user_data)

    response = {"phase": "exercise", "representation": rep, "subject": subject}

    if support_type == "strategy":
        fp = user_data["psychometrics"]["meta_accuracy"]["false_pos"]
        level = "full" if fp > 0.6 else "light"
        steps = ex["strategy"][level]
        if steps:
            step = steps[0]
            response["support"] = {
                "type": "strategy", "step_index": 0,
                "question": step["question"], "choices": step["choices"]
            }
            return jsonify(response)
    else:
        level = get_scaffold_level(user_data, subject, ex_id)
        if level:
            steps = ex["scaffolding"][level]
            if steps:
                step = steps[0]
                response["support"] = {
                    "type": "scaffold", "level": level,
                    "step_index": 0, "prompt": step["prompt"]
                }
                return jsonify(response)

    response["support"] = None
    response["final_question"] = ex.get("question", "Löse die Aufgabe.")
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
