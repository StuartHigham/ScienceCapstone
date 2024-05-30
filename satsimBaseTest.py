import os
import glob
from satsim import gen_multi, load_json
from astride import Streak

def do(ssp, m):
    ssp['geometry']['obs'] = {
            "mode": "list",
            "list": {
                "$sample": "random.list",
                "length": 30,
                "value": {
                    "mode": "line",
                    "origin": [
                        { "$sample": "random.uniform", "low": 0.0, "high": 1.0 },
                        { "$sample": "random.uniform", "low": 0.0, "high": 1.0 }
                    ],
                    "velocity": [
                        { "$sample": "random.uniform", "low": 50, "high": 200 },
                        { "$sample": "random.uniform", "low": 50, "high": 200 }
                    ],
                    "mv": m
            }
        }
    }
    # Output directory
    output_dir = 'outputBaseTest/'
    os.makedirs(output_dir, exist_ok=True)  # Create the output directory if it doesn't exist

    # Generate SatNet files to output directory
    gen_multi(ssp, eager=True, output_dir=output_dir)

    directory = os.path.join(os.getcwd(), output_dir)

    print(f"Simulation complete. Output saved to {directory}")

    folders = glob.glob(os.path.join(directory, '*/'))

    newest_folder = max(folders, key=os.path.getmtime)
    newest_folder = newest_folder + 'ImageFiles/'

    all_files = glob.glob(os.path.join(newest_folder, '*.fits'))

    for file in all_files:
        streak = Streak(file, shape_cut=0.3)

        # Detect streaks
        streak.detect()

        # Write outputs and plot figures
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

magnitudes = [8.0, 9.0, 10.0, 11.0, 12.0]

ssp['geometry']['obs']['list'] = [ {
    "mode": "tle",
    "tle1": "1 25544U 98067A   24142.22205931  .00027404  00000-0  45846-3 0  9994",
    "tle2": "2 25544  51.6386  89.0025 0003364 190.6074 311.8384 15.51673454454369",
    "mv": 11.0
} ]

ssp['fpa']['num_frames'] = 1
ssp['fpa']['time']['exposure'] = 0.3

for m in magnitudes:
    do(ssp, m)
    