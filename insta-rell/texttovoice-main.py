import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import pyttsx3
from pydub import AudioSegment

# Set up logging to help with debugging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Text-to-speech function
def text_to_speech_function(text, filename="output.wav"):
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 40)  # Slow down the speech rate if needed
    engine.say(text)
    engine.save_to_file(text, filename)
    engine.runAndWait()

# Convert WAV to MP3 using pydub
def convert_wav_to_mp3(wav_filename, mp3_filename):
    sound = AudioSegment.from_wav(wav_filename)
    sound.export(mp3_filename, format="mp3")

# Start command handler
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Hi! Send me any text and I will send you an MP3 file of the speech.')

# Handle incoming text messages and convert to speech
async def handle_text(update: Update, context: CallbackContext) -> None:
    text = update.message.text

    # Save the speech as a WAV file
    wav_filename = "output.wav"
    mp3_filename = "output.mp3"
    text_to_speech_function(text, wav_filename)

    # Convert the WAV to MP3
    convert_wav_to_mp3(wav_filename, mp3_filename)

    # Send the MP3 file to the user
    with open(mp3_filename, 'rb') as mp3_file:
        await update.message.reply_audio(mp3_file)

# Error handling function
async def error(update: Update, context: CallbackContext) -> None:
    logger.warning(f'Update {update} caused error {context.error}')

def main():
    # Set up the Application using your bot token
    application = Application.builder().token("7910201137:AAGvouyz_aVC1JFybfpN2Q8a0ohS_Ffx9ig").build()

    # Command handler to start the bot
    application.add_handler(CommandHandler("start", start))

    # Handler to process any text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    # Log all errors
    application.add_error_handler(error)

    # Start the bot (polling for messages)
    application.run_polling()

if __name__ == '__main__':
    main()
