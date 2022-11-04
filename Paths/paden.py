# three folder paths based on time and name of folder
from pathlib import Path

pad_naar_collectie= Path(r'C:\Users\Dhr.Ten Hoonte\PycharmProjects\pythonProject_Artwork_gewenst\
    testingground\switch_itemnumber_collector_folder')
klantnamen = ["HELLOPRINT.B.V", "DRUKWERKDEAL.NL", "PRINT.COM"]
PRODUCTS_path = r'PycharmProjects\pythonProject_Artwork_gewenst\testingground\Products'
wdir = Path.cwd()
itemnum_collection = list(pad_naar_collectie.rglob('*.pdf'))

# klantnamen = ["HELLOPRINT.B.V", "DRUKWERKDEAL.NL", "PRINT.COM"]
# klantnaam_met_eerste_letter = [(name[0], name) for name in klantnamen]
# hp_id = "806321"
# dwd_id = "569621"
# pdc_id = "935321"
# testingground = r'PycharmProjects\pythonProject_Artwork_gewenst\testingground\Products'
# wdir = Path.cwd()
# print(wdir.home().joinpath(testingground))
# print(wdir.absolute())

# pad_naar_klantNaam_is = Path(...)


def pad_naar_item_nummer_folder_maker(voor_itemnummer_uit_lijst):
    """Builds a path filename from the vila item number for the
    Helloprint, Drukwerkdeal and print.com reseller clients.
    # hp_id = "806321"
    # dwd_id = "569621"
    # pdc_id = "935321
    """
    voor_itemnummer_uit_lijst = str(voor_itemnummer_uit_lijst)
    itemnummer_pdf = voor_itemnummer_uit_lijst + ".pdf"

    def foldername_based_on_itemnummer(itemnummer):
        itemnummer = str(itemnummer)
        folderbase = itemnummer[4:9]
        foldername = folderbase + "000-" + folderbase + "999"
        return foldername

    def klantnummer_uit(itemnummer):
        itemnummer = str(itemnummer)
        klantnummer = itemnummer[0:6]
        return klantnummer

    klant_naam_paden = [(wdir.home().joinpath(PRODUCTS_path, name[0], name)) for name in klantnamen]

    helloprint_base_path = klant_naam_paden[0]
    drukwerkdeal_base_path = klant_naam_paden[1]
    print_dot_com_base_path = klant_naam_paden[2]

    foldername = foldername_based_on_itemnummer(voor_itemnummer_uit_lijst)

    match klantnummer_uit(voor_itemnummer_uit_lijst):
        case "806321":
            return Path(helloprint_base_path.joinpath(foldername, voor_itemnummer_uit_lijst, itemnummer_pdf))

        case "569621":
            return Path(drukwerkdeal_base_path.joinpath(foldername, voor_itemnummer_uit_lijst, itemnummer_pdf))

        case "935321":
            return Path(print_dot_com_base_path.joinpath(foldername, voor_itemnummer_uit_lijst, itemnummer_pdf))

    # pnt = pad_naar_item_nummer_folder_maker('56962100000')
    # pnt2 = pad_naar_item_nummer_folder_maker(8063210000)
    # pnt3 = pad_naar_item_nummer_folder_maker(93532100000)
    # print(pnt)
    # print(pnt.is_file())
    # print(pnt2)
    # print(pnt3)


# klant_naam_paden = [(wdir.home().joinpath(testingground, name[0], name)) for name in klantnamen]


def collect_itemnumber_path_from_folder(itemnumber):
    """try to collect from a rgob(*.pdf) folder a filepath"""

    pdfpad = [pad for pad in itemnum_collection if pad.stem == str(itemnumber) ]
    return pdfpad
