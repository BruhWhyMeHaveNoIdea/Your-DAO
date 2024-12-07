import openai
import config
import bot.gpt.utils as utils

openai.api_key = config.GPT_TOKEN


async def ask_gpt(questions):
    questions = [["system", "Ты хороший помощник. На все вопросы отвечай на русском"]] + questions
    messages = utils.gpt_converter(questions)
    response = await openai.ChatCompletion.acreate(
        model="gpt-4o-mini",
        messages=messages
    )
    return response['choices'][0]['message']['content']


async def speech_to_text(file_path):
    try:
        with open(file_path, 'rb') as audio_file:
            response = openai.Audio.transcribe(
                file=audio_file,
                model="whisper-1",
                language="ru"
            )
            decoded_data = response.to_dict()

        if "text" in decoded_data:
            return decoded_data["text"]
        else:
            return None

    except openai.error.OpenAIError:
        return None
