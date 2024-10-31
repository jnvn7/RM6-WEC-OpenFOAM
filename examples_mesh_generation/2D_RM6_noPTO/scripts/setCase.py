#!/usr/bin/env python3
import sys
import numpy as np
import coreFuncs as cF

#-----------------------------------Constant Definition----------------------------#
g = 9.81
tankWidth2D = 0.01

#---------------------------------Read In Flow Settings----------------------------#
# Read flowParams file
rOut = cF.readFlowParamMeshing(cF.flowParams)

##-----------------------------Unpack flowParams Properties------------------------#
# Find the Object Bounding Box
boundingBox = cF.readBoundingBox()

# Wave parameters
sim3D = rOut["sim3D"]
waveHeight = rOut["waveHeight"]
wavePeriod = rOut["wavePeriod"]
waveL = 2*np.pi/cF.waveNumber(g, 2*np.pi/rOut["wavePeriod"], rOut["waterDepth"], deepWater=True)

# Object Mesh and Refinement Parameters
objName = rOut["objName"]
objScale = rOut["objScale"] 
if rOut["baffleName"] == 'none':
    plotBaffle = 0
else:
    plotBaffle = 1

fOut = rOut["translate"].split('(')[1].split(',')
transX = float(fOut[0])
transY = float(fOut[1])
transZ = float(fOut[2][:-1])

# Background Mesh and Refinement Parameters
nRefineZones = rOut["nRefineZones"]
zoneHeightRatio = rOut["zoneHeightRatio"]
zoneWidthRatio = rOut["zoneWidthRatio"]
nLayerOverlap = rOut["nLayerOverlap"]

# Mesh resolution (finest region)e
xContr = rOut["xContr"]
zContr = rOut["zContr"]
hContr = rOut["hContr"]
lengthContr = rOut["lengthContr"]

# Wave Tank Parameters
waterDepth = rOut["waterDepth"]
tankL = rOut["tankLength"]
tankH = rOut["tankHeight"]
tankW = rOut["tankWidth"]

if (tankL == 0):
    tankL = lengthContr*waveL
    
if (tankH == 0):
    tankH = 2*waterDepth

if (sim3D == 0):
    tankW = tankWidth2D
 
tankLHW = [tankL, tankH, tankW]

##------------Evaluate object mesh setup and write data to file-----------------#
# Prep Data for Object Setup. Mesh location and cell sizes
Xfn = objScale*boundingBox[0]
Yfn = objScale*boundingBox[1]
Zfn = objScale*boundingBox[2]

Xfp = objScale*boundingBox[3]
Yfp = objScale*boundingBox[4]
Zfp = objScale*boundingBox[5]
    
objHeight = (Zfp-Zfn)
objWidth = (Yfp-Yfn)
objLength = (Xfp-Xfn)

# Determine the cellsize as minimum of cells per wavelength, 
# and cells per wave height
cellSize = min(waveHeight/zContr, waveL/xContr)
objSizeInc = nLayerOverlap*cellSize
Xfn -= objSizeInc 
Xfp += objSizeInc 
Yfn -= objSizeInc
Yfp += objSizeInc 
Zfn -= objSizeInc
Zfp += objSizeInc 

xCellsf = int(objLength/cellSize+nLayerOverlap)         
yCellsf = int(objWidth/cellSize+nLayerOverlap)          
zCellsf = int(objHeight/cellSize+nLayerOverlap)         

xc = (Xfn+Xfp)/2
yc = (Yfn+Yfp)/2
zc = (Zfn+Zfp)/2

if (sim3D == 0):
    Yfn = yc - tankWidth2D/2
    Yfp = yc + tankWidth2D/2
    yCellsf = 1

locMeshX = str(Xfn+5*cellSize)
locMeshY = str(yc)
locMeshZ = str(zc)

locationInMesh = ('('+locMeshX+' '+locMeshY+' '+locMeshZ+')')

# Writing Object Snappy Setup
if (len(sys.argv)>1 and sys.argv[1] == '-o'):
    with open(cF.objMeshingLoc,'w') as fout:        
        fout.write('//Object Dimensions and Mesh sizings:\n')
        fout.write('objName\t'+objName+';\n')
        fout.write('objEMesh\t'+objName.split('.')[0]+'.eMesh;\n')
        if (not rOut["baffleName"] == 'none'):
            fout.write('baffleName\t'+rOut["baffleName"]+';\n')
            fout.write('baffleEMesh\t'+rOut["baffleName"].split('.')[0]+'.eMesh;\n')
        fout.write('objScale\t'+str(objScale)+';\n')
        fout.write('plotBaffle\t'+str(plotBaffle)+';\n\n')
        fout.write('Xfn\t'+str(Xfn)+';\n')
        fout.write('Yfn\t'+str(Yfn)+';\n')
        fout.write('Zfn\t'+str(Zfn)+';\n')
        fout.write('Xfp\t'+str(Xfp)+';\n')
        fout.write('Yfp\t'+str(Yfp)+';\n')
        fout.write('Zfp\t'+str(Zfp)+';\n\n')

        fout.write('xCellsf\t'+str(xCellsf)+';\n')
        fout.write('yCellsf\t'+str(yCellsf)+';\n')
        fout.write('zCellsf\t'+str(zCellsf)+';\n\n')

        fout.write('// castellatedMeshControls in SnappyHexMesh:\n')
        fout.write('locationInMesh\t'+str(locationInMesh)+';\n\n')

##------------Evaluate background mesh setup and write data to file-----------------#
if (len(sys.argv)>1 and sys.argv[1] == '-b'):
    # Apply translation to the object
    Xfn += transX
    Xfp += transX
    Yfn += transY
    Yfp += transY
    Zfn += transZ
    Zfp += transZ

    # Prep Data for Wave Flume Setup. Mesh location and cell sizes. 
    waterSurface = 0.0  #zc
    zc = waterSurface	#reset zc to waterSurface?

    Xtn = xc - tankLHW[0]/2
    Xtp = xc + tankLHW[0]/2
    Ytn = yc - tankLHW[2]/2
    Ytp = yc + tankLHW[2]/2
    Ztn = zc - waterDepth
    Ztp = zc + (tankLHW[1]-waterDepth)

    if (nRefineZones == 0):
        bgCellSize = cellSize
    else:
        bgCellSize = cellSize*2**nRefineZones

    halfTankL = tankLHW[0]/2
    xCellsbg = int(halfTankL/bgCellSize)
    zCellsbg = int(tankLHW[1]/bgCellSize)

    if (sim3D == 0):
        yCellsbg = 1
    else:
        yCellsbg = int(tankLHW[2]/bgCellSize)

    # Store object geometric center
    objGeoCtrX = xc - Xtn + transX
    objGeoCtrY = yc + transY
    objGeoCtrZ = zc + transZ

    # Wave zone refinement
    hWaveZone = hContr*waveHeight
    Zwn = zc - hWaveZone/2
    Zwp = zc + hWaveZone/2

    # Writing Wave Flume Setup
    with open(cF.bgMeshingLoc,'w') as fout:
        fout.write('//Background Dimensions and Mesh sizings:\n')
        fout.write('Xtn\t'+str(Xtn)+';\n')
        fout.write('Ytn\t'+str(Ytn)+';\n')   ###
        fout.write('Ztn\t'+str(Ztn)+';\n')
        fout.write('Xtm\t'+str(xc)+';\n')
        fout.write('Xtp\t'+str(Xtp)+';\n')
        fout.write('Ytp\t'+str(Ytp)+';\n')
        fout.write('Ztp\t'+str(Ztp)+';\n')
        fout.write('Zwn\t'+str(Zwn)+';\n')
        fout.write('Zwp\t'+str(Zwp)+';\n\n')

        fout.write('xCellsbg\t'+str(xCellsbg)+';\n')
        fout.write('yCellsbg\t'+str(yCellsbg)+';\n')
        fout.write('zCellsbg\t'+str(zCellsbg)+';\n\n')
        fout.write('locationInMesh\t('+str(xc)+' '+str(yc)+' '+str(zc)+');\n')

    ## Refinement Boxes
    # Refinement Boxes over object
    XtnRef = [Xfn - zoneWidthRatio*(Xfp-Xfn)]
    XtpRef = [Xfp + zoneWidthRatio*(Xfp-Xfn)]
    ZtnRef = [Zfn - zoneHeightRatio*(Zfp-Zfn)]
    ZtpRef = [Zfp + zoneHeightRatio*(Zfp-Zfn)]

    if (sim3D == 0):
        YtnRef = [Ytn]
        YtpRef = [Ytp]
    else:
        YtnRef = [Yfn - zoneWidthRatio*(Yfp-Yfn)]
        YtpRef = [Yfp + zoneWidthRatio*(Yfp-Yfn)]

    # Refinement Boxes over Wave Zone
    Xwn = xc - tankLHW[0]/2
    Xwp = xc + tankLHW[0]/2
    Ywn = yc - tankLHW[2]/2
    Ywp = yc + tankLHW[2]/2
    ZwnRef = [zc - hWaveZone/2]
    ZwpRef = [zc + hWaveZone/2]

    for i in range(1,nRefineZones+1):
        tempL = XtpRef[i-1]-XtnRef[i-1]
        tempW = YtpRef[i-1]-YtnRef[i-1]
        tempH = ZtpRef[i-1]-ZtnRef[i-1]
        tempwH = ZwpRef[i-1]-ZwnRef[i-1]

        XtnRef.append(XtnRef[i-1] - zoneWidthRatio*(tempL))
        XtpRef.append(XtpRef[i-1] + zoneWidthRatio*(tempL))
        ZtnRef.append(ZtnRef[i-1] - zoneHeightRatio*(tempH))
        ZtpRef.append(ZtpRef[i-1] + zoneHeightRatio*(tempH))
        ZwnRef.append(ZwnRef[i-1] - (tempwH)/2)

        if (i==nRefineZones):
            ZwpRef.append(Ztp)
        else:
            ZwpRef.append(ZwpRef[i-1] + (tempwH)/2)

        if (sim3D == 0):
            YtnRef.append(YtnRef[i-1])
            YtpRef.append(YtpRef[i-1])
        else:
            YtnRef.append(YtnRef[i-1] - zoneWidthRatio*(tempW))
            YtpRef.append(YtpRef[i-1] + zoneWidthRatio*(tempW))

        zone =  i

    # Background Mesh Refinement 
        refineLevel = 1
        with open(cF.bgRefineLoc,'w') as fout:
            if (nRefineZones > 0):
                for i in range(zone,0,-1):
                    fout.write('refinementBox'+str(zone-i)+'\n')
                    fout.write('{\n')
                    fout.write('\ttype\tsearchableBox;\n')
                    fout.write('\tmin\t('+str(XtnRef[i-1])+' '+str(YtnRef[i-1])+' '+str(ZtnRef[i-1])+');\n')
                    fout.write('\tmax\t('+str(XtpRef[i-1])+' '+str(YtpRef[i-1])+' '+str(ZtpRef[i-1])+');\n')
                    fout.write('}\n\n')

                    fout.write('refinementBox'+str(zone-i)+'_waveZone\n')
                    fout.write('{\n')
                    fout.write('\ttype\tsearchableBox;\n')
                    fout.write('\tmin\t('+str(Xwn)+' '+str(Ywn)+' '+str(ZwnRef[i-1])+');\n')
                    fout.write('\tmax\t('+str(Xwp)+' '+str(Ywp)+' '+str(ZwpRef[i-1])+');\n')
                    fout.write('}\n\n')

        with open(cF.bgRefineLevelLoc,'w') as fout:
            if (nRefineZones > 0):
                for i in range(zone,0,-1):
                    fout.write('refinementBox'+str(zone-i)+'\n')
                    fout.write('{\n')
                    fout.write('\tmode\tinside;\n')
                    fout.write('\tlevels\t((1e15 '+str(refineLevel*((zone-i)+1))+'));\n')
                    fout.write('}\n\n')

                    fout.write('refinementBox'+str(zone-i)+'_waveZone\n')
                    fout.write('{\n')
                    fout.write('\tmode\tinside;\n')
                    fout.write('\tlevels\t((1e15 '+str(refineLevel*((zone-i)+1))+'));\n')
                    fout.write('}\n\n')


