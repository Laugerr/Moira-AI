// ── State ────────────────────────────────────────────────────────────────────

let currentStats = { age: 18, money: 50, health: 50, energy: 50, happiness: 50, social: 50 };
let careerState = { career_level: 0, education_level: 1 };
let currentHistory = [];
let usedScenarios = [];
let currentScenario = null;
let profileSeed = null;
let lifeFlags = [];
let lastStatsSnapshot = null;
let hasActiveScenario = false;  // true while this year's event is unanswered

// ── DOM refs ─────────────────────────────────────────────────────────────────

const startBtn        = document.getElementById("start-btn");
const restartBtn      = document.getElementById("restart-btn");
const ageBtn          = document.getElementById("age-btn");
const gameSection     = document.getElementById("game-section");
const gameMessage     = document.getElementById("game-message");
const scenarioTitle   = document.getElementById("scenario-title");
const scenarioText    = document.getElementById("scenario-text");
const choicesContainer  = document.getElementById("choices-container");
const actionsContainer  = document.getElementById("actions-container");
const resultText      = document.getElementById("result-text");
const gameOverCard    = document.getElementById("game-over-card");
const endingMessage   = document.getElementById("ending-message");
const endingTitle     = document.getElementById("ending-title");
const endingMeta      = document.getElementById("ending-meta");
const historyList     = document.getElementById("history-list");

const ageStat         = document.getElementById("age-stat");
const moneyStat       = document.getElementById("money-stat");
const healthStat      = document.getElementById("health-stat");
const energyStat      = document.getElementById("energy-stat");
const happinessStat   = document.getElementById("happiness-stat");
const socialStat      = document.getElementById("social-stat");
const healthState     = document.getElementById("health-state");
const energyState     = document.getElementById("energy-state");
const happinessState  = document.getElementById("happiness-state");
const socialState     = document.getElementById("social-state");
const historyCount    = document.getElementById("history-count");
const needsSummary    = document.getElementById("needs-summary");

const healthBar       = document.getElementById("health-bar");
const energyBar       = document.getElementById("energy-bar");
const happinessBar    = document.getElementById("happiness-bar");
const socialBar       = document.getElementById("social-bar");

const profileName     = document.getElementById("profile-name");
const profileSubtitle = document.getElementById("profile-subtitle");
const profileMood     = document.getElementById("profile-mood");
const profileStage    = document.getElementById("profile-stage");
const profileTrait    = document.getElementById("profile-trait");
const profileOrigin   = document.getElementById("profile-origin");
const profileSummary  = document.getElementById("profile-summary");
const profileAgeBadge = document.getElementById("profile-age-badge");
const profileJob      = document.getElementById("profile-job");
const profileEducation = document.getElementById("profile-education");
const salaryStat      = document.getElementById("salary-stat");

const animatedPanels  = document.querySelectorAll(
  ".identity-card, .story-panel, .actions-card, .status-card, .result-card, .history-card"
);

// ── Age button state ──────────────────────────────────────────────────────────

function setAgeBtnBlocked(reason) {
  ageBtn.disabled = true;
  ageBtn.classList.add("age-btn--blocked");
  ageBtn.classList.remove("age-btn--ready");
  ageBtn.querySelector(".age-btn-label").textContent = reason || "Next Year";
}

function setAgeBtnReady() {
  ageBtn.disabled = false;
  ageBtn.classList.add("age-btn--ready");
  ageBtn.classList.remove("age-btn--blocked");
  ageBtn.querySelector(".age-btn-label").textContent = "Next Year";
}

function setAgeBtnLoading() {
  ageBtn.disabled = true;
  ageBtn.classList.remove("age-btn--ready", "age-btn--blocked");
  ageBtn.querySelector(".age-btn-label").textContent = "Aging...";
}

// ── Need helpers ──────────────────────────────────────────────────────────────

function getNeedState(value) {
  if (value <= 20) return { label: "Critical", tone: "critical" };
  if (value <= 40) return { label: "Low", tone: "low" };
  if (value >= 75) return { label: "Strong", tone: "strong" };
  return { label: "Stable", tone: "stable" };
}

function applyNeedState(element, value) {
  const state = getNeedState(value);
  element.textContent = state.label;
  element.className = `stat-state ${state.tone}`;
}

function getNeedRanking(stats) {
  return [
    ["Health", stats.health],
    ["Energy", stats.energy],
    ["Happiness", stats.happiness],
    ["Social", stats.social]
  ].sort((a, b) => a[1] - b[1]);
}

// ── Animation helpers ─────────────────────────────────────────────────────────

function animatePanelSwap(element) {
  if (!element) return;
  element.classList.remove("content-refresh");
  void element.offsetWidth;
  element.classList.add("content-refresh");
}

function triggerValuePulse(element, direction) {
  if (!element || !direction) return;
  const className = direction > 0 ? "value-up" : "value-down";
  element.classList.remove("value-up", "value-down");
  void element.offsetWidth;
  element.classList.add(className);
}

function animateStatChanges(previousStats, nextStats) {
  if (!previousStats) return;
  [["money", moneyStat], ["health", healthStat], ["energy", energyStat],
   ["happiness", happinessStat], ["social", socialStat]].forEach(([key, el]) => {
    const before = previousStats[key];
    const after = nextStats[key];
    if (typeof before === "number" && typeof after === "number" && before !== after) {
      triggerValuePulse(el, after - before);
    }
  });
}

function animateDashboardEntrance() {
  animatedPanels.forEach((panel, index) => {
    panel.style.setProperty("--panel-delay", `${index * 80}ms`);
    panel.classList.remove("panel-enter");
    void panel.offsetWidth;
    panel.classList.add("panel-enter");
  });
}

// ── Render helpers ────────────────────────────────────────────────────────────

function updateStatsUI(stats) {
  animateStatChanges(lastStatsSnapshot, stats);

  ageStat.textContent = stats.age;
  moneyStat.textContent = `$${Number(stats.money).toLocaleString()}`;
  healthStat.textContent = `${stats.health}%`;
  energyStat.textContent = `${stats.energy}%`;
  happinessStat.textContent = `${stats.happiness}%`;
  socialStat.textContent = `${stats.social}%`;

  healthBar.style.width = `${stats.health}%`;
  energyBar.style.width = `${stats.energy}%`;
  happinessBar.style.width = `${stats.happiness}%`;
  socialBar.style.width = `${stats.social}%`;

  applyNeedState(healthState, stats.health);
  applyNeedState(energyState, stats.energy);
  applyNeedState(happinessState, stats.happiness);
  applyNeedState(socialState, stats.social);

  const [lowestNeed] = getNeedRanking(stats);
  const highestNeed = getNeedRanking(stats).at(-1);

  if (lowestNeed[1] <= 20) {
    needsSummary.textContent = `${lowestNeed[0]} is in critical condition. Stabilize it before the run starts collapsing.`;
  } else if (lowestNeed[1] <= 40) {
    needsSummary.textContent = `${lowestNeed[0]} is your weakest need right now. ${highestNeed[0]} is carrying the most stability.`;
  } else if (highestNeed[1] >= 75) {
    needsSummary.textContent = `${highestNeed[0]} is a major strength right now. Keep the rest of your life from falling too far behind.`;
  } else {
    needsSummary.textContent = "Your life is in balance right now. Keep an eye on the areas that start slipping.";
  }

  lastStatsSnapshot = { ...stats };
}

function renderProfile(profile) {
  profileName.textContent = profile.name;
  profileSubtitle.textContent = `${profile.title} — chasing a life to ${profile.dream}`;
  profileMood.textContent = profile.mood;
  profileStage.textContent = profile.stage;
  profileTrait.textContent = profile.trait;
  profileOrigin.textContent = profile.hometown;
  profileSummary.textContent = profile.summary;
  profileAgeBadge.textContent = profile.age_badge;
  if (profile.job_title) profileJob.textContent = profile.job_title;
  if (profile.education_label) profileEducation.textContent = profile.education_label;
  if (typeof profile.salary === "number") {
    salaryStat.textContent = profile.salary > 0 ? `$${profile.salary}/yr salary` : "No income";
  }
  animatePanelSwap(document.querySelector(".identity-card"));
}

function renderScenario(scenario) {
  if (!scenario) {
    // No event this year — quiet year
    hasActiveScenario = false;
    currentScenario = null;
    scenarioTitle.textContent = "A Quiet Year";
    scenarioText.textContent = "No major events this year. Take any actions you want, then press Next Year to continue.";
    choicesContainer.innerHTML = "";
    gameMessage.textContent = `Age ${currentStats.age} — nothing major happened.`;
    setAgeBtnReady();
    animatePanelSwap(document.querySelector(".story-panel"));
    return;
  }

  hasActiveScenario = true;
  currentScenario = scenario;
  scenarioTitle.textContent = scenario.title;
  scenarioText.textContent = scenario.text;
  choicesContainer.innerHTML = "";
  gameMessage.textContent = `Age ${currentStats.age} — something happened.`;
  setAgeBtnBlocked("Respond to this year's event");

  scenario.choices.forEach((choice) => {
    const button = document.createElement("button");
    button.className = "choice-btn";
    button.type = "button";
    button.textContent = choice.text;
    button.addEventListener("click", () => handleChoice(choice));
    choicesContainer.appendChild(button);
  });

  animatePanelSwap(document.querySelector(".story-panel"));
}

function renderScenarioResolved() {
  hasActiveScenario = false;
  currentScenario = null;
  scenarioTitle.textContent = "Year Resolved";
  scenarioText.textContent = "You handled this year's event. Take any final actions, then press Next Year.";
  choicesContainer.innerHTML = "";
  gameMessage.textContent = `Age ${currentStats.age} — year complete.`;
  setAgeBtnReady();
  animatePanelSwap(document.querySelector(".story-panel"));
}

function renderHistory(history) {
  historyList.innerHTML = "";
  historyCount.textContent = `${history.length} ${history.length === 1 ? "entry" : "entries"}`;

  const reversed = [...history].reverse();

  if (!reversed.length) {
    historyList.innerHTML = '<div class="history-empty">No major life events have been recorded yet.</div>';
    animatePanelSwap(document.querySelector(".history-card"));
    return;
  }

  reversed.forEach((entry) => {
    const item = document.createElement("div");
    item.className = "history-item";
    item.innerHTML = `<span class="history-age">Age ${entry.age}</span><p>${entry.event}</p>`;
    historyList.appendChild(item);
  });

  animatePanelSwap(document.querySelector(".history-card"));
}

function renderActions(actions) {
  actionsContainer.innerHTML = "";

  if (!actions || !actions.length) {
    actionsContainer.innerHTML = '<div class="history-empty">No actions available right now. Your best move is to respond to the current event or press Next Year.</div>';
    animatePanelSwap(document.querySelector(".actions-card"));
    return;
  }

  actions.forEach((action) => {
    const button = document.createElement("button");
    button.className = "action-btn";
    button.type = "button";
    button.innerHTML = `
      <span class="action-title">${action.title}</span>
      <span class="action-subtitle">${action.subtitle}</span>
      <span class="action-description">${action.description}</span>
    `;
    button.addEventListener("click", () => handleAction(action.id));
    actionsContainer.appendChild(button);
  });

  animatePanelSwap(document.querySelector(".actions-card"));
}

function showEnding(data) {
  gameOverCard.classList.remove("hidden");
  endingMessage.textContent = data.ending_message;
  endingTitle.textContent = data.ending_title || (data.status === "completed" ? "Life Complete" : "Game Over");
  endingMeta.textContent = `${data.player_profile.age_badge} — ${data.player_profile.title} — ${data.player_profile.mood}`;
  choicesContainer.innerHTML = "";
  scenarioTitle.textContent = "Your Journey Ends Here";
  scenarioText.textContent = "Your decisions created this life story. Restart and try a different path.";
  ageBtn.disabled = true;
  ageBtn.classList.remove("age-btn--ready");
  animatePanelSwap(gameOverCard);
}

// ── Core game functions ───────────────────────────────────────────────────────

async function startGame() {
  startBtn.disabled = true;
  startBtn.textContent = "Starting...";
  try {
    const response = await fetch("/start");
    if (!response.ok) throw new Error(`Start failed: ${response.status}`);
    const data = await response.json();

    currentStats   = data.stats;
    careerState    = data.career_state || { career_level: 0, education_level: 1 };
    currentHistory = data.history || [];
    usedScenarios  = data.used_scenarios || [];
    lifeFlags      = data.life_flags || [];
    profileSeed    = data.profile_seed || null;
    lastStatsSnapshot = null;
    hasActiveScenario = false;

    updateStatsUI(currentStats);
    renderProfile(data.player_profile);
    renderHistory(currentHistory);
    renderActions(data.available_actions || []);

    // Reset story panel to intro state
    gameMessage.textContent = "Your life is ready.";
    scenarioTitle.textContent = "Your Life Awaits";
    scenarioText.textContent = "Press Next Year to begin. Each year may bring an event that shapes your life — respond to it, take actions, then move on.";
    choicesContainer.innerHTML = "";
    resultText.textContent = "Choices and actions will appear here.";
    endingTitle.textContent = "Journey Complete";
    endingMessage.textContent = "";
    gameOverCard.classList.add("hidden");
    endingMeta.textContent = "";

    gameSection.classList.remove("hidden");
    animateDashboardEntrance();
    setAgeBtnReady();

  } catch (error) {
    gameMessage.textContent = "Something went wrong while starting the game.";
    console.error(error);
  } finally {
    startBtn.disabled = false;
    startBtn.textContent = "Start Your Life";
  }
}

async function ageUp() {
  setAgeBtnLoading();
  try {
    const response = await fetch("/age", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        stats: currentStats,
        career_state: careerState,
        history: currentHistory,
        used_scenarios: usedScenarios,
        life_flags: lifeFlags,
        profile_seed: profileSeed
      })
    });
    if (!response.ok) throw new Error(`Age request failed: ${response.status}`);
    const data = await response.json();

    currentStats   = data.updated_stats;
    careerState    = data.career_state || careerState;
    currentHistory = data.history || [];
    usedScenarios  = data.used_scenarios || [];
    lifeFlags      = data.life_flags || [];
    profileSeed    = data.profile_seed || profileSeed;

    updateStatsUI(currentStats);
    renderProfile(data.player_profile);
    renderHistory(currentHistory);
    renderActions(data.available_actions || []);

    if (data.status === "game_over" || data.status === "completed") {
      showEnding(data);
      return;
    }

    renderScenario(data.next_scenario);

  } catch (error) {
    resultText.textContent = "Something went wrong while advancing the year.";
    setAgeBtnReady();
    console.error(error);
  }
}

async function handleChoice(choice) {
  try {
    choicesContainer.innerHTML = '<button class="choice-btn" disabled>Processing...</button>';

    const response = await fetch("/choice", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        stats: currentStats,
        career_state: careerState,
        history: currentHistory,
        used_scenarios: usedScenarios,
        life_flags: lifeFlags,
        profile_seed: profileSeed,
        effects: choice.effects,
        result: choice.result,
        set_flags: choice.set_flags || [],
        clear_flags: choice.clear_flags || []
      })
    });
    if (!response.ok) throw new Error(`Choice failed: ${response.status}`);
    const data = await response.json();

    currentStats   = data.updated_stats;
    careerState    = data.career_state || careerState;
    currentHistory = data.history || [];
    lifeFlags      = data.life_flags || [];
    profileSeed    = data.profile_seed || profileSeed;

    updateStatsUI(currentStats);
    renderProfile(data.player_profile);
    renderHistory(currentHistory);
    renderActions(data.available_actions || []);
    resultText.textContent = data.result_text;
    animatePanelSwap(document.querySelector(".result-card"));

    if (data.status === "game_over" || data.status === "completed") {
      showEnding(data);
      return;
    }

    // Choice resolved — no new scenario, player presses Next Year when ready
    renderScenarioResolved();

  } catch (error) {
    resultText.textContent = "An error happened while processing your decision.";
    if (currentScenario) renderScenario(currentScenario);
    console.error(error);
  }
}

async function handleAction(actionId) {
  try {
    actionsContainer.innerHTML = '<button class="action-btn" disabled>Taking action...</button>';

    const response = await fetch("/action", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        stats: currentStats,
        career_state: careerState,
        history: currentHistory,
        used_scenarios: usedScenarios,
        life_flags: lifeFlags,
        profile_seed: profileSeed,
        action_id: actionId
      })
    });
    if (!response.ok) throw new Error(`Action failed: ${response.status}`);
    const data = await response.json();

    currentStats   = data.updated_stats;
    careerState    = data.career_state || careerState;
    currentHistory = data.history || [];
    lifeFlags      = data.life_flags || [];
    profileSeed    = data.profile_seed || profileSeed;

    updateStatsUI(currentStats);
    renderProfile(data.player_profile);
    renderHistory(currentHistory);
    renderActions(data.available_actions || []);
    resultText.textContent = data.result_text;
    animatePanelSwap(document.querySelector(".result-card"));

    if (data.status === "game_over" || data.status === "completed") {
      showEnding(data);
      return;
    }

    // Actions don't change scenario state — keep the story panel as-is
    animatePanelSwap(document.querySelector(".actions-card"));

  } catch (error) {
    resultText.textContent = "An error happened while processing your action.";
    console.error(error);
  }
}

// ── Event listeners ───────────────────────────────────────────────────────────

startBtn.addEventListener("click", startGame);
restartBtn.addEventListener("click", startGame);
ageBtn.addEventListener("click", ageUp);
