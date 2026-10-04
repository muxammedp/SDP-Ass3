import drawing.AsciiRenderer;
import drawing.Circle;
import drawing.RasterRenderer;
import drawing.Square;
import drawing.VectorRenderer;

public final class Main {
    private int passed;
    private int total;

    public static void main(String[] args) {
        if (args.length != 1 || !"--demo".equals(args[0])) {
            System.out.println("Usage: java -cp out Main --demo");
            return;
        }
        if (!new Main().runDemo()) {
            System.exit(1);
        }
    }

    private boolean runDemo() {
        checkResult("T1", "Circle + VectorRenderer",
                new Circle("circle-1", 2, new VectorRenderer()).execute(),
                "VECTOR circle radius=2");
        checkResult("T2", "Circle + RasterRenderer",
                new Circle("circle-1", 2, new RasterRenderer()).execute(),
                "RASTER circle radius=2");
        checkResult("T3", "Square + VectorRenderer",
                new Square("square-1", 3, new VectorRenderer()).execute(),
                "VECTOR square side=3");
        checkResult("T4", "Square + RasterRenderer",
                new Square("square-1", 3, new RasterRenderer()).execute(),
                "RASTER square side=3");
        checkRuntimeSwitch();
        checkResult("T6", "Circle + AsciiRenderer",
                new Circle("circle-1", 2, new AsciiRenderer()).execute(),
                "ASCII circle radius=2 (o)");
        checkResult("T7", "Square + AsciiRenderer",
                new Square("square-1", 3, new AsciiRenderer()).execute(),
                "ASCII square side=3 [#]");
        System.out.println("SUMMARY: " + passed + "/" + total + " PASS");
        return passed == total;
    }

    private void checkRuntimeSwitch() {
        Circle original = new Circle("circle-switch", 2, new VectorRenderer());
        String originalId = original.getId();
        int originalRadius = original.getRadius();
        String before = original.execute();

        Circle afterSwitch = original;
        afterSwitch.setImplementation(new RasterRenderer());
        String after = afterSwitch.execute();

        boolean sameObject = original == afterSwitch;
        boolean stateUnchanged = originalId.equals(afterSwitch.getId())
                && originalRadius == afterSwitch.getRadius();
        String expectedBefore = "VECTOR circle radius=2";
        String expectedAfter = "RASTER circle radius=2";
        boolean success = sameObject && stateUnchanged
                && expectedBefore.equals(before) && expectedAfter.equals(after);

        record("T5", success, "Circle + VectorRenderer -> RasterRenderer"
                + " | sameObject=" + sameObject + " | stateUnchanged=" + stateUnchanged
                + " | id=" + originalId + " -> " + afterSwitch.getId()
                + " | radius=" + originalRadius + " -> " + afterSwitch.getRadius()
                + "\n before=" + before + " | after=" + after,
                "sameObject=true | stateUnchanged=true | id=circle-switch -> circle-switch"
                + " | radius=2 -> 2 | before=" + expectedBefore + " | after=" + expectedAfter);
    }

    private void checkResult(String testId, String classes, String actual, String expected) {
        record(testId, expected.equals(actual), classes + " | result=" + actual, expected);
    }

    private void record(String testId, boolean success, String details, String expected) {
        total++;
        if (success) {
            passed++;
        }
        System.out.println(testId + " " + (success ? "PASS" : "FAIL") + " | " + details);
        if (!success) {
            System.out.println(" expected=" + expected);
        }
    }
}
