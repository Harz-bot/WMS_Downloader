
from owslib.wms import  WebMapService
import os



def wms_download(out,url,layername,EPSG,pic_format,extend_minx,extend_miny,extend_maxx,extend_maxy,size):

    #choose layers of wms-service
    layer_sel=0
    #wms link
    #identify wms
    wms = WebMapService(url)
    wms.identification.type
    wms.identification.version
    wms.identification.title
    wms.identification.abstract

    #details of layers, titles, CRS, bbox, styles
    wms_list=list(wms.contents)
    #choose with layer_sel
    chosen_layer=str(wms_list[layer_sel])

    layer_styles=wms[chosen_layer].styles

    layer_title=wms[chosen_layer].title
    layer_crs=wms[chosen_layer].crsOptions
    layer_bb=wms[chosen_layer].boundingBox
    layer_styles=wms[chosen_layer].styles
    #the wms-downloader needs this order xmin,ymin,xmax,ymax

    #print(layer_crs,layer_bb,wms_list,layer_styles)


    bb=extend_minx,extend_miny,extend_maxx,extend_maxy

    img = wms.getmap(layers=[layername],
         styles=['default'],
         srs=EPSG,
         bbox=bb,
         size=(size,size),
         format='image/'+pic_format,
         transparent=True)
    png_tile=out
    out = open(png_tile, 'wb')
    out.write(img.read())
    out.close()
