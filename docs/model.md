# Model and simulation monitors

## Assumptions

The world is an exactly known, bounded rectangular road in a planar metre-based
coordinate system: x east, y north. All footprints remain axis aligned. A heading
of 0 or 180 is descriptive; the demonstration permits sideways translation
without changing heading. Each step moves the centre on a straight line at
constant translational speed. Actions describe the interval ending at that frame.
Initial frame speeds are zero; configured speeds are cruise commands.

A starts already inside the bay. B travels west while A waits. Once B is behind
A with a scripted extra gap, A translates sideways to the lane and then travels
east. Speed and direction change instantly; acceleration, braking dynamics,
steering, wheelbase, turning radius, reversing and route planning are absent.
A rectangular gap does not prove a real car could steer into or out of it.

The road is the full rectangular drivable envelope, including the labeled passing
space. Parked rectangles block its north side except at the gap. The passing
space label is not an additional obstacle or a separate road polygon.

## Contact and clearance

Vehicle/vehicle and vehicle/obstacle rectangles are **closed**: edge or corner
contact is classified as `collision`, even without positive-area overlap.
This deliberately conservative contact rule is distinct from a `clearance`
violation, where physical rectangles do not touch but the required margin fails.

For each pair, let gx and gy be signed axis gaps (negative means overlapping
projections). Collision means gx <= 0 and gy <= 0. Clearance violation means
gx < c and gy < c after excluding collision. Thus exact c is allowed. This is
L-infinity/square clearance, not Euclidean distance; diagonal separations can be
rejected conservatively. No floating-point tolerance is applied. Near-equality
decimal inputs should be interpreted with normal binary floating-point limits.

Road-edge contact is a `road boundary` violation. Otherwise a vehicle must lie
inside the road inset by c; an exact c boundary gap is allowed for c > 0. With
c = 0, strict interior is still required. Static obstacles may touch the road
edge, but cannot overlap/contact one another or the passing-space rectangle.
Passing-space boundary contact with the road is allowed. Initially all moving
vehicles must satisfy the same monitored constraints as subsequent steps.

## Between-frame checks and termination

`monitor.py` is separate from the script. It checks each translated rectangle
against static obstacles and every other vehicle using continuous relative-motion
slab intersection over the entire normalized time interval [0, 1]. Physical contact
uses a closed forbidden rectangle; clearance uses an open expanded rectangle.
This detects tunneling through thin obstacles and vehicles exchanging positions
between frames. The rectangular road inset is convex: endpoint containment implies
segment containment for fixed footprints. Proposed identity, heading or size changes
and nonfinite positions are rejected.

Monitoring rejects the entire unsafe step and stops the run; no rollback animation
or movement up to an estimated contact instant is attempted. Accepted frames remain
safe under this model. `violation` takes precedence over success. `success` means
both exact scripted destinations were reached; it does not mean the encounter
was optimally resolved. Otherwise the run ends `timeout` after floor(duration/dt)
steps, so a non-divisible duration ends at the last full step before the bound.

No sensors, uncertainty, latency, communication protocol, local independent
decision-making or safety certification are modeled. The current global monitor
cannot establish that future decentralized controllers enforce their own safety.
