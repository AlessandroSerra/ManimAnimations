from manim import *


class MainScene(MovingCameraScene):
    def construct(self):
        config.frame_rate = 15

        # self.add_sound("music3.mp3")

        luvalamp = ImageMobject("luvalamp.jpeg")

        self.add(luvalamp)
        self.wait(2)
        self.play(FadeOut(luvalamp), run_time=1.5)

        # Creiamo il corpo principale della bottiglia (parte rettangolare)
        bottle_body = Rectangle(
            height=2.5,
            width=2,
            fill_color="#D3D3D3",
            fill_opacity=0.3,
            stroke_color=WHITE,
        ).shift(DOWN)

        # Creiamo il collo della bottiglia (parte rettangolare superiore)
        bottle_neck = Rectangle(
            height=0.7,
            width=0.6,
            fill_color="#D3D3D3",
            fill_opacity=0.3,
            stroke_color=WHITE,
        ).move_to(np.array([0, 1.2, 0]))

        # Creiamo le curve di raccordo
        left_curve = ArcBetweenPoints(
            start=[-1, 0.25, 0],  # Punto sinistro del corpo
            end=[-0.3, 0.85, 0],  # Punto sinistro del collo
            angle=-PI / 3,
        )

        right_curve = ArcBetweenPoints(
            start=[1, 0.25, 0],  # Punto destro del corpo
            end=[0.3, 0.85, 0],  # Punto destro del collo
            angle=PI / 3,
        )

        # Impostiamo lo stile per le curve
        for curve in [left_curve, right_curve]:
            curve.set_style(stroke_color=WHITE, fill_color="#D3D3D3", fill_opacity=0.2)

        # Creiamo il liquido come due rettangoli separati
        # Parte statica (base) del liquido
        liquid = Rectangle(
            height=2.0,  # Altezza aumentata per raggiungere il fondo
            width=1.8,
            fill_color=BLUE_E,
            fill_opacity=0.7,
            stroke_width=0,
        ).move_to(np.array([0, bottle_body.get_center()[1] - 0.2, 0]))

        # Gruppo tutti gli elementi della bottiglia
        bottle = VGroup(bottle_body, bottle_neck, left_curve, right_curve)

        bubbles = VGroup()

        for _ in range(30):
            bubble = Circle(
                radius=0.05,
                color=WHITE,
                stroke_width=0.05,
                stroke_color=BLUE,
                fill_opacity=0.2,
            ).move_to(
                np.array(
                    [
                        np.random.uniform(
                            liquid.get_left()[0] + 0.2,
                            liquid.get_right()[0] - 0.2,
                        ),
                        np.random.uniform(
                            liquid.get_top()[1] - 0.2,
                            liquid.get_bottom()[1] + 0.1,
                        ),
                        0,
                    ]
                )
            )

            def move_bubble(bubble, dt):
                dx = np.random.uniform(-0.05, 0.05)  # Movimento laterale casuale
                dy = np.random.uniform(0.05, 0.1)  # Movimento verso l'alto
                bubble.shift([dx, dy, 0])
                if bubble.get_top()[1] > liquid.get_top()[1]:  # Reset posizione
                    bubble.move_to(
                        np.array(
                            [
                                np.random.uniform(
                                    liquid.get_left()[0] + 0.2,
                                    liquid.get_right()[0] - 0.2,
                                ),
                                np.random.uniform(
                                    liquid.get_top()[1] - 0.1,
                                    liquid.get_bottom()[1],
                                ),
                                0,
                            ]
                        )
                    )

            bubble.add_updater(move_bubble)
            bubbles.add(bubble)

        # Cerchio che rappresenta uvetta
        circle = Circle(
            radius=0.2,
            stroke_width=2,
            stroke_color=PURPLE_E,
            fill_color=LOGO_BLUE,
            fill_opacity=1,
        ).move_to(np.array([0, bottle_neck.get_top()[1] + 0.5, 0]))

        # Fattori di scala per le frecce
        gravity_scale = ValueTracker(1)  # Scala iniziale della forza di gravità
        archimedes_scale = ValueTracker(1)  # Scala iniziale della forza di Archimede
        gravity_label_scale = ValueTracker(0.6)  # Scala iniziale della forza di gravità
        archimedes_label_scale = ValueTracker(
            0.2
        )  # Scala iniziale della forza di Archimede

        # Forza di gravità (sempre aggiornata)
        gravity_arrow = always_redraw(
            lambda: Arrow(
                start=circle.get_center(),
                end=circle.get_center()
                + gravity_scale.get_value() * np.array([0, -0.5, 0]),
                color=GREEN_E,
                buff=0,
            )
        )

        # Forza di Archimede (sempre aggiornata)
        archimedes_arrow = always_redraw(
            lambda: Arrow(
                start=circle.get_center(),
                end=circle.get_center()
                + archimedes_scale.get_value() * np.array([0, 0.5, 0]),
                color=BLUE,
                buff=0,
            )
        )

        # Etichetta per la forza di gravità
        gravity_label = always_redraw(
            lambda: MathTex("F_g = m \\cdot g", color=GREEN_E)
            .scale(gravity_label_scale.get_value())
            .next_to(gravity_arrow, RIGHT, buff=0.1)
        )

        # Etichetta per la forza di Archimede
        archimedes_label = always_redraw(
            lambda: MathTex("F_A = \\rho \\cdot V \\cdot g", color=BLUE)
            .scale(archimedes_label_scale.get_value())
            .next_to(archimedes_arrow, LEFT, buff=0.1)
        )

        # Animazione
        self.play(DrawBorderThenFill(bottle), run_time=3)
        self.play(FadeIn(VGroup(liquid, bubbles)), run_time=2)

        archimedes_face = ImageMobject(
            "archimede.png"
        )  # Assicurati che il file sia nella stessa directory

        archimedes_face.scale(0.25)  # Ridimensiona l'immagine se necessario
        archimedes_face.to_corner(UP + LEFT)  # Posiziona nell'angolo in alto a sinistra
        self.play(FadeIn(archimedes_face), run_time=2)

        # Crea la nuvoletta di fumetto con il testo
        bubble_text = (
            Text(
                "Eureka! Ho trovato la soluzione!\nMa... che ci fate voi qua!",
                font_size=24,
                color=WHITE,
            )
            .next_to(archimedes_face, RIGHT, buff=0.2)
            .shift(UP * 0.5)
        )

        bubble_shape = (
            RoundedRectangle(
                corner_radius=0.3,
                width=bubble_text.width + 0.5,  # Aggiunge spazio attorno al testo
                height=bubble_text.height + 0.3,  # Aggiunge spazio attorno al testo
            )
            .set_fill(BLUE, opacity=0.6)
            .set_stroke(BLUE, width=2)
        ).surround(bubble_text)

        # Mostra la nuvoletta con il testo
        self.play(FadeIn(bubble_shape), Write(bubble_text), run_time=2)
        self.wait(3)
        self.play(FadeOut(bubble_text), FadeOut(bubble_shape), run_time=2)

        text2 = (
            Text(
                "Ahh ora ricordo...\nOggi faremo un esperimento affascinante!",
                font_size=24,
                color=WHITE,
            )
            .next_to(archimedes_face, RIGHT, buff=0.2)
            .shift(UP * 0.5)
        )

        bubble_shape2 = (
            RoundedRectangle(
                corner_radius=0.3,
                width=text2.width + 0.5,  # Aggiunge spazio attorno al testo
                height=text2.height + 0.3,  # Aggiunge spazio attorno al testo
            )
            .set_fill(BLUE, opacity=0.6)
            .set_stroke(BLUE, width=2)
        ).surround(text2)

        self.play(FadeIn(bubble_shape2), Write(text2), run_time=2)
        self.wait(3)
        self.play(FadeOut(text2), FadeOut(bubble_shape2), run_time=2)

        text3 = (
            Text(
                "Dimostreremo il MIO principio usando...\ndell'uvetta! Siamo umili scienziati,\nnon possiamo permetterci una\ncorona d'oro come il re...",
                font_size=24,
                color=WHITE,
            )
            .next_to(archimedes_face, RIGHT, buff=0.2)
            .shift(UP * 0.5)
        )

        bubble_shape3 = (
            RoundedRectangle(
                corner_radius=0.3,
                width=text3.width + 0.5,  # Aggiunge spazio attorno al testo
                height=text3.height + 0.3,  # Aggiunge spazio attorno al testo
            )
            .set_fill(BLUE, opacity=0.6)
            .set_stroke(BLUE, width=2)
        ).surround(text3)

        self.play(FadeIn(bubble_shape3), Write(text3), run_time=2)
        self.wait(5)
        self.play(FadeOut(text3), FadeOut(bubble_shape3), run_time=2)

        self.play(Create(circle), run_time=2)
        self.play(Create(gravity_arrow), FadeIn(gravity_label), run_time=1.5)
        self.play(
            circle.animate.move_to(liquid.get_center()), run_time=2, rate_func=smooth
        )
        self.wait(3)

        text4 = (
            Text(
                "Come potete vedere il chicco raggrinzito d'uva\ncola a picco come una dracma",
                font_size=24,
                color=WHITE,
            )
            .next_to(archimedes_face, RIGHT, buff=0.2)
            .shift(UP * 0.5)
        )

        bubble_shape4 = (
            RoundedRectangle(
                corner_radius=0.3,
                width=text4.width + 0.5,  # Aggiunge spazio attorno al testo
                height=text4.height + 0.3,  # Aggiunge spazio attorno al testo
            )
            .set_fill(BLUE, opacity=0.6)
            .set_stroke(BLUE, width=2)
        ).surround(text4)

        self.play(FadeIn(bubble_shape4), Write(text4), run_time=2)
        self.wait(3)
        self.play(FadeOut(text4), FadeOut(bubble_shape4), run_time=2)

        bubbles_around_circle = VGroup()
        num_bubbles = 10

        for i in range(num_bubbles):
            angle = (
                2 * PI * i / num_bubbles
            )  # Distribuiamo le bolle uniformemente lungo il cerchio
            new_bubble = Circle(
                radius=0.05,
                color=WHITE,
                stroke_width=0.05,
                stroke_color=BLUE,
                fill_opacity=0.2,
            )
            x = circle.get_center()[0] + (circle.radius + bubble.radius) * np.cos(angle)
            y = circle.get_center()[1] + (circle.radius + bubble.radius) * np.sin(angle)
            new_bubble.move_to(np.array([x, y, 0]))
            bubbles_around_circle.add(new_bubble)

        # Zoom in animation
        self.camera.frame.save_state()
        self.play(
            self.camera.frame.animate.scale(0.2).move_to(bottle_body.get_center()),
            gravity_label_scale.animate.set_value(0.2),
            run_time=1.5,
        )

        # Animazione delle bolle verso il centro del cerchio
        self.play(FadeOut(bubbles), FadeIn(bubbles_around_circle), run_time=1.5)
        self.play(Create(archimedes_arrow), FadeIn(archimedes_label), run_time=1.5)

        self.play(
            gravity_scale.animate.set_value(0.8),  # Riduce la forza di gravità
            archimedes_scale.animate.set_value(2),  # Aumenta la forza di Archimede
            run_time=2,
        )

        self.wait(2)

        self.play(
            Restore(self.camera.frame),
            gravity_label_scale.animate.set_value(0.6),
            archimedes_label_scale.animate.set_value(0.6),
            run_time=1.5,
        )

        self.play(FadeIn(bubbles))

        circle_and_bubbles = VGroup(circle, bubbles_around_circle)

        self.play(
            circle_and_bubbles.animate.move_to(
                np.array([circle.get_center()[0], liquid.get_top()[1], 0])
            ),
            run_time=1.5,
        )

        text5 = (
            Text(
                "Ma che diavoleria e' questa?\nLe bolle del liquido riportano\na galla l'uvetta!",
                font_size=24,
                color=WHITE,
            )
            .next_to(archimedes_face, RIGHT, buff=0.2)
            .shift(UP * 0.5)
        )

        bubble_shape5 = (
            RoundedRectangle(
                corner_radius=0.3,
                width=text5.width + 0.5,  # Aggiunge spazio attorno al testo
                height=text5.height + 0.3,  # Aggiunge spazio attorno al testo
            )
            .set_fill(BLUE, opacity=0.6)
            .set_stroke(BLUE, width=2)
        ).surround(text5)

        self.play(FadeIn(bubble_shape5), Write(text5), run_time=2)
        self.wait(3)
        self.play(FadeOut(text5), FadeOut(bubble_shape5), run_time=2)

        self.play(
            bubbles_around_circle.animate.scale(2).set_opacity(0),
            run_time=0.5,
        )

        text6 = (
            Text(
                "Ahh sono scoppiate!\nPerdincibacco che spavento!",
                font_size=24,
                color=WHITE,
            )
            .next_to(archimedes_face, RIGHT, buff=0.2)
            .shift(UP * 0.5)
        )

        bubble_shape6 = (
            RoundedRectangle(
                corner_radius=0.3,
                width=text6.width + 0.5,  # Aggiunge spazio attorno al testo
                height=text6.height + 0.3,  # Aggiunge spazio attorno al testo
            )
            .set_fill(BLUE, opacity=0.6)
            .set_stroke(BLUE, width=2)
        ).surround(text6)

        self.play(FadeIn(bubble_shape6), Write(text6), run_time=2)
        self.wait(3)
        self.play(FadeOut(text6), FadeOut(bubble_shape6), run_time=2)

        bubbles_around_circle_bis = VGroup()
        num_bubbles = 10

        for i in range(num_bubbles):
            new_bubble = Circle(
                radius=0.05,
                color=WHITE,
                stroke_width=0.05,
                stroke_color=BLUE,
                fill_opacity=0.2,
            )
            bubbles_around_circle_bis.add(new_bubble)

        circle_and_bubbles_bis = VGroup(circle, bubbles_around_circle_bis)

        text7 = (
            Text(
                "Ed ecco di nuovo che sprofonda!\nEsilarante, proprio come un pendolo!",
                font_size=24,
                color=WHITE,
            )
            .next_to(archimedes_face, RIGHT, buff=0.2)
            .shift(UP * 0.5)
        )

        bubble_shape7 = (
            RoundedRectangle(
                corner_radius=0.3,
                width=text7.width + 0.5,  # Aggiunge spazio attorno al testo
                height=text7.height + 0.3,  # Aggiunge spazio attorno al testo
            )
            .set_fill(BLUE, opacity=0.6)
            .set_stroke(BLUE, width=2)
        ).surround(text7)

        self.play(FadeIn(bubble_shape7), Write(text7), run_time=2)

        for i in range(2):
            self.play(
                gravity_scale.animate.set_value(2),
                archimedes_scale.animate.set_value(0.8),
                run_time=1,
            )

            self.play(
                circle.animate.move_to(liquid.get_center()),
                run_time=2,
                rate_func=smooth,
            )

            for i, bubble in enumerate(bubbles_around_circle_bis):
                angle = 2 * PI * i / num_bubbles
                x = circle.get_center()[0] + (circle.radius + bubble.radius) * np.cos(
                    angle
                )
                y = circle.get_center()[1] + (circle.radius + bubble.radius) * np.sin(
                    angle
                )
                bubble.move_to(np.array([x, y, 0]))

            self.play(FadeIn(bubbles_around_circle_bis))

            self.play(
                gravity_scale.animate.set_value(0.8),
                archimedes_scale.animate.set_value(2),
                run_time=1,
            )

            self.play(
                circle_and_bubbles_bis.animate.move_to(
                    np.array([circle.get_center()[0], liquid.get_top()[1], 0])
                ),
                run_time=2,
                rate_func=smooth,
            )

            self.play(FadeOut(bubbles_around_circle_bis))

        self.wait(2)
        self.play(FadeOut(text7), FadeOut(bubble_shape7), run_time=2)

        mobjects_to_fade = [mob for mob in self.mobjects if mob is not archimedes_face]

        self.play(*[FadeOut(mob) for mob in mobjects_to_fade], run_time=2)

        text8 = (
            Text(
                "Eureka!\nMa un principio, per essere tale, deve valere ovunque!\nDalla simulazione alla realtà...\nmettiamolo alla prova!",
                font_size=30,
                color=WHITE,
            )
            .next_to(archimedes_face, RIGHT, buff=0.2)
            .shift(UP * 0.5)
        )

        bubble_shape8 = (
            RoundedRectangle(
                corner_radius=0.3,
                width=text7.width + 1,  # Aggiunge spazio attorno al testo
                height=text7.height + 0.5,  # Aggiunge spazio attorno al testo
            )
            .set_fill(BLUE, opacity=0.6)
            .set_stroke(BLUE, width=2)
        ).surround(text8)

        self.play(FadeIn(bubble_shape8), Write(text8), run_time=2)
        self.wait(2)
        self.play(FadeOut(text8, bubble_shape8, archimedes_face))


class Credits(MovingCameraScene):
    def construct(self):
        archimedes_face = ImageMobject(
            "archimede.png"
        )  # Assicurati che il file sia nella stessa directory
        archimedes_face.scale(0.25)  # Ridimensiona l'immagine se necessario
        archimedes_face.to_corner(UP + LEFT)  # Posiziona nell'angolo in alto a sinistra

        text8 = (
            Text(
                "GRAZIE PER L'ATTENZIONE!",
                font_size=30,
                color=WHITE,
            )
            .next_to(archimedes_face, RIGHT, buff=0.2)
            .shift(UP * 0.5)
        )

        bubble_shape8 = (
            RoundedRectangle(
                corner_radius=0.3,
                width=text8.width + 0.5,  # Aggiunge spazio attorno al testo
                height=text8.height + 0.3,  # Aggiunge spazio attorno al testo
            )
            .set_fill(BLUE, opacity=0.6)
            .set_stroke(BLUE, width=2)
        ).surround(text8)

        self.play(FadeIn(archimedes_face), run_time=1)
        self.play(FadeIn(bubble_shape8), Write(text8), run_time=2)

        experimentalist = Text(
            "Experiments", font_size=35, color=BLUE, weight=BOLD
        ).set_stroke(width=1)

        colleague_name = Text(
            "Gabriele Todde", font_size=30, color=BLUE_B, slant=ITALIC
        )

        animationist = Text(
            "Animations", font_size=35, color=PURPLE, weight=BOLD
        ).set_stroke(width=1)

        your_name = Text("Alessandro Serra", font_size=30, color=PURPLE_B, slant=ITALIC)

        left_credits = VGroup(experimentalist, colleague_name).arrange(DOWN, buff=0.3)
        right_credits = VGroup(animationist, your_name).arrange(DOWN, buff=0.3)

        left_bg = RoundedRectangle(
            width=left_credits.width + 0.5,
            height=left_credits.height + 0.3,
            corner_radius=0.2,
            fill_opacity=0.1,
            fill_color=BLUE,
            stroke_width=1,
        ).move_to(left_credits)

        right_bg = RoundedRectangle(
            width=right_credits.width + 0.5,
            height=right_credits.height + 0.3,
            corner_radius=0.2,
            fill_opacity=0.1,
            fill_color=PURPLE,
            stroke_width=1,
        ).move_to(right_credits)

        left_group = VGroup(left_bg, left_credits).move_to(LEFT * 3)
        right_group = VGroup(right_bg, right_credits).move_to(RIGHT * 3)

        manim_credit = Text(
            "Animation Engine: Manim Community", font_size=20, color=GRAY_A
        ).next_to(left_group, DOWN, buff=1)

        manim_link = Text(
            "github.com/ManimCommunity/manim", font_size=18, color=BLUE_B, slant=ITALIC
        ).next_to(manim_credit, DOWN, buff=0.2)

        source_code = Text("Source Code:", font_size=20, color=GRAY_A).next_to(
            right_group, DOWN, buff=1
        )

        source_link = Text(
            "github.com/AlessandroSerra/ManimAnimations",  # Replace with your actual repo
            font_size=18,
            color=BLUE_B,
            slant=ITALIC,
        ).next_to(source_code, DOWN, buff=0.2)

        footer_left = VGroup(manim_credit, manim_link)
        footer_right = VGroup(source_code, source_link)

        self.play(
            FadeIn(left_bg, right_bg, shift=UP),
            Write(left_credits),
            Write(right_credits),
            run_time=2,
        )
        self.play(
            FadeIn(footer_left, shift=UP * 0.3),
            FadeIn(footer_right, shift=UP * 0.3),
            run_time=1.5,
        )
