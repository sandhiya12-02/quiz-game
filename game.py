import sys
import random
import pygame

# Initialize Pygame
pygame.init()

# --- CONSTANTS & CONFIGURATION ---
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FPS = 60

# Neo-Brutalist Colors from Reference Image
COLOR_BG = (240, 240, 240)
COLOR_BLACK = (0, 0, 0)
COLOR_PURPLE = (99, 68, 209)
COLOR_PINK = (255, 117, 181)
COLOR_NEON_YELLOW = (208, 255, 67)
COLOR_WHITE = (255, 255, 255)
COLOR_LIGHT_GREY = (220, 220, 220)

# Cross-platform fonts
FONT_TITLE = pygame.font.SysFont("arial", 48, bold=True)
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
            "q": f"Is HTTP port 80 used for secure or unsecure traffic? (Q {i})",
            "options": ["Unsecure (HTTP)", "Secure (HTTPS)", "Email", "File Transfer"], "correct": "Unsecure (HTTP)"
        })
    else:
        QUESTION_POOL.append({
            "q": f"Which HTML tag is used to define an internal style sheet? (Q {i})",
            "options": ["<style>", "<script>", "<css>", "<link>"], "correct": "<style>"
        })

def draw_brutal_box(surface, rect, bg_color):
    pygame.draw.rect(surface, bg_color, rect)
    pygame.draw.rect(surface, COLOR_BLACK, rect, 4)

def draw_brutal_button(surface, rect, bg_color, text, is_hovered):
    if is_hovered:
        shadow_rect = pygame.Rect(rect.x + 6, rect.y + 6, rect.width, rect.height)
        pygame.draw.rect(surface, COLOR_BLACK, shadow_rect)
    draw_brutal_box(surface, rect, bg_color)
    text_surf = FONT_BODY.render(text, True, COLOR_BLACK)
    text_rect = text_surf.get_rect(center=rect.center)
    surface.blit(text_surf, text_rect)

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
        self.selected_questions = random.sample(QUESTION_POOL, 30)
        self.current_question_idx = 0
        self.score = 0
        self.current_round = 1
        self.selected_option = None
        self.answer_submitted = False
        self.timer_seconds = 20
        self.last_timer_event = pygame.time.get_ticks()
        self.state = "PLAYING"

    def update_timer(self):
        if self.state == "PLAYING" and not self.answer_submitted:
            now = pygame.time.get_ticks()
            if now - self.last_timer_event >= 1000:
                self.timer_seconds -= 1
                self.last_timer_event = now
                if self.timer_seconds <= 0:
                    self.answer_submitted = True

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
                            self.answer_submitted = True
                            if self.selected_option == current_q["correct"]:
                                self.score += 1
                    else:
                        next_rect = pygame.Rect(450, 560, 400, 55)
                        if next_rect.collidepoint(mouse_pos):
                            self.current_question_idx += 1
                            self.selected_option = None
                            self.answer_submitted = False
                            self.timer_seconds = 20
                            self.last_timer_event = pygame.time.get_ticks()
                            if self.current_question_idx >= 30:
                                self.state = "VICTORY_SCREEN"
                            elif self.current_question_idx == 20:
                                self.current_round = 3
                            elif self.current_question_idx == 10:
                                self.current_round = 2
                elif self.state == "VICTORY_SCREEN":
                    if pygame.Rect(350, 450, 300, 70).collidepoint(mouse_pos):
                        self.state = "MAIN_MENU"

    def render(self):
        self.screen.fill(COLOR_BG)
        mouse_pos = pygame.mouse.get_pos()
        
        if self.state == "MAIN_MENU":
            draw_brutal_box(self.screen, pygame.Rect(200, 100, 600, 200), COLOR_PURPLE)
            t_surf = FONT_TITLE.render("QUIZ GAME", True, COLOR_WHITE)
            self.screen.blit(t_surf, t_surf.get_rect(center=(500, 200)))
            sub_surf = FONT_SUBTITLE.render("100 Questions Pool | 3 Rounds | 30 Challenges", True, COLOR_BLACK)
            self.screen.blit(sub_surf, sub_surf.get_rect(center=(500, 340)))
            btn = pygame.Rect(350, 400, 300, 70)
            draw_brutal_button(self.screen, btn, COLOR_NEON_YELLOW, "START GAME", btn.collidepoint(mouse_pos))
            
        elif self.state == "PLAYING":
            current_q = self.selected_questions[self.current_question_idx]
            rq_num = (self.current_question_idx % 10) + 1
            
            # Left panel layout
            draw_brutal_box(self.screen, pygame.Rect(20, 20, 380, 660), COLOR_NEON_YELLOW)
            self.screen.blit(FONT_TITLE.render("QUIZ", True, COLOR_BLACK), (40, 50))
            self.screen.blit(FONT_TITLE.render("GAME", True, COLOR_BLACK), (40, 120))
            
            draw_brutal_box(self.screen, pygame.Rect(40, 240, 340, 120), COLOR_PURPLE)
            self.screen.blit(FONT_BODY.render(f"ROUND: {self.current_round} / 3", True, COLOR_WHITE), (60, 265))
            self.screen.blit(FONT_BODY.render(f"TOTAL Q: {self.current_question_idx + 1} / 30", True, COLOR_WHITE), (60, 310))
            
            draw_brutal_box(self.screen, pygame.Rect(40, 520, 340, 120), COLOR_PINK)
            self.screen.blit(FONT_SMALL.render("+1 Point Per Answer", True, COLOR_BLACK), (60, 550))
            self.screen.blit(FONT_SMALL.render("20 Seconds Speed Limit", True, COLOR_BLACK), (60, 580))

            # Main Question Area
            draw_brutal_box(self.screen, pygame.Rect(420, 20, 420, 50), COLOR_WHITE)
            self.screen.blit(FONT_SUBTITLE.render(f"QUESTION {rq_num} OF 10", True, COLOR_BLACK), (440, 32))
            
            draw_brutal_box(self.screen, pygame.Rect(420, 85, 420, 130), COLOR_WHITE)
            self.screen.blit(FONT_BODY.render(current_q["q"], True, COLOR_BLACK), (440, 120))

            # Render multiple options
            for idx, option in enumerate(current_q["options"]):
                opt_rect = pygame.Rect(450, 250 + (idx * 75), 400, 55)
                if not self.answer_submitted:
                    bg_col = COLOR_PINK if self.selected_option == option else COLOR_WHITE
                else:
                    if option == current_q["correct"]:
                        bg_col = COLOR_NEON_YELLOW
                    elif self.selected_option == option:
                        bg_col = COLOR_PINK
                    else:
                        bg_col = COLOR_WHITE
                draw_brutal_button(self.screen, opt_rect, bg_col, option, opt_rect.collidepoint(mouse_pos) and not self.answer_submitted)
                
                pref = pygame.Rect(420, 250 + (idx * 75), 35, 55)
                draw_brutal_box(self.screen, pref, COLOR_BLACK)
                p_txt = FONT_BODY.render(chr(65 + idx), True, COLOR_WHITE)
                self.screen.blit(p_txt, p_txt.get_rect(center=pref.center))

            # Bottom Action Bar
            action_rect = pygame.Rect(450, 560, 400, 55)
            btn_label = "NEXT CHALLENGE" if self.answer_submitted else "SUBMIT ANSWER"
            can_press = self.answer_submitted or (self.selected_option is not None)
            draw_brutal_button(self.screen, action_rect, COLOR_PURPLE if can_press else COLOR_LIGHT_GREY, btn_label, action_rect.collidepoint(mouse_pos) and can_press)

            # Scoreboard and Timer components
            draw_brutal_box(self.screen, pygame.Rect(860, 20, 120, 40), COLOR_PINK)
            self.screen.blit(FONT_SMALL.render("SCORE", True, COLOR_BLACK), (895, 30))
            draw_brutal_box(self.screen, pygame.Rect(860, 60, 120, 90), COLOR_WHITE)
