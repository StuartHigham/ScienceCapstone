import os
import glob
from satsim import gen_multi, load_json
from astride import Streak

def do(ssp, mag, bm):
    ssp['background']['galactic'] = bm
    ssp['geometry']['obs']['list'] = [ {
        "mode": "tle",
        "tle1": "1 25544U 98067A   24142.22205931  .00027404  00000-0  45846-3 0  9994",
        "tle2": "2 25544  51.6386  89.0025 0003364 190.6074 311.8384 15.51673454454369",
        "mv": mag
    } ]

    # Output directory
    output_dir = 'outputMagMag/'
    os.makedirs(output_dir, exist_ok=True)  # Create the output directory if it doesn't exist

    # Generate SatNet files to output directory
    gen_multi(ssp, eager=True, output_dir=output_dir)

    directory = os.path.join(os.getcwd(), output_dir)

    print(f"Simulation complete, commencing ASTRiDE analysis...")

    folders = glob.glob(os.path.join(directory, '*/'))

    newest_folder = max(folders, key=os.path.getmtime)
    newest_folder = newest_folder + 'ImageFiles/'

    all_files = glob.glob(os.path.join(newest_folder, '*.fits'))

    for file in all_files:
        streak = Streak(file)

        # Detect streaks.
        streak.detect()

        # Write outputs and plot figures.
        streak.write_outputs()
        streak.plot_figures()

# Print current working directory
print("Current Working Directory:", os.getcwd())

# Configuration file path
config_path = 'input/config.json'
if not os.path.isfile(config_path):
    raise FileNotFoundError(f"The configuration file was not found at: {config_path}")

# Load the configuration JSON file
ssp = load_json(config_path)

# Tests to be done
magnitudes = [6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0]
backMags = [26, 24, 22, 20, 18, 16, 14, 12, 10, 8]

magLength = len(magnitudes)
bacLength = len(backMags)
totLength = magLength * bacLength
ind = 0

ssp['fpa']['time']['exposure'] = 0.5
ssp['fpa']['num_frames'] = 3

for mag in magnitudes:
    for bm in backMags:
        ind += 1
        do(ssp, mag, bm)
        print(f"{round(100 * ind / totLength, 1)}% complete.")