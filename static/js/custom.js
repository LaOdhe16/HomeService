const socket = io();

// Logic Chat
function toggleChat() {
    const chatBox = document.getElementById('chatBox');
    chatBox.classList.toggle('hidden');
    if (!chatBox.classList.contains('hidden')) {
        const box = document.getElementById('messages');
        box.scrollTop = box.scrollHeight;
    }
}

function kirimPesan() {
    const input = document.getElementById('msgInput');
    
    // AMBIL DATA DARI ATRIBUT BODY 
    const currentUser = document.body.dataset.user;
    const currentRole = document.body.dataset.role;

    if(input.value.trim() !== "") {
        socket.emit('kirim_pesan', {
            msg: input.value, 
            sender: currentUser, 
            role: currentRole
        });
        input.value = '';
    }
}

socket.on('terima_pesan', (data) => {
    const box = document.getElementById('messages');
    
    // Validasi pengirim
    const currentUser = document.body.dataset.user;
    const isMe = data.sender === currentUser;
    
    const bubble = document.createElement('div');
    if(isMe) {
        bubble.className = "self-end bg-teal-600 text-white px-4 py-2 rounded-2xl rounded-tr-none shadow-md max-w-[80%] text-sm";
    } else {
        bubble.className = "self-start bg-white border border-slate-200 px-4 py-2 rounded-2xl rounded-tl-none shadow-sm max-w-[80%] text-sm text-slate-700";
    }
    
    bubble.innerHTML = `<span class="block text-[10px] opacity-70 mb-0.5 font-bold uppercase">${data.sender}</span>${data.msg}`;
    box.appendChild(bubble);
    box.scrollTop = box.scrollHeight;
});

document.getElementById('msgInput')?.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') kirimPesan();
});

// Toast Notification Logic
function showToast(message, type = 'success') {
    const container = document.getElementById('toast-container');
    if(!container) return; 

    const toast = document.createElement('div');
    
    const bgColor = type === 'success' ? 'bg-white border-l-4 border-green-500' : 'bg-white border-l-4 border-red-500';
    const textColor = type === 'success' ? 'text-green-600' : 'text-red-600';
    const icon = type === 'success' ? '✓' : '✕';

    toast.className = `${bgColor} p-4 rounded-lg shadow-2xl flex items-center gap-3 min-w-[300px] mb-3 transform transition-all duration-300 translate-x-full opacity-0`;
    toast.innerHTML = `
        <div class="w-8 h-8 rounded-full ${type==='success'?'bg-green-50':'bg-red-50'} flex items-center justify-center font-bold ${textColor}">${icon}</div>
        <p class="text-sm font-bold text-slate-700">${message}</p>
    `;

    container.appendChild(toast);

    requestAnimationFrame(() => {
        toast.classList.remove('translate-x-full', 'opacity-0');
    });

    setTimeout(() => {
        toast.classList.add('translate-x-full', 'opacity-0');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Inisialisasi Saat Halaman Dimuat
document.addEventListener("DOMContentLoaded", () => {
    
    // CEK FLASH MESSAGE DARI HTML 
    const flashContainer = document.getElementById('flash-messages');
    if (flashContainer) {
        // Ambil semua anak div di dalamnya
        const messages = flashContainer.children;
        for (let i = 0; i < messages.length; i++) {
            const msg = messages[i];
            // Panggil fungsi toast
            showToast(msg.dataset.message, msg.dataset.category);
        }
    }

    // Scroll Reveal
    if (typeof ScrollReveal !== 'undefined') {
        ScrollReveal().reveal('.reveal', { delay: 200, distance: '30px', origin: 'bottom', duration: 800, interval: 100 });
    }

    // Counter Up Animation
    const counters = document.querySelectorAll('.counter');
    counters.forEach(counter => {
        const updateCount = () => {
            const target = +counter.getAttribute('data-target');
            const count = +counter.innerText;
            const increment = target / 50; 
            if (count < target) {
                counter.innerText = Math.ceil(count + increment);
                setTimeout(updateCount, 30);
            } else {
                counter.innerText = target;
            }
        };
        updateCount();
    });
});