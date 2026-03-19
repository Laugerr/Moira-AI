let currentStats = {
  money: 50,
  energy: 50,
  happiness: 50,
  risk: 20
};

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

const moneyStat = document.getElementById("money-stat");
const energyStat = document.getElementById("energy-stat");
const happinessStat = document.getElementById("happiness-stat");
const riskStat = document.getElementById("risk-stat");

function updateStatsUI(stats) {
  moneyStat.textContent = stats.money;
  energyStat.textContent = stats.energy;
  happinessStat.textContent = stats.happiness;
  riskStat.textContent = stats.risk;
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

async function startGame() {
  try {
    const response = await fetch("/start");
    const data = await response.json();

    currentStats = data.stats;
    updateStatsUI(currentStats);

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
    const response = await fetch("/choice", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        stats: currentStats,
        effects: choice.effects,
        result: choice.result
      })
    });

    const data = await response.json();

    currentStats = data.updated_stats;
    updateStatsUI(currentStats);

    resultText.textContent = data.result_text;

    if (data.status === "game_over") {
      gameOverCard.classList.remove("hidden");
      endingMessage.textContent = data.ending_message;
      choicesContainer.innerHTML = "";
      scenarioTitle.textContent = "Your Journey Ends Here";
      scenarioText.textContent = "Your choices shaped this outcome. Restart and try a different path.";
      return;
    }

    renderScenario(data.next_scenario);
  } catch (error) {
    resultText.textContent = "An error happened while processing your decision.";
    console.error(error);
  }
}

startBtn.addEventListener("click", startGame);
restartBtn.addEventListener("click", startGame);