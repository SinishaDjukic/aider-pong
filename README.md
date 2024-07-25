# Intro
This as a remake of the Pong game in Python, created entirely using the [Aider Chat|https://aider.chat/].

My goal was to see how easy it is to create a game using Aider without ever changing a line of code manually - all code modifications were done via the Aider text console chat. The only manual actions were generating and downloading a background image, and downloading a powerup icon.

# Game Rules
I added some bells and whistles compared to the original, like powerups which spawn an extra ball, randomly generated obstacles that deflect the balls, increasing length of paddles upon hitting a powerup, reflection curvature of the paddle towards the edge, etc.

Objectives as summarized by the Aider Chat directly and entirely based on the code:

## Objective
 The game is a Pong-like game where two players control paddles to hit a ball back and
 forth. The goal is to score points by getting the ball past the opponent's paddle.

 ## Scoring
 - A player scores a point when the ball passes the opponent's paddle and hits the left o
 right edge of the screen.
 - The game ends when a player reaches 100 points.

 ## Paddles
 - Each player controls a paddle that can move up and down.
 - The left paddle is controlled using the 'W' and 'S' keys.
 - The right paddle is controlled using the 'UP' and 'DOWN' arrow keys.
 - Paddles have a maximum speed and acceleration/deceleration for smoother movement.

 ## Ball
 - The ball moves continuously and bounces off the top and bottom edges of the screen.
 - The ball can collide with paddles and obstacles.
 - When the ball collides with a paddle, it deflects based on where it hits the paddle,
 adding curvature to its trajectory.

 ## Obstacles
 - Obstacles are added to the game every 10 seconds.
 - Obstacles are randomly placed and can block the ball, causing it to bounce off.

 ## Power-ups
 - A power-up appears on the screen and can be collected by the ball.
 - When a ball collects a power-up, a new ball is spawned, and the paddle that last
 deflected the ball grows in size.
 - Power-ups have an animation effect when they appear.

 ## Game Reset
 - The game resets when a player wins, setting scores back to 0 and reinitializing paddle
 balls, and obstacles.

 ## Graphics
 - The game includes a background image, shadows for visual effects, and colored paddles
 and balls.
 - Scores are displayed at the top of the screen in different colors for each player.

# Installation
```
pip install pygame
python main.py
```

# Takeways from Aider Chat
- LLM: The code was generated using OpenAI GPT-4o - seems to work very well with Aider
- Dev experience: understands instructions for code modification based on desired functionality changes (indirect), as well as code/line specific instructions (direct). All code changes generate git diffs in the console and are committed (with auto-generated comments) to the local repo, which makes changes very transparent and understandable
- Cost: Total USD spent up until the initial code commit: ~7 USD
- Time:
  - Total time spent CHOPping (Chat-Oriented Programming) until the initial code commit: <3h
  - My previous experience with pygame: 0h. My previous experience with Python: beginner+
  - Gut feeling how much time it would take me to build the equivalent functionality in Python: ~20 hours
