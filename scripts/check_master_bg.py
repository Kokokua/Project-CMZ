from pptx import Presentation

prs = Presentation(r"presentations\1.pptx")
slide2 = prs.slides[1]
print("Slide 2 background:", slide2.background._element.xml[:500])
# Check slide master background
master = prs.slide_masters[0]
print("Master background:", master.background._element.xml[:500])
