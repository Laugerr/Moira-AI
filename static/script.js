// ── State ────────────────────────────────────────────────────────────────────

let currentStats = { age: 18, money: 50, health: 50, energy: 50, happiness: 50, social: 50 };
let careerState = { career_level: 0, education_level: 1 };
let relationshipState = { status: "single", partner_name: null, relationship_health: 0, children: 0 };
let currentHistory = [];
let usedScenarios = [];
let currentScenario = null;
let profileSeed = null;
let lifeFlags = [];
let lastStatsSnapshot = null;
let hasActiveScenario = false;

// ── DOM refs ─────────────────────────────────────────────────────────────────

const startBtn           = document.getElementById("start-btn");
const restartBtn         = document.getElementById("restart-btn");
const ageBtn             = document.getElementById("age-btn");
const gameSection        = document.getElementById("game-section");
const gameMessage        = document.getElementById("game-message");
const scenarioTitle      = document.getElementById("scenario-title");
const scenarioText       = document.getElementById("scenario-text");
const choicesContainer   = document.getElementById("choices-container");
const actionsContainer   = document.getElementById("actions-container");
const decisionsContainer = document.getElementById("decisions-container");
const resultTextEl       = document.getElementById("result-text");
const gameOverCard       = document.getElementById("game-over-card");
const endingMessage      = document.getElementById("ending-message");
const endingTitle        = document.getElementById("ending-title");
const endingMeta         = document.getElementById("ending-meta");
const historyList        = document.getElementById("history-list");
const historyCount       = document.getElementById("history-count");
const needsSummary       = document.getElementById("needs-summary");

// Strip elements
const profileNameEl      = document.getElementById("profile-name");
const profileAgeBadge    = document.getElementById("profile-age-badge");
const profileMood        = document.getElementById("profile-mood");
const profileRelationship = document.getElementById("profile-relationship");
const profileChildren    = document.getElementById("profile-children");
const moneyStatEl        = document.getElementById("money-stat");
const salaryStatEl       = document.getElementById("salary-stat");
const healthStatEl       = document.getElementById("health-stat");
const energyStatEl       = document.getElementById("energy-stat");
const happinessStatEl    = document.getElementById("happiness-stat");
const socialStatEl       = document.getElementById("social-stat");
const healthBar          = document.getElementById("health-bar");
const energyBar          = document.getElementById("energy-bar");
const happinessBar       = document.getElementById("happiness-bar");
const socialBar          = document.getElementById("social-bar");

// Profile tab elements
const profileJob         = document.getElementById("profile-job");
const profileEducation   = document.getElementById("profile-education");
const profileStage       = document.getElementById("profile-stage");
const profileTrait       = document.getElementById("profile-trait");
const profileOrigin      = document.getElementById("profile-origin");
const profileSubtitle    = document.getElementById("profile-subtitle");
const profileSummaryEl   = document.getElementById("profile-summary");

// Tab buttons
const tabBtns = document.querySelectorAll(".tab-btn");

// ── Tab switching ─────────────────────────────────────────────────────────────

function switchTab(tabName) {
  tabBtns.forEach(btn => {
    btn.classList.toggle("active", btn.dataset.tab === tabName);
  });
  document.querySelectorAll(".tab-panel").forEach(panel => {
    panel.classList.toggle("active", panel.id === `tab-${tabName}`);
  });
}

tabBtns.forEach(btn => {
  btn.addEventListener("click", () => switchTab(btn.dataset.tab));
});

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

// ── Stat animation helpers ────────────────────────────────────────────────────

function triggerValuePulse(element, direction) {
  if (!element || !direction) return;
  const className = direction > 0 ? "value-up" : "value-down";
  element.classList.remove("value-up", "value-down");
  void element.offsetWidth;
  element.classList.add(className);
}

function animateStatChanges(prev, next) {
  if (!prev) return;
  [["money", moneyStatEl], ["health", healthStatEl], ["energy", energyStatEl],
   ["happiness", happinessStatEl], ["social", socialStatEl]].forEach(([key, el]) => {
    const before = prev[key], after = next[key];
    if (typeof before === "number" && typeof after === "number" && before !== after) {
      triggerValuePulse(el, after - before);
    }
  });
}

// ── Render: stats strip ───────────────────────────────────────────────────────

function updateStatsUI(stats) {
  animateStatChanges(lastStatsSnapshot, stats);

  moneyStatEl.textContent    = `$${Number(stats.money).toLocaleString()}`;
  healthStatEl.textContent   = `${stats.health}%`;
  energyStatEl.textContent   = `${stats.energy}%`;
  happinessStatEl.textContent = `${stats.happiness}%`;
  socialStatEl.textContent   = `${stats.social}%`;

  healthBar.style.width    = `${stats.health}%`;
  energyBar.style.width    = `${stats.energy}%`;
  happinessBar.style.width = `${stats.happiness}%`;
  socialBar.style.width    = `${stats.social}%`;

  lastStatsSnapshot = { ...stats };
}

// ── Render: profile ───────────────────────────────────────────────────────────

function getRelationshipLabel(profile) {
  const status  = profile.relationship_status || "single";
  const partner = profile.partner_name;
  if (status === "single") return null;
  if (status === "dating"   && partner) return `Dating ${partner}`;
  if (status === "married"  && partner) return `Married to ${partner}`;
  if (status === "divorced")            return "Divorced";
  return status.charAt(0).toUpperCase() + status.slice(1);
}

function renderProfile(profile) {
  // Strip
  profileNameEl.textContent  = profile.name;
  profileAgeBadge.textContent = profile.age_badge;
  profileMood.textContent    = profile.mood;

  // Relationship chip
  const relLabel = getRelationshipLabel(profile);
  if (relLabel) {
    profileRelationship.textContent = relLabel;
    profileRelationship.classList.remove("hidden");
  } else {
    profileRelationship.classList.add("hidden");
  }

  // Children chip
  if (profile.children > 0) {
    profileChildren.textContent = `${profile.children} ${profile.children === 1 ? "Child" : "Children"}`;
    profileChildren.classList.remove("hidden");
  } else {
    profileChildren.classList.add("hidden");
  }

  // Money
  moneyStatEl.textContent = `$${Number(profile.salary > 0 ? profile.salary * 1000 : currentStats.money).toLocaleString()}`;
  // (keep money from stats which is more accurate — just update salary label)
  moneyStatEl.textContent = `$${Number(currentStats.money).toLocaleString()}`;
  salaryStatEl.textContent = profile.salary > 0 ? `$${profile.salary}k/yr` : "No income";

  // Profile tab
  if (profileJob)       profileJob.textContent       = profile.job_title || "Unemployed";
  if (profileEducation) profileEducation.textContent = profile.education_label || "High School";
  if (profileStage)     profileStage.textContent     = profile.stage;
  if (profileTrait)     profileTrait.textContent     = profile.trait;
  if (profileOrigin)    profileOrigin.textContent    = profile.hometown;
  if (profileSubtitle)  profileSubtitle.textContent  = `${profile.title} — chasing a life to ${profile.dream}`;
  if (profileSummaryEl) profileSummaryEl.textContent = profile.summary;

  // Needs summary (profile tab)
  if (needsSummary && lastStatsSnapshot) {
    const ranked = [
      ["Health", lastStatsSnapshot.health],
      ["Energy", lastStatsSnapshot.energy],
      ["Happiness", lastStatsSnapshot.happiness],
      ["Social", lastStatsSnapshot.social],
    ].sort((a, b) => a[1] - b[1]);
    const lowest  = ranked[0];
    const highest = ranked[ranked.length - 1];
    if (lowest[1] <= 20) {
      needsSummary.textContent = `${lowest[0]} is critical. Act now.`;
    } else if (lowest[1] <= 40) {
      needsSummary.textContent = `${lowest[0]} is your weakest need. ${highest[0]} is carrying your stability.`;
    } else if (highest[1] >= 75) {
      needsSummary.textContent = `${highest[0]} is a real strength. Don't let the rest slip.`;
    } else {
      needsSummary.textContent = "Life is in balance. Keep watching the edges.";
    }
  }
}

// ── Render: scenario ──────────────────────────────────────────────────────────

function renderScenario(scenario) {
  if (!scenario) {
    hasActiveScenario = false;
    currentScenario   = null;
    scenarioTitle.textContent = "A Quiet Year";
    scenarioText.textContent  = "Nothing major happened. Take any actions you want, then press Next Year.";
    choicesContainer.innerHTML = "";
    gameMessage.textContent    = `Age ${currentStats.age} — quiet year`;
    setAgeBtnReady();
    return;
  }

  hasActiveScenario = true;
  currentScenario   = scenario;
  scenarioTitle.textContent = scenario.title;
  scenarioText.textContent  = scenario.text;
  choicesContainer.innerHTML = "";
  gameMessage.textContent    = `Age ${currentStats.age} — something happened`;
  setAgeBtnBlocked("Respond first");

  scenario.choices.forEach((choice) => {
    const btn = document.createElement("button");
    btn.className  = "choice-btn";
    btn.type       = "button";
    btn.textContent = choice.text;
    btn.addEventListener("click", () => handleChoice(choice));
    choicesContainer.appendChild(btn);
  });

  // Auto-switch to story area (already visible) and animate the card
  document.querySelector(".stage-card").style.animation = "none";
  void document.querySelector(".stage-card").offsetWidth;
  document.querySelector(".stage-card").style.animation = "";
}

function renderScenarioResolved() {
  hasActiveScenario = false;
  currentScenario   = null;
  scenarioTitle.textContent  = "Year Resolved";
  scenarioText.textContent   = "Event handled. Take any final actions, then press Next Year.";
  choicesContainer.innerHTML = "";
  gameMessage.textContent    = `Age ${currentStats.age} — year complete`;
  setAgeBtnReady();
}

// ── Render: history ───────────────────────────────────────────────────────────

function renderHistory(history) {
  historyList.innerHTML = "";
  historyCount.textContent = `${history.length} ${history.length === 1 ? "entry" : "entries"}`;

  if (!history.length) {
    historyList.innerHTML = '<div class="history-empty">No events recorded yet.</div>';
    return;
  }

  [...history].reverse().forEach((entry) => {
    const item = document.createElement("div");
    const isMilestone = entry.type === "milestone";
    item.className = isMilestone ? "history-item history-item--milestone" : "history-item";

    if (isMilestone) {
      item.innerHTML = `<span class="history-age">Age ${entry.age}</span><span class="milestone-label">${entry.event}</span>`;
    } else {
      item.innerHTML = `<span class="history-age">Age ${entry.age}</span><p>${entry.event}</p>`;
    }

    historyList.appendChild(item);
  });

  // Flash the timeline tab badge when a new milestone arrives
  const lastEntry = history[history.length - 1];
  if (lastEntry && lastEntry.type === "milestone") {
    const timelineTab = document.querySelector('[data-tab="timeline"]');
    if (timelineTab) {
      timelineTab.classList.add("tab-btn--flash");
      setTimeout(() => timelineTab.classList.remove("tab-btn--flash"), 1200);
    }
  }
}

// ── Render: actions ───────────────────────────────────────────────────────────

function renderActions(actions) {
  actionsContainer.innerHTML = "";

  if (!actions || !actions.length) {
    actionsContainer.innerHTML = '<div class="history-empty" style="grid-column:1/-1">No actions available right now.</div>';
    return;
  }

  actions.forEach((action) => {
    const btn = document.createElement("button");
    btn.className = "action-btn";
    btn.type      = "button";
    btn.innerHTML = `
      <span class="action-title">${action.title}</span>
      <span class="action-subtitle">${action.subtitle}</span>
      <span class="action-description">${action.description}</span>
    `;
    btn.addEventListener("click", () => handleAction(action.id));
    actionsContainer.appendChild(btn);
  });
}

// ── Render: decisions ─────────────────────────────────────────────────────────

function renderDecisions(decisions) {
  decisionsContainer.innerHTML = "";

  if (!decisions || !decisions.length) {
    decisionsContainer.innerHTML = '<div class="history-empty">No major decisions available yet. Build your life and new paths will open.</div>';
    return;
  }

  decisions.forEach((decision) => {
    const btn = document.createElement("button");
    btn.className = "decision-btn";
    btn.type      = "button";
    btn.innerHTML = `
      <span class="decision-title">${decision.title}</span>
      <span class="decision-subtitle">${decision.subtitle}</span>
      <span class="decision-description">${decision.description}</span>
    `;
    btn.addEventListener("click", () => handleDecision(decision.id));
    decisionsContainer.appendChild(btn);
  });
}

// ── Render: game over ─────────────────────────────────────────────────────────

function showEnding(data) {
  gameOverCard.classList.remove("hidden");
  endingMessage.textContent = data.ending_message;
  endingTitle.textContent   = data.ending_title || (data.status === "completed" ? "Life Complete" : "Game Over");
  endingMeta.textContent    = `${data.player_profile.age_badge} — ${data.player_profile.title} — ${data.player_profile.mood}`;
  choicesContainer.innerHTML = "";
  ageBtn.disabled = true;
  ageBtn.classList.remove("age-btn--ready");
}

// ── Shared state sync ─────────────────────────────────────────────────────────

function syncState(data) {
  if (data.updated_stats)      currentStats      = data.updated_stats;
  if (data.career_state)       careerState       = data.career_state;
  if (data.relationship_state) relationshipState = data.relationship_state;
  if (data.history)            currentHistory    = data.history;
  if (data.used_scenarios)     usedScenarios     = data.used_scenarios;
  if (data.life_flags)         lifeFlags         = data.life_flags;
  if (data.profile_seed)       profileSeed       = data.profile_seed;
}

function buildRequestBody(extras = {}) {
  return JSON.stringify({
    stats: currentStats,
    career_state: careerState,
    relationship_state: relationshipState,
    history: currentHistory,
    used_scenarios: usedScenarios,
    life_flags: lifeFlags,
    profile_seed: profileSeed,
    ...extras
  });
}

// ── Core game functions ───────────────────────────────────────────────────────

async function startGame() {
  startBtn.disabled   = true;
  startBtn.textContent = "Starting...";
  try {
    const res = await fetch("/start");
    if (!res.ok) throw new Error(`Start failed: ${res.status}`);
    const data = await res.json();

    currentStats      = data.stats;
    careerState       = data.career_state  || { career_level: 0, education_level: 1 };
    relationshipState = data.relationship_state || { status: "single", partner_name: null, relationship_health: 0, children: 0 };
    currentHistory    = data.history       || [];
    usedScenarios     = data.used_scenarios || [];
    lifeFlags         = data.life_flags    || [];
    profileSeed       = data.profile_seed  || null;
    lastStatsSnapshot = null;
    hasActiveScenario = false;

    updateStatsUI(currentStats);
    renderProfile(data.player_profile);
    renderHistory(currentHistory);
    renderActions(data.available_actions  || []);
    renderDecisions(data.available_decisions || []);

    // Reset story stage
    scenarioTitle.textContent  = "Your Life Awaits";
    scenarioText.textContent   = "Press Next Year to begin. Each year may bring an event — respond to it, take actions, then move on.";
    choicesContainer.innerHTML = "";
    gameMessage.textContent    = "Ready.";
    resultTextEl.textContent   = "Choices and actions will appear here.";
    gameOverCard.classList.add("hidden");

    gameSection.classList.remove("hidden");
    switchTab("actions");
    setAgeBtnReady();

  } catch (err) {
    gameMessage.textContent = "Something went wrong while starting.";
    console.error(err);
  } finally {
    startBtn.disabled   = false;
    startBtn.textContent = "Start Your Life";
  }
}

async function ageUp() {
  setAgeBtnLoading();
  try {
    const res = await fetch("/age", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: buildRequestBody()
    });
    if (!res.ok) throw new Error(`Age failed: ${res.status}`);
    const data = await res.json();

    syncState(data);
    updateStatsUI(currentStats);
    renderProfile(data.player_profile);
    renderHistory(currentHistory);
    renderActions(data.available_actions   || []);
    renderDecisions(data.available_decisions || []);

    if (data.status === "game_over" || data.status === "completed") {
      showEnding(data);
      return;
    }

    renderScenario(data.next_scenario);

  } catch (err) {
    resultTextEl.textContent = "Something went wrong advancing the year.";
    setAgeBtnReady();
    console.error(err);
  }
}

async function handleChoice(choice) {
  try {
    choicesContainer.innerHTML = '<button class="choice-btn" disabled>Processing...</button>';

    const res = await fetch("/choice", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: buildRequestBody({
        effects:     choice.effects,
        result:      choice.result,
        set_flags:   choice.set_flags   || [],
        clear_flags: choice.clear_flags || []
      })
    });
    if (!res.ok) throw new Error(`Choice failed: ${res.status}`);
    const data = await res.json();

    syncState(data);
    updateStatsUI(currentStats);
    renderProfile(data.player_profile);
    renderHistory(currentHistory);
    renderActions(data.available_actions   || []);
    renderDecisions(data.available_decisions || []);
    resultTextEl.textContent = data.result_text;

    if (data.status === "game_over" || data.status === "completed") {
      showEnding(data);
      return;
    }

    renderScenarioResolved();

  } catch (err) {
    resultTextEl.textContent = "An error happened processing your decision.";
    if (currentScenario) renderScenario(currentScenario);
    console.error(err);
  }
}

async function handleAction(actionId) {
  try {
    actionsContainer.innerHTML = '<button class="action-btn" disabled>Taking action...</button>';

    const res = await fetch("/action", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: buildRequestBody({ action_id: actionId })
    });
    if (!res.ok) throw new Error(`Action failed: ${res.status}`);
    const data = await res.json();

    syncState(data);
    updateStatsUI(currentStats);
    renderProfile(data.player_profile);
    renderHistory(currentHistory);
    renderActions(data.available_actions   || []);
    renderDecisions(data.available_decisions || []);
    resultTextEl.textContent = data.result_text;

    if (data.status === "game_over" || data.status === "completed") {
      showEnding(data);
      return;
    }

  } catch (err) {
    resultTextEl.textContent = "An error happened processing your action.";
    console.error(err);
  }
}

async function handleDecision(decisionId) {
  try {
    decisionsContainer.innerHTML = '<button class="decision-btn" disabled>Deciding...</button>';

    const res = await fetch("/decision", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: buildRequestBody({ decision_id: decisionId })
    });
    if (!res.ok) throw new Error(`Decision failed: ${res.status}`);
    const data = await res.json();

    syncState(data);
    updateStatsUI(currentStats);
    renderProfile(data.player_profile);
    renderHistory(currentHistory);
    renderActions(data.available_actions   || []);
    renderDecisions(data.available_decisions || []);
    resultTextEl.textContent = data.result_text;

    if (data.status === "game_over" || data.status === "completed") {
      showEnding(data);
      return;
    }

    // Flash the timeline tab so the player sees the milestone
    switchTab("timeline");
    setTimeout(() => switchTab("decisions"), 1800);

  } catch (err) {
    resultTextEl.textContent = "An error happened processing your decision.";
    console.error(err);
  }
}

// ── Event listeners ───────────────────────────────────────────────────────────

startBtn.addEventListener("click", startGame);
restartBtn.addEventListener("click", startGame);
ageBtn.addEventListener("click", ageUp);
