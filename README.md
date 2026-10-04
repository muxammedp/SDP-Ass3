# Assignment 3 | Bridge Pattern

Topic A: Drawing. This base version demonstrates Circle (radius 2) and Square
(side 3) with VectorRenderer and RasterRenderer, including a runtime switch on
the same Circle object. The extension will add AsciiRenderer separately.

Requires JDK 17 or newer:

```sh
javac --release 17 -encoding UTF-8 -d out "@sources.txt"
java -cp out Main --demo
```

The base version runs T1-T5 and computes `SUMMARY: 5/5 PASS` if all checks pass.
The final README will record this version's commit hash after it is committed.
