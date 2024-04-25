#https://codereview.stackexchange.com/questions/281398/solar-system-simulation-with-real-values-in-pygame 

import sys
import contextlib
with contextlib.redirect_stdout(None):
    import pygame
from pygame.locals import *
from pygame.math import Vector2, Vector3
import math
from astroquery.jplhorizons import Horizons
from astropy.time import Time
import numpy as np
import warnings

warnings.simplefilter('ignore', UserWarning)

pygame.display.init()
pygame.font.init()

win = pygame.display.set_mode((750, 500), RESIZABLE)
pygame.display.set_caption("Solar System 2.0")
clock = pygame.time.Clock()

WIDTH, HEIGHT = pygame.display.get_surface().get_size()
FONT = pygame.font.SysFont("Tahoma", 16)
LARGE_FONT = pygame.font.SysFont("Tahoma", 26)

AU = 1.496e8 * 1000 # km to m
G = 6.67428e-11
SCALE = 15 / AU
TIME_STEP = 3600 * 24 * 1 # 1 day
WIN_CENTER = Vector2(WIDTH // 2, HEIGHT // 2)

BLACK = "#000000"
DARK_GREY = "#5A5A5A"
WHITE = "#FFFFFF"
PEARL_WHITE = "#E2DFD2"
YELLOW = "#FFFF00"
BLUE = "#0000FF"
RED = "#FF0000"
ORANGE = "#FFA500"
BROWN = "#964B00"
YELLOWISH_BROWN = "#9B7A01"
CYAN = "#00FFFF"
GREEN = '#1ee635'

def convert_to_win_pos(pos):
    "Converts a position in the real universe to window coordinates"
    # X increases towards right in pygame window
    # -pos[1] because Y increases downards in pygame window
    return WIN_CENTER + (pos[0] * SCALE, -pos[1] * SCALE)

def convert_to_real_pos(pos):
    "Converts a position on the window to real universe coordinates"
    real_pos = Vector2(pos) - WIN_CENTER
    real_pos.x /= SCALE
    real_pos.y /= -SCALE # -SCALE because Y increases downards in pygame window
    return real_pos

class Planet:
    def __init__(self, name, pos, color, mass, radius, orbital_period, vel):
        self.name = name
        self.pos = pos
        self.color = color
        self.mass = mass
        self.radius = radius
        self.x_vel = vel[0]
        self.y_vel = vel[1]
        self.z_vel = vel[2]
        self.x_vel_h = 0
        self.y_vel_h = 0
        self.z_vel_h = 0
        self.orbital_period = orbital_period
        self.orbit_counter = 0
        self.orbit = []

    def render(self, win):
        "Render the planet and orbit on the window."
        # Rendering orbit...
        if len(self.orbit) > 1:
            scaled_points = []
            for x, y, z in self.orbit:
                scaled_points.append(convert_to_win_pos((x, y)))
            pygame.draw.lines(win, self.color, False, scaled_points, 2)

        # Rendering planet...
        pygame.draw.circle(
            win,
            self.color,
            convert_to_win_pos(self.pos),
            self.radius*SCALE*AU/100
        )

    def render_info(self, win, sun):
        "Renders information about the planet."
        # Information text labels...
        distance_from_sun = self.pos.distance_to(sun.pos)
        name_text = FONT.render(f"Name: {self.name}", 1, self.color)
        mass_text = FONT.render(f"Mass: {self.mass}", 1, self.color)
        orbital_period_text = FONT.render(f"Orbital period: {self.orbital_period} days", 1, self.color)
        distance_text = FONT.render(f"Distance from sun: {round(distance_from_sun):,}km", 1, self.color)
        vel_text = FONT.render(f"Velocity: {round(np.sqrt(self.x_vel**2+self.y_vel**2) / 1000, 2):,} km/s", 1, self.color)

        # Rendering the labels...
        alignment = max(
            name_text.get_width(), mass_text.get_width(),
            orbital_period_text.get_width(), 
            distance_text.get_width(), vel_text.get_width()
        ) + 15
        win.blit(name_text, (WIDTH - alignment, 15))
        win.blit(mass_text, (WIDTH - alignment, 35))
        win.blit(orbital_period_text, (WIDTH - alignment, 55))
        win.blit(distance_text, (WIDTH - alignment, 75))
        win.blit(vel_text, (WIDTH - alignment, 95))

        # Rendering line joining planet and sun
        planet_pos = convert_to_win_pos(self.pos)
        sun_pos = convert_to_win_pos(sun.pos)
        pygame.draw.line(win, self.color, planet_pos, sun_pos, 1)

    def update_position(self, planets):
        "Updates the position considering gravity of other planets"
        total_force_x = total_force_y = total_force_z = 0
        for planet in planets:
            if planet == self:
                continue
            force_x, force_y, force_z = self.gravity(planet)
            total_force_x += force_x
            total_force_y += force_y
            total_force_z += force_z
        
        self.x_vel_h = self.x_vel+0.5*(total_force_x / self.mass) * TIME_STEP
        self.y_vel_h = self.y_vel+0.5*(total_force_y / self.mass) * TIME_STEP
        self.z_vel_h = self.z_vel+0.5*(total_force_z / self.mass) * TIME_STEP

        # F = ma, a = F / m
        self.pos.x = self.pos.x + self.x_vel_h * TIME_STEP 
        self.pos.y = self.pos.y + self.y_vel_h * TIME_STEP 
        self.pos.z = self.pos.z + self.z_vel_h * TIME_STEP 

        total_force_x2 = total_force_y2 = total_force_z2 = 0
        for planet in planets:
            if planet == self:
                continue
            force_x2, force_y2, force_z2 = self.gravity(planet)
            total_force_x2 += force_x2
            total_force_y2 += force_y2
            total_force_z2 += force_z2

        self.x_vel = self.x_vel_h + 0.5*(total_force_x2 / self.mass) * TIME_STEP
        self.y_vel = self.y_vel_h + 0.5*(total_force_y2 / self.mass) * TIME_STEP
        self.z_vel = self.z_vel_h + 0.5*(total_force_z2 / self.mass) * TIME_STEP

        if self.name == "Sun": # Do not render orbit for sun
            return
        
        point_dist = self.orbital_period // 80
        self.orbit_counter += 1
        if self.orbit_counter >= point_dist:
            self.orbit_counter = 0
            self.orbit.append([*self.pos])
            if len(self.orbit) > (self.orbital_period / point_dist) + 1:
                del self.orbit[0]


    def gravity(self, other):
        distance_x = other.pos.x - self.pos.x
        distance_y = other.pos.y - self.pos.y
        distance_z = other.pos.z - self.pos.z
        distance = math.sqrt(distance_x**2  + distance_y**2 + distance_z**2)
        # F = GMm/d^2
        force = G * self.mass * other.mass / distance**2
        x_angle = math.acos(distance_x/ distance)
        y_angle = math.acos(distance_y/ distance)
        z_angle = math.acos(distance_z/ distance)
        
        force_x = force * math.cos(x_angle)
        force_y = force * math.cos(y_angle)
        force_z = force * math.cos(z_angle)
        return force_x, force_y, force_z

class exp_Planet:
    def __init__(self, name, color, orbital_period, t0, id, radius):
        self.name = name
        self.lpos = Horizons(id=id, location="@sun", epochs={'start': t0,
                        'stop': '2024-04-21',
                        'step': '1d'}, id_type=None).vectors()
        self.color = color
        self.t = Time(sim_start_date).jd
        self.radius = radius
        self.orbital_period = orbital_period
        self.orbit_counter = 0
        self.exp_orbit = []
        

    def render(self, win):
        "Render the planet and orbit on the window."
        # Rendering orbit...
        if len(self.exp_orbit) > 1:
            scaled_points = []
            for x, y, z in self.exp_orbit:
                scaled_points.append(convert_to_win_pos((x, y)))
            pygame.draw.lines(win, self.color, False, scaled_points, 1)

        # Rendering planet...
        pygame.draw.circle(
            win,
            self.color,
            convert_to_win_pos(self.pos),
            self.radius*SCALE*AU/100
        )

    def exp_planet(self, i):
        xi = [np.double(self.lpos[i][xi]) for xi in ['x', 'y', 'z']]
        self.pos = Vector3(xi[0]*1.496e11, xi[1]*1.496e11, xi[2]*1.496e11)
        vxi = [np.double(self.lpos[i][xi]) for xi in ['vx', 'vy', 'vz']]
        self.Vv = Vector3(vxi[0]*1.496e11/(3600*24), vxi[1]*1.496e11/(3600*24), vxi[2]*1.496e11/(3600*24)).magnitude()
        self.exp_orbit.append(self.pos)
        self.tt = Time(self.t, format='jd', out_subfmt='str').iso[:-13]
        self.t += 1
        self.render(win)

    

sim_start_date = "1846-08-31"
time = Time(sim_start_date).jd
def get_pos(id):
    pos = Horizons(id=id, location="@sun", epochs=time, id_type=None).vectors()
    xi = [np.double(pos[xi]) for xi in ['x', 'y', 'z']]
    vxi = [np.double(pos[xi]) for xi in ['vx', 'vy', 'vz']]
    Vx = Vector3(xi[0]*1.496e11, xi[1]*1.496e11, xi[2]*1.496e11)
    Vvx = Vector3(vxi[0]*1.496e11/(3600*24), vxi[1]*1.496e11/(3600*24), vxi[2]*1.496e11/(3600*24))
    return Vx, Vvx


sun = Planet("Sun", Vector3(0, 0, 0), YELLOW, 1.9891e30, 22, 0, (0,0,0))
mercury = Planet(
    "Mercury", get_pos('1')[0],
    DARK_GREY, 3.30e23, 7.5, 88, get_pos('1')[1]
)
venus = Planet(
    "Venus", get_pos('2')[0],
    PEARL_WHITE, 4.87e24, 8.5, 224.7, get_pos('2')[1]
)
earth = Planet(
    "Earth", get_pos('3')[0],
    BLUE, 5.97e24, 9, 365.2, get_pos('3')[1]
)
mars = Planet(
    "Mars", get_pos('4')[0],
    RED, 6.42e23, 8.75, 687, get_pos('4')[1]
)
jupiter = Planet(
    "Jupiter", get_pos('5')[0],
    BROWN, 1.898e27, 18, 4331, get_pos('5')[1]
)
saturn = Planet(
    "Saturn", get_pos('6')[0],
    YELLOWISH_BROWN, 5.68e26, 16, 10747, get_pos('6')[1]
)
uranus = Planet(
    "Uranus", get_pos('7')[0],
    CYAN, 8.68e25, 14, 30589, get_pos('7')[1]
)
neptune = Planet(
    "Neptune", get_pos('8')[0],
    BLUE, 1.02e26, 12, 59800, get_pos('8')[1]
)

exp_uranus = exp_Planet("exp_Uranus",
    GREEN, 30589, sim_start_date, '7', 14
)


run = True
drag = False
drag_start = None
liste_delta = {}

def render_win_info():
    "Renders window related info such as x-pos, y-pos, scale, fps and timestep..."
    x, y = convert_to_real_pos(pygame.mouse.get_pos())
    x_text = FONT.render(f"Position - x: {round(x):,}km", 1, WHITE)
    y_text = FONT.render(f"Position - y: {round(y):,}km", 1, WHITE)
    scale_text = FONT.render(f"Scale: 1-(x, y): {round(1 / SCALE):,}km", 1, WHITE)
    timestep_text = FONT.render(f"Timestep: {TIME_STEP / (3600 * 24)} days", 1, WHITE)
    fps_text = FONT.render(f"FPS: {int(clock.get_fps())}", 1, WHITE)
    win.blit(fps_text, (15, 15))
    win.blit(x_text, (15, 35))
    win.blit(y_text, (15, 55))
    win.blit(scale_text, (15, 75))
    win.blit(timestep_text, (15, 95))


    distance_from_sun = exp_uranus.pos.distance_to(sun.pos)
    name_text = FONT.render(f"Name: {exp_uranus.name}", 1, exp_uranus.color)
    distance_text = FONT.render(f"Distance from sun: {round(distance_from_sun):,}km", 1, exp_uranus.color)
    vel_text = FONT.render(f"Velocity: {round(exp_uranus.Vv/ 1000, 2):,} km/s", 1, exp_uranus.color)
    date_text = FONT.render(f"Date: {exp_uranus.tt}", 1, exp_uranus.color)

    with open(path+file_name+extension, "a") as output:
        output.write(str((exp_uranus.pos-uranus.pos)[0])+','+str((exp_uranus.pos-uranus.pos)[1])+','+str((exp_uranus.pos-uranus.pos)[2])+'\n')

    delta_text = FONT.render("Delta_x= {:.2e}, Delta_y= {:.2e}".format((exp_uranus.pos-uranus.pos)[0], (exp_uranus.pos-uranus.pos)[1]), 1, exp_uranus.color)
    win.blit(name_text, (15, 380))
    win.blit(distance_text, (15, 400))
    win.blit(vel_text, (15, 420))
    win.blit(date_text, (15, 440))
    win.blit(delta_text, (15, 460))


planets = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus]
#planets = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]
selected_planet = uranus
path = 'projet\\'
file_name = 'temp'
extension = '.txt'
with open(path+file_name+extension, "w") as output:
    output.write('')
i = 1
for _ in range(4000):
#while run:
    clock.tick(100)
    win.fill(BLACK)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                drag = True
                drag_start = pygame.mouse.get_pos()
                for planet in planets:
                    planet_pos = convert_to_win_pos(planet.pos)
                    if planet_pos.distance_to(pygame.mouse.get_pos()) < planet.radius * 2:
                        selected_planet = planet
                        break
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                drag = False
                drag_start = None
        elif event.type == MOUSEMOTION:
            if drag:
                WIN_CENTER += Vector2(pygame.mouse.get_pos()) - drag_start
                drag_start = pygame.mouse.get_pos()
        elif event.type == VIDEORESIZE:
            WIDTH, HEIGHT = pygame.display.get_surface().get_size()
        elif event.type == MOUSEWHEEL:
            if event.y == 1:
                SCALE += 5/AU # Zoom in
            if event.y == -1:
                SCALE -= 5/AU # Zoom out
                if SCALE <= 0:
                    SCALE += 5/AU

    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[K_UP]:
        SCALE += 1/AU # Zoom in
    if keys_pressed[K_DOWN]:
        SCALE -= 1/AU # Zoom out
        if SCALE <= 0:
            SCALE += 5/AU

    exp_uranus.exp_planet(i)
    for planet in planets:
        planet.update_position(planets)
        planet.render(win)

    i += 1
    selected_planet.render_info(win, sun)
    render_win_info()
    pygame.display.update()
