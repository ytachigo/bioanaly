def get_pdbtraj(): # Get a PDB trajectory data set
    atomnum_list = []
    atomname_list = []
    resnum_list = []
    resname_list = []
    xcoord_list = []
    ycoord_list = []
    xcoord_list = []
    atomnum = []
    atomname = []
    resnum = []
    resname = []
    xcoord = []
    ycoord = []
    zcoord = []

    filename = input('Filename(pdb): ')
    open_file = open(filename, 'r')

    for kline in open_file.readlines():
        if kline[0:4] != 'ATOM' and kline[0:6] != 'HETATOM' and \
        kline[0:6] != 'ENDMDL':
            pass
        elif kline[0:4] == 'ATOM' or kline[0:6] == 'HETATOM':
                atomnum.append(int(kline[7:11]))
                atomname.append(str(kline[13:16].strip()))
                resnum.append(int(kline[23:26]))
                resname.append(str(kline[16:20].strip()))
                xcoord.append(float(kline[31:38]))
                ycoord.append(float(kline[39:46]))
                zcoord.append(float(kline[47:54]))
        elif kline[0:6] == 'ENDMDL':
            atomnum_list.append(atomnum)
            atomname_list.append(atomname)
            resnum_list.append(resnum)
            resname_list.append(resname)
            xcoord_list.append(xcoord)
            ycoord_list.append(ycoord)
            zcoord_list.append(zcoord)
            atomnum = []
            atomname = []
            resnum = []
            resname = []
            xcoord = []
            ycoord = []
            zcoord = []
    open_file.close()
    return atomnum_list, atomname_list, resnum_list,
           resname_list, xcoord_list, ycoord_list, zcoord_list

def get_inpcrd(): # Get coordinates from a AMBER input file.
    xcoord_list = []
    ycoord_list = []
    zcoord_list = []

    filename = input('Filename(inpcrd): ')
    open_file = open(filename, 'r')

    for kline in open_file.readlines()[2:]:
        xcoord_list.append(str(kline[0:12].strip()))
        ycoord_list.append(str(kline[12:24].strip()))
        zcoord_list.append(str(kline[24:36].strip()))
        xcoord_list.append(str(kline[36:48].strip()))
        ycoord_list.append(str(kline[48:60].strip()))
        zcoord_list.append(str(kline[60:72].strip()))
    return xcoord_list, ycoord_list, zcoord_list
