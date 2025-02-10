import pygame
import random
import json
import os
import sys
import main_menu
from classes import *
from tools import *
from params import *

pygame.init()
# Инициализация модуля шрифтов
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.font.init()

main_menu.main(screen)

pygame.quit()
