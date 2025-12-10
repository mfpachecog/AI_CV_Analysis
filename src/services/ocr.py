from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from src.services.config import settings

class AzureOCRService:
    def __init__(self):
        self.client = None
        if settings.AZURE_DOC_ENDPOINT and settings.AZURE_DOC_KEY:
            try:
                self.client = DocumentAnalysisClient(
                    endpoint=settings.AZURE_DOC_ENDPOINT,
                    credential=AzureKeyCredential(settings.AZURE_DOC_KEY)
                )
            except Exception as e:
                print(f"⚠️ Error inicializando Azure OCR: {e}")

    def extract_text_from_pdf(self, file_content: bytes) -> str:
        """
        Envía los bytes del PDF a Azure y retorna todo el texto extraído.
        """
        if not self.client:
            raise Exception("El servicio de Azure OCR no está configurado correctamente.")

        try:
            # Usamos el modelo 'prebuilt-read' que es ideal para texto general
            poller = self.client.begin_analyze_document(
                "prebuilt-read", document=file_content
            )
            result = poller.result()

            # Concatenamos todo el texto encontrado en todas las páginas
            full_text = []
            for page in result.pages:
                for line in page.lines:
                    full_text.append(line.content)
            
            return "\n".join(full_text)
            
        except Exception as e:
            print(f"❌ Error durante el análisis del documento: {e}")
            raise e