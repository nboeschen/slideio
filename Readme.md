# Slideio
Create slides in Drawio!
Slides are pages, animations are handled with the "appear"/"hide" attributes.
This script handles editing the drawio xml file and expands each page with "appear"/"hide" elements.
Use drawio to create the pdfs itself:

## Example:

- Create a drawio file with one page per slide
- For each element that should appear / be hidden, click "Edit Data"
- appear: Add the property "appear" and the value on which frame it should appear ("1" means it appears one "click" after the initial slide)
- hide: Add the property "hide" and the value on which frame it should be removed ("1" means it is removed one "click" after the initial slide)

```bash
python slideio.py slides.drawio tmp.drawio
drawio --export -a tmp.drawio
```