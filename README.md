# wheels-of-steele
A vehicle sim project

## Description
A study project for developing python skils in a data driven mechanical engineering context.

## What the sim is
Initially, it will be a longitudinal vehicle dynamics model, to produce a drive cycle comparison tool. So I can run the same drive cycle (WLTP, NEDC, a custom trace to represent a lap of a motorsport circuit) across different powertrains including ICE (various configurations), BEV, hybrid and then compare fuel and energy use.

Given the cycle's velocity over time, compute the force, torque and power demanded, then the fuel or energy consumed to arrive at a comparable "fuel economy" figure.

# Approach and conventions
- The sim will use SI units and convert on the boundary of passing information in and out, this will likely be a source of bugs which may take time to spot without careful handling.
- The intention is to use a Test Driven Development (TDD) approach for writing the code as good practice to catch issues early.
    - Once a skelton sim exists Behaviour Driven Development (BDD) may be useful, so review this in due course.


## Plan is continual WIP ;-)
1. Build a road-load calc in Python with a plot.
1. Road-load model: aero drag + rolling resistance + grade vs speed.
1. Steady-state consumption: introduce a BSFC map (ICE) or efficiency map (motor) at fixed speed.
1. Drive-cycle sim: ingest a cycle, run quasi-static, output L/100km or kWh/100km. (First "real" result.)
1. (prob worth setting up main branch and CI to run tests at this point?)
1. Swappable powertrains: ICE vs BEV vs hybrid on the same cycle — the comparison.
1. Gearing and operating points.
1. Forward-facing sim with a driver/PID model — introduces time-stepping and ODE integration
1. Lap-time sim: add a grip/curvature model.
1. Future: Optimisation, validation against real data, a small dashboard.

## Notes for future review?
- pint for baking units into variables? vs pydantic?
- vs pre-commit or llm to check that all variables hae units in name?
