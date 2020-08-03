from manimlib.imports import *

class TangentExplain(Scene):
    CONFIG = {
        "x_start": 3,
        "x_end": 7,
        "axes_config": {
            "center_point": [-4.5,-2.5,0],
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
        "func": lambda x: x ** 3,
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
        func = self.axes.get_graph(self.func,**self.func_config)

        x = 1
        # x_value = ValueTracker(1)
        # fx_value = ValueTracker(self.func(x_value))
        delta_x_value = ValueTracker(0.5)
        # plus_fx_value = ValueTracker(self.func(x_value.get_value() + delta_x_value.get_value()))
        delta_fx_value = ValueTracker(self.func(x + delta_x_value.get_value()) - self.func(x))

        delta_x_tex = DecimalNumber(delta_x_value.get_value()).add_updater(lambda v: v.set_value(delta_x_value.get_value()))
        delta_fx_tex = DecimalNumber(delta_fx_value.get_value()).add_updater(lambda v: v.set_value(delta_fx_value.get_value()))

        x_dot = self.get_dot_from_x_coord(x)
        plus_x_dot = self.get_dot_from_x_coord(x + delta_x_value.get_value())

        self.play(
            Write(axes),
            Write(x_dot),
            Write(plus_x_dot),
            ShowCreation(func),
        )
        self.wait()

    def get_axes(self):
        self.axes = Axes(**self.axes_config)
        # FIX Y LABELS
        y_labels = self.axes.get_y_axis().numbers
        for label in y_labels:
            label.rotate(-PI/2)
        return self.axes

    def get_dot_from_x_coord(self,x_coord,**kwargs):
        return Dot(
            self.get_f(x_coord),
            radius=self.dot_radius,
            **kwargs
        )

    def get_f(self,x_coord):
        return self.axes.c2p(x_coord, self.func(x_coord))

class FunctionTrackerWithNumberLine(Scene):
    def construct(self):
        # f(x) = x**2
        fx = lambda x: x.get_value()**2
        # ValueTrackers definition
        x_value = ValueTracker(0)
        fx_value = ValueTracker(fx(x_value))
        # DecimalNumber definition
        x_tex = DecimalNumber(x_value.get_value()).add_updater(lambda v: v.set_value(x_value.get_value()))
        fx_tex = DecimalNumber(fx_value.get_value()).add_updater(lambda v: v.set_value(fx(x_value)))
        # TeX labels definition
        x_label = TexMobject("x = ")
        fx_label = TexMobject("x^2 = ")
        # Grouping of labels and numbers
        group = VGroup(x_tex,fx_tex,x_label,fx_label).scale(2)
        # Set the labels position
        x_label.next_to(x_tex,LEFT, buff=0.7,aligned_edge=x_label.get_bottom())
        fx_label.next_to(fx_tex,LEFT, buff=0.7,aligned_edge=fx_label.get_bottom())
        # Grouping numbers and labels
        x_group = VGroup(x_label,x_tex)
        fx_group = VGroup(fx_label,fx_tex)
        # Align labels and numbers
        VGroup(x_group, fx_group).arrange_submobjects(RIGHT,buff=2,aligned_edge=DOWN).to_edge(UP)
        # Get NumberLine,Arrow and label from x
        x_number_line_group = self.get_number_line_group(
            "x",30,0.2,step_label=10,v_tracker=x_value,tick_frequency=2
            )
        x_number_line_group.to_edge(LEFT,buff=1)
        # Get NumberLine,Arrow and label from f(x)
        fx_number_line_group = self.get_number_line_group(
            "x^2",900,0.012,step_label=100,v_tracker=fx_tex,
            tick_frequency=50
            )
        fx_number_line_group.next_to(x_number_line_group,DOWN,buff=1).to_edge(LEFT,buff=1)

        self.add(
            x_number_line_group,
            fx_number_line_group,
            group
            )
        self.wait()
        self.play(
            x_value.set_value,30,
            rate_func=linear,
            run_time=10
            )
        self.wait()
        self.play(
            x_value.set_value,0,
            rate_func=linear,
            run_time=10
            )
        self.wait(3)


    def get_numer_labels_to_numberline(self,number_line,x_max=None,x_min=0,buff=0.2,step_label=1,**tex_kwargs):
        # This method return the labels of the NumberLine
        labels = VGroup()
        x_max = number_line.x_max
        for x in range(x_min,x_max+1,step_label):
            x_label = TexMobject(f"{x}",**tex_kwargs)
            # See manimlib/mobject/number_line.py CONFIG dictionary
            x_label.next_to(number_line.number_to_point(x),DOWN,buff=buff)
            labels.add(x_label)
        return labels

    def get_number_line_group(self,label,x_max,unit_size,v_tracker,step_label=1,**number_line_config):
        # Set the Label (x,or x**2)
        number_label = TexMobject(label)
        # Set the arrow 
        arrow = ArrowTip(start_angle=-90 * DEGREES)
        # Set the number_line
        number_line = NumberLine(
            x_min=0,
            x_max=x_max,
            unit_size=unit_size,
            numbers_with_elongated_ticks=[],
            **number_line_config
            )
        # Get the labels from number_line
        labels = self.get_numer_labels_to_numberline(number_line,step_label=step_label,height=0.2)
        # Set the arrow position
        arrow.next_to(number_line.number_to_point(0),UP,buff=0)
        # Grouping arrow and number_label
        label = VGroup(arrow,number_label)
        # Set the position of number_label
        number_label.next_to(arrow,UP,buff=0.1)
        # Grouping all elements
        numer_group = VGroup(label,number_line,labels)
        # Set the updater to the arrow and number_label
        label.add_updater(lambda mob: mob.next_to(number_line.number_to_point(v_tracker.get_value()),UP,buff=0))

        return numer_group