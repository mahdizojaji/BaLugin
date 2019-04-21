from main import *


def echo(bot: Bot, update: base_models.FatSeqUpdate):
    # Send a message to client
    bot.reply(update, 'test1')


returns = dict(
    func=echo
)
