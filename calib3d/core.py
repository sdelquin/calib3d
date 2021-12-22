from pathlib import Path

import yaml
from rich.console import Console
from rich.table import Table

import settings
from calib3d import utils


class Calibration:
    def __init__(self, x, y, z, config_file: Path = settings.CONFIG_FILE):
        self.config = yaml.load(config_file.read_text(), Loader=yaml.FullLoader)
        self.measurements = {'X': x, 'Y': y, 'Z': z}

    def calculate_errors(self):
        calcube_side = self.config['calcube']['side']
        self.abs_errors, self.rel_errors = {}, {}
        for axis, measurement in self.measurements.items():
            self.abs_errors[axis] = measurement - calcube_side
            self.rel_errors[axis] = self.abs_errors[axis] * 100 / calcube_side

    def fix_steps(self):
        self.steps = {}
        for axis, measurement in self.measurements.items():
            self.steps[axis] = (
                measurement
                * self.config['axis-steps'][axis]
                / self.config['calcube']['side']
            )

    def show_results(self):
        console = Console()

        table = Table()
        table.add_column(style='italic')

        for axis, color in settings.AXIS_COLORS.items():
            table.add_column(f'{axis}', header_style=color)

        values = (f'{steps:.2f}' for steps in self.config['axis-steps'].values())
        table.add_row('Current steps', *values, end_section=True)

        values = (f'{measurement:.2f}' for measurement in self.measurements.values())
        table.add_row('Measurements', *values)

        values = (f'{utils.format_value(error)}' for error in self.abs_errors.values())
        table.add_row('Abs. errors', *values)

        values = (
            f'{utils.format_value(error, format=".1f", suffix="%")}'
            for error in self.rel_errors.values()
        )
        table.add_row('Rel. errors', *values, end_section=True)

        values = (f'{steps:.2f}' for steps in self.steps.values())
        table.add_row('Fixed steps', *values, style='yellow')

        console.print(table)

        console.print(
            'Calibrating 3D printer stepping motors from a '
            f'{self.config["calcube"]["side"]}mm cube\n'
            f'{self.config["calcube"]["url"]}',
            style='dim italic',
        )
