import typer

from calib3d import Calibration

app = typer.Typer(add_completion=False)


@app.command()
def run(
    x: float = typer.Option(
        ..., '-X', help='Current measure (mm) for X axis from calibration cube'
    ),
    y: float = typer.Option(
        ..., '-Y', help='Current measure (mm) for Y axis from calibration cube'
    ),
    z: float = typer.Option(
        ..., '-Z', help='Current measure (mm) for Z axis from calibration cube'
    ),
    gcode: bool = typer.Option(
        False, '-g', '--gcode', help='Dump G-code', show_default=False
    ),
    verbose: bool = typer.Option(
        False, '-v', '--verbose', help='Verbose mode', show_default=False
    ),
    update_steps: bool = typer.Option(
        False,
        '-u',
        '--update',
        help='Update fixed steps on config file',
        show_default=False,
    ),
):
    calib = Calibration(x, y, z)
    calib.calculate_errors()
    calib.fix_steps()
    calib.show_results(show_gcode=gcode, show_details=verbose)
    if update_steps:
        calib.update_steps()


if __name__ == "__main__":
    app()
