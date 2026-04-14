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

CAREER_LEVELS = {
    0: {"title": "Unemployed", "salary": 0},
    1: {"title": "Entry-Level Worker", "salary": 6},
    2: {"title": "Junior Professional", "salary": 13},
    3: {"title": "Mid-Level Professional", "salary": 22},
    4: {"title": "Senior Professional", "salary": 34},
    5: {"title": "Director", "salary": 50},
}

EDUCATION_LEVELS = {
    0: {"label": "No Degree"},
    1: {"label": "High School"},
    2: {"label": "College Degree"},
    3: {"label": "Postgraduate"},
}


def get_salary(career_level):
    return CAREER_LEVELS.get(min(int(career_level), 5), CAREER_LEVELS[0])["salary"]


def get_living_cost(age):
    if age <= 22:
        return 3
    if age <= 30:
        return 5
    if age <= 45:
        return 7
    return 6


PLAYER_ACTIONS = [
    {
        "id": "apply_jobs",
        "title": "Apply for Jobs",
        "subtitle": "Start your career path",
        "description": "Actively search and apply for entry-level positions. Getting your foot in the door is the first step.",
        "effects": {"money": -2, "health": 0, "energy": -6, "happiness": 3, "social": 2, "career_change": 1},
        "result": "After a stretch of effort and rejection, you land your first real job. Your career has a starting point now.",
        "conditions": {
            "career_level_max": 0,
            "energy_min": 15
        },
        "set_flags": ["career_started"]
    },
    {
        "id": "work_shift",
        "title": "Work Extra",
        "subtitle": "Trade comfort for cash",
        "description": "Take on extra work to boost your finances this year, even if it costs you energy.",
        "effects": {"money": 10, "health": -2, "energy": -8, "happiness": -2, "social": -2},
        "result": "You put in extra hours and earn more money, but the pressure clearly costs you.",
        "conditions": {
            "energy_min": 18
        }
    },
    {
        "id": "study_focus",
        "title": "Study",
        "subtitle": "Build long-term potential",
        "description": "Spend time learning and improving your future options at the cost of short-term energy.",
        "effects": {"money": -4, "health": 0, "energy": -5, "happiness": 3, "social": -1},
        "result": "You invest time in growth and quietly become more capable than you were last year.",
        "conditions": {
            "energy_min": 15,
            "money_min": 4
        },
        "set_flags": ["self_improvement"]
    },
    {
        "id": "rest_reset",
        "title": "Rest",
        "subtitle": "Recover before you crack",
        "description": "Slow down and protect yourself before stress and fatigue become something worse.",
        "effects": {"money": -3, "health": 6, "energy": 12, "happiness": 4, "social": 1},
        "result": "You give yourself time to recover, and the decision makes the rest of life feel more manageable.",
    },
    {
        "id": "social_time",
        "title": "Socialize",
        "subtitle": "Invest in connection",
        "description": "Spend real time with people who matter and keep your relationships alive.",
        "effects": {"money": -4, "health": 1, "energy": -2, "happiness": 7, "social": 9},
        "result": "You reconnect with people around you and feel less alone in the life you are building.",
        "conditions": {
            "money_min": 4
        }
    }
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
                "effects": {"money": 8, "energy": -10, "happiness": -2, "health": -4, "social": -2, "career_change": 1},
                "result": "You gain some stability, but the routine quickly starts wearing on your body and your social life."
            },
            {
                "text": "Join your friend and try the business",
                "effects": {"money": -5, "energy": -5, "happiness": 10, "health": -2, "social": 5},
                "result": "You chase opportunity with someone you trust, and the uncertainty feels exciting."
            },
            {
                "text": "Focus on learning a valuable skill instead",
                "effects": {"money": -10, "energy": -3, "happiness": 5, "health": 0, "social": -1, "education_change": 1},
                "result": "You invest in yourself and quietly build toward a better future."
            }
        ]
    },
    {
        "id": 2,
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
        "id": 3,
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
                    valid = [s for s in data if is_valid_scenario(s)]
                    if valid:
                        return valid
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


def build_career_state(career_state, effects):
    career_level = career_state.get("career_level", 0)
    education_level = career_state.get("education_level", 1)
    return {
        "career_level": max(0, min(5, career_level + effects.get("career_change", 0))),
        "education_level": max(0, min(3, education_level + effects.get("education_change", 0)))
    }


def build_profile_snapshot(profile_seed, stats, career_state=None):
    age = stats.get("age", 18)
    money = stats.get("money", 50)
    health = stats.get("health", 50)
    energy = stats.get("energy", 50)
    happiness = stats.get("happiness", 50)
    social = stats.get("social", 50)

    career_level = (career_state or {}).get("career_level", 0)
    education_level = (career_state or {}).get("education_level", 1)
    job_title = CAREER_LEVELS.get(career_level, CAREER_LEVELS[0])["title"]
    education_label = EDUCATION_LEVELS.get(education_level, EDUCATION_LEVELS[1])["label"]
    salary = get_salary(career_level)
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
    elif career_level >= 4:
        title = "Established Force"
        summary = "Years of building have compounded. You carry real professional weight and the confidence to match."
        mood = "In Command"
    elif career_level == 0 and age >= 24:
        title = "Still Finding Ground"
        summary = "The career piece hasn't locked in yet, and the uncertainty is adding weight to everything else."
        mood = "Searching"
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
        "job_title": job_title,
        "education_label": education_label,
        "salary": salary,
        "career_level": career_level,
    }


def action_matches_player(action, stats, life_flags=None, career_state=None):
    return scenario_matches_player(
        {"conditions": action.get("conditions", {})},
        stats, life_flags, career_state
    )


def get_available_actions(stats, life_flags=None, career_state=None):
    return [
        {
            "id": a["id"],
            "title": a["title"],
            "subtitle": a["subtitle"],
            "description": a["description"],
        }
        for a in PLAYER_ACTIONS
        if action_matches_player(a, stats, life_flags, career_state)
    ]


def find_action(action_id):
    for action in PLAYER_ACTIONS:
        if action["id"] == action_id:
            return action
    return None


def build_updated_stats(current_stats, effects, career_level=0, increment_age=True):
    """Apply effects to stats. When increment_age=True, also advances one year
    and applies recurring salary and living costs. Actions and choices use
    increment_age=False — only /age advances time."""
    age = current_stats.get("age", 18)
    money_delta = effects.get("money", 0)

    if increment_age:
        money_delta += get_salary(career_level) - get_living_cost(age)

    return {
        "age": age + (1 if increment_age else 0),
        "money": clamp_money(current_stats.get("money", 50) + money_delta),
        "health": clamp_need(current_stats.get("health", 50) + effects.get("health", 0)),
        "energy": clamp_need(current_stats.get("energy", 50) + effects.get("energy", 0)),
        "happiness": clamp_need(current_stats.get("happiness", 50) + effects.get("happiness", 0)),
        "social": clamp_need(current_stats.get("social", 50) + effects.get("social", 0))
    }


def apply_flag_changes(life_flags, set_flags=None, clear_flags=None):
    updated = [f for f in life_flags if f not in (clear_flags or [])]
    for flag in set_flags or []:
        if flag not in updated:
            updated.append(flag)
    return updated


def evaluate_run_status(stats, profile_seed):
    if stats["health"] <= 5:
        ending = build_ending("health", stats, profile_seed)
        return "game_over", ending["title"], ending["message"]
    if stats["energy"] <= 5:
        ending = build_ending("energy", stats, profile_seed)
        return "game_over", ending["title"], ending["message"]
    if stats["happiness"] <= 5:
        ending = build_ending("happiness", stats, profile_seed)
        return "game_over", ending["title"], ending["message"]
    if stats["social"] <= 5:
        ending = build_ending("social", stats, profile_seed)
        return "game_over", ending["title"], ending["message"]
    if stats["money"] <= 5:
        ending = build_ending("money", stats, profile_seed)
        return "game_over", ending["title"], ending["message"]
    if stats["age"] >= 60:
        ending = build_ending("completed", stats, profile_seed)
        return "completed", ending["title"], ending["message"]
    return "continue", "", ""


def get_life_strengths(stats):
    ranked = sorted(
        [
            ("health", stats.get("health", 50)),
            ("energy", stats.get("energy", 50)),
            ("happiness", stats.get("happiness", 50)),
            ("social", stats.get("social", 50)),
            ("money", stats.get("money", 50)),
        ],
        key=lambda item: item[1],
        reverse=True,
    )
    return ranked[0][0], ranked[-1][0]


def build_ending(status, stats, profile_seed, career_state=None):
    strongest, weakest = get_life_strengths(stats)
    dream = profile_seed.get("dream", "build a meaningful life")
    career_level = (career_state or {}).get("career_level", 0)
    job_title = CAREER_LEVELS.get(career_level, CAREER_LEVELS[0])["title"]

    failure_messages = {
        "health": ("Health Gave Out", "Your body absorbed too many hard years without enough recovery. Ambition kept moving, but your health could not carry the weight any longer."),
        "energy": ("Burned Out", "You kept pushing through exhaustion until there was nothing left to draw from. The life you were building asked more from you than you could keep giving."),
        "happiness": ("Joy Slipped Away", "You stayed in motion, but somewhere along the way the meaning drained out of it. A life without enough joy became too heavy to continue."),
        "social": ("Left Too Alone", "Distance grew where support should have been. Without enough closeness or belonging, even ordinary years became harder to survive."),
        "money": ("Out of Options", "Your resources ran too low and survival took over every other priority. The pressure of getting by left too little room to keep shaping your future."),
        "no_scenarios": ("A Quiet Pause", "This chapter closes with unfinished possibilities still in the air. Your life kept moving, but the record of major turning points comes to rest here."),
    }

    if status in failure_messages:
        title, message = failure_messages[status]
        return {"title": title, "message": message}

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

    career_line = ""
    if career_level >= 4:
        career_line = f" You reached the level of {job_title}, a result of years of deliberate effort."
    elif career_level >= 2:
        career_line = f" You built a career as a {job_title} that gave your adult years shape and direction."

    return {
        "title": completion_titles.get(strongest, "Journey Complete"),
        "message": (
            f"You reached later adulthood still chasing your dream to {dream}."
            f"{career_line} "
            f"{strongest_lines[strongest]} {weakest_lines[weakest]}"
        )
    }


def scenario_matches_player(scenario, stats, life_flags=None, career_state=None):
    conditions = scenario.get("conditions", {})
    active_flags = set(life_flags or [])
    career_level = (career_state or {}).get("career_level", 0)
    education_level = (career_state or {}).get("education_level", 1)

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
        "career_level_min": lambda v: career_level >= v,
        "career_level_max": lambda v: career_level <= v,
        "education_level_min": lambda v: education_level >= v,
        "education_level_max": lambda v: education_level <= v,
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
        return {"education": 4, "work": 3, "growth": 3, "life": 2, "risk": 1}
    if stage == "Young Professional":
        return {"work": 4, "money": 3, "housing": 2, "social": 2, "relationship": 2, "growth": 1}
    if stage == "Established Adult":
        return {"work": 3, "family": 3, "housing": 3, "money": 2, "health": 2, "social": 1}
    return {"health": 4, "family": 3, "growth": 3, "life": 3, "money": 2, "social": 2}


def get_recent_domains(scenarios, used_scenarios, recent_count=2):
    scenario_by_id = {s.get("id"): s for s in scenarios}
    recent = []
    for sid in reversed(used_scenarios):
        s = scenario_by_id.get(sid)
        if s:
            recent.append(s.get("domain", "general"))
            if len(recent) >= recent_count:
                break
    return recent


def score_scenario(scenario, stats, used_scenarios, scenarios, career_state=None):
    domain = scenario.get("domain", "general")
    age = stats.get("age", 18)
    money = stats.get("money", 50)
    health = stats.get("health", 50)
    energy = stats.get("energy", 50)
    happiness = stats.get("happiness", 50)
    social = stats.get("social", 50)
    career_level = (career_state or {}).get("career_level", 0)
    education_level = (career_state or {}).get("education_level", 1)

    score = random.random()
    score += get_life_stage_domain_bias(age).get(domain, 0)

    if money <= 25 and domain in {"money", "work", "housing"}: score += 4
    if health <= 35 and domain == "health": score += 5
    if energy <= 35 and domain in {"health", "life"}: score += 4
    if happiness <= 35 and domain in {"growth", "social", "life", "relationship"}: score += 4
    if social <= 35 and domain in {"social", "family", "relationship"}: score += 5
    if money >= 70 and domain in {"growth", "education", "housing"}: score += 2
    if social >= 70 and domain in {"relationship", "family", "social"}: score += 2
    if happiness >= 70 and domain in {"growth", "life", "social"}: score += 1.5
    if career_level == 0 and domain == "work" and age >= 20: score += 4
    if career_level >= 1 and career_level <= 3 and domain == "work": score += 1.5
    if education_level == 1 and domain == "education" and age <= 26: score += 3

    used_domain_counts = {}
    for item in scenarios:
        if item.get("id") in used_scenarios:
            d = item.get("domain", "general")
            used_domain_counts[d] = used_domain_counts.get(d, 0) + 1
    score -= used_domain_counts.get(domain, 0) * 0.75

    recent = get_recent_domains(scenarios, used_scenarios)
    if recent:
        if domain == recent[0]: score -= 4
        elif domain in recent: score -= 2

    return score


def get_next_scenario(stats, used_scenarios, life_flags=None, career_state=None):
    scenarios = load_scenarios()
    matching = [
        s for s in scenarios
        if scenario_matches_player(s, stats, life_flags, career_state) and s.get("id") not in used_scenarios
    ]
    if not matching:
        matching = [s for s in scenarios if scenario_matches_player(s, stats, life_flags, career_state)]
    if not matching:
        matching = FALLBACK_SCENARIOS
    if not matching:
        return None
    return max(matching, key=lambda s: score_scenario(s, stats, used_scenarios, scenarios, career_state))


# ── Routes ──────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/start", methods=["GET"])
def start_game():
    """Initialize a new life. Returns character state with no scenario — the
    player presses Next Year to begin their first year."""
    initial_stats = {"age": 18, "money": 50, "health": 50, "energy": 50, "happiness": 50, "social": 50}
    initial_career_state = {"career_level": 0, "education_level": 1}
    profile_seed = generate_profile_seed()
    life_flags = []

    return jsonify({
        "stats": initial_stats,
        "career_state": initial_career_state,
        "life_flags": life_flags,
        "profile_seed": profile_seed,
        "player_profile": build_profile_snapshot(profile_seed, initial_stats, initial_career_state),
        "available_actions": get_available_actions(initial_stats, life_flags, initial_career_state),
        "history": [{"age": 18, "event": "You entered adulthood with uncertainty, potential, and a future still unwritten."}],
        "used_scenarios": [],
        "message": "Your life is ready. Press Next Year to see what each year brings."
    })


@app.route("/age", methods=["POST"])
def advance_year():
    """Advance one year. Applies salary and living costs, then surfaces a
    scenario for this year. Actions and choices never call this — only the
    Next Year button does."""
    data = request.get_json(silent=True) or {}

    current_stats = data.get("stats", {"age": 18, "money": 50, "health": 50, "energy": 50, "happiness": 50, "social": 50})
    career_state = data.get("career_state", {"career_level": 0, "education_level": 1})
    history = data.get("history", [])
    used_scenarios = data.get("used_scenarios", [])
    life_flags = data.get("life_flags", [])
    profile_seed = data.get("profile_seed") or generate_profile_seed()

    career_level = career_state.get("career_level", 0)
    updated_stats = build_updated_stats(current_stats, {}, career_level, increment_age=True)

    status, ending_title, ending_message = evaluate_run_status(updated_stats, profile_seed)

    next_scenario = None
    if status == "continue":
        next_scenario = get_next_scenario(updated_stats, used_scenarios, life_flags, career_state)
        if next_scenario:
            used_scenarios.append(next_scenario.get("id"))

    return jsonify({
        "updated_stats": updated_stats,
        "career_state": career_state,
        "available_actions": get_available_actions(updated_stats, life_flags, career_state),
        "life_flags": life_flags,
        "profile_seed": profile_seed,
        "player_profile": build_profile_snapshot(profile_seed, updated_stats, career_state),
        "history": history,
        "used_scenarios": used_scenarios,
        "next_scenario": next_scenario,
        "status": status,
        "ending_title": ending_title,
        "ending_message": ending_message
    })


@app.route("/choice", methods=["POST"])
def make_choice():
    """Resolve a scenario choice. Does NOT advance age — the player must press
    Next Year for that. Career/education changes take effect immediately."""
    data = request.get_json(silent=True) or {}

    current_stats = data.get("stats", {"age": 18, "money": 50, "health": 50, "energy": 50, "happiness": 50, "social": 50})
    career_state = data.get("career_state", {"career_level": 0, "education_level": 1})
    history = data.get("history", [])
    used_scenarios = data.get("used_scenarios", [])
    life_flags = data.get("life_flags", [])
    profile_seed = data.get("profile_seed") or generate_profile_seed()
    choice_effects = data.get("effects", {})
    result_text = data.get("result", "You made a choice and moved forward.")
    set_flags = data.get("set_flags", [])
    clear_flags = data.get("clear_flags", [])

    updated_career_state = build_career_state(career_state, choice_effects)
    updated_stats = build_updated_stats(current_stats, choice_effects, increment_age=False)
    updated_life_flags = apply_flag_changes(life_flags, set_flags, clear_flags)

    history.append({"age": current_stats.get("age", 18), "event": result_text})

    status, ending_title, ending_message = evaluate_run_status(updated_stats, profile_seed)

    return jsonify({
        "result_text": result_text,
        "updated_stats": updated_stats,
        "career_state": updated_career_state,
        "available_actions": get_available_actions(updated_stats, updated_life_flags, updated_career_state),
        "life_flags": updated_life_flags,
        "profile_seed": profile_seed,
        "player_profile": build_profile_snapshot(profile_seed, updated_stats, updated_career_state),
        "history": history,
        "used_scenarios": used_scenarios,
        "status": status,
        "ending_title": ending_title,
        "ending_message": ending_message
    })


@app.route("/action", methods=["POST"])
def take_action():
    """Execute a player action. Does NOT advance age. The current year's
    scenario (if any) stays open until the player responds to it."""
    data = request.get_json(silent=True) or {}

    current_stats = data.get("stats", {"age": 18, "money": 50, "health": 50, "energy": 50, "happiness": 50, "social": 50})
    career_state = data.get("career_state", {"career_level": 0, "education_level": 1})
    history = data.get("history", [])
    used_scenarios = data.get("used_scenarios", [])
    life_flags = data.get("life_flags", [])
    profile_seed = data.get("profile_seed") or generate_profile_seed()
    action_id = data.get("action_id")

    action = find_action(action_id)
    if not action or not action_matches_player(action, current_stats, life_flags, career_state):
        return jsonify({"error": "Action is not available right now."}), 400

    action_effects = action.get("effects", {})
    updated_career_state = build_career_state(career_state, action_effects)
    updated_stats = build_updated_stats(current_stats, action_effects, increment_age=False)
    updated_life_flags = apply_flag_changes(life_flags, action.get("set_flags", []), action.get("clear_flags", []))

    history.append({"age": current_stats.get("age", 18), "event": action.get("result", "You took action.")})

    status, ending_title, ending_message = evaluate_run_status(updated_stats, profile_seed)

    return jsonify({
        "result_text": action.get("result", "You took action."),
        "updated_stats": updated_stats,
        "career_state": updated_career_state,
        "available_actions": get_available_actions(updated_stats, updated_life_flags, updated_career_state),
        "life_flags": updated_life_flags,
        "profile_seed": profile_seed,
        "player_profile": build_profile_snapshot(profile_seed, updated_stats, updated_career_state),
        "history": history,
        "used_scenarios": used_scenarios,
        "status": status,
        "ending_title": ending_title,
        "ending_message": ending_message
    })


if __name__ == "__main__":
    app.run(debug=True)
