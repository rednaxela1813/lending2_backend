/** @type {import('tailwindcss').Config} */

module.exports = {
  content: [
    './backend_templates/**/*.html',
  ],
  safelist: [
  'bg-navbar',
  'bg-footer',
  'bg-body',
  'bg-primary',
  'hover:bg-primary-hover',
  'bg-background',
  'text-text',
  'text-primary',
  'text-secondary-text',
  'hover:text-primary',
  'hover:text-hover',
  'border-border',
  'hover:border-hover',
],

  theme: {
    extend: {},
  },
  plugins: [],
}
