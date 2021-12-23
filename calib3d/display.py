from rich.console import Console
from rich.table import Table

import settings
from calib3d import utils


class Display:
    def __init__(self, calibration, show_gcode=False, show_details=False):
        self.calibration = calibration
        self.show_gcode = show_gcode
        self.show_details = show_details
        self.console = Console()

    def add_header(self, table):
        table.add_column(style='italic')
        for axis, color in settings.AXIS_COLORS.items():
            table.add_column(f'{axis}', header_style=color)

    def add_current_steps(self, table):
        values = (f'{steps:.2f}' for steps in self.calibration.config['steps'].values())
        table.add_row('Current steps', *values, end_section=True)

    def add_measurements(self, table):
        values = (
            f'{measurement:.2f}' for measurement in self.calibration.measurements.values()
        )
        table.add_row('Measurements', *values)

    def add_errors(self, table):
        valid_error = self.calibration.config['calcube']['valid-error']
        values = (
            f'{utils.format_value(error, threshold=valid_error)}'
            for error in self.calibration.errors.values()
        )
        table.add_row('Errors', *values, end_section=True)

    def add_fixed_steps(self, table):
        values = []
        for axis, steps in self.calibration.steps.items():
            if self.calibration.valid_errors[axis]:
                display = f'{steps:.2f}'
            else:
                display = f'[yellow]{steps:.2f}[/yellow]'
            values.append(display)
        table.add_row('Fixed steps', *values)

    def print_table(self, table):
        self.console.print(table)

    def print_details(self):
        self.console.print(
            'Calibrating 3D printer stepping motors from a '
            f'{self.calibration.config["calcube"]["side"]}mm cube',
            style='tan',
        )
        self.console.print(
            'Valid errors equal or lower than '
            f'{self.calibration.config["calcube"]["valid-error"]}mm',
            style='tan',
        )

    def print_gcode(self):
        values = []
        for axis, color in settings.AXIS_COLORS.items():
            if not self.calibration.valid_errors[axis]:
                values.append(
                    f'[{color}]{axis}{self.calibration.steps[axis]:.2f}[/{color}]'
                )
        fixed_steps = ' '.join(values)
        self.console.print(f'[dim]G-code:[/dim] M92 {fixed_steps}')

    def print(self):
        if self.show_details:
            self.print_details()
        table = Table()
        self.add_header(table)
        self.add_current_steps(table)
        self.add_measurements(table)
        self.add_errors(table)
        self.add_fixed_steps(table)
        self.print_table(table)
        if self.show_gcode:
            self.print_gcode()
