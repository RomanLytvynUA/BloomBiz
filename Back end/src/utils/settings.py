from .. import db
from ..models.settings import Settings


default_settings = {
    'ordersSafetyMode': True,
    'ordersHideOutOfStock': True,
    'ordersGoodsToIgnore': [],
    'ordersStatuses': ["Продано", "Списано", "Чорнетка", "Вітрина"],

    'expensesSafetyMode': True,
    'expensesSuppliersToIgnore': [],
    'expensesGoodsToIgnore': [],

    'goodsSafetyMode': True,
    'defaultMargin': 120,
 
    'suppliersSafetyMode': True,
}


available_settings = [
    'ordersSafetyMode',
    'ordersHideOutOfStock',
    'ordersGoodsToIgnore',
    'ordersStatuses',
    'expensesSafetyMode',
    'expensesSuppliersToIgnore',
    'expensesGoodsToIgnore',
    'goodsSafetyMode',
    'defaultMargin',
    'suppliersSafetyMode',
]


multiple_options_settings = [
    'ordersGoodsToIgnore',
    'ordersStatuses',
    'expensesSuppliersToIgnore',
    'expensesGoodsToIgnore',
]


def util_set_settings(name, value):
    if name in available_settings:
        if type(value) is list:
            # Delete old options
            for option in Settings.query.filter_by(name=name):
                db.session.delete(option)
            # Add new options
            for option in value:
                new_option = Settings(name=name, value=option)
                db.session.add(new_option)
        else:
            option = Settings.query.filter_by(name=name).all()
            if not len(option):
                new_option = Settings(name=name, value=value)
                db.session.add(new_option)
            else:    
                option[0].value = value
                db.session.add(option[0])
        db.session.commit()

        return {'message': 'Added setting successfuly.'}
    else:
        return {'message': 'Invalid setting name.'}


def util_reset_settings():
    for name, value in default_settings.items():
        util_set_settings(name, value)


def util_generate_settings_dict():
    dict = {}
    for setting in available_settings:
        setting_data = Settings.query.filter_by(name=setting).all()
        if setting in multiple_options_settings:
            dict[setting] = [option.value for option in setting_data]
        else:
            dict[setting] = setting_data[0].value
    return dict
