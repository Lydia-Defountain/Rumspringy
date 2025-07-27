import pygame
from constants import ZONES

class ToastManager:
    def __init__(self, max_toasts=4):
        self.toasts = []
        self.max_toasts = max_toasts
        self.font = pygame.font.Font(None, 28)
        self.toast_pos = ZONES["toast_area"]
        self.default_duration = 360  # 6 seconds at 60 FPS
        self.linger_duration = 120 
        self.persistent_duration = 9999  # Very long duration for persistent
    
    def show_toast(self, message, duration=None, toast_type="info"):
        """Show a toast message with queue management"""
        

        if duration is None:
            if len(self.toasts) < self.max_toasts:
                duration = self.persistent_duration  # Stay until pushed out
    
            else:
                duration = self.default_duration  # Normal duration when at capacity
                
            
            
        colors = {
            "info": (200, 100, 255),      # Purple
            "success": (100, 255, 100),   # Green
            "warning": (255, 255, 100),   # Yellow
            "error": (255, 100, 100),     # Red
            "computer": (255, 150, 100),  # Orange for computer actions
            "turn": (100, 200, 255)       # Light blue for turn info
        }
        
        toast = {
            "message": message,
            "timer": duration,
            "original_duration": duration,
            "color": colors.get(toast_type, colors["info"]),
            "type": toast_type,
            "is_lingering": False,
            "is_persistent": duration == self.persistent_duration
        }
        
        


        
        self.toasts.append(toast)
        
        
        if len(self.toasts) > self.max_toasts:
            self._start_linger_oldest()

    def _start_linger_oldest(self):
        """Start linger timer for oldest toast if not already lingering"""
        for toast in self.toasts:
            if not toast["is_lingering"]:
                toast["is_lingering"] = True
                toast["timer"] = self.linger_duration
                toast["is_persistent"] = False  # No longer persistent
                break
    
    def update(self):
        """Update toast timers and manage queue"""
        

        for toast in self.toasts[:]:
            # Only decrement timer for non-persistent toasts or lingering toasts
            if not toast["is_persistent"] or toast["is_lingering"]:
                toast["timer"] -= 1
                

                # Only remove expired toasts if they're not persistent OR they're lingering
                if toast["timer"] <= 0:
                    self.toasts.remove(toast)
                    
                    continue
            
    
        
        # If still have too many toasts, continue lingering process
        if len(self.toasts) > self.max_toasts:
            # Find the oldest non-lingering toast
            oldest_non_lingering = None
            for toast in self.toasts:
                if not toast["is_lingering"]:
                    oldest_non_lingering = toast
                    break
            
            if oldest_non_lingering:
                oldest_non_lingering["is_lingering"] = True
                oldest_non_lingering["timer"] = self.linger_duration
                oldest_non_lingering["is_persistent"] = False
            else:
                # All toasts are lingering, remove the first one
                self.toasts.pop(0)

    
    def draw(self, screen):
        """Draw all active toasts with fade effect for lingering ones"""
        for i, toast in enumerate(self.toasts):
            y_pos = self.toast_pos[1] + (i * 35) 
            
            # Calculate alpha for fade effect on lingering toasts
            alpha = 255
            if toast["is_lingering"]:
                # Fade out during linger period
                fade_progress = toast["timer"] / self.linger_duration
                alpha = int(255 * fade_progress * 0.7)  # Max 70% opacity when lingering
            
            # Create toast background
            text_surface = self.font.render(toast["message"], True, toast["color"])
            text_rect = text_surface.get_rect()
            text_rect.x = self.toast_pos[0] + 10
            text_rect.y = y_pos
            
            # Toast background with padding
            bg_rect = text_rect.inflate(16, 6)
            
            # Semi-transparent background with fade
            bg_surface = pygame.Surface((bg_rect.width, bg_rect.height))
            bg_alpha = min(alpha, 180)
            bg_surface.set_alpha(bg_alpha)
            bg_surface.fill((0, 0, 0))
            screen.blit(bg_surface, bg_rect)
            
            # Border
            pygame.draw.rect(screen, toast["color"], bg_rect, 2)
            
            # Text with fade
            if alpha < 255:
                text_surface.set_alpha(alpha)
            screen.blit(text_surface, text_rect)
    
    def clear_all(self):
        """Clear all toasts (useful for new game)"""
        self.toasts.clear()