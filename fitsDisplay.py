import matplotlib.pyplot as plt
from astropy.io import fits
import glob
import os

# Directory containing the FITS files
directory = 'C:/Users/arnni/Documents/Code Projects/NPS/output/2024-05-21T15-09-24.644543/ImageFiles/'

# List all FITS files in the directory
fits_files = glob.glob(os.path.join(directory, '*.fits'))

# Number of FITS files
num_files = len(fits_files)

# Determine the number of rows and columns for the subplots
cols = 3  # You can change this value based on how many columns you want
rows = (num_files // cols) + (num_files % cols > 0)

# Create subplots
fig, axes = plt.subplots(rows, cols, figsize=(15, 5 * rows))
axes = axes.flatten()  # Flatten the 2D array of axes for easy iteration

# Loop through all FITS files and display them
for i, file_path in enumerate(fits_files):
    # Load the FITS file
    hdul = fits.open(file_path)

    # Print FITS file information
    print(f"Displaying {file_path}")
    hdul.info()

    # Select the primary HDU
    image_data = hdul[0].data

    # Close the FITS file
    hdul.close()

    # Adjust brightness by setting vmin and vmax
    vmin = image_data.mean() - 0.5 * image_data.std()
    vmax = image_data.mean() + 3 * image_data.std()

    # Display the image data in the corresponding subplot
    im = axes[i].imshow(image_data, cmap='gray', vmin=vmin, vmax=vmax)
    axes[i].set_title(os.path.basename(file_path))
    axes[i].axis('off')  # Hide the axis

# Hide any remaining empty subplots
for j in range(i + 1, len(axes)):
    axes[j].axis('off')

# Adjust layout to prevent overlapping
plt.tight_layout()

# Add a colorbar to one of the subplots for reference
cbar = fig.colorbar(im, ax=axes, orientation='horizontal', fraction=0.05, pad=0.05)
cbar.set_label('Pixel Value Intensity')

plt.show()
