from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class IndicTransTranslator:
    def __init__(self):
        # Load the IndicTrans model and tokenizer
        self.model_name = "ai4bharat/indic-trans-encoder-decoder"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)

    def translate(self, text, source_lang="ta", target_lang="ta"):
        # Encode the input text
        inputs = self.tokenizer.encode(text, return_tensors="pt")
        # Perform translation
        outputs = self.model.generate(inputs, max_length=512)
        # Decode the output
        translated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return translated_text

# Create a single instance of the translator
indictrans_translator = IndicTransTranslator()
