# 🎭 Moira AI — Life Simulator

**Moira AI** is a premium, story-driven life simulator where every choice shapes who you become.

Start at 18. Navigate careers, relationships, health, money, and connection. Make decisions that compound over decades. See where your life ends up.

---

## 🎮 How to Run

### Requirements
- Python 3.8+
- pip

### Setup

```bash
# Clone the repo
git clone https://github.com/Laugerr/Moira-AI.git
cd Moira-AI

# Create and activate a virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the server
python app.py
```

Then open your browser and go to: **http://localhost:5000**

---

## ✨ What You Can Do

- 🔁 **Press Next Year** to advance time — your salary ticks, costs rise, and a new life event appears
- 🎯 **Make choices** in response to events — each decision has consequences across your stats
- ⚡ **Take actions** within the year — Work Extra, Socialize, Study, Rest, or Apply for Jobs
- 💍 **Make life decisions** — Start Dating, Propose, Have a Child, or Move City
- 📖 **Watch your timeline** — milestones like marriage and children are marked in gold
- 💀 **Survive to 60** — or burn out trying

---

## 🧠 Core Systems

| System | What it does |
|---|---|
| 🏢 Career | 6 levels from Unemployed to Director — salary ticks every year |
| 🎓 Education | 4 levels that unlock new scenarios and career paths |
| 💍 Relationships | Persistent partner with health that decays yearly — invest or lose them |
| 👶 Family | Have children who create new story events |
| 📊 Needs | Health, Energy, Happiness, Social — let one hit zero and it's over |
| 💰 Money | Salary minus living costs each year — budget matters |
| 🗂️ Flags | Hidden state that chains consequences across multiple years |

---

## 🛠 Tech Stack

- 🐍 Python + Flask
- 🌐 Vanilla HTML / CSS / JavaScript
- 🎨 Glassmorphism UI with animations and transitions
- 📦 JSON-driven scenario system

---

## 📌 Current Version

`v0.4.0` — Relationships & Life Events

> Persistent relationships, Life Decisions panel, milestone timeline, and relationship-aware scenarios are all live.

---

## 🗺️ Roadmap

See the full plan: [Release Plan](./RELEASE_PLAN.md)

| Version | Focus | Status |
|---|---|---|
| v0.1.0 | First working prototype | ✅ Done |
| v0.2.0 | First playable version | ✅ Done |
| v0.3.0 | Career, education, BitLife-style loop | ✅ Done |
| v0.4.0 | Relationships & life decisions | ✅ Done |
| v0.5.0 | Identity & product polish | 🔜 Next |
| v0.6.0 | AI-enhanced narrative | 📅 Planned |
| v1.0.0 | Full release | 📅 Planned |
