# 🗺️ Moira-AI Release Plan

## ✨ Purpose
This document defines the release roadmap for `Moira-AI` so development stays focused and moves toward a clear product vision.

`Moira-AI` is not intended to be a clone of BitLife. It may take inspiration from the life-simulation loop, but it should evolve into its own premium, story-driven, AI-enhanced life simulator with a distinct tone and identity.

## 🎯 Product Direction
Core inspiration:
- Life progression over time
- Meaningful choices and consequences
- Replayable simulation loops
- Multiple life domains such as work, relationships, health, money, and social connection

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
- Needs-based stats
- History timeline
- Connected scenario chains
- State-aware selection
- UI clarity improvements

This means `v0.1.0` and `v0.2.0` are complete, and the project is ready to move into deeper systems work.

## 🚦 Release Roadmap

### ✅ v0.1.0 - First Usable Prototype
Goal:
Establish the first fully working life-simulation prototype.

Current status:
- Complete

Scope:
- Flask app runs locally
- Player can start a life
- Player receives scenarios and makes choices
- Stats and needs update properly
- History updates properly
- Endings trigger correctly
- Scenario loading works from JSON

Definition of done:
- A complete play session can be finished without breaking the game flow
- Core screens work from start to ending
- No critical logic bugs in start, choice, or ending flow

### ✅ v0.2.0 - First Truly Playable Version
Goal:
Make the prototype enjoyable and replayable.

Current status:
- Complete

Scope:
- More scenarios across multiple life domains
- Better balancing for money, health, energy, happiness, and social
- Cleaner UI and better readability
- Improved life-profile feedback
- Better ending variety
- State-aware scenario selection
- First consequence chains and follow-up events

Definition of done:
- Multiple runs feel meaningfully different
- The game is fun enough to replay on purpose

### 🧱 v0.3.0 - First Systems-Heavy Version
Goal:
Expand from a scenario prototype into a deeper life simulator.

Scope:
- Player actions in addition to random scenarios
- Education progression
- Career progression
- Relationship systems
- Health and burnout pressure
- More state-aware scenario logic

Definition of done:
- The player feels they are building a life, not only reacting to events

### 🎨 v0.4.0 - Identity and Product Polish
Goal:
Make Moira-AI feel unique and recognizable.

Scope:
- Stronger visual identity
- Better writing tone and world feel
- More immersive history and summaries
- Distinct product personality around fate, life, ambition, and consequence

Definition of done:
- Moira-AI no longer feels like a generic prototype or simple inspiration project

### 🤖 v0.5.0 - AI-Enhanced Version
Goal:
Add AI where it genuinely improves the experience.

Scope:
- AI-generated life summaries
- AI-assisted personalized endings
- Optional AI-generated scenario variations
- Narrative responses shaped by player history

Definition of done:
- AI adds replayability and depth without replacing the core simulation

### 🏁 v1.0.0 - Official First Complete Release
Goal:
Ship the first polished, complete version of Moira-AI.

Scope:
- Stable and balanced core systems
- Polished UI/UX
- Strong replayability
- Clean project structure
- Deployment-ready release

Definition of done:
- The project is solid enough to present as a real product, not just an experiment
