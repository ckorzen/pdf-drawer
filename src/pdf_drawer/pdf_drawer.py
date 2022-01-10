from typing import List, Tuple

import argparse
import fitz
import logging

# ==================================================================================================

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)

# The default border width.
DEFAULT_BORDER_WIDTH = 1.0
# The default border color.
DEFAULT_BORDER_COLOR = (.0, .0, .0)
# The default filling color.
DEFAULT_FILLING_COLOR = None
# The default border opacity.
DEFAULT_BORDER_OPACITY = 1.0
# The default filling opacity.
DEFAULT_FILLING_OPACITY = 1.0
# The default font name.
DEFAULT_FONT_NAME = "helv"
# The default font size.
DEFAULT_FONT_SIZE = 11

# ==================================================================================================

class PdfDrawer:
    """
    This class can be used to add simple drawings (i.e., rectangles, lines and text) to existing
    PDF files.
    """

    def __init__(self, pdf_path: str = None, pdf_bytes: str = None):
        """
        Creates a new instance of this class for drawing into the given PDF file.

        Args:
            pdf_path: str
                The path to the PDF file to which drawings should be added.
            pdf_bytes: str
                The PDF file to which drawings should be added, given as a binary string.
        """
        if pdf_path is not None:
            self.pdf = fitz.open(pdf_path)
        else:
            self.pdf = fitz.open("pdf", pdf_bytes)

    def process_instruction_file(self, file_path: str):
        """
        This method reads the given instruction file, parses and processes the contained drawing
        instructions.

        Args:
            file_path: str
                The path to the instruction file to process.
        """
        # Read the instruction file line by line.
        with open(file_path, "r") as stream:
            for line in stream:
                line = line.strip()

                # Ignore empty lines.
                if len(line) == 0:
                    continue

                # Ignore comment lines.
                first_char = line[0].upper()
                if line[0] == "%" or line[0] == "#":
                    continue

                # Split the line into its fields.
                fields = line.split("\t")

                # The first character specifies the type of the drawing instruction.
                if first_char == "R":
                    # Draw a rectangle.
                    self.draw_rectangle(
                        page_num=self.parse_int(fields, 1),
                        x0=self.parse_float(fields, 2),
                        y0=self.parse_float(fields, 3),
                        x1=self.parse_float(fields, 4),
                        y1=self.parse_float(fields, 5),
                        border_width=self.parse_float(fields, 6, DEFAULT_BORDER_WIDTH),
                        border_color=self.parse_color(fields, 7, DEFAULT_BORDER_COLOR),
                        border_opacity=self.parse_float(fields, 8, DEFAULT_BORDER_OPACITY),
                        filling_color=self.parse_color(fields, 9, DEFAULT_FILLING_COLOR),
                        filling_opacity=self.parse_float(fields, 10, DEFAULT_FILLING_OPACITY)
                    )
                elif first_char == "L":
                    # Draw a line.
                    self.draw_line(
                        page_num=self.parse_int(fields, 1),
                        x0=self.parse_float(fields, 2),
                        y0=self.parse_float(fields, 3),
                        x1=self.parse_float(fields, 4),
                        y1=self.parse_float(fields, 5),
                        width=self.parse_float(fields, 6, DEFAULT_BORDER_WIDTH),
                        color=self.parse_color(fields, 7, DEFAULT_BORDER_COLOR),
                        opacity=self.parse_float(fields, 8, DEFAULT_BORDER_OPACITY)
                    )
                elif first_char == "T":
                    # Draw text.
                    self.draw_text(
                        page_num=self.parse_int(fields, 1),
                        x=self.parse_float(fields, 2),
                        y=self.parse_float(fields, 3),
                        text=self.parse_string(fields, 4),
                        font_name=self.parse_string(fields, 5, DEFAULT_FONT_NAME),
                        font_size=self.parse_float(fields, 6, DEFAULT_FONT_SIZE),
                        border_width=self.parse_float(fields, 7, DEFAULT_BORDER_WIDTH),
                        border_color=self.parse_color(fields, 8, DEFAULT_BORDER_COLOR),
                        border_opacity=self.parse_float(fields, 9, DEFAULT_BORDER_OPACITY),
                        filling_color=self.parse_color(fields, 10, DEFAULT_FILLING_COLOR),
                        filling_opacity=self.parse_float(fields, 11, DEFAULT_FILLING_OPACITY)
                    )
                else:
                    LOG.warn(f"Unknown drawing instruction '{line}'")

    # ==============================================================================================

    def draw_rectangle(self, page_num: int, x0: float, y0: float, x1: float, y1: float,
                       border_width: float = DEFAULT_BORDER_WIDTH,
                       border_color: Tuple[float, float, float] = DEFAULT_BORDER_COLOR,
                       filling_color: Tuple[float, float, float] = DEFAULT_FILLING_COLOR,
                       border_opacity: float = DEFAULT_BORDER_OPACITY,
                       filling_opacity: float = DEFAULT_FILLING_OPACITY):
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
        shape.draw_rect(fitz.Rect(x0, y1, x1, y0))
        # shape.draw_rect(fitz.Rect(x0, y0, x1, y1))
        # Draw the rectangle.
        shape.finish(
            width=border_width,
            color=border_color,
            fill=filling_color,
            stroke_opacity=border_opacity,
            fill_opacity=filling_opacity
        )
        shape.commit()

    def draw_line(self, page_num: int, x0: float, y0: float, x1: float, y1: float,
                  width: float = DEFAULT_BORDER_WIDTH,
                  color: Tuple[float, float, float] = DEFAULT_BORDER_COLOR,
                  opacity: float = DEFAULT_BORDER_OPACITY):
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
            width: float
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
        shape.finish(width=width, color=color, stroke_opacity=opacity)
        shape.commit()

    def draw_text(self, text: str, page_num: int, x: float, y: float,
                  font_name: str = DEFAULT_FONT_NAME,
                  font_size: float = DEFAULT_FONT_SIZE,
                  border_width: float = DEFAULT_BORDER_WIDTH,
                  border_color: Tuple[float, float, float] = DEFAULT_BORDER_COLOR,
                  filling_color: Tuple[float, float, float] = DEFAULT_FILLING_COLOR,
                  border_opacity: float = DEFAULT_BORDER_OPACITY,
                  filling_opacity: float = DEFAULT_FILLING_COLOR):
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
        # Draw the text.
        shape = page.new_shape()
        shape.insert_text(
            fitz.Point(x, y),
            text,
            fontname=font_name,
            fontsize=font_size,
            border_width=border_width,
            color=border_color,
            fill=filling_color,
            stroke_opacity=border_opacity,
            fill_opacity=filling_opacity
        )
        shape.commit()


    def save(self, output_path: str):
        """
        Writes the PDF, including the added drawings, to the given file path.

        output_path: str
            The path to the file to which the PDF should be written.
        """
        self.pdf.save(output_path)

    # ==============================================================================================

    def parse_int(self, args: List[str], i: int, default_int: int = 0) -> int:
        """
        This method parses the i-th element in the given list of strings to an integer value.
        Returns the given default integer if there is no such element or if the element is empty.
        Throws an exception if the i-th element doesn't represent an integer.

        Args:
            args: List[str]
                The list of strings.
            i: int
                The index of the element to parse.
            default_int: int
                The default value to return if no such element exists or if the element is empty.
        Returns:
            int:
                The i-th element of the array as an integer.
        """
        if not args:
            return default_int
        if i >= len(args):
            return default_int
        if not args[i]:
            return default_int

        return int(args[i])


    def parse_float(self, args: List[str], i: int, default_float: float = 0.0) -> float:
        """
        This method parses the i-th element in the given list of strings to a float value.
        Returns the given default float if there is no such element or if the element is empty.
        Throws an exception if the i-th element doesn't represent a float.

        Args:
            args: List[str]
                The list of strings.
            i: int
                The index of the element to parse.
            default_int: float
                The default value to return if no such element exists or if the element is empty.
        Returns:
            float:
                The i-th element of the array as a float.
        """
        if not args:
            return default_float
        if i >= len(args):
            return default_float
        if not args[i]:
            return default_float

        return float(args[i])

    def parse_string(self, args: List[str], i: int, default_string: str = "") -> str:
        """
        This method returns the i-th element in the given list of strings. Returns the given
        default string if there is no such element or if the element is empty.

        Args:
            args: List[str]
                The list of strings.
            i: int
                The index of the element to parse.
            default_string: str
                The default value to return if no such element exists or if the element is empty.
        Returns:
            str:
                The i-th element of the array or the default string.
        """
        if not args:
            return default_string
        if i >= len(args):
            return default_string
        if not args[i]:
            return default_string

        return args[i]

    def parse_color(self, args: List[str], i: int, default_color: Tuple[float, float, float]
            = (0, 0, 0)) -> Tuple[float, float, float]:
        """
        This method parses the i-th element in the given list of strings to a color value.
        Returns the given default color if there is no such element or if the element is empty.
        Throws an exception if the i-th element couldn't be parsed to a color.

        Args:
            args: List[str]
                The list of strings.
            i: int
                The index of the element to parse.
            default_color: Tuple[float, float, float]
                The default value to return if no such element exists or if the element is empty.
        Returns:
            Tuple[float, float, float]:
                The i-th element of the array as a color.
        """
        if not args:
            return default_color
        if i >= len(args):
            return default_color
        if not args[i]:
            return default_color

        # Check if the color is provided as an RGB value, in the form "rgb(R,G,B)".
        if args[i].startswith("rgb("):
          # Extract the "R,G,B" part
          rgb_str = args[i][4:-1]
          # Translate it to an array [R, G, B]
          rgb_array = rgb_str.split(",");
          if len(rgb_array) != 3:
              raise ValueError(f"'{args[i]}' isn't a valid RGB color code.", args[i]);

          # Compute the float values of R, G and B.
          r = float(rgb_array[0].strip())
          g = float(rgb_array[1].strip())
          b = float(rgb_array[2].strip())

          return (r, g, b)


if __name__ == "__main__":
    # Create a command line argument parser.
    arg_parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # The path to the PDF file to which the drawings should be added.
    arg_parser.add_argument(
        "-i", "--input_pdf",
        type=str,
        required=True,
        help="The path to the PDF file to which the drawings should be added."
    )

    # The path to the file that contains drawing instructions.
    arg_parser.add_argument(
        "-j", "--instruction_file",
        type=str,
        required=True,
        help="The path to the file that contains drawing instructions."
    )

    # The path where the final PDF file (with drawings added to it) should be stored.
    arg_parser.add_argument(
        "-o", "--output_pdf",
        type=str,
        required=True,
        help="The path where the final PDF file (with drawings added to it) should be stored."
    )

    args = arg_parser.parse_args()
    pdf_drawer = PdfDrawer(pdf_path=args.input_pdf)
    pdf_drawer.process_instruction_file(args.instruction_file)
    pdf_drawer.save(args.output_pdf)