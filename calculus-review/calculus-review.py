from manimlib.imports import *
import numpy as np


def get_arrow(number_line, tracking_value, value_update_function):
    arrow = ArrowTip(start_angle=-90 * DEGREES)
    arrow.next_to(number_line.number_to_point(tracking_value), UP, buff=0)
    arrow.add_updater(lambda mob: mob.next_to(number_line.number_to_point(value_update_function()), UP, buff=0))
    return arrow


class TangentExplain(ZoomedScene):
    CONFIG = {
        "x_start": 3,
        "x_end": 7,
        "axes_config": {
            "center_point": [-4.5, -2.5, 0],
            "x_axis_config": {
                "x_min": -1,
                "x_max": 10,
                "include_numbers": True
            },
            "y_axis_config": {
                "label_direction": UP,
                "x_min": -1,
                "x_max": 6,
                "include_numbers": True
            },
        },
        "func": lambda x: x ** 2,
        "func_config": {
            "color": RED,
            "x_min": -1,
            "x_max": 9,
        },
        "dot_radius": 0.1,
        "line_config": {}
    }

    def construct(self):
        axes = self.get_axes()
        func_graph = self.axes.get_graph(self.func, **self.func_config)

        # --- Definition ---
        x = 1
        # ValueTrackers definition
        delta_x_value = ValueTracker(0.5)
        # DecimalNumber definition
        delta_x_tex = DecimalNumber(
            delta_x_value.get_value()
        ).add_updater(
            lambda v: v.set_value(delta_x_value.get_value())
        )
        delta_fx_tex = DecimalNumber(
            self.delta_func(x, delta_x_value.get_value())
        ).add_updater(
            lambda v: v.set_value(self.delta_func(x, delta_x_value.get_value()))
        )
        # TeX labels definition
        delta_x_label = TexMobject(r"\Delta x=")
        delta_fx_label = TexMobject(r"\Delta f(x)=")
        # Dot definition
        x_dot = Dot(point=self.get_point_from_x_coordinate(x))
        plus_x_dot = Dot(point=self.get_point_from_x_coordinate(x + delta_x_value.get_value()))
        plus_x_dot.add_updater(
            lambda mob: mob.move_to(self.get_point_from_x_coordinate(x + delta_x_value.get_value()))
        )
        # Line definition
        tangent_line = Line(start=x_dot.get_center(), end=plus_x_dot.get_center())
        tangent_line.set_length(10)
        tangent_line.add_updater(
            lambda mob:
                True if delta_x_value.get_value() == 0
                else mob.put_start_and_end_on(
                        x_dot.get_center(),
                        plus_x_dot.get_center(),
                    ).set_length(10)
        )

        # --- Grouping ---
        # all labels and numbers
        group = VGroup(delta_x_tex, delta_fx_tex, delta_x_label, delta_fx_label)
        # separated labels and numbers
        delta_x_group = VGroup(delta_x_tex, delta_x_label)
        delta_fx_group = VGroup(delta_fx_tex, delta_fx_label)

        # --- Set position ---
        delta_x_label.next_to(delta_x_tex, LEFT, buff=0.2, aligned_edge=ORIGIN)
        delta_fx_label.next_to(delta_fx_tex, LEFT, buff=0.2, aligned_edge=ORIGIN)
        # Align labels and numbers
        VGroup(delta_x_group, delta_fx_group).arrange(DOWN, buff=2, aligned_edge=DOWN).to_edge(UR).shift(LEFT)

        # --- Create NumberLine ---
        delta_x_number_line = NumberLine(
            x_min=-0.5,
            x_max=0.5,
            unit_size=3,
            tick_frequency=0.1,
            include_numbers=True,
            numbers_to_show=[-0.5, 0, 0.5],
            decimal_number_config={
                "num_decimal_places": 1,
            },
        )
        delta_x_number_line_arrow = get_arrow(
            delta_x_number_line,
            delta_x_value.get_value(),
            delta_x_value.get_value,
        )
        delta_x_number_line_group = VGroup(delta_x_number_line, delta_x_number_line_arrow)
        delta_x_number_line_group.next_to(delta_x_group, DOWN, buff=0.5)

        delta_fx_number_line = NumberLine(
            x_min=-1,
            x_max=3,
            unit_size=1,
            include_numbers=True,
        )
        delta_fx_number_line_arrow = get_arrow(
            delta_fx_number_line,
            self.delta_func(x, delta_x_value.get_value()),
            lambda: self.delta_func(x, delta_x_value.get_value()),
        )
        delta_fx_number_line_group = VGroup(delta_fx_number_line, delta_fx_number_line_arrow)
        delta_fx_number_line_group.next_to(delta_fx_group, DOWN, buff=0.5)

        # --- Animation ---
        self.play(
            Write(axes),
            Write(x_dot),
            Write(plus_x_dot),
            Write(group),
            Write(delta_x_number_line_group),
            Write(delta_fx_number_line_group),
            Write(tangent_line),
            ShowCreation(func_graph),
        )
        self.wait()

        self.play(
            delta_x_value.set_value, -0.5,
            rate_func=double_smooth,
            run_time=10
        )
        self.wait()

    def delta_func(self, x, delta_x):
        return self.func(x + delta_x) - self.func(x)

    def get_axes(self):
        self.axes = Axes(**self.axes_config)
        # FIX Y LABELS
        y_labels = self.axes.get_y_axis().numbers
        for label in y_labels:
            label.rotate(-PI/2)
        return self.axes

    def get_point_from_x_coordinate(self,x_coord):
        return self.axes.c2p(x_coord, self.func(x_coord))
