function lightToggle() {
    const btn = document.getElementById('light-toggle');
    fetch('/toggle_light', { method: 'POST' })
      .then(res => res.json())
      .then(data => {
        btn.classList.remove('active');
        if (data.light_status === "ON") btn.classList.add('active');
        document.querySelector('.control-item .control-status').textContent = data.light_status;
      })
      .catch(err => console.error('Light toggle error:', err));
  }
  
  function fanToggle() {
    const btn = document.getElementById('fan-toggle');
    fetch('/toggle_fan', { method: 'POST' })
      .then(res => res.json())
      .then(data => {
        btn.classList.remove('active');
        if (data.fan_status === "ON") btn.classList.add('active');
        document.querySelectorAll('.control-item .control-status')[1].textContent = data.fan_status;
      })
      .catch(err => console.error('Fan toggle error:', err));
  }
  
  function valveToggle() {
    const btn = document.getElementById('valve-toggle');
    fetch('/toggle_valve', { method: 'POST' })
      .then(res => res.json())
      .then(data => {
        btn.classList.remove('active');
        if (data.valve_status === "OPEN") btn.classList.add('active');
        document.querySelectorAll('.control-item .control-status')[2].textContent = data.valve_status;
      })
      .catch(err => console.error('Valve toggle error:', err));
  }
  
  function setBrightness(value) {
    const display = document.getElementById('brightness-value');
    if (display) display.textContent = value + '%';
    fetch('/set_brightness', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `brightness=${value}`
    })
    .catch(err => console.error('Brightness set error:', err));
  }
  
  function sendQuickReport() {
    const btn = document.getElementById('report-btn');
    btn.textContent = 'Sending...';
    fetch('/send_quick_report', { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            alert(data.message || 'Report sent!');
            btn.textContent = 'Send Quick Report';
        })
        .catch(err => {
            console.error('Report error:', err);
            alert('Failed to send report.');
            btn.textContent = 'Send Quick Report';
        });
  }
  
  window.onload = () => {
    fetch('/get_status')
        .then(res => res.json())
        .then(data => {
            const lightToggle = document.getElementById('light-toggle');
            if (lightToggle) {
                lightToggle.classList.remove('active');
                if (data.light === "ON") lightToggle.classList.add('active');
            }
            const fanToggle = document.getElementById('fan-toggle');
            if (fanToggle) {
                fanToggle.classList.remove('active');
                if (data.fan === "ON") fanToggle.classList.add('active');
            }
            const valveToggle = document.getElementById('valve-toggle');
            if (valveToggle) {
                valveToggle.classList.remove('active');
                if (data.valve === "OPEN") valveToggle.classList.add('active');
            }
            const slider = document.getElementById('brightness-slider');
            const display = document.getElementById('brightness-value');
            if (slider) slider.value = data.brightness || 70;
            if (display) display.textContent = (data.brightness || 70) + '%';
        })
        .catch(err => console.error('Initial status fetch error:', err));
  };
  
  // Live update for temperature/humidity (if not using inline script)
  setInterval(() => {
    fetch('/get_status')
      .then(res => res.json())
      .then(data => {
        // console.log(data); ← try adding this line temporarily
        ...
      });
  }, 5000);
  