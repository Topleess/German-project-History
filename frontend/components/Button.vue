<script setup>
defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'secondary', 'outline', 'danger'].includes(value)
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg'].includes(value)
  },
  type: {
    type: String,
    default: 'button'
  },
  disabled: {
    type: Boolean,
    default: false
  }
})

const variantClasses = {
  primary: 'bg-primary-600 hover:bg-primary-700 text-white',
  secondary: 'bg-secondary-200 hover:bg-secondary-300 text-secondary-900',
  outline: 'bg-transparent hover:bg-gray-100 text-gray-700 border border-gray-300',
  danger: 'bg-red-600 hover:bg-red-700 text-white'
}

const sizeClasses = {
  sm: 'py-1 px-2 text-sm',
  md: 'py-2 px-4 text-base',
  lg: 'py-3 px-6 text-lg'
}
</script>

<template>
  <button
    :type="type"
    :disabled="disabled"
    :class="[
      'rounded-md font-medium focus:outline-none focus:ring-2 focus:ring-offset-2 transition-colors',
      variantClasses[variant],
      sizeClasses[size],
      disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'
    ]"
  >
    <slot />
  </button>
</template> 