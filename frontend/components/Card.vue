<script setup>
defineProps({
  title: {
    type: String,
    default: ''
  },
  subtitle: {
    type: String,
    default: ''
  },
  hoverable: {
    type: Boolean,
    default: false
  }
})
</script>

<template>
  <div
    class="bg-white rounded-lg shadow-md overflow-hidden h-full"
    :class="{ 'transition-transform hover:shadow-lg hover:-translate-y-1 cursor-pointer': hoverable }"
  >
    <div class="p-5">
      <h3 v-if="title" class="text-lg font-semibold text-gray-900 mb-2">{{ title }}</h3>
      <p v-if="subtitle" class="text-sm text-gray-500 mt-1 mb-2">{{ subtitle }}</p>
      <div class="mt-3">
        <slot />
      </div>
    </div>
    <div v-if="$slots.footer" class="px-5 py-4 bg-gray-50 border-t border-gray-100">
      <slot name="footer" />
    </div>
  </div>
</template> 