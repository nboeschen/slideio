import argparse
from lxml import etree
from copy import deepcopy

"""
Slideio:

Create slides in Drawio!
Slides are pages, animations are handled with the "appear" attribute.
This script handles editing the drawio xml file and expands each page with appear elements.
Use drawio to create the pdfs itself:

Example: 
python slideio.py slides.drawio tmp.drawio
drawio --export -a tmp.drawio

"""


def open_diagram(filepath):
    with open(filepath,"r") as file:
        tree = etree.fromstring(file.read())
    return tree

def save_diagram(tree, outfile):
    with open(outfile,"w") as file:
        xmlstring = etree.tostring(tree, encoding="unicode", pretty_print=True)
        file.write(xmlstring)

def expand(tree):
    """
    Handle "appear" and "hide" attributes
    """
    added_pages = 0

    # Iterate all "diagram" types in xml tree. These are all pages in drawio, and will be the slides of the pdf.
    for page_index, x in enumerate(tree.xpath(".//diagram")):
        # find maximum "appear"/"hide" value:
        max_expand = 0
        for z in x.xpath(".//*[@appear|@hide]"):
            max_expand = max(max_expand, int(z.get("appear",0)))
            max_expand = max(max_expand, int(z.get("hide",0)))

        added_pages += max_expand

        # add page number to "page_number" elements
        for z in x.xpath(".//*[@slide_number]"):
            z.attrib["label"] = f"{page_index+1}"

        # add a duplicate of the full diagram max_expand times
        # the first one added will be the last one in the final file
        parent = x.getparent()
        for i in range(max_expand,0,-1):
            # i is the current frame of the slide
            y = deepcopy(x)
            # change diagram id
            y.attrib["id"] = y.attrib["id"] + "X"*i
            # remove "appear" elements
            for z in y.xpath(".//*[@appear]"):
                if i < int(z.attrib["appear"]):
                    z.getparent().remove(z)
            # remove "hide" elements
            for z in y.xpath(".//*[@hide]"):
                if i >= int(z.attrib["hide"]):
                    z.getparent().remove(z)
            parent.insert(parent.index(x)+1, y)

        # remove "appear" elements from original page
        for z in x.xpath(".//*[@appear]"):
            if int(z.attrib["appear"]) > 0:
                z.getparent().remove(z)

    # update number of pages
    tree.attrib["pages"] = str(int(tree.attrib["pages"]) + added_pages)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                    prog='slideio',
                    description='Drawio 2 pdf slide helper')
    parser.add_argument('inpath')
    parser.add_argument('outpath')

    args = parser.parse_args()

    tree = open_diagram(args.inpath)
    expand(tree)
    save_diagram(tree, args.outpath)

