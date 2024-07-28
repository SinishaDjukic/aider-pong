# Intro
This as a remake of the Pong game in Python, created entirely using the Aider Chat https://aider.chat/

My goal was to see how easy it is to create a game using Aider without ever changing a line of code manually - all code modifications were done via the Aider text console chat. The only manual actions were generating and downloading a background image, and downloading a powerup icon.

# Game Rules (Summary)

1. **Objective**: Hit the ball past the opponent's paddle to score points.
2. **Scoring**: First to 100 points wins.
3. **Controls**: 'W'/'S' for left paddle, 'UP'/'DOWN' for right paddle.
4. **Ball Dynamics**: Bounces off edges, obstacles, and paddles.
5. **Obstacles**: Randomly generated, deflect the ball.
6. **Power-ups**: Spawn randomly, can add extra balls or increase paddle length.
7. **Game Reset**: Resets everything when a player wins.
8. **Graphics**: Custom background, shadows, colored paddles/balls, score display.

# Installation
```
pip install pygame
python main.py
```

# Takeways from Aider Chat
- LLM: The code was generated using OpenAI GPT-4o - seems to work very well with Aider
- Dev experience: Understands instructions for code modification based on desired functionality changes (indirect), as well as code/line specific instructions (direct). All code changes generate git diffs in the console and are committed (with auto-generated comments) to the local repo, which makes changes very transparent and understandable
- Cost: Total USD spent up until the initial code commit: ~7 USD
- Time:
  - Total time spent CHOPping (Chat-Oriented Programming) until the initial code commit: <3h
  - My previous experience with pygame: 0h. My previous experience with Python: beginner+
  - Gut feeling how much time it would take me to build the equivalent functionality in Python: ~16 hours
