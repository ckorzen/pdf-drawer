import pdf_drawer
import os

dir = os.path.dirname(__file__)

if __name__ == "__main__":
    pdf_d = pdf_drawer.PdfDrawer(os.path.join(dir, "../../example-heading-sub-super-scripts-hyphenated-word.pdf"))
    pdf_d.crop_page(1, 0, 0, 500, 200)
    pdf_d.select_pages([1])
    pdf_d.save("xxx.pdf")