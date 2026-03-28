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

const startBtn = document.getElementById("start-btn");
const restartBtn = document.getElementById("restart-btn");
const gameSection = document.getElementById("game-section");
const gameMessage = document.getElementById("game-message");
const scenarioTitle = document.getElementById("scenario-title");
const scenarioText = document.getElementById("scenario-text");
const choicesContainer = document.getElementById("choices-container");
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

function updateStatsUI(stats) {
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
}

function renderScenario(scenario) {
  if (!scenario) {
    currentScenario = null;
    scenarioTitle.textContent = "No Scenario Available";
    scenarioText.textContent = "There are no life events available right now. Restart and try again.";
    choicesContainer.innerHTML = "";
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
}

function renderHistory(history) {
  historyList.innerHTML = "";

  const reversedHistory = [...history].reverse();

  reversedHistory.forEach((entry) => {
    const item = document.createElement("div");
    item.className = "history-item";
    item.innerHTML = `
      <span class="history-age">Age ${entry.age}</span>
      <p>${entry.event}</p>
    `;
    historyList.appendChild(item);
  });
}

async function startGame() {
  try {
    const response = await fetch("/start");
    const data = await response.json();

    currentStats = data.stats;
    currentHistory = data.history || [];
    usedScenarios = data.used_scenarios || [];
    profileSeed = data.profile_seed || null;

    updateStatsUI(currentStats);
    renderProfile(data.player_profile);
    renderHistory(currentHistory);

    gameMessage.textContent = data.message;
    resultText.textContent = "Choose a path to reveal the consequences.";
    endingTitle.textContent = "Journey Complete";
    endingMessage.textContent = "";
    gameOverCard.classList.add("hidden");
    endingMeta.textContent = "";
    gameSection.classList.remove("hidden");

    renderScenario(data.scenario);
  } catch (error) {
    gameMessage.textContent = "Something went wrong while starting the game.";
    console.error(error);
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
        profile_seed: profileSeed,
        effects: choice.effects,
        result: choice.result
      })
    });

    const data = await response.json();

    currentStats = data.updated_stats;
    currentHistory = data.history || [];
    usedScenarios = data.used_scenarios || [];
    profileSeed = data.profile_seed || profileSeed;

    updateStatsUI(currentStats);
    renderProfile(data.player_profile);
    renderHistory(currentHistory);
    resultText.textContent = data.result_text;

    if (data.status === "game_over" || data.status === "completed") {
      gameOverCard.classList.remove("hidden");
      endingMessage.textContent = data.ending_message;
      endingTitle.textContent = data.ending_title || (data.status === "completed" ? "Life Complete" : "Game Over");
      endingMeta.textContent = `${data.player_profile.age_badge} - ${data.player_profile.title} - ${data.player_profile.mood}`;
      choicesContainer.innerHTML = "";
      scenarioTitle.textContent = "Your Journey Ends Here";
      scenarioText.textContent = "Your decisions created this life story. Restart and try a different path.";
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

startBtn.addEventListener("click", startGame);
restartBtn.addEventListener("click", startGame);
