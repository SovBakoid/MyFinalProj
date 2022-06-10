import streamlit as st
import streamlit.components.v1 as components

with st.echo(code_location="below"):

    #from telegram import ForceReply
    #from telegram import Update
    #from telegram.ext import MessageHandler
    #from telegram.ext import filters
    #from telegram.ext import Application
    #from telegram.ext import ContextTypes, CommandHandler
    #import sqlite3
    #import logging

    #TOKEN = '5551708011:AAEOHzx-oA8auTNg4MsD6VkQqV4DqczrFIM'

    #logging.basicConfig(
        #format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    #)
    #logger = logging.getLogger(__name__)

    #async def start(update: Update, context: ContextTypes) -> None:
        #user = update.effective_user
        #await update.message.reply_html(
            #rf"Привет, {user.mention_html()}! Я придумал одну классную штуку! Часто случается, что вам приглянулась какая-то машина на улице, но вы не можете определить марку или модель. Если такое случилось, просто напишите мне номер в формате А777МР77 кириллическими буквами, и я вам все раскажу.",
            #reply_markup=ForceReply(selective=True),
        #)

    #async def numberplate(update: Update, context: ContextTypes) -> None:
        #text=update.message.text
        #print(text)
        #con = sqlite3.connect("number_plates_database.sqlite")
        #c = con.cursor()
        #answers = c.execute('''SELECT gibdd2_car_model FROM sheesh
        #WHERE gibdd2_car_plate_number = ?''', [f'{text}']).fetchall()
        #c.close()
        #await update.message.reply_text(f"С таким номером в Москве есть всего {len(answers)} машина(ы): {answers}")


    #def main():
        #print("start")
        #application = Application.builder().token(TOKEN).build()
        #application.add_handler(CommandHandler("start", start))
        #application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, numberplate))
        #application.run_polling()
        #print("finish")

    #if __name__=='__main__':
        #main()

    st.header("@shurovbogbot")

    st.write("Я решил написать бота. Это быстро и просто.")

    st.write("Я сначала создал табличку из всех моделей машин и номеров машин, у которых код региона соответствует любому из московских.")

    HtmlFile = open('Вывод_данных3.html', 'r', encoding='utf-8')

    components.html(HtmlFile.read(), height=500, width=1000, scrolling=True)

    st.write("Потом я все это дело загрузил в базу банных sqlite3 и написал бота, который обращается к SQL запросами к необходимым данным. Код бота вы можете увидеть ниже. БольшУю часть кода для бота я взял из официальной документации.")

    st.write("Чтобы воспользоваться ботом, напишите ему в тг @shurovbogbot. Идея бота в том, что вы можете написать ему номер машины в формате А777МР77 кириллическими буквами и он вам расскажет какой модели эта машина.")

    st.write("Возможное применение: ваш друг мажор пригоняет на новом гелике в обвесе BRABUS и задвигает, что в нем 900 сил. Но вы то слышите дизельный стук в моторе и чувствуете, что обвес то из китайского пластика. Просто берете, вбиваете номер тачки в бота, а он вам отвечает, что модель G350D, а вовсе никакой не G63. ")