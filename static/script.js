let currentStats = {
  age: 18,
  money: 50,
  health: 50,
  energy: 50,
  happiness: 50,
  social: 50
};

let currentHistory = [];
let usedScenarios = [];
let currentScenario = null;
let profileSeed = null;
let lifeFlags = [];
let lastStatsSnapshot = null;

const startBtn = document.getElementById("start-btn");
const restartBtn = document.getElementById("restart-btn");
const gameSection = document.getElementById("game-section");
const gameMessage = document.getElementById("game-message");
const scenarioTitle = document.getElementById("scenario-title");
const scenarioText = document.getElementById("scenario-text");
const choicesContainer = document.getElementById("choices-container");
const actionsContainer = document.getElementById("actions-container");
const resultText = document.getElementById("result-text");
const gameOverCard = document.getElementById("game-over-card");
const endingMessage = document.getElementById("ending-message");
const endingTitle = document.getElementById("ending-title");
const endingMeta = document.getElementById("ending-meta");
const historyList = document.getElementById("history-list");

const ageStat = document.getElementById("age-stat");
const moneyStat = document.getElementById("money-stat");
const healthStat = document.getElementById("health-stat");
const energyStat = document.getElementById("energy-stat");
const happinessStat = document.getElementById("happiness-stat");
const socialStat = document.getElementById("social-stat");
const healthState = document.getElementById("health-state");
const energyState = document.getElementById("energy-state");
const happinessState = document.getElementById("happiness-state");
const socialState = document.getElementById("social-state");
const historyCount = document.getElementById("history-count");
const needsSummary = document.getElementById("needs-summary");

const healthBar = document.getElementById("health-bar");
const energyBar = document.getElementById("energy-bar");
const happinessBar = document.getElementById("happiness-bar");
const socialBar = document.getElementById("social-bar");
const profileName = document.getElementById("profile-name");
const profileSubtitle = document.getElementById("profile-subtitle");
const profileMood = document.getElementById("profile-mood");
const profileStage = document.getElementById("profile-stage");
const profileTrait = document.getElementById("profile-trait");
const profileOrigin = document.getElementById("profile-origin");
const profileSummary = document.getElementById("profile-summary");
const profileAgeBadge = document.getElementById("profile-age-badge");

const animatedPanels = document.querySelectorAll(
  ".identity-card, .story-panel, .actions-card, .status-card, .result-card, .history-card"
);

function getNeedState(value) {
  if (value <= 20) {
    return { label: "Critical", tone: "critical" };
  }

  if (value <= 40) {
    return { label: "Low", tone: "low" };
  }

  if (value >= 75) {
    return { label: "Strong", tone: "strong" };
  }

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

function animatePanelSwap(element) {
  if (!element) {
    return;
  }

  element.classList.remove("content-refresh");
  void element.offsetWidth;
  element.classList.add("content-refresh");
}

function triggerValuePulse(element, direction) {
  if (!element || !direction) {
    return;
  }

  const className = direction > 0 ? "value-up" : "value-down";
  element.classList.remove("value-up", "value-down");
  void element.offsetWidth;
  element.classList.add(className);
}

function animateStatChanges(previousStats, nextStats) {
  if (!previousStats) {
    return;
  }

  const statMap = [
    ["money", moneyStat],
    ["health", healthStat],
    ["energy", energyStat],
    ["happiness", happinessStat],
    ["social", socialStat]
  ];

  statMap.forEach(([key, element]) => {
    const before = previousStats[key];
    const after = nextStats[key];

    if (typeof before === "number" && typeof after === "number" && before !== after) {
      triggerValuePulse(element, after - before);
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
  profileSubtitle.textContent = `${profile.title} - Chasing a life to ${profile.dream}`;
  profileMood.textContent = profile.mood;
  profileStage.textContent = profile.stage;
  profileTrait.textContent = profile.trait;
  profileOrigin.textContent = profile.hometown;
  profileSummary.textContent = profile.summary;
  profileAgeBadge.textContent = profile.age_badge;
  animatePanelSwap(document.querySelector(".identity-card"));
}

function renderScenario(scenario) {
  if (!scenario) {
    currentScenario = null;
    scenarioTitle.textContent = "No Scenario Available";
    scenarioText.textContent = "There are no life events available right now. Restart and try again.";
    choicesContainer.innerHTML = "";
    animatePanelSwap(document.querySelector(".story-panel"));
    return;
  }

  currentScenario = scenario;
  scenarioTitle.textContent = scenario.title;
  scenarioText.textContent = scenario.text;
  choicesContainer.innerHTML = "";

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

function renderHistory(history) {
  historyList.innerHTML = "";
  historyCount.textContent = `${history.length} ${history.length === 1 ? "entry" : "entries"}`;

  const reversedHistory = [...history].reverse();

  if (!reversedHistory.length) {
    historyList.innerHTML = '<div class="history-empty">No major life events have been recorded yet.</div>';
    animatePanelSwap(document.querySelector(".history-card"));
    return;
  }

  reversedHistory.forEach((entry) => {
    const item = document.createElement("div");
    item.className = "history-item";
    item.innerHTML = `
      <span class="history-age">Age ${entry.age}</span>
      <p>${entry.event}</p>
    `;
    historyList.appendChild(item);
  });

  animatePanelSwap(document.querySelector(".history-card"));
}

function renderActions(actions) {
  actionsContainer.innerHTML = "";

  if (!actions || !actions.length) {
    actionsContainer.innerHTML = '<div class="history-empty">No self-directed actions are available right now. Your best option is to respond to the current life event.</div>';
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

async function startGame() {
  startBtn.disabled = true;
  startBtn.textContent = "Starting...";
  try {
    const response = await fetch("/start");
    if (!response.ok) {
      throw new Error(`Start request failed: ${response.status}`);
    }
    const data = await response.json();

    currentStats = data.stats;
    currentHistory = data.history || [];
    usedScenarios = data.used_scenarios || [];
    lifeFlags = data.life_flags || [];
    profileSeed = data.profile_seed || null;

    updateStatsUI(currentStats);
    renderProfile(data.player_profile);
    renderHistory(currentHistory);
    renderActions(data.available_actions || []);

    gameMessage.textContent = data.message;
    resultText.textContent = "Choose a path to reveal the consequences.";
    endingTitle.textContent = "Journey Complete";
    endingMessage.textContent = "";
    gameOverCard.classList.add("hidden");
    endingMeta.textContent = "";
    gameSection.classList.remove("hidden");
    animateDashboardEntrance();

    renderScenario(data.scenario);
  } catch (error) {
    gameMessage.textContent = "Something went wrong while starting the game.";
    console.error(error);
  } finally {
    startBtn.disabled = false;
    startBtn.textContent = "Start Your Life";
  }
}

async function handleChoice(choice) {
  try {
    choicesContainer.innerHTML = '<button class="choice-btn" disabled>Processing your decision...</button>';

    const response = await fetch("/choice", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        stats: currentStats,
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
    if (!response.ok) {
      throw new Error(`Choice request failed: ${response.status}`);
    }

    const data = await response.json();

    currentStats = data.updated_stats;
    currentHistory = data.history || [];
    usedScenarios = data.used_scenarios || [];
    lifeFlags = data.life_flags || [];
    profileSeed = data.profile_seed || profileSeed;

    updateStatsUI(currentStats);
    renderProfile(data.player_profile);
    renderHistory(currentHistory);
    renderActions(data.available_actions || []);
    resultText.textContent = data.result_text;
    animatePanelSwap(document.querySelector(".result-card"));

    if (data.status === "game_over" || data.status === "completed") {
      gameOverCard.classList.remove("hidden");
      endingMessage.textContent = data.ending_message;
      endingTitle.textContent = data.ending_title || (data.status === "completed" ? "Life Complete" : "Game Over");
      endingMeta.textContent = `${data.player_profile.age_badge} - ${data.player_profile.title} - ${data.player_profile.mood}`;
      choicesContainer.innerHTML = "";
      scenarioTitle.textContent = "Your Journey Ends Here";
      scenarioText.textContent = "Your decisions created this life story. Restart and try a different path.";
      animatePanelSwap(gameOverCard);
      return;
    }

    renderScenario(data.next_scenario);
  } catch (error) {
    resultText.textContent = "An error happened while processing your decision.";

    if (currentScenario) {
      renderScenario(currentScenario);
    }

    console.error(error);
  }
}

async function handleAction(actionId) {
  try {
    actionsContainer.innerHTML = '<button class="action-btn" disabled>Taking action...</button>';

    const response = await fetch("/action", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        stats: currentStats,
        history: currentHistory,
        used_scenarios: usedScenarios,
        life_flags: lifeFlags,
        profile_seed: profileSeed,
        action_id: actionId
      })
    });

    if (!response.ok) {
      throw new Error(`Action request failed: ${response.status}`);
    }

    const data = await response.json();

    currentStats = data.updated_stats;
    currentHistory = data.history || [];
    usedScenarios = data.used_scenarios || [];
    lifeFlags = data.life_flags || [];
    profileSeed = data.profile_seed || profileSeed;

    updateStatsUI(currentStats);
    renderProfile(data.player_profile);
    renderHistory(currentHistory);
    renderActions(data.available_actions || []);
    resultText.textContent = data.result_text;
    animatePanelSwap(document.querySelector(".result-card"));

    if (data.status === "game_over" || data.status === "completed") {
      gameOverCard.classList.remove("hidden");
      endingMessage.textContent = data.ending_message;
      endingTitle.textContent = data.ending_title || (data.status === "completed" ? "Life Complete" : "Game Over");
      endingMeta.textContent = `${data.player_profile.age_badge} - ${data.player_profile.title} - ${data.player_profile.mood}`;
      choicesContainer.innerHTML = "";
      scenarioTitle.textContent = "Your Journey Ends Here";
      scenarioText.textContent = "Your decisions created this life story. Restart and try a different path.";
      animatePanelSwap(gameOverCard);
      return;
    }

    renderScenario(data.next_scenario);
  } catch (error) {
    resultText.textContent = "An error happened while processing your action.";
    renderActions(getFallbackActions());
    console.error(error);
  }
}

function getFallbackActions() {
  return [
    {
      id: "work_shift",
      title: "Work Extra",
      subtitle: "Trade comfort for cash",
      description: "Take on extra work to strengthen your finances, even if it drains your energy."
    },
    {
      id: "study_focus",
      title: "Study",
      subtitle: "Build long-term potential",
      description: "Spend time learning and improving your future options at the cost of short-term energy."
    },
    {
      id: "rest_reset",
      title: "Rest",
      subtitle: "Recover before you crack",
      description: "Slow down and protect yourself before stress and fatigue become something worse."
    },
    {
      id: "social_time",
      title: "Socialize",
      subtitle: "Invest in connection",
      description: "Spend real time with people who matter and keep your relationships alive."
    }
  ];
}

startBtn.addEventListener("click", startGame);
restartBtn.addEventListener("click", startGame);
