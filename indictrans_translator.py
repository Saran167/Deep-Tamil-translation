from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_name = "ai4bharat/indictrans2-en-indic-1B"

tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name, trust_remote_code=True)

def translate_text(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True)
    outputs = model.generate(**inputs, max_length=256)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

