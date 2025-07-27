let logs = [];
let isPaused = false;

function logAction(action){
  const now = new Date();
  const time = now.toLocaleTimeString('ar-EG');
  const date = now.toLocaleDateString('ar-EG');
  logs.unshift(`✔ ${action} — ${time} ${date}`);
  renderLog();
  isPaused = false;
  hideOverlay();
}

function renderLog(){
  const box = document.getElementById('logBox');
  box.innerHTML = logs.map(item => `<div class='logentry'>${item}</div>`).join('');
}

function toggleLog(){
  const logBox = document.getElementById('logBox');
  if (logBox.style.display === 'none' || logBox.style.display === ''){
    logBox.style.display = 'block';
    renderLog();
  } else {
    logBox.style.display = 'none';
  }
}

function showOverlay(){
  document.getElementById('alertOverlay').style.display = 'flex';
}

function hideOverlay(){
  document.getElementById('alertOverlay').style.display = 'none';
}

function updateUI(data){
  document.getElementById('type').textContent = data.objectType;
  document.getElementById('location').textContent = data.location;
  document.getElementById('speed').textContent = `${data.speed} كم/س`;
  document.getElementById('altitude').textContent = `${data.height} م`;
  document.getElementById('accuracy').textContent = data.accuracy;
  document.getElementById('timestamp').textContent = data.timestamp;

  document.getElementById('energy').textContent = data.energy.toFixed(2);
  document.getElementById('size_score').textContent = data.size_score.toFixed(2);
  document.getElementById('flap_rate').textContent = data.flap_rate.toFixed(2) + ' Hz';


  const isDanger = ['درون', 'طائر', 'Drone', 'Bird'].includes(data.objectType);
  const statusText = document.getElementById('statusText');
  const actions = document.getElementById('actions');

  if (isDanger){
    isPaused = true;
    actions.style.display = 'flex';
    statusText.style.color = '#ff5252';
    statusText.classList.add("warning");
    statusText.textContent = data.objectType === 'درون' || data.objectType === 'Drone'
      ? '🚨 تنبيه: تم رصد درون غير مصرح به'
      : '🚨 تنبيه: تم رصد طائر في منطقة المطار';

    showOverlay();
  } else {
    actions.style.display = 'none';
    statusText.style.color = '#00e676';
    statusText.textContent = '🟢 الحالة: لا توجد أجسام خطيرة';
    statusText.classList.remove("warning");
    hideOverlay();
  }
}

async function getLivePrediction() {
  if (isPaused) return;

  try {
    const response = await fetch('http://127.0.0.1:5000/predict_random'); // استدعاء GET للصف العشوائي من السيرفر
    const result = await response.json();

    const objectType = result.prediction === 'drone' ? 'درون' : 'طائر';
    const uiData = {
      objectType: objectType,
      location: result.location,
      speed: result.features.speed,
      height: result.features.altitude,
      accuracy: result.confidence,
      timestamp: new Date(result.timestamp).toLocaleString('ar-EG'),

      energy: result.features.energy,
      size_score: result.features.size_score,
      flap_rate: result.features.flap_rate
      
    };

    updateUI(uiData);
    logAction(`تم التنبؤ بجسم: ${objectType} عند الموقع: ${result.location}`);

  } catch (error) {
    console.error("API Error:", error);
    logAction('حدث خطأ أثناء الاتصال بالخادم');
  }
}

// تشغيل التنبؤ كل 6 ثواني
setInterval(getLivePrediction, 6000);
// استدعاء أول عند بداية تشغيل الصفحة
getLivePrediction();
