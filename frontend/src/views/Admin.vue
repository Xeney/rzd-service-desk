<template>
  <div>
    <header class="header">
      <div class="container header-inner">
        <router-link to="/" class="logo">
          <span>Р</span><span>Ж</span><span>Д</span>
        </router-link>

        <nav class="nav">
          <router-link to="/" class="nav-link">Главная</router-link>
          <router-link to="/tickets" class="nav-link">Все заявки</router-link>
          <router-link to="/my-tickets" class="nav-link">Мои заявки</router-link>
        </nav>

        <div class="user-menu">
          <router-link to="/tickets/new" class="btn btn-primary">
            <i class="fas fa-plus"></i>
            Новая заявка
          </router-link>

          <div class="dropdown">
            <button class="user-avatar" @click="showMenu = !showMenu">
              {{ userInitials }}
            </button>

            <div v-if="showMenu" class="dropdown-menu">
              <div class="dropdown-header">
                <div class="dropdown-user-name">{{ authStore.user?.full_name }}</div>
                <div class="dropdown-user-role">{{ userRoles[authStore.user?.role] }}</div>
              </div>
              <router-link to="/profile" class="dropdown-item" @click="showMenu = false">
                <i class="fas fa-user"></i>
                Профиль
              </router-link>
              <router-link to="/admin" class="dropdown-item dropdown-item-active" @click="showMenu = false">
                <i class="fas fa-cog"></i>
                Админ-панель
              </router-link>
              <button class="dropdown-item dropdown-item-danger" @click="handleLogout">
                <i class="fas fa-sign-out-alt"></i>
                Выйти
              </button>
            </div>
          </div>
        </div>
      </div>
    </header>

    <main class="main-content">
      <div class="admin-page">
        <div class="admin-hero">
          <div class="hero-bg-deco">
            <div class="deco-circle d1"></div>
            <div class="deco-circle d2"></div>
            <div class="deco-circle d3"></div>
          </div>
          
          <div class="hero-content">
            <div class="hero-title-wrap">
              <div class="hero-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>
              </div>
              <div>
                <h1>Админ-панель</h1>
                <p>Управление системой Service Desk</p>
              </div>
            </div>
            <button class="btn-refresh" @click="refreshData">
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="23 4 23 10 17 10"></polyline><polyline points="1 20 1 14 7 14"></polyline><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path></svg>
              Обновить
            </button>
          </div>
        </div>

        <div class="stats-row">
          <div class="stat-card-admin">
            <div class="stat-icon-admin blue">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>
            </div>
            <div class="stat-info-admin">
              <span class="stat-num-admin">{{ stats.totalUsers }}</span>
              <span class="stat-lbl-admin">Пользователей</span>
            </div>
          </div>
          <div class="stat-card-admin">
            <div class="stat-icon-admin red">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"></path><polyline points="14 2 14 8 20 8"></polyline></svg>
            </div>
            <div class="stat-info-admin">
              <span class="stat-num-admin">{{ stats.totalTickets }}</span>
              <span class="stat-lbl-admin">Всего заявок</span>
            </div>
          </div>
          <div class="stat-card-admin">
            <div class="stat-icon-admin yellow">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
            </div>
            <div class="stat-info-admin">
              <span class="stat-num-admin">{{ stats.openTickets }}</span>
              <span class="stat-lbl-admin">Открытых</span>
            </div>
          </div>
          <div class="stat-card-admin">
            <div class="stat-icon-admin green">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="4" y="2" width="16" height="20" rx="2" ry="2"></rect><line x1="9" y1="22" x2="15" y2="22"></line><line x1="12" y1="2" x2="12" y2="22"></line></svg>
            </div>
            <div class="stat-info-admin">
              <span class="stat-num-admin">{{ stats.totalDepartments }}</span>
              <span class="stat-lbl-admin">Подразделений</span>
            </div>
          </div>
        </div>

        <div class="admin-tabs">
          <button class="tab-btn" :class="{ tabActive: tab === 'dashboard' }" @click="tab = 'dashboard'">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>
            Обзор
          </button>
          <button class="tab-btn" :class="{ tabActive: tab === 'users' }" @click="tab = 'users'">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle></svg>
            Пользователи
            <span class="tab-count">{{ users.length }}</span>
          </button>
          <button class="tab-btn" :class="{ tabActive: tab === 'departments' }" @click="tab = 'departments'">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="4" y="2" width="16" height="20" rx="2" ry="2"></rect><line x1="9" y1="22" x2="15" y2="22"></line><line x1="12" y1="2" x2="12" y2="22"></line></svg>
            Подразделения
            <span class="tab-count">{{ departments.length }}</span>
          </button>
          <button class="tab-btn" :class="{ tabActive: tab === 'tickets' }" @click="tab = 'tickets'">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"></path><polyline points="14 2 14 8 20 8"></polyline></svg>
            Заявки
            <span class="tab-count">{{ allTickets.length }}</span>
          </button>
        </div>

        <div v-if="tab === 'dashboard'" class="admin-content">
          <div class="dashboard-grid">
            <div class="dash-card">
              <div class="dash-header">
                <h3>Статистика заявок</h3>
              </div>
              <div class="bars-list">
                <div class="bar-row">
                  <div class="bar-info">
                    <span class="bar-label">Новые</span>
                    <span class="bar-pct">{{ getPercent('new') }}%</span>
                  </div>
                  <div class="bar-track">
                    <div class="bar-fill red" :style="{ width: getPercent('new') + '%' }"></div>
                  </div>
                  <div class="bar-num">{{ ticketStats.new }}</div>
                </div>
                <div class="bar-row">
                  <div class="bar-info">
                    <span class="bar-label">В работе</span>
                    <span class="bar-pct">{{ getPercent('in_progress') }}%</span>
                  </div>
                  <div class="bar-track">
                    <div class="bar-fill yellow" :style="{ width: getPercent('in_progress') + '%' }"></div>
                  </div>
                  <div class="bar-num">{{ ticketStats.in_progress }}</div>
                </div>
                <div class="bar-row">
                  <div class="bar-info">
                    <span class="bar-label">Закрытые</span>
                    <span class="bar-pct">{{ getPercent('closed') }}%</span>
                  </div>
                  <div class="bar-track">
                    <div class="bar-fill green" :style="{ width: getPercent('closed') + '%' }"></div>
                  </div>
                  <div class="bar-num">{{ ticketStats.closed }}</div>
                </div>
                <div class="bar-row">
                  <div class="bar-info">
                    <span class="bar-label">Отклонённые</span>
                    <span class="bar-pct">{{ getPercent('rejected') }}%</span>
                  </div>
                  <div class="bar-track">
                    <div class="bar-fill gray" :style="{ width: getPercent('rejected') + '%' }"></div>
                  </div>
                  <div class="bar-num">{{ ticketStats.rejected }}</div>
                </div>
              </div>
            </div>

            <div class="dash-card">
              <div class="dash-header">
                <h3>По ролям</h3>
              </div>
              <div class="roles-grid">
                <div class="role-card">
                  <div class="role-icon admin">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
                  </div>
                  <div class="role-text">
                    <span class="role-num">{{ getRoleCount('admin') }}</span>
                    <span class="role-lbl">Администраторы</span>
                  </div>
                </div>
                <div class="role-card">
                  <div class="role-icon specialist">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
                  </div>
                  <div class="role-text">
                    <span class="role-num">{{ getRoleCount('specialist') }}</span>
                    <span class="role-lbl">Специалисты</span>
                  </div>
                </div>
                <div class="role-card">
                  <div class="role-icon employee">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
                  </div>
                  <div class="role-text">
                    <span class="role-num">{{ getRoleCount('employee') }}</span>
                    <span class="role-lbl">Сотрудники</span>
                  </div>
                </div>
              </div>
            </div>

            <div class="dash-card">
              <div class="dash-header">
                <h3>Активность</h3>
              </div>
              <div class="activity-grid">
                <div class="activity-item">
                  <div class="act-icon red">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
                  </div>
                  <div class="act-text">
                    <span class="act-num">{{ stats.todayTickets }}</span>
                    <span class="act-lbl">Новых сегодня</span>
                  </div>
                </div>
                <div class="activity-item">
                  <div class="act-icon green">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"></polyline></svg>
                  </div>
                  <div class="act-text">
                    <span class="act-num">{{ stats.closedToday }}</span>
                    <span class="act-lbl">Закрыто сегодня</span>
                  </div>
                </div>
              </div>
            </div>

            <div class="dash-card wide">
              <div class="dash-header">
                <h3>Последние заявки</h3>
                <router-link to="/tickets" class="link-all">Все заявки</router-link>
              </div>
              <div class="recent-tickets">
                <router-link v-for="t in recentTickets" :key="t.id" :to="`/tickets/${t.id}`" class="recent-item">
                  <div class="recent-id">#{{ t.id }}</div>
                  <div class="recent-title">{{ t.title }}</div>
                  <span class="tag tag-sm" :class="`tag-${t.status}`">{{ ticketStatuses[t.status] }}</span>
                </router-link>
                <div v-if="recentTickets.length === 0" class="empty">Заявок пока нет</div>
              </div>
            </div>
          </div>
        </div>

        <div v-if="tab === 'users'" class="admin-content">
          <div class="content-toolbar">
            <div class="filters-group">
              <div class="search-input">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                <input v-model="userSearch" type="text" placeholder="Поиск..." />
              </div>
              <select v-model="userRoleFilter" class="filter-select">
                <option value="">Все роли</option>
                <option value="admin">Администраторы</option>
                <option value="specialist">Специалисты</option>
                <option value="employee">Сотрудники</option>
              </select>
            </div>
            <button class="btn-main" @click="openUserModal()">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
              Добавить
            </button>
          </div>

          <div class="content-pagination" v-if="paginatedUsers.length > 0">
            <span class="page-info">{{ userPageStart }}-{{ userPageEnd }} из {{ filteredUsers.length }}</span>
            <div class="page-btns">
              <button class="page-btn" :disabled="userPage === 1" @click="userPage--">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"></polyline></svg>
              </button>
              <button class="page-btn" :disabled="userPage >= userPageCount" @click="userPage++">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"></polyline></svg>
              </button>
            </div>
          </div>

          <div class="table-wrap">
            <table class="data-table-admin">
              <thead>
                <tr>
                  <th>Логин</th>
                  <th>ФИО</th>
                  <th>Роль</th>
                  <th>Подразделение</th>
                  <th>Email</th>
                  <th>Дата</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="user in paginatedUsers" :key="user.id">
                  <td><code>{{ user.login }}</code></td>
                  <td>{{ user.full_name }}</td>
                  <td><span class="tag" :class="`tag-${user.role}`">{{ userRoles[user.role] }}</span></td>
                  <td>{{ user.department || '—' }}</td>
                  <td>{{ user.email || '—' }}</td>
                  <td>{{ formatDate(user.created_at) }}</td>
                  <td>
                    <div class="btn-group">
                      <button class="btn-icon" @click="editUser(user)" title="Редактировать">
                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
                      </button>
                      <button class="btn-icon danger" @click="deleteUser(user)" title="Удалить">
                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
            <div v-if="filteredUsers.length === 0" class="empty-state">
              <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle></svg>
              <p>Пользователи не найдены</p>
            </div>
          </div>
        </div>

        <div v-if="tab === 'departments'" class="admin-content">
          <div class="content-toolbar">
            <div class="search-input">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
              <input v-model="deptSearch" type="text" placeholder="Поиск..." />
            </div>
            <button class="btn-main" @click="openDeptModal()">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
              Добавить
            </button>
          </div>

          <div class="dept-grid">
            <div v-for="dept in filteredDepartments" :key="dept.id" class="dept-card-new">
              <div class="dept-body">
                <div class="dept-icon-new">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="4" y="2" width="16" height="20" rx="2" ry="2"></rect><line x1="9" y1="22" x2="15" y2="22"></line><line x1="12" y1="2" x2="12" y2="22"></line></svg>
                </div>
                <div class="dept-text">
                  <h4>{{ dept.name }}</h4>
                  <code>{{ dept.code }}</code>
                </div>
                <div class="dept-count">{{ getDeptUserCount(dept.id) }}</div>
              </div>
              <div class="dept-btns">
                <button class="btn-icon" @click="editDept(dept)">
                  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
                </button>
                <button class="btn-icon danger" @click="deleteDept(dept)">
                  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
                </button>
              </div>
            </div>
            <div v-if="filteredDepartments.length === 0" class="empty-state">
              <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1"><rect x="4" y="2" width="16" height="20" rx="2" ry="2"></rect></svg>
              <p>Подразделения не найдены</p>
            </div>
          </div>
        </div>

        <div v-if="tab === 'tickets'" class="admin-content">
          <div class="content-toolbar">
            <div class="filters-group">
              <div class="search-input">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                <input v-model="ticketSearch" type="text" placeholder="Поиск..." />
              </div>
              <select v-model="ticketStatusFilter" class="filter-select">
                <option value="">Все статусы</option>
                <option value="new">Новые</option>
                <option value="in_progress">В работе</option>
                <option value="closed">Закрытые</option>
                <option value="rejected">Отклонённые</option>
              </select>
              <select v-model="ticketTypeFilter" class="filter-select">
                <option value="">Все типы</option>
                <option value="equipment">Оборудование</option>
                <option value="software">ПО</option>
                <option value="access">Доступы</option>
              </select>
            </div>
          </div>

          <div class="content-pagination" v-if="filteredTickets.length > 0">
            <span class="page-info">{{ ticketPageStart }}-{{ ticketPageEnd }} из {{ filteredTickets.length }}</span>
            <div class="page-btns">
              <button class="page-btn" :disabled="ticketPage === 1" @click="ticketPage--">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"></polyline></svg>
              </button>
              <button class="page-btn" :disabled="ticketPage >= ticketPageCount" @click="ticketPage++">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"></polyline></svg>
              </button>
            </div>
          </div>

          <div class="table-wrap">
            <table class="data-table-admin">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Заголовок</th>
                  <th>Тип</th>
                  <th>Статус</th>
                  <th>Приоритет</th>
                  <th>Автор</th>
                  <th>Исполнитель</th>
                  <th>Дата</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="ticket in paginatedTickets" :key="ticket.id">
                  <td><router-link :to="`/tickets/${ticket.id}`" class="link-id">#{{ ticket.id }}</router-link></td>
                  <td>{{ ticket.title }}</td>
                  <td>{{ ticketTypes[ticket.type] }}</td>
                  <td><span class="tag" :class="`tag-${ticket.status}`">{{ ticketStatuses[ticket.status] }}</span></td>
                  <td><span class="tag" :class="`tag-${ticket.priority}`">{{ ticketPriorities[ticket.priority] }}</span></td>
                  <td>{{ ticket.created_by?.full_name }}</td>
                  <td>{{ ticket.assigned_to?.full_name || '—' }}</td>
                  <td>{{ formatDate(ticket.created_at) }}</td>
                </tr>
              </tbody>
            </table>
            <div v-if="filteredTickets.length === 0" class="empty-state">
              <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"></path></svg>
              <p>Заявки не найдены</p>
            </div>
          </div>
        </div>
      </div>
    </main>

    <div v-if="showUserModal" class="modal-back" @click.self="closeUserModal">
      <div class="modal-box">
        <div class="modal-head">
          <h3>{{ editingUser ? 'Редактировать' : 'Новый пользователь' }}</h3>
          <button class="modal-x" @click="closeUserModal">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
          </button>
        </div>
        <form @submit.prevent="saveUser" class="modal-form">
          <div class="form-field">
            <label>Логин</label>
            <input v-model="userForm.login" required :disabled="editingUser" />
          </div>
          <div v-if="!editingUser" class="form-field">
            <label>Пароль</label>
            <input v-model="userForm.password" type="password" :required="!editingUser" />
          </div>
          <div class="form-field">
            <label>ФИО</label>
            <input v-model="userForm.full_name" required />
          </div>
          <div class="form-field">
            <label>Роль</label>
            <select v-model="userForm.role" required>
              <option value="employee">Сотрудник</option>
              <option value="specialist">Специалист</option>
              <option value="admin">Администратор</option>
            </select>
          </div>
          <div class="form-field">
            <label>Email</label>
            <input v-model="userForm.email" type="email" />
          </div>
          <div class="form-field">
            <label>Телефон</label>
            <input v-model="userForm.phone" />
          </div>
          <div class="form-field">
            <label>Подразделение</label>
            <select v-model="userForm.department_id">
              <option :value="null">Не выбрано</option>
              <option v-for="d in departments" :key="d.id" :value="d.id">{{ d.name }}</option>
            </select>
          </div>
          <div class="form-btns">
            <button type="button" class="btn-sec" @click="closeUserModal">Отмена</button>
            <button type="submit" class="btn-pri">{{ editingUser ? 'Сохранить' : 'Создать' }}</button>
          </div>
        </form>
      </div>
    </div>

    <div v-if="showDeptModal" class="modal-back" @click.self="closeDeptModal">
      <div class="modal-box">
        <div class="modal-head">
          <h3>{{ editingDept ? 'Редактировать' : 'Новое подразделение' }}</h3>
          <button class="modal-x" @click="closeDeptModal">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
          </button>
        </div>
        <form @submit.prevent="saveDept" class="modal-form">
          <div class="form-field">
            <label>Название</label>
            <input v-model="deptForm.name" required />
          </div>
          <div class="form-field">
            <label>Код</label>
            <input v-model="deptForm.code" placeholder="DIT" required :disabled="editingDept" />
          </div>
          <div class="form-btns">
            <button type="button" class="btn-sec" @click="closeDeptModal">Отмена</button>
            <button type="submit" class="btn-pri">{{ editingDept ? 'Сохранить' : 'Создать' }}</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../api'

const router = useRouter()
const authStore = useAuthStore()

const showMenu = ref(false)
const tab = ref('dashboard')
const users = ref([])
const departments = ref([])
const allTickets = ref([])

const showUserModal = ref(false)
const showDeptModal = ref(false)
const editingUser = ref(null)
const editingDept = ref(null)

const userSearch = ref('')
const userRoleFilter = ref('')
const userPage = ref(1)
const userPerPage = ref(10)

const deptSearch = ref('')

const ticketSearch = ref('')
const ticketStatusFilter = ref('')
const ticketTypeFilter = ref('')
const ticketPage = ref(1)
const ticketPerPage = ref(15)

const userForm = reactive({
  login: '',
  password: '',
  full_name: '',
  role: 'employee',
  email: '',
  phone: '',
  department_id: null
})

const deptForm = reactive({
  name: '',
  code: ''
})

const stats = ref({
  totalUsers: 0,
  totalTickets: 0,
  openTickets: 0,
  totalDepartments: 0,
  todayTickets: 0,
  closedToday: 0,
  totalComments: 0
})

const ticketStats = reactive({
  new: 0,
  in_progress: 0,
  closed: 0,
  rejected: 0
})

const userRoles = {
  employee: 'Сотрудник',
  specialist: 'Специалист',
  admin: 'Администратор'
}

const ticketTypes = { equipment: 'Оборудование', software: 'ПО', access: 'Доступ' }
const ticketPriorities = { low: 'Низкий', normal: 'Обычный', high: 'Высокий', critical: 'Критический' }
const ticketStatuses = { new: 'Новая', in_progress: 'В работе', closed: 'Закрыта', rejected: 'Отклонена' }

const userInitials = computed(() => {
  if (!authStore.user?.full_name) return '?'
  return authStore.user.full_name.split(' ').map(n => n[0]).join('').slice(0, 2)
})

const filteredUsers = computed(() => {
  let result = users.value
  if (userSearch.value) {
    const q = userSearch.value.toLowerCase()
    result = result.filter(u => u.login.toLowerCase().includes(q) || u.full_name.toLowerCase().includes(q))
  }
  if (userRoleFilter.value) {
    result = result.filter(u => u.role === userRoleFilter.value)
  }
  return result
})

const filteredDepartments = computed(() => {
  if (!deptSearch.value) return departments.value
  const q = deptSearch.value.toLowerCase()
  return departments.value.filter(d => d.name.toLowerCase().includes(q) || d.code.toLowerCase().includes(q))
})

const filteredTickets = computed(() => {
  let result = allTickets.value
  if (ticketSearch.value) {
    const q = ticketSearch.value.toLowerCase()
    result = result.filter(t => t.title.toLowerCase().includes(q) || String(t.id).includes(q))
  }
  if (ticketStatusFilter.value) {
    result = result.filter(t => t.status === ticketStatusFilter.value)
  }
  if (ticketTypeFilter.value) {
    result = result.filter(t => t.type === ticketTypeFilter.value)
  }
  return result
})

const recentTickets = computed(() => allTickets.value.slice(0, 5))

const userPageCount = computed(() => Math.ceil(filteredUsers.value.length / userPerPage.value) || 1)
const userPageStart = computed(() => (userPage.value - 1) * userPerPage.value + 1)
const userPageEnd = computed(() => Math.min(userPage.value * userPerPage.value, filteredUsers.value.length))
const paginatedUsers = computed(() => filteredUsers.value.slice((userPage.value - 1) * userPerPage.value, userPage.value * userPerPage.value))

const ticketPageCount = computed(() => Math.ceil(filteredTickets.value.length / ticketPerPage.value) || 1)
const ticketPageStart = computed(() => (ticketPage.value - 1) * ticketPerPage.value + 1)
const ticketPageEnd = computed(() => Math.min(ticketPage.value * ticketPerPage.value, filteredTickets.value.length))
const paginatedTickets = computed(() => filteredTickets.value.slice((ticketPage.value - 1) * ticketPerPage.value, ticketPage.value * ticketPerPage.value))

const getPercent = (status) => {
  const total = ticketStats.new + ticketStats.in_progress + ticketStats.closed + ticketStats.rejected || 1
  return Math.round((ticketStats[status] / total) * 100)
}

const getRoleCount = (role) => users.value.filter(u => u.role === role).length
const getDeptUserCount = (deptId) => users.value.filter(u => u.department_id === deptId).length

const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString('ru-RU')
}

const refreshData = async () => {
  await Promise.all([loadUsers(), loadDepartments(), loadTickets(), loadStats()])
}

const loadUsers = async () => {
  const res = await api.get('/users')
  users.value = res.data.users
}

const loadDepartments = async () => {
  const res = await api.get('/departments')
  departments.value = res.data.departments
}

const loadTickets = async () => {
  const res = await api.get('/tickets')
  allTickets.value = res.data.tickets
  ticketStats.new = allTickets.value.filter(t => t.status === 'new').length
  ticketStats.in_progress = allTickets.value.filter(t => t.status === 'in_progress').length
  ticketStats.closed = allTickets.value.filter(t => t.status === 'closed').length
  ticketStats.rejected = allTickets.value.filter(t => t.status === 'rejected').length
}

const loadStats = async () => {
  const res = await api.get('/dashboard/stats')
  const data = res.data
  stats.value = {
    totalUsers: users.value.length,
    totalTickets: data.total || 0,
    openTickets: (data.new || 0) + (data.in_progress || 0),
    totalDepartments: departments.value.length,
    todayTickets: data.new || 0,
    closedToday: data.closed || 0,
    totalComments: 0
  }
}

const openUserModal = (user = null) => {
  if (user) {
    editingUser.value = user
    Object.assign(userForm, {
      login: user.login,
      password: '',
      full_name: user.full_name,
      role: user.role,
      email: user.email || '',
      phone: user.phone || '',
      department_id: user.department_id
    })
  } else {
    editingUser.value = null
    Object.assign(userForm, { login: '', password: '', full_name: '', role: 'employee', email: '', phone: '', department_id: null })
  }
  showUserModal.value = true
}

const closeUserModal = () => {
  showUserModal.value = false
  editingUser.value = null
}

const saveUser = async () => {
  try {
    if (editingUser.value) {
      await api.put(`/users/${editingUser.value.id}`, userForm)
    } else {
      await api.post('/users', userForm)
    }
    closeUserModal()
    loadUsers()
    loadStats()
  } catch (e) {
    alert(e.response?.data?.error || 'Ошибка')
  }
}

const editUser = (user) => openUserModal(user)

const deleteUser = async (user) => {
  if (!confirm(`Удалить ${user.full_name}?`)) return
  try {
    await api.delete(`/users/${user.id}`)
    loadUsers()
    loadStats()
  } catch (e) {
    alert(e.response?.data?.error || 'Ошибка')
  }
}

const openDeptModal = (dept = null) => {
  if (dept) {
    editingDept.value = dept
    Object.assign(deptForm, { name: dept.name, code: dept.code })
  } else {
    editingDept.value = null
    Object.assign(deptForm, { name: '', code: '' })
  }
  showDeptModal.value = true
}

const closeDeptModal = () => {
  showDeptModal.value = false
  editingDept.value = null
}

const saveDept = async () => {
  try {
    if (editingDept.value) {
      await api.put(`/admin/departments/${editingDept.value.id}`, deptForm)
    } else {
      await api.post('/admin/departments', deptForm)
    }
    closeDeptModal()
    loadDepartments()
    loadStats()
  } catch (e) {
    alert(e.response?.data?.error || 'Ошибка')
  }
}

const editDept = (dept) => openDeptModal(dept)

const deleteDept = async (dept) => {
  if (!confirm(`Удалить ${dept.name}?`)) return
  try {
    await api.delete(`/admin/departments/${dept.id}`)
    loadDepartments()
    loadStats()
  } catch (e) {
    alert(e.response?.data?.error || 'Ошибка')
  }
}

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
}

onMounted(() => {
  loadUsers()
  loadDepartments()
  loadTickets()
  loadStats()
})
</script>

<style scoped>
.admin-page {
  padding: 0 0 48px;
}

.admin-hero {
  position: relative;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  padding: 40px 24px;
  margin-bottom: 24px;
  overflow: hidden;
}

.hero-bg-deco {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.deco-circle {
  position: absolute;
  border-radius: 50%;
  filter: blur(60px);
}

.d1 {
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(231, 76, 60, 0.2) 0%, transparent 70%);
  top: -100px;
  right: -50px;
}

.d2 {
  width: 250px;
  height: 250px;
  background: radial-gradient(circle, rgba(52, 152, 219, 0.15) 0%, transparent 70%);
  bottom: -80px;
  left: -50px;
}

.d3 {
  width: 150px;
  height: 150px;
  background: radial-gradient(circle, rgba(231, 76, 60, 0.1) 0%, transparent 70%);
  top: 40%;
  left: 30%;
}

.hero-content {
  position: relative;
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.hero-title-wrap {
  display: flex;
  align-items: center;
  gap: 16px;
}

.hero-icon {
  width: 60px;
  height: 60px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}

.hero-title-wrap h1 {
  font-size: 26px;
  font-weight: 700;
  color: #fff;
  margin-bottom: 4px;
}

.hero-title-wrap p {
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
}

.btn-refresh {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 10px;
  color: #fff;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-refresh:hover {
  background: rgba(255, 255, 255, 0.2);
}

.stats-row {
  max-width: 1400px;
  margin: 0 auto 24px;
  padding: 0 24px;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.stat-card-admin {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 14px;
}

.stat-icon-admin {
  width: 52px;
  height: 52px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-icon-admin.blue {
  background: rgba(52, 152, 219, 0.15);
  color: #3498db;
}

.stat-icon-admin.red {
  background: rgba(231, 76, 60, 0.15);
  color: #e74c3c;
}

.stat-icon-admin.yellow {
  background: rgba(241, 196, 15, 0.15);
  color: #f1c40f;
}

.stat-icon-admin.green {
  background: rgba(46, 204, 113, 0.15);
  color: #2ecc71;
}

.stat-info-admin {
  display: flex;
  flex-direction: column;
}

.stat-num-admin {
  font-size: 26px;
  font-weight: 700;
}

.stat-lbl-admin {
  font-size: 13px;
  color: var(--text-secondary);
}

.admin-tabs {
  max-width: 1400px;
  margin: 0 auto 20px;
  padding: 0 24px;
  display: flex;
  gap: 8px;
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 12px;
}

.tab-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 14px 20px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-secondary);
  background: transparent;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.tab-btn:hover {
  color: var(--text-primary);
}

.tabActive {
  background: var(--accent);
  color: #fff;
}

.tab-count {
  padding: 2px 8px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 10px;
  font-size: 12px;
}

.admin-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 24px;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 20px;
}

.dash-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 20px;
}

.dash-card.wide {
  grid-column: 1 / -1;
}

.dash-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.dash-header h3 {
  font-size: 15px;
  font-weight: 600;
}

.link-all {
  font-size: 13px;
  color: var(--accent);
}

.bars-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.bar-row {
  display: grid;
  grid-template-columns: 1fr 120px 40px;
  gap: 12px;
  align-items: center;
}

.bar-info {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
}

.bar-pct {
  color: var(--text-muted);
}

.bar-track {
  height: 8px;
  background: var(--bg-tertiary);
  border-radius: 4px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.3s;
}

.bar-fill.red { background: var(--accent); }
.bar-fill.green { background: var(--success); }
.bar-fill.yellow { background: var(--warning); }
.bar-fill.gray { background: var(--text-muted); }

.bar-num {
  font-size: 16px;
  font-weight: 700;
  text-align: right;
}

.roles-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.role-card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px;
  background: var(--bg-primary);
  border-radius: 10px;
}

.role-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.role-icon.admin {
  background: rgba(231, 76, 60, 0.15);
  color: var(--accent);
}

.role-icon.specialist {
  background: rgba(241, 196, 15, 0.15);
  color: var(--warning);
}

.role-icon.employee {
  background: rgba(52, 152, 219, 0.15);
  color: var(--secondary);
}

.role-text {
  display: flex;
  flex-direction: column;
}

.role-text .role-num {
  font-size: 18px;
  font-weight: 700;
}

.role-text .role-lbl {
  font-size: 12px;
  color: var(--text-secondary);
}

.activity-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px;
  background: var(--bg-primary);
  border-radius: 10px;
}

.act-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.act-icon.red {
  background: rgba(231, 76, 60, 0.15);
  color: var(--accent);
}

.act-icon.green {
  background: rgba(46, 204, 113, 0.15);
  color: var(--success);
}

.act-text {
  display: flex;
  flex-direction: column;
}

.act-num {
  font-size: 20px;
  font-weight: 700;
}

.act-lbl {
  font-size: 12px;
  color: var(--text-secondary);
}

.recent-tickets {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.recent-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: var(--bg-primary);
  border-radius: 8px;
  transition: all 0.2s;
}

.recent-item:hover {
  background: var(--bg-tertiary);
}

.recent-id {
  font-family: monospace;
  font-size: 12px;
  color: var(--text-muted);
}

.recent-title {
  flex: 1;
  font-size: 14px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.tag-sm {
  font-size: 11px;
  padding: 2px 8px;
}

.content-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 12px;
}

.filters-group {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.search-input {
  position: relative;
  width: 200px;
}

.search-input svg {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-muted);
}

.search-input input {
  width: 100%;
  padding: 12px 14px 12px 42px;
  border: 1px solid var(--border);
  border-radius: 10px;
  font-size: 14px;
  background: var(--bg-primary);
  color: var(--text-primary);
}

.search-input input:focus {
  outline: none;
  border-color: var(--accent);
}

.filter-select {
  padding: 12px 14px;
  border: 1px solid var(--border);
  border-radius: 10px;
  font-size: 14px;
  background: var(--bg-primary);
  color: var(--text-primary);
  cursor: pointer;
}

.filter-select:focus {
  outline: none;
  border-color: var(--accent);
}

.btn-main {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 18px;
  background: var(--accent);
  border: none;
  border-radius: 10px;
  color: #fff;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
}

.content-pagination {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.page-info {
  font-size: 13px;
  color: var(--text-secondary);
}

.page-btns {
  display: flex;
  gap: 8px;
}

.page-btn {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-primary);
  border: 1px solid var(--border);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s;
}

.page-btn:hover:not(:disabled) {
  border-color: var(--accent);
  color: var(--accent);
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.table-wrap {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 14px;
  overflow: hidden;
}

.data-table-admin {
  width: 100%;
  border-collapse: collapse;
}

.data-table-admin th,
.data-table-admin td {
  padding: 14px 16px;
  text-align: left;
  border-bottom: 1px solid var(--border);
}

.data-table-admin th {
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
  background: var(--bg-tertiary);
}

.data-table-admin tbody tr:hover {
  background: var(--bg-tertiary);
}

.btn-group {
  display: flex;
  gap: 6px;
}

.btn-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-primary);
  border: 1px solid var(--border);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s;
}

.btn-icon:hover {
  border-color: var(--accent);
  color: var(--accent);
}

.btn-icon.danger:hover {
  border-color: var(--error);
  color: var(--error);
}

.link-id {
  color: var(--accent);
  font-weight: 500;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 48px;
  color: var(--text-muted);
}

.empty-state svg {
  margin-bottom: 12px;
  opacity: 0.5;
}

.empty {
  text-align: center;
  padding: 24px;
  color: var(--text-muted);
}

.dept-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}

.dept-card-new {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 20px;
}

.dept-body {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 14px;
}

.dept-icon-new {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: var(--accent-light);
  color: var(--accent);
  display: flex;
  align-items: center;
  justify-content: center;
}

.dept-text {
  flex: 1;
}

.dept-text h4 {
  font-size: 15px;
  font-weight: 600;
  margin-bottom: 2px;
}

.dept-text code {
  font-size: 13px;
  color: var(--text-muted);
}

.dept-count {
  font-size: 20px;
  font-weight: 700;
}

.dept-btns {
  display: flex;
  gap: 8px;
}

.modal-back {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-box {
  width: 100%;
  max-width: 420px;
  background: var(--bg-secondary);
  border-radius: 16px;
  margin: 16px;
}

.modal-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid var(--border);
}

.modal-head h3 {
  font-size: 18px;
  font-weight: 600;
}

.modal-x {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
}

.modal-form {
  padding: 20px;
}

.form-field {
  margin-bottom: 16px;
}

.form-field label {
  display: block;
  font-size: 13px;
  color: var(--text-secondary);
  margin-bottom: 6px;
}

.form-field input,
.form-field select {
  width: 100%;
  padding: 12px;
  border: 1px solid var(--border);
  border-radius: 10px;
  font-size: 14px;
  background: var(--bg-primary);
  color: var(--text-primary);
}

.form-field input:focus,
.form-field select:focus {
  outline: none;
  border-color: var(--accent);
}

.form-btns {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  padding-top: 16px;
}

.btn-sec, .btn-pri {
  padding: 12px 20px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
}

.btn-sec {
  background: transparent;
  color: var(--text-secondary);
  border: 1px solid var(--border);
}

.btn-pri {
  background: var(--accent);
  color: #fff;
  border: none;
}

code {
  font-family: monospace;
  padding: 2px 8px;
  background: var(--bg-tertiary);
  border-radius: 4px;
  font-size: 13px;
}

.tag {
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
}

.tag-admin { background: rgba(231, 76, 60, 0.15); color: var(--accent); }
.tag-specialist { background: rgba(241, 196, 15, 0.15); color: var(--warning); }
.tag-employee { background: rgba(52, 152, 219, 0.15); color: var(--secondary); }
.tag-new { background: rgba(231, 76, 60, 0.15); color: var(--accent); }
.tag-in_progress { background: rgba(241, 196, 15, 0.15); color: var(--warning); }
.tag-closed { background: rgba(46, 204, 113, 0.15); color: var(--success); }
.tag-rejected { background: rgba(149, 165, 166, 0.15); color: #95a5a6; }
.tag-low { background: rgba(46, 204, 113, 0.15); color: var(--success); }
.tag-normal { background: rgba(52, 152, 219, 0.15); color: var(--secondary); }
.tag-high { background: rgba(241, 196, 15, 0.15); color: var(--warning); }
.tag-critical { background: rgba(231, 76, 60, 0.15); color: var(--accent); }

@media (max-width: 1024px) {
  .stats-row, .dashboard-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .hero-content {
    flex-direction: column;
    gap: 16px;
    text-align: center;
  }
  .hero-title-wrap {
    flex-direction: column;
  }
  .stats-row {
    grid-template-columns: 1fr;
  }
  .filters-group {
    width: 100%;
  }
  .search-input {
    flex: 1;
    min-width: 150px;
  }
}
</style>