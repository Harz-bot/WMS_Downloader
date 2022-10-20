import geopandas as gpd
import os
from grids_extend import *
from tile_to_cords import *
from wms_tiler import *
from check_duplicates import *
from gdal_cut import *
from grids_25832 import  *
from zet_to_pxlsize import *
import glob
                    ###parameters###
zet_start = 9
zet_end= 4

zet_range = zet_start - (zet_end +1)


end_size = z_to_PxlSisze(zet_end+1)
start_size = z_to_PxlSisze(zet_start)

pixl_size=int(start_size/end_size*256)
print(pixl_size)
epsg = "EPSG:25832"
minx, miny, maxx, maxy =415362.1930292358738370,5777902.0869861943647265, 434407.3158020462142304,5793783.7157657882198691
try:
    gpkgs = 'gpkgs'
    os.mkdir(gpkgs)
except:
    pass
try:
    start_tile_dir = 'start_tiles'
    os.mkdir(start_tile_dir)
except:
    pass
try:
    doubles_dir = 'start_tiles/doubles'
    os.mkdir(doubles_dir)
except:
    pass


bndl=gpd.read_file('BNDL_WMS_LINKS.gpkg',bbox=(minx, miny, maxx, maxy))
grid=crt_grid(zet_start, minx, miny, maxx, maxy, epsg)



grid_bndl = bndl.overlay(grid, how='intersection')
grid_bndl.to_file('bndl_grid.gpkg')
doubles=list_duplicates(grid_bndl['x_y'])

##download data


for index, tile in grid_bndl.iterrows():
    full_tile=calc_cords(tile['x_y'], zet_start, epsg)
    cutted_tile=tile['geometry']
    url=tile['wms_link']
    layername=tile['layer']
    print(tile['x_y'])

    ##download doubles tiles
    if tile['x_y'] in doubles:
        cutted_tile_gdf = gpd.GeoDataFrame(geometry=[cutted_tile], crs=epsg)
        cutted_tile_gdf.to_file(gpkgs + '/cutted' + tile['GEN'] + '_' + tile['x_y'] + '.gpkg')

        print('double')
        double_tiff = doubles_dir + '/' + tile['GEN'] + '_' + tile['x_y'] + '.tiff'
        wms_download(double_tiff, url, layername, epsg, 'tiff', full_tile.bounds.minx[0], full_tile.bounds.miny[0],
                     full_tile.bounds.maxx[0], full_tile.bounds.maxy[0],pixl_size)
        cutted_tiff = doubles_dir + '/cutted_' + tile['GEN'] + '_' + tile['x_y'] + '.tiff'
        cut_border(gpkgs + '/cutted' + tile['GEN'] + '_' + tile['x_y'] + '.gpkg', epsg, double_tiff, cutted_tiff)
        os.remove(double_tiff)
    else: #download normal tiles
        start_tile_png = start_tile_dir + '/' + tile['x_y'] + '.tiff'
        wms_download(start_tile_png,url,layername,epsg,'tiff',full_tile.bounds.minx[0],full_tile.bounds.miny[0],
                     full_tile.bounds.maxx[0],full_tile.bounds.maxy[0],pixl_size)
        print(tile['GEN'])
#        os.remove(start_tile_png)
for double in doubles:
    print(double)
    double_files = glob.glob(doubles_dir + '/*' + double + '.tiff')
    merge_tiffs(epsg, start_tile_dir + '/' + double + '.tiff',double_files)
    print(double_files)
for delete_files in glob.glob(doubles_dir + '/*.tiff'):
    os.remove(delete_files)

