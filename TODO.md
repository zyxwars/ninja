Add convert or convert_alpha to every image for massive performance improvement

# Current:

# Back burner:

- [ ] Smooth out scrolling jitter over small distance
- [x] Block camera movement over 0, 0
- [x] Add image background, parallax
- [ ] Add paint bucket
- [ ] Minimize the number of places where assets are loaded in
- [ ] Add editor undo button
- [ ] Add jump buffer back
- [ ] Background scrolling doesn't work over 0, 0

# Bugs:

- [ ] Weird collision still sometimes happens
- [x] Scrolling camera causes weird speed up effect after running for some time
- [x] Rounding error when value is less than a pixel due to delta_time
- [ ] Fix crosshair accuracy
- [ ] Fix projectile indicator offset

# Roadmap:

- [x] Textures
  - [x] Texture importing workflow
  - [ ] Fall impact smoke, particles
- [x] Sound effects
  - [ ] Add variation
  - [ ] Change based on in-game tension (number of enemies, player health, player kill streak)
- [ ] Add layers to editor
- [ ] Level loading
- [ ] Saving game state
- [ ] Menu screen

- [ ] Dialog system, bubbles, gibberish sound effects
- [ ] Boost orbs
- [ ] Enemies

- [ ] Resolution scaling

- [ ] VS mode
  - tag mode
  - duel mode
  - co-op
- [ ] Browser, Mobile port
