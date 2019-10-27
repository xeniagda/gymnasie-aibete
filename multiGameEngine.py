import numpy as np
from gameEngine import GameEngine
from util import Actions

EPSILON = 1e-5

SECONDS_PER_TICK = 0.3

GROUND_SPEED = 2.0
AIR_SPEED = 1.2
GRAVITY = -3
JUMP_FORCE = 4

PLAYER_WIDTH = 0.2

LEFT = Actions.LEFT.value
RIGHT = Actions.RIGHT.value
JUMP = Actions.JUMP.value
OTHER = -1

DEBUG = False

class MultiGameEngine:
    def __init__(self, levels):
        levels = np.array(levels)
        self.n_games = levels.shape[0]

        self.level_heights = levels[:,:,0]
        self.level_bads = levels[:,:,1]

        self.players_x = np.zeros((self.n_games, ))
        self.players_y = 5 + np.array(self.level_heights[:,0], dtype="float")

        self.players_vx = np.zeros((self.n_games, ))
        self.players_vy = np.zeros((self.n_games, ))

        self.players_on_ground = np.ones((self.n_games, ), dtype="bool")

    def performTick(self, actions, timeStep=SECONDS_PER_TICK):
        actions = np.array([
                 LEFT if action == Actions.LEFT
            else RIGHT if action == Actions.RIGHT
            else JUMP if action == Actions.JUMP
            else OTHER
            for action in actions
        ])

        # Update player based on action
        current_speeds = np.where(self.players_on_ground, GROUND_SPEED, AIR_SPEED)

        vx_left = np.maximum(self.players_vx - 0.2 * timeStep, -current_speeds)
        self.players_vx = np.where(actions == LEFT, vx_left, self.players_vx)

        vx_right = np.minimum(self.players_vx + 0.2 * timeStep, current_speeds)
        self.players_vx = np.where(actions == RIGHT, vx_right, self.players_vx)

        vy_jump = JUMP_FORCE * np.ones((self.n_games, ))
        self.players_vy = np.where(
            (actions == JUMP) & self.players_on_ground,
            vy_jump,
            self.players_vy + GRAVITY * timeStep / 2
        )

        dx = self.players_vx * timeStep
        dy = self.players_vy * timeStep

        v_slopes = np.divide(
            dy,
            dx,
            out=np.zeros((self.n_games, )),
            where=dx != 0 # Don't divide by zero!
        )

        collisions_horiz = np.zeros((self.n_games, ), dtype="bool")
        # Check collision with floor
        for offset in [0, PLAYER_WIDTH]:
            at_x = self.players_x + offset
            inds = np.array(at_x, dtype="int")

            heights = self.level_heights[np.arange(self.n_games), inds]

            dist_left_down = self.players_y - heights

            ends_up_under = (dist_left_down < -dy)

            dxs = np.divide(
                dist_left_down,
                v_slopes,
                out=np.zeros((self.n_games, )),
                where=v_slopes != 0,
            )
            coll_res_x = self.players_x + dxs
            coll_res_y = heights

            self.players_x = np.where(ends_up_under, coll_res_x, self.players_x)
            self.players_y = np.where(ends_up_under, coll_res_y, self.players_y) + EPSILON
            self.players_vy = np.where(ends_up_under, np.zeros((self.n_games, )), self.players_vy)
            dy = np.where(ends_up_under, np.zeros((self.n_games, )), dy)

            collisions_horiz |= ends_up_under

        # Check for collisions between the bottom right corner and the next block's left edge

        v_slopes = np.divide(
            dy,
            dx,
            out=np.zeros((self.n_games, )),
            where=dx != 0 # Don't divide by zero!
        )

        inds = np.array(np.ceil(self.players_x), dtype="int")
        heights = self.level_heights[np.arange(self.n_games), inds]

        dists_left_to_block = 1 - self.players_x % 1 - PLAYER_WIDTH


        in_range = (0 < dists_left_to_block) & (dists_left_to_block < dx)

        dys = v_slopes * dists_left_to_block
        rys = self.players_y + dys

        collisions_vert = (rys < heights) & in_range

        coll_res_x = self.players_x + dists_left_to_block - EPSILON
        coll_res_y = self.players_y + v_slopes * dists_left_to_block

        self.players_x = np.where(collisions_vert, coll_res_x, self.players_x)
        self.players_y = np.where(collisions_vert, coll_res_y, self.players_y)
        self.players_vx = np.where(collisions_vert, np.zeros((self.n_games, )), self.players_vx)
        dx = np.where(collisions_vert, np.zeros((self.n_games, )), dx)

        # Check for collisions between the bottom left corner and the previous block's right edge

        v_slopes = np.divide(
            dy,
            dx,
            out=np.zeros((self.n_games, )),
            where=dx != 0 # Don't divide by zero!
        )

        inds = np.array(self.players_x - 1, dtype="int")
        heights = self.level_heights[np.arange(self.n_games), inds]

        dists_left_to_block = self.players_x % 1

        in_range = (0 < dists_left_to_block) & (dists_left_to_block < -dx)

        dys = -v_slopes * dists_left_to_block
        rys = self.players_y + dys

        collisions_vert = (rys < heights) & in_range

        coll_res_x = self.players_x - dists_left_to_block + EPSILON
        coll_res_y = self.players_y - v_slopes * dists_left_to_block

        self.players_x = np.where(collisions_vert, coll_res_x, self.players_x)
        self.players_y = np.where(collisions_vert, coll_res_y, self.players_y)
        self.players_vx = np.where(collisions_vert, np.zeros((self.n_games, )), self.players_vx)
        dx = np.where(collisions_vert, np.zeros((self.n_games, )), dx)


        self.players_x += dx
        self.players_y += dy

        self.players_on_ground = collisions_horiz

        self.players_vy = self.players_vy + GRAVITY * timeStep / 2


    def into_regular_engine(self, index, ui):
        lvl = list(zip(self.level_heights[index], self.level_bads[index]))
        ge = GameEngine(ui, lvl)

        ge.player.x = self.players_x[index]
        ge.player.y = self.players_y[index]
        ge.player.vx = self.players_vx[index]
        ge.player.vy = self.players_vy[index]
        ge.player.width = PLAYER_WIDTH

        return ge

    def __str__(self):
        return """MGE(
    level_heights=
        {},
    level_bads=
        {},
    px={},
    py={},
    pvx={},
    pvy={},
)""".format(
            np.array2string(self.level_heights, prefix="        "),
            np.array2string(self.level_bads, prefix="        "),
            self.players_x,
            self.players_y,
            self.players_vx,
            self.players_vy,
        )

if __name__ == "__main__":

    mge = MultiGameEngine(
        [[(0, 0), (1, 0), (0, 0)] for _ in range(3)]
    )

    # mge.performTick([Actions.NONE, Actions.RIGHT, Actions.RIGHT])

    mge.players_x[2] = 0.79
    mge.players_y[2] = 0.8
    mge.players_vx[2] = 0.2

    print(mge)
    mge.performTick([Actions.RIGHT, Actions.RIGHT, Actions.JUMP])
    print(mge)
