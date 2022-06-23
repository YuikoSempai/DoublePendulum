import pygame
from Constants import *


def paint():
    global phi1, phi2, phi_der2, phi_der1
    screen.fill(BLACK)
    phi1, phi_der1, phi2, phi_der2 = calculate_next_phis(phi1, phi_der1, function1, phi2, phi_der2, function2, dx)
    x1, y1, x2, y2 = calculate_next_coordinates(phi1, phi2)
    pygame.draw.line(screen, RED, (point_x, point_y), (x1, y1), width=2*int(max(1, M1//10)))
    pygame.draw.line(screen, BLUE, (x1, y1), (x2, y2), width=2*int(max(1, M2//10)))
    pygame.draw.circle(screen, BLUE, (x2, y2), M2*2)
    pygame.draw.circle(screen, RED, (x1, y1), M1*2)
    pygame.display.flip()


def function1(phi1, phi_der1, phi2, phi_der2):
    first = -M2/(M1 + M2*math.sin(phi1 - phi2)**2)
    second = math.sin(phi1 - phi2) * (phi_der1**2 * math.cos(phi1 - phi2) + L2/L1*phi_der2**2)
    third = -g/L1 * (math.sin(phi2)*math.cos(phi1 - phi2) - (M2 + M1)/M2*math.sin(phi1))
    return first*(second - third)


def function2(phi1, phi_der1, phi2, phi_der2):
    first = (M1 + M2)/(M1 + M2*math.sin(phi1 - phi2)**2)
    second = math.sin(phi1 - phi2) * (M2/(M2 + M1) * phi_der2**2 * math.cos(phi1 - phi2) + L1/L2*phi_der1 ** 2)
    third = -g/L2*(math.sin(phi1) * math.cos(phi1 - phi2) - math.sin(phi2))
    return first * (second + third)


def calculate_next_phis(cur_phi, cur_phi_der, func1, cur_phi2, cur_der_phi2, func2, delta_x):
    phi_der = cur_phi_der
    phi = cur_phi
    phi3 = cur_phi2
    phi_der3 = cur_der_phi2
    for i in range(25):
        phi_der = phi_der + func1(phi, phi_der, phi3, phi_der3) * delta_x / 2
        phi = phi + phi_der * delta_x
        phi_der3 = phi_der3 + func2(phi, phi_der, phi3, phi_der3) * delta_x / 2
        phi3 = phi3 + phi_der3 * delta_x
    return phi, phi_der, phi3, phi_der3


def calculate_next_coordinates(phi, phi3):
    x1 = point_x + 100*L1 * math.sin(phi)
    y1 = point_y - 100*L1 * math.cos(phi)
    x2 = x1 + 100*L2 * math.sin(phi3)
    y2 = y1 - 100*L2 * math.cos(phi3)
    return x1, y1, x2, y2


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Double pendulum")
clock = pygame.time.Clock()
phi1 = math.pi - math.pi/2
phi_der1 = 0
phi2 = math.pi - math.pi/4
phi_der2 = 0

running = True
while running:
    for event in pygame.event.get():
        # проверить закрытие окна
        if event.type == pygame.QUIT:
            running = False
    paint()
    clock.tick(FPS)
