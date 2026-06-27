import math
 
 
def find_angle_ABC(a, b, c, d, theta_deg):
    """
    Given quadrilateral ABCD with:
      AB = a, BC = b, CD = c, AD = d
      angle DAB = theta (in degrees)
 
    Returns angle ABC = x (in degrees).
 
    Strategy:
      1. Place A at the origin, B along the positive x-axis.
      2. Compute positions of A, B, D using theta.
      3. C lies on the intersection of:
           - circle centred at B with radius b  (BC = b)
           - circle centred at D with radius c  (CD = c)
      4. Pick the intersection point that keeps the quadrilateral
         convex / non-self-intersecting (C on the correct side).
      5. Compute angle ABC from vectors BA and BC.
    """
 
    theta = math.radians(theta_deg)
 
    # --- Place vertices ---
    A = (0.0, 0.0)
    B = (a, 0.0)
    D = (d * math.cos(theta), d * math.sin(theta))
 
    # --- Find C: intersection of circle(B, b) and circle(D, c) ---
    # Two circles:  |C - B|² = b²   and   |C - D|² = c²
    # Let dx, dy = D - B
    Bx, By = B
    Dx, Dy = D
 
    dx = Dx - Bx
    dy = Dy - By
    dist_BD = math.hypot(dx, dy)
 
    if dist_BD > b + c:
        raise ValueError(
            f"No solution: BD = {dist_BD:.4f} > b + c = {b + c:.4f}. "
            "The quadrilateral cannot close."
        )
    if dist_BD < abs(b - c):
        raise ValueError(
            f"No solution: BD = {dist_BD:.4f} < |b - c| = {abs(b - c):.4f}. "
            "One circle is inside the other."
        )
 
    # Distance from B to the radical axis along BD
    # (standard two-circle intersection formula)
    alpha = (b**2 - c**2 + dist_BD**2) / (2 * dist_BD)
 
    # Half-chord length
    h_sq = b**2 - alpha**2
    if h_sq < 0:
        h_sq = 0.0          # numerical clamp
    h = math.sqrt(h_sq)
 
    # Unit vector along BD and its perpendicular
    ux, uy = dx / dist_BD, dy / dist_BD   # along BD
    px, py = -uy, ux                       # perpendicular (rotated 90° CCW)
 
    # Midpoint of the chord
    mx = Bx + alpha * ux
    my = By + alpha * uy
 
    # Two candidate positions for C
    C1 = (mx + h * px, my + h * py)
    C2 = (mx - h * px, my - h * py)
 
    # --- Choose the correct C ---
    # For a simple (non-self-intersecting) quadrilateral ABCD,
    # C should be on the opposite side of line AB from D
    # when the quadrilateral is convex, OR we pick the candidate
    # that gives a positive (CCW) orientation for the quad.
    #
    # General rule: in a simple quadrilateral ABCD traversed CCW,
    # the signed area should be positive. We pick the C that gives
    # a larger (positive) signed area.
 
    def signed_area(C):
        """Shoelace signed area for quad A->B->C->D."""
        pts = [A, B, C, D]
        n = len(pts)
        s = 0.0
        for i in range(n):
            x1, y1 = pts[i]
            x2, y2 = pts[(i + 1) % n]
            s += x1 * y2 - x2 * y1
        return s / 2.0
 
    # Pick the C with larger signed area (more CCW / less self-intersecting)
    C = C1 if signed_area(C1) >= signed_area(C2) else C2
 
    # --- Compute angle ABC ---
    # Vectors from B to A and from B to C
    BAx, BAy = A[0] - B[0], A[1] - B[1]
    BCx, BCy = C[0] - B[0], C[1] - B[1]
 
    cos_x = (BAx * BCx + BAy * BCy) / (math.hypot(BAx, BAy) * math.hypot(BCx, BCy))
    cos_x = max(-1.0, min(1.0, cos_x))   # clamp for floating-point safety
    x = math.degrees(math.acos(cos_x))
 
    return x, C
 
 
# ---------------------------------------------------------------------------
# Example / demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("Quadrilateral ABCD — find angle ABC (x)")
    print("=" * 45)
 
    # --- Get input from user ---
    try:
        a     = float(input("Enter AB (a)          : "))
        b     = float(input("Enter BC (b)          : "))
        c     = float(input("Enter CD (c)          : "))
        d     = float(input("Enter AD (d)          : "))
        theta = float(input("Enter angle DAB (deg) : "))
 
        x, C = find_angle_ABC(a, b, c, d, theta)
 
        print()
        print(f"  C is at coordinates : ({C[0]:.6f}, {C[1]:.6f})")
        print(f"  Angle ABC (x)       : {x:.6f}°")
 
    except ValueError as e:
        print(f"\nError: {e}")
 
    # --- Built-in sanity check: a square ---
    print()
    print("Sanity check — unit square (expect x = 90°):")
    x_sq, _ = find_angle_ABC(a=1, b=1, c=1, d=1, theta_deg=90)
    print(f"  Angle ABC = {x_sq:.6f}°  ✓" if abs(x_sq - 90) < 1e-9
          else f"  Angle ABC = {x_sq:.6f}°  ✗ (unexpected)")
 
    print()
    print("Sanity check — rectangle 3×4 (expect x = 90°):")
    x_rect, _ = find_angle_ABC(a=3, b=4, c=3, d=4, theta_deg=90)
    print(f"  Angle ABC = {x_rect:.6f}°  ✓" if abs(x_rect - 90) < 1e-9
          else f"  Angle ABC = {x_rect:.6f}°  ✗ (unexpected)")