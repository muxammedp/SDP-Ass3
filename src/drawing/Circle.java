package drawing;

public final class Circle extends Shape {
    private final int radius;

    public Circle(String id, int radius, Renderer renderer) {
        super(id, renderer);
        if (radius <= 0) {
            throw new IllegalArgumentException("radius must be positive");
        }
        this.radius = radius;
    }

    public int getRadius() {
        return radius;
    }

    @Override
    public String execute() {
        return getRenderer().renderCircle(radius);
    }
}
