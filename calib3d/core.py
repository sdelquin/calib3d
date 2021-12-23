from pathlib import Path

import yaml
from rich.console import Console
from rich.table import Table

import settings
from calib3d import utils


class Calibration:
    def __init__(self, x, y, z, config_file: Path = settings.CONFIG_FILE):
        self.measurements = {'X': x, 'Y': y, 'Z': z}
        self.config_file = config_file
        self.config = yaml.load(config_file.read_text(), Loader=yaml.FullLoader)

    def calculate_errors(self):
        calcube_side = self.config['calcube']['side']
        self.errors, self.valid_errors = {}, {}
        for axis, measurement in self.measurements.items():
            self.errors[axis] = measurement - calcube_side
            self.valid_errors[axis] = (
                abs(self.errors[axis]) <= self.config['calcube']['valid-error']
            )

    def fix_steps(self):
        self.steps = {}
        for axis, measurement in self.measurements.items():
            if self.valid_errors[axis]:
                step = self.config['steps'][axis]
            else:
                step = (
                    measurement
                    * self.config['steps'][axis]
                    / self.config['calcube']['side']
                )
            self.steps[axis] = step

    def update_steps(self):
        self.config['steps'] = self.steps
        # Fix floating point issues
        for axis in self.config['steps']:
            self.config['steps'][axis] = round(self.config['steps'][axis], 2)
        output = yaml.dump(self.config, Dumper=yaml.Dumper)
        self.config_file.write_text(output)

    def show_results(self, show_gcode=False):
        console = Console()

        table = Table()
        table.add_column(style='italic')

        for axis, color in settings.AXIS_COLORS.items():
            table.add_column(f'{axis}', header_style=color)

        values = (f'{steps:.2f}' for steps in self.config['steps'].values())
        table.add_row('Current steps', *values, end_section=True)

        values = (f'{measurement:.2f}' for measurement in self.measurements.values())
        table.add_row('Measurements', *values)

        valid_error = self.config['calcube']['valid-error']
        values = (
            f'{utils.format_value(error, threshold=valid_error)}'
            for error in self.errors.values()
        )
        table.add_row('Errors', *values, end_section=True)

        values = (f'{steps:.2f}' for steps in self.steps.values())
        table.add_row('Fixed steps', *values, style='yellow')

        console.print(table)

        console.print(
            'Calibrating 3D printer stepping motors from a '
            f'{self.config["calcube"]["side"]}mm cube',
            style='dim italic',
        )

        if show_gcode:
            fixed_steps = ' '.join(
                f'{axis}{step:.2f}'
                for axis, step in self.steps.items()
                if not self.valid_errors[axis]
            )
            console.print(f'[dark_orange]G-code: M92 {fixed_steps}[/dark_orange]')
