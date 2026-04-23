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

PARTNER_FIRST_NAMES = [
    "Alex", "Sam", "Jamie", "Chris", "Taylor", "Morgan", "Riley", "Casey",
    "Drew", "Nadia", "Blake", "Remi", "Sasha", "Theo", "Devon", "Maren",
    "Eli", "Camille", "Nico", "Petra"
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
        "effects": {"money": -4, "health": 1, "energy": -2, "happiness": 7, "social": 9,
                    "relationship_health_delta": 8},
        "result": "You reconnect with people around you and feel less alone in the life you are building.",
        "conditions": {
            "money_min": 4
        }
    }
]

LIFE_DECISIONS = [
    {
        "id": "start_dating",
        "title": "Start Dating",
        "subtitle": "Open yourself to connection",
        "description": "Put yourself out there and pursue a meaningful romantic connection.",
        "effects": {"money": -3, "happiness": 12, "social": 8, "energy": -3},
        "relationship_effect": {"status": "dating", "health_set": 60},
        "result": "You meet someone who catches your attention. Things are still new, but there is something real starting here.",
        "milestone": "Started dating {partner_name}",
        "conditions": {
            "relationship_status_not": ["dating", "married"],
            "social_min": 30,
            "age_min": 18
        }
    },
    {
        "id": "propose",
        "title": "Propose",
        "subtitle": "Commit to your future together",
        "description": "Take the step that changes everything. Ask your partner to build a life together.",
        "effects": {"money": -8, "happiness": 18, "social": 5},
        "relationship_effect": {"status": "married"},
        "result": "They said yes. The life you were building just took its most significant turn yet.",
        "milestone": "Married {partner_name}",
        "conditions": {
            "relationship_status_in": ["dating"],
            "relationship_health_min": 50,
            "age_min": 21
        }
    },
    {
        "id": "have_child",
        "title": "Have a Child",
        "subtitle": "Grow your family",
        "description": "Bring a new life into the world. A decision that reshapes everything around it.",
        "effects": {"money": -15, "happiness": 20, "energy": -10, "health": -3},
        "relationship_effect": {"children_delta": 1},
        "result": "A child enters your life and rewrites your priorities, your sense of time, and what it all means.",
        "milestone": "Welcomed a child into the family",
        "conditions": {
            "relationship_status_in": ["married"],
            "children_max": 2,
            "money_min": 25,
            "age_min": 20,
            "age_max": 45
        }
    },
    {
        "id": "move_city",
        "title": "Move City",
        "subtitle": "Start fresh somewhere new",
        "description": "Relocate to a new city. Reset the environment your life is built in.",
        "effects": {"money": -20, "happiness": 8, "social": -8, "energy": -6},
        "result": "You pack up your life and land somewhere new. The unfamiliarity is uncomfortable, but there is energy in the reset.",
        "milestone": "Moved to a new city",
        "conditions": {
            "money_min": 25
        }
    },
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

RELATIONSHIP_SCENARIOS = [
    {
        "id": 9001,
        "domain": "relationship",
        "title": "Rough Patch",
        "text": "You and your partner have been tense for a while. Something small sparked a real argument and now there is distance between you that has to be addressed.",
        "conditions": {
            "relationship_status_in": ["dating", "married"],
            "relationship_health_max": 55
        },
        "choices": [
            {
                "text": "Have the hard conversation",
                "effects": {"energy": -5, "happiness": 6, "social": 3, "relationship_health_delta": 15},
                "result": "It was uncomfortable, but talking through it brought you closer. The distance shrinks."
            },
            {
                "text": "Give it space and time",
                "effects": {"energy": 2, "happiness": -4, "relationship_health_delta": -5},
                "result": "You step back, hoping things will calm down on their own. They mostly do, but the tension lingers."
            },
            {
                "text": "Throw yourself into work to avoid it",
                "effects": {"money": 6, "energy": -6, "happiness": -8, "social": -4, "relationship_health_delta": -14},
                "result": "You bury the conflict under busyness. When you surface, the gap between you has grown."
            }
        ]
    },
    {
        "id": 9002,
        "domain": "relationship",
        "title": "A Quiet Night That Mattered",
        "text": "Nothing important happened — just the two of you, no plans, no pressure. Your partner said something small that stayed with you all week.",
        "conditions": {
            "relationship_status_in": ["dating", "married"],
            "relationship_health_min": 40
        },
        "choices": [
            {
                "text": "Lean into it — be fully present",
                "effects": {"happiness": 10, "social": 5, "energy": 3, "relationship_health_delta": 12},
                "result": "You let yourself be there completely. It becomes one of those evenings you hold onto."
            },
            {
                "text": "Enjoy it but keep some emotional distance",
                "effects": {"happiness": 4, "social": 2, "relationship_health_delta": 3},
                "result": "A pleasant evening. Nothing changes, but nothing breaks either."
            }
        ]
    },
    {
        "id": 9003,
        "domain": "family",
        "title": "Parenting Under Pressure",
        "text": "Your child is going through something difficult at school. They need more from you right now than your schedule usually allows.",
        "conditions": {
            "children_min": 1,
            "relationship_status_in": ["married"]
        },
        "choices": [
            {
                "text": "Rearrange your week to be there for them",
                "effects": {"money": -5, "energy": -8, "happiness": 12, "social": 3, "relationship_health_delta": 6},
                "result": "You show up for your child in a way that matters. They do not forget it, and neither do you."
            },
            {
                "text": "Handle it from a distance — check in but keep working",
                "effects": {"money": 4, "energy": -3, "happiness": -5, "relationship_health_delta": -4},
                "result": "You manage both, but the split attention costs everyone a little. The issue passes, but something does not feel resolved."
            },
            {
                "text": "Ask your partner to take the lead this time",
                "effects": {"energy": 3, "happiness": -2, "relationship_health_delta": -8},
                "result": "Your partner handles it. They do not say anything, but you can feel the uneven weight."
            }
        ]
    },
    {
        "id": 9004,
        "domain": "relationship",
        "title": "The Question of the Future",
        "text": "Your partner brings up something you have both been avoiding — where this relationship is actually going. It is not an ultimatum, but it is not casual either.",
        "conditions": {
            "relationship_status_in": ["dating"],
            "age_min": 24
        },
        "choices": [
            {
                "text": "Be honest — you see a future with them",
                "effects": {"happiness": 10, "social": 5, "relationship_health_delta": 18},
                "result": "Something settles between you. The conversation was overdue, and having it makes everything feel clearer."
            },
            {
                "text": "Deflect — say you need more time",
                "effects": {"happiness": -4, "relationship_health_delta": -10},
                "result": "They accept it, but the conversation hovers. You bought time you are not sure how to use."
            },
            {
                "text": "Be honest — you are not sure where you stand",
                "effects": {"happiness": -8, "social": -4, "relationship_health_delta": -20},
                "result": "The honesty lands hard. Your partner pulls back, and the space between you grows noticeably."
            }
        ]
    },
    {
        "id": 9005,
        "domain": "relationship",
        "title": "Something Changed",
        "text": "You notice something has quietly shifted between you and your partner. Nothing dramatic, but the rhythm you had does not feel the same.",
        "conditions": {
            "relationship_status_in": ["married"],
            "relationship_health_min": 30,
            "relationship_health_max": 65
        },
        "choices": [
            {
                "text": "Name it and start a real conversation",
                "effects": {"energy": -4, "happiness": 7, "relationship_health_delta": 14},
                "result": "You name what you noticed, and they had been feeling it too. Talking about it does not fix everything, but it stops the drift."
            },
            {
                "text": "Plan something meaningful together",
                "effects": {"money": -8, "happiness": 10, "social": 5, "relationship_health_delta": 10},
                "result": "You invest in reconnecting and it works. A shared experience pulls you back toward each other."
            },
            {
                "text": "Assume it will pass on its own",
                "effects": {"relationship_health_delta": -8},
                "result": "You wait. The shift does not reverse. The distance becomes the new normal."
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
                        return valid + RELATIONSHIP_SCENARIOS
    except Exception:
        pass
    return FALLBACK_SCENARIOS + RELATIONSHIP_SCENARIOS


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


def build_updated_relationship_state(rel_state, rel_effect, partner_name=None):
    updated = dict(rel_state)
    if "status" in rel_effect:
        updated["status"] = rel_effect["status"]
    if "health_set" in rel_effect:
        updated["relationship_health"] = rel_effect["health_set"]
    if "health_delta" in rel_effect:
        updated["relationship_health"] = clamp_need(
            updated.get("relationship_health", 0) + rel_effect["health_delta"]
        )
    if "children_delta" in rel_effect:
        updated["children"] = max(0, updated.get("children", 0) + rel_effect["children_delta"])
    if partner_name:
        updated["partner_name"] = partner_name
    return updated


def apply_relationship_health_effect(rel_state, delta):
    """Apply a relationship_health_delta from a choice or action effect."""
    status = rel_state.get("status", "single")
    if status not in ("dating", "married"):
        return rel_state, None
    updated = dict(rel_state)
    new_health = clamp_need(rel_state.get("relationship_health", 60) + delta)
    updated["relationship_health"] = new_health
    breakup_event = None
    if new_health == 0:
        partner = rel_state.get("partner_name", "your partner")
        if status == "dating":
            updated["status"] = "single"
            updated["partner_name"] = None
            breakup_event = f"Things with {partner} fell apart. The relationship ended."
        else:
            updated["status"] = "divorced"
            breakup_event = f"Your marriage with {partner} reached a breaking point. You separated."
    return updated, breakup_event


def apply_relationship_decay(rel_state):
    """Passive yearly relationship health decay. Returns (updated_state, breakup_event_or_None)."""
    status = rel_state.get("status", "single")
    if status not in ("dating", "married"):
        return rel_state, None
    decay = 4 if status == "dating" else 3
    return apply_relationship_health_effect(rel_state, -decay)


def build_profile_snapshot(profile_seed, stats, career_state=None, relationship_state=None):
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

    rel_status = (relationship_state or {}).get("status", "single")
    partner_name = (relationship_state or {}).get("partner_name")
    children = (relationship_state or {}).get("children", 0)
    rel_health = (relationship_state or {}).get("relationship_health", 0)

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
    elif rel_status == "divorced" and happiness <= 55:
        title = "Starting Over"
        summary = "A chapter closed in a way you did not plan for. You are still moving forward, but the weight of it travels with you."
        mood = "Recovering"
    elif rel_status == "married" and rel_health >= 70 and happiness >= 60:
        title = "Grounded Together"
        summary = "Your relationship is one of the strongest pillars in your life right now. It gives everything else more stability."
        mood = "Settled"
    elif career_level >= 4:
        title = "Established Force"
        summary = "Years of building have compounded. You carry real professional weight and the confidence to match."
        mood = "In Command"
    elif career_level == 0 and age >= 24:
        title = "Still Finding Ground"
        summary = "The career piece has not locked in yet, and the uncertainty is adding weight to everything else."
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
        "relationship_status": rel_status,
        "partner_name": partner_name,
        "children": children,
        "relationship_health": rel_health,
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


def decision_matches_player(decision, stats, life_flags=None, career_state=None, relationship_state=None):
    return scenario_matches_player(
        {"conditions": decision.get("conditions", {})},
        stats, life_flags, career_state, relationship_state
    )


def get_available_decisions(stats, life_flags=None, career_state=None, relationship_state=None):
    return [
        {
            "id": d["id"],
            "title": d["title"],
            "subtitle": d["subtitle"],
            "description": d["description"],
        }
        for d in LIFE_DECISIONS
        if decision_matches_player(d, stats, life_flags, career_state, relationship_state)
    ]


def find_action(action_id):
    for action in PLAYER_ACTIONS:
        if action["id"] == action_id:
            return action
    return None


def find_decision(decision_id):
    for decision in LIFE_DECISIONS:
        if decision["id"] == decision_id:
            return decision
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


def build_ending(status, stats, profile_seed, career_state=None, relationship_state=None):
    strongest, weakest = get_life_strengths(stats)
    dream = profile_seed.get("dream", "build a meaningful life")
    career_level = (career_state or {}).get("career_level", 0)
    job_title = CAREER_LEVELS.get(career_level, CAREER_LEVELS[0])["title"]
    rel_status = (relationship_state or {}).get("status", "single")
    partner_name = (relationship_state or {}).get("partner_name")
    children = (relationship_state or {}).get("children", 0)

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

    relationship_line = ""
    if rel_status == "married" and partner_name:
        relationship_line = f" You built your life alongside {partner_name}."
        if children > 0:
            relationship_line += f" Together you raised {children} {'child' if children == 1 else 'children'}."
    elif rel_status == "divorced":
        relationship_line = " A marriage ended along the way — one of the harder chapters you had to move through."
    elif children > 0:
        relationship_line = f" You raised {children} {'child' if children == 1 else 'children'} and carried that weight with you every year."

    return {
        "title": completion_titles.get(strongest, "Journey Complete"),
        "message": (
            f"You reached later adulthood still chasing your dream to {dream}."
            f"{career_line}{relationship_line} "
            f"{strongest_lines[strongest]} {weakest_lines[weakest]}"
        )
    }


def scenario_matches_player(scenario, stats, life_flags=None, career_state=None, relationship_state=None):
    conditions = scenario.get("conditions", {})
    active_flags = set(life_flags or [])
    career_level = (career_state or {}).get("career_level", 0)
    education_level = (career_state or {}).get("education_level", 1)
    rel_status = (relationship_state or {}).get("status", "single")
    rel_health = (relationship_state or {}).get("relationship_health", 0)
    children = (relationship_state or {}).get("children", 0)

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
        "relationship_health_min": lambda v: rel_health >= v,
        "relationship_health_max": lambda v: rel_health <= v,
        "children_min": lambda v: children >= v,
        "children_max": lambda v: children <= v,
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
        if key == "relationship_status_in":
            if rel_status not in value:
                return False
            continue
        if key == "relationship_status_not":
            if rel_status in value:
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
        return {"work": 3, "family": 3, "housing": 3, "money": 2, "health": 2, "social": 1, "relationship": 2}
    return {"health": 4, "family": 3, "growth": 3, "life": 3, "money": 2, "social": 2, "relationship": 2}


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


def score_scenario(scenario, stats, used_scenarios, scenarios, career_state=None, relationship_state=None):
    domain = scenario.get("domain", "general")
    age = stats.get("age", 18)
    money = stats.get("money", 50)
    health = stats.get("health", 50)
    energy = stats.get("energy", 50)
    happiness = stats.get("happiness", 50)
    social = stats.get("social", 50)
    career_level = (career_state or {}).get("career_level", 0)
    education_level = (career_state or {}).get("education_level", 1)
    rel_status = (relationship_state or {}).get("status", "single")
    rel_health = (relationship_state or {}).get("relationship_health", 60)
    children = (relationship_state or {}).get("children", 0)

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

    # Relationship scoring
    if rel_status in ("dating", "married") and domain == "relationship": score += 2
    if rel_status in ("dating", "married") and rel_health <= 40 and domain == "relationship": score += 4
    if rel_status == "single" and age >= 25 and social >= 45 and domain == "relationship": score += 1
    if children >= 1 and domain == "family": score += 4

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


def get_next_scenario(stats, used_scenarios, life_flags=None, career_state=None, relationship_state=None):
    scenarios = load_scenarios()
    matching = [
        s for s in scenarios
        if scenario_matches_player(s, stats, life_flags, career_state, relationship_state)
        and s.get("id") not in used_scenarios
    ]
    if not matching:
        matching = [
            s for s in scenarios
            if scenario_matches_player(s, stats, life_flags, career_state, relationship_state)
        ]
    if not matching:
        matching = FALLBACK_SCENARIOS
    if not matching:
        return None
    return max(matching, key=lambda s: score_scenario(s, stats, used_scenarios, scenarios, career_state, relationship_state))


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
    initial_relationship_state = {"status": "single", "partner_name": None, "relationship_health": 0, "children": 0}
    profile_seed = generate_profile_seed()
    life_flags = []

    return jsonify({
        "stats": initial_stats,
        "career_state": initial_career_state,
        "relationship_state": initial_relationship_state,
        "life_flags": life_flags,
        "profile_seed": profile_seed,
        "player_profile": build_profile_snapshot(profile_seed, initial_stats, initial_career_state, initial_relationship_state),
        "available_actions": get_available_actions(initial_stats, life_flags, initial_career_state),
        "available_decisions": get_available_decisions(initial_stats, life_flags, initial_career_state, initial_relationship_state),
        "history": [{"age": 18, "event": "You entered adulthood with uncertainty, potential, and a future still unwritten.", "type": "event"}],
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
    relationship_state = data.get("relationship_state", {"status": "single", "partner_name": None, "relationship_health": 0, "children": 0})
    history = data.get("history", [])
    used_scenarios = data.get("used_scenarios", [])
    life_flags = data.get("life_flags", [])
    profile_seed = data.get("profile_seed") or generate_profile_seed()

    career_level = career_state.get("career_level", 0)
    updated_stats = build_updated_stats(current_stats, {}, career_level, increment_age=True)

    # Apply passive relationship decay and check for breakup
    updated_relationship_state, breakup_event = apply_relationship_decay(relationship_state)
    if breakup_event:
        history.append({"age": updated_stats["age"], "event": breakup_event, "type": "milestone"})

    status, ending_title, ending_message = evaluate_run_status(updated_stats, profile_seed)

    next_scenario = None
    if status == "continue":
        next_scenario = get_next_scenario(updated_stats, used_scenarios, life_flags, career_state, updated_relationship_state)
        if next_scenario:
            used_scenarios.append(next_scenario.get("id"))

    return jsonify({
        "updated_stats": updated_stats,
        "career_state": career_state,
        "relationship_state": updated_relationship_state,
        "available_actions": get_available_actions(updated_stats, life_flags, career_state),
        "available_decisions": get_available_decisions(updated_stats, life_flags, career_state, updated_relationship_state),
        "life_flags": life_flags,
        "profile_seed": profile_seed,
        "player_profile": build_profile_snapshot(profile_seed, updated_stats, career_state, updated_relationship_state),
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
    relationship_state = data.get("relationship_state", {"status": "single", "partner_name": None, "relationship_health": 0, "children": 0})
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

    # Apply relationship health delta from choice effects if present
    updated_relationship_state = relationship_state
    breakup_event = None
    rel_delta = choice_effects.get("relationship_health_delta", 0)
    if rel_delta:
        updated_relationship_state, breakup_event = apply_relationship_health_effect(relationship_state, rel_delta)

    history.append({"age": current_stats.get("age", 18), "event": result_text, "type": "event"})
    if breakup_event:
        history.append({"age": current_stats.get("age", 18), "event": breakup_event, "type": "milestone"})

    status, ending_title, ending_message = evaluate_run_status(updated_stats, profile_seed)

    return jsonify({
        "result_text": result_text,
        "updated_stats": updated_stats,
        "career_state": updated_career_state,
        "relationship_state": updated_relationship_state,
        "available_actions": get_available_actions(updated_stats, updated_life_flags, updated_career_state),
        "available_decisions": get_available_decisions(updated_stats, updated_life_flags, updated_career_state, updated_relationship_state),
        "life_flags": updated_life_flags,
        "profile_seed": profile_seed,
        "player_profile": build_profile_snapshot(profile_seed, updated_stats, updated_career_state, updated_relationship_state),
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
    relationship_state = data.get("relationship_state", {"status": "single", "partner_name": None, "relationship_health": 0, "children": 0})
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

    # Apply relationship health delta from action effects if present
    updated_relationship_state = relationship_state
    breakup_event = None
    rel_delta = action_effects.get("relationship_health_delta", 0)
    if rel_delta:
        updated_relationship_state, breakup_event = apply_relationship_health_effect(relationship_state, rel_delta)

    history.append({"age": current_stats.get("age", 18), "event": action.get("result", "You took action."), "type": "event"})
    if breakup_event:
        history.append({"age": current_stats.get("age", 18), "event": breakup_event, "type": "milestone"})

    status, ending_title, ending_message = evaluate_run_status(updated_stats, profile_seed)

    return jsonify({
        "result_text": action.get("result", "You took action."),
        "updated_stats": updated_stats,
        "career_state": updated_career_state,
        "relationship_state": updated_relationship_state,
        "available_actions": get_available_actions(updated_stats, updated_life_flags, updated_career_state),
        "available_decisions": get_available_decisions(updated_stats, updated_life_flags, updated_career_state, updated_relationship_state),
        "life_flags": updated_life_flags,
        "profile_seed": profile_seed,
        "player_profile": build_profile_snapshot(profile_seed, updated_stats, updated_career_state, updated_relationship_state),
        "history": history,
        "used_scenarios": used_scenarios,
        "status": status,
        "ending_title": ending_title,
        "ending_message": ending_message
    })


@app.route("/decision", methods=["POST"])
def take_decision():
    """Execute a major life decision. Does NOT advance age. Updates relationship
    state and adds a milestone to the timeline."""
    data = request.get_json(silent=True) or {}

    current_stats = data.get("stats", {"age": 18, "money": 50, "health": 50, "energy": 50, "happiness": 50, "social": 50})
    career_state = data.get("career_state", {"career_level": 0, "education_level": 1})
    relationship_state = data.get("relationship_state", {"status": "single", "partner_name": None, "relationship_health": 0, "children": 0})
    history = data.get("history", [])
    used_scenarios = data.get("used_scenarios", [])
    life_flags = data.get("life_flags", [])
    profile_seed = data.get("profile_seed") or generate_profile_seed()
    decision_id = data.get("decision_id")

    decision = find_decision(decision_id)
    if not decision or not decision_matches_player(decision, current_stats, life_flags, career_state, relationship_state):
        return jsonify({"error": "Decision is not available right now."}), 400

    decision_effects = decision.get("effects", {})
    updated_stats = build_updated_stats(current_stats, decision_effects, increment_age=False)

    # Handle relationship effects
    updated_relationship_state = dict(relationship_state)
    rel_effect = decision.get("relationship_effect", {})
    updated_profile_seed = dict(profile_seed)

    new_partner_name = None
    if rel_effect.get("status") == "dating" and relationship_state.get("status") != "dating":
        new_partner_name = f"{random.choice(PARTNER_FIRST_NAMES)} {random.choice(LAST_NAMES)}"

    if rel_effect:
        updated_relationship_state = build_updated_relationship_state(
            relationship_state, rel_effect, new_partner_name
        )

    # Move city updates hometown
    if decision_id == "move_city":
        current_hometown = profile_seed.get("hometown", "")
        new_cities = [c for c in HOMETOWNS if c != current_hometown]
        if new_cities:
            updated_profile_seed["hometown"] = random.choice(new_cities)

    # Build milestone text
    milestone_text = decision.get("milestone", "")
    partner_name = updated_relationship_state.get("partner_name") or new_partner_name
    if milestone_text and partner_name:
        milestone_text = milestone_text.replace("{partner_name}", partner_name)

    result_text = decision.get("result", "You made a major life decision.")

    # Add milestone to history
    history.append({
        "age": current_stats.get("age", 18),
        "event": milestone_text if milestone_text else result_text,
        "type": "milestone"
    })

    status, ending_title, ending_message = evaluate_run_status(updated_stats, updated_profile_seed)

    return jsonify({
        "result_text": result_text,
        "updated_stats": updated_stats,
        "career_state": career_state,
        "relationship_state": updated_relationship_state,
        "available_actions": get_available_actions(updated_stats, life_flags, career_state),
        "available_decisions": get_available_decisions(updated_stats, life_flags, career_state, updated_relationship_state),
        "life_flags": life_flags,
        "profile_seed": updated_profile_seed,
        "player_profile": build_profile_snapshot(updated_profile_seed, updated_stats, career_state, updated_relationship_state),
        "history": history,
        "used_scenarios": used_scenarios,
        "status": status,
        "ending_title": ending_title,
        "ending_message": ending_message
    })


if __name__ == "__main__":
    app.run(debug=True)
