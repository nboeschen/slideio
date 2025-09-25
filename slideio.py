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

    # find all nodes with "appear" in attrib, but iterate over the ancestors of tag "diagram"
    for x in tree.xpath(".//*[@appear]/ancestor::diagram"):
        # duplicate the full diagram
        parent = x.getparent()
        y = deepcopy(x)
        # change diagram id
        y.attrib["id"] = y.attrib["id"] + "xxx"
        # remove appear elements in the original diagram
        for z in x.xpath(".//*[@appear]"):
            z.getparent().remove(z)
        parent.insert(parent.index(x)+1, y)

    # update number of pages
    tree.attrib["pages"] = str(int(tree.attrib["pages"])+1)

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
