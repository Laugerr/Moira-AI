# 🗺 Moira-AI Release Plan

## ✨ Purpose
This document defines the release roadmap for `Moira-AI` so development stays focused and moves toward a clear product vision.

`Moira-AI` is not intended to be a clone of BitLife. It may take inspiration from the life-simulation loop, but it should evolve into its own premium, story-driven, AI-enhanced life simulator with a distinct tone and identity.

## 🎯 Product Direction
Core inspiration:
- Life progression over time
- Meaningful choices and consequences
- Replayable simulation loops
- Multiple life domains such as work, relationships, health, and money

Moira-AI identity:
- More cinematic and premium than parody-like
- More emotionally aware and story-driven
- Designed to support future AI-generated narrative systems
- Built around the feeling of shaping a life, not only reacting to random prompts

## 🧭 Release Philosophy
The roadmap should move in this order:
1. Prove the core loop works
2. Make the loop fun and replayable
3. Add real life-simulation systems
4. Make the game feel uniquely like Moira-AI
5. Add AI where it improves the experience
6. Polish into a stable version `1.0`

## 📍 Current State
Current repo already includes:
- Flask application setup
- Start game flow
- Scenario and choice system
- Basic stat system
- History timeline
- Basic endings
- JSON-based scenario loading with fallback scenarios

This means the project is already beyond idea stage and is close to `v0.1.0`.

## 🚦 Release Roadmap

### 🛠 v0.1.0 - Foundation Prototype
Goal:
Establish the first fully working life-simulation prototype.

Scope:
- Flask app runs locally
- Player can start a life
- Player receives scenarios and makes choices
- Stats update properly
- History updates properly
- Endings trigger correctly
- Scenario loading works from JSON

Definition of done:
- A complete play session can be finished without breaking the game flow
- Core screens work from start to ending
- No critical logic bugs in start, choice, or ending flow

Status:
- Mostly achieved

### 🎮 v0.2.0 - Playable Life Loop
Goal:
Turn the prototype into a replayable, enjoyable game loop.

Scope:
- Fix encoding and text-quality issues
- Expand scenario count significantly
- Add scenario categories:
  - education
  - work
  - relationships
  - health
  - money
  - risk
- Improve balancing of existing stats
- Improve endings so different life outcomes feel distinct
- Improve profile identity and storytelling tone
- Polish UI enough to feel cohesive and readable

Definition of done:
- Multiple playthroughs feel different from each other
- Players can recognize basic life paths through the game
- Core simulation feels stable and worth replaying

Priority:
- Highest immediate target

### 🧠 v0.3.0 - Systems Expansion
Goal:
Move from a scenario prototype into a true life simulator.

Scope:
- Introduce player-driven actions in addition to random scenarios
- Add yearly action menu
- Add early domain systems:
  - education progression
  - work and career progression
  - relationships
  - health and burnout
  - money management
- Add state-aware event conditions
- Add follow-up event chains and longer consequence arcs

Definition of done:
- The player is building a life, not only reacting to events
- Different strategies lead to visibly different life outcomes
- The game has multiple interconnected systems

### 🌌 v0.4.0 - Moira Identity Layer
Goal:
Make the experience clearly feel like `Moira-AI`, not just “life sim inspired by BitLife.”

Scope:
- Stronger narrative voice and writing tone
- Better visual identity and premium UI direction
- More meaningful profile summaries
- Life archetypes and personality-driven outcomes
- Stronger history/timeline presentation
- Distinct world tone around fate, life, ambition, risk, and consequence

Definition of done:
- The project has a recognizable identity beyond its genre inspiration
- A player can describe what makes `Moira-AI` feel different

### 🤖 v0.5.0 - AI-Assisted Features
Goal:
Introduce AI as a meaningful enhancement to the game experience.

Scope:
- AI-generated end-of-life summaries
- AI-generated yearly reflections
- AI-personalized scenario variations
- Context-aware narrative responses based on player history
- Optional “Moira reflection” moments after major decisions

Definition of done:
- AI improves immersion, replayability, or personalization
- AI does not replace the core game structure
- The game still works well without depending on fragile AI flow

### 🏆 v1.0.0 - Premium Core Experience
Goal:
Ship the first complete and stable version of `Moira-AI`.

Scope:
- Balanced core life simulation
- Clear and polished UI/UX
- Strong replay value
- Stable code structure
- Better content organization beyond a single large app file
- Save/load support if feasible
- Deployment-ready app state
- Finalized identity for presentation and public sharing

Definition of done:
- The game feels like a real product, not a prototype
- The core loop is polished, stable, and replayable
- The codebase is structured enough to scale post-1.0

## 🧱 Recommended Build Order
The next practical order of work should be:
1. Finish `v0.1.0`
2. Prioritize `v0.2.0`
3. Use `v0.3.0` to add deeper systems
4. Use `v0.4.0` to define identity
5. Add AI in `v0.5.0`
6. Polish and stabilize for `v1.0.0`

## 🔥 Recommended Immediate Milestone
The next milestone should be:

`v0.2.0 - Playable Life Loop`

Reason:
- The current project already has the prototype foundation
- The game needs stronger structure before deeper systems or AI
- This release will reduce drift and create a clear base for future expansion

## ✅ v0.2.0 Proposed Task Breakdown
Recommended work items:
- Clean up text encoding issues in UI and scenario content
- Audit and refine the current stats model
- Expand scenario library with better category coverage
- Improve scenario conditions so events feel more relevant to the player state
- Improve endings and life-outcome variety
- Refine the current UI for readability and consistency
- Prepare code for modular growth

## 🧪 Post-v0.2.0 Technical Direction
Current structure is acceptable for prototyping, but future releases should move toward:

- `app.py` for routes and app bootstrapping
- `app/game_state.py`
- `app/event_engine.py`
- `app/profile.py`
- `app/actions.py`
- `data/events/*.json`
- `data/actions.json`

This should begin gradually after `v0.2.0` once systems become more complex.

## 📝 Notes
- Avoid expanding too many systems before the current loop is fun
- Avoid adding AI before the game has a stable base design
- Avoid chasing UI redesigns before the gameplay direction is clearer
- Focus on milestone-based progress, not isolated feature experiments

## 🌟 Summary
Moira-AI roadmap:
- `v0.1.0` Foundation Prototype
- `v0.2.0` Playable Life Loop
- `v0.3.0` Systems Expansion
- `v0.4.0` Moira Identity Layer
- `v0.5.0` AI-Assisted Features
- `v1.0.0` Premium Core Experience

Immediate target:
- Build and complete `v0.2.0`
