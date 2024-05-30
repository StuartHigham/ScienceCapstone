import os
import glob
from satsim import gen_multi, load_json
from astride import Streak

def do(ssp, mag, exp, sam):
    ssp['fpa']['time']['exposure'] = exp

    ssp['geometry']['obs'] = {
            "mode": "list",
            "list": {
                "$sample": "random.list",
                "length": sam,
                "value": {
                    "mode": "line",
                    "origin": [
                        { "$sample": "random.uniform", "low": 0.1, "high": 0.9 },
                        { "$sample": "random.uniform", "low": 0.1, "high": 0.9 }
                    ],
                    "velocity": [
                        { "$sample": "random.uniform", "low": 50, "high": 200 },
                        { "$sample": "random.uniform", "low": 50, "high": 200 }
                    ],
                    "mv": mag
            }
        }
    }

    print(f"Current image:\n\tMag = {mag}\n\tSam = {sam}\n\tExp = {exp}")

    # Output directory
    output_dir = 'outputMultiStreak/'
    os.makedirs(output_dir, exist_ok=True)  # Create the output directory if it doesn't exist

    # Generate SatNet files to output directory
    print("Generating SatSim files...")
    gen_multi(ssp, eager=True, output_dir=output_dir)

    directory = os.path.join(os.getcwd(), output_dir)

    print(f"Simulation complete. Output saved to {directory}")
    print("Commencing ASTRiDE analysis...")

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
    
    print("Finished analysis.\n")

# Print current working directory
print("Current Working Directory:", os.getcwd())

# Configuration file path
config_path = 'input/config.json'
if not os.path.isfile(config_path):
    raise FileNotFoundError(f"The configuration file was not found at: {config_path}")

# Load the configuration JSON file
ssp = load_json(config_path)

# Tests to be done
magnitudes = [6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0]
exposures = [0.1, 0.2, 0.3, 0.4, 0.5]
samples = [5, 15, 25]

ssp['fpa']['num_frames'] = 1

for mag in magnitudes:
    for i, exp in enumerate(exposures):
        for j, sam in enumerate(samples):
            do(ssp, mag, exp, sam)