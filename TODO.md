Add convert or convert_alpha to every image for massive performance improvement

# Current:

- [x] Add enemy sounds
- [x] Fix enemy attack range
- [x] Make enemy search after last seen player pos was seen
- [x] Rework enemy to state machine
- [x] Add attacking back
- [x] Fix enemy spawns
- [x] Change alert rect size, wall collisions

- [ ] Add jump possible check
- [x] Change enemy speed when chasing player
- [ ] Use custom pygame events
- [x] Add gray hp to player on kill
- [ ] Clean up prop passing inside playable_scene
- [ ] Load tiled object images using their name as the filename

# Back burner:

- [ ] Animation transitions
- [ ] Order sprites rendering with layers
- [ ] Fix roaming enemies getting stuck when jumping
- [ ] Add proper support for larger non tileable images, like trees
- [x] Block camera movement over 0, 0
- [x] Add image background, parallax
- [ ] Minimize the number of places where assets are loaded in
- [ ] Minimize number of surfaces, especially transparency
- [ ] Add jump buffer back
- [ ] Background scrolling doesn't work over 0, 0

# Bugs:

- [ ] Enemy jumping against wall
- [ ] Smooth out scrolling jitter over small distance
- [x] Weird collision still sometimes happens
  - This had something to do with rect.height += 1 being applied even for jump collision and not just fall collision
- [x] Scrolling camera causes weird speed up effect after running for some time
- [x] Rounding error when value is less than a pixel due to delta_time

# Roadmap:

- [x] Textures
  - Texture importing workflow
- [x] Sound effects
- [x] Move to Tiled
- [ ] Enemies

### v0.2 ^

- [ ] Level loading
- [ ] Saving game state
- [ ] Menu screen
- [ ] Particles
- [ ] Dynamic sound track
  - Change based on in-game tension (number of enemies, player health, player kill streak)

### v0.3 ^

- [ ] Dialog system, bubbles, gibberish sound effects
- [ ] Boost orbs
- [ ] Resolution scaling

### v1 ^

### Concepts

- [ ] Ragdolls
- [ ] VS mode
  - tag mode
  - duel mode
  - co-op
- [ ] Browser, Mobile port
