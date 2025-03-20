import pygame
import sys
import math

# Inicialización de Pygame
pygame.init()

# Constantes
WIDTH, HEIGHT = 800, 600
TOWER_WIDTH = 20
DISK_HEIGHT = 30
BASE_HEIGHT = 20
TOWER_COLOR = (139, 69, 19)  # Marrón
BASE_COLOR = (139, 69, 19)   # Marrón
BACKGROUND_COLOR = (230, 230, 230)  # Gris claro
TEXT_COLOR = (0, 0, 0)  # Negro

# Colores para los discos
DISK_COLORS = [
    (255, 0, 0),      # Rojo
    (0, 0, 255),      # Azul
    (0, 255, 0),      # Verde
    (255, 255, 0),    # Amarillo
    (255, 0, 255),    # Magenta
    (0, 255, 255),    # Cian
    (255, 165, 0),    # Naranja
    (128, 0, 128)     # Púrpura
]

class Disk:
    def __init__(self, width, value):
        self.width = width
        self.value = value
        self.color = DISK_COLORS[value % len(DISK_COLORS)]
        self.rect = pygame.Rect(0, 0, width, DISK_HEIGHT)
        self.selected = False

class Tower:
    def __init__(self, x, y, height):
        self.x = x
        self.y = y
        self.height = height
        self.disks = []
        self.rect = pygame.Rect(x - TOWER_WIDTH // 2, y - height, TOWER_WIDTH, height)

    def add_disk(self, disk):
        # Posicionar el disco en la torre
        disk_y = self.y - BASE_HEIGHT - DISK_HEIGHT * (len(self.disks) + 1)
        disk.rect.midbottom = (self.x, disk_y)
        self.disks.append(disk)

    def remove_top_disk(self):
        if self.disks:
            return self.disks.pop()
        return None

    def can_add_disk(self, disk):
        if not self.disks:
            return True
        return disk.value < self.disks[-1].value

    def draw(self, screen):
        # Dibujar la base
        base_rect = pygame.Rect(self.x - 100, self.y - BASE_HEIGHT, 200, BASE_HEIGHT)
        pygame.draw.rect(screen, BASE_COLOR, base_rect)
        
        # Dibujar la torre
        pygame.draw.rect(screen, TOWER_COLOR, self.rect)
        
        # Dibujar los discos
        for disk in self.disks:
            pygame.draw.rect(screen, disk.color, disk.rect, border_radius=5)
            pygame.draw.rect(screen, (0, 0, 0), disk.rect, 2, border_radius=5)  # Borde negro

class Game:
    def __init__(self, num_disks=3):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Torres de Hanoi")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 24)
        self.big_font = pygame.font.SysFont('Arial', 36)
        self.reset_game(num_disks)

    def reset_game(self, num_disks):
        self.num_disks = num_disks
        self.moves = 0
        self.selected_disk = None
        self.game_won = False
        self.start_time = pygame.time.get_ticks()
        
        # Crear torres
        tower_height = (num_disks + 1) * DISK_HEIGHT + BASE_HEIGHT
        tower_y = HEIGHT - 100
        self.towers = [
            Tower(WIDTH // 4, tower_y, tower_height),
            Tower(WIDTH // 2, tower_y, tower_height),
            Tower(3 * WIDTH // 4, tower_y, tower_height)
        ]
        
        # Crear y colocar discos iniciales
        max_disk_width = 180
        width_step = max_disk_width / num_disks
        
        for i in range(num_disks, 0, -1):
            disk_width = width_step * i + 20  # Mínimo 20 de ancho
            disk = Disk(disk_width, i - 1)
            self.towers[0].add_disk(disk)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"
                elif event.key == pygame.K_r:
                    self.reset_game(self.num_disks)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_won:
                    return "menu"
                self.handle_mouse_click(event.pos)
        return "game"

    def handle_mouse_click(self, pos):
        # Verificar si se hizo clic en alguna torre
        for i, tower in enumerate(self.towers):
            tower_rect = pygame.Rect(tower.x - 100, tower.y - tower.height, 200, tower.height)
            if tower_rect.collidepoint(pos):
                # Si no hay disco seleccionado, intentar seleccionar uno
                if self.selected_disk is None:
                    if tower.disks:
                        self.selected_disk = (i, tower.remove_top_disk())
                # Si hay un disco seleccionado, intentar colocarlo
                else:
                    source_tower_idx, disk = self.selected_disk
                    # Verificar si se puede colocar el disco
                    if tower.can_add_disk(disk):
                        tower.add_disk(disk)
                        self.selected_disk = None
                        self.moves += 1
                        # Verificar si el juego ha terminado
                        if len(self.towers[2].disks) == self.num_disks:
                            self.game_won = True
                    else:
                        # Si no se puede colocar, devolverlo a la torre original
                        self.towers[source_tower_idx].add_disk(disk)
                        self.selected_disk = None
                break

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        
        # Dibujar torres
        for tower in self.towers:
            tower.draw(self.screen)
        
        # Dibujar disco seleccionado
        if self.selected_disk:
            _, disk = self.selected_disk
            pos = pygame.mouse.get_pos()
            disk.rect.center = pos
            pygame.draw.rect(self.screen, disk.color, disk.rect, border_radius=5)
            pygame.draw.rect(self.screen, (0, 0, 0), disk.rect, 2, border_radius=5)  # Borde negro
        
        # Mostrar número de movimientos
        moves_text = self.font.render(f"Movimientos: {self.moves}", True, TEXT_COLOR)
        self.screen.blit(moves_text, (20, 20))
        
        # Mostrar tiempo transcurrido
        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        time_text = self.font.render(f"Tiempo: {minutes:02d}:{seconds:02d}", True, TEXT_COLOR)
        self.screen.blit(time_text, (20, 60))
        
        # Mostrar movimientos mínimos necesarios
        min_moves = (2 ** self.num_disks) - 1
        min_moves_text = self.font.render(f"Movimientos mínimos: {min_moves}", True, TEXT_COLOR)
        self.screen.blit(min_moves_text, (WIDTH - min_moves_text.get_width() - 20, 20))
        
        # Mostrar mensaje de victoria
        if self.game_won:
            panel = pygame.Surface((500, 200), pygame.SRCALPHA)
            panel.fill((0, 0, 0, 180))
            self.screen.blit(panel, (WIDTH // 2 - 250, HEIGHT // 2 - 100))
            
            win_text = self.big_font.render("¡Has ganado!", True, (255, 255, 255))
            self.screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - 70))
            
            stats_text = self.font.render(f"Movimientos: {self.moves} | Mínimo: {min_moves}", True, (255, 255, 255))
            self.screen.blit(stats_text, (WIDTH // 2 - stats_text.get_width() // 2, HEIGHT // 2 - 20))
            
            time_text = self.font.render(f"Tiempo: {minutes:02d}:{seconds:02d}", True, (255, 255, 255))
            self.screen.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, HEIGHT // 2 + 20))
            
            continue_text = self.font.render("Haz clic para volver al menú", True, (255, 255, 255))
            self.screen.blit(continue_text, (WIDTH // 2 - continue_text.get_width() // 2, HEIGHT // 2 + 60))
        
        pygame.display.flip()

    def run(self):
        while True:
            state = self.handle_events()
            if state == "menu":
                return state
            self.draw()
            self.clock.tick(60)

class Menu:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Torres de Hanoi - Menú")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 36)
        self.small_font = pygame.font.SysFont('Arial', 24)
        
        # Botones para diferentes cantidades de discos
        button_width, button_height = 200, 60
        self.buttons = [
            {'rect': pygame.Rect(WIDTH // 2 - button_width // 2, 200, button_width, button_height),
             'text': '3 Discos', 'disks': 3},
            {'rect': pygame.Rect(WIDTH // 2 - button_width // 2, 280, button_width, button_height),
             'text': '5 Discos', 'disks': 5},
            {'rect': pygame.Rect(WIDTH // 2 - button_width // 2, 360, button_width, button_height),
             'text': '8 Discos', 'disks': 8}
        ]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Verificar si se hizo clic en algún botón
                for button in self.buttons:
                    if button['rect'].collidepoint(event.pos):
                        return button['disks']
        return None

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        
        # Dibujar título
        title = self.font.render("Torres de Hanoi", True, TEXT_COLOR)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
        
        # Dibujar instrucciones
        instructions = [
            "Selecciona la cantidad de discos para comenzar",
            "Objetivo: Mover todos los discos a la torre derecha",
            "Reglas: No colocar un disco grande sobre uno pequeño",
            "Controles: Clic para seleccionar/colocar discos",
            "ESC: Volver al menú | R: Reiniciar nivel"
        ]
        
        y_pos = 450
        for instruction in instructions:
            text = self.small_font.render(instruction, True, TEXT_COLOR)
            self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y_pos))
            y_pos += 30
        
        # Dibujar botones
        for button in self.buttons:
            # Verificar si el mouse está sobre el botón
            mouse_pos = pygame.mouse.get_pos()
            if button['rect'].collidepoint(mouse_pos):
                color = (100, 100, 255)  # Azul claro cuando el mouse está encima
            else:
                color = (150, 150, 255)  # Azul normal
                
            # Dibujar el botón
            pygame.draw.rect(self.screen, color, button['rect'], border_radius=10)
            pygame.draw.rect(self.screen, (0, 0, 0), button['rect'], 2, border_radius=10)  # Borde negro
            
            # Dibujar el texto del botón
            text = self.font.render(button['text'], True, (0, 0, 0))
            text_rect = text.get_rect(center=button['rect'].center)
            self.screen.blit(text, text_rect)
        
        pygame.display.flip()

    def run(self):
        while True:
            num_disks = self.handle_events()
            if num_disks:
                return num_disks
            self.draw()
            self.clock.tick(60)

def main():
    menu = Menu()
    game = None
    
    current_screen = "menu"
    
    while True:
        if current_screen == "menu":
            num_disks = menu.run()
            game = Game(num_disks)
            current_screen = "game"
        elif current_screen == "game":
            current_screen = game.run()

if __name__ == "__main__":
    main()