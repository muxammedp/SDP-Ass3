# Assignment 3 | Bridge Pattern

Topic A: Drawing. Circle (radius 2) and Square (side 3) work with VectorRenderer,
RasterRenderer, and AsciiRenderer. T5 switches the renderer on the same Circle.

Base commit: `423467d70f88646b802b9eb139b2db4efc1c2ec2`.

Requires JDK 17 or newer:

```sh
javac --release 17 -encoding UTF-8 -d out "@sources.txt"
java -cp out Main --demo
```

The program runs T1-T7 and computes `SUMMARY: 7/7 PASS` if all checks pass.
Within `src/`, the extension adds only AsciiRenderer and updates Main.
