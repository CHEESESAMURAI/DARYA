from aiogram import Bot, Dispatcher, executor, types
from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel

STICKER_ID1 = 'CAACAgIAAxkBAAEETMtiQZDXr7ucg_Y2XzkyPqrT5m-ucgACqwIAAjZ2IA4vRxK7XlfP0yME' #POS
STICKER_ID2 = 'CAACAgIAAxkBAAEETM1iQZEVYPCV623EnrHJwsAgUnBXcwACuQIAAjZ2IA7tdOsFZ9JbhSME' #HI
STICKER_ID3 = 'CAACAgIAAxkBAAEETMdiQZC6AAGNKTdYX3iihcx0JaNM1lAAArUCAAI2diAOBDcfp-Faa4gjBA' #ANGRY
STICKER_ID4 = 'CAACAgIAAxkBAAEETMViQZC2qcuUd-lg_acEwLApmf3nmgACvAIAAjZ2IA51EqleGhaPFSME' #NEPON
STICKER_ID5 = 'CAACAgIAAxkBAAEETMliQZDHQlZZB4XES56LoOFuHv62AAOxAgACNnYgDstvp_Zy2sn9IwQ' #HZ
STICKER_ID6 = 'CAACAgIAAxkBAAEETM9iQZFlJCK3KhqsCuMBNHYe1WQOIgACtgIAAjZ2IA7n32q5Z54wcSME' #what
STICKER_ID7 = 'CAACAgIAAxkBAAEETNNiQZI8UDS4NsXRWlgy7KCrRxtgfQACvgIAAjZ2IA7h0bEDcPJpciME' #start
STICKER_ID8 = 'CAACAgIAAxkBAAEETNdiQZRtSQL9LXT59OQ7VdOMKhqcxgACvwIAAjZ2IA6DDqb7e0kSxSME' #rech

bot = Bot(token='5132803445:AAHnqE872bqje9aRs2JY_8FjrbNLe7q04CI')
dp = Dispatcher(bot)

itembtn1 = types.KeyboardButton('Запустить анализатор')
itembtn2 = types.KeyboardButton('Что может этот бот ?')

keyboard = types.ReplyKeyboardMarkup(True,False)
keyboard.row(itembtn1,itembtn2)


@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    await bot.send_sticker(message.chat.id, STICKER_ID2)
    await bot.send_message(message.chat.id , 'Позлравляю вы запустили бота , теперь выберите функцию',reply_markup=keyboard)
    await bot.send_message(message.chat.id,'Что бы начать работу с ботом \n, нажмите: Запустить анализатор ,а что бы узнать ,\n что это за бот и его возможности, то нажмите :Что может этот бот? ')

@dp.message_handler(text = ['Запустить анализатор'])
async def start_bot(message: types.Message):
    await bot.send_sticker(message.chat.id, STICKER_ID7)
    await bot.send_message(message.chat.id,'1)Напишите любое предложение или текст и отправьте боту одним сообщением\n'
                                           '2)Бот проанализирует ваше сообщение или текст по 5 основным критерям оценивания в русском языке\n'
                                           '3)Вы должны понимать , что это оценивает нейронная сеть и точность оценки не всегда объективная\n'
                                           '4)Радуся жизин!')


@dp.message_handler(text=['Что может этот бот ?'])
async def start_any(message: types.Message):
    await bot.send_sticker(message.chat.id, STICKER_ID6)
    await bot.send_message(message.chat.id,'Данный бот был придуман Дашей , для оценки тональности сообщений.'
                                           ' Оценка происходит нейронной сетью , которая была ранее обученая на моделях.\n'
                                           'Для начала, давайте разберемся с терминологией. Определение тональности — это метод анализа речи в компьютерной лингвистике.\n'
                                           'Он используется для определения настроения конкретных высказываний. Приведу простые примеры позитивных и негативных предложений.\n'
                                           'Позитивные: «Сегодня хорошая погода», «Я счастлив проводить с тобою время», «Мне нравится эта музыкальная композиция».\n'
                                           'Негативные: «В больнице была ужасная очередь», «Сосед с верхнего этажа мешает спать», «Маленькая девочка потерялась в торговом центре».\n'
                                           'Помимо позитивных и негативных оценок тональности существуют еще нейтральные. Нейтральная тональность не содержит в себе эмоциональной окраски.')
    await bot.send_photo(message.chat.id,'https://egorovegor.ru/wp-content/uploads/8bcc7bc6.jpg')

@dp.message_handler(content_types=types.ContentTypes.ANY)
async def all_other_messages(message: types.Message):

    tokenizer = RegexTokenizer()
    model = FastTextSocialNetworkModel(tokenizer=tokenizer)

    slova = []
    slova.append(message.text)

    results = model.predict(slova, k=2)
    for slova, sentiment in zip(slova, results):
        print(slova, '-&gt;', sentiment)

        par = 5
        opr = ['neutral','positive','negative','skip','speech']

        if sentiment.get('positive', False) == False:
            sentiment['positive'] = 0
            par-=1
            opr.remove('positive')
        if sentiment.get('negative', False) == False:
            sentiment['negative'] = 0
            par-= 1
            opr.remove('negative')
        if sentiment.get('neutral', False) == False:
            sentiment['neutral'] = 0
            par-=1
            opr.remove('neutral')
        if sentiment.get('skip', False) == False:
            sentiment['skip'] = 0
            par-= 1
            opr.remove('skip')
        if sentiment.get('speech', False) == False:
            sentiment['speech'] = 0
            par-=1
            opr.remove('speech')

        # def toFixed(f: float, n=0):
        #     a, b = str(f).split('.')
        #     return '{}.{}{}'.format(a, b[:n], '0' * (n - len(b)))
        #
        def toFixed(f: float, n=0):
            a, b = str(f).split('.')
            return '{}.{}{}'.format(a, b[:n], '0' * (n - len(b)))

        print(toFixed(float(sentiment['skip']),2))
        print(toFixed(float(sentiment['neutral']),2))
        print(toFixed(float(sentiment['positive']),2))
        print(toFixed(float(sentiment['negative']),2))
        print(toFixed(float(sentiment['speech']),2))
        print(par)
        print(opr)

        if sentiment['positive'] > sentiment['negative'] or sentiment['positive'] > sentiment['neutral'] or sentiment['positive'] > sentiment['skip'] or sentiment['positive'] > sentiment['speech']:
            if par == 2 or par == 1 or par == 3:
                await bot.send_sticker(message.chat.id, STICKER_ID1)
                await bot.send_message(message.chat.id, 'Ваше сообщение содержит несколько парамметров:')
                await bot.send_message(message.chat.id, 'Ваше сообщение больше ПОЗИТИВНОЕ '+toFixed(float(sentiment['positive']),2)+' %, но и содержит ')
                if 'negative' in opr:
                    await bot.send_message(message.chat.id, 'негатив '+toFixed(float(sentiment['negative']),2)+' %')
                    await bot.send_message(message.chat.id,
                                           'Что бы продолжить работу анализтора , просто напишите еще текст и бот оценит его')
                    break
                elif 'neutral' in opr:
                    await bot.send_message(message.chat.id, 'нейтральность '+toFixed(float(sentiment['neutral']),2)+' %')
                    await bot.send_message(message.chat.id,
                                           'Что бы продолжить работу анализтора , просто напишите еще текст и бот оценит его')
                    break
                elif 'skip' in opr:
                    await bot.send_message(message.chat.id, 'непонятность '+toFixed(float(sentiment['skip']),2)+' %')
                    await bot.send_message(message.chat.id,
                                           'Что бы продолжить работу анализтора , просто напишите еще текст и бот оценит его')
                    break
                elif 'speech' in opr:
                    await bot.send_message(message.chat.id, 'речь '+toFixed(float(sentiment['speech']),2)+' %')
                    await bot.send_message(message.chat.id,
                                           'Что бы продолжить работу анализтора , просто напишите еще текст и бот оценит его')
                    break

            elif par == 4:
                await bot.send_message(message.chat.id, 'Ваше сообщение позитивное')
                await bot.send_message(message.chat.id,
                                       'Что бы продолжить работу анализтора , просто напишите еще текст и бот оценит его')

        if sentiment['negative'] > sentiment['positive'] or sentiment['negative'] > sentiment['neutral'] or sentiment['negative'] > sentiment['skip'] or sentiment['negative'] > sentiment['speech']:
            if par == 2 or par == 1 or par == 3:
                await bot.send_sticker(message.chat.id, STICKER_ID3)
                await bot.send_message(message.chat.id, 'Ваше сообщение содержит несколько парамметров:')
                await bot.send_message(message.chat.id, 'Ваше сообщение больше НЕГАТИВНОЕ не '+toFixed(float(sentiment['negative']),2)+' %, но и содержит ')
                if 'positive' in opr:
                    await bot.send_message(message.chat.id, 'позитива '+toFixed(float(sentiment['positive']),2)+' %')
                    await bot.send_message(message.chat.id,'Что бы продолжить работу анализтора , просто напишите еще текст и бот оценит его')
                    break
                elif 'neutral' in opr:
                    await bot.send_message(message.chat.id, 'нейтральность '+toFixed(float(sentiment['neutral']),2)+' %')
                    await bot.send_message(message.chat.id,'Что бы продолжить работу анализтора , просто напишите еще текст и бот оценит его')
                    break
                elif 'skip' in opr:
                    await bot.send_message(message.chat.id, 'непонятность '+toFixed(float(sentiment['skip']),2)+' %')
                    await bot.send_message(message.chat.id,
                                           'Что бы продолжить работу анализтора , просто напишите еще текст и бот оценит его')
                    break
                elif 'speech' in opr:
                    await bot.send_message(message.chat.id, 'речь '+toFixed(float(sentiment['speech']),2)+' %')
                    await bot.send_message(message.chat.id,
                                           'Что бы продолжить работу анализтора , просто напишите еще текст и бот оценит его')
                    break

            elif par == 4 :
                await bot.send_message(message.chat.id, 'Ваше сообщение негативное ')
                await bot.send_message(message.chat.id,
                                       'Что бы продолжить работу анализтора , просто напишите еще текст и бот оценит его')

        if sentiment['neutral'] > sentiment['negative'] or sentiment['neutral'] > sentiment['positive'] or sentiment['neutral'] > sentiment['skip'] or sentiment['neutral'] > sentiment['speech']:
            if par == 2 or par == 1 or par == 3:
                await bot.send_sticker(message.chat.id,STICKER_ID4)
                await bot.send_message(message.chat.id, 'Ваше сообщение содержит несколько парамметров:')
                await bot.send_message(message.chat.id, 'Ваше сообщение больше НЕЙТРАЛЬНОЕ на '+toFixed(float(sentiment['neutral']),2)+' %, но и содержит ')
                if 'negative' in opr:
                    await bot.send_message(message.chat.id, 'негатив '+toFixed(float(sentiment['negative']),2)+' %')
                    await bot.send_message(message.chat.id,
                                           'Что бы продолжить работу анализтора , просто напишите еще текст и бот оценит его')
                    break
                elif 'positive' in opr:
                    await bot.send_message(message.chat.id, 'позитива '+toFixed(float(sentiment['positive']),2)+' %')
                    await bot.send_message(message.chat.id,
                                           'Что бы продолжить работу анализтора , просто напишите еще текст и бот оценит его')
                    break
                elif 'skip' in opr:
                    await bot.send_message(message.chat.id, 'непонятность '+toFixed(float(sentiment['skip']),2)+' %')
                    await bot.send_message(message.chat.id,
                                           'Что бы продолжить работу анализтора , просто напишите еще текст и бот оценит его')
                    break
                elif 'speech' in opr:
                    await bot.send_message(message.chat.id, 'речь '+toFixed(float(sentiment['speech']),2)+' %')
                    await bot.send_message(message.chat.id,
                                           'Что бы продолжить работу анализтора , просто напишите еще текст и бот оценит его')
                    break
            elif par == 4:
                await bot.send_message(message.chat.id, 'Ваше сообщение нейтральное ')
                await bot.send_message(message.chat.id,
                                       'Что бы продолжить работу анализтора , просто напишите еще текст и бот оценит его')

        if sentiment['skip'] > sentiment['negative'] or sentiment['skip'] > sentiment['neutral'] or sentiment['skip'] > sentiment['positive'] or sentiment['skip'] > sentiment['speech']:
            if par == 2 or par == 1 or par == 3:
                await bot.send_sticker(message.chat.id, STICKER_ID5)
                await bot.send_message(message.chat.id, 'Ваше сообщение содержит несколько парамметров:')
                await bot.send_message(message.chat.id, 'Ваше сообщение больше НЕПОНЯТНОЕ на '+toFixed(float(sentiment['skip']),2)+' % , но и содержит ')
                if 'negative' in opr:
                    await bot.send_message(message.chat.id, 'негатив '+toFixed(float(sentiment['negative']),2)+' %')
                    await bot.send_message(message.chat.id,
                                           'Что бы продолжить работу анализтора , просто напишите еще текст и бот оценит его')
                    break
                elif 'neutral' in opr:
                    await bot.send_message(message.chat.id, 'нейтральность '+toFixed(float(sentiment['neutral']),2)+' %')
                    await bot.send_message(message.chat.id,
                                           'Что бы продолжить работу анализтора , просто напишите еще текст и бот оценит его')
                    break
                elif 'positive' in opr:
                    await bot.send_message(message.chat.id, 'позитива '+toFixed(float(sentiment['positive']),2)+' %')
                    await bot.send_message(message.chat.id,
                                           'Что бы продолжить работу анализтора , просто напишите еще текст и бот оценит его')
                    break
                elif 'speech' in opr:
                    await bot.send_message(message.chat.id, 'речь '+toFixed(float(sentiment['speech']),2)+' %')
                    await bot.send_message(message.chat.id,
                                           'Что бы продолжить работу анализтора , просто напишите еще текст и бот оценит его')
                    break
            elif par == 4:
                await bot.send_message(message.chat.id, 'Ваше сообщение непонятное ')
                await bot.send_message(message.chat.id,
                                       'Что бы продолжить работу анализтора , просто напишите еще текст и бот оценит его')

        if sentiment['speech'] > sentiment['negative'] or sentiment['speech'] > sentiment['neutral'] or sentiment['speech'] > sentiment['positive'] or sentiment['speech'] > sentiment['skip']:
            if par == 2 or par == 1 or par == 3:
                await bot.send_sticker(message.chat.id,STICKER_ID8)
                await bot.send_message(message.chat.id, 'Ваше сообщение содержит несколько парамметров:')
                await bot.send_message(message.chat.id, 'Ваше сообщение больше РЕЧЕВОЕ на '+toFixed(float(sentiment['speech']),2)+' %, но и содержит ')
                if 'negative' in opr:
                    await bot.send_message(message.chat.id, 'негатив'+toFixed(float(sentiment['negative']),2)+'%')
                    await bot.send_message(message.chat.id,
                                           'Что бы продолжить работу анализтора , просто напишите еще текст и бот оценит его')
                    break
                elif 'neutral' in opr:
                    await bot.send_message(message.chat.id, 'нейтральность '+toFixed(float(sentiment['neutral']),2)+' %')
                    await bot.send_message(message.chat.id,
                                           'Что бы продолжить работу анализтора , просто напишите еще текст и бот оценит его')
                    break
                elif 'positive' in opr:
                    await bot.send_message(message.chat.id, 'позитива'+toFixed(float(sentiment['positive']),2)+' %')
                    await bot.send_message(message.chat.id,
                                           'Что бы продолжить работу анализтора , просто напишите еще текст и бот оценит его')
                    break
                elif 'speech' in opr:
                    await bot.send_message(message.chat.id, 'непонятность '+toFixed(float(sentiment['speech']),2)+' %')
                    await bot.send_message(message.chat.id,
                                           'Что бы продолжить работу анализтора , просто напишите еще текст и бот оценит его')
                    break
            elif par == 4:
                await bot.send_message(message.chat.id, 'Ваше сообщениене речевое ')
                await bot.send_message(message.chat.id,
                                       'Что бы продолжить работу анализтора , просто напишите еще текст и бот оценит его')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)