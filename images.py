import xml.etree.ElementTree as xmltree
import pygame

def load_images():

    class Images:
        pass

    with open("assets/sheet.xml", "rt") as f:
        imageData = f.read()
    
    atlas = xmltree.fromstring(imageData)

    sheet = pygame.image.load("assets/sheet.png").convert_alpha()

    images = Images()

    for child in atlas:
        if child.tag == "SubTexture" :
            x = int(child.attrib["x"])
            y = int(child.attrib["y"])            
            w = int(child.attrib["width"])
            h = int(child.attrib["height"])
            # Image data has origin at top, left 
            image = pygame.Surface((w,h), pygame.SRCALPHA).convert_alpha()
            image.blit(sheet, (0, 0), (x, y, w, h))
            setattr(images, child.attrib["name"].replace('.png', ''), image)

    return images