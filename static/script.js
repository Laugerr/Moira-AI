let currentStats = {
  age: 18,
  money: 50,
  energy: 50,
  happiness: 50,
  risk: 20
};

let currentHistory = [];
let usedScenarios = [];
let currentScenario = null;

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
const historyList = document.getElementById("history-list");

const ageStat = document.getElementById("age-stat");
const moneyStat = document.getElementById("money-stat");
const energyStat = document.getElementById("energy-stat");
const happinessStat = document.getElementById("happiness-stat");
const riskStat = document.getElementById("risk-stat");

const energyBar = document.getElementById("energy-bar");
const happinessBar = document.getElementById("happiness-bar");
const riskBar = document.getElementById("risk-bar");

function updateStatsUI(stats) {
  ageStat.textContent = stats.age;
  moneyStat.textContent = `$${stats.money}`;
  energyStat.textContent = `${stats.energy}%`;
  happinessStat.textContent = `${stats.happiness}%`;
  riskStat.textContent = `${stats.risk}%`;

  energyBar.style.width = `${stats.energy}%`;
  happinessBar.style.width = `${stats.happiness}%`;
  riskBar.style.width = `${stats.risk}%`;
}

function renderScenario(scenario) {
  currentScenario = scenario;
  scenarioTitle.textContent = scenario.title;
  scenarioText.textContent = scenario.text;
  choicesContainer.innerHTML = "";

  scenario.choices.forEach((choice) => {
    const button = document.createElement("button");
    button.className = "choice-btn";
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

    updateStatsUI(currentStats);
    renderHistory(currentHistory);

    gameMessage.textContent = data.message;
    resultText.textContent = "Choose a path to reveal the consequences.";
    gameOverCard.classList.add("hidden");
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
        effects: choice.effects,
        result: choice.result
      })
    });

    const data = await response.json();

    currentStats = data.updated_stats;
    currentHistory = data.history || [];
    usedScenarios = data.used_scenarios || [];

    updateStatsUI(currentStats);
    renderHistory(currentHistory);
    resultText.textContent = data.result_text;

    if (data.status === "game_over" || data.status === "completed") {
      gameOverCard.classList.remove("hidden");
      endingMessage.textContent = data.ending_message;
      endingTitle.textContent = data.status === "completed" ? "Life Complete" : "Game Over";
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
