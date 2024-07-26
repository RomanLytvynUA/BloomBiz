import { useSuppliersStore } from "./suppliers";
import { useCustomersStore } from "./customers";
import { useGoodsStore } from "./goods";
import { useExpensesStore } from "./expenses";
import { useOrdersStore } from "./orders";

export function updateData(data) {
    Object.keys(data).forEach((key) => {
        switch (key) {
            case 'suppliers':
                const suppliersData = useSuppliersStore().suppliersData
                data['suppliers'].forEach((changedSupplier) => {
                    const existing_suppleir = suppliersData.find(supplier => supplier.id === changedSupplier.id)

                    // Determine if new supplier was created or existing one was edited
                    if (existing_suppleir) {
                        Object.keys(changedSupplier).forEach((changedSupplierProperty) => {
                            existing_suppleir[changedSupplierProperty] = changedSupplier[changedSupplierProperty]
                        })
                    } else {
                        useSuppliersStore().suppliersData.unshift(changedSupplier)
                    }
                })

                break;
            case 'customers':
                const customersData = useCustomersStore().customersData
                data['customers'].forEach((changedCustomer) => {
                    let existing_customer = customersData.find(customer => customer.id === changedCustomer.id)

                    // Determine if new customer was created or existing one was edited
                    if (existing_customer) {
                        Object.keys(changedCustomer).forEach((changedCustomerProperty) => {
                            existing_customer[changedCustomerProperty] = changedCustomer[changedCustomerProperty]
                        })
                    } else {
                        useCustomersStore().customersData.unshift(changedCustomer)
                    }
                })

                break;
            case 'goods':
                const goodsData = useGoodsStore().goodsData
                data['goods'].forEach((changedProduct) => {
                    // Add category placeholder if category of product is missing
                    const existing_category = goodsData.find(category => category.id === changedProduct.category)
                    if (!existing_category) {
                        useGoodsStore().goodsData.push({ id: changedProduct.category })
                        existing_category = goodsData.find(category => category.id === changedProduct.category)
                    }

                    // Determine if new product was created or existing one was edited
                    const existing_product = existing_category.goods.find(product => product.id === changedProduct.id)
                    if (existing_product) {
                        Object.keys(changedProduct).forEach((changedProductProperty) => {
                            existing_product[changedProductProperty] = changedProduct[changedProductProperty]
                        })
                    } else {
                        existing_category.goods.push(changedProduct)
                    }
                })

                break;
            case 'categories':
                const categoriesData = useGoodsStore().goodsData
                data['categories'].forEach((changedCategory) => {
                    const existing_category = categoriesData.find(category => category.id === changedCategory.id)

                    // Determine if new category was created or existing one was edited
                    if (existing_category) {
                        Object.keys(changedCategory).forEach((changedCategoryProperty) => {
                            existing_category[changedCategoryProperty] = changedCategory[changedCategoryProperty]
                        })
                    } else {
                        useGoodsStore().goodsData.push(changedCategory)
                    }
                })

                break;
            case 'expenses':
                const expensesData = useExpensesStore().expensesData
                data['expenses'].forEach((changedExpense) => {
                    const existing_expense = expensesData.find(expense => expense.id === changedExpense.id)

                    // Determine if new expense was created or existing one was edited
                    if (existing_expense) {
                        Object.keys(changedExpense).forEach((changedExpenseProperty) => {
                            existing_expense[changedExpenseProperty] = changedExpense[changedExpenseProperty]
                        })
                    } else {
                        useExpensesStore().expensesData.unshift(changedExpense);
                    }
                })

                break;
            case 'orders':
                const ordersData = useOrdersStore().ordersData
                data['orders'].forEach((changedOrder) => {
                    const existing_order = ordersData.find(order => order.id === changedOrder.id)

                    // Determine if new expense was created or existing one was edited
                    if (existing_order) {
                        Object.keys(changedOrder).forEach((changedOrderProperty) => {
                            existing_order[changedOrderProperty] = changedOrder[changedOrderProperty]
                        })
                    } else {
                        useOrdersStore().ordersData.unshift(changedOrder);
                    }
                })

                break;
            default:
                break;
        }
    })
}

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