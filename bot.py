from aiogram import executor

import handlers
from bot_init import dp

handlers.register_handlers(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
