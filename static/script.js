// static/script.js

function lightToggle() {
    const btn = document.getElementById('light-toggle');
    fetch('/toggle_light', { method: 'POST' })
        .then(res => {
            if (!res.ok) throw new Error('Network response was not OK');
            return res.json();
        })
        .then(data => {
            console.log('Light toggle response:', data);
            btn.classList.toggle('active', data.light_status === "ON");
        })
        .catch(err => console.error('Light toggle error:', err));
}

function fanToggle() {
    const btn = document.getElementById('fan-toggle');
    fetch('/toggle_fan', { method: 'POST' })
        .then(res => {
            if (!res.ok) throw new Error('Network response was not OK');
            return res.json();
        })
        .then(data => {
            console.log('Fan toggle response:', data);
            btn.classList.toggle('active', data.fan_status === "ON");
        })
        .catch(err => console.error('Fan toggle error:', err));
}

function valveToggle() {
    const btn = document.getElementById('valve-toggle');
    fetch('/toggle_valve', { method: 'POST' })
        .then(res => {
            if (!res.ok) throw new Error('Network response was not OK');
            return res.json();
        })
        .then(data => {
            console.log('Valve toggle response:', data);
            btn.classList.toggle('active', data.valve_status === "OPEN");
        })
        .catch(err => console.error('Valve toggle error:', err));
}

function setBrightness(value) {
    const display = document.getElementById('brightness-value');
    display.textContent = value + '%';
    fetch('/set_brightness', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `brightness=${value}`
    })
    .then(res => {
        if (!res.ok) throw new Error('Network response was not OK');
        return res.json();
    })
    .then(data => {
        console.log('Brightness set response:', data);
    })
    .catch(err => console.error('Brightness set error:', err));
}

// On page load, sync UI state from backend
window.onload = () => {
    fetch('/get_status')
        .then(res => res.json())
        .then(data => {
            console.log('Initial status:', data);
            document.getElementById('light-toggle').classList.toggle('active', data.light === "ON");
            document.getElementById('fan-toggle').classList.toggle('active', data.fan === "ON");
            document.getElementById('valve-toggle').classList.toggle('active', data.valve === "OPEN");

            const slider = document.getElementById('brightness-slider');
            const display = document.getElementById('brightness-value');
            slider.value = data.brightness || 70;
            display.textContent = slider.value + '%';

            const waterFlowEl = document.getElementById('water-flow-value');
            if (data.water_flow && data.water_flow.flow_rate !== undefined) {
                waterFlowEl.textContent = data.water_flow.flow_rate + ' L/min';
            }
        })
        .catch(err => console.error('Initial fetch error:', err));
};
