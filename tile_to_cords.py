import geopandas as gpd
from shapely.geometry import Polygon






def calc_cords(tile_x_y,zet,epsg):
    tile_x,tile_y=int(tile_x_y.split('_')[0]),int(tile_x_y.split('_')[1])

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

    offset_xmin=226226
    offset_ymin=5266302

    x=(KL*tile_x)+offset_xmin
    y=(KL*tile_y)+offset_ymin
    k=(Polygon([(x,y), (x+KL, y), (x+KL, y+KL), (x, y+KL)]))
    k_k=gpd.GeoSeries({'geometry':k},crs=epsg)
    return k_k


