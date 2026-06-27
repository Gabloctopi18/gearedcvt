"""
quadrilateral.py
================
Plots angle ABC (x) vs time t, where angle DAB = theta = k*t.

Mathematical approach
---------------------
Diagonal BD splits ABCD into two triangles. Everything is closed-form:

  Step 1 — BD from Law of Cosines in triangle ABD:
      BD²(θ) = a² + d² − 2ad·cos θ

  Step 2 — Sub-angles at B from Law of Cosines in each triangle:
      cos(∠ABD) = (a − d·cos θ) / BD
      cos(∠DBC) = (b² + BD² − c²) / (2b·BD)

  Step 3 — Branch selection:
      sin θ ≥ 0  →  D above AB  →  x = ∠ABD + ∠DBC
      sin θ < 0  →  D below AB  →  x = |∠ABD − ∠DBC|

  Step 4 — Admissible range: quad exists iff |b−c| < BD < b+c.
      Solved analytically: cos θ = (a²+d²−R²)/(2ad) for R = b+c and |b−c|.

  Step 5 — Derivative dx/dθ computed analytically (chain rule) for
      adaptive sampling — more points where the curve is steepest.
"""

import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.collections import LineCollection


# ─────────────────────────────────────────────────────────────────────────────
# CLOSED-FORM  x(θ)
# ─────────────────────────────────────────────────────────────────────────────

def x_of_theta(theta: float, a: float, b: float, c: float, d: float):
    """
    Closed-form angle ABC (radians) for angle DAB = theta (radians).
    Returns None when the quadrilateral cannot close at this theta.
    """
    BD2 = a**2 + d**2 - 2*a*d * math.cos(theta)
    if BD2 <= 0:
        return None
    BD = math.sqrt(BD2)
    if BD >= b + c or BD <= abs(b - c):
        return None

    cos_ABD = max(-1.0, min(1.0, (a - d * math.cos(theta)) / BD))
    cos_DBC = max(-1.0, min(1.0, (b**2 + BD2 - c**2) / (2 * b * BD)))

    ABD = math.acos(cos_ABD)
    DBC = math.acos(cos_DBC)

    return ABD + DBC if math.sin(theta) >= 0 else abs(ABD - DBC)


# ─────────────────────────────────────────────────────────────────────────────
# ANALYTIC DERIVATIVE  dx/dθ  (used for adaptive sampling)
# ─────────────────────────────────────────────────────────────────────────────

def dx_dtheta(theta: float, a: float, b: float, c: float, d: float):
    """
    Analytic derivative of x(θ).

      BD' = dBD/dθ = ad·sin θ / BD

      f₁ = cos(∠ABD) = (a − d cos θ) / BD
      f₁' = (d sin θ − f₁ · BD') / BD
      d(∠ABD)/dθ = −f₁' / √(1 − f₁²)

      f₂ = cos(∠DBC) = (b² + BD² − c²) / (2b·BD)
      f₂' = BD' · (b² − BD² + c²) / (2b·BD²)
      d(∠DBC)/dθ = −f₂' / √(1 − f₂²)
    """
    BD2 = a**2 + d**2 - 2*a*d * math.cos(theta)
    if BD2 <= 0:
        return None
    BD = math.sqrt(BD2)
    if BD >= b + c or BD <= abs(b - c):
        return None

    sin_t  = math.sin(theta)
    BD_dot = a * d * sin_t / BD

    f1 = max(-1.0 + 1e-12, min(1.0 - 1e-12, (a - d * math.cos(theta)) / BD))
    f1_dot = (d * sin_t - f1 * BD_dot) / BD
    dABD   = -f1_dot / math.sqrt(1 - f1**2)

    f2 = max(-1.0 + 1e-12, min(1.0 - 1e-12, (b**2 + BD2 - c**2) / (2 * b * BD)))
    f2_dot = BD_dot * (b**2 - BD2 + c**2) / (2 * b * BD2)
    dDBC   = -f2_dot / math.sqrt(1 - f2**2)

    if sin_t >= 0:
        return dABD + dDBC
    else:
        sign = 1 if math.acos(f1) >= math.acos(f2) else -1
        return sign * (dABD - dDBC)


# ─────────────────────────────────────────────────────────────────────────────
# ADMISSIBLE RANGE OF θ
# ─────────────────────────────────────────────────────────────────────────────

def admissible_theta_range(a: float, b: float, c: float, d: float,
                           margin: float = 1e-6):
    """Largest contiguous θ-interval in (0, 2π) where the quad can close."""
    def critical_thetas(R):
        val = (a**2 + d**2 - R**2) / (2 * a * d)
        if abs(val) > 1.0:
            return []
        base = math.acos(max(-1.0, min(1.0, val)))
        return [base, 2*math.pi - base]

    boundaries = sorted({0.0, 2*math.pi}
                        | set(critical_thetas(b + c))
                        | set(critical_thetas(abs(b - c))))

    valid = []
    for lo, hi in zip(boundaries, boundaries[1:]):
        if x_of_theta((lo + hi) / 2, a, b, c, d) is not None:
            valid.append((lo + margin, hi - margin))

    if not valid:
        raise ValueError("No valid θ range — check that the side lengths "
                         "can form a quadrilateral.")
    return valid[0][0], valid[-1][1]


# ─────────────────────────────────────────────────────────────────────────────
# ADAPTIVE SAMPLING
# ─────────────────────────────────────────────────────────────────────────────

def adaptive_samples(a: float, b: float, c: float, d: float, n: int = 800):
    """θ samples concentrated where |dx/dθ| is largest (inverse-CDF method)."""
    lo, hi  = admissible_theta_range(a, b, c, d)
    coarse  = np.linspace(lo, hi, n)
    weights = np.array([abs(dx_dtheta(t, a, b, c, d) or 0.0) for t in coarse])
    total   = weights.sum()
    if total == 0:
        return coarse
    cdf   = np.cumsum(weights) / total
    extra = np.interp(np.random.default_rng(42).uniform(0, 1, n // 2), cdf, coarse)
    return np.sort(np.concatenate([coarse, extra]))


# ─────────────────────────────────────────────────────────────────────────────
# GRAPH
# ─────────────────────────────────────────────────────────────────────────────

def graph_angle_x(a: float, b: float, c: float, d: float,
                  k: float = 1.0,
                  n_samples: int = 800,
                  output_file: str = "angle_x_graph.png") -> None:
    """
    Plot angle ABC (degrees) vs time t, where theta(t) = k*t.

    Parameters
    ----------
    a, b, c, d  : side lengths AB, BC, CD, AD
    k           : angular speed in rad/time-unit  (theta = k*t)
    n_samples   : number of sample points
    output_file : path to save the PNG
    """
    thetas = adaptive_samples(a, b, c, d, n=n_samples)
    # Repeat three periods (θ, θ+2π, θ+4π) so the plot shows 3 cycles
    thetas_full = np.concatenate([thetas + 2 * math.pi * m for m in range(3)])
    times  = thetas_full / k                                   # t = θ / k
    xs_deg = np.degrees([x_of_theta(t, a, b, c, d) for t in thetas_full])

    # ── Figure ───────────────────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(11, 5))
    fig.patch.set_facecolor("#0f1117")
    ax.set_facecolor("#0f1117")

    # Gradient line coloured by the angle value
    pts      = np.array([times, xs_deg]).T.reshape(-1, 1, 2)
    segments = np.concatenate([pts[:-1], pts[1:]], axis=1)
    norm     = plt.Normalize(xs_deg.min(), xs_deg.max())
    lc       = LineCollection(segments, cmap="plasma", norm=norm, linewidth=2.5)
    lc.set_array(xs_deg[:-1])
    ax.add_collection(lc)
    ax.set_xlim(times[0], times[-1])
    ax.set_ylim(xs_deg.min() - 8, xs_deg.max() + 8)

    # Colourbar
    cbar = fig.colorbar(lc, ax=ax, pad=0.015)
    cbar.set_label("∠ABC (degrees)", color="#e0e0e0", fontsize=11)
    cbar.ax.yaxis.set_tick_params(color="#e0e0e0")
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color="#e0e0e0")

    # Annotate min / max
    for idx, label, dy in [(xs_deg.argmin(), f"min {xs_deg.min():.1f}°",  10),
                           (xs_deg.argmax(), f"max {xs_deg.max():.1f}°", -16)]:
        ax.plot(times[idx], xs_deg[idx], "o", color="white", ms=6, zorder=5)
        ax.annotate(label, xy=(times[idx], xs_deg[idx]),
                    xytext=(8, dy), textcoords="offset points",
                    color="white", fontsize=9)

    # Styling
    for spine in ax.spines.values():
        spine.set_color("#444")
    ax.tick_params(colors="#e0e0e0")
    for lbl in (ax.xaxis.label, ax.yaxis.label, ax.title):
        lbl.set_color("#e0e0e0")
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter("%.1f°"))
    ax.grid(True, color="#2a2a2a", linewidth=0.7, linestyle="--")

    k_str = f"{k:g}"
    ax.set_xlabel(f"time  t      (θ = {k_str}·t  rad)", fontsize=12)
    ax.set_ylabel("∠ABC  x  (degrees)", fontsize=12)
    ax.set_title(
        f"Angle ABC vs time  —  ABCD: a={a}, b={b}, c={c}, d={d},  k={k_str}",
        fontsize=13, pad=12,
    )

    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    print(f"Saved → {output_file}")
    plt.close()


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    a, b, c, d = 55, 15.05443, 56.36918, 11
    k          = 5.0
    graph_angle_x(a, b, c, d, k=k, output_file="angle_x_graph.png")