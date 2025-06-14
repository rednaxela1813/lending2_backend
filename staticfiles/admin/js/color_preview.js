document.addEventListener('DOMContentLoaded', function () {
  const inputs = document.querySelectorAll('.color-preview')

  inputs.forEach((input) => {
    // 👉 Принудительно делаем input пипеткой
    input.setAttribute('type', 'color')

    // ✅ Превью цветного квадрата (рядом)
    const preview = document.createElement('span')
    preview.style.display = 'inline-block'
    preview.style.width = '24px'
    preview.style.height = '24px'
    preview.style.marginLeft = '8px'
    preview.style.border = '1px solid #ccc'
    preview.style.verticalAlign = 'middle'
    preview.style.backgroundColor = input.value

    // 🔁 Обновляем цвет при изменении
    input.addEventListener('input', () => {
      preview.style.backgroundColor = input.value
    })

    // 🧩 Вставляем после input
    input.parentNode.appendChild(preview)
  })
})
