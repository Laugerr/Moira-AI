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
        "domain": "work",
        "title": "First Job, First Pressure",
        "text": "You are young, low on money, and trying to build your future. A local cafe offers you a stable but tiring job, while your friend asks you to join a risky online business.",
        "conditions": {
            "age_min": 18,
            "age_max": 24,
            "money_max": 70
        },
        "choices": [
            {
                "text": "Take the cafe job for stability",
                "effects": {"money": 15, "energy": -10, "happiness": -2, "health": -4, "social": -2},
                "result": "You gain some stability, but the routine quickly starts wearing on your body and your social life."
            },
            {
                "text": "Join your friend and try the business",
                "effects": {"money": -5, "energy": -5, "happiness": 10, "health": -2, "social": 5},
                "result": "You chase opportunity with someone you trust, and the uncertainty feels exciting."
            },
            {
                "text": "Focus on learning a valuable skill instead",
                "effects": {"money": -10, "energy": -3, "happiness": 5, "health": 0, "social": -1},
                "result": "You invest in yourself and quietly build toward a better future."
            }
        ]
    },
    {
        "id": 2,
        "domain": "life",
        "title": "A New City Calls",
        "text": "A chance appears to move to a bigger city with more opportunity. The cost of living is much higher, but so is your potential.",
        "conditions": {
            "age_min": 18,
            "age_max": 35
        },
        "choices": [
            {
                "text": "Move and start over",
                "effects": {"money": -12, "energy": -8, "happiness": 8, "health": -2, "social": -3},
                "result": "The city energizes you, but the move leaves you tired and disconnected."
            },
            {
                "text": "Stay and save money",
                "effects": {"money": 10, "energy": 2, "happiness": -3, "health": 0, "social": 1},
                "result": "You stay safe financially, though life feels a little smaller."
            },
            {
                "text": "Visit first before deciding",
                "effects": {"money": -4, "energy": -2, "happiness": 4, "health": 0, "social": 1},
                "result": "You explore carefully and give yourself more time to decide."
            }
        ]
    },
    {
        "id": 3,
        "domain": "risk",
        "title": "The Tempting Shortcut",
        "text": "Someone offers you a fast way to make money online. It sounds easy, but something about it feels dangerous.",
        "conditions": {
            "age_min": 18
        },
        "choices": [
            {
                "text": "Take the shortcut",
                "effects": {"money": 20, "energy": -3, "happiness": 2, "health": -10, "social": -4},
                "result": "The money comes fast, but the pressure and paranoia start taking a toll."
            },
            {
                "text": "Refuse and stay clean",
                "effects": {"money": -2, "energy": 1, "happiness": 4, "health": 2, "social": 0},
                "result": "You protect your future, even if the decision feels frustrating today."
            },
            {
                "text": "Investigate before deciding",
                "effects": {"money": 0, "energy": -2, "happiness": 1, "health": -1, "social": 0},
                "result": "You buy yourself time by learning more before stepping into danger."
            }
        ]
    },
    {
        "id": 4,
        "domain": "education",
        "title": "The Expensive Dream",
        "text": "A course appears that could change your future, but it costs a painful amount of money. It could be a breakthrough or a mistake.",
        "conditions": {
            "age_min": 18,
            "money_min": 15
        },
        "choices": [
            {
                "text": "Buy the course",
                "effects": {"money": -18, "energy": -4, "happiness": 8, "health": 0, "social": -1},
                "result": "You take a serious bet on your future and commit to growth."
            },
            {
                "text": "Keep the money and learn for free",
                "effects": {"money": 4, "energy": -2, "happiness": 2, "health": 0, "social": 0},
                "result": "You stay safer financially and move forward more slowly."
            },
            {
                "text": "Borrow to buy it now",
                "effects": {"money": 8, "energy": -5, "happiness": 3, "health": -2, "social": -1},
                "result": "You move faster, but the pressure begins building behind the scenes."
            }
        ]
    },
    {
        "id": 5,
        "domain": "relationship",
        "title": "Love or Ambition",
        "text": "Someone important in your life wants more time from you, but your ambitions are accelerating. You cannot fully prioritize both.",
        "conditions": {
            "age_min": 20,
            "age_max": 40
        },
        "choices": [
            {
                "text": "Prioritize the relationship",
                "effects": {"money": -5, "energy": 5, "happiness": 12, "health": 3, "social": 10},
                "result": "Your heart feels fuller, and the connection strengthens your life."
            },
            {
                "text": "Prioritize ambition",
                "effects": {"money": 12, "energy": -8, "happiness": -5, "health": -3, "social": -8},
                "result": "You push ahead quickly, but the emotional cost is real."
            },
            {
                "text": "Try to balance both",
                "effects": {"money": 4, "energy": -6, "happiness": 4, "health": -1, "social": 4},
                "result": "You keep both parts of life alive, but the strain shows."
            }
        ]
    },
    {
        "id": 6,
        "domain": "health",
        "title": "Burnout Warning",
        "text": "You have been pushing too hard for too long. Your body and mind are sending you a warning.",
        "conditions": {
            "energy_max": 35
        },
        "choices": [
            {
                "text": "Take a real break",
                "effects": {"money": -6, "energy": 18, "happiness": 8, "health": 10, "social": 2},
                "result": "You slow down, recover, and regain some balance."
            },
            {
                "text": "Push through it",
                "effects": {"money": 7, "energy": -10, "happiness": -5, "health": -10, "social": -3},
                "result": "You get more done, but you feel yourself cracking."
            },
            {
                "text": "Reduce workload slightly",
                "effects": {"money": -2, "energy": 8, "happiness": 4, "health": 6, "social": 1},
                "result": "You choose moderation and begin recovering without stopping completely."
            }
        ]
    },
    {
        "id": 7,
        "domain": "money",
        "title": "An Investment Opportunity",
        "text": "A friend shows you a small investment opportunity. It might help you grow your money, or it might go badly.",
        "conditions": {
            "age_min": 21,
            "money_min": 20
        },
        "choices": [
            {
                "text": "Invest aggressively",
                "effects": {"money": 15, "energy": -2, "happiness": 5, "health": -1, "social": 2},
                "result": "You go in hard and hope the opportunity works in your favor."
            },
            {
                "text": "Invest cautiously",
                "effects": {"money": 6, "energy": -1, "happiness": 3, "health": 0, "social": 1},
                "result": "You take a measured approach and protect yourself somewhat."
            },
            {
                "text": "Skip it entirely",
                "effects": {"money": 0, "energy": 1, "happiness": -1, "health": 0, "social": 0},
                "result": "You stay safe, though you wonder what could have happened."
            }
        ]
    }
]


def is_valid_scenario(scenario):
    if not isinstance(scenario, dict):
        return False

    choices = scenario.get("choices")
    if not isinstance(choices, list) or not choices:
        return False

    required_fields = ("id", "title", "text", "domain")
    if any(not scenario.get(field) for field in required_fields):
        return False

    for choice in choices:
        if not isinstance(choice, dict):
            return False
        if not choice.get("text") or not isinstance(choice.get("effects"), dict):
            return False
        if choice.get("set_flags") and not isinstance(choice.get("set_flags"), list):
            return False
        if choice.get("clear_flags") and not isinstance(choice.get("clear_flags"), list):
            return False

    return True


def load_scenarios():
    try:
        if DATA_FILE.exists():
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    valid_scenarios = [scenario for scenario in data if is_valid_scenario(scenario)]
                    if valid_scenarios:
                        return valid_scenarios
    except Exception:
        pass
    return FALLBACK_SCENARIOS


def clamp_need(value):
    return max(0, min(100, value))


def clamp_money(value):
    return max(0, value)


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
    return "Midlife Builder"


def build_profile_snapshot(profile_seed, stats):
    age = stats.get("age", 18)
    money = stats.get("money", 50)
    health = stats.get("health", 50)
    energy = stats.get("energy", 50)
    happiness = stats.get("happiness", 50)
    social = stats.get("social", 50)

    stage = get_life_stage(age)

    if health <= 20:
        title = "Running on Empty"
        summary = "Your body has been carrying more than it should, and recovery is becoming urgent."
        mood = "Fragile"
    elif social <= 20:
        title = "Disconnected"
        summary = "You are moving through life with too little support, and the loneliness is beginning to show."
        mood = "Isolated"
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
    elif energy <= 20:
        title = "Exhausted Dreamer"
        summary = "You are still chasing your future, but your energy is becoming one of your biggest limitations."
        mood = "Burnout Warning"
    else:
        title = "Life In Progress"
        summary = "You are shaping your identity one year at a time, balancing health, connection, ambition, and stability."
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


def get_life_strengths(stats):
    ranked = sorted(
        (
            ("health", stats.get("health", 50)),
            ("energy", stats.get("energy", 50)),
            ("happiness", stats.get("happiness", 50)),
            ("social", stats.get("social", 50)),
            ("money", stats.get("money", 50)),
        ),
        key=lambda item: item[1],
        reverse=True,
    )
    return ranked[0][0], ranked[-1][0]


def build_ending(status, stats, profile_seed):
    strongest, weakest = get_life_strengths(stats)
    dream = profile_seed.get("dream", "build a meaningful life")

    if status == "health":
        return {
            "title": "Health Gave Out",
            "message": "Your body absorbed too many hard years without enough recovery. Ambition kept moving, but your health could not carry the weight any longer."
        }
    if status == "energy":
        return {
            "title": "Burned Out",
            "message": "You kept pushing through exhaustion until there was nothing left to draw from. The life you were building asked more from you than you could keep giving."
        }
    if status == "happiness":
        return {
            "title": "Joy Slipped Away",
            "message": "You stayed in motion, but somewhere along the way the meaning drained out of it. A life without enough joy became too heavy to continue."
        }
    if status == "social":
        return {
            "title": "Left Too Alone",
            "message": "Distance grew where support should have been. Without enough closeness or belonging, even ordinary years became harder to survive."
        }
    if status == "money":
        return {
            "title": "Out of Options",
            "message": "Your resources ran too low and survival took over every other priority. The pressure of getting by left too little room to keep shaping your future."
        }
    if status == "no_scenarios":
        return {
            "title": "A Quiet Pause",
            "message": "This chapter closes with unfinished possibilities still in the air. Your life kept moving, but the record of major turning points comes to rest here."
        }

    strongest_lines = {
        "health": "You protected your health well enough to keep going through changing seasons of life.",
        "energy": "You managed your energy carefully enough to keep showing up for the life you wanted.",
        "happiness": "You kept returning to what made life feel warm, personal, and worth living.",
        "social": "You built enough connection that your life was not carried alone.",
        "money": "You turned money into a stabilizing force instead of letting scarcity control every choice.",
    }

    weakest_lines = {
        "health": "Your health remained one of the hardest parts of your journey.",
        "energy": "Energy was a constant challenge, even when other parts of life improved.",
        "happiness": "Happiness was harder to hold onto than it should have been.",
        "social": "Connection never came as easily or as steadily as you needed.",
        "money": "Money kept adding pressure, even when you found momentum elsewhere.",
    }

    completion_titles = {
        "money": "Built for Stability",
        "social": "A Life of Connection",
        "happiness": "A Fulfilled Journey",
        "health": "Steady Through the Years",
        "energy": "Still Standing",
    }

    return {
        "title": completion_titles.get(strongest, "Journey Complete"),
        "message": (
            f"You reached later adulthood still chasing your dream to {dream}. "
            f"{strongest_lines[strongest]} {weakest_lines[weakest]}"
        )
    }


def scenario_matches_player(scenario, stats, life_flags=None):
    conditions = scenario.get("conditions", {})
    active_flags = set(life_flags or [])

    checks = {
        "age_min": lambda v: stats.get("age", 18) >= v,
        "age_max": lambda v: stats.get("age", 18) <= v,
        "money_min": lambda v: stats.get("money", 50) >= v,
        "money_max": lambda v: stats.get("money", 50) <= v,
        "health_min": lambda v: stats.get("health", 50) >= v,
        "health_max": lambda v: stats.get("health", 50) <= v,
        "energy_min": lambda v: stats.get("energy", 50) >= v,
        "energy_max": lambda v: stats.get("energy", 50) <= v,
        "happiness_min": lambda v: stats.get("happiness", 50) >= v,
        "happiness_max": lambda v: stats.get("happiness", 50) <= v,
        "social_min": lambda v: stats.get("social", 50) >= v,
        "social_max": lambda v: stats.get("social", 50) <= v,
    }

    for key, value in conditions.items():
        if key == "flags_include":
            if not set(value).issubset(active_flags):
                return False
            continue

        if key == "flags_exclude":
            if set(value) & active_flags:
                return False
            continue

        if key in checks and not checks[key](value):
            return False

    return True


def get_life_stage_domain_bias(age):
    stage = get_life_stage(age)

    if stage == "Emerging Adult":
        return {
            "education": 4,
            "work": 3,
            "growth": 3,
            "life": 2,
            "risk": 1,
        }

    if stage == "Young Professional":
        return {
            "work": 4,
            "money": 3,
            "housing": 2,
            "social": 2,
            "relationship": 2,
            "growth": 1,
        }

    if stage == "Established Adult":
        return {
            "work": 3,
            "family": 3,
            "housing": 3,
            "money": 2,
            "health": 2,
            "social": 1,
        }

    return {
        "health": 4,
        "family": 3,
        "growth": 3,
        "life": 3,
        "money": 2,
        "social": 2,
    }


def get_recent_domains(scenarios, used_scenarios, recent_count=2):
    scenario_by_id = {scenario.get("id"): scenario for scenario in scenarios}
    recent_domains = []

    for scenario_id in reversed(used_scenarios):
        scenario = scenario_by_id.get(scenario_id)
        if not scenario:
            continue

        recent_domains.append(scenario.get("domain", "general"))
        if len(recent_domains) >= recent_count:
            break

    return recent_domains


def score_scenario(scenario, stats, used_scenarios, scenarios):
    domain = scenario.get("domain", "general")
    age = stats.get("age", 18)
    money = stats.get("money", 50)
    health = stats.get("health", 50)
    energy = stats.get("energy", 50)
    happiness = stats.get("happiness", 50)
    social = stats.get("social", 50)

    score = random.random()
    stage_bias = get_life_stage_domain_bias(age)
    score += stage_bias.get(domain, 0)

    if money <= 25 and domain in {"money", "work", "housing"}:
        score += 4
    if health <= 35 and domain == "health":
        score += 5
    if energy <= 35 and domain in {"health", "life"}:
        score += 4
    if happiness <= 35 and domain in {"growth", "social", "life", "relationship"}:
        score += 4
    if social <= 35 and domain in {"social", "family", "relationship"}:
        score += 5

    if money >= 70 and domain in {"growth", "education", "housing"}:
        score += 2
    if social >= 70 and domain in {"relationship", "family", "social"}:
        score += 2
    if happiness >= 70 and domain in {"growth", "life", "social"}:
        score += 1.5

    used_domain_counts = {}
    for item in scenarios:
        if item.get("id") in used_scenarios:
            used_domain = item.get("domain", "general")
            used_domain_counts[used_domain] = used_domain_counts.get(used_domain, 0) + 1

    score -= used_domain_counts.get(domain, 0) * 0.75

    recent_domains = get_recent_domains(scenarios, used_scenarios)
    if recent_domains:
        if domain == recent_domains[0]:
            score -= 4
        elif domain in recent_domains:
            score -= 2

    return score


def get_next_scenario(stats, used_scenarios, life_flags=None):
    scenarios = load_scenarios()

    matching = [
        s for s in scenarios
        if scenario_matches_player(s, stats, life_flags) and s.get("id") not in used_scenarios
    ]

    if not matching:
        matching = [s for s in scenarios if scenario_matches_player(s, stats, life_flags)]

    if not matching:
        matching = FALLBACK_SCENARIOS

    if not matching:
        return None

    return max(
        matching,
        key=lambda scenario: score_scenario(scenario, stats, used_scenarios, scenarios)
    )


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/start", methods=["GET"])
def start_game():
    initial_stats = {
        "age": 18,
        "money": 50,
        "health": 50,
        "energy": 50,
        "happiness": 50,
        "social": 50
    }

    profile_seed = generate_profile_seed()
    life_flags = []
    scenario = get_next_scenario(initial_stats, [], life_flags)

    return jsonify({
        "scenario": scenario,
        "stats": initial_stats,
        "life_flags": life_flags,
        "profile_seed": profile_seed,
        "player_profile": build_profile_snapshot(profile_seed, initial_stats),
        "history": [
            {
                "age": 18,
                "event": "You entered adulthood with uncertainty, potential, and a future still unwritten."
            }
        ],
        "used_scenarios": [scenario.get("id")] if scenario else [],
        "message": "Your life begins. Every year, every choice, every consequence matters."
    })


@app.route("/choice", methods=["POST"])
def make_choice():
    data = request.get_json(silent=True) or {}

    current_stats = data.get("stats", {
        "age": 18,
        "money": 50,
        "health": 50,
        "energy": 50,
        "happiness": 50,
        "social": 50
    })

    history = data.get("history", [])
    used_scenarios = data.get("used_scenarios", [])
    life_flags = data.get("life_flags", [])
    profile_seed = data.get("profile_seed") or generate_profile_seed()
    choice_effects = data.get("effects", {})
    result_text = data.get("result", "You made a choice and moved forward.")
    set_flags = data.get("set_flags", [])
    clear_flags = data.get("clear_flags", [])

    updated_stats = {
        "age": current_stats.get("age", 18) + 1,
        "money": clamp_money(current_stats.get("money", 50) + choice_effects.get("money", 0)),
        "health": clamp_need(current_stats.get("health", 50) + choice_effects.get("health", 0)),
        "energy": clamp_need(current_stats.get("energy", 50) + choice_effects.get("energy", 0)),
        "happiness": clamp_need(current_stats.get("happiness", 50) + choice_effects.get("happiness", 0)),
        "social": clamp_need(current_stats.get("social", 50) + choice_effects.get("social", 0))
    }

    history.append({
        "age": updated_stats["age"],
        "event": result_text
    })

    updated_life_flags = [flag for flag in life_flags if flag not in clear_flags]
    for flag in set_flags:
        if flag not in updated_life_flags:
            updated_life_flags.append(flag)

    status = "continue"
    ending_title = ""
    ending_message = ""

    if updated_stats["health"] <= 5:
        status = "game_over"
        ending = build_ending("health", updated_stats, profile_seed)
        ending_title = ending["title"]
        ending_message = ending["message"]
    elif updated_stats["energy"] <= 5:
        status = "game_over"
        ending = build_ending("energy", updated_stats, profile_seed)
        ending_title = ending["title"]
        ending_message = ending["message"]
    elif updated_stats["happiness"] <= 5:
        status = "game_over"
        ending = build_ending("happiness", updated_stats, profile_seed)
        ending_title = ending["title"]
        ending_message = ending["message"]
    elif updated_stats["social"] <= 5:
        status = "game_over"
        ending = build_ending("social", updated_stats, profile_seed)
        ending_title = ending["title"]
        ending_message = ending["message"]
    elif updated_stats["money"] <= 5:
        status = "game_over"
        ending = build_ending("money", updated_stats, profile_seed)
        ending_title = ending["title"]
        ending_message = ending["message"]
    elif updated_stats["age"] >= 60:
        status = "completed"
        ending = build_ending("completed", updated_stats, profile_seed)
        ending_title = ending["title"]
        ending_message = ending["message"]

    next_scenario = None

    if status == "continue":
        next_scenario = get_next_scenario(updated_stats, used_scenarios, updated_life_flags)
        if next_scenario:
            used_scenarios.append(next_scenario.get("id"))
        else:
            status = "completed"
            ending = build_ending("no_scenarios", updated_stats, profile_seed)
            ending_title = ending["title"]
            ending_message = ending["message"]

    return jsonify({
        "result_text": result_text,
        "updated_stats": updated_stats,
        "life_flags": updated_life_flags,
        "profile_seed": profile_seed,
        "player_profile": build_profile_snapshot(profile_seed, updated_stats),
        "history": history,
        "used_scenarios": used_scenarios,
        "next_scenario": next_scenario,
        "status": status,
        "ending_title": ending_title,
        "ending_message": ending_message
    })


if __name__ == "__main__":
    app.run(debug=True)
