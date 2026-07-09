from manim import *

class Intro(Scene):
    def construct(self):
        title = Text("Exact Cover", font_size=60)
        subtitle = Text("a classic decision problem", font_size=28)
        subtitle.next_to(title, DOWN)
        self.play(Write(title), run_time=2)
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(1.5)
        self.play(FadeOut(title), FadeOut(subtitle))


class TetrisExactCover(Scene):
    def construct(self):
        # ---------- config ----------
        n = 4
        cell = 1.0
        grid_origin = LEFT * (n * cell / 2) + UP * (n * cell / 2)  # top-left corner

        # ---------- draw U as an empty grid ----------
        grid = VGroup()
        for r in range(n):
            for c in range(n):
                sq = Square(side_length=cell, stroke_width=2, stroke_color=GREY_B)
                sq.move_to(grid_origin + RIGHT * (c + 0.5) * cell + DOWN * (r + 0.5) * cell)
                grid.add(sq)

        u_label = Text("U", font_size=40).next_to(grid, UP, buff=0.4)
        question = Text("Can these pieces exactly cover U?", font_size=30).to_edge(UP)

        self.play(Write(question))
        self.play(Create(grid), FadeIn(u_label))
        self.wait(0.5)

        # ---------- define the 4 subsets V_i as tetromino cell-lists ----------
        # a pinwheel tiling: 4 rotations of the same L-tetromino, verified to
        # cover all 16 cells exactly once
        pieces_cells = {
            "V1": [(0, 0), (1, 0), (2, 0), (2, 1)],
            "V2": [(0, 1), (0, 2), (0, 3), (1, 1)],
            "V3": [(1, 2), (1, 3), (2, 3), (3, 3)],
            "V4": [(2, 2), (3, 0), (3, 1), (3, 2)],
        }
        colors = {"V1": BLUE, "V2": RED, "V3": GREEN, "V4": YELLOW}
        entry_offsets = {          # off-screen "drop-in" direction per piece
            "V1": LEFT * 7,
            "V2": UP * 6,
            "V3": RIGHT * 7,
            "V4": DOWN * 6,
        }

        def make_piece(cells, color):
            piece = VGroup()
            for (r, c) in cells:
                sq = Square(side_length=cell, fill_color=color, fill_opacity=0.85,
                            stroke_color=WHITE, stroke_width=2)
                sq.move_to(grid_origin + RIGHT * (c + 0.5) * cell + DOWN * (r + 0.5) * cell)
                piece.add(sq)
            return piece

        final_pieces = {name: make_piece(cells, colors[name])
                         for name, cells in pieces_cells.items()}

        # ---------- legend ----------
        legend = VGroup(*[
            VGroup(Square(side_length=0.3, fill_color=colors[n_], fill_opacity=1,
                           stroke_color=WHITE),
                   Text(n_, font_size=22)).arrange(RIGHT, buff=0.15)
            for n_ in pieces_cells
        ]).arrange(RIGHT, buff=0.5).next_to(grid, DOWN, buff=0.5)

        narration = Tex(r"Each piece represents a disjoint subset $V_i$",
                          font_size=26).next_to(legend, DOWN, buff=0.4)
        self.play(FadeIn(legend), FadeIn(narration))

        # ---------- drop each piece into place ----------
        for name, piece in final_pieces.items():
            start_piece = piece.copy().shift(entry_offsets[name])
            self.play(FadeIn(start_piece), run_time=0.3)
            self.play(
                start_piece.animate.move_to(piece.get_center()),
                run_time=1.0,
                rate_func=rush_into,
            )
            self.wait(0.2)

        self.wait(0.3)

        # ---------- success ----------
        success = Text("This is the Exact Cover problem", font_size=36, color=GREEN)
        success.next_to(legend, DOWN, buff=0.4)
        self.play(FadeOut(narration))
        self.play(Flash(grid, color=GREEN, flash_radius=n * cell * 0.7))
        self.play(Write(success))
        self.wait(2)
        self.clear()
        
        # self.play(FadeOut(success),FadeOut(legend),FadeOut(narration))
        self.wait(1.5)

        intro = Tex(
            r"More Formally",
            font_size=60
        ).to_edge(UP)
        
        setup = Tex(
            r"Consider a set $ U = \{1, \dots, n\} $ such that",
            r"$$ U = \bigcup_{i} V_i $$"
        ).next_to(intro, DOWN, buff=0.6)
        
        math=Tex(
            r"Is there a subset of the set of sets $\{V_i\}$, called R, \\"
            r"such that the elements of R are disjoint sets, and the union of \\"
            r"the elements of R is U ?",
            font_size=32
        ).next_to(setup,DOWN,buff=0.5)

        # safety net in case it's still too wide
        if intro.width > config.frame_width - 1:
            intro.scale_to_fit_width(config.frame_width - 1)

        self.play(Write(intro),font_size=50)
        self.wait(1)
        self.play(Write(setup))
        self.wait(2.5)
        self.play(Write(math),run_time=2)
        self.wait(1.5)
        
        
class QUBO(Scene):
    def construct(self):
        NP = Text("This decision problem is known to be NP Complete", font_size=40).to_edge(UP)
        anneal = Text("Simulated Annealing", font_size=24).next_to(NP, DOWN, buff=1)
        andrew = Text("From Andrew Lucas's Paper", font_size=28).next_to(anneal, DOWN, buff=0.4)
        paper = Text("'Ising Formulations of many NP problems'", font_size=28).next_to(andrew, DOWN, buff=0.2)
        propose = Text("a Non-Deterministic approach to solve this problem", font_size=24).next_to(paper, DOWN, buff=0.3)

        self.play(Write(NP))
        self.wait(1)
        self.play(Write(anneal))
        self.play(Write(andrew))
        self.wait(1)
        self.play(Write(paper))
        self.play(Write(propose))
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in [NP, anneal, andrew, paper, propose]])
        
  
class Hamiltonian(Scene):
    def construct(self):
        # Step 1: consider an element alpha
        consider = Tex(r"Consider an element $\alpha$")
        self.play(Write(consider))
        self.wait(1)
        self.play(FadeOut(consider))

        # Step 2: inner sum, defined as beta_alpha (nothing destroyed)
        inner = MathTex(r"\sum_{i:\alpha \in V_i} x_i")
        self.play(Write(inner))
        self.wait(1)

        meaning = Tex(r"$x_i = 1$ if the chosen set $V_i$ contains $\alpha$").scale(0.7)
        meaning.next_to(inner, DOWN, buff=0.6)
        self.play(FadeIn(meaning, shift=UP))
        self.wait(1.5)
        self.play(FadeOut(meaning))

        beta_label = MathTex(r"\beta_\alpha = \sum_{i:\alpha \in V_i} x_i").move_to(inner)
        self.play(ReplacementTransform(inner, beta_label))
        self.wait(1)

        # group the whole "sum = beta_alpha" line and send it up as a reference
        definition = VGroup(inner, beta_label)
        self.play(definition.animate.to_edge(UP))
        self.wait(0.5)

        # Step 3: good/bad cases, fresh in the center
        cases = VGroup(
            MathTex(r"\beta_\alpha < 1", r"\;").set_color(RED),
            MathTex(r"\beta_\alpha > 1", r"\;").set_color(RED),
            MathTex(r"\beta_\alpha = 1", r"\;").set_color(GREEN),
        ).arrange(DOWN, buff=0.3)
        self.play(LaggedStartMap(FadeIn, cases,run_time=3,rate_func=linear))
        self.wait(1.5)
        self.play(FadeOut(cases))

        # Step 4: penalty shape, fresh in center, reusing beta_alpha from up top
        penalty = MathTex(r"(1-\beta_\alpha)^2")
        self.play(Write(penalty))
        self.wait(1)
        self.play(FadeOut(penalty))
        self.wait(1.5)

        # Step 5: outer sum, beta expanded back into the full subscripted sum
        full = MathTex(
            r"\sum_{\alpha=1}^{n}"
            r"\left(1-\beta_\alpha)^2"
        )
        self.play(Write(full))
        self.wait(1)

        # Step 6: multiply by A
        H = MathTex(
            r"H_A = A"
            r"\sum_{\alpha=1}^{n}"
            r"\left(1-\sum_{i:\alpha \in V_i} x_i\right)^2"
        )
        H.move_to(full)
        self.play(ReplacementTransform(full, H))
        self.wait(2)
        self.play(FadeOut(definition))
        self.play(H.animate.to_edge(UP))
        self.wait(2)
        
        
        caseH = VGroup(
            MathTex(r"min(H_A) > 0", r"\;").set_color(RED),
            MathTex(r"min(H_A) = 0", r"\;").set_color(GREEN),
        ).arrange(DOWN, buff=0.3)
        self.play(LaggedStartMap(FadeIn, caseH,run_time=3,rate_func=linear))
        self.wait(1.5)
        exist=Text("There exists a solution for the exact cover problem",font_size=24).next_to(caseH,DOWN,buff=0.5)
        self.play(FadeIn(exist))
        self.wait(1.5)
        self.play(FadeOut(caseH))
        self.play(FadeOut(exist))
        self.wait(1.5)
        
        HB = MathTex(
            r"H_B = B\sum_{i} x_i"
        )
        self.play(FadeIn(HB))
        self.wait(2)
        
        H_full = MathTex(
            r"H=A\sum_{\alpha=1}^{n}",
            r"\left(1-\sum_{i:\alpha \in V_i} x_i\right)^2",
            r"+ B\sum_{i} x_i"
        )

        self.play(
            ReplacementTransform(H, VGroup(H_full[0], H_full[1])),
            ReplacementTransform(HB, H_full[2]),
        )
        self.wait(2)
        self.play(H_full.animate.to_edge(UP))
        self.wait(2)
        
        caseH_full = VGroup(
            MathTex(r"min(H) = mB", r"\;").set_color(GREEN)
        ).arrange(DOWN, buff=0.3)
        
        minH=Text("Where m is the minimum number of subsets needed to cover U exactly",font_size=20).next_to(H_full,DOWN,buff=0.5)
        
        self.play(FadeIn(caseH_full))
        self.wait(0.5)
        self.play(FadeIn(minH))
        self.wait(2)
        
        # talk about constraint
        
        self.play(FadeOut(minH),FadeOut(caseH_full))
        
        # --- worst-case scenario ---
        concern = Tex(
            r"But if B is too large relative to A, minimizing $H_B$",
            font_size=32
        )
        concern2 = Text(
            "could tempt the solver into breaking exact coverage",
            font_size=24
        ).next_to(concern, DOWN, buff=0.2)
        self.play(FadeIn(concern), FadeIn(concern2))
        self.wait(2)
        self.play(FadeOut(concern), FadeOut(concern2))

        worst_case = Text(
            "Worst case: a few subsets with one shared element still cover U",
            font_size=24
        )
        self.play(FadeIn(worst_case))
        self.wait(2)
        self.play(FadeOut(worst_case))

        safeguard = MathTex(r"A > nB").scale(1.2)
        safeguard_note = Text(
            "ensures violating a constraint never pays off",
            font_size=22
        ).next_to(safeguard, DOWN, buff=0.4)
        self.play(Write(safeguard))
        self.wait(0.5)
        self.play(FadeIn(safeguard_note))
        self.wait(2)
        self.play(FadeOut(safeguard), FadeOut(safeguard_note))



class Thumbnail(Scene):
    def construct(self):
        self.camera.background_color = "#0b0b12"

        # ---------- faint background grid ----------
        n = 6
        cell = 1.1
        grid_origin = LEFT * (n * cell / 2) + DOWN * 0.3 + UP * (n * cell / 2)

        grid = VGroup()
        for r in range(n):
            for c in range(n):
                sq = Square(side_length=cell, stroke_width=1.5, stroke_color=GREY_D,
                             fill_color=GREY_E, fill_opacity=0.15)
                sq.move_to(grid_origin + RIGHT * (c + 0.5) * cell + DOWN * (r + 0.5) * cell)
                grid.add(sq)
        grid.set_z_index(0)

        # ---------- a few bold "solved" tetromino pieces ----------
        def make_piece(cells, color):
            piece = VGroup()
            for (r, c) in cells:
                sq = Square(side_length=cell, fill_color=color, fill_opacity=0.95,
                             stroke_color=WHITE, stroke_width=2.5)
                sq.move_to(grid_origin + RIGHT * (c + 0.5) * cell + DOWN * (r + 0.5) * cell)
                piece.add(sq)
            return piece

        pieces = VGroup(
            make_piece([(0, 0), (1, 0), (2, 0), (2, 1)], BLUE),
            make_piece([(0, 1), (0, 2), (0, 3), (1, 1)], "#FF5C5C"),
            make_piece([(4, 4), (4, 5), (5, 5), (5, 4)], "#FFD93D"),
            make_piece([(3, 2), (3, 3), (4, 3), (4, 2)], "#4ADE80"),
        )
        pieces.set_z_index(1)

        # ---------- title text ----------
        title = Text("EXACT COVER", font_size=90, weight=BOLD, color=WHITE)
        title.set_z_index(2)
        title.to_edge(UP, buff=0.6)

        # subtle drop-shadow effect: duplicate title behind, offset, dark
        title_shadow = title.copy().set_color(BLACK).set_opacity(0.6)
        title_shadow.shift(DOWN * 0.05 + RIGHT * 0.05)
        title_shadow.set_z_index(1.5)


        self.add(grid, pieces, title_shadow, title)
        self.wait(0.1)