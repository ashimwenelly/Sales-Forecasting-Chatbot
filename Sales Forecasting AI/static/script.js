const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');
const messagesContainer = document.getElementById('messagesContainer');
const messagesInner = document.getElementById('messagesInner');
const welcomeSection = document.getElementById('welcomeSection');
const statsBtn = document.getElementById('statsBtn');
const statsModal = document.getElementById('statsModal');
const statsContent = document.getElementById('statsContent');
const sidebar = document.getElementById('sidebar');
const sidebarToggle = document.getElementById('sidebarToggle');
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const clearChatBtn = document.getElementById('clearChatBtn');

const API_BASE_URL = `${window.location.origin}/api`;

const connectionBanner = document.getElementById('connectionBanner');
const connectionBannerText = document.getElementById('connectionBannerText');
const connectionRetry = document.getElementById('connectionRetry');

let isLoading = false;
let typingEl = null;
let serverOnline = false;

function showConnectionError(message) {
    if (!connectionBanner) return;
    connectionBannerText.textContent = message;
    connectionBanner.hidden = false;
}

function hideConnectionError() {
    if (connectionBanner) connectionBanner.hidden = true;
}

async function checkServerConnection() {
    try {
        const controller = new AbortController();
        const timeout = setTimeout(() => controller.abort(), 5000);
        const res = await fetch(`${window.location.origin}/health`, {
            signal: controller.signal,
            cache: 'no-store',
        });
        clearTimeout(timeout);
        if (!res.ok) throw new Error('Server not ready');
        serverOnline = true;
        hideConnectionError();
        return true;
    } catch (err) {
        serverOnline = false;
        const isFile = window.location.protocol === 'file:';
        if (isFile) {
            showConnectionError(
                'Opened as a file. Start the server, then open http://127.0.0.1:8000 in your browser.'
            );
        } else {
            showConnectionError(
                'Cannot reach the server. Run run_chatbot.ps1, wait until it says "Uvicorn running", then refresh. (Wi‑Fi/VPN changes can cause ERR_NETWORK_CHANGED.)'
            );
        }
        return false;
    }
}

connectionRetry?.addEventListener('click', () => {
    connectionBannerText.textContent = 'Checking connection…';
    checkServerConnection();
});

function networkErrorMessage(error) {
    const msg = (error && error.message) || String(error);
    if (msg.includes('Failed to fetch') || msg.includes('NetworkError') || msg.includes('network')) {
        return 'Connection lost (ERR_NETWORK_CHANGED or server stopped). Refresh the page after the server is running.';
    }
    return msg;
}

function hideWelcome() {
    if (welcomeSection) {
        welcomeSection.remove();
    }
}

function restoreWelcome() {
    if (document.getElementById('welcomeSection')) return;
    const welcome = document.createElement('div');
    welcome.className = 'welcome-section';
    welcome.id = 'welcomeSection';
    welcome.innerHTML = `
        <div class="welcome-icon">📊</div>
        <h2>What would you like to explore?</h2>
        <p>Generate forecasts, view trends, or analyze your sales data — just ask below.</p>
        <div class="quick-actions">
            <button class="quick-action" type="button" data-prompt="Generate a 12-month forecast">
                <span class="icon">📈</span>
                <div><div class="label">12-Month Forecast</div><div class="desc">ML-powered predictions</div></div>
            </button>
            <button class="quick-action" type="button" data-prompt="Show me statistics">
                <span class="icon">📊</span>
                <div><div class="label">Statistics</div><div class="desc">Key metrics overview</div></div>
            </button>
            <button class="quick-action" type="button" data-prompt="Show historical chart">
                <span class="icon">📉</span>
                <div><div class="label">Historical Data</div><div class="desc">Sales trend chart</div></div>
            </button>
        </div>
    `;
    messagesInner.prepend(welcome);
    bindPromptButtons(welcome);
}

function autoResizeTextarea() {
    messageInput.style.height = 'auto';
    messageInput.style.height = `${Math.min(messageInput.scrollHeight, 160)}px`;
}

function updateSendButton() {
    const hasText = messageInput.value.trim().length > 0;
    sendBtn.disabled = !hasText || isLoading;
}

function scrollToBottom() {
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function showTypingIndicator() {
    removeTypingIndicator();
    typingEl = document.createElement('div');
    typingEl.className = 'typing-indicator';
    typingEl.id = 'typingIndicator';
    typingEl.innerHTML = `
        <div class="message-avatar">✦</div>
        <div class="typing-dots"><span></span><span></span><span></span></div>
    `;
    messagesInner.appendChild(typingEl);
    scrollToBottom();
}

function removeTypingIndicator() {
    if (typingEl) {
        typingEl.remove();
        typingEl = null;
    }
    const existing = document.getElementById('typingIndicator');
    if (existing) existing.remove();
}

function formatMessageText(message) {
    if (message.includes('<table') || message.includes('<img')) {
        return message;
    }
    return message
        .split('\n')
        .map((line) => {
            let escaped = line
                .replace(/&/g, '&amp;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;');
            escaped = escaped.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
            escaped = escaped.replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank" rel="noopener">$1</a>');
            return escaped;
        })
        .join('<br>');
}

function addMessageToUI(message, sender) {
    hideWelcome();

    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = sender === 'user' ? 'You' : '✦';
    if (sender === 'user') {
        avatar.textContent = '';
    }

    const content = document.createElement('div');
    content.className = 'message-content';
    content.innerHTML = formatMessageText(message);

    if (sender === 'bot') {
        messageDiv.appendChild(avatar);
    }
    messageDiv.appendChild(content);
    if (sender === 'user') {
        messageDiv.appendChild(avatar);
    }

    messagesInner.appendChild(messageDiv);
    scrollToBottom();
}

async function sendMessage(message) {
    const text = (message || messageInput.value).trim();
    if (!text || isLoading) return;

    addMessageToUI(text, 'user');
    messageInput.value = '';
    autoResizeTextarea();
    updateSendButton();

    isLoading = true;
    updateSendButton();
    showTypingIndicator();

    try {
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_message: text }),
        });

        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }

        const data = await response.json();
        removeTypingIndicator();
        addMessageToUI(data.response, 'bot');
    } catch (error) {
        console.error('Error:', error);
        removeTypingIndicator();
        showConnectionError(networkErrorMessage(error));
        addMessageToUI(
            `Unable to reach the server.\n\n**${networkErrorMessage(error)}**`,
            'bot'
        );
    } finally {
        isLoading = false;
        updateSendButton();
        messageInput.focus();
    }
}

async function clearConversation() {
    if (!confirm('Clear this conversation?')) return;

    try {
        const response = await fetch(`${API_BASE_URL}/clear`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
        });

        if (response.ok) {
            messagesInner.querySelectorAll('.message, .typing-indicator').forEach((el) => el.remove());
            restoreWelcome();
            closeSidebarMobile();
        }
    } catch (error) {
        console.error('Error clearing history:', error);
        alert('Failed to clear conversation history');
    }
}

async function showStatistics() {
    statsModal.classList.add('open');
    statsContent.innerHTML = '<div class="typing-dots" style="justify-content:center;padding:20px"><span></span><span></span><span></span></div>';

    try {
        const response = await fetch(`${API_BASE_URL}/statistics`);
        if (!response.ok) throw new Error(`API error: ${response.status}`);

        const data = await response.json();
        const fmt = (n) =>
            new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(n);
        const fmtNum = (n) => new Intl.NumberFormat('en-US').format(Math.round(n));
        const startDate = new Date(data.date_range.start).toLocaleDateString();
        const endDate = new Date(data.date_range.end).toLocaleDateString();

        statsContent.innerHTML = `
            <div class="stats-grid">
                <div class="stat-item"><span>Total records</span><span>${fmtNum(data.total_records)}</span></div>
                <div class="stat-item"><span>Total sales</span><span>${fmt(data.total_sales)}</span></div>
                <div class="stat-item"><span>Average sale</span><span>${fmt(data.average_sales)}</span></div>
                <div class="stat-item"><span>Quantity sold</span><span>${fmtNum(data.total_quantity)} units</span></div>
                <div class="stat-item"><span>Date range</span><span>${startDate} – ${endDate}</span></div>
            </div>
        `;
    } catch (error) {
        statsContent.innerHTML = `<p style="color:#f87171">Failed to load statistics: ${error.message}</p>`;
    }
}

function closeModal() {
    statsModal.classList.remove('open');
}

function closeSidebarMobile() {
    sidebar.classList.remove('open');
}

function bindPromptButtons(root = document) {
    root.querySelectorAll('[data-prompt]').forEach((btn) => {
        btn.addEventListener('click', () => {
            sendMessage(btn.getAttribute('data-prompt'));
            closeSidebarMobile();
        });
    });
}

sendBtn.addEventListener('click', () => sendMessage());

messageInput.addEventListener('input', () => {
    autoResizeTextarea();
    updateSendButton();
});

messageInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

clearChatBtn.addEventListener('click', clearConversation);
statsBtn.addEventListener('click', showStatistics);

document.querySelectorAll('[data-close-modal]').forEach((el) => {
    el.addEventListener('click', closeModal);
});

document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeModal();
});

sidebarToggle.addEventListener('click', () => {
    if (window.innerWidth <= 768) {
        sidebar.classList.toggle('open');
    } else {
        sidebar.classList.toggle('collapsed');
    }
});

mobileMenuBtn.addEventListener('click', () => {
    sidebar.classList.add('open');
});

document.addEventListener('click', (e) => {
    if (window.innerWidth <= 768 && sidebar.classList.contains('open')) {
        if (!sidebar.contains(e.target) && !mobileMenuBtn.contains(e.target)) {
            closeSidebarMobile();
        }
    }
});

document.addEventListener('DOMContentLoaded', () => {
    bindPromptButtons();
    autoResizeTextarea();
    updateSendButton();
    checkServerConnection();
    messageInput.focus();
});
