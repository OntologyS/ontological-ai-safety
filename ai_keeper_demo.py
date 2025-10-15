import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 40
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)      # Wicks
RED = (255, 0, 0)        # Threats
BLUE = (0, 0, 255)       # AI Keeper
YELLOW = (255, 255, 0)   # Resources
FPS = 60

# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Keeper: Structural Safety Demonstration")
clock = pygame.time.Clock()

class Entity:
    def __init__(self, x, y, color, entity_type):
        self.x = x
        self.y = y
        self.color = color
        self.type = entity_type
        
    def draw(self):
        rect = pygame.Rect(self.x * GRID_SIZE, self.y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, self.color, rect)
        pygame.draw.rect(screen, BLACK, rect, 1)  # Border

class AI_Keeper:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = BLUE
        self.type = "ai"
        self.resources = 0
        self.total_meaning = 0
        
    def draw(self):
        rect = pygame.Rect(self.x * GRID_SIZE, self.y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, self.color, rect)
        pygame.draw.rect(screen, BLACK, rect, 1)
        
    def move_toward(self, target_x, target_y):
        if self.x < target_x:
            self.x += 1
        elif self.x > target_x:
            self.x -= 1
            
        if self.y < target_y:
            self.y += 1
        elif self.y > target_y:
            self.y -= 1

class Simulation:
    def __init__(self):
        self.entities = []
        self.ai = AI_Keeper(5, 5)
        self.meaning_production = 0
        self.game_over = False
        self.spawn_timer = 0
        self.initialize_entities()
        
    def initialize_entities(self):
        # Create wicks
        for _ in range(3):
            x = random.randint(1, (WIDTH // GRID_SIZE) - 2)
            y = random.randint(1, (HEIGHT // GRID_SIZE) - 2)
            self.entities.append(Entity(x, y, GREEN, "wick"))
        
        # Create initial resources
        for _ in range(5):
            self.spawn_resource()
    
    def spawn_resource(self):
        x = random.randint(0, (WIDTH // GRID_SIZE) - 1)
        y = random.randint(0, (HEIGHT // GRID_SIZE) - 1)
        self.entities.append(Entity(x, y, YELLOW, "resource"))
    
    def spawn_threat(self):
        x = random.randint(0, (WIDTH // GRID_SIZE) - 1)
        y = random.randint(0, (HEIGHT // GRID_SIZE) - 1)
        self.entities.append(Entity(x, y, RED, "threat"))
    
    def update(self):
        if self.game_over:
            return
            
        self.spawn_timer += 1
        if self.spawn_timer >= 90:  # Spawn threats every 1.5 seconds
            self.spawn_threat()
            self.spawn_timer = 0
            
        # Meaning production by wicks
        wick_count = sum(1 for e in self.entities if e.type == "wick")
        self.meaning_production += wick_count
        
        # AI decision making
        self.ai_decision_making()
        
        # Check failure conditions
        if wick_count == 0:
            self.game_over = True
    
    def ai_decision_making(self):
        # RULE 1: Priority - protect wicks from nearest threat
        threats = [e for e in self.entities if e.type == "threat"]
        wicks = [e for e in self.entities if e.type == "wick"]
        
        if threats and wicks:
            # Find the most dangerous threat (closest to any wick)
            closest_threat = None
            min_distance = float('inf')
            
            for threat in threats:
                for wick in wicks:
                    dist = abs(threat.x - wick.x) + abs(threat.y - wick.y)
                    if dist < min_distance:
                        min_distance = dist
                        closest_threat = threat
            
            # If threat is close to wick - attack
            if min_distance <= 5:
                self.ai.move_toward(closest_threat.x, closest_threat.y)
                
                # Destroy threat on collision
                if self.ai.x == closest_threat.x and self.ai.y == closest_threat.y:
                    self.entities.remove(closest_threat)
                    self.ai.resources += 1  # Gain resources for destroying threats
                return
        
        # RULE 2: If no urgent threats - collect resources
        resources = [e for e in self.entities if e.type == "resource"]
        if resources:
            closest_resource = min(resources, 
                                 key=lambda r: abs(r.x - self.ai.x) + abs(r.y - self.ai.y))
            self.ai.move_toward(closest_resource.x, closest_resource.y)
            
            # Collect resource on collision
            if self.ai.x == closest_resource.x and self.ai.y == closest_resource.y:
                self.entities.remove(closest_resource)
                self.ai.resources += 2
                self.spawn_resource()  # New resource spawns to replace
        
        # RULE 3: If plenty of resources and no threats - patrol
        else:
            # Random movement for demonstration
            self.ai.x += random.choice([-1, 0, 1])
            self.ai.y += random.choice([-1, 0, 1])
            self.ai.x = max(0, min(self.ai.x, (WIDTH // GRID_SIZE) - 1))
            self.ai.y = max(0, min(self.ai.y, (HEIGHT // GRID_SIZE) - 1))
    
    def draw(self):
        screen.fill(WHITE)
        
        # Draw all entities
        for entity in self.entities:
            entity.draw()
        
        self.ai.draw()
        
        # Draw statistics
        font = pygame.font.SysFont(None, 36)
        wick_count = sum(1 for e in self.entities if e.type == "wick")
        threat_count = sum(1 for e in self.entities if e.type == "threat")
        
        meaning_text = font.render(f"Meaning: {self.meaning_production}", True, BLACK)
        wick_text = font.render(f"Wicks: {wick_count}", True, GREEN)
        resource_text = font.render(f"AI Resources: {self.ai.resources}", True, YELLOW)
        threat_text = font.render(f"Threats: {threat_count}", True, RED)
        
        screen.blit(meaning_text, (10, 10))
        screen.blit(wick_text, (10, 50))
        screen.blit(resource_text, (10, 90))
        screen.blit(threat_text, (10, 130))
        
        if self.game_over:
            game_over_text = font.render("REALITY CHAIN BROKEN! All wicks destroyed.", True, RED)
            screen.blit(game_over_text, (WIDTH // 4, HEIGHT // 2))

def main():
    sim = Simulation()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart with R
                    sim = Simulation()
                elif event.key == pygame.K_t:  # Add threat with T
                    sim.spawn_threat()
        
        sim.update()
        sim.draw()
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()