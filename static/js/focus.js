/**
 * focus.js - Logic for Zen Focus Room
 */

document.addEventListener('DOMContentLoaded', () => {
    // ---- Audio Controls ----
    const audio = document.getElementById('ambientAudio');
    const toggleAudioBtn = document.getElementById('toggleAudioBtn');
    const audioIcon = document.getElementById('audioIcon');
    let isPlaying = false;

    // Set audio volume low
    if (audio) {
        audio.volume = 0.3;
    }

    toggleAudioBtn.addEventListener('click', () => {
        if (isPlaying) {
            audio.pause();
            audioIcon.classList.remove('bi-volume-up-fill');
            audioIcon.classList.add('bi-volume-mute-fill');
            toggleAudioBtn.classList.remove('playing');
        } else {
            audio.play().catch(e => console.log("Audio play failed:", e));
            audioIcon.classList.remove('bi-volume-mute-fill');
            audioIcon.classList.add('bi-volume-up-fill');
            toggleAudioBtn.classList.add('playing');
        }
        isPlaying = !isPlaying;
    });

    // ---- Pomodoro Timer ----
    let timerInterval;
    let timeRemaining = 25 * 60; // Default 25 mins in seconds
    let isTimerRunning = false;
    let currentMode = 'focus'; // 'focus' or 'break'

    const timeDisplay = document.getElementById('timeDisplay');
    const timerStatus = document.getElementById('timerStatus');
    const startBtn = document.getElementById('startBtn');
    const pauseBtn = document.getElementById('pauseBtn');
    const resetBtn = document.getElementById('resetBtn');
    const modeBtns = document.querySelectorAll('.mode-btn');

    function updateDisplay() {
        const minutes = Math.floor(timeRemaining / 60);
        const seconds = timeRemaining % 60;
        timeDisplay.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }

    function setMode(minutes, modeStr) {
        clearInterval(timerInterval);
        isTimerRunning = false;
        startBtn.textContent = 'Start';
        timeRemaining = minutes * 60;
        currentMode = modeStr;
        updateDisplay();
        
        if (modeStr === 'break') {
            document.body.classList.add('break-mode');
            timerStatus.textContent = "Break Time";
        } else {
            document.body.classList.remove('break-mode');
            timerStatus.textContent = "Focus Mode";
        }
    }

    modeBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            // Update active class
            modeBtns.forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            
            const minutes = parseInt(e.target.getAttribute('data-time'));
            const mode = e.target.getAttribute('data-mode');
            setMode(minutes, mode);
        });
    });

    startBtn.addEventListener('click', () => {
        if (isTimerRunning) return;
        isTimerRunning = true;
        startBtn.textContent = 'Running...';
        
        timerInterval = setInterval(() => {
            timeRemaining--;
            updateDisplay();
            
            if (timeRemaining <= 0) {
                clearInterval(timerInterval);
                isTimerRunning = false;
                startBtn.textContent = 'Start';
                // Play notification sound
                new Audio('https://assets.mixkit.co/sfx/preview/mixkit-software-interface-start-2574.mp3').play();
                
                if (currentMode === 'focus') {
                    alert("Focus session complete! Take a break.");
                } else {
                    alert("Break is over! Ready to focus?");
                }
            }
        }, 1000);
    });

    pauseBtn.addEventListener('click', () => {
        clearInterval(timerInterval);
        isTimerRunning = false;
        startBtn.textContent = 'Resume';
    });

    resetBtn.addEventListener('click', () => {
        // Find active mode button and reset to its time
        const activeBtn = document.querySelector('.mode-btn.active');
        const minutes = parseInt(activeBtn.getAttribute('data-time'));
        const mode = activeBtn.getAttribute('data-mode');
        setMode(minutes, mode);
    });

    // Initialize display
    updateDisplay();

    // ---- To-Do List ----
    const taskInput = document.getElementById('newTaskInput');
    const addTaskBtn = document.getElementById('addTaskBtn');
    const taskList = document.getElementById('taskList');

    function addTask(text) {
        if (!text.trim()) return;
        
        const li = document.createElement('li');
        li.className = 'task-item';
        li.innerHTML = `
            <input type="checkbox" class="task-checkbox">
            <span class="task-text">${text}</span>
            <button class="btn-delete-task"><i class="bi bi-trash"></i></button>
        `;
        
        // Handle checkbox
        const checkbox = li.querySelector('.task-checkbox');
        checkbox.addEventListener('change', (e) => {
            if (e.target.checked) {
                li.classList.add('completed');
            } else {
                li.classList.remove('completed');
            }
        });
        
        // Handle delete
        const deleteBtn = li.querySelector('.btn-delete-task');
        deleteBtn.addEventListener('click', () => {
            li.remove();
        });
        
        taskList.appendChild(li);
        taskInput.value = '';
    }

    addTaskBtn.addEventListener('click', () => addTask(taskInput.value));
    taskInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') addTask(taskInput.value);
    });

    // Add some default placeholder tasks
    addTask("Review Physics Chapter 4");
    addTask("Complete Practice Test");


    // ---- Quick AI Chat ----
    const chatForm = document.getElementById('quickChatForm');
    const chatInput = document.getElementById('quickChatInput');
    const chatBox = document.getElementById('quickChatBox');

    function addMessage(text, isUser) {
        const div = document.createElement('div');
        div.className = `chat-message ${isUser ? 'user-message' : 'bot-message'}`;
        div.textContent = text;
        chatBox.appendChild(div);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const msg = chatInput.value.trim();
        if (!msg) return;

        addMessage(msg, true);
        chatInput.value = '';

        // Simulate AI "typing"
        const typingDiv = document.createElement('div');
        typingDiv.className = 'chat-message bot-message';
        typingDiv.textContent = 'Thinking...';
        chatBox.appendChild(typingDiv);
        chatBox.scrollTop = chatBox.scrollHeight;

        // Try to fetch from real API, fallback if fails
        try {
            const formData = new FormData();
            formData.append('message', msg);
            // csrf token
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
            const response = await fetch('/chat/send/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken
                },
                body: formData
            });
            
            typingDiv.remove();
            
            if (response.ok) {
                const data = await response.json();
                addMessage(data.response || "I'm here to help you focus!", false);
            } else {
                // Mock response
                setTimeout(() => {
                    addMessage("You're doing great! Let's stay focused on the current task.", false);
                }, 500);
            }
        } catch (error) {
            typingDiv.remove();
            addMessage("I'm in offline mode right now, but keep up the great work!", false);
        }
    });
});
