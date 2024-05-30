import subprocess

scripts = ['satsimTestMagExp.py', 'satsimTestMagMag.py', 'satsimTestNoStars.py']

for script in scripts:
    print(f'Beginning script {script}...')

    # Run each script and wait for it to finish
    result = subprocess.run(['py', script], capture_output=True, text=True)
    
    # Print the output of each script
    print(f"Output of {script}:\n{result.stdout}")
    print(f"Errors of {script}:\n{result.stderr}")
    
    # Check if the script ran successfully
    if result.returncode != 0:
        print(f"Script {script} failed with return code {result.returncode}")
        break