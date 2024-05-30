import os
import logging
import ssl
import astrosat
import urllib.request
import yaml
from datetime import datetime
from astropy.coordinates import EarthLocation, AltAz, SkyCoord
import astropy.units as u

# Set up logging
logging.basicConfig(filename='astroSat.log', 
                    level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s: %(message)s')

print("Starting astroTest.py...")

# Set coordinates to Swinburne Hawthorn Campus
lat = -37.826350
lon = 145.038180
alt = 50

# Get current time
date_time = datetime.now()
# date_time = date_time.replace(hour=10)
# date_time = date_time.replace(minute=0)
# date_time = date_time.replace(second=0)

# Location of the observer
location = EarthLocation(lat=lat*u.deg, lon=lon*u.deg, height=alt*u.m)

# Convert to AltAz frame (zenith)
altaz = AltAz(obstime=date_time, location=location)
zenith = SkyCoord(alt=90*u.deg, az=0*u.deg, frame=altaz)

# Convert zenith to RA/Dec
ra_dec = zenith.transform_to('icrs')
ra = ra_dec.ra
dec = ra_dec.dec

# Convert RA and Dec to string format
#ra_str = ra.to_string(unit=u.hour, sep=':').split('.')[0]
#dec_str = dec.to_string(unit=u.deg, sep=':')
ra_str = str(ra.to_string(unit=u.hour, sep=':'))
dec_str = str(dec.to_string(unit=u.deg, sep=':'))

# Print set values
print("Generating parameters...")

# Parameters for the YAML file
params = {
    "cross_section": 0.01,
    "radius": 2.0,
    "duration": 5000,
    "Mmin": 0,
    "Mmax": 10.0,
    "plotDir": "./plots",
    "fdir": "./data",
    "TLEdir": "./TLE",
    "RA": ra_str,           # Example RA
    "DEC": dec_str,         # Example DEC
    "year": date_time.year,
    "month": date_time.month,
    "day": date_time.day,
    "hour": date_time.hour,
    "minute": date_time.minute,
    "seconds": date_time.second,
    "lat": lat,             # Latitude for Swinburne University of Technology
    "lon": lon,             # Longitude for Swinburne University of Technology
    "alt": alt,             # Elevation in meters
    "verbose": True,
}

# Retrieve and format dynamic date data
params_time = [params['hour'], params['minute'], params['seconds']]
for i, p in enumerate(params_time):
    params_time[i] = str(p).rjust(2, '0')

params_date = [params['day'], params['month'], params['year']]
params_date[0] = str(params_date[0]).rjust(2, '0')
params_date[1] = str(params_date[1]).rjust(2, '0')
params_date[2] = str(params_date[2]).rjust(4, '0')

# Retrieve and collate datetime
params_datetime = " ".join([
    ":".join(params_time),
    "-".join(params_date)
])

# Verify dynamic parameters for debug
print(f"\tTime: {params_datetime}")
print(f"\tLatitude: {lat}\n\tLongitude: {lon}\n\tAltitude: {alt}\n\tRA: {ra_str}\n\tDEC: {dec_str}\n\tDuration: {params['duration']}")

# Check with user
print("Are these parameters correct? (\'n\' will exit)")
if input().lower() == 'n':
    exit()

# Check if the parameters.yaml file exists, and create it if it doesn't
parameters_file = 'parameters.yaml'
if os.path.exists(parameters_file):
    with open(parameters_file, 'r') as file:
        existing_params = yaml.load(file, Loader=yaml.FullLoader)
    
    # Update the existing parameters with new values
    existing_params.update(params)

    with open(parameters_file, 'w') as file:
        yaml.dump(existing_params, file)
    logging.info('parameters.yaml file updated with new parameters.')
else:
    with open(parameters_file, 'w') as file:
        yaml.dump(params, file)
    logging.info('parameters.yaml file created with default parameters.')

# Custom function to download TLEs with SSL verification disabled
def download_tles(url):
    context = ssl._create_unverified_context()
    return original_urlopen(url, context=context)

# Save the original urlopen function
original_urlopen = urllib.request.urlopen

# Override the urlopen function in urllib.request
urllib.request.urlopen = download_tles

try:
    # Ensure the TLE directory exists
    TLE_DIR = './TLE'
    if not os.path.exists(TLE_DIR):
        os.makedirs(TLE_DIR)

    # Load parameters from the YAML file
    parameters = astrosat.Parameters(parameter_file=parameters_file)
    logging.info('Parameters loaded successfully.')

    # Initialize the AstroSat class
    AS = astrosat.AstroSat(parameters)
    logging.info('AstroSat object created.')

    # Download TLEs for active satellites
    satTLEs = AS.get_TLEs(satellite_type='active', forceNew=1)
    satTLEs += AS.get_TLEs(satellite_type='visual', forceNew=1)
    logging.info('TLEs downloaded.')

    # Get the satellite objects from TLEs
    satellites = AS.get_satellites(satTLEs)
    logging.info('Satellites data retrieved.')

    # Find satellites
    satDict = AS.find_intercept_sats(Fmodel=None)
    logging.info('Satellites interception calculated.')

    # Print the satellites that are overhead
    sat_table = AS.print_satellite_dictionary(satDict)
    logging.info('Satellites overhead printed.')

    # plot field
    plot = astrosat.Plot(AS)
    if len(sat_table)>0:
        plot.plot_satellites(sat_table)
    plot.plot_stars()
    plot.plot_legend([AS.parameters.Mmin, int(round((AS.parameters.Mmin + AS.parameters.Mmax) / 3.)), 2 * int(round((AS.parameters.Mmin + AS.parameters.Mmax) / 3.))])
    plot.make_plot(":".join(params_time))
    plot.save_plot('skyView_%i_%i.png' % (AS.parameters.radius, AS.parameters.date.timestamp()))

    print("Complete.")
except Exception as e:
    logging.error('An error occurred: %s', e, exc_info=True)
    print(f"An error occurred: {e}")
finally:
    # Restore the original urlopen function
    urllib.request.urlopen = original_urlopen

# Keep the console window open
input("Press Enter to exit...")
