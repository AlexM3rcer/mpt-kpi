<template>
	<div class="employee-password-reset">
		<h2 class="widget-title">Сотрудник<br />успешно добавлен!</h2>
		<label class="copy-link-label">
			<span>Ссылка на смену пароля:</span>
			<div class="copy-link">
				<input
					class="input"
					type="text"
					placeholder="Здесь должна быть ссылка на смену пароля"
					:value="passwordResetLink"
					disabled
				/>
				<div class="copy-icon" @click="copyLink">
					<copy-icon />
				</div>
			</div>
		</label>
		<button class="button" @click="saveData">Продолжить</button>
	</div>
</template>

<script>
import CopyIcon from '@/components/Icons/CopyIcon.vue'

export default {
	props: ['passwordResetLink'],

	components: {
		CopyIcon,
	},

	methods: {
		copyLink() {
			navigator.clipboard.writeText(this.passwordResetLink)
		},
	},
}
</script>

<style lang="sass" scoped>
.employee-password-reset {
    display: flex;
    flex-direction: column;
  	align-items: center;

    background-color: white;
    min-width: 30em;
    min-height: 20em;
    border-radius: 1em;

    padding: 2em 1.9em;
	text-align: center;

	gap: 1.5em;
}

.widget-title {
    color: var(--primary-blue);
    font-size: 1.6em;
    line-height: 2em;
    font-variation-settings: "wght" 600;
    font-weight: 600;
}

.input {
	width: 100%
}

.button {
    width: fit-content;
    color: white;
    padding: 0.5em 1.8em;
    font-size: 1em;
    font-variation-settings: "wght" 600;
    font-weight: 600;
    background-color: var(--primary-blue);
    border-radius: 0.4em;
    border-style: hidden;
}

.copy-link {
	margin-top: 0.5em;
	display: flex;
	flex-direction: row;
	gap: 1em;
}

.copy-icon {
	height: 100%;
	min-height: 2em;
	min-width: 2em;
	background-color: var(--accent-blue);
	border-radius: 0.625rem;
	display: flex;
  	align-items: center;
  	justify-content: center;
}

.copy-icon:hover {
	cursor: pointer;
	background-color: var(--primary-blue);
}

.copy-link-label {
	width: 100%;
}
</style>
