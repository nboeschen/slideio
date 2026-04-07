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

def safe_remove(page, element):
    # first remove all elements that are children of the element in the current page
    for w in page.xpath(f".//*[@parent='{element.attrib['id']}']"):
        if w.getparent().tag == "object":
            # special case: some images use an extra layer of tag "object" ...
            tmp = w.getparent().getparent()
            tmp.remove(w.getparent())
        else:
            w.getparent().remove(w)
    # remove the element
    element.getparent().remove(element)


def expand(tree):
    """
    Handle "appear" and "hide" attributes
    """
    added_pages = 0
    skipped_pages = 0

    # Iterate all "diagram" types in xml tree. These are all pages in drawio, and will be the slides of the pdf.
    for page_index, orig_page in enumerate(tree.xpath(".//diagram")):

        # skip pages containing any object with the "skip_page" property
        if len(orig_page.xpath(".//*[@skip_page]")) != 0:
            skipped_pages += 1
            orig_page.getparent().remove(orig_page)
            continue

        # find maximum "appear"/"hide" value:
        max_expand = 0
        for z in orig_page.xpath(".//*[@appear|@hide]"):
            max_expand = max(max_expand, int(z.get("appear",0)))
            max_expand = max(max_expand, int(z.get("hide",0)))

        added_pages += max_expand

        # add page number to "page_number" elements
        for z in orig_page.xpath(".//*[@slide_number]"):
            z.attrib["label"] = f"{page_index-skipped_pages+1}"

        # add a duplicate of the full diagram max_expand+1 times
        # the first one added will be the last one in the final file
        parent = orig_page.getparent()
        for i in range(max_expand,-1,-1):
            # i is the current frame of the slide
            copied_page = deepcopy(orig_page)
            # change diagram id
            copied_page.attrib["id"] = copied_page.attrib["id"] + "X"*i
            # remove "appear" elements
            for z in copied_page.xpath(".//*[@appear]"):
                if i < int(z.attrib["appear"]):
                    safe_remove(copied_page,z)
            # remove "hide" elements
            for z in copied_page.xpath(".//*[@hide]"):
                if i >= int(z.attrib["hide"]):
                    safe_remove(copied_page,z)
            parent.insert(parent.index(orig_page)+1, copied_page)

        # remove original page
        parent.remove(orig_page)


    # update number of pages
    tree.attrib["pages"] = str(int(tree.attrib["pages"]) + added_pages - skipped_pages)


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

