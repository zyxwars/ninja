# Only import with "import game" to make the module pattern "singleton" work properly

from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from main import Game


RENDER_SCREEN_WIDTH = 1280
RENDER_SCREEN_HEIGHT = 720
RENDER_SCREEN_CENTER = (int(RENDER_SCREEN_WIDTH/2),
                        int(RENDER_SCREEN_HEIGHT/2))

TILE_SIZE = 32
CAMERA_X_SPEED = 500
CAMERA_Y_SPEED = 500


# Player
SPEED = 0.5
GRAVITY = 0.005
JUMP_FORCE = 1.4
ANIMATION_SPEED = 0.008
JUMP_BUFFER = 160
ALERT_AREA = (128, 0)

PLAYABLE_SCENES_PATH = './scenes/map/'
LEVEL_MAP = {
    0: PLAYABLE_SCENES_PATH + 'plain.json',
    1: PLAYABLE_SCENES_PATH + 'castle.json',
}


loop: Optional['Game'] = None
