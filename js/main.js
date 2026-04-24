// main.js

document.addEventListener('DOMContentLoaded', () => {
    // Check for welcome message or stored toasts after redirects
    const welcomeMsg = sessionStorage.getItem('welcomeMessage');
    if (welcomeMsg) {
        showToast(welcomeMsg, 'success');
        sessionStorage.removeItem('welcomeMessage');
    }

    // Login Form Submission Simulator
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const email = loginForm.email.value;
            if(email) {
                // Determine user role for simulation (if mentor in email, goto mentor dashboard)
                const name = email.split('@')[0];
                sessionStorage.setItem('welcomeMessage', `Welcome back, ${name}!`);
                
                if (email.includes('mentor')) {
                    window.location.href = '/dashboard_mentor.html';
                } else {
                    window.location.href = '/dashboard_student.html';
                }
            }
        });
    }

    // Signup Form Submission Simulator
    const signupForm = document.getElementById('signupForm');
    if (signupForm) {
        signupForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const role = signupForm.role.value;
            const name = signupForm.name.value;
            
            sessionStorage.setItem('welcomeMessage', `Welcome to Skillify, ${name}! Your ${role} account is ready.`);
            
            if (role === 'mentor') {
                window.location.href = '/dashboard_mentor.html';
            } else {
                window.location.href = '/dashboard_student.html';
            }
        });
    }

    // Profile Form Update Simulator
    const profileForm = document.getElementById('profileForm');
    if (profileForm) {
        profileForm.addEventListener('submit', (e) => {
            e.preventDefault();
            showToast('Profile updated successfully!', 'success');
            
            // Add a little visual cue to the button
            const submitBtn = profileForm.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            submitBtn.textContent = 'Saved!';
            submitBtn.style.background = '#00C853';
            
            setTimeout(() => {
                submitBtn.textContent = originalText;
                submitBtn.style.background = ''; // restore gradient
            }, 2000);
        });
    }

    // Modal Logic for Adding Skill (Mentor Dashboard)
    const addSkillBtn = document.getElementById('addSkillBtn');
    const skillModal = document.getElementById('skillModal');
    
    // Close modal variables
    if (skillModal) {
        const closeBtn = skillModal.querySelector('.close-btn');
        const skillForm = document.getElementById('skillForm');

        if (addSkillBtn) {
            addSkillBtn.addEventListener('click', (e) => {
                e.preventDefault();
                skillModal.classList.add('active');
            });
        }

        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                skillModal.classList.remove('active');
            });
        }

        // Close modal on outside click
        window.addEventListener('click', (e) => {
            if (e.target === skillModal) {
                skillModal.classList.remove('active');
            }
        });

        if (skillForm) {
            skillForm.addEventListener('submit', (e) => {
                e.preventDefault();
                const skillTitle = skillForm.skill_name.value;
                showToast(`Skill "${skillTitle}" added to your catalogue!`, 'success');
                skillModal.classList.remove('active');
                skillForm.reset();
                
                // Real app would update DOM here or reload
                setTimeout(() => {
                    location.reload(); 
                    // To show simulation reload properly we could save state, 
                    // but for static demo we just toast.
                }, 1000);
            });
        }
    }

    // Request connect buttons (Student Dashboard)
    const connectBtns = document.querySelectorAll('.connect-btn');
    connectBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const skillName = btn.getAttribute('data-skill');
            showToast(`Connection request sent for ${skillName}!`, 'success');
            
            btn.textContent = 'Requested';
            btn.disabled = true;
            btn.classList.remove('btn-primary');
            btn.classList.add('btn-outline');
            btn.style.borderColor = '#00C853';
            btn.style.color = '#00C853';
        });
    });
    
    // Accept/Reject buttons (Mentor Dashboard)
    const actionBtns = document.querySelectorAll('.req-action-btn');
    actionBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const action = btn.getAttribute('data-action');
            const name = btn.getAttribute('data-name');
            const card = btn.closest('.glass-card');
            
            if (action === 'accept') {
                showToast(`You accepted ${name}'s request!`, 'success');
            } else {
                showToast(`You declined ${name}'s request.`, 'info');
            }
            
            if (card) {
                card.style.opacity = '0';
                card.style.transform = 'scale(0.9)';
                setTimeout(() => card.remove(), 300);
            }
        });
    });

    // Add entry animations to cards
    const cards = document.querySelectorAll('.glass-card');
    cards.forEach((card, index) => {
        card.classList.add('slide-up');
        // stagger delays up to 5 items, then cap
        const delay = Math.min(index + 1, 5);
        card.classList.add(`delay-${delay}`);
    });
});

// Toast Notification System
window.showToast = function(message, type = 'info') {
    let container = document.querySelector('.toast-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container';
        document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    // Icon based on type
    let icon = '💡';
    if (type === 'success') icon = '✨';
    if (type === 'error') icon = '⚠️';

    toast.innerHTML = `
        <span class="toast-icon">${icon}</span>
        <span class="toast-message">${message}</span>
    `;

    container.appendChild(toast);

    // Remove toast after 4 seconds
    setTimeout(() => {
        toast.classList.add('hiding');
        toast.addEventListener('animationend', () => {
            toast.remove();
        });
    }, 4000);
};
