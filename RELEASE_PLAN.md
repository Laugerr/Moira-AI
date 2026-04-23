# 🗺️ Moira-AI Release Plan

## ✨ Purpose
This document defines the release roadmap for `Moira-AI` so development stays focused and moves toward a clear product vision.

`Moira-AI` is not intended to be a clone of BitLife. It takes inspiration from the life-simulation loop but evolves into its own premium, story-driven, AI-enhanced life simulator with a distinct tone and identity.

## 🎯 Product Direction
Core inspiration:
- Life progression over time
- Meaningful choices and consequences
- Replayable simulation loops
- Multiple life domains: work, relationships, health, money, and social connection

Moira-AI identity:
- More cinematic and premium than parody-like
- More emotionally aware and story-driven
- Designed to support future AI-generated narrative systems
- Built around the feeling of shaping a life, not only reacting to random prompts

## 🧭 Release Philosophy
The roadmap moves in this order:
1. Prove the core loop works
2. Make the loop fun and replayable
3. Build the BitLife-style game feel — Next Year button, persistent identity, real systems
4. Add relationships and player-initiated life events
5. Polish Moira-AI into something distinctly its own
6. Add AI where it improves the experience
7. Ship a stable, complete v1.0

## 📍 Current State
Completed as of v0.4.0:
- Flask application with `/start`, `/age`, `/choice`, `/action`, `/decision` routes
- **BitLife-style game loop** — Next Year button advances time; actions and choices happen within the current year without aging
- 81 scenarios across 11 life domains + 5 relationship/family scenarios
- 5 player actions with conditional availability (Socialize now boosts relationship health)
- 4 life decisions: Start Dating, Propose, Have a Child, Move City
- Career system: 6 levels (Unemployed → Director) with salary that ticks every year
- Education system: 4 levels (High School → Postgraduate) that unlock new scenarios
- **Persistent relationship state** — partner name, status (single/dating/married/divorced), relationship health (decays yearly), children count
- **Life Decisions panel** — dedicated section for major player-driven choices with prerequisites
- **Milestone timeline** — marriage, children, and major decisions appear as gold-bordered entries
- Relationship-aware scenario selection and scoring
- Relationship and children chips on identity card
- Glassmorphism UI with smooth animations and responsive layout

Known gaps heading into v0.5.0:
- Writing tone is inconsistent across the 81 existing scenarios
- No distinct visual identity beyond the glass UI — colors and typography feel generic
- End-of-life summary is functional but not cinematic
- No decade summaries (your 20s, your 30s, etc.)
- Stat balance has not been audited across all scenarios and actions

---

## 🚦 Release Roadmap

### ✅ v0.1.0 — First Usable Prototype
**Status:** Complete

**Goal:** Establish the first fully working life-simulation prototype.

**Scope:**
- Flask app runs locally
- Player can start a life, receive scenarios, make choices
- Stats and needs update properly
- History and endings work
- Scenario loading works from JSON

**Definition of done:**
- A complete play session can be finished without breaking the game flow

---

### ✅ v0.2.0 — First Truly Playable Version
**Status:** Complete

**Goal:** Make the prototype enjoyable and replayable.

**Scope:**
- More scenarios across multiple life domains
- Better stat balancing
- Cleaner UI and better readability
- State-aware scenario selection and consequence chains
- Player actions system

**Definition of done:**
- Multiple runs feel meaningfully different
- The game is fun enough to replay on purpose

---

### ✅ v0.3.0 — Core Systems Foundation
**Status:** Complete

**Goal:** Give the player a persistent identity and a BitLife-style game feel. Every run now has a career arc, education path, and real financial pressure — not just reactive stat changes.

**Scope:**
- ✅ **Next Year button** as the central time-advance mechanic
- ✅ Actions and choices no longer age the player — only Next Year does
- ✅ Career and education as persistent tracked state
- ✅ Salary ticks every year; living costs scale with age
- ✅ 81 scenarios (up from 36) with career/education conditions
- ✅ Apply for Jobs action for unemployed players
- ✅ Career and education displayed live on the identity card

**Definition of done:**
- ✅ Player has a visible career that changes across the run
- ✅ Two runs with different career choices feel structurally different
- ✅ Money feels like it reflects the player's life situation

---

### ✅ v0.4.0 — Relationships and Life Events
**Status:** Complete

**Goal:** Add the relationship layer and player-initiated decisions. Currently relationships are isolated one-off scenarios with no memory. This version makes them persistent and meaningful.

**Scope:**
- Persistent relationship state
  - Track partner name, relationship status (single, dating, married, divorced), and relationship health
  - Partner persists across turns and can improve or deteriorate based on choices
  - Children tracked as a count with basic age progression
- Player-initiated life decisions panel
  - New dedicated "Life Decisions" section for major player-driven actions
  - Examples: propose, have a child, move city, change career field
  - These decisions have prerequisites and multi-turn consequences
- Life milestone system
  - Major events (graduated, married, promoted, bought a house) get milestone markers in the timeline
  - Distinct visual treatment from regular history entries
- Relationship-aware scenarios
  - Scenarios branch based on relationship status
  - Partner and family create new event domains (conflict, support, milestones)

**Definition of done:**
- ✅ Player has a persistent partner who exists across the whole run
- ✅ Player can initiate major life changes, not only react to them
- ✅ The history timeline reads like a real life story with visible milestones

---

### 🎨 v0.5.0 — Identity and Product Polish
**Status:** Next

**Goal:** Make Moira-AI feel like its own product, not a generic prototype.

**Scope:**
- Stronger visual identity
  - Refined color palette and typography
  - More distinctive UI elements that feel uniquely Moira-AI
- Consistent writing tone
  - Rewrite weak or generic scenario text to match the cinematic, emotionally aware voice
- Immersive history summaries
  - End-of-life summary that reads as a narrative, not a list
  - Decade summaries (your 20s, your 30s, etc.)
- Balance and tuning pass
  - Full stat balance audit across all 81 scenarios and actions
  - Adjusted difficulty curve and pacing

**Definition of done:**
- Moira-AI no longer feels like a generic prototype or simple inspiration project
- The tone and visual identity are consistent from start to ending screen

---

### 🤖 v0.6.0 — AI-Enhanced Version
**Status:** Planned

**Goal:** Add AI where it genuinely improves the experience, not as a gimmick.

**Scope:**
- AI-generated life summaries at game end
- AI-assisted personalized endings that reflect the specific run
- Optional AI-generated scenario variations based on player history
- Narrative responses shaped by who the player became

**Definition of done:**
- AI adds replayability and depth without replacing the core simulation
- AI features are optional enhancements, not load-bearing systems

---

### 🏁 v1.0.0 — Official First Complete Release
**Status:** Planned

**Goal:** Ship the first polished, complete version of Moira-AI.

**Scope:**
- Stable and balanced core systems
- Polished UI/UX
- Strong replayability across career, education, and relationship paths
- Clean project structure
- Deployment-ready release

**Definition of done:**
- The project is solid enough to present as a real product, not just an experiment
- A first-time player can discover the full depth of the game across 2–3 runs
