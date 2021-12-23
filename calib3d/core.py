from pathlib import Path

import yaml

import settings
from calib3d import display


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
        display.Display(self, show_gcode).print()
