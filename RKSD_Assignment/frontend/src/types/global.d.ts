// Global type declarations

// Extend HTMLElement to include _clickOutside property used by the click-outside directive
declare global {
  interface HTMLElement {
    _clickOutside?: {
      handler: (e: MouseEvent) => void
      exclude: () => HTMLElement[]
    }
  }
}

export {}
