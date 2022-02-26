Add convert or convert_alpha to every image for massive performance improvement

# Current:

- [ ] Add menu screen
- [ ] Change between levels, triggers
- [ ] Add checkpoints

# Back burner:

- [ ] Use custom pygame events
- [ ] Clean up prop passing inside playable_scene
- [ ] Load tiled object images using their name as the filename
- [ ] Animation transitions
- [ ] Order sprites rendering with layers
- [ ] Add proper support for larger non tileable images, like trees
- [ ] Minimize the number of places where assets are loaded in
- [ ] Minimize number of surfaces, especially transparency
- [ ] Add jump buffer back
- [ ] Smooth out scrolling jitter over small distance

# Bugs:

- [ ] Background scrolling doesn't work over 0, 0
- [ ] Fix roaming enemies getting stuck when jumping
- [ ] Enemy jumping against wall

# Roadmap:

### - [x] v0.2

- [x] Textures
  - Texture importing workflow
- [x] Sound effects
- [x] Move to Tiled
- [x] Enemies

### v0.3

- [ ] Level loading
- [ ] Saving game state
- [ ] Menu screen

### v0.4

- [ ] Particles
- [ ] Dynamic sound track
  - Change based on in-game tension (number of enemies, player health, player kill streak)

### v1

- [ ] Dialog system, bubbles, gibberish sound effects
- [ ] Boost orbs
- [ ] Resolution scaling

### Concepts

- [ ] Ragdolls
- [ ] VS mode
  - tag
  - duel
  - co-op
- [ ] Browser, Mobile port
