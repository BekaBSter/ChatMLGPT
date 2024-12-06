from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from Settings import DEBUG, out
from aiogram import Router, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import main_keyboards as main_kb
import Database

router = Router()


class Registration(StatesGroup):
    first_name = State()


class Promo(StatesGroup):
    promocode = State()


# Начало работы с ботом посредством команды Start
@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.delete()
    user_id = str(message.from_user.id)
    first_name = message.from_user.first_name
    isSearch = Database.search_user(user_id)
    if isSearch:
        await message.answer("Привет! Мы знакомы!", reply_markup=main_kb.main_menu)
    else:
        await message.answer("Привет! Давай познакомимся! Введи свое имя.")
        await state.set_state(Registration.first_name)
    if DEBUG:
        out("Бот: Успешно выполнен обработчик команды /start. "
            f"Пользователь: {first_name}. "
            f"User ID: {user_id}.", "g")


@router.message(Command("promocode"))
async def promo(message: Message, state: FSMContext):
    await state.set_state(Promo.promocode)
    await message.answer("Введите промокод")


@router.message(Promo.promocode)
async def enter_promo(message: Message, state: FSMContext):
    await state.update_data(promocode=message.text)
    user_id = message.from_user.id
    data = await state.get_data()
    promocode = data["promocode"]
    await state.clear()
    isSearch, sum, uses = Database.search_promocode(promocode)
    if isSearch:
        if user_id not in uses:
            balance = Database.get_balance_user(user_id)
            balance += sum
            Database.update_balance(user_id, balance)
            uses.append(user_id)
            Database.update_uses_promocode(promocode, uses)
            await message.answer(f"Промокод найден, сумма {sum} рублей зачислена на ваш счет!")
        else:
            await message.answer(f"Промокод уже был использован!")
    else:
        await message.answer("Промокод не найден!")


@router.message(Registration.first_name)
async def reg_name(message: Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await message.answer("Регистрация завершена!", reply_markup=main_kb.main_menu)
    data = await state.get_data()
    await state.clear()
    user_id = str(message.from_user.id)
    Database.new_user(user_id, data["first_name"])
    out(f"Бот: Регистрация нового пользователя. User_id: {user_id}", "g")


@router.message(F.text.in_({"Выбор нейросети", "Профиль", "Контакты"}))
async def main_menu(message: Message):
    await message.delete()
    if message.text == "Выбор нейросети":

        await message.answer("Выберите нейросеть:", reply_markup=main_kb.change_neuro)

    elif message.text == "Профиль":

        await message.answer("Профиль")

    elif message.text == "Контакты":

        await message.answer("Контакты")

    first_name = message.from_user.first_name
    user_id = message.from_user.id
    out(f"Бот: успешно выполнен обработчик текста. "
        f"Пользователь: {first_name}. "
        f"User_id: {user_id}", "g")


@router.callback_query(F.data.startswith("neuro_"))
async def change_neuro(callback: CallbackQuery):
    await callback.message.delete()
    neuro = callback.data.split("_")[1]
    await callback.message.answer(f"Выбрана нейросеть {neuro}. Введите для нее ваш запрос.")
    first_name = callback.message.from_user.first_name
    user_id = callback.message.chat.id
    Database.update_neuro_user(user_id, neuro)
    out(f"Бот: успешно выполнен обработчик обратного вызова. "
        f"Пользователь: {first_name}. "
        f"User_id: {user_id}", "g")


@router.message(F.text)
async def request(message: Message, state: FSMContext):
    await message.delete()
    user_id = message.from_user.id
    isSearch = Database.search_user(user_id)
    if isSearch:
        neuro = Database.get_neuro_user(user_id)
        balance = Database.get_balance_user(user_id)
        if neuro is not None:
            if balance < 0.5:
                await message.answer(f"Недостаточно средств!")
            else:
                balance -= 0.5
                Database.update_balance(user_id, balance)
                await message.answer(f"Вы выполнили запрос к нейросети {neuro}: {message.text}")
        else:
            await message.answer("Выберите нейросеть:", reply_markup=main_kb.change_neuro)
    else:
        await message.answer("Привет! Давай познакомимся! Введи свое имя.")
        await state.set_state(Registration.first_name)
