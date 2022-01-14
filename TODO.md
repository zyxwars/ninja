Add convert or convert_alpha to every image for massive performance improvement

# Current:

- [ ] Framework for adding weapons and attack types easily
- [ ] Make camera shift accessible in debug

# Back burner:

- [ ] Enemy player alert
  - [ ] Roam activated when searching for player or the patrol route is broken for some other reason
- [ ] Fix roaming enemies getting stuck when jumping
- [ ] Add proper support for larger non tileable images, like trees
- [x] Block camera movement over 0, 0
- [x] Add image background, parallax
- [ ] Minimize the number of places where assets are loaded in
- [ ] Add jump buffer back
- [ ] Background scrolling doesn't work over 0, 0

# Bugs:

- [ ] Smooth out scrolling jitter over small distance
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
- [x] Move to Tiled
- [ ] Enemies

### v0.2 ^

- [ ] Dialog system, bubbles, gibberish sound effects
- [ ] Boost orbs
- [ ] Level loading
- [ ] Saving game state
- [ ] Menu screen
- [ ] Resolution scaling

### v1 ^

### Concepts

- [ ] VS mode
  - tag mode
  - duel mode
  - co-op
- [ ] Browser, Mobile port
