# Assignment 3 | Bridge Pattern

- **Student name:** Zhuman Mukhammed.
- **Group:** SE-2522.
- **Topic:** A - Drawing.
- **Repository URL:** https://github.com/muxammedp/SDP-Ass3
- **Base commit:** `423467d70f88646b802b9eb139b2db4efc1c2ec2`.
- **I3 source commit:** `be88bfaeeb7be8418ab0b2cd7ef11996e0e0555a`.
- **Submitted commit:** the exact packaged revision is recorded in `SUBMISSION.txt` at the ZIP root.

The submission archive is `Assignment3_SE-2522_Zhuman_Mukhammed.zip`.
In the Moodle submission text, provide the repository URL above and the exact
submitted commit from `SUBMISSION.txt`. All report and program text is in English.

## Role map

| Role | Class | Source |
| --- | --- | --- |
| Abstraction | Shape | [src/drawing/Shape.java](src/drawing/Shape.java) |
| A1 | Circle | [src/drawing/Circle.java](src/drawing/Circle.java) |
| A2 | Square | [src/drawing/Square.java](src/drawing/Square.java) |
| Implementor | Renderer | [src/drawing/Renderer.java](src/drawing/Renderer.java) |
| I1 | VectorRenderer | [src/drawing/VectorRenderer.java](src/drawing/VectorRenderer.java) |
| I2 | RasterRenderer | [src/drawing/RasterRenderer.java](src/drawing/RasterRenderer.java) |
| I3 | AsciiRenderer | [src/drawing/AsciiRenderer.java](src/drawing/AsciiRenderer.java) |
| Client / demo | Main | [src/Main.java](src/Main.java) |

The interface-typed bridge is `private Renderer renderer` in `Shape.java:7`.
The constructor receives that reference at `Shape.java:9`.
`Shape.setImplementation(Renderer)` at line 22 changes only this reference.
`Shape.execute()` is declared at line 26; `Circle.execute()` and
`Square.execute()` at line 19 delegate through `getRenderer()`.
The low-level interface operations are `renderCircle(int)` and `renderSquare(int)`.

The two dimensions are shape data/behavior and rendering style. A shape knows
which operation and dimension to use; its renderer returns the style-specific
description. Shapes never construct, cast to, or test the type of a concrete
renderer. The client composes them. Every shape has an immutable ID and an
immutable positive dimension. A null ID or renderer is rejected.

## Build and run

Use a JDK 17 or newer on PATH (both `java` and `javac`). From the project root:

```sh
javac --release 17 -encoding UTF-8 -d out "@sources.txt"
java -cp out Main --demo
```

There are no application dependencies beyond JDK classes. `Main.java` is in the
default package. Other classes use the `drawing` package. The demo requires no
input, network, database, GUI, or hardware. Rendering is a text simulation.

On the current Windows machine, the default PATH selects Java 8 and does not expose
`javac`. An existing JDK 25 is available outside this project. To select it for the
current PowerShell session before running the standard commands above:

```powershell
$env:JAVA_HOME = "$env:USERPROFILE/.jdks/openjdk-25.0.1"
$env:PATH = "$env:JAVA_HOME/bin;$env:PATH"
```

The final program was also verified on JDK 17. Each receiving machine must provide
its own JDK. `--release 17` generates Java 17-compatible class files.

## Expected demonstration results

All ordinary Circle cases use ID `circle-1`, radius `2`; Square cases use ID
`square-1`, side `3`. Each result is compared with an independent expected string.

| Check | Participating classes | Expected actual result |
| --- | --- | --- |
| T1 | Circle + VectorRenderer | `VECTOR circle radius=2` |
| T2 | Circle + RasterRenderer | `RASTER circle radius=2` |
| T3 | Square + VectorRenderer | `VECTOR square side=3` |
| T4 | Square + RasterRenderer | `RASTER square side=3` |
| T5 | Circle + VectorRenderer -> RasterRenderer | Before: `VECTOR circle radius=2`; after: `RASTER circle radius=2` |
| T6 | Circle + AsciiRenderer | `ASCII circle radius=2 (o)` |
| T7 | Square + AsciiRenderer | `ASCII square side=3 [#]` |

T5 is `Main.checkRuntimeSwitch()` at `src/Main.java:45`. It saves the original
reference, ID, and radius before execution. `Circle afterSwitch = original` keeps
an alias to that object. After calling `setImplementation(new RasterRenderer())`,
`original == afterSwitch` must be true, the ID must still equal `circle-switch`,
and the radius must still equal `2`. Both before/after results must also match.
Expected evidence: `sameObject=true`, `stateUnchanged=true`,
`id=circle-switch -> circle-switch`, and `radius=2 -> 2`.

`checkResult()` (line 72) computes equality and `record()` (line 76) counts results.
Each failed comparison prints `FAIL` and its expected result. All seven checks run
in order, and the summary is calculated from the counters. A failed demo exits
with status 1. Successful execution ends with `SUMMARY: 7/7 PASS` and status 0.
The actual captured output is in [demo-output.txt](demo-output.txt).

## Independent extension and commit evidence

The base commit was compiled and ran T1-T5 successfully before it was committed.
The second commit added I3. Within `src/`, exactly these files changed:

- `src/drawing/AsciiRenderer.java`: a new implementation of the same Renderer contract.
- `src/Main.java`: an import and T6-T7 calls using the new implementation.

Shape, Circle, Square, Renderer, VectorRenderer, and RasterRenderer were unchanged.
`sources.txt` and documentation were also updated, as the assignment allows.
Subsequent documentation commits do not change any Java source.

[extension.diff](extension.diff) was saved after committing I3, using:

```sh
git diff 423467d70f88646b802b9eb139b2db4efc1c2ec2 HEAD -- src > extension.diff
```

The saved diff is UTF-8 without a BOM. In Windows PowerShell 5, use Git Bash for
the redirection above or explicitly write UTF-8, since its default `>` encoding
is UTF-16. The packaged sources match the revision recorded in `SUBMISSION.txt`.

## Report and UML

[report.pdf](report.pdf) contains the three-page report, including the UML diagram,
five annotated excerpts from the real Java files, the extension explanation,
Bridge/Adapter comparison, trade-off, and references.
The editable diagram is [docs/bridge.puml](docs/bridge.puml); its rendered version
is [docs/bridge.png](docs/bridge.png). PlantUML uses its built-in Smetana layout.

## Five-minute defense guide

1. Run the two build/demo commands. Show T1-T7 and the calculated summary.
2. Use the role map and UML. Trace `new Circle("circle-1", 2, new VectorRenderer())`:
   the constructor stores the renderer; `execute()` calls `renderCircle(radius)`
   on that stored interface reference; VectorRenderer returns the vector string.
3. Open `checkRuntimeSwitch()`. Explain that the Circle reference, ID, and radius
   stay the same; only Shape's renderer field changes. `==` proves object identity,
   while getter comparisons check domain data and string comparisons check behavior.
4. Open `extension.diff`. Explain why implementing Renderer and changing the client
   suffices. Bridge separates two planned dimensions; Adapter translates an
   incompatible existing API into one the client expects. There is no legacy API here.
5. Explain a chosen method and predict a change: a Circle of radius 5 with the ASCII
   renderer returns `ASCII circle radius=5 (o)`. Changing only T1's radius to 5 makes
   T1 fail against its fixed radius-2 expectation. The summary then becomes 6/7.

One trade-off is the additional interface, classes, and delegation for a small
simulation. Also, adding a new shape-specific primitive (for example, a triangle)
would require updating Renderer and all renderers; the proven independent extension
here is adding a rendering style under the existing contract.

## References

- Astana IT University, School of Software Engineering. *Assignment 3 | Bridge Pattern*,
  ShP-2216 Software Design Patterns, 2026-2027. User-provided assignment brief.
- Refactoring.Guru. [Bridge](https://refactoring.guru/design-patterns/bridge).
  Consulted 4 October 2026 for the two-hierarchy design and its trade-offs.
- Refactoring.Guru. [Adapter](https://refactoring.guru/design-patterns/adapter).
  Consulted 4 October 2026 for the difference in intent.

The course's Moodle resources and syllabus were not provided and are not cited as
consulted sources. This project and report were prepared with AI assistance; review,
understand, and adapt them in accordance with the course's stated AI-use rules.
