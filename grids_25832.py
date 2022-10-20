import geopandas as gpd
# pip install geopandas / pip3 install geopandas
from shapely.geometry import Polygon
import numpy as np
import pandas as pd
import os
import math


def create_grid(zet, ebounds_minx, ebounds_miny, ebounds_maxx, ebounds_maxy,epsg):
    ##    ####bounds from UTM32N buffer , dont touch!
    xmin, ymin, xmax, ymax = 226226, 5266302, 773777.6070429870160297, 6260143.1024185577407479
    # print(extent.total_bounds)
    if zet == 2:
        KL = 4
    if zet == 3:
        KL = 8
    if zet == 4:
        KL = 16
    if zet == 5:
        KL = 32
    if zet == 6:
        KL = 64
    if zet == 7:
        KL = 128
    if zet == 8:
        KL = 256
    if zet == 9:
        KL = 512
    if zet == 10:
        KL = 1024
    if zet == 11:
        KL = 2048
    if zet == 12:
        KL = 4096
    if zet == 13:
        KL = 8192
    if zet == 14:
        KL = 16384
    if zet == 15:
        KL = 32768
    if zet == 16:
        KL = 65536
    if zet == 17:
        KL = 131072

    length = KL
    wide = length

    MINX, MINY, MAXX, MAXY = math.floor((ebounds_minx - xmin) / wide), math.floor(
        (ebounds_miny - ymin) / wide), math.ceil((ebounds_maxx - xmax) / wide), math.ceil((ebounds_maxy - ymax) / wide)

    cols = list(np.arange(xmin, xmax + wide, wide))
    rows = list(np.arange(ymin, ymax + length, length))

    polygons = []
    names = []
    for x in cols[MINX:MAXX - 2]:
        x_unity = int((x - xmin) / length)
        for y in rows[MINY:MAXY - 2]:
            y_unity = int((y - ymin) / length)
            k_unity = str(x_unity) + '_' + str(y_unity)
            Xmax, Ymax = x + wide, y + wide
            d = {'x_y': names}
            polygons.append(Polygon([(x, y), (x + wide, y), (x + wide, y + length), (x, y + length)]))
            names.append(k_unity)
    df = pd.DataFrame(d)
    grid = gpd.GeoDataFrame({'geometry': polygons})
    gdf = gpd.GeoDataFrame(df, geometry=polygons, crs=epsg)
    return gdf







