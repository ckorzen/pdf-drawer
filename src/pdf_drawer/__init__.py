from typing import List, Tuple, Union

import fitz

class PdfDrawer:
    """
    A class that can be used to add simple drawings (i.e., rectangles, lines and text) to existing
    PDF files.
    """

    def __init__(self, pdf_path: str = None, pdf_mem: Union[bytes, bytearray] = None):
        """
        Creates a new instance of this class for drawing into the given PDF file.

        Args:
            pdf_path: str
                The path to the PDF file to which drawings should be added.
            pdf_mem: bytes or bytearray
                The PDF file to which drawings should be added, given as an in-memory
                representation.
        """
        if pdf_mem is not None:
            self.pdf = fitz.open("pdf", pdf_mem)
        else:
            self.pdf = fitz.open(pdf_path)

    def draw_rectangle(self, page_num: int, x0: float, y0: float, x1: float, y1: float,
            border_width: float = 1.0, border_color: Tuple[float, float, float] = (.0, .0, .0),
            filling_color: Tuple[float, float, float] = None, border_opacity: float = 1.0,
            filling_opacity: float = 1.0):
        """
        Draws a rectangle into the PDF.

        Args:
            page_num: int
                The 1-based page number of the page to which the rectangle should be added.
            x0: float
                The x-coordinate of the rectangle's lower left corner, relative to the upper left
                corner of the page.
            y0: float
                The y-coordinate of the rectangle's lower left corner, relative to the upper left
                corner of the page.
            x1: float
                The x-coordinate of the rectangle's upper right corner, relative to the upper left
                corner of the page.
            y1: float
                The y-coordinate of the rectangle's upper right corner, relative to the upper left
                corner of the page.
            border_width: float
                The border width.
            border_color: Tuple[float, float, float]
                The border color. The tuple is interpreted as an RGB color value. The values are
                floating values between 0 and 1, each representing a specific RGB color component.
            filling_color: Tuple[float, float, float]
                The filling color. The tuple is interpreted as an RGB color value. The values are
                floating values between 0 and 1, each representing a specific RGB color component.
            border_opacity: float
                The transparency of the border, given as a float between 0 (transparent) and 1
                (intransparent).
            filling_opacity: float
                The transparency of the filling, given as a float between 0 (transparent) and 1
                (intransparent).
        """
        # Load the page.
        page = self.pdf[page_num - 1]
        # Create the rectangle.
        shape = page.new_shape()
        shape.draw_rect(fitz.Rect(x0, y0, x1, y1))
        # Draw the rectangle.
        shape.finish(width=border_width, color=border_color, fill=filling_color,
            stroke_opacity=border_opacity, fill_opacity=filling_opacity)
        shape.commit()

    def draw_line(self, page_num: int, x0: float, y0: float, x1: float, y1: float,
            line_width: float = 1.0, color: Tuple[float, float, float] = (.0, .0, .0),
            opacity: float = 1.0):
        """
        Draws a line into the PDF.

        Args:
            page_num: int
                The 1-based page number of the page to which the line should be added.
            x0: float
                The x-coordinate of the first endpoint of the line, relative to the upper left
                corner of the page.
            y0: float
                The y-coordinate of the first endpoint of the line, relative to the upper left
                corner of the page.
            x1: float
                The x-coordinate of the second endpoint of the line, relative to the upper left
                corner of the page.
            y1: float
                The y-coordinate of the second endpoint of the line, relative to the upper left
                corner of the page.
            line_width: float
                The line width.
            color: Tuple[float, float, float]
                The line color. The tuple is interpreted as an RGB color value. The values are
                floating values between 0 and 1, each representing a specific RGB color component.
            opacity: float
                The transparency of the border, given as a float between 0 (transparent) and 1
                (intransparent).
        """
        # Load the page.
        page = self.pdf[page_num - 1]
        # Create the line.
        shape = page.new_shape()
        shape.draw_line(fitz.Point(x0, y0), fitz.Point(x1, y1))
        # Draw the line.
        shape.finish(width=line_width, color=color, stroke_opacity=opacity)
        shape.commit()

    def draw_text(self, text: str, page_num: int, x: float, y: float, font_name: str = "helv",
            font_size: float = 11, border_color: Tuple[float, float, float] = (.0, .0, .0),
            filling_color: Tuple[float, float, float] = None, border_opacity: float = 1.0,
            filling_opacity: float = 1.0):
        """
        Draws the given text into the PDF.

        Args:
            text: str:
                The text to draw.
            page_num: int
                The 1-based page number of the page to which the text should be added.
            x: float
                The x-coordinate of the lower left position of the text to draw.
            y: float
                The y-coordinate of the lower left position of the text to draw.
            font_name: str
                The font to use on drawing the text. Possible values are: "helv", "cour", "tiro",
                "zadb" and "symb".
            font_size: float
                The font size.
            border_color: Tuple[float, float, float]
                The border color. The tuple is interpreted as an RGB color value. The values are
                floating values between 0 and 1, each representing a specific RGB color component.
            filling_color: Tuple[float, float, float]
                The filling color. The tuple is interpreted as an RGB color value. The values are
                floating values between 0 and 1, each representing a specific RGB color component.
            border_opacity: float
                The transparency of the border, given as a float between 0 (transparent) and 1
                (intransparent).
            filling_opacity: float
                The transparency of the filling, given as a float between 0 (transparent) and 1
                (intransparent).
        """
        # Load the page.
        page = self.pdf[page_num - 1]
        # Draw the text.
        shape = page.new_shape()
        shape.insert_text(fitz.Point(x, y), text, fontname=font_name,
            fontsize=font_size, color=border_color, fill=filling_color,
            stroke_opacity=border_opacity, fill_opacity=filling_opacity)
        shape.commit()

    def crop_page(self, page_num: int, x0: float, y0: float, x1: float, y1: float):
        """
        Crops the given page to the box defined by the given coordinates.
        """
        page = self.pdf[page_num - 1]
        print("Crop page")
        print("rect before:", page.rect)
        print("crop before:", page.cropbox)
        rect = fitz.Rect(
          max(0, x0),
          max(0, y0),
          min(page.rect.width, x1),
          min(page.rect.height, y1)
        )
        print("croppping: ", rect)
        page.set_cropbox(fitz.Rect(
          max(0, x0),
          max(0, y0),
          min(page.rect.width, x1),
          min(page.rect.height, y1)
        ))
        print("rect after:", page.rect)
        print("crop after:", page.cropbox)


    def select_pages(self, page_nums: List[int]):
        """
        Reduces the PDF to the given pages.
        """
        self.pdf.select([x - 1 for x in page_nums])

    def save(self, output_path: str):
        """
        Writes the PDF, including the added drawings, to the given file path.

        output_path: str
            The path to the file to which the PDF should be written.
        """
        self.pdf.save(output_path)