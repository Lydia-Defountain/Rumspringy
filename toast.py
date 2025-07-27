import pygame
from constants import ZONES

class ToastManager:
    def __init__(self, max_toasts=4):
        self.toasts = []
        self.max_toasts = max_toasts
        self.font = pygame.font.Font(None, 28)
        self.toast_pos = ZONES["toast_area"]
        self.linger_duration = 120  # 2 seconds at 60 FPS
        
        # Simple FIFO message queue
        self.message_queue = []
        self.message_delay = 60  # 2 seconds between messages at 60 FPS
    
    def show_toast(self, message, duration=None, toast_type="info"):
        """Show a toast message - simple FIFO queue"""
        # Calculate delay based on queue position
        if self.message_queue:
            # Each message waits for the previous one + delay
            last_delay = max(msg["delay_timer"] for msg in self.message_queue)
            delay_timer = last_delay + self.message_delay
        else:
            # First message shows immediately
            delay_timer = 0
        
        queued_message = {
            "message": message,
            "duration": duration,  # None for persistent
            "toast_type": toast_type,
            "delay_timer": delay_timer
        }
        
        self.message_queue.append(queued_message)
    
    def _post_toast(self, message, duration, toast_type):
        """Actually create and post the toast"""
        colors = {
            "info": (200, 100, 255),
            "success": (100, 255, 100),
            "warning": (255, 255, 100),
            "error": (255, 100, 100),
            "computer": (255, 150, 100),
            "turn": (100, 200, 255)
        }
        
        toast = {
            "message": message,
            "timer": duration,  # None for persistent, number for timed
            "color": colors.get(toast_type, colors["info"]),
            "type": toast_type,
            "is_lingering": False
        }
        
        self.toasts.append(toast)
        self._manage_queue()
    
    def _manage_queue(self):
        """Manage the toast queue when new toasts are added"""
        excess_count = len(self.toasts) - self.max_toasts
        
        if excess_count > 0:
            # Start lingering for the oldest excess toasts
            lingered_count = 0
            for toast in self.toasts:
                if not toast["is_lingering"] and lingered_count < excess_count:
                    toast["is_lingering"] = True
                    toast["timer"] = self.linger_duration
                    lingered_count += 1
    
    def update(self):
        """Update toast timers and process message queue"""
        # Process message queue
        for queued_message in self.message_queue[:]:
            queued_message["delay_timer"] -= 1
            if queued_message["delay_timer"] <= 0:
                self._post_toast(
                    queued_message["message"],
                    queued_message["duration"],
                    queued_message["toast_type"]
                )
                self.message_queue.remove(queued_message)
        
        # Update existing toast timers
        for toast in self.toasts[:]:
            if toast["timer"] is not None:
                toast["timer"] -= 1
                
                if toast["timer"] <= 0:
                    self.toasts.remove(toast)
    
    def draw(self, screen):
        """Draw all active toasts with fade effect for lingering ones"""
        for i, toast in enumerate(self.toasts):
            y_pos = self.toast_pos[1] + (i * 35)
            
            # Only fade if lingering
            alpha = 255
            if toast["is_lingering"] and toast["timer"] is not None:
                # Fade out during linger period
                fade_progress = toast["timer"] / self.linger_duration
                alpha = int(255 * fade_progress * 0.7)
            
            # Create toast background
            text_surface = self.font.render(toast["message"], True, toast["color"])
            text_rect = text_surface.get_rect()
            text_rect.x = self.toast_pos[0] + 10
            text_rect.y = y_pos
            
            # Toast background with padding
            bg_rect = text_rect.inflate(16, 6)
            
            # Semi-transparent background
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
        """Clear all toasts and queued messages"""
        self.toasts.clear()
        self.message_queue.clear()
