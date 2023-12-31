from transformers import pipeline
from ..abstract_transsum_text_summarizer import AbstractTranssumTextSummarizer
from ...text_translation import AbstractTextTranslator
from ..transsum_text_summarization_result import TranssumTextSummarizationResult

class FlanT5Summarizer(AbstractTranssumTextSummarizer):
    def __init__(
        self,
        de_to_en_translator: AbstractTextTranslator,
        en_to_de_translator: AbstractTextTranslator,
    ):
        super().__init__(de_to_en_translator, en_to_de_translator)

        self.summarizer = pipeline(
            'summarization',
            model='philschmid/flan-t5-base-samsum',
            truncation=True
        )

    @staticmethod
    def get_name() -> str:
        return 'FlanT5Summarizer (philschmid/flan-t5-base-samsum)'

    def summarize(self, input_text: str) -> TranssumTextSummarizationResult:
        text_de = input_text
        text_en = self._pre_summarize(text_de)
        summary_en = self.summarizer(text_en, max_length=1512)[0]['summary_text']
        summary_de = self._post_summarize(summary_en)

        return TranssumTextSummarizationResult(text_de, summary_de, text_en, summary_en)