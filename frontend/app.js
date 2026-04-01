const API_URL = 'http://localhost:8000/api/users/';
const msgDiv = document.getElementById('message');

function showMsg(text, color = 'green') {
    msgDiv.style.color = color;
    msgDiv.innerText = text;
    setTimeout(() => msgDiv.innerText = '', 3000);
}

function getAuthHeaders(isFormData = false) {
    const token = localStorage.getItem('access_token');
    const headers = { 'Authorization': `Bearer ${token}` };
    if (!isFormData) {
        headers['Content-Type'] = 'application/json';
    }
    return headers;
}

if (localStorage.getItem('access_token')) {
    document.getElementById('auth-section').style.display = 'none';
    document.getElementById('profile-section').style.display = 'block';
    fetchProfile();
}

// Register
let regSkillsArray = [];

document.getElementById('add-skill-btn').addEventListener('click', () => {
    const skillInput = document.getElementById('reg-skill-input');
    const skill = skillInput.value.trim().toLowerCase();
    
    if (skill && !regSkillsArray.includes(skill)) {
        regSkillsArray.push(skill);
        renderRegSkills();
        skillInput.value = '';
    }
});

function renderRegSkills() {
    const container = document.getElementById('reg-skills-list');
    container.innerHTML = '';
    
    regSkillsArray.forEach((skill, index) => {
        const badge = document.createElement('span');
        badge.style.background = '#17a2b8';
        badge.style.color = 'white';
        badge.style.padding = '5px 10px';
        badge.style.borderRadius = '15px';
        badge.style.fontSize = '0.85em';
        badge.innerHTML = `${skill} <span style="cursor:pointer; margin-left:5px; color:#ffcccc; font-weight:bold;" onclick="removeRegSkill(${index})">×</span>`;
        container.appendChild(badge);
    });
}

window.removeRegSkill = function(index) {
    regSkillsArray.splice(index, 1);
    renderRegSkills();
};

document.getElementById('register-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = {
        username: document.getElementById('reg-username').value,
        password: document.getElementById('reg-password').value,
        email: document.getElementById('reg-email').value,
        skills: regSkillsArray
    };
    try {
        const res = await fetch(`${API_URL}register/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        if (res.ok) showMsg('Registered successfully! Now login.');
        else showMsg('Register failed', 'red');
    } catch (err) { console.error(err); }
});

// Login
document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = {
        username: document.getElementById('log-username').value,
        password: document.getElementById('log-password').value,
    };
    try {
        const res = await fetch(`${API_URL}login/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        const json = await res.json();
        if (res.ok) {
            localStorage.setItem('access_token', json.access);
            localStorage.setItem('refresh_token', json.refresh);
            window.location.reload();
        } else {
            showMsg('Login failed', 'red');
        }
    } catch (err) { console.error(err); }
});

async function fetchProfile() {
    try {
        const res = await fetch(`${API_URL}profile/`, { headers: getAuthHeaders() });
        const data = await res.json();
        if (res.ok) {
            document.getElementById('p-username').innerText = data.username;
            document.getElementById('p-email').innerText = data.email;
            document.getElementById('p-location').innerText = data.location || 'N/A';
            document.getElementById('p-bio').innerText = data.bio || 'N/A';
            document.getElementById('p-skills').innerText = data.skills.map(s => s.name).join(', ') || 'None';
            
            if (data.avatar) {
                const img = document.getElementById('avatar-img');
                img.src = `http://localhost:8000${data.avatar}`;
                img.style.display = 'block';
            }
        }
    } catch (err) { console.error(err); }
}

document.getElementById('update-profile-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = {
        location: document.getElementById('up-location').value,
        bio: document.getElementById('up-bio').value
    };
    try {
        const res = await fetch(`${API_URL}profile/`, {
            method: 'PATCH',
            headers: getAuthHeaders(),
            body: JSON.stringify(data)
        });
        if (res.ok) {
            showMsg('Profile updated!');
            fetchProfile();
        }
    } catch (err) { console.error(err); }
});

document.getElementById('avatar-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const fileInput = document.getElementById('up-avatar');
    const formData = new FormData();
    formData.append('avatar', fileInput.files[0]);

    try {
        const res = await fetch(`${API_URL}profile/`, {
            method: 'PATCH',
            headers: getAuthHeaders(true),
            body: formData
        });
        if (res.ok) {
            showMsg('Avatar updated!');
            fetchProfile();
        }
    } catch (err) { console.error(err); }
});

document.getElementById('logout-btn').addEventListener('click', () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    window.location.reload();
});

// Search Public Profile
document.getElementById('search-btn').addEventListener('click', async () => {
    const username = document.getElementById('search-username').value.trim();
    const pubDisplay = document.getElementById('public-profile-display');
    
    if (!username) {
        showMsg('Please enter a username first!', 'red');
        return;
    }

    try {
        const res = await fetch(`${API_URL}profile/${username}/`, {
            headers: getAuthHeaders()
        });
        
        if (res.ok) {
            const data = await res.json();
            document.getElementById('pub-username').innerText = data.username;
            document.getElementById('pub-bio').innerText = data.bio || 'N/A';
            document.getElementById('pub-location').innerText = data.location || 'N/A';
            document.getElementById('pub-skills').innerText = data.skills.map(s => s.name).join(', ') || 'None';
            
            const avatarImg = document.getElementById('pub-avatar-img');
            if (data.avatar) {
                avatarImg.src = `http://localhost:8000${data.avatar}`;
                avatarImg.style.display = 'block';
            } else {
                avatarImg.style.display = 'none';
            }
            
            pubDisplay.style.display = 'block';
            showMsg('User found!', 'green');
        } else if (res.status === 404) {
            pubDisplay.style.display = 'none';
            showMsg('User not found. Check the username.', 'red');
        } else {
            showMsg('Something went wrong.', 'red');
        }
    } catch (err) {
        console.error(err);
        showMsg('Error fetching profile.', 'red');
    }
});

const networkResults = document.getElementById('network-results');
const networkList = document.getElementById('network-list');
const networkTitle = document.getElementById('network-title');

function renderUsers(users, title) {
    networkTitle.innerText = title;
    networkList.innerHTML = '';
    
    if (users.length === 0) {
        networkList.innerHTML = '<p>No users found.</p>';
    } else {
        users.forEach(user => {
            const div = document.createElement('div');
            div.style.borderBottom = '1px solid #ccc';
            div.style.padding = '10px 0';
            div.innerHTML = `
                <strong>${user.username}</strong> 
                <span style="font-size: 0.9em; color: #555;">(Skills: ${user.skills.map(s => s.name).join(', ') || 'None'})</span>
                <button onclick="toggleFriend('${user.username}')" style="display: inline-block; width: auto; padding: 5px 10px; margin-left: 10px; font-size: 0.8em; background: #28a745;">Toggle Friend</button>
            `;
            networkList.appendChild(div);
        });
    }
    networkResults.style.display = 'block';
}

document.getElementById('skill-search-btn').addEventListener('click', async () => {
    const query = document.getElementById('skill-search-input').value.trim();
    if (!query) return showMsg('Type a skill first!', 'red');

    try {
        const res = await fetch(`${API_URL}search/skills/?query=${encodeURIComponent(query)}`, {
            headers: getAuthHeaders()
        });
        if (res.ok) {
            const data = await res.json();
            renderUsers(data, `Users knowing "${query}"`);
        }
    } catch (err) { console.error(err); }
});

document.getElementById('friend-search-btn').addEventListener('click', async () => {
    const query = document.getElementById('friend-search-input').value.trim();
    
    try {
        const res = await fetch(`${API_URL}friends/search/?username=${encodeURIComponent(query)}`, {
            headers: getAuthHeaders()
        });
        if (res.ok) {
            const data = await res.json();
            renderUsers(data, query ? `Friends matching "${query}"` : 'My Friends');
        }
    } catch (err) { console.error(err); }
});

window.toggleFriend = async function(username) {
    try {
        const res = await fetch(`${API_URL}friends/toggle/${encodeURIComponent(username)}/`, {
            method: 'POST',
            headers: getAuthHeaders()
        });
        const data = await res.json();
        
        if (res.ok) {
            showMsg(data.message, 'green');
            document.getElementById('friend-search-btn').click();
        } else {
            showMsg(data.error || 'Failed to update friend status', 'red');
        }
    } catch (err) { console.error(err); }
};
