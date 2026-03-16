

# from docling.datamodel.pipeline_options import PictureDescriptionVlmOptions
#%%

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    PdfPipelineOptions,
    VlmConvertOptions
)
from docling.datamodel.vlm_engine_options import (    
    ApiVlmEngineOptions,
    VlmEngineType,)
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.pipeline.vlm_pipeline import VlmPipeline
from docling.datamodel.pipeline_options import  VlmPipelineOptions
input_doc_path = r"D:\Git\docling_demo\tests\testinputpdf\2408.09869v5.pdf"
#"https://arxiv.org/pdf/2408.09869"
vlm_options = VlmConvertOptions.from_preset(
        "granite_docling",
        engine_options=ApiVlmEngineOptions(
            engine_type=VlmEngineType.API_OLLAMA,
            # url is pre-configured for Ollama (http://localhost:11434/v1/chat/completions)
            # model name is pre-configured from the preset (should be ibm/granite-docling:258m)
            timeout=90,
        ),
    )

# Debug: confirm which model will be requested from Ollama
print("Engine options:", vlm_options.engine_options)
print("Effective API params:", vlm_options.model_spec.get_api_params(vlm_options.engine_options.engine_type))

pipeline_options = VlmPipelineOptions(
        vlm_options=vlm_options,
        enable_remote_services=True,
    )

doc_converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=pipeline_options,
                pipeline_cls=VlmPipeline,
            )
        }
    )

result = doc_converter.convert(input_doc_path)

# Save output to disk
from pathlib import Path

output_dir = Path("output")
output_dir.mkdir(parents=True, exist_ok=True)

output_path = output_dir / (Path(input_doc_path).stem + ".doctags.txt")
output_text = result.document.export_to_doctags()
output_path.write_text(output_text, encoding="utf-8")

print(f"Saved output to {output_path}")




#%%

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    PdfPipelineOptions,
    VlmConvertOptions
)
from docling.datamodel.vlm_engine_options import (    
    ApiVlmEngineOptions,
    VlmEngineType,)
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.pipeline.vlm_pipeline import VlmPipeline
from docling.datamodel.pipeline_options import  VlmPipelineOptions
input_doc_path = r"D:\Git\docling_demo\tests\testinputpdf\2408.09869v5.pdf"
#"https://arxiv.org/pdf/2408.09869"
vlm_options = VlmConvertOptions.from_preset(
        "granite_docling",
        engine_options=ApiVlmEngineOptions(
            engine_type=VlmEngineType.API_OLLAMA,
            # url is pre-configured for Ollama (http://localhost:11434/v1/chat/completions)
            # model name is pre-configured from the preset (should be ibm/granite-docling:258m)
            timeout=90,
        ),
    )

# Debug: confirm which model will be requested from Ollama
print("Engine options:", vlm_options.engine_options)
print("Effective API params:", vlm_options.model_spec.get_api_params(vlm_options.engine_options.engine_type))

pipeline_options = VlmPipelineOptions(
        vlm_options=vlm_options,
        enable_remote_services=True,
    )

doc_converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=pipeline_options,
                pipeline_cls=VlmPipeline,
            )
        }
    )

result = doc_converter.convert(input_doc_path)

# Save output to disk
from pathlib import Path

output_dir = Path("output")
output_dir.mkdir(parents=True, exist_ok=True)

output_path = output_dir / (Path(input_doc_path).stem + ".doctags.txt")
output_text = result.document.export_to_doctags()
output_path.write_text(output_text, encoding="utf-8")

print(f"Saved output to {output_path}")
