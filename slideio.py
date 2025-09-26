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

def expand_appear(filepath, outfile):

    with open(filepath,"r") as file:
        tree = etree.fromstring(file.read())

    added_pages = 0

    # find all nodes with "appear" in attrib, but iterate over their ancestors of tag "diagram"
    for x in tree.xpath(".//*[@appear]/ancestor::diagram"):
        # find maximum appear value:
        max_appear = 0
        for z in x.xpath(".//*[@appear]"):
            max_appear = max(max_appear, int(z.attrib["appear"]))

        added_pages += max_appear

        # add a duplicate of the full diagram max_appear times
        # the first one added will be the last one in the final file
        parent = x.getparent()
        for i in range(max_appear,0,-1):
            y = deepcopy(x)
            # change diagram id
            y.attrib["id"] = y.attrib["id"] + "X"*i
            # remove appear elements
            for z in y.xpath(".//*[@appear]"):
                if int(z.attrib["appear"]) > i:
                    z.getparent().remove(z)
            parent.insert(parent.index(x)+1, y)
        # remove from original page
        for z in x.xpath(".//*[@appear]"):
            if int(z.attrib["appear"]) > 0:
                z.getparent().remove(z)

    # update number of pages
    tree.attrib["pages"] = str(int(tree.attrib["pages"]) + added_pages)

    with open(outfile,"w") as file:
        xmlstring = etree.tostring(tree, encoding="unicode", pretty_print=True)
        file.write(xmlstring)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                    prog='slideio',
                    description='Drawio 2 pdf slide helper')
    parser.add_argument('inpath')
    parser.add_argument('outpath')

    args = parser.parse_args()

    expand_appear(args.inpath, args.outpath)
