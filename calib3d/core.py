from pathlib import Path

import yaml
from rich import print
from rich.console import Console
from rich.table import Table

import settings


class Calibration:
    def __init__(self, config_file: Path = settings.CONFIG_FILE):
        self.config = yaml.load(config_file.read_text(), Loader=yaml.FullLoader)

    def read_measurements(self):
        self.measurements = {}
        print(
            f'[dim]Enter measurements for {self.config["cube-side"]}mm '
            'calibration cube:[/dim]'
        )
        for axis, color in settings.AXIS_COLORS.items():
            print(f'[bold {color}]{axis}:[/bold {color}]', end=' ')
            self.measurements[axis] = float(input())

    def calculate_errors(self):
        self.errors = {}
        for axis, measurement in self.measurements.items():
            self.errors[axis] = measurement - self.config['cube-side']

    def fix_steps(self):
        self.steps = {}
        for axis, measurement in self.measurements.items():
            self.steps[axis] = (
                measurement * self.config['axis-steps'][axis] / self.config['cube-side']
            )

    def show_steps(self):
        table = Table()
        table.add_column(style='italic')

        for axis, color in settings.AXIS_COLORS.items():
            table.add_column(f'{axis}', header_style=color)

        values = (f'{measurement:.2f}' for measurement in self.measurements.values())
        table.add_row('Measurements', *values)

        display = []
        for error in self.errors.values():
            if error > 0:
                color = 'green'
            elif error < 0:
                color = 'red'
            else:
                color = 'white'
            display.append(f'[{color}]{error:.2f}[/{color}]')
        table.add_row('Errors', *display)

        values = (f'{steps:.2f}' for steps in self.config['axis-steps'].values())
        table.add_row('Current steps', *values)

        values = (f'{steps:.2f}' for steps in self.steps.values())
        table.add_row('Fixed steps', *values, style='yellow')

        console = Console()
        console.print(table)
