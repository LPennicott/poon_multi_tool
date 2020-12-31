import csv
import io
import re
import xml.etree.ElementTree as ET

from django.http import HttpResponse


def _process_file(csv_data, xml_data):
        
    for fieldname in csv_data.fieldnames:
        if result := re.match('hawb(s*)', fieldname, re.IGNORECASE):
            name = result.group(0)

            # collect hawbs to compare against hawb nodes in xml
            # file
            hawbs = {str(row[name]) for row in csv_data}
            new_hawbs = []
            for hawb in hawbs:
                while len(hawb) < 11:
                    hawb = '0' + hawb
                new_hawbs.append(hawb)

    parsed_xml = ET.parse(xml_data)
    parsed_xml_root = parsed_xml.getroot()
    parsed_list = parsed_xml_root.findall("ENTRY")

    for item in parsed_list:
        if item.find("MANIFEST").find(
                "HOUSE").text not in new_hawbs:
            parsed_xml_root.remove(item)

    return parsed_xml.write('new_file.xml', xml_declaration=True)