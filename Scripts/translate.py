from googletrans import Translator

translator = Translator()

async def translator_function(text):
    translated_text = await translator.translate(text, dest='fr')
    return translated_text.text

