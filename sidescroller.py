import game
import mover
import pygame

from pvector import PVector
from pygame.locals import *


class Sprite(mover.Mover):

    """Extends the Mover to also have an image, so it becomes a sprite"""

    def __init__(self, x, y, image_path=""):
        super(Sprite, self).__init__(x, y)

        self.image = pygame.Surface([25, 25])
        self.image.fill(pygame.Color('blue'))

        self.movingleft = False
        self.movingright = False
        self.jumping = False

        self.acc_force_val = 1.5
        self.fri_force_val = .25
        self.grv_force_val = .2
        self.dec_force_val = 3
        self.jmp_force_val = 10
        self.jmp_force_val_end = 4
        self.acc_force = PVector(self.acc_force_val, 0)
        self.dec_force = PVector(self.dec_force_val, 0)
        self.max_velo = 6

    def update(self):
        # Update the position of the Sprite
        self.doWalking()

        # Temporary to keep the sprite from falling through the bottom
        if self.location.y > 300:
            self.location.y = 300

        # TODO: delete
        print(self.velocity, self.acceleration)

    def doWalking(self):
        # If we are walking in the same direction as the keyboard input
        # apply more force, but only if the maximal velocity is not already
        # reached.
        # If we are walking in the opp. direction as the keyboard input
        # change the velocity directly to dec_force in the opp direction
        if self.movingright:
            if self.velocity.x >= 0:
                if self.velocity.x < self.max_velo:
                    self.applyForce(self.acc_force)
                else:
                    self.velocity.x = self.max_velo
            else:
                self.velocity.x = self.dec_force.x
        if self.movingleft:
            if self.velocity.x <= 0:
                if self.velocity.x > -self.max_velo:
                    self.applyForce(PVector.s_mult(self.acc_force, -1))
                else:
                    self.velocity.x = -self.max_velo
            else:
                self.velocity.x = -self.dec_force.x

        # If neither button is pressed apply friction. For small velocities
        # just set the velocity to zero.
        if not self.movingright and not self.movingleft:
            if abs(self.velocity.x) < self.fri_force_val:
                self.velocity.x = 0
            elif self.velocity.x > 0:
                self.velocity.x -= self.fri_force_val
            else:
                self.velocity.x += self.fri_force_val

        if not self.jumping:
            # If the jump button is released end the jump
            # => variable jump height
            if self.velocity.y < -self.jmp_force_val_end:
                self.velocity.y = -self.jmp_force_val_end
        # If gathering height, apply friction to slowly stop the jump
        if self.velocity.y < 0:
            self.velocity.y += self.fri_force_val

        # Apply normal gravity up to the point of maximal velocity
        if self.velocity.y + self.grv_force_val <= self.max_velo:
            self.velocity.y += self.grv_force_val

        # Apply the forces in the mover update function
        super(Sprite, self).update()

    def doJump(self):
        # Apply impuls to the player so he starts to jump.
        self.velocity.y = -self.jmp_force_val
        self.jumping = True

    def evnt_hndlr(self, event):
        # Handle left and right moving
        if event.type == KEYDOWN:
            if event.key == K_d:
                self.movingright = True
            if event.key == K_a:
                self.movingleft = True
        elif event.type == KEYUP:
            if event.key == K_d:
                self.movingright = False
            if event.key == K_a:
                self.movingleft = False

        # Handle jumping
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                self.doJump()
        if event.type == KEYUP:
            if event.key == K_SPACE:
                self.jumping = False

    def draw(self, surf):
        surf.blit(self.image, (self.location.x, self.location.y))


class SimpleWindow(game.Game):

    """Simple Window to display stuff"""

    def __init__(self):
        super(SimpleWindow, self).__init__()

        self.player = Sprite(230, 370)

    def update(self, delta):
        self.player.update()

    def evnt_hndlr(self, event):
        if event.type in [KEYDOWN, KEYUP]:
            if event.key in [K_a, K_d, K_SPACE]:
                self.player.evnt_hndlr(event)

    def draw(self, surf):
        self.player.draw(surf)

if __name__ == '__main__':
    simpleWindow = SimpleWindow()
    simpleWindow.run()
