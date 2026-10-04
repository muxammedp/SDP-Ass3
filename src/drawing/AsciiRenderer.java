package drawing;

public final class AsciiRenderer implements Renderer {
    @Override
    public String renderCircle(int radius) {
        return "ASCII circle radius=" + radius + " (o)";
    }

    @Override
    public String renderSquare(int side) {
        return "ASCII square side=" + side + " [#]";
    }
}
