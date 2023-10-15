from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from PyPDF2 import PdfWriter, PdfReader
import PyPDF2
import fitz  # PyMuPDF
import datetime
from aiogram.types import FSInputFile
import os
# Вместо BOT TOKEN HERE нужно вставить токен вашего бота,
# полученный у @BotFather
BOT_TOKEN = '6462087787:AAEDuWwzxtMFbunSgRJ88Jb6vfoxIOJwCZU'

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def remove_image_from_all_pages(pdf_path, output_path, image_index):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    for page_number in range(len(pdf_document)):
        # Get the current page
        page = pdf_document[page_number]

        # Get the list of images on the page
        images = page.get_images(full=True)

        if image_index < len(images):
            # Get the image to remove
            image_to_remove = images[image_index]

            # Remove the image from the page
            page.delete_image(image_to_remove[0])

    # Save the modified PDF to the output file
    pdf_document.save(output_path)
    pdf_document.close()
    os.remove(pdf_path)
# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands='start'))
async def process_start_command(message: Message):
    await message.answer('Здравствуйте. Пришлите мне документ для обработки.')

# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(
        'Пришлите мне документ для обработки.'
    )

# Этот хэндлер будет срабатывать на любые ваши сообщения,
# кроме команд "/start" и "/help"
@dp.message(F.document)
async def send_echo(message: Message):
        await message.answer('Документ получен, запущена обработка.')
        document = message.document
        input_pdf = str(message.from_user.id)+"- first.pdf"  # Replace with the path to your input PDF file
        await bot.download(document,input_pdf)
        output_pdf = str(message.from_user.id)+"- second.pdf"  # Replace with the path for the output PDF file
        image_index_to_remove = 1  # Replace with the index of the image you want to remove
        remove_image_from_all_pages(input_pdf, output_pdf, image_index_to_remove)
        # opened file as reading (r) in binary (b) mode
        with open(str(message.from_user.id)+"- second.pdf", "rb") as file:
            # store data in pdfReader
            pdfReader = PyPDF2.PdfReader(file)
            # count number of pages
            totalPages = len(pdfReader.pages)
            reader = PdfReader(str(message.from_user.id)+"- second.pdf")
            for i in range(totalPages):
                page = reader.pages[i]
                page.trimbox.lower_left = (25, 25)
                page.trimbox.upper_right = (500, 500)
                a = 14
                b = 18
                c = 582.5
                d = 830
                page.cropbox.lower_left = (a, b)
                page.cropbox.upper_right = (d, c)
                page.cropbox.upper_left = (a, c)
                page.cropbox.lower_right = (d, b)
                output = PdfWriter()
                output.add_page(page)
                with open(str(i+1)+" - "+str(message.from_user.id)+".pdf", "wb") as out_f:
                    output.write(out_f)
                    output.close()
                doc_from_pc = FSInputFile(str(i+1)+" - "+str(message.from_user.id)+".pdf")
                result = await message.answer_document(doc_from_pc,filename=str(i+1))
                os.remove(str(i+1)+" - "+str(message.from_user.id)+".pdf")
        os.remove(str(message.from_user.id)+"- second.pdf")
@dp.message()
async def send_echo(message: Message):
        await message.answer('Это не документ. Пришлите мне документ для обработки')
        #doc=open("1.pdf", "rb")
        #await message.answer_document(types.InputFile('1.pdf'))
        #await message.answer_document(doc)
        #doc.close()
if __name__ == '__main__':
    dp.run_polling(bot)