import hardpotato as hp
import glob
import re 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# select the potentiostat model to use:
model = 'chi920d'

# Path to the chi software, including  extension .exe
path = 'C:/Users/parasita/Downloads/chi920d/chi920d.exe'

# Folder where to save the datam it needs to be created previusly
folder = './data/tests/SECM_test'

# Setup hardpotato:
hp.potentiostat.Setup(model, path, folder)
# Setup SECM mode:
secm = hp.potentiostat.SECM()

# Approach paramenters:
E1 = 0.4             # V, Potential in working electrode 1 (UME)
iratio = 60          # %, Current ratio threshold
sens = 1e-9          # A/V, Current sensitivity of the working electrode 1 (UME)
maxincr = 1          # um/s, Approach speed
withdraw = 150         # um, Probe withdraw distance before probe approach
# Grid parameters:
xsize = 20          # um, X size
ysize = 30          # um, Y size
xstep = 2           # um, Step in X
ystep = 3           # um, Step in Y
currentX = 0        # Set x position to 0 before imaging
currentY = 0        # Set y position to 0 before imaging

# Scan for loop (NOTE: you can change the long direction by inverting the order of the loops)
for x in range (0, xsize, xstep):
    for y in range (0, ysize, ystep): 
        dX = x - currentX
        currentX = x
        dY = y - currentY
        currentY = y
        fileName = f'PAC_x{x}_y{y}'
        secm.MOVE('step', x=dX, y=dY)
        secm.PAC(E1, iratio, sens, maxincr, withdraw, fileName)
        secm.RUN()

# Plot
# Preprocessing: separating data from each PAC and labelling with x e y position
files = glob.glob("*.txt")
data = []
for file in files:
    match = re.search(r"_x(-?\d+)_y(-?\d+)", file)
    if match is None:
        continue

    x = int(match.group(1))
    y = int(match.group(2))

    df = pd.read_csv(file)
    distance_max = df['Distance/um'].max()
    data.append((x, y, distance_max))

data = pd.DataFrame(data, columns=['x', 'y', 'Distance'])

# Plotting
heatmap = data.pivot(index='y', columns='x', 'Distance')
x = heatmap.columns.values
y = heatmap.index.values
z = heatmap.values

plt.figure(figsize=8,6)
plt.pcolormesh(x, y, z, shading='auto', cmap='viridis')
plt.xlabel('X')
plt.ylabel('Y')
plt.colorbar(label='Maximum Distance / um')
plt.tight_layout()
plt.show()

