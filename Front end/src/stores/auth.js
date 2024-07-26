import { ref } from 'vue';
import { defineStore } from 'pinia';
import { urlList } from './general';

export const useAuthStore = defineStore('auth', () => {
    const isAuthenticated = ref(Boolean(localStorage.getItem('jwt')));
    const jwt_token = ref(localStorage.getItem('jwt'));

    const login = async (username, password) => {
        try {
            const response = await fetch(urlList.login, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
            });

            if (!response.ok) {
                logout()

                return 1;
            } else {
                const data = await response.json();
                localStorage.setItem('jwt', data.token);
                jwt_token.value = localStorage.getItem('jwt');
                isAuthenticated.value = true;

                return 0;
            }

        } catch (error) {
            console.log('Login error:', error.message);
            // console.error(error);

            isAuthenticated.value = false;
            localStorage.removeItem('jwt');

            return 1;
        }
    };

    const register = async (json) => {
        try {
            const response = await fetch(urlList.register, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(json)
            });

            if (!response.ok) {
                logout()

                return 1;
            } else {
                const data = await response.json();
                localStorage.setItem('jwt', data.token);
                jwt_token.value = localStorage.getItem('jwt');
                isAuthenticated.value = true;

                return 0;
            }
        } catch (error) {
            console.log('Registration error:', error.message);

            isAuthenticated.value = false;
            localStorage.removeItem('jwt');

            return 1;
        }
    };

    const logout = () => {
        localStorage.removeItem('jwt');
        jwt_token.value = localStorage.getItem('jwt');;
        isAuthenticated.value = false;
    };

    return { login, logout, register, jwt_token, isAuthenticated };
});