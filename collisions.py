# Collisions class
class Collisions:
    def circle_rect_collision(circle_pos, radius, rect):
        closest_x = max(rect.left, min(circle_pos.x, rect.right))
        closest_y = max(rect.top, min(circle_pos.y, rect.bottom))
        dx = circle_pos.x - closest_x
        dy = circle_pos.y - closest_y
        return dx * dx + dy * dy <= radius * radius