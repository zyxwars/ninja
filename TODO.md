# Current:

- [x] Add filetype to dialog
- [x] Delta time rounding, still not fixed
- [x] If delta is too low nothing will move as 0.5 -> 0

# Back burner:

- [ ] Block camera movement over 0, 0
- [ ] Add image background, parallax
- [ ] Add paint bucket
- [ ] Minimize the number of places where assets are loaded in
- [ ] Add editor undo button
- [ ] Change the multi surface layout to single surface with multiple sprite groups
- [ ] Add jump buffer back

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

- [ ] Boost orbs
- [ ] Enemies

- [ ] Resolution scaling

- [ ] VS mode
  - tag mode
  - duel mode
  - co-op
- [ ] Browser, Mobile port
