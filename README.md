# VR Physics Puzzle Sandbox: an interactive physics lab

A room-scale VR physics puzzle game for Unity 6.3 (URP). You grab, throw, stack and freeze
physics objects to get a glowing orb into the goal. There are twelve puzzles and a free-play sandbox.
Each puzzle is timed and rated with 1–3 stars, and step-by-step tips are there if you get stuck.
It also runs with mouse and keyboard when no headset is connected.

## Purpose

Physics is often taught from formulas on a board, and many schools have no laboratory equipment.
This project is a **virtual physics laboratory**: every puzzle is built around one law of physics,
so students learn it by doing it, then see the formula behind what they just did.

- **One concept per level.** The lesson board on the lectern (and the HUD card, `L`) shows the concept,
  its formula, a plain explanation and where it is used in real life.
- **Lab meter.** Grab or aim at any object to read its mass, speed, height, kinetic and potential energy,
  momentum and weight, live.
- **Theory vs. measurement.** Every throw is measured (launch speed and angle, peak height, distance,
  flight time) and the measured peak is compared with `h = h₀ + (v₀·sinθ)² / 2g`.
- **Trajectory preview** (desktop, `T`): while holding an object, the parabola a throw would follow is drawn,
  with its landing point.
- **Quick check.** After every solved puzzle a board with a three-option question about its concept appears in front
  of the player (poke, laser-point or click A / B / C). Wrong answers get an explanation; passed quizzes show on the Level Select board.
- **Lab report.** Every solve (time, stars, last measured throw: speed, angle, measured and predicted peak) and every quiz
  answer is appended to `LabReport.csv` in `Application.persistentDataPath`, ready to open in Excel and hand in. `J` opens the folder.
- **English / Uzbek.** Lessons, quizzes and their labels switch language with `U` or the EN / UZ button on the lesson board.
- **Motivation.** Par times, stars and records turn practice into a game; the sandbox is for the player's own experiments.

Who it is for: school and first-year university students (physics, informatics), teachers who want a demo
in class, and anyone without access to a real lab. It runs in a VR headset or on an ordinary PC.

| # | Level | Concept | Formula |
| --- | --- | --- | --- |
| 1 | First Toss | Projectile motion | `R = v₀²·sin2θ / g` |
| 2 | Heavy Lifting | Mass and weight | `F = m·g` |
| 3 | Updraft | Newton's second law | `F_net = m·a` |
| 4 | Mind the Gap | Conservation of energy | `m·g·h = ½·m·v²` |
| 5 | Launch Pad | Inclined plane | `F = m·g·sinθ` |
| 6 | Double Lock | Logic gate AND | `A AND B` |
| 7 | Reflections | Law of reflection | `θi = θr` |
| 8 | Cargo Lift | Work and machines | `W = m·g·h` |
| 9 | Eclipse | Shadows, NOT gate | `NOT sensor` |
| 10 | Balance | Levers and torque | `m₁·d₁ = m₂·d₂` |
| 11 | Momentum | Momentum and collisions | `p = m·v` |
| 12 | Live Wire | Series and parallel circuits | `S1 AND (S2 OR S3)` |
| 13 | Sandbox | Scientific method | question → experiment → conclusion |

### Meta Quest controllers

On a Quest (standalone or Link) each hand shows a Touch-style controller that mirrors the real one: the stick tilts,
buttons and the trigger glow when pressed. Labels next to each control say what it does.

- **Laser pointer:** aim at any button from up to 6 m away and pull the trigger to press it.
- **Wrist display (left hand):** level, timer, stars and the lab meter reading. Turn your wrist to read it.
- **Haptics:** the controller buzzes on hover, grab, release, impacts of the held object and when you score.
- **Stick clicks:** left = show / hide the control labels, right = slow motion.
- **Slow motion** (`V` on desktop): physics at 0.25× speed to watch collisions and throws up close.

Everything is built from code at runtime: levels, materials, sounds and UI. The scene holds
a single `SandboxBootstrap` component, so there are no prefabs or material assets to keep in sync.

## Getting started

1. Open the project in **Unity 6000.3.12f1**. On first import the editor script creates
   `Assets/PuzzleSandbox/Scenes/VRPuzzleSandbox.unity` and adds it to Build Settings.
2. Open the scene: **VR Puzzle Sandbox > Open Sandbox Scene**.
3. Press **Play**. With no headset you get desktop controls. Click the Game view to capture the mouse.

### Enabling VR (OpenXR)

The manifest already includes `com.unity.xr.management` and `com.unity.xr.openxr`.

1. Run **VR Puzzle Sandbox > Configure OpenXR (PC + Android)**. This turns on the OpenXR loader and the
   Oculus/Meta Touch, Valve Index, HTC Vive and Khronos Simple controller profiles.
   If the XR settings don't exist yet, the menu opens *Project Settings > XR Plug-in Management*.
   Visiting that page creates them; then run the menu item again.
2. **PC VR (Quest Link, SteamVR, WMR):** make sure your OpenXR runtime is active, then press Play.
3. **Quest standalone:** switch the platform to Android. In *XR Plug-in Management > OpenXR (Android tab)*,
   also enable the **Meta Quest Support** feature group. Then build.

The rig reads controllers through the XR input subsystem (`UnityEngine.XR.InputDevices`),
so any OpenXR controller profile works without the XR Interaction Toolkit.

## Controls

| Action | VR | Desktop |
| --- | --- | --- |
| Grab / carry | Grip | Hold left mouse |
| Throw | Swing and let go of grip | Right mouse while holding (or flick and release) |
| Freeze object in mid-air | Trigger while holding | `F` while holding |
| Unfreeze | Just grab it again | Grab it, or aim and press `F` |
| Rotate held object | Your wrist | `Q`/`E` (yaw), `Z`/`C` (pitch), mouse wheel = distance |
| Move | Left stick | `WASD`, `Shift` sprint, `Space` jump |
| Turn | Right stick (30° snap) | Mouse |
| Press buttons | Poke with your fingertip | Left-click |
| Reset level / next level | `X` / `Y` (left controller) | `R` / `N` (`P` = previous) |
| Pick any level | Poke a button on the Level Select board | `1`–`7`, or click the board |
| Show the next tip | HINT button on the lectern | `H` |
| Sandbox: spawn / cycle item | `A` / `B` (right controller) | `G` / `Tab` (`Backspace` clears) |
| Show / hide the physics lesson card | Lesson board above the lectern | `L` |
| Show / hide the throw trajectory | | `T` |
| Slow motion on / off | Click the right stick | `V` |
| English / Uzbek lessons | EN / UZ button on the lesson board | `U` |
| Open the lab report folder | | `J` |
| Show / hide controller labels | Click the left stick | |
| Press a button from a distance | Point at it, pull the trigger | |
| Hide the controls help | | `F1` |

Two boards are always around the spawn point:
- **Lectern (to your left):** level name, hint, revealed tips, a live timer and PREV / RESET / HINT / NEXT buttons.
- **Level Select (behind you):** one button per level, with its best stars, best time and par time.

A bobbing arrow floats above every orb, so you always know which object to deliver.

## Levels

1. **First Toss**: throw the orb over a lava strip into the basket.
2. **Heavy Lifting**: keep 3 kg on a pressure plate to hold the vault gate open, then deliver the orb.
3. **Updraft**: weigh down a plate to open a tower's intake, feed the orb in, and switch on the fan
   that lifts it to the goal at the top.
4. **Mind the Gap**: the orb can't be touched. Bridge the gap in its track with a plank, then release it down the ramp.
5. **Launch Pad**: a heavy orb that can't be thrown must reach a pad in a lava moat. Build a ramp from a long
   plank (freeze it or prop it on crates). The pad fires the orb onto a high ledge.
6. **Double Lock**: the vault gate opens only while *both* plates hold 2 kg (AND logic). One plate is across
   a lava river, so you throw crates onto it.
7. **Sandbox**: a spawner console, fan, launch pad, seesaw, dominoes, ice rink and a plate-operated goal.

Rules that hold everywhere:
- Lava respawns objects (and you).
- The orb can be thrown or rolled across lava, but never carried over it.
- Held or frozen objects don't count toward pressure plates.

### Time and stars

The timer starts on your first grab or button press, not when the level loads, so reading the hint is free.
Each puzzle has a par time:

| Stars | Condition |
| --- | --- |
| 3 | Solved within par time |
| 2 | Solved within twice the par time |
| 1 | Solved |

Progress (solved levels, best time, best stars and the last level played) is saved in `PlayerPrefs` by `Progress`.

## Project layout

```
Assets/PuzzleSandbox/
  Scripts/                     (PuzzleSandbox.asmdef)
    Core/         SandboxBootstrap, ArenaEnvironment, MaterialLibrary, Shapes, Sounds, WorldText, PhysicsMaterials
    Interaction/  Grabbable, Grabber, XRHand, DesktopGrabber, DesktopController, PlayerRig, Respawnable
    Puzzle/       PuzzleSource/PuzzleReceiver, PokeButton, PressurePlate, Gate, Fan, LaunchPad, GoalZone, KillZone, Wire,
                  ObjectiveMarker
    Levels/       LevelManager, LevelDefinition, Progress, ControlPanel, LevelSelectBoard, Props, SpawnCatalog
      Puzzles/    one class per level
  Editor/                      (PuzzleSandbox.Editor.asmdef) scene creation and OpenXR setup menu
```

### How it works

- **Grabbing** is velocity-based: each physics step the held body's velocity is set to reach the hand's pose.
  Held objects therefore still collide, push other objects and can't pass through walls. If an object is
  held back from the hand for a moment (for example stuck behind a wall), it is dropped. Throws use the
  hand's averaged velocity over the last few physics steps.
- **Signals**: `PuzzleSource`s (buttons, plates) power `PuzzleReceiver`s (gates, fans) with AND/OR logic.
  `Wire` draws the connection on the floor and lights up while the source is on.
- **Physics** runs at 90 Hz with 12 solver iterations, so stacks stay stable and held objects move smoothly.

### Adding a level

Create a class deriving from `LevelDefinition`, build objects under `context.Root` with `Props.*` and the puzzle
component `Create` helpers, and add it to `LevelCatalog.All()`. Override `ParTime` to time it and `Tips` to give
step-by-step help. The player spawns at the origin facing +Z.
Keep the area around `(-1.3, 0, 0.7)` clear for the control panel and around `(0, 0, -1.5)` for the level select board.

Progress is saved by level index, so add new levels at the end of the list (before the sandbox) to keep saved records
pointing at the right levels.
