from buttons.buttons import records_menu, yes_no_menu, cancel_menu, year_menu, monthes_menu, delete_stop_menu
from aiogram import types, Dispatcher
from database.requests import SQLighter
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext


""" dict for monthes """

monthes = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05',
'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}


""" connecting to database """

database_records = SQLighter()


""" /My_records """

async def command_my_records(message: types.Message):
    servises = database_records.get_utilities(message.from_user.id)
    await message.answer(servises, reply_markup=records_menu)

""" /Add_record """
class Record_adder(StatesGroup):
    service_name = State()
    year = State()
    month = State()
    total = State()
    confirmation = State()
    stop_edit = State()

async def command_add_record(message: types.Message):
    await Record_adder.service_name.set()
    await message.reply('What is the name of expense?', reply_markup=cancel_menu)

async def record_add_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    if data['name'] == 'Cancel':
        await state.finish()
        await message.answer('The operation is cancelled.')
        await command_my_records(message)
    elif database_records.is_service(message.from_user.id, data['name']):
        await Record_adder.next()
        await message.reply(f"Pick the year", reply_markup=year_menu)
    else:
        await message.reply(f"You don't have this expense type!\n\nThe operation is cancelled.", reply_markup=records_menu)
        await state.finish()
        await command_my_records(message)

async def record_add_year(message: types.Message, state: FSMContext):
    years = [2020, 2021, 2022, 2023]
    async with state.proxy() as data:
        try:
            data['year'] = message.text
            if data['year'] == 'Cancel':
                await state.finish()
                await message.answer('The operation is cancelled.')
                await command_my_records(message)
            elif int(data['year']) in years:
                await Record_adder.next()
                await message.reply(f"Pick the month", reply_markup=monthes_menu)
            else: raise ValueError
        except ValueError:
            await Record_adder.year.set()
            await message.reply(f"You have entered incorrect data!\nUse buttons, please.", reply_markup=year_menu)

async def record_add_month(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['month'] = message.text
    if data['month'] == 'Cancel':
        await state.finish()
        await message.answer('The operation is cancelled.')
        await command_my_records(message)
    elif data['month'] in monthes:
        date = f"{data['year']}-{monthes[data['month']]}"
        is_record = database_records.is_record(message.from_user.id, data['name'], date)
        if is_record:
            await Record_adder.stop_edit.set()
            await message.reply(f"You have this record already:\n\nService name: {is_record[0][2]}\n\
Date: {is_record[0][3]}\nAmount: {is_record[0][4]}\nPrice: {is_record[0][5]}\nSumm: {is_record[0][6]}\
\nWhat do You want to do?", reply_markup=delete_stop_menu)
        else:
            await Record_adder.next()
            await message.reply(f"Enter total sum", reply_markup=cancel_menu)
    else:
        await Record_adder.month.set()
        await message.reply(f"You have entered incorrect data!\nUse buttons, please.", reply_markup=monthes_menu)

async def record_add_total(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            data['total'] = message.text.replace
            if data['total'] == 'Cancel':
                await state.finish()
                await message.answer('The operation is cancelled.')
                await command_my_records(message)
            else:
                data['total'] = round(float(data['total'](',', '.')), 2)
                await Record_adder.next()
                await message.reply(f"Do you really want to add a record with values:\n\n\
Service: \"{data['name']}\"\n\
Date: {data['year']} {data['month']}\n\
Total sum: {data['total']:.2f}?", reply_markup=yes_no_menu)
        except ValueError:
            await Record_adder.number.set()
            await message.reply(f"You have entered incorrect data!\nEnter only digits, please.", reply_markup=cancel_menu)


async def record_add_confirm(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['confirm'] = message.text
    if data['confirm'] == 'Yes':
        date = f"{data['year']}-{monthes[data['month']]}"
        reply = database_records.add_record(message.from_user.id, data['name'], date, data['total'])
        await message.reply(f"{reply}", reply_markup=records_menu)
        await state.finish()
    elif data['confirm'] == 'No':
        await message.answer('The operation is cancelled.')
        await command_my_records(message)
        await state.finish()
    else:
        await Record_adder.confirmation.set()
        await message.reply(f"You have entered incorrect data!\nUse buttons, please.", reply_markup=yes_no_menu)

async def record_add_stop_edit(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['stopedit'] = message.text
    if data['stopedit'] == 'Stop':
        await message.answer('The operation is cancelled.')
        await state.finish()
        await command_my_records(message)
    elif data['stopedit'] == 'delete the record':
        await message.answer('Do You really want to delete this record?', reply_markup=yes_no_menu)
        await Record_deleter.confirmation.set()
    else:
        await Record_adder.stop_edit.set()
        await message.reply(f"Pick the option.\nUse the button, please!", reply_markup=delete_stop_menu)


""" /delete_record """
class Record_deleter(StatesGroup):
    service_name = State()
    year = State()
    month = State()
    confirmation = State()

async def command_delete_record(message: types.Message):
    await Record_deleter.service_name.set()
    await message.reply('What is the name of expense?', reply_markup=cancel_menu)

async def record_delete_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    if data['name'] == 'Cancel':
        await state.finish()
        await message.answer('The operation is cancelled.')
        await command_my_records(message)
    elif database_records.is_service(message.from_user.id, data['name']):
        await Record_deleter.next()
        await message.reply(f"Pick the year", reply_markup=year_menu)
    else:
        await message.reply(f"You don't have this expense type!\n\nThe operation is cancelled.", reply_markup=records_menu)
        await state.finish()
        await command_my_records(message)

async def record_delete_year(message: types.Message, state: FSMContext):
    years = [2020, 2021, 2022, 2023]
    async with state.proxy() as data:
        try:
            data['year'] = message.text
            if data['year'] == 'Cancel':
                await state.finish()
                await message.answer('The operation is cancelled.')
                await command_my_records(message)
            elif int(data['year']) in years:
                await Record_deleter.next()
                await message.reply(f"Pick the month", reply_markup=monthes_menu)
            else: raise ValueError
        except ValueError:
            await Record_deleter.year.set()
            await message.reply(f"You have entered incorrect data!\nUse buttons, please.", reply_markup=year_menu)

async def record_delete_month(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['month'] = message.text
    if data['month'] == 'Cancel':
        await state.finish()
        await message.answer('The operation is cancelled.')
        await command_my_records(message)
    elif data['month'] in monthes:
        date = f"{data['year']}-{monthes[data['month']]}"
        is_record = database_records.is_record(message.from_user.id, data['name'], date)
        if is_record:
            await message.reply(f"You have this record:\n\nService name: {is_record[0][2]}\n\
Date: {is_record[0][3]}\nAmount: {is_record[0][4]}\nPrice: {is_record[0][5]}\nSumm: {is_record[0][6]}\n\n\
Do You really want to delete this record?", reply_markup=yes_no_menu)
            await Record_deleter.next()
        else:
            await message.reply(f"You don't have such record", reply_markup=records_menu)
            await state.finish()
    else:
        await Record_deleter.month.set()
        await message.reply(f"You have entered incorrect data!\nUse buttons, please.", reply_markup=monthes_menu)

async def record_delete_confirm(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['confirm'] = message.text
    if data['confirm'] == 'Yes':
        date = f"{data['year']}-{monthes[data['month']]}"
        reply = database_records.delete_record(message.from_user.id, data['name'], date)
        await state.finish()
        await message.reply(f"{reply}", reply_markup=records_menu)
        await command_my_records(message)
    elif data['confirm'] == 'No':
        await state.finish()
        await message.answer('The operation is cancelled.')
        await command_my_records(message)
    else:
        await Record_deleter.confirmation.set()
        await message.reply(f"You have entered incorrect data!\nUse buttons, please.", reply_markup=yes_no_menu)


""" the registration of message handlers """

def register_handlers_records(dp : Dispatcher):
    dp.register_message_handler(command_my_records, commands=['Enter_the_total_of_expense'], state=None)
    dp.register_message_handler(command_add_record, commands=['Add_the_total_of_expense'], state=None)
    dp.register_message_handler(record_add_name, state=Record_adder.service_name)
    dp.register_message_handler(record_add_year, state=Record_adder.year)
    dp.register_message_handler(record_add_month, state=Record_adder.month)
    dp.register_message_handler(record_add_total, state=Record_adder.total)
    dp.register_message_handler(record_add_confirm, state=Record_adder.confirmation)
    dp.register_message_handler(record_add_stop_edit, state=Record_adder.stop_edit)
    dp.register_message_handler(command_delete_record, commands=['Delete_the_total_of_expense'], state=None)
    dp.register_message_handler(record_delete_name, state=Record_deleter.service_name)
    dp.register_message_handler(record_delete_year, state=Record_deleter.year)
    dp.register_message_handler(record_delete_month, state=Record_deleter.month)
    dp.register_message_handler(record_delete_confirm, state=Record_deleter.confirmation)