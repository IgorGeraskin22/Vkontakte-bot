# -*- coding: utf-8 -*-
import vk_api
import logging

try:
    from _token import my_token
except ImportError:
    my_token = None
    print('Ошибка импорта my_token')
    exit()

from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id


group_id = 'group_id'
log = logging.getLogger('bot')  # имя логера


def configure_logging():
    stream_handler = logging.StreamHandler()
    # stream_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s')).
    stream_handler.setFormatter(logging.Formatter('%(levelname)s %(message)s'))
    stream_handler.setLevel(logging.INFO)
    log.addHandler(stream_handler)

    file_handler = logging.FileHandler('bot.log', encoding='utf8')
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%d.%m.%Y %H:%M'))
    log.setLevel(logging.DEBUG)
    log.addHandler(file_handler)
    file_handler.setLevel(logging.DEBUG)


class Bot:
    def __init__(self, _group_id, token):
        self.group_id = group_id
        self.my_token = my_token
        self.vk = vk_api.VkApi(token=token)
        self.long_poller = VkBotLongPoll(self.vk, self.group_id)
        self.api = self.vk.get_api()

    def run(self):
        for event in self.long_poller.listen():
            try:
                self.on_event(event)
            except Exception:
                log.exception('ошибка в обработке события')
                # print('Error - ', ex) заменили на log.exception

    def on_event(self, event):
        if event.type == VkBotEventType.MESSAGE_NEW:
            log.debug('отправляем сообщение назад')  # что бы видеть как разные уровни логирования срабатывают
            self.api.messages.send(message=event.message.text,
                                   random_id=get_random_id(),
                                   peer_id=event.message.peer_id)

        else:
            log.info('Мы не умеем обрабатывать события такого типа %s', event.type)


if __name__ == '__main__':
    configure_logging()
    bot = Bot(group_id, my_token)
    bot.run()
