const BASE_URL = 'http://127.0.0.1:5000/';

export const urlList = {
    "getSuppliers": BASE_URL+"suppliers/get",
    "delSupplier": BASE_URL+"suppliers/delete/",
    "addSupplier": BASE_URL+"suppliers/create",
    "editSupplier": BASE_URL+"suppliers/edit",

    "getGoods": BASE_URL+"goods/get",
    "setProductPrice": BASE_URL+"goods/edit_price",
    "getInStockGoods": BASE_URL+"goods/get_instock",
    "addDecommission": BASE_URL+"goods/create_decommission",

    "getExpenses": BASE_URL+"expenses/get",
    "addExpense": BASE_URL+"expenses/create",
    "editExpense": BASE_URL+"expenses/edit",
    "delExpense": BASE_URL+"expenses/delete/",
    
    "getOrders": BASE_URL+"orders/get",
    "addOrder": BASE_URL+"orders/create",
    "editOrder": BASE_URL+"orders/edit",
    "delOrder": BASE_URL+"orders/delete/",
}