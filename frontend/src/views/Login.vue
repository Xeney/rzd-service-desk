<template>
  <div class="login-page">
    <div class="login-scene">
      <div class="stars">
        <div v-for="i in 30" :key="i" class="star" :style="getStarStyle(i)"></div>
      </div>
      
      <div class="moon"></div>
      
      <div class="mountains">
        <div class="mountain mountain-1"></div>
        <div class="mountain mountain-2"></div>
        <div class="mountain mountain-3"></div>
      </div>
      
      <div class="tracks-container">
        <div class="track">
          <div class="rail"></div>
          <div class="ties">
            <div v-for="i in 25" :key="i" class="tie" :style="{ animationDelay: `${i * 0.12}s` }"></div>
          </div>
        </div>
        <div class="track">
          <div class="rail"></div>
          <div class="ties">
            <div v-for="i in 25" :key="i" class="tie" :style="{ animationDelay: `${i * 0.12}s` }"></div>
          </div>
        </div>
      </div>
      
      <div class="train-wrapper" :class="{ moving: trainMoving }">
        <div class="train">
          <div class="locomotive">
            <div class="cabin"></div>
            <div class="body"></div>
            <div class="chimney">
              <div class="smoke">
                <div class="smoke-puff"></div>
                <div class="smoke-puff"></div>
                <div class="smoke-puff"></div>
              </div>
            </div>
          </div>
          <div class="car car-1">
            <div class="car-body"></div>
          </div>
          <div class="car car-2">
            <div class="car-body"></div>
          </div>
          <div class="wheels">
            <div class="wheel"></div>
            <div class="wheel"></div>
            <div class="wheel"></div>
            <div class="wheel"></div>
          </div>
        </div>
      </div>
      
      <div class="glows">
        <div class="glow glow-1"></div>
        <div class="glow glow-2"></div>
        <div class="glow glow-3"></div>
      </div>
    </div>

    <div class="login-container">
      <transition name="login-card" appear>
        <div class="login-card">
          <div class="login-header">
            <div class="login-logo">
              <div class="rzd-emblem">
                <span>Р</span><span>Ж</span><span>Д</span>
              </div>
            </div>
            <h1 class="login-title">Service Desk</h1>
            <p class="login-subtitle">Вход в систему</p>
          </div>

          <form @submit.prevent="handleLogin" class="login-form">
            <transition-group name="form-field" tag="div">
              <div key="login" class="form-group">
                <label class="label">Логин</label>
                <div class="input-wrapper">
                  <i class="fas fa-user input-icon"></i>
                  <input
                    v-model="login"
                    type="text"
                    class="input input-with-icon"
                    placeholder="Введите логин"
                    required
                    autocomplete="username"
                  />
                </div>
              </div>

              <div key="password" class="form-group">
                <label class="label">Пароль</label>
                <div class="input-wrapper">
                  <i class="fas fa-lock input-icon"></i>
                  <input
                    v-model="password"
                    :type="showPassword ? 'text' : 'password'"
                    class="input input-with-icon input-with-toggle"
                    placeholder="Введите пароль"
                    required
                    autocomplete="current-password"
                  />
                  <button
                    type="button"
                    class="input-toggle"
                    @click="showPassword = !showPassword"
                  >
                    <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                  </button>
                </div>
              </div>
            </transition-group>

            <transition name="error-fade">
              <div v-if="error" class="error-message">
                <i class="fas fa-circle-exclamation"></i>
                {{ error }}
              </div>
            </transition>

            <button
              type="submit"
              class="btn btn-primary btn-lg btn-block btn-login"
              :disabled="loading"
            >
              <i v-if="loading" class="fas fa-spinner fa-spin"></i>
              <span v-else>Войти</span>
            </button>
          </form>

          <div class="login-footer">
            <div class="rzd-badge">
              <i class="fas fa-train"></i>
              <span>РЖД</span>
            </div>
            <p>Единая система обработки заявок</p>
          </div>
        </div>
      </transition>

      <transition name="info-fade" appear>
        <div class="login-info">
          <div class="info-card">
            <div class="info-icon">
              <i class="fas fa-shield-alt"></i>
            </div>
            <div class="info-content">
              <h4>Безопасность</h4>
              <p>Защищённое соединение</p>
            </div>
          </div>
          <div class="info-card">
            <div class="info-icon">
              <i class="fas fa-bolt"></i>
            </div>
            <div class="info-content">
              <h4>Скорость</h4>
              <p>Быстрая обработка заявок</p>
            </div>
          </div>
          <div class="info-card">
            <div class="info-icon">
              <i class="fas fa-comments"></i>
            </div>
            <div class="info-content">
              <h4>Общение</h4>
              <p>Обсуждение в реальном времени</p>
            </div>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useToast } from '../composables/useToast'

const router = useRouter()
const authStore = useAuthStore()
const toast = useToast()

const login = ref('')
const password = ref('')
const showPassword = ref(false)
const loading = ref(false)
const error = ref('')
const trainMoving = ref(false)

const getStarStyle = (i) => {
  const x = Math.random() * 100
  const y = Math.random() * 40
  const size = 1 + Math.random() * 2
  const duration = 2 + Math.random() * 3
  return {
    left: `${x}%`,
    top: `${y}%`,
    width: `${size}px`,
    height: `${size}px`,
    animationDuration: `${duration}s`
  }
}

const handleLogin = async () => {
  loading.value = true
  error.value = ''

  const success = await authStore.login(login.value, password.value)

  if (success) {
    toast.success('Добро пожаловать!')
    router.push('/')
  } else {
    error.value = authStore.error || 'Неверный логин или пароль'
  }

  loading.value = false
}

onMounted(() => {
  setTimeout(() => {
    trainMoving.value = true
  }, 500)
})
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  background: linear-gradient(180deg, #0a0a1a 0%, #1a1a2e 50%, #0f0f1f 100%);
  position: relative;
  overflow: hidden;
}

.login-scene {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.stars {
  position: absolute;
  inset: 0;
}

.star {
  position: absolute;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 50%;
  animation: twinkle 3s ease-in-out infinite;
}

@keyframes twinkle {
  0%, 100% { opacity: 0.3; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.2); }
}

.moon {
  position: absolute;
  top: 40px;
  right: 80px;
  width: 80px;
  height: 80px;
  background: radial-gradient(circle at 30% 30%, #fff 0%, #e8e8e8 50%, #c0c0c0 100%);
  border-radius: 50%;
  box-shadow: 0 0 40px rgba(255, 255, 255, 0.3), 0 0 80px rgba(255, 255, 255, 0.1);
}

.moon::before {
  content: '';
  position: absolute;
  top: 15px;
  left: 20px;
  width: 15px;
  height: 15px;
  background: rgba(200, 200, 200, 0.5);
  border-radius: 50%;
}

.moon::after {
  content: '';
  position: absolute;
  top: 35px;
  left: 45px;
  width: 20px;
  height: 20px;
  background: rgba(200, 200, 200, 0.4);
  border-radius: 50%;
}

.mountains {
  position: absolute;
  bottom: 100px;
  left: 0;
  right: 0;
  height: 200px;
}

.mountain {
  position: absolute;
  bottom: 0;
  width: 0;
  height: 0;
  border-style: solid;
}

.mountain-1 {
  left: -50px;
  border-width: 0 200px 180px 200px;
  border-color: transparent transparent #1a1a2e transparent;
  opacity: 0.8;
}

.mountain-2 {
  right: -30px;
  border-width: 0 250px 220px 250px;
  border-color: transparent transparent #15152a transparent;
  opacity: 0.9;
}

.mountain-3 {
  left: 30%;
  border-width: 0 150px 140px 150px;
  border-color: transparent transparent #202040 transparent;
}

.tracks-container {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 80px;
}

.track {
  position: relative;
  height: 100%;
}

.track:first-child {
  top: 10px;
}

.rail {
  position: absolute;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, 
    transparent 0%, 
    rgba(255, 255, 255, 0.4) 20%, 
    rgba(255, 255, 255, 0.4) 80%, 
    transparent 100%
  );
}

.ties {
  display: flex;
  gap: 20px;
  justify-content: center;
}

.tie {
  width: 4px;
  height: 25px;
  background: rgba(255, 255, 255, 0.25);
  animation: tieBlink 1.5s ease-in-out infinite;
}

@keyframes tieBlink {
  0%, 100% { opacity: 0.25; }
  50% { opacity: 0.6; }
}

.train-wrapper {
  position: absolute;
  bottom: 15px;
  left: -300px;
  transition: left 12s ease-in-out;
}

.train-wrapper.moving {
  left: 110%;
}

.train {
  display: flex;
  align-items: flex-end;
}

.locomotive {
  position: relative;
  width: 70px;
  height: 40px;
}

.cabin {
  position: absolute;
  top: 0;
  left: 5px;
  width: 25px;
  height: 25px;
  background: linear-gradient(180deg, #2a2a4a 0%, #1a1a3a 100%);
  border-radius: 4px 4px 0 0;
  border: 2px solid rgba(231, 76, 60, 0.5);
  border-bottom: none;
}

.body {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 60px;
  height: 25px;
  background: linear-gradient(180deg, #e74c3c 0%, #c0392b 100%);
  border-radius: 4px;
}

.chimney {
  position: absolute;
  top: -15px;
  left: 40px;
  width: 12px;
  height: 20px;
  background: linear-gradient(180deg, #444 0%, #333 100%);
  border-radius: 2px 2px 0 0;
}

.smoke {
  position: absolute;
  top: -25px;
  left: 5px;
}

.smoke-puff {
  position: absolute;
  width: 15px;
  height: 15px;
  background: rgba(255, 255, 255, 0.4);
  border-radius: 50%;
  animation: smokeRise 2s ease-out infinite;
}

.smoke-puff:nth-child(1) { left: 0; animation-delay: 0s; }
.smoke-puff:nth-child(2) { left: 8px; animation-delay: 0.6s; }
.smoke-puff:nth-child(3) { left: -5px; animation-delay: 1.2s; }

@keyframes smokeRise {
  0% { transform: scale(0.5) translateY(0); opacity: 0.6; }
  100% { transform: scale(2.5) translateY(-30px); opacity: 0; }
}

.car {
  width: 45px;
  height: 30px;
  margin-left: 3px;
}

.car-body {
  width: 100%;
  height: 100%;
  background: linear-gradient(180deg, #e74c3c 0%, #c0392b 100%);
  border-radius: 2px;
}

.wheels {
  display: flex;
  gap: 35px;
  position: absolute;
  bottom: -4px;
  left: 5px;
}

.wheel {
  width: 12px;
  height: 12px;
  background: rgba(255, 255, 255, 0.3);
  border: 2px solid rgba(255, 255, 255, 0.5);
  border-radius: 50%;
  animation: wheelSpin 0.8s linear infinite;
}

@keyframes wheelSpin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.glows {
  position: absolute;
  inset: 0;
}

.glow {
  position: absolute;
  border-radius: 50%;
  filter: blur(100px);
}

.glow-1 {
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, rgba(231, 76, 60, 0.15) 0%, transparent 70%);
  top: -150px;
  right: -100px;
  animation: glowPulse 5s ease-in-out infinite;
}

.glow-2 {
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(52, 152, 219, 0.1) 0%, transparent 70%);
  bottom: -100px;
  left: -100px;
  animation: glowPulse 6s ease-in-out infinite 1s;
}

.glow-3 {
  width: 250px;
  height: 250px;
  background: radial-gradient(circle, rgba(155, 89, 182, 0.1) 0%, transparent 70%);
  top: 30%;
  left: 40%;
  animation: glowPulse 7s ease-in-out infinite 2s;
}

@keyframes glowPulse {
  0%, 100% { transform: scale(1); opacity: 0.7; }
  50% { transform: scale(1.15); opacity: 1; }
}

.login-container {
  display: flex;
  gap: 64px;
  align-items: center;
  max-width: 1000px;
  width: 100%;
  position: relative;
  z-index: 1;
}

.login-card {
  flex: 1;
  max-width: 420px;
  background: rgba(30, 30, 50, 0.9);
  backdrop-filter: blur(20px);
  border-radius: var(--radius-xl);
  padding: 40px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.login-logo {
  margin-bottom: 20px;
}

.rzd-emblem {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, var(--accent) 0%, #c0392b 100%);
  border-radius: var(--radius-lg);
  box-shadow: 0 8px 24px rgba(231, 76, 60, 0.3);
  animation: emblemGlow 3s ease-in-out infinite;
}

@keyframes emblemGlow {
  0%, 100% { box-shadow: 0 8px 24px rgba(231, 76, 60, 0.3); }
  50% { box-shadow: 0 8px 40px rgba(231, 76, 60, 0.5); }
}

.rzd-emblem span {
  font-family: var(--font-display);
  font-size: 24px;
  font-weight: 900;
  color: white;
  margin: 0 2px;
}

.login-title {
  font-family: var(--font-display);
  font-size: 24px;
  font-weight: 700;
  color: #fff;
  margin-bottom: 8px;
}

.login-subtitle {
  color: rgba(255, 255, 255, 0.6);
  font-size: 14px;
}

.login-form {
  margin-bottom: 24px;
}

.form-group {
  margin-bottom: 20px;
}

.label {
  display: block;
  color: rgba(255, 255, 255, 0.6);
  font-size: 13px;
  font-weight: 500;
  margin-bottom: 8px;
}

.input-wrapper {
  position: relative;
}

.input-icon {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  color: rgba(255, 255, 255, 0.4);
  font-size: 14px;
}

.input {
  width: 100%;
  padding: 14px 16px;
  padding-left: 42px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: var(--radius-md);
  color: #fff;
  font-size: 15px;
  transition: var(--transition);
}

.input::placeholder {
  color: rgba(255, 255, 255, 0.35);
}

.input:focus {
  outline: none;
  border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(231, 76, 60, 0.2);
}

.input-with-toggle {
  padding-right: 44px;
}

.input-toggle {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.4);
  cursor: pointer;
  padding: 4px;
}

.input-toggle:hover {
  color: rgba(255, 255, 255, 0.7);
}

.error-message {
  background: rgba(192, 57, 43, 0.15);
  border: 1px solid rgba(192, 57, 43, 0.3);
  border-radius: var(--radius-md);
  padding: 12px 16px;
  color: #e74c3c;
  font-size: 14px;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.error-fade-enter-active,
.error-fade-leave-active {
  transition: all 0.3s ease;
}

.error-fade-enter-from,
.error-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.btn-login {
  background: linear-gradient(135deg, var(--accent) 0%, #c0392b 100%);
  color: #fff;
  border: none;
  font-weight: 600;
}

.btn-login:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(231, 76, 60, 0.4);
}

.login-footer {
  text-align: center;
}

.rzd-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: rgba(255, 255, 255, 0.08);
  border-radius: var(--radius-full);
  color: rgba(255, 255, 255, 0.6);
  font-size: 13px;
  margin-bottom: 8px;
}

.rzd-badge i {
  color: var(--accent);
}

.login-footer p {
  color: rgba(255, 255, 255, 0.4);
  font-size: 12px;
}

.login-info {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.info-card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 16px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: var(--radius-lg);
}

.info-icon {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-md);
  background: rgba(231, 76, 60, 0.15);
  color: var(--accent);
  display: flex;
  align-items: center;
  justify-content: center;
}

.info-content h4 {
  color: #fff;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 2px;
}

.info-content p {
  color: rgba(255, 255, 255, 0.5);
  font-size: 12px;
}

.login-card-enter-active,
.login-card-leave-active {
  transition: all 0.8s ease;
}

.login-card-enter-from {
  opacity: 0;
  transform: translateX(-50px);
}

.login-card-leave-to {
  opacity: 0;
  transform: translateX(50px);
}

.form-field-enter-active {
  transition: all 0.5s ease;
}

.form-field-leave-active {
  transition: all 0.3s ease;
}

.form-field-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.form-field-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

.form-field-move {
  transition: transform 0.5s ease;
}

.info-fade-enter-active,
.info-fade-leave-active {
  transition: all 0.8s ease 0.3s;
}

.info-fade-enter-from,
.info-fade-leave-to {
  opacity: 0;
  transform: translateX(30px);
}

@media (max-width: 900px) {
  .login-container {
    flex-direction: column;
    gap: 32px;
  }
  
  .login-info {
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: center;
  }
  
  .info-card {
    flex: 1;
    min-width: 180px;
    max-width: 250px;
  }
}
</style>