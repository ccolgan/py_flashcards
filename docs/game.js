// Simple Text-Based Adventure Game in JavaScript

// Function to start the game
function startGame() {
  alert("Welcome to the Adventure Game!"); // Welcome message
  alert("You wake up in a dark forest with no memory of how you got there.");

  // First choice: Where to go?
  let choice1 = prompt("Do you want to go left into the thick trees or right towards a cave? (Type 'left' or 'right')").toLowerCase();

  switch (choice1) {
      case 'left':
          goLeft();
          break;
      case 'right':
          goRight();
          break;
      default:
          alert("Invalid choice. The adventure ends before it begins.");
  }
}

// Function for the 'left' path
function goLeft() {
  alert("You walk through the thick trees and find an old cabin.");

  let choice2 = prompt("Do you enter the cabin or keep walking? (Type 'enter' or 'walk')").toLowerCase();

  switch (choice2) {
      case 'enter':
          alert("Inside the cabin, you find supplies and shelter. You survive the night. You win!");
          break;
      case 'walk':
          alert("You keep walking but get lost in the darkness. A mysterious creature finds you. Game Over.");
          break;
      default:
          alert("You hesitate too long. The forest consumes you. Game Over.");
  }
}

// Function for the 'right' path
function goRight() {
  alert("You approach the cave cautiously and hear strange noises from within.");

  let choice2 = prompt("Do you enter the cave or turn back? (Type 'enter' or 'back')").toLowerCase();

  switch (choice2) {
      case 'enter':
          alert("Inside the cave, you find hidden treasure but also awaken a sleeping dragon. Game Over.");
          break;
      case 'back':
          alert("You turn back and safely find your way out of the forest. You survive. You win!");
          break;
      default:
          alert("You freeze in fear. The cave's darkness swallows you. Game Over.");
  }
}

// Start the game
startGame();