# Intro
This as a remake of the Pong game in Python, created entirely using the Aider Chat https://aider.chat/

My goal was to see how easy it is to create a game using Aider without ever changing a line of code manually - all code modifications were done via the Aider text console chat. The only manual actions were generating and downloading a background image, and downloading a powerup icon.

# Game Rules

This Pong remake includes several enhancements compared to the original:

1. **Objective**: Two players control paddles to hit a ball back and forth. Score points by getting the ball past your opponent's paddle.

2. **Scoring**: 
   - Score a point when the ball passes the opponent's paddle and hits the screen edge.
   - First player to reach 100 points wins.

3. **Controls**:
   - Left paddle: 'W' (up) and 'S' (down)
   - Right paddle: 'UP' and 'DOWN' arrow keys

4. **Ball Dynamics**:
   - Bounces off screen edges and obstacles.
   - Deflects off paddles with curvature based on hit location.

5. **Obstacles**: 
   - Randomly generated every 10 seconds.
   - Deflect the ball on contact.

6. **Power-ups**:
   - Spawn randomly on the field.
   - Effects when collected:
     - Spawns an extra ball
     - Increases the length of the paddle that last hit the ball

7. **Game Reset**: 
   - Occurs when a player wins.
   - Resets scores, paddles, balls, and obstacles.

8. **Graphics**:
   - Custom background image
   - Visual effects like shadows
   - Colored paddles and balls
   - Score display at the top of the screen

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
