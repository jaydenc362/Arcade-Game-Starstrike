# Collisions class
class Collisions:
    def circle_rect_collision(circle_position, radius, rect):
        closest_x = max(rect.left, min(circle_position.x, rect.right))
        closest_y = max(rect.top, min(circle_position.y, rect.bottom))
        dx = circle_position.x - closest_x
        dy = circle_position.y - closest_y
        return dx * dx + dy * dy <= radius * radius

    def rect_rect_collision(a, b):
        return a.colliderect(b)

    def circle_circle_collision(a_position, a_radius, b_position, b_radius):
        dx = a_position.x - a_radius.x
        dy = a_position.y - a_radius.y
        radius_sum = a_radius + b_radius
        return dx * dx + dy * dy <= radius_sum * radius_sum