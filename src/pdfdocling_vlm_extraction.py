
#%%
from docling.document_converter import DocumentConverter
import pandas as pd
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import PdfFormatOption
from docling.datamodel.base_models import InputFormat
#%%
# Initialize converter with default settings
converter = DocumentConverter()

# Convert any document format - we'll use the Docling technical report itself
source_url = "https://arxiv.org/pdf/2408.09869"
result = converter.convert(source_url)

# Access structured data immediately
doc = result.document
print(f"Successfully processed document from: {source_url}")

#%%
from collections import defaultdict

# Create a dictionary to categorize all document elements by type
element_types = defaultdict(list)

# Iterate through all document elements and group them by label
for item, _ in doc.iterate_items():
    element_type = item.label
    element_types[element_type].append(item)

# Display the breakdown of document structure
print("Document structure breakdown:")
for element_type, items in element_types.items():
    print(f"  {element_type}: {len(items)} elements")


# %%
first_table = element_types["table"][0]
# Export to DataFrame and show raw table
table_df = first_table.export_to_dataframe(doc=doc)
print(table_df.to_markdown())
# notice how there are some merged cells in the table and they have two values in some columns

# Example: detect multi-valued columns (including space-delimited numeric/unit pairs)
from table_utils import split_and_explode, detect_multivalue_columns
pattern = r"\s*(?:;|,|/|\n)\s*"

candidate_cols = detect_multivalue_columns(table_df)
if candidate_cols:
    expanded = split_and_explode(table_df, candidate_cols, delimiter_regex=pattern, mode="pairwise", smart=True)
    print("\nExpanded table (pairwise, smart=True) with one value per cell:")
    print(expanded.to_markdown())
else:
    print("No multi-valued columns detected; table unchanged.")


# %%
first_list_items = element_types["list_item"][0:6]
for list_item in first_list_items:
    print(list_item.text)
# %%
first_caption = element_types["caption"][0]
print(first_caption.text)
# %%
# Human-readable markdown for review
markdown_content = doc.export_to_markdown()
print(markdown_content[:500] + "...")

# %%

pipeline_options = PdfPipelineOptions(generate_picture_images=True)

# Create converter with enhanced table processing
converter_enhanced = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    }
)

result_enhanced = converter_enhanced.convert("https://arxiv.org/pdf/2408.09869")
doc_enhanced = result_enhanced.document

# %%
# Extract and display the first image
from IPython.display import Image, display

for item, _ in doc_enhanced.iterate_items():
    if item.label == "picture":
        image_data = item.image

        # Get the image URI
        uri = str(image_data.uri)

        # Display the image using IPython
        display(Image(url=uri))
        break

# %%
from docling.datamodel.pipeline_options import PdfPipelineOptions, TableFormerMode
from docling.datamodel.base_models import InputFormat
from docling.document_converter import PdfFormatOption

# Enhanced table processing for complex layouts
pipeline_options = PdfPipelineOptions()
pipeline_options.table_structure_options.mode = TableFormerMode.ACCURATE

# Create converter with enhanced table processing
converter_enhanced = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    }
)

result_enhanced = converter_enhanced.convert("https://arxiv.org/pdf/2408.09869")
doc_enhanced = result_enhanced.document
# %%
first_table = element_types["table"][0]
# Export to DataFrame and show raw table (enhanced parsing)
table_df = first_table.export_to_dataframe(doc=doc_enhanced)
print(table_df.to_markdown())

# Expanded example for enhanced parsing (smart splitting enabled)
from table_utils import split_and_explode, detect_multivalue_columns
pattern = r"\s*(?:;|,|/|\n)\s*"

candidate_cols = detect_multivalue_columns(table_df)
if candidate_cols:
    expanded = split_and_explode(table_df, candidate_cols, delimiter_regex=pattern, mode="pairwise", smart=True)
    print("\nExpanded table (pairwise, smart=True) with one value per cell:")
    print(expanded.to_markdown())
else:
    print("No multi-valued columns detected; table unchanged.")
# %%
# from docling.datamodel.pipeline_options import PictureDescriptionVlmOptions

# # AI-powered content enrichment
# pipeline_options = PdfPipelineOptions(
#     do_picture_description=True,  # AI-generated image descriptions
#     picture_description_options=PictureDescriptionVlmOptions(
#         repo_id="ibm-granite/granite-docling-258M",
#         prompt="Describe this picture. Be precise and concise.",
#     ),
#     generate_picture_images=True,
# )

# converter_enhanced = DocumentConverter(
#     format_options={
#         InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
#     }
# )

# result_enhanced = converter_enhanced.convert("https://arxiv.org/pdf/2408.09869")
# doc_enhanced = result_enhanced.document
from docling.datamodel.pipeline_options import PictureDescriptionVlmOptions

# AI-powered content enrichment
pipeline_options = PdfPipelineOptions(
    do_picture_description=True,  # AI-generated image descriptions
    picture_description_options=PictureDescriptionVlmOptions(
        repo_id="ibm-granite/granite-docling-258M",
        prompt="Describe this picture. Be precise and concise.",
    ),
    generate_picture_images=True,
)

converter_enhanced = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    }
)

result_enhanced = converter_enhanced.convert("https://arxiv.org/pdf/2408.09869")
doc_enhanced = result_enhanced.document
# %%
second_picture = doc_enhanced.pictures[1]

print(f"Caption: {second_picture.caption_text(doc=doc_enhanced)}")

# Check for annotations
for annotation in second_picture.annotations:
    print(annotation.text)