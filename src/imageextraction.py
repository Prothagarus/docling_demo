from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import PdfFormatOption

pipeline_options = PdfPipelineOptions(generate_picture_images=True)

# Create converter with enhanced table processing
converter_enhanced = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    }
)

result_enhanced = converter_enhanced.convert("https://arxiv.org/pdf/2408.09869")
doc_enhanced = result_enhanced.document