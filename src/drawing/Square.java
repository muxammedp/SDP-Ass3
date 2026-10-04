package drawing;

public final class Square extends Shape {
    private final int side;

    public Square(String id, int side, Renderer renderer) {
        super(id, renderer);
        if (side <= 0) {
            throw new IllegalArgumentException("side must be positive");
        }
        this.side = side;
    }

    public int getSide() {
        return side;
    }

    @Override
    public String execute() {
        return getRenderer().renderSquare(side);
    }
}
