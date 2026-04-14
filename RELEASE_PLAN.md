# Moira-AI Release Plan

## Purpose
This document defines the release roadmap for `Moira-AI` so development stays focused and moves toward a clear product vision.

`Moira-AI` is not intended to be a clone of BitLife. It takes inspiration from the life-simulation loop but evolves into its own premium, story-driven, AI-enhanced life simulator with a distinct tone and identity.

## Product Direction
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

## Release Philosophy
The roadmap moves in this order:
1. Prove the core loop works
2. Make the loop fun and replayable
3. Build persistent life systems that give the player an identity
4. Add relationships and player-initiated life events
5. Polish Moira-AI into something distinctly its own
6. Add AI where it improves the experience
7. Ship a stable, complete v1.0

## Current State
Completed as of v0.2.0:
- Flask application with start, choice, and action routes
- 36 scenarios across 11 life domains
- 4 player actions with conditional availability
- 5 life need stats with tracking and visualization
- Flag-based consequence chains
- State-aware scenario selection with life stage biasing
- Dynamic character profile generation
- History timeline and ending system
- Glassmorphism UI with smooth animations

Known gaps heading into v0.3.0:
- No persistent career or education state (flags track events, not identity)
- No recurring income or living cost mechanics (money is purely event-driven)
- 36 scenarios is too few for meaningful replayability across multiple runs
- No relationship persistence (partner, family state across turns)
- No player-initiated major life decisions (only reactive choices + 4 passive actions)

---

## Release Roadmap

### v0.1.0 - First Usable Prototype
Status: Complete

Goal: Establish the first fully working life-simulation prototype.

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

---

### v0.2.0 - First Truly Playable Version
Status: Complete

Goal: Make the prototype enjoyable and replayable.

Scope:
- More scenarios across multiple life domains
- Better balancing for money, health, energy, happiness, and social
- Cleaner UI and better readability
- Improved life-profile feedback
- Better ending variety
- State-aware scenario selection
- First consequence chains and follow-up events
- Player actions system

Definition of done:
- Multiple runs feel meaningfully different
- The game is fun enough to replay on purpose

---

### v0.3.0 - Core Systems Foundation
Status: Next

Goal: Give the player a persistent identity that builds and changes across the run. Right now every run has the same skeleton — stats go up and down but nothing about who the player IS changes. This version fixes that.

Scope:
- Career and education tracked as persistent game state
  - Store `education_level` (none, diploma, degree, postgrad) and `career_level` (0-5) in session
  - Display job title and education level on the identity card
  - Scenarios that involve jobs or education actually change these values
- Recurring income mechanic
  - Each age tick adds salary to money based on career level
  - Basic living costs deducted each turn (scales with age/lifestyle)
  - Makes money feel like a real resource, not just a score
- Scenario content expansion
  - Expand from 36 to 80+ scenarios
  - Add new scenarios that reference and react to career/education state
  - More variety in work, money, and growth domains
- Career-gated scenario logic
  - Scenarios can require or exclude certain career levels and education levels
  - Unlocks new content as the player builds their life

Definition of done:
- Player has a visible job title and education level that changes across the run
- Two runs with different career choices feel structurally different, not just narratively different
- Money feels like it reflects the player's life situation, not random noise

---

### v0.4.0 - Relationships and Life Events
Status: Planned

Goal: Add the relationship layer and player-initiated decisions that BitLife-style games are built on. Currently relationships are isolated one-off scenarios with no memory. This version makes them persistent and meaningful.

Scope:
- Persistent relationship state
  - Track partner name, relationship status (single, dating, married, divorced), and relationship health
  - Partner persists across turns and can improve or deteriorate based on choices
  - Children tracked as a count with basic age progression
- Player-initiated life decisions
  - New "Life Decisions" panel for major player-driven actions
  - Examples: apply for a new job, pursue further education, propose, have a child, move city
  - These decisions have prerequisites and multi-turn consequences
- Life milestone system
  - Major events (graduated, married, promoted, bought a house) appear as milestone markers in the timeline
  - Separate visual treatment from regular history entries
- Relationship-aware scenarios
  - Scenarios branch based on relationship status
  - Partner and family create new event domains (conflict, support, milestones)

Definition of done:
- Player has a persistent partner who exists across the whole run
- Player can initiate major life changes, not only react to them
- The history timeline reads like a real life story with visible milestones

---

### v0.5.0 - Identity and Product Polish
Status: Planned

Goal: Make Moira-AI feel like its own product, not a generic prototype. The game should have a recognizable tone, voice, and visual identity by this point.

Scope:
- Stronger visual identity
  - Refined color palette and typography
  - More distinctive UI elements that feel uniquely Moira-AI
- Consistent writing tone across all scenarios and endings
  - Rewrite weak or generic scenario text to match the cinematic, emotionally aware voice
- Immersive history summaries
  - End-of-life summary that reads as a narrative, not a list
  - Decade summaries (your 20s, your 30s, etc.)
- Balance and tuning pass
  - Full stat balance audit across all scenarios and actions
  - Adjust difficulty curve and pacing

Definition of done:
- Moira-AI no longer feels like a generic prototype or simple inspiration project
- The tone and visual identity are consistent from start to ending screen

---

### v0.6.0 - AI-Enhanced Version
Status: Planned

Goal: Add AI where it genuinely improves the experience, not as a gimmick.

Scope:
- AI-generated life summaries at game end
- AI-assisted personalized endings that reflect the specific run
- Optional AI-generated scenario variations based on player history
- Narrative responses shaped by who the player became

Definition of done:
- AI adds replayability and depth without replacing the core simulation
- AI features are optional enhancements, not load-bearing systems

---

### v1.0.0 - Official First Complete Release
Status: Planned

Goal: Ship the first polished, complete version of Moira-AI.

Scope:
- Stable and balanced core systems
- Polished UI/UX
- Strong replayability across career, education, and relationship paths
- Clean project structure
- Deployment-ready release

Definition of done:
- The project is solid enough to present as a real product, not just an experiment
- A first-time player can discover the full depth of the game across 2-3 runs
