from manim import *

class Intro(Scene):
    def construct(self):
        # Title
        title = Text("Set Packing", font_size=60)
        subtitle = Text("a classic combinatorial optimization problem", font_size=28)
        subtitle.next_to(title, DOWN)

        self.play(Write(title),run_time=3)
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(1.5)
        self.play(FadeOut(title), FadeOut(subtitle))

        # Show the universe U as scattered dots
        universe_label = Text("Universe U", font_size=32).to_edge(UP)
        dots = VGroup(*[
            Dot(point=np.array([
                np.random.uniform(-5, 5),
                np.random.uniform(-2, 2),
                0
            ]), radius=0.08)
            for _ in range(30)
        ])

        self.play(Write(universe_label),run_time=3)
        self.play(LaggedStartMap(FadeIn, dots, lag_ratio=0.05))
        self.wait(1)

        # Draw three overlapping circles representing subsets
        set_colors = [BLUE, GREEN, RED]
        sets = VGroup()
        positions = [LEFT * 2, RIGHT * 1, UP * 1 + RIGHT * 2.5]

        for pos, color in zip(positions, set_colors):
            circle = Circle(radius=1.3, color=color, fill_opacity=0.2)
            circle.move_to(pos)
            sets.add(circle)

        self.play(*[Create(s) for s in sets],run_time=3)
        self.wait(1)

        question = Text(
            "Which sets can we pick so none overlap?",
            font_size=30
        ).to_edge(DOWN)

        self.play(Write(question))
        self.wait(2)

        self.play(
            FadeOut(dots), FadeOut(sets),
            FadeOut(universe_label), FadeOut(question)
        )
        
class NPHardIntro(Scene):
    def construct(self):
        # State the hardness
        hardness = Text(
            "Set Packing is NP-hard",
            font_size=44
        )
        self.play(Write(hardness))
        self.wait(1)

        subtext = Text(
            "no known algorithm solves it efficiently\nfor all cases",
            font_size=26,
            line_spacing=1.2
        ).next_to(hardness, DOWN, buff=0.5)

        self.play(FadeIn(subtext, shift=UP))
        self.wait(1)

        self.play(FadeOut(hardness), FadeOut(subtext))

        # Pivot to the alternative approach
        pivot = Text(
            "But there's another way to approach it",
            font_size=36
        )
        self.play(Write(pivot))
        self.wait(1.5)
        self.play(FadeOut(pivot))

        # Introduce the method name, piece by piece
        method1 = Text("Simulated Annealing", font_size=48, color=BLUE)
        self.play(Write(method1))
        self.wait(0.5)

        method2 = Text(
            "a form of probabilistic computing",
            font_size=28
        ).next_to(method1, DOWN, buff=0.4)
        self.play(FadeIn(method2, shift=UP))
        self.wait(1)

        self.play(FadeOut(method1), FadeOut(method2))

        # Credit the formulation source
        credit = Text(
            "using the QUBO formulation",
            font_size=32
        )
        credit2 = Text(
            "from Andrew Lucas's paper",
            font_size=32,
            color=YELLOW
        ).next_to(credit, DOWN, buff=0.3)
        
        credit3 = Text(
            "'Ising Formulation of many NP problems'",
            font_size=32,
            color=YELLOW
        ).next_to(credit2, DOWN, buff=0.3)

        self.play(Write(credit))
        self.play(Write(credit2))
        self.play(Write(credit3))
        self.wait(2)

        self.play(FadeOut(credit), FadeOut(credit2))
        

class SimulatedAnnealingLandscape(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[0, 4, 1],
            x_length=10,
            y_length=5,
            axis_config={"include_tip": False}
        )

        def energy_func(x):
            return 0.15 * (x**2) + 0.8 * np.sin(2 * x) + 1.8

        curve = axes.plot(energy_func, color=BLUE, x_range=[-5, 5])
        label = Text("Energy Landscape", font_size=32).to_edge(UP)

        self.play(Write(label))
        self.play(Create(axes), Create(curve))
        self.wait(1)

        # Starting state
        np.random.seed(42)  # reproducible run
        current_x = -4.5
        point = Dot(axes.coords_to_point(current_x, energy_func(current_x)), color=RED, radius=0.12)
        self.play(FadeIn(point))
        self.wait(0.5)

        temp_label = Text("Temperature: High", font_size=26, color=ORANGE).to_edge(DOWN)
        self.play(Write(temp_label))
        self.wait(0.3)

        # Cooling schedule: temperature decreases geometrically over steps
        n_steps = 25
        T0 = 3.0
        T_min = 0.05
        cooling_rate = (T_min / T0) ** (1 / n_steps)

        T = T0
        step_size = 0.6  # proposal jump size — stays roughly constant, NOT tied to temperature
        
        algorithm = VGroup(
        Tex(r"if $\Delta E < 0$: accept the move", font_size=32, color=YELLOW),
        Tex(r"if $\Delta E > 0$: accept with probability $e^{-\Delta E / T}$", font_size=32, color=YELLOW)).arrange(DOWN, aligned_edge=LEFT, buff=0.3)

        algorithm.next_to(axes, LEFT, buff=-3.8)  # relative to another object
        self.play(Write(algorithm))

        for step in range(n_steps):
            # propose a small local move
            candidate_x = current_x + np.random.uniform(-step_size, step_size)
            candidate_x = np.clip(candidate_x, -5, 5)

            current_E = energy_func(current_x)
            candidate_E = energy_func(candidate_x)
            dE = candidate_E - current_E

            # Metropolis acceptance criterion
            if dE < 0:
                accept = True
            else:
                accept_prob = np.exp(-dE / T)
                accept = np.random.uniform(0, 1) < accept_prob

            candidate_point = axes.coords_to_point(candidate_x, candidate_E)
            ghost = Dot(candidate_point, color=YELLOW, radius=0.08)

            self.play(FadeIn(ghost), run_time=0.15)

            if accept:
                self.play(
                    point.animate.move_to(candidate_point),
                    FadeOut(ghost),
                    run_time=0.25
                )
                current_x = candidate_x
            else:
                self.play(FadeOut(ghost), run_time=0.15)
                # point stays, rejected candidate just vanishes

            # update temperature label periodically, not every step
            if step in (0, n_steps // 3, 2 * n_steps // 3):
                if T > 1.5:
                    new_text = "Temperature: High"
                    color = ORANGE
                elif T > 0.4:
                    new_text = "Temperature: Cooling"
                    color = YELLOW
                else:
                    new_text = "Temperature: Low"
                    color = GREEN
                new_temp_label = Text(new_text, font_size=26, color=color).to_edge(DOWN)
                self.play(Transform(temp_label, new_temp_label), run_time=0.3)

            T *= cooling_rate

        self.wait(0.5)

        found_label = Text("converged near a minimum", font_size=28, color=GREEN)
        found_label.next_to(point, UP, buff=0.3)
        self.play(FadeIn(found_label, shift=UP))
        self.wait(2)

        self.play(
            FadeOut(point), FadeOut(curve), FadeOut(axes), FadeOut(label),
            FadeOut(temp_label), FadeOut(found_label)
        )
        
class SetPackingFormalism(Scene):
    def construct(self):
        # Setup text
        intro = Text(
            "Set Packing: find the largest number of disjoint subsets",
            font_size=32
        ).to_edge(UP)
        self.play(Write(intro))
        self.wait(1.5)

        # Universe and subset notation
        setup = MathTex(
            r"U = \{1, \dots, n\}, \quad V_i \subseteq U"
        ).next_to(intro, DOWN, buff=0.6)
        self.play(Write(setup))
        self.wait(2)

        self.play(FadeOut(intro), setup.animate.to_edge(UP))
        self.wait(0.5)

        # Hamiltonian, built term by term
        hamiltonian = MathTex(
            r"H", r"=", r"H_A", r"+", r"H_B"
        ).next_to(setup, DOWN, buff=0.8)
        self.play(Write(hamiltonian))
        self.wait(2.5)

        # HA — penalty term
        HA_eq = MathTex(
            r"H_A = A \sum_{i,j:\, V_i \cap V_j \neq \emptyset} x_i x_j"
        ).next_to(hamiltonian, DOWN, buff=0.8)
        self.play(Write(HA_eq))
        self.wait(1)

        HA_note = Text(
            "Penalty term : punishes overlapping sets chosen together",
            font_size=26, color=RED
        ).next_to(HA_eq, DOWN, buff=0.3)
        self.play(FadeIn(HA_note, shift=UP))
        self.wait(2)

        self.play(FadeOut(HA_eq), FadeOut(HA_note))

        # HB — objective term
        HB_eq = MathTex(
            r"H_B = -B \sum_i x_i"
        ).next_to(hamiltonian, DOWN, buff=0.8)
        self.play(Write(HB_eq))
        self.wait(1)

        HB_note = Text(
            "Objective term: rewards including more sets",
            font_size=26, color=GREEN
        ).next_to(HB_eq, DOWN, buff=0.3)
        self.play(FadeIn(HB_note, shift=UP))
        self.wait(2)

        self.play(FadeOut(HB_eq), FadeOut(HB_note))

        # Constraint on B < A
        constraint = MathTex(
            r"B < A"
        ).next_to(hamiltonian, DOWN, buff=0.8)
        constraint_note = Text(
            "ensures it's never worth breaking the constraint to gain reward",
            font_size=26, color=YELLOW
        ).next_to(constraint, DOWN, buff=0.3)

        self.play(Write(constraint))
        self.play(FadeIn(constraint_note, shift=UP))
        self.wait(2.5)

        self.play(
            FadeOut(setup), FadeOut(hamiltonian),
            FadeOut(constraint), FadeOut(constraint_note)
        )

class QUBOImplementation(Scene):
    def construct(self):
        # Setup: remind viewer the Hamiltonian uses binary variables
        intro = Text(
            "Every x_i in our Hamiltonian is binary: 0 or 1",
            font_size=32
        ).to_edge(UP)
        self.play(Write(intro))
        self.wait(2)

        binary_note = MathTex(
            r"x_i \in \{0, 1\}"
        ).next_to(intro, DOWN, buff=0.6)
        self.play(Write(binary_note))
        self.wait(1.5)

        self.play(FadeOut(intro), FadeOut(binary_note))

        # State that this means it's directly a QUBO
        qubo_intro = Text(
            "This means our Hamiltonian is already a QUBO",
            font_size=34
        ).to_edge(UP)
        self.play(Write(qubo_intro))
        self.wait(1.5)

        qubo_full_name = Text(
            "Quadratic Unconstrained Binary Optimization",
            font_size=26, color=YELLOW
        ).next_to(qubo_intro, DOWN, buff=0.4)
        self.play(FadeIn(qubo_full_name, shift=UP))
        self.wait(2)

        self.play(FadeOut(qubo_intro), FadeOut(qubo_full_name))

        # Show the full combined Hamiltonian as the QUBO form
        full_qubo = MathTex(
            r"H = A \sum_{i,j:\, V_i \cap V_j \neq \emptyset} x_i x_j",
            r"\; - \;",
            r"B \sum_i x_i"
        ).scale(0.9)
        full_qubo.move_to(ORIGIN)

        self.play(Write(full_qubo))
        self.wait(1)

        # Label the two halves directly underneath, like before
        penalty_brace = Brace(full_qubo[0], DOWN, color=RED)
        penalty_label = Text("penalty term", font_size=24, color=RED).next_to(penalty_brace, DOWN)

        objective_brace = Brace(full_qubo[2], DOWN, color=GREEN)
        objective_label = Text("objective term", font_size=24, color=GREEN).next_to(objective_brace, DOWN)

        self.play(
            GrowFromCenter(penalty_brace), FadeIn(penalty_label),
            GrowFromCenter(objective_brace), FadeIn(objective_label)
        )
        self.wait(2.5)

        self.play(
            FadeOut(full_qubo), FadeOut(penalty_brace), FadeOut(penalty_label),
            FadeOut(objective_brace), FadeOut(objective_label)
        )

        # Mention D-Wave's package for actually solving it
        dwave_intro = Text(
            "This QUBO can be solved using D-Wave's software",
            font_size=32
        ).to_edge(UP)
        self.play(Write(dwave_intro))
        self.wait(1.5)

        dwave_detail = Text(
            "dimod + dwave-neal, simulating the annealing process",
            font_size=26, color=BLUE
        ).next_to(dwave_intro, DOWN, buff=0.4)
        self.play(FadeIn(dwave_detail, shift=UP))
        self.wait(2.5)

        self.play(FadeOut(dwave_intro), FadeOut(dwave_detail))

        # Point to the code, linked in description
        code_pointer = Text(
            "Full implementation linked in the description",
            font_size=34, color=YELLOW
        )
        self.play(Write(code_pointer))
        self.wait(2.5)

        self.play(FadeOut(code_pointer))