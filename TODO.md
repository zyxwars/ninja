Add convert or convert_alpha to every image for massive performance improvement

# Current:

- [ ] Add enemy sounds
- [ ] Change enemy speed when chasing player
- [ ] Use custom pygame events
- [ ] Fix enemy attack range
- [ ] Add gray hp to player on kill
- [ ] Clean up prop passing inside playable_scene
- [ ] Use layers
- [ ] Load tiled object images using their name as the filename

# Back burner:

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

- [ ] Smooth out scrolling jitter over small distance
- [ ] Weird collision still sometimes happens
- [x] Scrolling camera causes weird speed up effect after running for some time
- [x] Rounding error when value is less than a pixel due to delta_time
- [ ] Fix crosshair accuracy
- [ ] Fix projectile indicator offset

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

- [ ] VS mode
  - tag mode
  - duel mode
  - co-op
- [ ] Browser, Mobile port
