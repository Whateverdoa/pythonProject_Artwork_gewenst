# This is a sample Python script.
import shutil
import time
from datetime import date, timedelta
from pathlib import Path, PurePath
import pandas as pd
import re

wdir_JOBS = Path(r'G:\Prepress\ESKO\Jobs')
opvangmap=Path(r'G:\Prepress\ESKO\opvangmap')
opvangmap_logs=Path(r'G:\Prepress\ESKO\opvangmap_logs')

def timer_op_functie(functie):
    tic = time.perf_counter()
    functie
    toc = time.perf_counter()
    # print(f"{str(functie)} has been done in {toc - tic:0.8f} seconden")
    print(f"timer funct: done in {toc - tic:0.8f} seconden")
    return functie

def check_ordernummer_met_regex_in(jobfolder, ordernummer,regex_search=r"(\d{4})(\d{2})(\d{3})(.xml)"):
    # input is string otherwise int will be made string
    # regex_search = r"(\d{4})(\d{2})(\d{3})(.xml)"  # geeft 4 zoek groepen
    jobfolder = str(jobfolder)
    ordernummer=str(ordernummer)

    try:
        basisordernummer_check_regex = re.search(regex_search, ordernummer)
        output_regex_search_order = basisordernummer_check_regex.group()
        jaar = basisordernummer_check_regex.group(1)
        mapnr = basisordernummer_check_regex.group(2)

        if jaar + mapnr == jobfolder and output_regex_search_order != "no_match":
            # return 0,"check1", output_regex_search_order,jaar,mapnr
            "match"
        else:
            return "no_match"

        return output_regex_search_order

    except AttributeError:
        "AttributeError: no Match"


def get_xml_with_glob_from_(WDIR_JOBS, de_te_doorzoeken_folder):
    # todo maak xmls ook tijdgevoelig binnen 5 - 10 minuten

    # de jaar maand map waarin naar xmls gezocht kan worden
    folder = str(de_te_doorzoeken_folder)
    # bouw het pad naar de te doorzoeken folder
    folder_naar_xml = WDIR_JOBS.joinpath(folder)

    globxml = sorted(folder_naar_xml.rglob("*.xml"))

    tic = time.perf_counter()

    xml_named_files = [
        (padnaam.stem,
         check_ordernummer_met_regex_in(folder, padnaam.name),
         padnaam)
        for padnaam in globxml
        if check_ordernummer_met_regex_in(folder, padnaam.name) != None
    ]
    toc = time.perf_counter()
    print(f"built in timer : done in {toc - tic:0.8f} seconden")
    return xml_named_files


def gebruik_shutill_en_verplaats_file_van(original_pad, destination_pad):

    try:

        shutil.copyfile(original_pad, destination_pad)

    except OSError as e:
        print(e)

    return original_pad.stem, destination_pad.stem


try:
    from lxml import etree

    print("running with lxml.etree")
except ImportError:
    try:
        # Python 2.5
        import xml.etree.cElementTree as etree

        print("running with cElementTree on Python 2.5+")
    except ImportError:
        try:
            # Python 2.5
            import xml.etree.ElementTree as etree

            print("running with ElementTree on Python")
        except ImportError:
            try:
                # normal cElementTree install
                import cElementTree as etree

                print("running with cElementTree")
            except ImportError:
                try:
                    # normal ElementTree install
                    import elementtree.ElementTree as etree

                    print("running with ElementTree")
                except ImportError:
                    print("Failed to import ElementTree from any known place")


def destination_name_from_vila_(xml_file):
    """builds a new name for switch scan Hierarchy from
    # todo make tuple with origin and destination path for shutil"""
    vila_order = xml_file.stem
    tree = etree.parse(str(xml_file))
    root = tree.getroot()
    CustomerJobReference = root[1][3].text
    CustomerName = root[1][1].text
    print(xml_file)
    return f'{vila_order}_{CustomerJobReference}_{CustomerName}.xml'


onlineklanten = ['PRINT.COM', 'DRUKWERKDEAL.NL', 'HELLOPRINT B.V']


def xml_origin_and_new_(destination_wdir, from_xml_file):
    """builds a new name for switch scan Hierarchy from args
    # factory that builds a tuple with origin(xml file) and destination path for shutil

    Args:
        Path(destination_wdir
        Path.XML.is_file()

    Return:
        tuple(original xml path,
        destination xml path
        Customer name (for selecting xml files afterwards
        """

    vila_order = from_xml_file.stem
    tree = etree.parse(str(from_xml_file))
    root = tree.getroot()
    try:
        # todo make M number available

        CustomerJobReference = root[1][3].text
        CustomerName= root[1][1].text

        # print(from_xml_file)
        new_file_xml_name =f'{vila_order}_{CustomerJobReference}.xml'
        xml_destination = PurePath(destination_wdir,new_file_xml_name)
        xml_destination = Path(xml_destination)

        return (from_xml_file, xml_destination, CustomerName)
    except IndexError as IE:
        return (0,0,0)


def check_jobfolder_with_regex(jobfolder_to_check, jaar):
    # jaar optie is optioneel
    jaar = jaar
    jaar_check = r"(2022)(\d{2})"
    basischeck_verzamelmap = r"\d{6}"  # geeft 6 digits
    jobfolder_is_zes_getallen = len(jobfolder_to_check)
    try:
        jaar_test = re.search(jaar_check, jobfolder_to_check)
        if jaar_test.group(1) == str(jaar) and jobfolder_is_zes_getallen == 6:

            basismap_check_regex = re.search(basischeck_verzamelmap, jobfolder_to_check)
            output_regex_search = basismap_check_regex.group()

            print(f'{output_regex_search = }')
            # return output_regex_search
            return True
        else:
            print(f"vergelijk {jaar_test.group(1)}  met {jaar}")
            print(f'aantal posities (6) van folder = {jobfolder_is_zes_getallen}')
            return False

    except AttributeError:
        print("AttributeError: no Match")
        return False


def find_(hoofd_folder, tijdsduur_in_dagen):
    # todo hoe neem ik het weekeinde mee zonder die 48 uur te gebruiken
    # todo hoe jaar egt gebruiken in de regex rond de jaarwisseling
    past_time = date.today() - timedelta(days=tijdsduur_in_dagen)

    folders = []
    for path in Path(hoofd_folder).iterdir():
        timestamp = date.fromtimestamp(path.stat().st_mtime)
        # print(f'{timestamp > past_time = }')

        if path.is_dir() and timestamp > past_time and check_jobfolder_with_regex(path.name,2022):
            # print(f'folder: {path}')
            folders.append((path.name,0,0))
            print(f"{path.name =}")
            # print(path.is_dir())
            # print(WDIR_Job.joinpath(path.name))
            # nieuwdwir = WDIR_Job.joinpath(hoofd_folder)
            # order_nummerpad = nieuwdwir.joinpath(path.name)



    return sorted(folders)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    tic = time.perf_counter()

    # JOB_folders_to_check = [(202229, 0, 0), (202230, 0, 0), (202231, 0, 0),(202232, 0, 0), (202233, 0, 0)]
    # JOB_folders_to_check = [(202223, 0, 0)]
    JOB_folders_to_check = find_(wdir_JOBS, tijdsduur_in_dagen=3)


    xmls_relevante_mappen = [get_xml_with_glob_from_(wdir_JOBS, map[0]) for map
                             in JOB_folders_to_check]

    xml_flat_list_voor_destination_name = timer_op_functie(
        [item for sublist in xmls_relevante_mappen for item in sublist])

    paths_to_xml_files = [xml[2] for xml in xml_flat_list_voor_destination_name]

    xml_files_ONLINE_KLANTEN = [xml_origin_and_new_(opvangmap, xml_pad) for xml_pad in paths_to_xml_files
                                if xml_origin_and_new_(opvangmap, xml_pad)[2] in onlineklanten]

    dataframe_printdotcom = pd.DataFrame(xml_files_ONLINE_KLANTEN,
                                         columns=['original_xml', 'destination_xml', 'customername'])

    namen_voor_shutil = [xml_origin_and_new_(opvangmap, Print_com_xml[0])
                         for Print_com_xml in xml_files_ONLINE_KLANTEN]

    xml_naar_opvangmap = [gebruik_shutill_en_verplaats_file_van(xml[0], xml[1])
                          for xml in namen_voor_shutil]

    toc = time.perf_counter()
    # print(f"{str(functie)} has been done in {toc - tic:0.8f} seconden")
    print(f"totaal tijd timer: done in {toc - tic:0.2f} seconden voor mappen {JOB_folders_to_check}")
    logtijd = f"totaal tijd timer: done in {toc - tic:0.2f} seconden voor mappen {JOB_folders_to_check}"
    time.sleep(10)
    print("task_schedule regulated")

    import logging


    #Creating and Configuring Logger

    # Log_Format = "%(levelname)s %(asctime)s - %(message)s"
    #
    # logging.basicConfig(filename = "logfile.log",
    #                     filemode = "w",
    #                     format = Log_Format,
    #                     level = logging.ERROR)
    #
    # logger = logging.getLogger()
    #
    # #Testing our Logger
    #
    # logger.error(logtijd)
    # logger.log(msg=logtijd,)
    # #Opening a file
    # file1 = open('log.log', 'a')
    #
    # # Writing a string to file
    # file1.write(logtijd)