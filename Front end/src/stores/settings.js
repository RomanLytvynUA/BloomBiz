import { ref } from 'vue'
import { defineStore } from 'pinia'
import { urlList } from '../config'
import { useGoodsStore } from './goods'
import { useAuthStore } from './auth'

export const useSettingsStore = defineStore('settings', () => {
    const settingsData = ref({})

    async function fetchSettings() {
        try {
            const response = await fetch(urlList.getSettings, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${useAuthStore().jwt_token}`,
                }
            })
            if (!response.ok) {
                useAuthStore().logout()
            } else {
                const data = await response.json()
                settingsData.value = data
            }
        } catch (error) {
            console.error('Error fetching settings:', error)
        }
    }

    async function resetSettings(json) {
        const response = await fetch(urlList.resetSettings, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${useAuthStore().jwt_token}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(json),
        })

        if (!response.ok) {
            useAuthStore().logout()
        } else {
            fetchSettings();
            useGoodsStore().fetchGoods();
        }
    }

    async function editSettings(json) {
        const response = await fetch(urlList.editSettings, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${useAuthStore().jwt_token}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(json),
        })

        if (!response.ok) {
            useAuthStore().logout()
        } else {
            fetchSettings();
            if (Object.keys(json).includes('defaultMargin')) {
                useGoodsStore().fetchGoods();
            }
        }
    }


    return { settingsData, fetchSettings, resetSettings, editSettings }
})
