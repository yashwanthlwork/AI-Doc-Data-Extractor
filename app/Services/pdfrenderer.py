import pymupdf

class PDFRenderer:

    def render(self, pdf_bytes: bytes) -> list[bytes]:
            document=None
            try:
                document = pymupdf.open(stream=pdf_bytes, filetype="pdf")
                png_pages = []

                for page in document:
                    pixmap = page.get_pixmap()
                    png_pages.append(pixmap.tobytes("png"))
                return png_pages
            finally:
                 if document:
                    document.close()
                
    