from manim import *
import numpy as np

class Thumbnail(Scene):
    def construct(self):
        self.camera.background_color = "#0d1117"

        # ---- Background: scattered "packing blocks" of varying sizes ----
        np.random.seed(7)
        colors = [BLUE_D, BLUE_E, TEAL_D, PURPLE_D, GREEN_D, MAROON_D]

        blocks = VGroup()
        for _ in range(14):
            w = np.random.uniform(0.8, 2.4)
            h = np.random.uniform(0.8, 2.4)
            block = RoundedRectangle(
                width=w, height=h, corner_radius=0.1,
                fill_color=np.random.choice(colors),
                fill_opacity=0.55,
                stroke_color=WHITE,
                stroke_width=1.5
            )
            block.move_to(np.array([
                np.random.uniform(-7, 7),
                np.random.uniform(-4, 4),
                0
            ]))
            block.rotate(np.random.uniform(-0.3, 0.3))
            blocks.add(block)

        self.add(blocks)

        # Darken background slightly behind text for readability
        overlay = Rectangle(
            width=14, height=4.5,
            fill_color="#0d1117", fill_opacity=0.65, stroke_width=0
        ).move_to(ORIGIN)
        self.add(overlay)

        # ---- Main title ----
        title = Text("SET PACKING", font_size=96, weight=BOLD, color=WHITE)
        title.move_to(ORIGIN)

        # subtle outline/glow via stroke
        title.set_stroke(color=BLUE_B, width=2)

        self.add(title)

        # ---- Bottom subtitle ----
        subtitle = Text(
            "solved using Simulated Annealing",
            font_size=44, weight=BOLD, color=YELLOW
        )
        subtitle.next_to(title, DOWN, buff=0.6)

        self.add(subtitle)

        self.wait(1)