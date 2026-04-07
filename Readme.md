# Slideio
Create slides in Drawio!
Slides are pages, animations are handled with the "appear"/"hide" attributes.
This script handles editing the drawio xml file and expands each page with "appear"/"hide" elements.
Use drawio to create the pdfs itself.

## Features
The following feature are supported and can be enabled by adding the respective property of objects:
- `appear`: Add this property and set the value on which frame the object should appear ("1" means it appears one "click" after the initial slide).
- `hide`: Add this property and set the value on which frame it should be removed ("1" means it is removed one "click" after the initial slide).
- `slide_number`: Add this property (value does not matter) to a text label, to automatically replace the text with the slide number.
- `skip_page`: Add this property (value does not matter) to at least one object to remove the containing page completely (useful for template pages).

## Example:
- Create a drawio file with one page per slide
- For each element that should appear / be hidden, click "Edit Data" and update the properties (see above)
- Then create the updated/expanded drawio file and let drawio export the pages as pdfs:
```bash
python slideio.py slides.drawio tmp.drawio
drawio --export -a tmp.drawio
```
- An example drawio file and build script can be found in the `example` folder