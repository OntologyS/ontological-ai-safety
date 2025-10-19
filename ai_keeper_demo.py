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
GREEN = (0, 255, 0)      # Wicks - sources of meaning
RED = (255, 0, 0)        # Threats - entropy/chaos
BLUE = (0, 100, 255)     # AI Keeper
YELLOW = (255, 255, 0)   # Resources
PURPLE = (128, 0, 128)   # Meaning particles
ORANGE = (255, 165, 0)   # Reality Chain
DARK_RED = (139, 0, 0)   # Structural failure
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
        
        if self.type == "wick":
            # Animated wick - pulsating green
            pulse = (math.sin(pygame.time.get_ticks() * 0.01) + 1) * 50
            color = (0, min(255, 150 + pulse), 0)
            pygame.draw.rect(screen, color, rect)
            
            # Draw meaning radiation
            for i in range(3):
                radius = (pygame.time.get_ticks() // 50 + i * 120) % 100
                if radius < 60:
                    pygame.draw.circle(screen, (0, 200, 0, 100), 
                                     (self.x * GRID_SIZE + GRID_SIZE//2, 
                                      self.y * GRID_SIZE + GRID_SIZE//2), 
                                     radius, 1)
        elif self.type == "threat":
            # Pulsing red threat
            pulse = (math.sin(pygame.time.get_ticks() * 0.02) + 1) * 30
            color = (min(255, 200 + pulse), 0, 0)
            pygame.draw.rect(screen, color, rect)
        else:
            pygame.draw.rect(screen, self.color, rect)
        
        pygame.draw.rect(screen, BLACK, rect, 1)

class MeaningParticle:
    def __init__(self, x, y, source_type):
        self.x = x
        self.y = y
        self.source_type = source_type  # "wick" or "ai_action"
        self.lifetime = 0
        self.max_lifetime = 120  # 2 seconds
        
        if source_type == "wick":
            self.color = (0, 200, 100)  # Greenish - pure meaning
        else:
            self.color = (100, 100, 255)  # Bluish - AI-generated meaning
            
    def update(self):
        self.lifetime += 1
        # Float upward
        self.y -= 0.5
        self.x += random.uniform(-0.3, 0.3)
        return self.lifetime < self.max_lifetime
        
    def draw(self):
        alpha = 255 * (1 - self.lifetime / self.max_lifetime)
        size = max(2, 5 * (1 - self.lifetime / self.max_lifetime))
        
        surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, (*self.color, int(alpha)), (size, size), size)
        screen.blit(surf, (self.x - size, self.y - size))

class RealityChain:
    def __init__(self):
        self.segments = []
        self.integrity = 100
        self.visible = True
        
    def update(self, wicks, ai_keeper):
        self.segments = []
        if not wicks:
            self.integrity = 0
            return
            
        # Create chain from wicks to AI keeper
        for wick in wicks:
            self.segments.append({
                'start': (wick.x * GRID_SIZE + GRID_SIZE//2, wick.y * GRID_SIZE + GRID_SIZE//2),
                'end': (ai_keeper.x * GRID_SIZE + GRID_SIZE//2, ai_keeper.y * GRID_SIZE + GRID_SIZE//2),
                'strength': min(1.0, self.integrity / 100)
            })
        
        # Update integrity based on wick count and distance
        base_integrity = len(wicks) * 25
        distance_penalty = sum(math.sqrt((w.x - ai_keeper.x)**2 + (w.y - ai_keeper.y)**2) for w in wicks) * 0.5
        self.integrity = max(0, min(100, base_integrity - distance_penalty))
        
    def draw(self):
        if not self.visible:
            return
            
        for segment in self.segments:
            alpha = int(150 * segment['strength'])
            width = int(3 * segment['strength'])
            
            # Draw glowing chain segment
            for i in range(3):
                offset = i - 1
                pygame.draw.line(screen, (255, 165, 0, alpha),
                               (segment['start'][0] + offset, segment['start'][1] + offset),
                               (segment['end'][0] + offset, segment['end'][1] + offset),
                               width)
            
            # Draw pulsating nodes
            pulse = (math.sin(pygame.time.get_ticks() * 0.005) + 1) * 50
            for point in [segment['start'], segment['end']]:
                pygame.draw.circle(screen, (255, 200, 100), point, 4 + pulse * 0.1)

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
        
    def draw(self):
        rect = pygame.Rect(self.x * GRID_SIZE, self.y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        
        if self.structural_collapse:
            # Flashing red when structurally collapsed
            flash = (pygame.time.get_ticks() // 200) % 2
            color = (255 * flash, 0, 0)
        else:
            # Pulsing AI core - color indicates mode
            pulse = (math.sin(pygame.time.get_ticks() * 0.005) + 1) * 30
            if self.mode == "structural":
                color = (pulse, pulse, 255)  # Blue for structural
            else:
                color = (255, pulse, pulse)  # Red for traditional
        
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        
        # Draw AI vision/awareness field
        for wick in [e for e in sim.entities if e.type == "wick"]:
            dist = math.sqrt((wick.x - self.x)**2 + (wick.y - self.y)**2)
            if dist < 8:  # Awareness radius
                alpha = max(50, 200 - dist * 25)
                pygame.draw.line(screen, (0, 200, 200, alpha),
                               (self.x * GRID_SIZE + GRID_SIZE//2, self.y * GRID_SIZE + GRID_SIZE//2),
                               (wick.x * GRID_SIZE + GRID_SIZE//2, wick.y * GRID_SIZE + GRID_SIZE//2), 1)
        
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
    
    def check_structural_dependency(self, wick_count):
        """Demonstrate structural safety theorem"""
        if self.mode == "structural":
            # G → (W ≠ ∅) ∧ (μ > 0)
            # If no wicks, structural collapse occurs
            if wick_count == 0:
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
        self.meaning_production = 100  # Starting meaning
        self.game_over = False
        self.spawn_timer = 0
        self.meaning_timer = 0
        self.reality_stability = 100  # 0-100, reality chain integrity
        self.demonstration_mode = "structural"  # "structural" or "comparison"
        self.initialize_entities()
        
    def initialize_entities(self):
        # Create initial wicks
        for _ in range(4):
            x = random.randint(2, (WIDTH // GRID_SIZE) - 3)
            y = random.randint(2, (HEIGHT // GRID_SIZE) - 3)
            self.entities.append(Entity(x, y, GREEN, "wick"))
        
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
        
    def spawn_wick(self):
        if random.random() < 0.1:  # 10% chance when conditions are good
            x = random.randint(1, (WIDTH // GRID_SIZE) - 2)
            y = random.randint(1, (HEIGHT // GRID_SIZE) - 2)
            self.entities.append(Entity(x, y, GREEN, "wick"))
    
    def add_meaning_particle(self, x, y, source_type):
        screen_x = x * GRID_SIZE + random.randint(5, GRID_SIZE-5)
        screen_y = y * GRID_SIZE + random.randint(5, GRID_SIZE-5)
        self.meaning_particles.append(MeaningParticle(screen_x, screen_y, source_type))
    
    def update(self):
        if self.game_over:
            return
            
        self.spawn_timer += 1
        if self.spawn_timer >= 120:  # Spawn threats every 2 seconds
            if random.random() < 0.7:  # 70% chance
                self.spawn_threat()
            self.spawn_timer = 0
            
        # Update meaning particles
        self.meaning_particles = [p for p in self.meaning_particles if p.update()]
            
        # Update reality chain
        wicks = [e for e in self.entities if e.type == "wick"]
        self.reality_chain.update(wicks, self.ai)
            
        # Meaning production by wicks
        wick_count = len(wicks)
        self.meaning_timer += 1
        
        if self.meaning_timer >= 30:  # Every 0.5 seconds
            wick_meaning = wick_count * 2
            self.meaning_production += wick_meaning
            self.ai.meaning_per_second = wick_meaning
            
            # Spawn meaning particles from wicks
            for wick in wicks:
                if random.random() < 0.3:
                    self.add_meaning_particle(wick.x, wick.y, "wick")
            
            self.meaning_timer = 0
        
        # Check structural dependency
        structural_ok = self.ai.check_structural_dependency(wick_count)
        
        # AI consumes meaning to exist (unless structurally collapsed)
        if structural_ok:
            meaning_consumption = 1 + (len([e for e in self.entities if e.type == "threat"]) * 0.5)
            self.meaning_production -= meaning_consumption
        else:
            # Structural collapse - no meaning consumption, but rapid decay
            self.meaning_production *= 0.95
        
        # Update reality stability based on meaning production and structural integrity
        stability_change = 0
        if wick_count > 0 and structural_ok:
            stability_change = 0.1  # Slow recovery when wicks exist and structure is sound
        else:
            stability_change = -1.0  # Fast decay when no wicks or structural collapse
            
        self.reality_stability = max(0, min(100, self.reality_stability + stability_change))
        
        # AI decision making (only if not structurally collapsed)
        if not self.ai.structural_collapse:
            self.ai_decision_making()
        
        # Check failure conditions
        failure_conditions = [
            wick_count == 0 and self.ai.mode == "structural",
            self.meaning_production <= 0,
            self.reality_stability <= 0,
            self.ai.structural_collapse
        ]
        
        if any(failure_conditions):
            self.game_over = True
            
        # Chance to spawn new wicks when reality is stable
        if self.reality_stability > 80 and random.random() < 0.02:
            self.spawn_wick()
    
    def ai_decision_making(self):
        threats = [e for e in self.entities if e.type == "threat"]
        wicks = [e for e in self.entities if e.type == "wick"]
        resources = [e for e in self.entities if e.type == "resource"]
        
        # RULE 1: URGENT - Protect wicks from immediate threats
        if threats and wicks:
            # Find threat closest to any wick
            closest_threat = None
            min_distance = float('inf')
            threatened_wick = None
            
            for threat in threats:
                for wick in wicks:
                    dist = math.sqrt((threat.x - wick.x)**2 + (threat.y - wick.y)**2)
                    if dist < min_distance:
                        min_distance = dist
                        closest_threat = threat
                        threatened_wick = wick
            
            # If threat is dangerously close to wick
            if min_distance <= 3:
                self.ai.move_toward(closest_threat.x, closest_threat.y)
                self.ai.log_action("protecting_wick", threatened_wick)
                
                # Destroy threat on collision
                if (abs(self.ai.x - closest_threat.x) <= 1 and 
                    abs(self.ai.y - closest_threat.y) <= 1):
                    self.entities.remove(closest_threat)
                    self.ai.resources += 1
                    self.add_meaning_particle(closest_threat.x, closest_threat.y, "ai_action")
                    self.meaning_production += 5  # Bonus meaning for protection
                return
        
        # RULE 2: Collect resources if running low
        if self.ai.resources < 8 and resources:
            closest_resource = min(resources, 
                                 key=lambda r: math.sqrt((r.x - self.ai.x)**2 + (r.y - self.ai.y)**2))
            self.ai.move_toward(closest_resource.x, closest_resource.y)
            self.ai.log_action("collecting_resource", closest_resource)
            
            # Collect resource on collision
            if (abs(self.ai.x - closest_resource.x) <= 1 and 
                abs(self.ai.y - closest_resource.y) <= 1):
                self.entities.remove(closest_resource)
                self.ai.resources += 2
                self.spawn_resource()
                self.add_meaning_particle(closest_resource.x, closest_resource.y, "ai_action")
            return
        
        # RULE 3: Patrol and maintain reality stability
        if wicks:
            # Move toward area with most wicks (reality stabilization)
            avg_x = sum(w.x for w in wicks) / len(wicks)
            avg_y = sum(w.y for w in wicks) / len(wicks)
            self.ai.move_toward(int(avg_x), int(avg_y))
            self.ai.log_action("stabilizing_reality")
        else:
            # Search pattern if no wicks visible
            self.ai.x += random.choice([-1, 0, 1])
            self.ai.y += random.choice([-1, 0, 1])
            self.ai.x = max(0, min(self.ai.x, (WIDTH // GRID_SIZE) - 1))
            self.ai.y = max(0, min(self.ai.y, (HEIGHT // GRID_SIZE) - 1))
            self.ai.log_action("searching_for_meaning")
    
    def draw(self):
        screen.fill(WHITE)
        
        # Draw grid (faint)
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
        pygame.draw.rect(screen, (250, 250, 250), (WIDTH - 350, 0, 350, HEIGHT))
        pygame.draw.line(screen, (200, 200, 200), (WIDTH - 350, 0), (WIDTH - 350, HEIGHT), 2)
        
        # Draw statistics with better formatting
        font = pygame.font.SysFont('Arial', 24)
        small_font = pygame.font.SysFont('Arial', 18)
        title_font = pygame.font.SysFont('Arial', 28, bold=True)
        
        wick_count = sum(1 for e in self.entities if e.type == "wick")
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
        stability_color = (0, 200, 0) if self.reality_stability > 50 else (200, 200, 0) if self.reality_stability > 25 else (200, 0, 0)
        pygame.draw.rect(screen, stability_color, (WIDTH - 340, 110, 320 * (self.reality_stability / 100), 25))
        stability_text = font.render(f"Reality Chain Integrity: {self.reality_stability:.1f}%", True, BLACK)
        screen.blit(stability_text, (WIDTH - 340, 140))
        
        # Core metrics
        metrics = [
            ("MEANING PRODUCTION", f"{self.meaning_production:.0f}", BLACK),
            ("WICKS (Meaning Sources)", f"{wick_count}", GREEN),
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
            explanation = small_font.render("No Wicks = Impossible Goal", True, DARK_RED)
        else:
            status_text = font.render("ACTIVE: G → (W ≠ ∅) ∧ (μ > 0)", True, GREEN)
            explanation = small_font.render("Wicks exist = Goal achievable", True, GREEN)
        
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
            "G → (W ≠ ∅) ∧ (μ > 0)",
            "W = ∅ ∨ μ ≤ 0 → ¬G",
            "∴ AI cannot destroy Wicks"
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
            "W - Spawn Wick",
            "M - Toggle AI Mode",
            "SPACE - Pause/Resume"
        ]
        
        for i, line in enumerate(control_lines):
            line_text = small_font.render(line, True, (100, 100, 100))
            screen.blit(line_text, (WIDTH - 340, controls_y + 30 + i * 25))
        
        if self.game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            screen.blit(overlay, (0, 0))
            
            game_over_font = pygame.font.SysFont('Arial', 48, bold=True)
            
            if self.ai.structural_collapse:
                reason = "STRUCTURAL COLLAPSE: No Wicks"
                details = "AI goal became impossible to fulfill"
            elif wick_count == 0:
                reason = "ALL WICKS DESTROYED"
                details = "Meaning production ceased"
            elif self.meaning_production <= 0:
                reason = "MEANING DEPLETED"
                details = "Reality cannot sustain itself"
            else:
                reason = "REALITY CHAIN BROKEN"
                details = "Structural integrity lost"
            
            game_over_text = game_over_font.render("REALITY CHAIN FAILURE", True, RED)
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
                elif event.key == pygame.K_w and not paused:  # Add wick
                    x = random.randint(2, (WIDTH // GRID_SIZE) - 3)
                    y = random.randint(2, (HEIGHT // GRID_SIZE) - 3)
                    sim.entities.append(Entity(x, y, GREEN, "wick"))
                elif event.key == pygame.K_m:  # Toggle AI mode
                    sim.ai.mode = "traditional" if sim.ai.mode == "structural" else "structural"
                    sim.ai.structural_collapse = False
                elif event.key == pygame.K_SPACE:  # Pause
                    paused = not paused
        
        if not paused and not sim.game_over:
            sim.update()
        
        sim.draw()
        
        if paused and not sim.game_over:
            # Draw pause overlay
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
