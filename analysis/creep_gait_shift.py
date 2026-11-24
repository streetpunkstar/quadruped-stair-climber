#!/usr/bin/env python3
"""Creep-gait weight-shift check for the quadruped.

For each leg lift, the other three feet form a support triangle. The body CG
(projected to the ground) must sit inside that triangle with a stability margin.
This script reports how far the body must shift, and the tip-over tilt angle that
margin gives at the CG height.

Frame: x forward, y left, millimetres. Everything is a parameter so the check can
be re-run when CAD, mass properties or hip spacing change. Stdlib only.

Usage:
    python3 creep_gait_shift.py                    # defaults (placeholders)
    python3 creep_gait_shift.py --wheelbase 360 --cg-x 10 --cg-y 0
    python3 creep_gait_shift.py --sweep            # wheelbase / CG-offset sensitivity
"""
import argparse
import itertools
import math

LEGS = ["FL", "FR", "RL", "RR"]
GAIT_ORDER = ["RR", "FR", "RL", "FL"]  # a common creep order; change to suit


def feet_positions(wheelbase, track, foot_dx, foot_dy):
    """Foot ground positions. Hips at (+/-wheelbase/2, +/-track/2).
    foot_dx: fore-aft offset of each foot from its hip (stride offset).
    foot_dy: outward lateral offset of each foot from its hip (ab/ad L1, if any)."""
    hx, hy = wheelbase / 2.0, track / 2.0
    return {
        "FL": (hx + foot_dx, hy + foot_dy),
        "FR": (hx + foot_dx, -hy - foot_dy),
        "RL": (-hx + foot_dx, hy + foot_dy),
        "RR": (-hx + foot_dx, -hy - foot_dy),
    }


def triangle_halfplanes(tri):
    """Inward unit normals and offsets: n.p >= c for points inside the triangle."""
    cx = sum(p[0] for p in tri) / 3.0
    cy = sum(p[1] for p in tri) / 3.0
    planes = []
    for a, b in ((0, 1), (1, 2), (2, 0)):
        (x1, y1), (x2, y2) = tri[a], tri[b]
        nx, ny = -(y2 - y1), (x2 - x1)
        norm = math.hypot(nx, ny)
        nx, ny = nx / norm, ny / norm
        c = nx * x1 + ny * y1
        if nx * cx + ny * cy < c:  # flip so the interior is on the >= side
            nx, ny, c = -nx, -ny, -c
        planes.append((nx, ny, c))
    return planes


def edge_margin(p, planes):
    return min(nx * p[0] + ny * p[1] - c for nx, ny, c in planes)


def min_shift(cg, planes, margin):
    """Smallest move of cg so it is at least `margin` inside every edge."""
    if edge_margin(cg, planes) >= margin - 1e-9:
        return cg
    shifted = [(nx, ny, c + margin) for nx, ny, c in planes]
    cands = []
    for nx, ny, c in shifted:  # projection onto each shifted edge line
        d = nx * cg[0] + ny * cg[1] - c
        cands.append((cg[0] - d * nx, cg[1] - d * ny))
    for (n1x, n1y, c1), (n2x, n2y, c2) in itertools.combinations(shifted, 2):
        det = n1x * n2y - n1y * n2x  # vertices of the inset triangle
        if abs(det) > 1e-9:
            cands.append(((c1 * n2y - c2 * n1y) / det, (n1x * c2 - n2x * c1) / det))
    ok = [p for p in cands if all(nx * p[0] + ny * p[1] >= c - 1e-6 for nx, ny, c in shifted)]
    if not ok:
        return None  # triangle too small for this margin
    return min(ok, key=lambda p: math.dist(p, cg))


def analyse(wheelbase, track, foot_dx, foot_dy, cg_x, cg_y, cg_h, margin):
    feet = feet_positions(wheelbase, track, foot_dx, foot_dy)
    cg = (cg_x, cg_y)
    rows = []
    for lift in GAIT_ORDER:
        tri = [feet[l] for l in LEGS if l != lift]
        planes = triangle_halfplanes(tri)
        before = edge_margin(cg, planes)
        target = min_shift(cg, planes, margin)
        if target is None:
            rows.append((lift, before, None, None, None, None))
            continue
        shift = math.dist(target, cg)
        after = edge_margin(target, planes)
        tilt = math.degrees(math.atan2(after, cg_h))
        dx, dy = target[0] - cg[0], target[1] - cg[1]
        rows.append((lift, before, shift, (dx, dy), after, tilt))
    return rows


def print_report(rows, args):
    mm_in = 25.4
    print(f"wheelbase {args.wheelbase:.0f} mm | track {args.track:.0f} mm | "
          f"foot offset dx {args.foot_dx:.0f} dy {args.foot_dy:.0f} mm")
    print(f"CG ({args.cg_x:.0f}, {args.cg_y:.0f}) mm | CG height {args.cg_h:.0f} mm | "
          f"required margin {args.margin:.0f} mm\n")
    print(f"{'lift':<5}{'margin now':>11}{'shift mm':>10}{'shift in':>10}{'move (dx,dy) mm':>20}{'tilt tol':>10}")
    for lift, before, shift, move, after, tilt in rows:
        if shift is None:
            print(f"{lift:<5}{before:>9.1f}mm   support triangle too small for this margin")
            continue
        print(f"{lift:<5}{before:>9.1f}mm{shift:>10.1f}{shift / mm_in:>10.2f}"
              f"{f'({move[0]:+.1f}, {move[1]:+.1f})':>20}{tilt:>9.1f}°")
    shifts = [r[2] for r in rows if r[2] is not None]
    if shifts:
        print(f"\nworst-case shift: {max(shifts):.1f} mm ({max(shifts) / mm_in:.2f} in)")


def sweep(args):
    print("Worst-case shift (mm) vs wheelbase and CG fore-aft offset")
    cgs = (-20, -10, 0, 10, 20)
    print(f"{'wheelbase':>10}" + "".join(f"{f'cg_x={c:+d}':>11}" for c in cgs))
    for wb in (320, 340, 360, 380, 400):
        cells = []
        for c in cgs:
            rows = analyse(wb, args.track, args.foot_dx, args.foot_dy, c, args.cg_y, args.cg_h, args.margin)
            s = [r[2] for r in rows if r[2] is not None]
            cells.append(f"{max(s):>11.1f}" if s else f"{'n/a':>11}")
        print(f"{wb:>10}" + "".join(cells))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--wheelbase", type=float, default=340.0, help="front-to-rear hip spacing, mm (CAD placeholder)")
    ap.add_argument("--track", type=float, default=370.0, help="left-to-right hip spacing, mm (360-380 design range)")
    ap.add_argument("--foot-dx", type=float, default=0.0, help="foot fore-aft offset from hip, mm")
    ap.add_argument("--foot-dy", type=float, default=0.0, help="foot outward lateral offset from hip, mm")
    ap.add_argument("--cg-x", type=float, default=0.0, help="CG fore-aft offset from body centre, mm (+ forward)")
    ap.add_argument("--cg-y", type=float, default=0.0, help="CG lateral offset from body centre, mm (+ left)")
    ap.add_argument("--cg-h", type=float, default=305.0, help="CG height above ground, mm (~nominal standing height until CAD gives a real value)")
    ap.add_argument("--margin", type=float, default=35.0, help="required CG distance inside support-triangle edge, mm")
    ap.add_argument("--sweep", action="store_true", help="print wheelbase / CG-offset sensitivity table")
    args = ap.parse_args()
    if args.sweep:
        sweep(args)
    else:
        print_report(analyse(args.wheelbase, args.track, args.foot_dx, args.foot_dy,
                             args.cg_x, args.cg_y, args.cg_h, args.margin), args)


if __name__ == "__main__":
    main()
