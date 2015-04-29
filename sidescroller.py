import game
import mover
import pygame

from pvector import PVector
from pygame.locals import *


class AnimationController(object):

    """Handles the animations of the character, therefore we need the sprite
    that is linked to this animation controller. Maybe other inputs?"""

    def __init__(self, arg):
        super(AnimationController, self).__init__()
        self.arg = arg


class Collider(pygame.sprite.Sprite):

    """docstring for Collider"""

    def __init__(self, sprite, width, height, xoff=0, yoff=0, color='green'):
        super(Collider, self).__init__()

        self.sprite = sprite
        self.xoff = xoff
        self.yoff = yoff

        self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect()
        self.image.fill(pygame.Color(color))

    def update(self):
        self.rect.centerx = self.sprite.location.x + self.xoff
        self.rect.centerx += self.sprite.width / 2
        self.rect.centery = self.sprite.location.y + self.yoff
        self.rect.centery += self.sprite.height / 2

    def draw(self, surf):
        surf.blit(self.image, (self.rect.x, self.rect.y))


class Sprite(mover.Mover):

    """Extends the Mover to also have an image, so it becomes a sprite"""

    def __init__(self, x, y, image_path=""):
        super(Sprite, self).__init__(x, y)

        # Placeholder for an image for the character
        # TODO: Replace this with an animation object that returns an image
        #       every frame
        self.width = 32
        self.height = 42
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(pygame.Color('cyan'))

        # Collider
        self.collider_t = Collider(self, 10, 10, xoff=0, yoff=-25)
        self.collider_b = Collider(self, 10, 10,
                                   xoff=0, yoff=25, color='blue')
        self.collider_rt = Collider(self, 10, 10,
                                    xoff=20, yoff=-15, color='red')
        self.collider_rb = Collider(self, 10, 10,
                                    xoff=20, yoff=15, color='red')
        self.collider_lt = Collider(self, 10, 10,
                                    xoff=-20, yoff=-15, color='yellow')
        self.collider_lb = Collider(self, 10, 10,
                                    xoff=-20, yoff=15, color='yellow')
        self.colliders = [self.collider_t, self.collider_b,
                          self.collider_rt, self.collider_rb,
                          self.collider_lt, self.collider_lb]

        # Possible states of the character.
        self.movingleft = False
        self.movingright = False
        self.jumping = False

        # Constant values that determine the movement of the character
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

        # Update the collider position
        for c in self.colliders:
            c.update()

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
        # Draw the player image
        # TODO: Does this change after implementation of animation controller?
        surf.blit(self.image, (self.location.x, self.location.y))

        # Draw the collider(s)
        for c in self.colliders:
            c.draw(surf)


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
