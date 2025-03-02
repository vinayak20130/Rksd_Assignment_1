import type { Directive } from 'vue'

interface ClickOutsideElement extends HTMLElement {
  _clickOutside?: {
    handler: (e: MouseEvent) => void
    exclude: () => HTMLElement[]
  }
}

export const clickOutside: Directive = {
  mounted(el: ClickOutsideElement, binding) {
    el._clickOutside = {
      handler: (e: MouseEvent) => {
        // Get the elements to exclude (like toggle buttons)
        const excludedElements = el._clickOutside?.exclude() || []

        // Check if the click was outside the element and excluded elements
        if (
          !el.contains(e.target as Node) &&
          !excludedElements.some((excludedEl) => excludedEl.contains(e.target as Node))
        ) {
          binding.value(e)
        }
      },
      exclude: () => (binding.arg ? Array.from(document.querySelectorAll(binding.arg)) : []),
    }

    document.addEventListener('click', el._clickOutside.handler, true)
  },

  unmounted(el: ClickOutsideElement) {
    if (el._clickOutside) {
      document.removeEventListener('click', el._clickOutside.handler, true)
      delete el._clickOutside
    }
  },
}
