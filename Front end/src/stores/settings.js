import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { urlList } from '../config'
import { useGoodsStore } from './goods'

export const useSettingsStore = defineStore('settings', () => {
    const settingsData = ref({})

    async function fetchSettings() {
        try {
            const response = await fetch(urlList.getSettings)
            const data = await response.json()
            settingsData.value = data
        } catch (error) {
            console.error('Error fetching settings:', error)
        }
    }

    async function resetSettings(json) {
        const response = await fetch(urlList.resetSettings, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(json),
        })

        fetchSettings();
    }

    async function editSettings(json) {
        const response = await fetch(urlList.editSettings, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(json),
        })

        fetchSettings();
    }


    return { settingsData, fetchSettings, resetSettings, editSettings }
})
