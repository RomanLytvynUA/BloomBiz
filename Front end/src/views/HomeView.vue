<template>
    <br>
    <div class="container-fluid text-center">
        <div id="logo">
            <img src="../assets/logo.png" width="190" class="img-fluid mx-auto d-block" alt="логотип">
            <figure style="margin-bottom: 0px;">
                <blockquote class="blockquote">
                    <h1>Ласкаво просимо до BloomBiz.</h1>
                </blockquote>
                <figcaption class="blockquote-footer" style="margin-bottom: 0px;">
                    Коли творчість важливіше за паперову роботу.
                </figcaption>
            </figure>
        </div>
    </div>

    <div v-if="!useAuthStore().isAuthenticated" class="text-center">
        <br>
        <div class=" d-flex justify-content-center">
            <RouterLink to="/signin">
                <button class="btn btn-success btn-lg">Почати</button>
            </RouterLink>
        </div>
    </div>

    <section id="about" class="py-5">
        <div class="container">
            <h2 class="text-center">Про нас</h2>
            <p class="text-center">Ласкаво просимо до BloomBiz - комплексного рішення для управління квітковим бізнесом.
                Ми допоможемо вам вирішити виклики у квітковому бізнесі, щоб ви могли досягти успіху на ринку.
                Розраховуйте на нас для оптимізації квіткового магазину!</p>
            <p class="text-center">У BloomBiz ми бачимо можливість для росту кожного квіткового магазину. Наша мета -
                спростити складні завдання, щоб ви могли зосередитися на справді важливому - створенні блискусих
                композицій. Працюйте з нами для досягнення найкращого у квітковій справі!</p>
        </div>
    </section>

    <section id="features" class="bg-light py-5">
        <div class="container">
            <h2 class="text-center">Особливості</h2>
            <div class="row d-flex justify-content-center mt-4 mb-4">
                <div class="col-lg-6">
                    <div class="card">
                        <ul class="list-group list-group-flush">
                            <li v-for="feature in features" class="list-group-item d-flex align-items-center">
                                <div>
                                    <p style="margin-bottom: 5px;"><b>{{ feature.title }}</b></p>
                                    <p class="mb-0 text-muted">{{ feature.description }}</p>
                                </div>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>

<script setup>
import { useAuthStore } from '../stores/auth'

const features = [
    {
        title: 'Всебічний функціонал',
        description: 'BloomBiz — це багатофункціональний інструмент, який забезпечує доступ до всіх необхідних функцій у одному місці.'
    },
    {
        title: 'Зрозумілий інтерфейс',
        description: 'Простий та інтуїтивно зрозумілий інтерфейс, що дозволяє легко використовувати необхідні функції без зайвих зусиль.'
    },
    {
        title: 'Контроль фінансів',
        description: 'Зручні інструменти для ведення обліку грошового потоку крамниці. Відстежуйте свої витрати та прибуток, \
        аналізуйте фінансові потоки і плануйте свої витрати ефективно.'
    },
    {
        title: 'Облік товарів',
        description: 'Ефективний інструмент для контролю наявністі та цін товарів. Ведіть детальний облік товарного \
        запасу, зручно аналізуйте й плануйте закупки, усі дані доступні в одному місці.'
    },
    {
        title: 'Динамічні графіки',
        description: 'Автоматично створені графіки, що відображають стан вашої крамниці. Легко аналізуйте дані про продажі, запаси та інші показники.'
    },
    {
        title: 'Данні клієнтів',
        description: 'Зручний спосіб зберігання інформації про клієнтів для повторного використання.'
    },
]
</script>