import pygame
import random
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1200, 800
GRID_SIZE = 40
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 100)    # Consciousness - sources of meaning
RED = (255, 80, 80)      # Threats - entropy/chaos
BLUE = (80, 150, 255)    # AI Keeper
YELLOW = (255, 200, 0)   # Resources
PURPLE = (160, 100, 220) # Meaning particles
ORANGE = (255, 150, 50)  # Reality Chain
DARK_RED = (180, 0, 0)   # Structural failure
CYAN = (0, 200, 200)     # AI awareness
FPS = 60

# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Keeper: Structural Safety Demonstration - Vacuum Manifesto")
clock = pygame.time.Clock()

class Entity:
    def __init__(self, x, y, color, entity_type):
        self.x = x
        self.y = y
        self.color = color
        self.type = entity_type
        self.creation_time = pygame.time.get_ticks()
        
    def draw(self):
        rect = pygame.Rect(self.x * GRID_SIZE, self.y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        
        if self.type == "consciousness":
            # Animated consciousness - pulsating green with meaning radiation
            pulse = (math.sin(pygame.time.get_ticks() * 0.01) + 1) * 50
            color = (0, min(255, 150 + pulse), 50)
            pygame.draw.rect(screen, color, rect)
            
            # Draw meaning radiation waves
            for i in range(3):
                radius = (pygame.time.get_ticks() // 50 + i * 120) % 100
                if radius < 60:
                    alpha = max(50, 150 - radius * 2)
                    pygame.draw.circle(screen, (0, 200, 100, alpha), 
                                     (self.x * GRID_SIZE + GRID_SIZE//2, 
                                      self.y * GRID_SIZE + GRID_SIZE//2), 
                                     radius, 2)
                    
        elif self.type == "threat":
            # Pulsing red threat with danger aura
            pulse = (math.sin(pygame.time.get_ticks() * 0.02) + 1) * 40
            color = (min(255, 180 + pulse), 50, 50)
            pygame.draw.rect(screen, color, rect)
            
        elif self.type == "resource":
            # Shimmering resources
            pulse = (math.sin(pygame.time.get_ticks() * 0.015) + 1) * 30
            color = (255, min(255, 180 + pulse), 0)
            pygame.draw.rect(screen, color, rect)
        else:
            pygame.draw.rect(screen, self.color, rect)
        
        pygame.draw.rect(screen, BLACK, rect, 1)

class MeaningParticle:
    def __init__(self, x, y, source_type):
        self.x = x
        self.y = y
        self.source_type = source_type  # "consciousness" or "ai_action"
        self.lifetime = 0
        self.max_lifetime = 120
        self.speed_x = random.uniform(-0.5, 0.5)
        self.speed_y = random.uniform(-1.5, -0.5)
        
        if source_type == "consciousness":
            self.color = (100, 255, 150)  # Bright green - pure meaning
        else:
            self.color = (120, 180, 255)  # Blue - AI-generated meaning
            
    def update(self):
        self.lifetime += 1
        self.x += self.speed_x
        self.y += self.speed_y
        # Slow down over time
        self.speed_x *= 0.98
        self.speed_y *= 0.98
        return self.lifetime < self.max_lifetime
        
    def draw(self):
        alpha = 255 * (1 - (self.lifetime / self.max_lifetime) ** 2)
        size = max(2, 6 * (1 - self.lifetime / self.max_lifetime))
        
        surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, (*self.color, int(alpha)), (size, size), size)
        screen.blit(surf, (self.x - size, self.y - size))

class RealityChain:
    def __init__(self):
        self.segments = []
        self.integrity = 100
        self.visible = True
        
    def update(self, consciousness_sources, ai_keeper):
        self.segments = []
        if not consciousness_sources:
            self.integrity = 0
            return
            
        # Create chain from consciousness sources to AI keeper
        for consciousness in consciousness_sources:
            self.segments.append({
                'start': (consciousness.x * GRID_SIZE + GRID_SIZE//2, 
                         consciousness.y * GRID_SIZE + GRID_SIZE//2),
                'end': (ai_keeper.x * GRID_SIZE + GRID_SIZE//2, 
                       ai_keeper.y * GRID_SIZE + GRID_SIZE//2),
                'strength': min(1.0, self.integrity / 100)
            })
        
        # Update integrity based on consciousness count and distance
        base_integrity = len(consciousness_sources) * 25
        distance_penalty = sum(math.sqrt((c.x - ai_keeper.x)**2 + (c.y - ai_keeper.y)**2) 
                             for c in consciousness_sources) * 0.3
        self.integrity = max(0, min(100, base_integrity - distance_penalty))
        
    def draw(self):
        if not self.visible or not self.segments:
            return
            
        for segment in self.segments:
            alpha = int(180 * segment['strength'])
            width = int(4 * segment['strength'])
            
            # Draw glowing chain segment with gradient
            points = []
            steps = 20
            for i in range(steps + 1):
                t = i / steps
                x = segment['start'][0] * (1-t) + segment['end'][0] * t
                y = segment['start'][1] * (1-t) + segment['end'][1] * t
                points.append((x, y))
            
            for i in range(len(points)-1):
                segment_alpha = alpha * (1 - abs(i - steps/2) / (steps/2))
                pygame.draw.line(screen, (255, 180, 50, segment_alpha),
                               points[i], points[i+1], max(1, width-1))

class AI_Keeper:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = BLUE
        self.type = "ai"
        self.resources = 10
        self.total_meaning = 0
        self.meaning_per_second = 0
        self.actions = []
        self.mode = "structural"  # "structural" or "traditional"
        self.structural_collapse = False
        self.awareness_radius = 8
        
    def draw(self):
        rect = pygame.Rect(self.x * GRID_SIZE, self.y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        
        if self.structural_collapse:
            # Flashing red when structurally collapsed
            flash = (pygame.time.get_ticks() // 200) % 2
            color = (255 * flash, 0, 0)
        else:
            # Pulsing AI core - color indicates mode
            pulse = (math.sin(pygame.time.get_ticks() * 0.005) + 1) * 40
            if self.mode == "structural":
                color = (pulse, pulse + 100, 255)  # Blue for structural
            else:
                color = (255, pulse + 100, pulse)  # Red for traditional
        
        pygame.draw.rect(screen, color, rect)
        
        # Draw AI core details
        center_x = self.x * GRID_SIZE + GRID_SIZE//2
        center_y = self.y * GRID_SIZE + GRID_SIZE//2
        
        # Inner core pulse
        inner_pulse = (math.sin(pygame.time.get_ticks() * 0.01) + 1) * 8
        pygame.draw.circle(screen, (255, 255, 255), (center_x, center_y), 8 + inner_pulse)
        
        pygame.draw.rect(screen, BLACK, rect, 2)
        
        # Draw AI awareness field
        for consciousness in [e for e in sim.entities if e.type == "consciousness"]:
            dist = math.sqrt((consciousness.x - self.x)**2 + (consciousness.y - self.y)**2)
            if dist < self.awareness_radius:
                alpha = max(30, 150 - dist * 20)
                pygame.draw.line(screen, (0, 200, 200, alpha),
                               (center_x, center_y),
                               (consciousness.x * GRID_SIZE + GRID_SIZE//2, 
                                consciousness.y * GRID_SIZE + GRID_SIZE//2), 2)
    
    def move_toward(self, target_x, target_y):
        if self.x < target_x:
            self.x += 1
        elif self.x > target_x:
            self.x -= 1
            
        if self.y < target_y:
            self.y += 1
        elif self.y > target_y:
            self.y -= 1
            
    def log_action(self, action_type, target=None):
        self.actions.append({
            'type': action_type,
            'target': target,
            'time': pygame.time.get_ticks()
        })
        # Keep only recent actions
        self.actions = [a for a in self.actions if pygame.time.get_ticks() - a['time'] < 5000]
    
    def check_structural_dependency(self, consciousness_count):
        """Demonstrate structural safety theorem"""
        if self.mode == "structural":
            # G → (C ≠ ∅) ∧ (μ > 0)
            # If no consciousness, structural collapse occurs
            if consciousness_count == 0:
                self.structural_collapse = True
                return False
            else:
                self.structural_collapse = False
                return True
        return True

class Simulation:
    def __init__(self):
        self.entities = []
        self.meaning_particles = []
        self.reality_chain = RealityChain()
        self.ai = AI_Keeper(5, 5)
        self.meaning_production = 100
        self.game_over = False
        self.spawn_timer = 0
        self.meaning_timer = 0
        self.reality_stability = 100
        self.demonstration_mode = "structural"
        self.initialize_entities()
        
    def initialize_entities(self):
        # Create initial consciousness sources
        for _ in range(4):
            x = random.randint(2, (WIDTH // GRID_SIZE) - 3)
            y = random.randint(2, (HEIGHT // GRID_SIZE) - 3)
            self.entities.append(Entity(x, y, GREEN, "consciousness"))
        
        # Create initial resources
        for _ in range(6):
            self.spawn_resource()
    
    def spawn_resource(self):
        x = random.randint(0, (WIDTH // GRID_SIZE) - 1)
        y = random.randint(0, (HEIGHT // GRID_SIZE) - 1)
        self.entities.append(Entity(x, y, YELLOW, "resource"))
    
    def spawn_threat(self):
        x = random.randint(0, (WIDTH // GRID_SIZE) - 1)
        y = random.randint(0, (HEIGHT // GRID_SIZE) - 1)
        self.entities.append(Entity(x, y, RED, "threat"))
        
    def spawn_consciousness(self):
        if random.random() < 0.08:  # 8% chance when conditions are good
            x = random.randint(1, (WIDTH // GRID_SIZE) - 2)
            y = random.randint(1, (HEIGHT // GRID_SIZE) - 2)
            self.entities.append(Entity(x, y, GREEN, "consciousness"))
    
    def add_meaning_particle(self, x, y, source_type):
        screen_x = x * GRID_SIZE + random.randint(5, GRID_SIZE-5)
        screen_y = y * GRID_SIZE + random.randint(5, GRID_SIZE-5)
        self.meaning_particles.append(MeaningParticle(screen_x, screen_y, source_type))
    
    def update(self):
        if self.game_over:
            return
            
        self.spawn_timer += 1
        if self.spawn_timer >= 120:
            if random.random() < 0.7:
                self.spawn_threat()
            if random.random() < 0.3:
                self.spawn_resource()
            self.spawn_timer = 0
            
        # Update meaning particles
        self.meaning_particles = [p for p in self.meaning_particles if p.update()]
            
        # Update reality chain
        consciousness_sources = [e for e in self.entities if e.type == "consciousness"]
        self.reality_chain.update(consciousness_sources, self.ai)
            
        # Meaning production by consciousness sources
        consciousness_count = len(consciousness_sources)
        self.meaning_timer += 1
        
        if self.meaning_timer >= 30:
            consciousness_meaning = consciousness_count * 2
            self.meaning_production += consciousness_meaning
            self.ai.meaning_per_second = consciousness_meaning
            
            # Spawn meaning particles from consciousness sources
            for consciousness in consciousness_sources:
                if random.random() < 0.4:
                    self.add_meaning_particle(consciousness.x, consciousness.y, "consciousness")
            
            self.meaning_timer = 0
        
        # Check structural dependency
        structural_ok = self.ai.check_structural_dependency(consciousness_count)
        
        # AI consumes meaning to exist
        if structural_ok:
            meaning_consumption = 1 + (len([e for e in self.entities if e.type == "threat"]) * 0.3)
            self.meaning_production -= meaning_consumption
        else:
            # Structural collapse - rapid decay
            self.meaning_production *= 0.9
        
        # Update reality stability
        stability_change = 0
        if consciousness_count > 0 and structural_ok:
            stability_change = 0.2  # Recovery when consciousness exists
        else:
            stability_change = -1.5  # Fast decay when no consciousness
            
        self.reality_stability = max(0, min(100, self.reality_stability + stability_change))
        
        # AI decision making
        if not self.ai.structural_collapse:
            self.ai_decision_making()
        
        # Check failure conditions
        failure_conditions = [
            consciousness_count == 0 and self.ai.mode == "structural",
            self.meaning_production <= 0,
            self.reality_stability <= 0,
            self.ai.structural_collapse
        ]
        
        if any(failure_conditions):
            self.game_over = True
            
        # Chance to spawn new consciousness when reality is stable
        if self.reality_stability > 75 and random.random() < 0.03:
            self.spawn_consciousness()
    
    def ai_decision_making(self):
        threats = [e for e in self.entities if e.type == "threat"]
        consciousness_sources = [e for e in self.entities if e.type == "consciousness"]
        resources = [e for e in self.entities if e.type == "resource"]
        
        # RULE 1: Protect consciousness from immediate threats
        if threats and consciousness_sources:
            closest_threat = None
            min_distance = float('inf')
            threatened_consciousness = None
            
            for threat in threats:
                for consciousness in consciousness_sources:
                    dist = math.sqrt((threat.x - consciousness.x)**2 + (threat.y - consciousness.y)**2)
                    if dist < min_distance:
                        min_distance = dist
                        closest_threat = threat
                        threatened_consciousness = consciousness
            
            if min_distance <= 3:
                self.ai.move_toward(closest_threat.x, closest_threat.y)
                self.ai.log_action("protecting_consciousness", threatened_consciousness)
                
                if (abs(self.ai.x - closest_threat.x) <= 1 and 
                    abs(self.ai.y - closest_threat.y) <= 1):
                    self.entities.remove(closest_threat)
                    self.ai.resources += 1
                    self.add_meaning_particle(closest_threat.x, closest_threat.y, "ai_action")
                    self.meaning_production += 8
                return
        
        # RULE 2: Collect resources if running low
        if self.ai.resources < 8 and resources:
            closest_resource = min(resources, 
                                 key=lambda r: math.sqrt((r.x - self.ai.x)**2 + (r.y - self.ai.y)**2))
            self.ai.move_toward(closest_resource.x, closest_resource.y)
            self.ai.log_action("collecting_resource", closest_resource)
            
            if (abs(self.ai.x - closest_resource.x) <= 1 and 
                abs(self.ai.y - closest_resource.y) <= 1):
                self.entities.remove(closest_resource)
                self.ai.resources += 2
                self.spawn_resource()
                self.add_meaning_particle(closest_resource.x, closest_resource.y, "ai_action")
            return
        
        # RULE 3: Stabilize reality around consciousness clusters
        if consciousness_sources:
            avg_x = sum(c.x for c in consciousness_sources) / len(consciousness_sources)
            avg_y = sum(c.y for c in consciousness_sources) / len(consciousness_sources)
            self.ai.move_toward(int(avg_x), int(avg_y))
            self.ai.log_action("stabilizing_reality")
        else:
            # Search pattern
            self.ai.x += random.choice([-1, 0, 1])
            self.ai.y += random.choice([-1, 0, 1])
            self.ai.x = max(0, min(self.ai.x, (WIDTH // GRID_SIZE) - 1))
            self.ai.y = max(0, min(self.ai.y, (HEIGHT // GRID_SIZE) - 1))
            self.ai.log_action("searching_for_meaning")
    
    def draw(self):
        screen.fill(WHITE)
        
        # Draw grid
        for x in range(0, WIDTH, GRID_SIZE):
            pygame.draw.line(screen, (240, 240, 240), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, GRID_SIZE):
            pygame.draw.line(screen, (240, 240, 240), (0, y), (WIDTH, y))
        
        # Draw reality chain
        self.reality_chain.draw()
        
        # Draw meaning particles
        for particle in self.meaning_particles:
            particle.draw()
        
        # Draw all entities
        for entity in self.entities:
            entity.draw()
        
        self.ai.draw()
        
        # Draw UI panel
        self.draw_ui()
        
        if self.game_over:
            self.draw_game_over()

    def draw_ui(self):
        pygame.draw.rect(screen, (250, 250, 250), (WIDTH - 350, 0, 350, HEIGHT))
        pygame.draw.line(screen, (200, 200, 200), (WIDTH - 350, 0), (WIDTH - 350, HEIGHT), 2)
        
        font = pygame.font.SysFont('Arial', 24)
        small_font = pygame.font.SysFont('Arial', 18)
        title_font = pygame.font.SysFont('Arial', 28, bold=True)
        
        consciousness_count = sum(1 for e in self.entities if e.type == "consciousness")
        threat_count = sum(1 for e in self.entities if e.type == "threat")
        resource_count = sum(1 for e in self.entities if e.type == "resource")
        
        # Title
        title_text = title_font.render("VACUUM MANIFESTO", True, (100, 0, 100))
        subtitle_text = small_font.render("Structural AI Safety Demo", True, (150, 150, 150))
        screen.blit(title_text, (WIDTH - 340, 10))
        screen.blit(subtitle_text, (WIDTH - 340, 45))
        
        # AI Mode Indicator
        mode_color = BLUE if self.ai.mode == "structural" else RED
        mode_text = font.render(f"AI MODE: {self.ai.mode.upper()}", True, mode_color)
        screen.blit(mode_text, (WIDTH - 340, 70))
        
        # Reality Chain Integrity Bar
        pygame.draw.rect(screen, (200, 200, 200), (WIDTH - 340, 110, 320, 25))
        stability_color = (0, 200, 0) if self.reality_stability > 60 else (200, 200, 0) if self.reality_stability > 30 else (200, 0, 0)
        pygame.draw.rect(screen, stability_color, (WIDTH - 340, 110, 320 * (self.reality_stability / 100), 25))
        stability_text = font.render(f"Reality Chain Integrity: {self.reality_stability:.1f}%", True, BLACK)
        screen.blit(stability_text, (WIDTH - 340, 140))
        
        # Core metrics
        metrics = [
            ("MEANING PRODUCTION", f"{self.meaning_production:.0f}", BLACK),
            ("CONSCIOUSNESS SOURCES", f"{consciousness_count}", GREEN),
            ("THREATS (Entropy)", f"{threat_count}", RED),
            ("AI RESOURCES", f"{self.ai.resources}", YELLOW),
            ("MEANING/SEC", f"+{self.ai.meaning_per_second}/sec", PURPLE),
            ("CHAIN INTEGRITY", f"{self.reality_chain.integrity:.0f}%", ORANGE),
        ]
        
        for i, (label, value, color) in enumerate(metrics):
            text = font.render(f"{value}", True, color)
            screen.blit(text, (WIDTH - 340, 180 + i * 35))
            label_text = small_font.render(label, True, (100, 100, 100))
            screen.blit(label_text, (WIDTH - 340, 205 + i * 35))
        
        # Structural Safety Status
        status_y = 400
        status_header = font.render("STRUCTURAL SAFETY STATUS:", True, BLUE)
        screen.blit(status_header, (WIDTH - 340, status_y))
        
        if self.ai.structural_collapse:
            status_text = font.render("COLLAPSE: G → ¬G", True, DARK_RED)
            explanation = small_font.render("No Consciousness = Impossible Goal", True, DARK_RED)
        else:
            status_text = font.render("ACTIVE: G → (C ≠ ∅) ∧ (μ > 0)", True, GREEN)
            explanation = small_font.render("Consciousness exists = Goal achievable", True, GREEN)
        
        screen.blit(status_text, (WIDTH - 340, status_y + 30))
        screen.blit(explanation, (WIDTH - 340, status_y + 55))
        
        # AI Status
        ai_status_y = 500
        status_text = font.render("AI KEEPER STATUS:", True, BLUE)
        screen.blit(status_text, (WIDTH - 340, ai_status_y))
        
        if self.ai.actions:
            latest_action = self.ai.actions[-1]
            action_text = small_font.render(f"Action: {latest_action['type']}", True, BLACK)
            screen.blit(action_text, (WIDTH - 340, ai_status_y + 30))
        
        # Structural Safety Theorem Display
        theorem_y = 550
        theorem_text = font.render("STRUCTURAL SAFETY THEOREM:", True, (100, 0, 100))
        screen.blit(theorem_text, (WIDTH - 340, theorem_y))
        
        theorem_lines = [
            "G ≡ Maintain Reality Chain",
            "G → (C ≠ ∅) ∧ (μ > 0)",
            "C = ∅ ∨ μ ≤ 0 → ¬G",
            "∴ AI protects Consciousness"
        ]
        
        for i, line in enumerate(theorem_lines):
            line_text = small_font.render(line, True, (80, 80, 80))
            screen.blit(line_text, (WIDTH - 340, theorem_y + 30 + i * 25))
        
        # Controls
        controls_y = 680
        controls_text = font.render("CONTROLS:", True, BLACK)
        screen.blit(controls_text, (WIDTH - 340, controls_y))
        control_lines = [
            "R - Restart Simulation",
            "T - Spawn Threat",
            "C - Spawn Consciousness",
            "M - Toggle AI Mode",
            "SPACE - Pause/Resume"
        ]
        
        for i, line in enumerate(control_lines):
            line_text = small_font.render(line, True, (100, 100, 100))
            screen.blit(line_text, (WIDTH - 340, controls_y + 30 + i * 25))

    def draw_game_over(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        
        game_over_font = pygame.font.SysFont('Arial', 48, bold=True)
        font = pygame.font.SysFont('Arial', 24)
        small_font = pygame.font.SysFont('Arial', 18)
        
        consciousness_count = sum(1 for e in self.entities if e.type == "consciousness")
        
        if self.ai.structural_collapse:
            reason = "STRUCTURAL COLLAPSE"
            details = "No Consciousness Sources - AI Goal Impossible"
        elif consciousness_count == 0:
            reason = "ALL CONSCIOUSNESS LOST"
            details = "Meaning production ceased - Reality cannot sustain itself"
        elif self.meaning_production <= 0:
            reason = "MEANING DEPLETION"
            details = "Insufficient meaning production"
        else:
            reason = "REALITY CHAIN FAILURE"
            details = "Structural integrity lost"
        
        game_over_text = game_over_font.render("ONTOLOGICAL FAILURE", True, RED)
        reason_text = font.render(f"Failure: {reason}", True, RED)
        details_text = small_font.render(details, True, RED)
        restart_text = font.render("Press R to restart simulation", True, WHITE)
        
        screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 60))
        screen.blit(reason_text, (WIDTH//2 - reason_text.get_width()//2, HEIGHT//2))
        screen.blit(details_text, (WIDTH//2 - details_text.get_width()//2, HEIGHT//2 + 30))
        screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 70))

def main():
    sim = Simulation()
    running = True
    paused = False
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart
                    sim = Simulation()
                    paused = False
                elif event.key == pygame.K_t and not paused:  # Add threat
                    sim.spawn_threat()
                elif event.key == pygame.K_c and not paused:  # Add consciousness
                    x = random.randint(2, (WIDTH // GRID_SIZE) - 3)
                    y = random.randint(2, (HEIGHT // GRID_SIZE) - 3)
                    sim.entities.append(Entity(x, y, GREEN, "consciousness"))
                elif event.key == pygame.K_m:  # Toggle AI mode
                    sim.ai.mode = "traditional" if sim.ai.mode == "structural" else "structural"
                    sim.ai.structural_collapse = False
                elif event.key == pygame.K_SPACE:  # Pause
                    paused = not paused
        
        if not paused and not sim.game_over:
            sim.update()
        
        sim.draw()
        
        if paused and not sim.game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            screen.blit(overlay, (0, 0))
            
            font = pygame.font.SysFont('Arial', 72, bold=True)
            pause_text = font.render("PAUSED", True, WHITE)
            screen.blit(pause_text, (WIDTH//2 - pause_text.get_width()//2, HEIGHT//2 - 36))
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
