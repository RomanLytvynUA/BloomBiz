<template>
	<div class="container" style="margin-top: 2%">
		<div class="row">
			<div class="col-sm-10 col-md-8 col-lg-6 mx-auto d-table">
				<div class="d-table-cell align-middle">
					<div class="card">
						<div class="card-body">
							<div class="m-sm-4" style="margin-top: 0 !important; margin-bottom: 0 !important">
								<div class="text-center mt-4" style="margin-top: 1% !important">
									<h2>{{ !registration ? t('auth.login.title') : t('auth.registration.title') }}</h2>
									<p class="lead" style="margin-bottom: 1%">
										{{ !registration ? t('auth.login.description') :
										t('auth.registration.description') }}
									</p>
									<small @click.prevent="registration = !registration; alert = ''; reset()">
										<a href="">{{ !registration ? t('auth.login.suggestion') :
										t('auth.registration.suggestion') }}</a>
									</small>
								</div>
								<br>
								<div v-if="alert.length" class="alert alert-danger" role="alert">{{ alert[0].value }}
								</div>
								<form id="login-form" v-if="!registration" @keyup.enter="login()">
									<div class="form-group mb-3">
										<label>{{ t('auth.login.fields.nameLabel') }}</label>
										<input class="form-control" type="text" name="username"
											:placeholder="t('auth.login.fields.namePlaceholder')">
									</div>
									<div class="form-group mb-3">
										<label>{{ t('auth.login.fields.passwordLabel') }}</label>
										<input class="form-control" type="password" name="password"
											:placeholder="t('auth.login.fields.passwordPlaceholder')">
									</div>
								</form>
								<form id="registration-form" v-if="registration" @keyup.enter="register()">
									<div class="form-group mb-3">
										<label>{{ t('auth.registration.fields.nameLabel') }}</label>
										<input class="form-control" autocomplete="off" type="text" name="username"
											:placeholder="t('auth.registration.fields.namePlaceholder')">
									</div>
									<div class="form-group mb-3">
										<label>{{ t('auth.registration.fields.passwordLabel') }}</label>
										<input style="border-bottom-left-radius: 0px; border-bottom-right-radius: 0px;"
											v-model="registrationPassword" class="form-control" autocomplete="off"
											type="password" name="password"
											:placeholder="t('auth.registration.fields.passwordPlaceholder')">
										<div style="border-top-left-radius: 0px; border-top-right-radius: 0px; border-top: 0px"
											class="card">
											<ul style="margin-top: 1%; margin-bottom: 1%;">
												<li
													:style="registrationPassword.length ? (registrationPassword.length >= 8 ? 'color: green' : 'color: red') : 'color: black'">
													{{ t('auth.registration.passwordRules.length') }}</li>
												<li
													:style="registrationPassword.length ? (/\p{Lu}/u.test(registrationPassword) ? 'color: green' : 'color: red') : 'color: black'">
													{{ t('auth.registration.passwordRules.capitalLetter') }}</li>
												<li
													:style="registrationPassword.length ? (/\p{Ll}/u.test(registrationPassword) ? 'color: green' : 'color: red') : 'color: black'">
													{{ t('auth.registration.passwordRules.smallLetter') }}</li>
												<li
													:style="registrationPassword.length ? (/\d/.test(registrationPassword) ? 'color: green' : 'color: red') : 'color: black'">
													{{ t('auth.registration.passwordRules.digit') }}</li>
											</ul>
										</div>
									</div>
									<div class="form-group mb-3">
										<label>{{ t('auth.registration.fields.confirmPasswordLabel') }}
											<span v-show="registrationPassword !== registrationPasswordVerification"
												class="badge text-bg-danger">{{
										t('auth.registration.fields.differsTag')
									}}</span>
											<span
												v-show="registrationPassword !== '' && (registrationPassword === registrationPasswordVerification)"
												class="badge text-bg-success">{{
										t('auth.registration.fields.matchesTag')
									}}</span>
										</label>
										<input v-model="registrationPasswordVerification" class="form-control"
											autocomplete="off" type="password" name="verify-password"
											:placeholder="t('auth.registration.fields.confirmPasswordPlaceholder')">
									</div>
									<div class="form-group mb-3">
										<label>{{ t('auth.registration.fields.codeLabel') }}</label>
										<input class="form-control" autocomplete="off" type="text" name="code"
											:placeholder="t('auth.registration.fields.codePlaceholder')">
									</div>
								</form>
								<div class="text-center">
									<button v-if="!registration" class="btn btn-success" @click.prevent="login()">{{
										t('auth.login.fields.btnText') }}</button>
									<button v-if="registration" class="btn btn-success" @click.prevent="register()">{{
										t('auth.registration.fields.btnText') }}</button>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '../stores/auth';

import { useI18n } from 'vue-i18n';
const { t } = useI18n();

const alert = ref([])
const loginErrorText = computed(() => t('auth.errors.authFailed'))
const registrationErrorText = computed(() => t('auth.errors.registrationFailed'))

const registration = ref(false)

const registrationPassword = ref('')
const registrationPasswordVerification = ref('')

async function reset() {
	$('#login-form')[0]?.reset()
	$('#registration-form')[0]?.reset()
	alert.value = [];
	registrationPassword.value = '';
	registrationPasswordVerification.value = '';
}

async function login() {
	alert.value = [];
	const form = $('#login-form')[0]
	let valid = true

	// add 'is-invalid' class to every element of <form> where there is no value
	for (const element of form.elements) {
		if (element.tagName === 'INPUT' && !element.value) {
			element.classList.add('is-invalid');
			valid = false
		} else {
			element.classList.remove('is-invalid');
		}
	}

	if (valid) {
		const userData = new FormData(form)

		const resut = await useAuthStore().login(userData.get('username'), userData.get('password'))

		switch (resut) {
			case 0:
				form.reset();
				break;
			case 1:
				alert.value.push(loginErrorText)
				break;
			default:
				break;
		}
	}
}

async function register() {
	alert.value = [];
	const form = $('#registration-form')[0]
	let valid = true

	// add 'is-invalid' class to every element of <form> where there is no value
	for (const element of form.elements) {
		if (element.tagName === 'INPUT' && !element.value) {
			element.classList.add('is-invalid');
			valid = false
		} else {
			element.classList.remove('is-invalid');
		}
	}

	// validate password
	if (registrationPassword.value !== registrationPasswordVerification.value) {
		valid = false;
	}
	if (registrationPassword.value.length < 8 || !/\p{Lu}/u.test(registrationPassword.value)
		|| !/\p{Ll}/u.test(registrationPassword.value) || !/\d/.test(registrationPassword.value)) {
		valid = false;
	}

	if (valid) {
		const userData = new FormData(form)

		const resut = await useAuthStore().register({ username: userData.get('username'), password: userData.get('password'), code: userData.get('code') })

		switch (resut) {
			case 0:
				form.reset();
				break;
			case 1:
				alert.value.push(registrationErrorText)
				break;
			default:
				break;
		}
	}

}
</script>

<style scoped>
label {
	margin-bottom: 1%;
}

input:focus {
	outline: none !important;
	border-color: #dee2e6;
	box-shadow: none !important;
}

.card {
	border-color: #DEE2E6;
}
</style>