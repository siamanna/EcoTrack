// script.js

let totalCarbon = 0;

// Track activity and calculate carbon footprint
function trackActivity() {
  const activity = document.getElementById('activity').value;
  totalCarbon += parseFloat(activity);
  document.getElementById('carbon').textContent = totalCarbon.toFixed(2);
}

// Weekly challenges
const challenges = [
  "Walk instead of drive for 2 days",
  "Take public transport this week",
  "Reduce water use by 10%",
  "Avoid single-use plastics for 3 days"
];

function getChallenge() {
  const challenge = challenges[Math.floor(Math.random() * challenges.length)];
  document.getElementById('challenge').textContent = challenge;
}

// Sustainability tips
const tips = [
  "Switch to LED bulbs to save energy.",
  "Unplug electronics when not in use.",
  "Reduce food waste by planning meals."
];

function getTip() {
  const tip = tips[Math.floor(Math.random() * tips.length)];
  document.getElementById('tip').textContent = tip;
}
