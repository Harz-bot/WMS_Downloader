from osgeo import gdal

def cut_border(cut_tile ,epsg,tile_in, out_cutted_tiff):

    warp1 = gdal.Warp(out_cutted_tiff, tile_in, cutlineDSName=cut_tile, cropToCutline=True,
                      dstNodata=-0)


    #to_png = gdal.Translate(out_fin, out_merge, noData=None, format="PNG")  # ,bandList=[1,2,3])

def cut_tile(tiff_in,out_tiff,png_out,minx_zoom,miny_zoom,maxx_zoom,maxy_zoom,epsg):
    gdal.Warp(out_tiff, tiff_in, dstNodata=0, srcSRS=epsg, height=256, width=256, dstSRS=epsg,
              outputBoundsSRS=epsg, outputBounds=[minx_zoom,miny_zoom,maxx_zoom,maxy_zoom])
    gdal.Translate(png_out, out_tiff, noData=None, format="PNG")# ,bandList=[1,2,3])


def merge_tiffs(epsg,out_tiff, files,):
    gdal.Warp(out_tiff, files, dstNodata=0, srcSRS=epsg, height=256, width=256, dstSRS=epsg)
