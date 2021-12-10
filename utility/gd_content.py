def read_paragraph_element(element):
    """Returns text in given ParagraphElement

        Args:
            element: ParagraphElement from Google Doc
    """
    text_run = element.get('textRun')
    if not text_run:
        return ''
    return text_run.get('content')

def read_structural_elements(elements):
    """Recurses through list of Structural Elements to read document's 
       text where text may be in nested elements

        Args:
            elements: list of Structural Elements.
    """
    text = ''
    for value in elements:
        if 'paragraph' in value:
            elements = value.get('paragraph').get('elements')
            for elem in elements:
                text += read_paragraph_element(elem)
        elif 'table' in value:
            # text in table cells are in nested Structural Elements
            # and tables may be nested
            table = value.get('table')
            for row in table.get('tableRows'):
                cells = row.get('tableCells')
                for cell in cells:
                    text += read_strucutural_elements(cell.get('content'))
        elif 'tableOfContents' in value:
            # text in TOC is also in Structural Element.
            toc = value.get('tableOfContents')
            text += read_strucutural_elements(toc.get('content'))
    return text
