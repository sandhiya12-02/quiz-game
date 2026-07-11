import sys
import random
import pygame

# Initialize Pygame
pygame.init()

# --- CONSTANTS & CONFIGURATION ---
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FPS = 60

# Neo-Brutalist Color Palette from the reference picture
COLOR_BG = (240, 240, 240)
COLOR_BLACK = (0, 0, 0)
COLOR_PURPLE = (99, 68, 209)
COLOR_PINK = (255, 117, 181)
COLOR_NEON_YELLOW = (208, 255, 67)
COLOR_WHITE = (255, 255, 255)
COLOR_LIGHT_GREY = (220, 220, 220)

# Safe cross-platform fonts
FONT_TITLE = pygame.font.SysFont("impact", 50)
FONT_SUBTITLE = pygame.font.SysFont("arial", 20, bold=True)
FONT_BODY = pygame.font.SysFont("arial", 22, bold=True)
FONT_SMALL = pygame.font.SysFont("arial", 16, bold=True)

# --- QUESTION BANK (100 Questions) ---
QUESTION_POOL = []
for i in range(1, 101):
    if i % 4 == 0:
        QUESTION_POOL.append({
            "q": f"Which language is primarily used for Data Science? (Q {i})",
            "options": ["Python", "Java", "C++", "Ruby"], "correct": "Python"
        })
    elif i % 4 == 1:
        QUESTION_POOL.append({
            "q": f"What is the value of 5 multiplied by {i}? (Q {i})",
            "options": [str(5*i), str(5*i+2), str(5*i-3), str(5*i+10)], "correct": str(5*i)
        })
    elif i % 4 == 2:
        QUESTION_POOL.append({
            "q": f"Is HTTP port 80 used for secure or unsecure web traffic? (Q {i})",
            "options": ["Unsecure (HTTP)", "Secure (HTTPS)", "Email", "File Transfer"], "correct": "Unsecure (HTTP)"
        })
    else:
        QUESTION_POOL.append({
            "q": f"Which HTML tag is used to define an internal style sheet? (Q {i})",
            "options": ["<style>", "<script>", "<css>", "<link>"], "correct": "<style>"
        })

# --- UI DRAWING HELPERS ---
def draw_brutal_box(surface, rect, bg_color, border_thickness=4):
    """Draws a blocky element with thick black borders."""
    pygame.draw.rect(surface, bg_color, rect)
    pygame.draw.rect(surface, COLOR_BLACK, rect, border_thickness)

def draw_brutal_button(surface, rect, bg_color, text, is_hovered, border_thickness=4):
    """Draws a button that renders a blocky shadow offset when hovered."""
    if is_hovered:
        shadow_rect = pygame.Rect(rect.x + 6, rect.y + 6, rect.width, rect.height)
        pygame.draw.rect(surface, COLOR_BLACK, shadow_rect)
    
    draw_brutal_box(surface, rect, bg_color, border_thickness)
    text_surf = FONT_BODY.render(text, True, COLOR_BLACK)
    text_rect = text_surf.get_rect(center=rect.center)
    surface.blit(text_surf, text_rect)

# --- GAME SYSTEM CLASS ---
class QuizGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Neo-Brutalist Quiz Game")
        self.clock = pygame.time.Clock()
        self.state = "MAIN_MENU"
        
        self.selected_questions = []
        self.current_question_idx = 0
        self.score = 0
        self.current_round = 1
        self.selected_option = None
        self.answer_submitted = False
        
        self.timer_seconds = 20
        self.last_timer_event = 0

    def start_new_game(self):
        # Dynamically grabs 30 random questions from the pool of 100
        self.selected_questions = random.sample(QUESTION_POOL, 30)
        self.current_question_idx = 0
        self.score = 0
        self.current_round = 1
        self.selected_option = None
        self.answer_submitted = False
        self.reset_timer()
        self.state = "PLAYING"

    def reset_timer(self):
        self.timer_seconds = 20
        self.last_timer_event = pygame.time.get_ticks()

    def update_timer(self):
        if self.state == "PLAYING" and not self.answer_submitted:
            now = pygame.time.get_ticks()
            if now - self.last_timer_event >= 1000:
                self.timer_seconds -= 1
                self.last_timer_event = now
                if self.timer_seconds <= 0:
                    self.submit_answer(timeout=True)

    def submit_answer(self, timeout=False):
        self.answer_submitted = True
        current_q = self.selected_questions[self.current_question_idx]
        if not timeout and self.selected_option == current_q["correct"]:
            self.score += 1
            
    def next_question(self):
        self.current_question_idx += 1
        self.selected_option = None
        self.answer_submitted = False
        self.reset_timer()
        
        # 3 Rounds progression logic (10 questions per round)
        if self.current_question_idx >= 30:
            self.state = "VICTORY_SCREEN"
        elif self.current_question_idx == 20:
            self.current_round = 3
        elif self.current_question_idx == 10:
            self.current_round = 2

    def run(self):
        while True:
            self.clock.tick(FPS)
            self.update_timer()
            self.handle_events()
            self.render()

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.state == "MAIN_MENU":
                    if pygame.Rect(350, 400, 300, 70).collidepoint(mouse_pos):
                        self.start_new_game()
                        
                elif self.state == "PLAYING":
                    current_q = self.selected_questions[self.current_question_idx]
                    
                    if not self.answer_submitted:
                        for idx in range(4):
                            opt_rect = pygame.Rect(450, 250 + (idx * 75), 400, 55)
                            if opt_rect.collidepoint(mouse_pos):
                                self.selected_option = current_q["options"][idx]
                        
                        submit_rect = pygame.Rect(450, 560, 400, 55)
                        if submit_rect.collidepoint(mouse_pos) and self.selected_option is not None:
                            self.submit_answer()
                    else:
                        next_rect = pygame.Rect(450, 560, 400, 55)
                        if next_rect.collidepoint(mouse_pos):
                            self.next_question()
                            
                elif self.state == "VICTORY_SCREEN":
                    if pygame.Rect(350, 450, 300, 70).collidepoint(mouse_pos):
                        self.state = "MAIN_MENU"

    def render(self):
        self.screen.fill(COLOR_BG)
        mouse_pos = pygame.mouse.get_pos()
        
        if self.state == "MAIN_MENU":
            # Main Menu Banner
            draw_brutal_box(self.screen, pygame.Rect(200, 100, 600, 200), COLOR_PURPLE)
            title_text = FONT_TITLE.render("QUIZ GAME", True, COLOR_WHITE)
            self.screen.blit(title_text, title_text.get_rect(center=(500, 200)))
            
            sub_text = FONT_SUBTITLE.render("100 Questions Pool | 3 Rounds | 30 Random Questions", True, COLOR_BLACK)
            self.screen.blit(sub_text, sub_text.get_rect(center=(500, 340)))
            
            btn_rect = pygame.Rect(350, 400, 300, 70)
            draw_brutal_button(self.screen, btn_rect, COLOR_NEON_YELLOW, "START GAME", btn_rect.collidepoint(mouse_pos))
            
        elif self.state == "PLAYING":
            current_q = self.selected_questions[self.current_question_idx]
            round_q_num = (self.current_question_idx % 10) + 1
            
            # --- LEFT BANNER SYSTEM ---
            draw_brutal_box(self.screen, pygame.Rect(20, 20, 380, 660), COLOR_NEON_YELLOW)
            title_side = FONT_TITLE.render("QUIZ", True, COLOR_BLACK)
            game_side = FONT_TITLE.render("GAME", True, COLOR_BLACK)
            self.screen.blit(title_side, (40, 50))
            self.screen.blit(game_side, (40, 120))
            
            draw_brutal_box(self.screen, pygame.Rect(40, 240, 340, 120), COLOR_PURPLE)
            r_text = FONT_BODY.render(f"ROUND: {self.current_round} / 3", True, COLOR_WHITE)
            q_text = FONT_BODY.render(f"TOTAL Q: {self.current_question_idx + 1} / 30", True, COLOR_WHITE)
            self.screen.blit(r_text, (60, 265))
            self.screen.blit(q_text, (60, 310))
            
            draw_brutal_box(self.screen, pygame.Rect(40, 520, 340, 120), COLOR_PINK)
            rule_t1 = FONT_SMALL.render("+1 Point Per Answer", True, COLOR_BLACK)
            rule_t2 = FONT_SMALL.render("20 Seconds Speed Limit", True, COLOR_BLACK)
            self.screen.blit(rule_t1, (60, 550))
            self.screen.blit(rule_t2, (60, 580))

            # --- CENTER MAIN QUESTION AREA ---
            header_rect = pygame.Rect(420, 20, 420, 50)
            draw_brutal_box(self.screen, header_rect, COLOR_WHITE)
            q_header_text = FONT_SUBTITLE.render(f"QUESTION {round_q_num} OF 10", True, COLOR_BLACK)
            self.screen.blit(q_header_text, (440, 32))
            
            q_body_rect = pygame.Rect(420, 85, 420, 130)
            draw_brutal_box(self.screen, q_body_rect, COLOR_WHITE)
            
            # Simple text wrap engine
            words = current_q["q"].split(' ')
            lines = []
            current_line = ""
            for word in words:
                test_line = current_line + word + " "
                if FONT_BODY.size(test_line) < 380:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word + " "
            lines.append(current_line)
            
            for i, line in enumerate(lines):
                q_surf = FONT_BODY.render(line, True, COLOR_BLACK)
                self.screen.blit(q_surf, (440, 105 + (i * 30)))

            # Option Cards (A, B, C, D)
            for idx, option in enumerate(current_q["options"]):
                opt_rect = pygame.Rect(450, 250 + (idx * 75), 400, 55)
