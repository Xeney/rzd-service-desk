<template>
  <router-link :to="`/tickets/${ticket.id}`" class="ticket-card">
    <div class="ticket-card-inner">
    <div class="ticket-card-header">
      <span class="ticket-id">#{{ String(ticket.id).padStart(4, '0') }}</span>
      <div class="ticket-badges">
        <span :class="['badge', `badge-${ticket.priority}`]">
          {{ priorities[ticket.priority] }}
        </span>
        <span :class="['badge', `badge-${ticket.status}`]">
          {{ statuses[ticket.status] }}
        </span>
      </div>
    </div>

    <h3 class="ticket-title">{{ ticket.title }}</h3>

    <p v-if="ticket.description" class="ticket-description">
      {{ ticket.description }}
    </p>

    <div class="ticket-card-footer">
      <div class="ticket-meta">
        <span class="ticket-type">
          <i class="fas" :class="typeIcons[ticket.type]"></i>
          {{ types[ticket.type] }}
        </span>
        <span class="ticket-date">
          <i class="fas fa-calendar"></i>
          {{ formatDate(ticket.created_at) }}
        </span>
      </div>

      <div v-if="ticket.assigned_to" class="ticket-assignee">
        <i class="fas fa-user-check"></i>
        {{ ticket.assigned_to.full_name?.split(' ').slice(0, 2).join(' ') }}
      </div>
    </div>

    <div v-if="ticket.created_by && showCreator" class="ticket-creator">
      <i class="fas fa-user"></i>
      {{ ticket.created_by.full_name }}
    </div>
    </div>
  </router-link>
</template>

<script setup>
defineProps({
  ticket: {
    type: Object,
    required: true
  },
  showCreator: {
    type: Boolean,
    default: false
  }
})

const priorities = {
  low: 'Низкий',
  normal: 'Обычный',
  high: 'Высокий',
  critical: 'Критический'
}

const statuses = {
  new: 'Новая',
  in_progress: 'В работе',
  closed: 'Закрыта',
  rejected: 'Отклонена'
}

const types = {
  equipment: 'Оборудование',
  software: 'ПО',
  access: 'Доступ'
}

const typeIcons = {
  equipment: 'fa-laptop',
  software: 'fa-desktop',
  access: 'fa-key'
}

const formatDate = (date) => {
  if (!date) return ''
  const d = new Date(date)
  const now = new Date()
  const diff = now - d
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))

  if (days === 0) return 'Сегодня'
  if (days === 1) return 'Вчера'
  if (days < 7) return `${days} дн. назад`

  return d.toLocaleDateString('ru-RU', { day: 'numeric', month: 'short' })
}
</script>

<style scoped>
.ticket-card {
  display: block;
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  transition: var(--transition);
  position: relative;
  overflow: hidden;
}

.ticket-card:hover {
  border-color: var(--accent);
  box-shadow: var(--shadow-md);
  transform: translateY(-3px);
}

.ticket-card-inner {
  padding: 20px;
  display: flex;
  flex-direction: column;
  min-height: 180px;
}

.ticket-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
  gap: 12px;
  flex-shrink: 0;
}

.ticket-id {
  font-family: var(--font-mono);
  font-size: 12px;
  font-weight: 500;
  color: var(--text-muted);
  letter-spacing: 0.02em;
}

.ticket-badges {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
  justify-content: flex-end;
  flex-shrink: 0;
}

.ticket-title {
  font-size: 15px;
  font-weight: 600;
  line-height: 1.4;
  margin-bottom: 8px;
  color: var(--text-primary);
  flex-shrink: 0;
}

.ticket-description {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.5;
  margin-bottom: 16px;
  flex: 1;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  word-wrap: break-word;
}

.ticket-card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 12px;
  border-top: 1px solid var(--border);
  gap: 12px;
  flex-shrink: 0;
  margin-top: auto;
}

.ticket-meta {
  display: flex;
  gap: 12px;
  font-size: 12px;
  color: var(--text-muted);
  flex-wrap: wrap;
}

.ticket-type,
.ticket-date {
  display: flex;
  align-items: center;
  gap: 5px;
}

.ticket-type i,
.ticket-date i {
  font-size: 11px;
}

.ticket-assignee {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 12px;
  color: var(--success);
  background: var(--success-light);
  padding: 4px 10px;
  border-radius: var(--radius-full);
  flex-shrink: 0;
}

.ticket-creator {
  position: absolute;
  bottom: 12px;
  right: 12px;
  font-size: 11px;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  gap: 4px;
}

@media (max-width: 640px) {
  .ticket-card-footer {
    flex-direction: column;
    align-items: flex-start;
  }

  .ticket-card {
    min-height: auto;
  }

  .ticket-badges {
    order: -1;
    width: 100%;
    justify-content: flex-start;
  }
}
</style>