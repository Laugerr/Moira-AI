from flask import Flask, render_template, jsonify, request
import json
import random
from pathlib import Path

app = Flask(__name__)

DATA_FILE = Path("data/scenarios.json")

FIRST_NAMES = [
    "Avery", "Jordan", "Sage", "Milan", "Noah", "Lena", "Kai", "Elena",
    "Theo", "Amara", "Ezra", "Nina", "Julian", "Zara", "Ivy", "Leo"
]

LAST_NAMES = [
    "Vale", "Mercer", "Rowe", "Bennett", "Hale", "Cross", "Quinn", "Blake",
    "Santos", "Cole", "Hart", "Lane", "Marlow", "Stone", "Reed", "Brooks"
]

HOMETOWNS = [
    "Kyiv, Ukraine", "Toronto, Canada", "Lisbon, Portugal", "Chicago, USA",
    "Seoul, South Korea", "Prague, Czech Republic", "Valencia, Spain",
    "Warsaw, Poland", "Tallinn, Estonia", "Melbourne, Australia"
]

STARTING_TRAITS = [
    "ambitious", "curious", "restless", "thoughtful",
    "bold", "resourceful", "idealistic", "independent"
]

STARTING_DREAMS = [
    "build a meaningful career",
    "create financial freedom",
    "find a life that feels exciting",
    "prove their potential",
    "turn talent into stability",
    "build a future on their own terms"
]


FALLBACK_SCENARIOS = [
    {
        "id": 1,
        "title": "First Job, First Pressure",
        "text": "You are young, low on money, and trying to build your future. A local café offers you a stable but tiring job, while your friend asks you to join a risky online business.",
        "conditions": {
            "age_min": 18,
            "age_max": 24,
            "money_max": 70
        },
        "choices": [
            {
                "text": "Take the café job for stability",
                "effects": {"money": 15, "energy": -10, "happiness": -2, "risk": -5},
                "result": "You gain some stability, but routine begins to wear you down."
            },
            {
                "text": "Join your friend and try the business",
                "effects": {"money": -5, "energy": -5, "happiness": 10, "risk": 15},
                "result": "You chase opportunity, but your future becomes less certain."
            },
            {
                "text": "Focus on learning a valuable skill instead",
                "effects": {"money": -10, "energy": -3, "happiness": 5, "risk": 6},
                "result": "You invest in yourself, hoping the payoff comes later."
            }
        ]
    },
    {
        "id": 2,
        "title": "A New City Calls",
        "text": "A chance appears to move to a bigger city with more opportunity. The cost of living is much higher, but so is your potential.",
        "conditions": {
            "age_min": 18,
            "age_max": 35
        },
        "choices": [
            {
                "text": "Move and start over",
                "effects": {"money": -12, "energy": -8, "happiness": 8, "risk": 10},
                "result": "The city excites you, but survival becomes more expensive."
            },
            {
                "text": "Stay and save money",
                "effects": {"money": 10, "energy": 2, "happiness": -3, "risk": -3},
                "result": "You stay safe financially, though life feels smaller."
            },
            {
                "text": "Visit first before deciding",
                "effects": {"money": -4, "energy": -2, "happiness": 4, "risk": 2},
                "result": "You test the waters without fully committing."
            }
        ]
    },
    {
        "id": 3,
        "title": "The Tempting Shortcut",
        "text": "Someone offers you a fast way to make money online. It sounds easy, but something about it feels dangerous.",
        "conditions": {
            "age_min": 18,
            "risk_max": 75
        },
        "choices": [
            {
                "text": "Take the shortcut",
                "effects": {"money": 20, "energy": -3, "happiness": 2, "risk": 20},
                "result": "The money arrives quickly, but danger follows close behind."
            },
            {
                "text": "Refuse and stay clean",
                "effects": {"money": -2, "energy": 1, "happiness": 4, "risk": -10},
                "result": "You protect your future, even if it feels frustrating now."
            },
            {
                "text": "Investigate before deciding",
                "effects": {"money": 0, "energy": -2, "happiness": 1, "risk": 4},
                "result": "You buy yourself time by learning more."
            }
        ]
    },
    {
        "id": 4,
        "title": "The Expensive Dream",
        "text": "A course appears that could change your future, but it costs a painful amount of money. It could be a breakthrough or a mistake.",
        "conditions": {
            "age_min": 18,
            "money_min": 15
        },
        "choices": [
            {
                "text": "Buy the course",
                "effects": {"money": -18, "energy": -4, "happiness": 8, "risk": 8},
                "result": "You take a serious bet on your future."
            },
            {
                "text": "Keep the money and learn for free",
                "effects": {"money": 4, "energy": -2, "happiness": 2, "risk": -2},
                "result": "You stay safer financially and progress more slowly."
            },
            {
                "text": "Borrow to buy it now",
                "effects": {"money": 8, "energy": -5, "happiness": 3, "risk": 12},
                "result": "You move faster, but pressure builds behind the scenes."
            }
        ]
    },
    {
        "id": 5,
        "title": "Love or Ambition",
        "text": "Someone important in your life wants more time from you, but your ambitions are accelerating. You cannot fully prioritize both.",
        "conditions": {
            "age_min": 20,
            "age_max": 40
        },
        "choices": [
            {
                "text": "Prioritize the relationship",
                "effects": {"money": -5, "energy": 5, "happiness": 12, "risk": -3},
                "result": "Your heart feels fuller, though your progress slows."
            },
            {
                "text": "Prioritize ambition",
                "effects": {"money": 12, "energy": -8, "happiness": -5, "risk": 6},
                "result": "You move forward quickly, but emotionally it costs you."
            },
            {
                "text": "Try to balance both",
                "effects": {"money": 4, "energy": -10, "happiness": 4, "risk": 4},
                "result": "You hold both worlds together, but the strain is real."
            }
        ]
    },
    {
        "id": 6,
        "title": "Burnout Warning",
        "text": "You have been pushing too hard for too long. Your body and mind are sending you a warning.",
        "conditions": {
            "energy_max": 35
        },
        "choices": [
            {
                "text": "Take a real break",
                "effects": {"money": -6, "energy": 18, "happiness": 8, "risk": -6},
                "result": "You slow down and recover some of what you lost."
            },
            {
                "text": "Push through it",
                "effects": {"money": 10, "energy": -12, "happiness": -6, "risk": 10},
                "result": "You get more done, but you feel yourself cracking."
            },
            {
                "text": "Reduce workload slightly",
                "effects": {"money": -2, "energy": 8, "happiness": 4, "risk": -2},
                "result": "You choose moderation and regain some balance."
            }
        ]
    },
    {
        "id": 7,
        "title": "An Investment Opportunity",
        "text": "A friend shows you a small investment opportunity. It might help you grow your money, or it might go badly.",
        "conditions": {
            "age_min": 21,
            "money_min": 20
        },
        "choices": [
            {
                "text": "Invest aggressively",
                "effects": {"money": 15, "energy": -2, "happiness": 5, "risk": 14},
                "result": "You go in hard and hope the opportunity works in your favor."
            },
            {
                "text": "Invest cautiously",
                "effects": {"money": 6, "energy": -1, "happiness": 3, "risk": 5},
                "result": "You take a measured approach and protect yourself somewhat."
            },
            {
                "text": "Skip it entirely",
                "effects": {"money": 0, "energy": 1, "happiness": -1, "risk": -3},
                "result": "You stay safe, though you wonder what could have happened."
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


def generate_profile_seed():
    return {
        "name": f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
        "hometown": random.choice(HOMETOWNS),
        "trait": random.choice(STARTING_TRAITS),
        "dream": random.choice(STARTING_DREAMS),
    }


def get_life_stage(age):
    if age <= 22:
        return "Emerging Adult"
    if age <= 30:
        return "Young Professional"
    if age <= 45:
        return "Established Adult"
    if age <= 59:
        return "Midlife Builder"
    return "Legacy Years"


def build_profile_snapshot(profile_seed, stats):
    age = stats.get("age", 18)
    money = stats.get("money", 50)
    energy = stats.get("energy", 50)
    happiness = stats.get("happiness", 50)
    risk = stats.get("risk", 20)

    stage = get_life_stage(age)

    if risk >= 75:
        title = "Volatile Path"
        summary = "Your choices are creating fast momentum, but danger is now part of daily life."
        mood = "High Risk"
    elif energy <= 20:
        title = "Exhausted Dreamer"
        summary = "You are still chasing your future, but your energy is becoming one of your biggest limitations."
        mood = "Burnout Warning"
    elif happiness >= 70 and money >= 60:
        title = "Rising Success Story"
        summary = "You are building a life with visible momentum, stronger stability, and room for bigger ambitions."
        mood = "Thriving"
    elif money <= 25:
        title = "Under Pressure"
        summary = "Money is tight, and every decision feels heavier because survival is always in the background."
        mood = "Financial Stress"
    elif happiness <= 25:
        title = "Emotionally Drained"
        summary = "Even when life keeps moving, your sense of joy is fading. Recovery matters now."
        mood = "Low Morale"
    else:
        title = "Life In Progress"
        summary = "You are shaping your identity one year at a time, balancing risk, ambition, and stability."
        mood = "Steady"

    return {
        "name": profile_seed["name"],
        "hometown": profile_seed["hometown"],
        "trait": profile_seed["trait"].title(),
        "dream": profile_seed["dream"],
        "stage": stage,
        "title": title,
        "summary": summary,
        "mood": mood,
        "age_badge": f"Age {age}",
    }


def scenario_matches_player(scenario, stats):
    conditions = scenario.get("conditions", {})

    checks = {
        "age_min": lambda v: stats.get("age", 18) >= v,
        "age_max": lambda v: stats.get("age", 18) <= v,
        "money_min": lambda v: stats.get("money", 50) >= v,
        "money_max": lambda v: stats.get("money", 50) <= v,
        "energy_min": lambda v: stats.get("energy", 50) >= v,
        "energy_max": lambda v: stats.get("energy", 50) <= v,
        "happiness_min": lambda v: stats.get("happiness", 50) >= v,
        "happiness_max": lambda v: stats.get("happiness", 50) <= v,
        "risk_min": lambda v: stats.get("risk", 20) >= v,
        "risk_max": lambda v: stats.get("risk", 20) <= v,
    }

    for key, value in conditions.items():
        if key in checks and not checks[key](value):
            return False

    return True


def get_next_scenario(stats, used_scenarios):
    scenarios = load_scenarios()

    matching = [
        s for s in scenarios
        if scenario_matches_player(s, stats) and s.get("id") not in used_scenarios
    ]

    if not matching:
        matching = [s for s in scenarios if scenario_matches_player(s, stats)]

    if not matching:
        matching = scenarios

    return random.choice(matching)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/start", methods=["GET"])
def start_game():
    initial_stats = {
        "age": 18,
        "money": 50,
        "energy": 50,
        "happiness": 50,
        "risk": 20
    }

    profile_seed = generate_profile_seed()
    scenario = get_next_scenario(initial_stats, [])

    return jsonify({
        "scenario": scenario,
        "stats": initial_stats,
        "profile_seed": profile_seed,
        "player_profile": build_profile_snapshot(profile_seed, initial_stats),
        "history": [
            {
                "age": 18,
                "event": "You entered adulthood with uncertainty, potential, and a future still unwritten."
            }
        ],
        "used_scenarios": [scenario.get("id")],
        "message": "Your life begins. Every year, every choice, every consequence matters."
    })


@app.route("/choice", methods=["POST"])
def make_choice():
    data = request.get_json(silent=True) or {}

    current_stats = data.get("stats", {
        "age": 18,
        "money": 50,
        "energy": 50,
        "happiness": 50,
        "risk": 20
    })

    history = data.get("history", [])
    used_scenarios = data.get("used_scenarios", [])
    profile_seed = data.get("profile_seed") or generate_profile_seed()
    choice_effects = data.get("effects", {})
    result_text = data.get("result", "You made a choice and moved forward.")

    updated_stats = {
        "age": current_stats.get("age", 18) + 1,
        "money": clamp_stat(current_stats.get("money", 50) + choice_effects.get("money", 0)),
        "energy": clamp_stat(current_stats.get("energy", 50) + choice_effects.get("energy", 0)),
        "happiness": clamp_stat(current_stats.get("happiness", 50) + choice_effects.get("happiness", 0)),
        "risk": clamp_stat(current_stats.get("risk", 20) + choice_effects.get("risk", 0))
    }

    history.append({
        "age": updated_stats["age"],
        "event": result_text
    })

    status = "continue"
    ending_message = ""

    if updated_stats["risk"] >= 90:
        status = "game_over"
        ending_message = "Your life spiraled into dangerous territory. Risk took control of your future."
    elif updated_stats["energy"] <= 5:
        status = "game_over"
        ending_message = "Burnout finally broke you. You pushed too hard for too long."
    elif updated_stats["happiness"] <= 5:
        status = "game_over"
        ending_message = "You lost your sense of joy and purpose. Life became emotionally empty."
    elif updated_stats["money"] <= 5:
        status = "game_over"
        ending_message = "You ran out of money and options. Survival became your whole reality."
    elif updated_stats["age"] >= 60:
        status = "completed"
        ending_message = "You reached later adulthood. Your journey ends with a life shaped by every decision you made."

    next_scenario = None

    if status == "continue":
        next_scenario = get_next_scenario(updated_stats, used_scenarios)
        used_scenarios.append(next_scenario.get("id"))

    return jsonify({
        "result_text": result_text,
        "updated_stats": updated_stats,
        "profile_seed": profile_seed,
        "player_profile": build_profile_snapshot(profile_seed, updated_stats),
        "history": history,
        "used_scenarios": used_scenarios,
        "next_scenario": next_scenario,
        "status": status,
        "ending_message": ending_message
    })


if __name__ == "__main__":
    app.run(debug=True)
