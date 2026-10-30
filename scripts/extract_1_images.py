from pptx import Presentation
import os

prs = Presentation(r"presentations\1.pptx")
out_dir = r"pic\extracted_from_1"
os.makedirs(out_dir, exist_ok=True)

img_idx = 0
for i, slide in enumerate(prs.slides):
    for s in slide.shapes:
        # Check direct picture
        if s.shape_type == 13: # Picture
            img = s.image
            ext = img.ext
            path = os.path.join(out_dir, f"slide_{i+1}_img_{img_idx}.{ext}")
            with open(path, "wb") as f:
                f.write(img.blob)
            print(f"Slide {i+1}: Picture saved to {path}")
            img_idx += 1
        # Check shapes in group
        if s.shape_type == 6:
            for sub in s.shapes:
                if hasattr(sub, 'fill') and sub.fill.type == 6: # Picture fill
                    # let's see if we can get blip
                    sp_elem = sub._element
                    blip_elems = sp_elem.xpath('.//a:blip')
                    for b in blip_elems:
                        rId = b.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
                        if rId:
                            rel = slide.part.rels[rId]
                            img_part = rel.target_part
                            ext = img_part.content_type.split('/')[-1]
                            path = os.path.join(out_dir, f"slide_{i+1}_subimg_{img_idx}.{ext}")
                            with open(path, "wb") as f:
                                f.write(img_part.blob)
                            print(f"Slide {i+1}: Group picture fill saved to {path} ({img_part.content_type})")
                            img_idx += 1
print("Done extracting pictures from 1.pptx")
