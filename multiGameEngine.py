import numpy as np
from gameEngine import GameEngine, AROUND_RAD, AGENT_INPUT_SIZE, VISION_SIZE
from util import Actions

EPSILON = 1e-5

SECONDS_PER_TICK = 0.3

GROUND_SPEED = 1.5
AIR_SPEED = 0.8
GRAVITY = -3
JUMP_FORCE = 3.4 #4
ACCELERATION_FORCE = 1.0 #0.2

PLAYER_WIDTH = 0.2

LEFT = Actions.LEFT.value
RIGHT = Actions.RIGHT.value
JUMP = Actions.JUMP.value
OTHER = -1

def ifloor(x):
    return np.array(np.floor(x), dtype="int")

def iceil(x):
    return np.array(np.ceil(x), dtype="int")

class MultiGameEngine:
    def __init__(self, levels):
        levels = np.array(levels)
        self.n_games = levels.shape[0]

        self.level_heights = levels[:,:,0]
        self.level_bads = levels[:,:,1]

        self.players_x = np.zeros((self.n_games, ))
        self.players_y = np.array(self.level_heights[:,0], dtype="float")

        self.players_vx = np.zeros((self.n_games, ))
        self.players_vy = np.zeros((self.n_games, ))

        self.players_on_ground = np.ones((self.n_games, ), dtype="bool")

    def performTick(self, actions, timeStep=SECONDS_PER_TICK):
        last_xs = np.array(self.players_x)

        self.movePlayers(actions, timeStep)

        reward = self.players_x - last_xs

        inds = ifloor(self.players_x)
        inds %= self.level_heights.shape[1]
        bads = self.level_bads[np.arange(self.n_games), inds]

        is_on_bad = bads & self.players_on_ground

        reward -= is_on_bad * SECONDS_PER_TICK

        agentInput = self.getAgentInputs()

        return (agentInput, reward)

    def movePlayers(self, actions, timeStep=SECONDS_PER_TICK):
        actions = np.array([
                 LEFT if action == Actions.LEFT
            else RIGHT if action == Actions.RIGHT
            else JUMP if action == Actions.JUMP
            else OTHER
            for action in actions
        ])

        # Update player based on action
        current_speeds = np.where(self.players_on_ground, GROUND_SPEED, AIR_SPEED)

        vx_left = np.maximum(self.players_vx - ACCELERATION_FORCE * timeStep, -current_speeds)
        self.players_vx = np.where(actions == LEFT, vx_left, self.players_vx)

        vx_right = np.minimum(self.players_vx + ACCELERATION_FORCE * timeStep, current_speeds)
        self.players_vx = np.where(actions == RIGHT, vx_right, self.players_vx)

        vy_jump = JUMP_FORCE * np.ones((self.n_games, ))
        self.players_vy = np.where(
            (actions == JUMP) & self.players_on_ground,
            vy_jump,
            self.players_vy + GRAVITY * timeStep
        )

        dx = self.players_vx * timeStep
        dy = self.players_vy * timeStep

        self.players_on_ground = np.zeros((self.n_games, ), dtype="bool")

        # Check collision with floor
        for offset in [0, PLAYER_WIDTH]:
            at_x = self.players_x + offset
            inds = ifloor(at_x)
            inds %= self.level_heights.shape[1]

            heights = self.level_heights[np.arange(self.n_games), inds]
            dists_left_down = self.players_y - heights
            ends_up_under = dists_left_down < -dy

            dy = np.where(ends_up_under, np.zeros_like(dy), dy)
            self.players_vy = np.where(ends_up_under, np.zeros_like(self.players_vy), self.players_vy)
            self.players_y = np.where(ends_up_under, self.players_y - dists_left_down, self.players_y)

            self.players_on_ground |= ends_up_under

        # Check for collisions between the bottom right corner and the next block's left edge
        v_slopes = np.divide(
            dy,
            dx,
            out=np.zeros((self.n_games, )),
            where=dx != 0 # Don't divide by zero!
        )

        inds = iceil(self.players_x)
        inds %= self.level_heights.shape[1]
        heights = self.level_heights[np.arange(self.n_games), inds]
        dists_left_to_block = 1 - self.players_x % 1 - PLAYER_WIDTH

        in_range = (0 < dists_left_to_block) & (dists_left_to_block < dx)
        height_at_pass = self.players_y + v_slopes * dists_left_to_block
        collisions = (height_at_pass < heights) & in_range

        dx = np.where(collisions, np.zeros_like(dx), dx)
        self.players_vx = np.where(collisions, np.zeros_like(self.players_vx), self.players_vx)
        self.players_x = np.where(collisions, self.players_x + dists_left_to_block - EPSILON, self.players_x)

        # Check for collisions between the bottom left corner and the previous block's right edge
        inds = ifloor(self.players_x - 1)
        inds %= self.level_heights.shape[1]
        heights = self.level_heights[np.arange(self.n_games), inds]
        dists_left_to_block = self.players_x % 1

        in_range = (0 < dists_left_to_block) & (dists_left_to_block < -dx)
        height_at_pass = self.players_y - v_slopes * dists_left_to_block
        collisions = (height_at_pass < heights) & in_range

        dx = np.where(collisions, np.zeros_like(dx), dx)
        self.players_vx = np.where(collisions, np.zeros_like(self.players_vx), self.players_vx)
        self.players_x = np.where(collisions, self.players_x - dists_left_to_block + EPSILON, self.players_x)

        self.players_x += dx
        self.players_y += dy


    def getAgentInputs(self):
        delta_range = np.arange(-AROUND_RAD, AROUND_RAD + 1)

        dx, dy = np.meshgrid(delta_range, delta_range)

        dxs = np.broadcast_to(dx, (self.n_games, VISION_SIZE, VISION_SIZE))
        dys = np.broadcast_to(dy, (self.n_games, VISION_SIZE, VISION_SIZE))

        xs = dxs + np.repeat(self.players_x, VISION_SIZE * VISION_SIZE).reshape(dxs.shape)
        ys = dys + np.repeat(self.players_y, VISION_SIZE * VISION_SIZE).reshape(dys.shape)

        vision = np.zeros(ys.shape)

        inds = np.repeat(np.arange(self.n_games), VISION_SIZE * VISION_SIZE).reshape(dxs.shape)

        for yCorner in (0, 1):
            for xCorner in (0, 1):
                yCoords = ys + yCorner
                xCoords = xs + xCorner
                xCoordsI = ifloor(xCoords) % self.level_heights.shape[1]

                if xCorner:
                    xMul = self.players_x % 1
                else:
                    xMul = 1 - (self.players_x % 1)

                if yCorner:
                    yMul = self.players_y % 1
                else:
                    yMul = 1 - (self.players_y % 1)

                xMul = np.broadcast_to(xMul, (VISION_SIZE, VISION_SIZE, self.n_games)).T
                yMul = np.broadcast_to(yMul, (VISION_SIZE, VISION_SIZE, self.n_games)).T

                heights = self.level_heights[inds.flatten(), xCoordsI.flatten()]
                heights = heights.reshape(xs.shape)

                vision_here = np.array(yCoords < heights, dtype="float")

                vision += vision_here * xMul * yMul

        vels = np.concatenate(
            (self.players_vx.reshape(-1, 1), self.players_vy.reshape(-1, 1)),
            axis=1
        )

        agent_input = vision.reshape((self.n_games, -1))
        agent_input = np.concatenate((agent_input, vels), axis=1)

        return agent_input

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
        [[(0, 0), (1, 0), (0, 0), (0, 0), (1, 0), (0, 0), (0, 0), (1, 0), (0, 0), (0, 0), (1, 0), (0, 0)] for _ in range(3)]
    )

    # mge.performTick([Actions.NONE, Actions.RIGHT, Actions.RIGHT])

    mge.players_x[0] = 0.79
    mge.players_y[0] = 0.8
    mge.players_vx[0] = 0.2

    print(mge)
    mge.performTick([Actions.RIGHT, Actions.RIGHT, Actions.JUMP])
    print(mge)

    print(mge.getAgentInputs())
