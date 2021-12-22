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
            f'[dim]Enter measurements of {self.config["cube-side"]}mm '
            'calibration cube:[/dim]'
        )
        for axis, color in settings.AXIS_COLORS.items():
            print(f'[bold {color}]{axis}:[/bold {color}]', end=' ')
            self.measurements[axis] = float(input())

    def fix_steps(self):
        self.steps = {}
        for axis, measurement in self.measurements.items():
            self.steps[axis] = (
                measurement * self.config['steps'][axis] / self.config['cube-side']
            )

    def show_steps(self):
        table = Table(show_header=True, header_style="bold magenta")
        for axis in self.steps.keys():
            table.add_column(f'{axis} steps')
        values = (f'{steps:.2f}' for steps in self.steps.values())
        table.add_row(*values)
        console = Console()
        console.print(table)
