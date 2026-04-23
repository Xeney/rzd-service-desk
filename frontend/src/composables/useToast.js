import { ref, reactive } from 'vue'

const toasts = reactive([])
let toastId = 0

export function useToast() {
  const add = (options) => {
    const id = ++toastId
    const toast = {
      id,
      type: options.type || 'success',
      title: options.title || '',
      message: options.message || '',
      duration: options.duration || 4000
    }

    toasts.push(toast)

    if (toast.duration > 0) {
      setTimeout(() => {
        remove(id)
      }, toast.duration)
    }

    return id
  }

  const remove = (id) => {
    const index = toasts.findIndex(t => t.id === id)
    if (index !== -1) {
      toasts.splice(index, 1)
    }
  }

  const success = (message, title = 'Успешно') => {
    return add({ type: 'success', title, message })
  }

  const error = (message, title = 'Ошибка') => {
    return add({ type: 'error', title, message, duration: 6000 })
  }

  const warning = (message, title = 'Внимание') => {
    return add({ type: 'warning', title, message })
  }

  return {
    toasts,
    add,
    remove,
    success,
    error,
    warning
  }
}