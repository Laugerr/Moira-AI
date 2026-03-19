from flask import Flask, render_template, jsonify, request
import json
import random
from pathlib import Path

app = Flask(__name__)

DATA_FILE = Path("data/scenarios.json")

# Fallback scenarios in case JSON file is empty or missing
FALLBACK_SCENARIOS = [
    {
        "id": 1,
        "title": "First Job, First Pressure",
        "text": "You are 19 years old, living in a small apartment, with only €250 left. A local café offers you a low-paying job, but your friend wants you to join him in building a small online business.",
        "choices": [
            {
                "text": "Take the café job for stability",
                "effects": {"money": 15, "energy": -10, "happiness": -2, "risk": -5},
                "result": "You gain stability, but the routine drains your energy."
            },
            {
                "text": "Join your friend and build the business",
                "effects": {"money": -5, "energy": -5, "happiness": 10, "risk": 15},
                "result": "You chase opportunity, but success is far from guaranteed."
            },
            {
                "text": "Reject both and focus on learning a high-income skill",
                "effects": {"money": -10, "energy": -3, "happiness": 5, "risk": 8},
                "result": "You invest in your future, but money becomes tight."
            }
        ]
    },
    {
        "id": 2,
        "title": "A New City",
        "text": "You get the chance to move to a bigger city where salaries are higher, but living costs are much worse. Staying means comfort. Leaving means uncertainty.",
        "choices": [
            {
                "text": "Move to the bigger city",
                "effects": {"money": -10, "energy": -8, "happiness": 8, "risk": 12},
                "result": "The city feels alive and full of possibilities, but it is expensive."
            },
            {
                "text": "Stay where you are and save money",
                "effects": {"money": 10, "energy": 2, "happiness": -3, "risk": -4},
                "result": "You gain breathing room financially, but life feels repetitive."
            },
            {
                "text": "Visit first and decide later",
                "effects": {"money": -5, "energy": -2, "happiness": 4, "risk": 2},
                "result": "You take a cautious step without fully committing."
            }
        ]
    },
    {
        "id": 3,
        "title": "The Tempting Shortcut",
        "text": "Someone offers you a fast way to make money online. It sounds easy, but the method feels questionable and could damage your future.",
        "choices": [
            {
                "text": "Take the shortcut and cash in fast",
                "effects": {"money": 20, "energy": -3, "happiness": 2, "risk": 20},
                "result": "You make money quickly, but the danger grows in the background."
            },
            {
                "text": "Refuse and keep things clean",
                "effects": {"money": -2, "energy": 1, "happiness": 4, "risk": -10},
                "result": "You stay safe, even if you feel a little frustrated."
            },
            {
                "text": "Research it before deciding",
                "effects": {"money": 0, "energy": -2, "happiness": 1, "risk": 3},
                "result": "You delay the decision and gather more information."
            }
        ]
    }
]


def load_scenarios():
    try:
        if DATA_FILE.exists():
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list) and data:
                    return data
    except Exception:
        pass
    return FALLBACK_SCENARIOS


def clamp_stat(value):
    return max(0, min(100, value))


def get_random_scenario():
    scenarios = load_scenarios()
    return random.choice(scenarios)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/start", methods=["GET"])
def start_game():
    scenario = get_random_scenario()
    initial_stats = {
        "money": 50,
        "energy": 50,
        "happiness": 50,
        "risk": 20
    }

    return jsonify({
        "scenario": scenario,
        "stats": initial_stats,
        "message": "Your life begins. Every choice shapes your path."
    })


@app.route("/choice", methods=["POST"])
def make_choice():
    data = request.get_json(silent=True) or {}

    current_stats = data.get("stats", {
        "money": 50,
        "energy": 50,
        "happiness": 50,
        "risk": 20
    })

    choice_effects = data.get("effects", {})
    result_text = data.get("result", "You made a choice and moved forward.")

    updated_stats = {
        "money": clamp_stat(current_stats.get("money", 50) + choice_effects.get("money", 0)),
        "energy": clamp_stat(current_stats.get("energy", 50) + choice_effects.get("energy", 0)),
        "happiness": clamp_stat(current_stats.get("happiness", 50) + choice_effects.get("happiness", 0)),
        "risk": clamp_stat(current_stats.get("risk", 20) + choice_effects.get("risk", 0))
    }

    next_scenario = get_random_scenario()

    # Basic ending signals
    status = "continue"
    ending_message = ""

    if updated_stats["risk"] >= 90:
        status = "game_over"
        ending_message = "Your life spiraled into dangerous territory. Risk consumed your path."
    elif updated_stats["energy"] <= 5:
        status = "game_over"
        ending_message = "Burnout caught up with you. You pushed too hard for too long."
    elif updated_stats["happiness"] <= 5:
        status = "game_over"
        ending_message = "You lost your sense of joy. Your life feels emotionally empty."
    elif updated_stats["money"] <= 5:
        status = "game_over"
        ending_message = "You ran out of money and options. Survival became your only focus."

    return jsonify({
        "result_text": result_text,
        "updated_stats": updated_stats,
        "next_scenario": next_scenario,
        "status": status,
        "ending_message": ending_message
    })


if __name__ == "__main__":
    app.run(debug=True)