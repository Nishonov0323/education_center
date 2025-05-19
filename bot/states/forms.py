from aiogram.fsm.state import State, StatesGroup

class StudentForm(StatesGroup):
    SUBJECT = State()
    NAME = State()
    PHONE = State()

class TeacherForm(StatesGroup):
    SUBJECT = State()
    NAME = State()
    PHONE = State()

class LeaveForm(StatesGroup):
    DATE = State()
    REASON = State()

class PaymentForm(StatesGroup):
    CHECK = State()