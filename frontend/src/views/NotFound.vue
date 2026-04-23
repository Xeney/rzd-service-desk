<template>
  <div class="error-page">
    <div class="error-bg">
      <div class="track">
        <div v-for="i in 15" :key="i" class="tie" :style="{ left: `${i * 7}%`, animationDelay: `${i * 0.1}s` }"></div>
      </div>
      <div class="glow g1"></div>
      <div class="glow g2"></div>
      <div class="glow g3"></div>
    </div>

    <div class="error-content">
      <div class="error-icon">
        <svg xmlns="http://www.w3.org/2000/svg" width="120" height="120" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="12" y1="8" x2="12" y2="12"></line>
          <line x1="12" y1="16" x2="12.01" y2="16"></line>
        </svg>
      </div>
      
      <h1>404</h1>
      <p class="error-title">Страница не найдена</p>
      <p class="error-desc">
        Извините, запрошенная вами страница не существует или была перемещена.
      </p>
      
      <div class="error-actions">
        <router-link to="/" class="btn-home">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
            <polyline points="9 22 9 12 15 12 15 22"></polyline>
          </svg>
          На главную
        </router-link>
        <button @click="goBack" class="btn-back">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="19" y1="12" x2="5" y2="12"></line>
            <polyline points="12 19 5 12 12 5"></polyline>
          </svg>
          Назад
        </button>
      </div>

      <div class="train-animation">
        <div class="train">
          <div class="train-body">
            <div class="window"></div>
            <div class="window"></div>
            <div class="window"></div>
          </div>
          <div class="train-wheels">
            <div class="wheel w1"></div>
            <div class="wheel w2"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goBack = () => {
  router.back()
}
</script>

<style scoped>
.error-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  position: relative;
  overflow: hidden;
}

.error-bg {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.track {
  position: absolute;
  bottom: 80px;
  left: 0;
  right: 0;
  height: 20px;
}

.tie {
  position: absolute;
  width: 12px;
  height: 20px;
  background: #3a3a5c;
  animation: moveTie 2s linear infinite;
}

@keyframes moveTie {
  0% { transform: translateX(-50px); }
  100% { transform: translateX(50px); }
}

.glow {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
}

.g1 {
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(231, 76, 60, 0.15) 0%, transparent 70%);
  top: -100px;
  right: -50px;
}

.g2 {
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(52, 152, 219, 0.1) 0%, transparent 70%);
  bottom: -50px;
  left: -50px;
}

.g3 {
  width: 200px;
  height: 200px;
  background: radial-gradient(circle, rgba(231, 76, 60, 0.1) 0%, transparent 70%);
  top: 40%;
  left: 30%;
}

.error-content {
  position: relative;
  text-align: center;
  padding: 24px;
}

.error-icon {
  width: 120px;
  height: 120px;
  margin: 0 auto 24px;
  background: rgba(231, 76, 60, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--accent);
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.error-content h1 {
  font-size: 120px;
  font-weight: 800;
  background: linear-gradient(135deg, var(--accent) 0%, #ff6b6b 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 8px;
  line-height: 1;
}

.error-title {
  font-size: 28px;
  font-weight: 600;
  color: #fff;
  margin-bottom: 12px;
}

.error-desc {
  font-size: 16px;
  color: rgba(255, 255, 255, 0.7);
  max-width: 400px;
  margin: 0 auto 32px;
  line-height: 1.6;
}

.error-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
}

.btn-home, .btn-back {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 24px;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  text-decoration: none;
}

.btn-home {
  background: var(--accent);
  color: #fff;
  border: none;
}

.btn-home:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 30px rgba(231, 76, 60, 0.4);
}

.btn-back {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.btn-back:hover {
  background: rgba(255, 255, 255, 0.2);
}

.train-animation {
  margin-top: 60px;
}

.train {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  animation: trainMove 3s ease-in-out infinite;
}

@keyframes trainMove {
  0%, 100% { transform: translateX(-20px); }
  50% { transform: translateX(20px); }
}

.train-body {
  display: flex;
  gap: 4px;
  padding: 12px 16px;
  background: linear-gradient(135deg, var(--accent) 0%, #c0392b 100%);
  border-radius: 8px 16px 0 0;
}

.window {
  width: 16px;
  height: 14px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 2px;
}

.train-wheels {
  display: flex;
  gap: 24px;
}

.wheel {
  width: 16px;
  height: 16px;
  background: #2a2a4a;
  border: 3px solid var(--accent);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.w1 { animation-delay: 0s; }
.w2 { animation-delay: 0.5s; }

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@media (max-width: 480px) {
  .error-content h1 {
    font-size: 80px;
  }

  .error-title {
    font-size: 22px;
  }

  .error-icon {
    width: 80px;
    height: 80px;
  }
}
</style>