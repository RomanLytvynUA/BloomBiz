const BASE_URL = 'http://127.0.0.1:5000/';

export const urlList = {
    "login": BASE_URL + "auth/login",
    "register": BASE_URL + "auth/register",

    "getSuppliers": BASE_URL + "suppliers/get",
    "delSupplier": BASE_URL + "suppliers/delete/",
    "addSupplier": BASE_URL + "suppliers/create",
    "editSupplier": BASE_URL + "suppliers/edit",

    "getCustomers": BASE_URL + "customers/get",
    "delCustomer": BASE_URL + "customers/delete/",
    "addCustomer": BASE_URL + "customers/create",
    "editCustomer": BASE_URL + "customers/edit",

    "getGoods": BASE_URL + "goods/get",
    "addProduct": BASE_URL + "goods/create_product",
    "editProduct": BASE_URL + "goods/edit_product",
    "delProduct": BASE_URL + "goods/delete_product",
    "addCategory": BASE_URL + "goods/create_category",
    "editCategory": BASE_URL + "goods/edit_category",
    "delCategory": BASE_URL + "goods/delete_category",
    "setProductPrice": BASE_URL + "goods/edit_price",
    "resetProductPrices": BASE_URL + "goods/reset_prices",
    "getInStockGoods": BASE_URL + "goods/get_instock",
    "addDecommission": BASE_URL + "goods/create_decommission",

    "getExpenses": BASE_URL + "expenses/get",
    "addExpense": BASE_URL + "expenses/create",
    "editExpense": BASE_URL + "expenses/edit",
    "delExpense": BASE_URL + "expenses/delete/",

    "getSettings": BASE_URL + "settings/get",
    "editSettings": BASE_URL + "settings/edit",
    "resetSettings": BASE_URL + "settings/reset",

    "getOrders": BASE_URL + "orders/get",
    "addOrder": BASE_URL + "orders/create",
    "editOrder": BASE_URL + "orders/edit",
    "delOrder": BASE_URL + "orders/delete/",
}