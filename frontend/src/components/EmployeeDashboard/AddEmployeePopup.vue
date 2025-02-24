<template>
	<popup-type-minimal v-if="modelValue" v-bind="$attrs" @close="$emit('update:modelValue', false)">
		<add-employee-form
			v-if="addingEmployee"
			@employeeAdded="showPasswordResetLink"
			:jobsList="jobsList"
		/>
		<employee-password-reset-link v-else :passwordResetLink="passwordResetLink" />
	</popup-type-minimal>
</template>

<script>
import PopupTypeMinimal from '@/components/Popup/TypeMinimal.vue'
import AddEmployeeForm from '@/components/EmployeeDashboard/AddEmployeeForm.vue'
import EmployeePasswordResetLink from '@/components/EmployeeDashboard/EmployeePasswordResetLink.vue'

export default {
	props: ['modelValue'],

	components: {
		PopupTypeMinimal,
		AddEmployeeForm,
		EmployeePasswordResetLink,
	},

	data() {
		return {
			addingEmployee: true,
			passwordResetLink: '',
			jobsList: [],
		}
	},
	methods: {
		showPasswordResetLink(link) {
			this.addingEmployee = false
			this.passwordResetLink = link
		},
	},
}
</script>
