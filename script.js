// ===========================
// DATA STORAGE & STATE
// ===========================

let currentUser = null;
let allUsers = [];
let requests = [];

// Sample skill categories with icons
const skillCategories = {
    tech: { name: 'Tech & Programming', icon: '💻', color: '#6C5CE7' },
    design: { name: 'Design & Creative', icon: '🎨', color: '#FF3366' },
    language: { name: 'Languages', icon: '🌍', color: '#00D9FF' },
    music: { name: 'Music', icon: '🎵', color: '#FFB800' },
    marketing: { name: 'Marketing', icon: '📱', color: '#00E676' },
    other: { name: 'Other', icon: '📚', color: '#A8B2D1' }
};

// Sample users data (pre-populated for demo)
const sampleUsers = [
    {
        id: 1,
        name: 'Priya Sharma',
        year: '2nd',
        bio: 'Passionate about web development and design',
        availability: ['morning', 'evening'],
        teachSkills: [
            { name: 'Python', category: 'tech', level: 'advanced' },
            { name: 'Canva', category: 'design', level: 'intermediate' }
        ],
        learnSkills: [
            { name: 'Guitar', category: 'music', level: 'beginner' },
            { name: 'Spanish', category: 'language', level: 'beginner' }
        ],
        credits: 5,
        rating: 4.8
    },
    {
        id: 2,
        name: 'Aisha Khan',
        year: '3rd',
        bio: 'Love teaching languages and learning tech',
        availability: ['evening', 'weekend'],
        teachSkills: [
            { name: 'Spanish', category: 'language', level: 'advanced' },
            { name: 'French', category: 'language', level: 'intermediate' }
        ],
        learnSkills: [
            { name: 'React', category: 'tech', level: 'intermediate' },
            { name: 'Data Science', category: 'tech', level: 'beginner' }
        ],
        credits: 8,
        rating: 4.9
    },
    {
        id: 3,
        name: 'Neha Gupta',
        year: '1st',
        bio: 'Designer exploring code',
        availability: ['morning', 'weekend'],
        teachSkills: [
            { name: 'Figma', category: 'design', level: 'advanced' },
            { name: 'Adobe XD', category: 'design', level: 'intermediate' }
        ],
        learnSkills: [
            { name: 'JavaScript', category: 'tech', level: 'beginner' },
            { name: 'HTML/CSS', category: 'tech', level: 'intermediate' }
        ],
        credits: 3,
        rating: 4.7
    },
    {
        id: 4,
        name: 'Riya Patel',
        year: '2nd',
        bio: 'Music enthusiast and tech lover',
        availability: ['afternoon', 'evening'],
        teachSkills: [
            { name: 'Guitar', category: 'music', level: 'intermediate' },
            { name: 'Music Theory', category: 'music', level: 'beginner' }
        ],
        learnSkills: [
            { name: 'Python', category: 'tech', level: 'beginner' },
            { name: 'Video Editing', category: 'design', level: 'intermediate' }
        ],
        credits: 4,
        rating: 4.6
    },
    {
        id: 5,
        name: 'Simran Singh',
        year: '3rd',
        bio: 'Full-stack developer sharing knowledge',
        availability: ['morning', 'evening'],
        teachSkills: [
            { name: 'React', category: 'tech', level: 'advanced' },
            { name: 'Node.js', category: 'tech', level: 'advanced' },
            { name: 'MongoDB', category: 'tech', level: 'intermediate' }
        ],
        learnSkills: [
            { name: 'Machine Learning', category: 'tech', level: 'beginner' },
            { name: 'UI/UX Design', category: 'design', level: 'beginner' }
        ],
        credits: 12,
        rating: 5.0
    },
    {
        id: 6,
        name: 'Kavya Reddy',
        year: '1st',
        bio: 'Marketing student learning to code',
        availability: ['weekend', 'evening'],
        teachSkills: [
            { name: 'Social Media Marketing', category: 'marketing', level: 'intermediate' },
            { name: 'Content Writing', category: 'marketing', level: 'advanced' }
        ],
        learnSkills: [
            { name: 'Canva', category: 'design', level: 'beginner' },
            { name: 'Video Editing', category: 'design', level: 'beginner' }
        ],
        credits: 2,
        rating: 4.5
    }
];

// Initialize data from localStorage or use sample data
function initializeData() {
    const savedUsers = localStorage.getItem('skillswap_users');
    const savedCurrentUser = localStorage.getItem('skillswap_currentUser');
    const savedRequests = localStorage.getItem('skillswap_requests');
    
    if (savedUsers) {
        allUsers = JSON.parse(savedUsers);
    } else {
        allUsers = [...sampleUsers];
        saveData();
    }
    
    if (savedCurrentUser) {
        currentUser = JSON.parse(savedCurrentUser);
        updateUserInterface();
    }
    
    if (savedRequests) {
        requests = JSON.parse(savedRequests);
    }
}

function saveData() {
    localStorage.setItem('skillswap_users', JSON.stringify(allUsers));
    if (currentUser) {
        localStorage.setItem('skillswap_currentUser', JSON.stringify(currentUser));
    }
    localStorage.setItem('skillswap_requests', JSON.stringify(requests));
}

// ===========================
// NAVIGATION
// ===========================

function initializeNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const pageName = link.getAttribute('data-page');
            navigateToPage(pageName);
            
            // Update active state
            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
        });
    });
    
    // Get Started buttons
    document.getElementById('createProfileBtn').addEventListener('click', () => {
        navigateToPage('profile');
    });
    
    document.getElementById('heroGetStarted').addEventListener('click', () => {
        navigateToPage('profile');
    });
    
    document.getElementById('heroBrowseSkills').addEventListener('click', () => {
        navigateToPage('browse');
    });
}

function navigateToPage(pageName) {
    // Hide all pages
    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('active');
    });
    
    // Show selected page
    const selectedPage = document.getElementById(`${pageName}-page`);
    if (selectedPage) {
        selectedPage.classList.add('active');
        
        // Load page-specific content
        if (pageName === 'browse') {
            loadBrowseSkills();
        } else if (pageName === 'requests') {
            loadRequests();
        } else if (pageName === 'profile' && currentUser) {
            showProfileView();
        }
    }
}

// ===========================
// PROFILE MANAGEMENT
// ===========================

function initializeProfileForm() {
    const form = document.getElementById('profileForm');
    
    // Add skill buttons
    document.getElementById('addTeachSkill').addEventListener('click', () => {
        addSkillInput('teachSkillsContainer');
    });
    
    document.getElementById('addLearnSkill').addEventListener('click', () => {
        addSkillInput('learnSkillsContainer');
    });
    
    // Handle remove skill buttons (event delegation)
    document.addEventListener('click', (e) => {
        if (e.target.classList.contains('remove-skill')) {
            const container = e.target.closest('.skill-input-group');
            if (container.parentElement.children.length > 1) {
                container.remove();
            } else {
                showToast('You need at least one skill!', 'error');
            }
        }
    });
    
    // Form submission
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        createUserProfile();
    });
}

function addSkillInput(containerId) {
    const container = document.getElementById(containerId);
    const skillGroup = document.createElement('div');
    skillGroup.className = 'skill-input-group';
    skillGroup.innerHTML = `
        <input type="text" class="skill-name" placeholder="Skill name">
        <select class="skill-category">
            <option value="">Category</option>
            <option value="tech">Tech</option>
            <option value="design">Design</option>
            <option value="language">Language</option>
            <option value="music">Music</option>
            <option value="marketing">Marketing</option>
            <option value="other">Other</option>
        </select>
        <select class="skill-level">
            <option value="">Level</option>
            <option value="beginner">Beginner</option>
            <option value="intermediate">Intermediate</option>
            <option value="advanced">Advanced</option>
        </select>
        <button type="button" class="btn-icon remove-skill" title="Remove">❌</button>
    `;
    container.appendChild(skillGroup);
}

function createUserProfile() {
    const name = document.getElementById('userName').value.trim();
    const year = document.getElementById('userYear').value;
    const bio = document.getElementById('userBio').value.trim();
    const college = document.getElementById('userCollege').value.trim();
    const email = document.getElementById('userEmail').value.trim();
    const phone = document.getElementById('userPhone').value.trim();

    
    if (!name || !year || !email || !college || !phone) {
        showToast('Please fill in all required fields!', 'error');
        return;
    }
    
    // Get availability
    const availabilityCheckboxes = document.querySelectorAll('input[name="availability"]:checked');
    const availability = Array.from(availabilityCheckboxes).map(cb => cb.value);
    
    if (availability.length === 0) {
        showToast('Please select at least one availability slot!', 'error');
        return;
    }
    
    // Get teach skills
    const teachSkills = getSkillsFromContainer('teachSkillsContainer');
    if (teachSkills.length === 0) {
        showToast('Please add at least one skill you can teach!', 'error');
        return;
    }
    
    // Get learn skills
    const learnSkills = getSkillsFromContainer('learnSkillsContainer');
    if (learnSkills.length === 0) {
        showToast('Please add at least one skill you want to learn!', 'error');
        return;
    }
    
    // Create user object
    const newUser = {
        id: Date.now(),
        name,
        year,
        bio,
        institution: college,
        email,
        phone,
        availability,
        teachSkills,
        learnSkills,
        credits: 0,
        rating: 0
    };
    
    currentUser = newUser;
    allUsers.push(newUser);
    saveData();
    
    showToast('Profile created successfully! 🎉', 'success');
    updateUserInterface();
    showProfileView();
}

function getSkillsFromContainer(containerId) {
    const container = document.getElementById(containerId);
    const skillGroups = container.querySelectorAll('.skill-input-group');
    const skills = [];
    
    skillGroups.forEach(group => {
        const name = group.querySelector('.skill-name').value.trim();
        const category = group.querySelector('.skill-category').value;
        const level = group.querySelector('.skill-level').value;
        
        if (name && category && level) {
            skills.push({ name, category, level });
        }
    });
    
    return skills;
}

function showProfileView() {
    if (!currentUser) {
        document.getElementById('createProfileSection').style.display = 'block';
        document.getElementById('viewProfileSection').style.display = 'none';
        return;
    }
    
    document.getElementById('createProfileSection').style.display = 'none';
    document.getElementById('viewProfileSection').style.display = 'block';
    
    const viewSection = document.getElementById('viewProfileSection');
    viewSection.innerHTML = `
        <div class="profile-header">
            <div class="profile-avatar-large">${currentUser.name.charAt(0)}</div>
            <h2>${currentUser.name}</h2>
            <p>${currentUser.year} Year | ${currentUser.institution}</p>
            <p>${currentUser.email} | ${currentUser.phone}</p>
            <p style="margin-top: 16px; color: var(--text-secondary);">${currentUser.bio}</p>
            
            <div class="profile-stats">
                <div class="stat">
                    <div class="stat-number">${currentUser.credits}</div>
                    <div class="stat-label">Credits</div>
                </div>
                <div class="stat">
                    <div class="stat-number">${currentUser.rating || 'N/A'}</div>
                    <div class="stat-label">Rating</div>
                </div>
                <div class="stat">
                    <div class="stat-number">${currentUser.teachSkills.length}</div>
                    <div class="stat-label">Can Teach</div>
                </div>
            </div>
        </div>
        
        <div class="skills-section">
            <h3>🎯 Skills I Can Teach</h3>
            <div class="skills-list">
                ${currentUser.teachSkills.map(skill => `
                    <div class="skill-item">
                        <span class="skill-tag ${skill.category}">${skill.name}</span>
                        <span class="skill-level">${skill.level}</span>
                    </div>
                `).join('')}
            </div>
        </div>
        
        <div class="skills-section">
            <h3>📚 Skills I Want to Learn</h3>
            <div class="skills-list">
                ${currentUser.learnSkills.map(skill => `
                    <div class="skill-item">
                        <span class="skill-tag ${skill.category}">${skill.name}</span>
                        <span class="skill-level">${skill.level}</span>
                    </div>
                `).join('')}
            </div>
        </div>
        
        <div class="skills-section">
            <h3>🕒 Availability</h3>
            <div class="skills-list">
                ${currentUser.availability.map(slot => `
                    <div class="skill-item">
                        <span class="badge-availability">${slot}</span>
                    </div>
                `).join('')}
            </div>
        </div>
        
        <button class="btn btn-secondary" onclick="editProfile()">Edit Profile</button>
    `;
}

function editProfile() {
    document.getElementById('createProfileSection').style.display = 'block';
    document.getElementById('viewProfileSection').style.display = 'none';
    
    // Pre-fill form with current user data
    document.getElementById('userName').value = currentUser.name;
    document.getElementById('userYear').value = currentUser.year;
    document.getElementById('userBio').value = currentUser.bio;
    document.getElementById('userCollege').value = currentUser.institution;
    document.getElementById('userEmail').value = currentUser.email;
    document.getElementById('userPhone').value = currentUser.phone;
    document.getElementById('teachSkillsContainer').innerHTML = `
        ${currentUser.teachSkills.map(skill => `
            <div class="skill-item">
                <span class="skill-tag ${skill.category}">${skill.name}</span>
                <span class="skill-level">${skill.level}</span>
            </div>
        `).join('')}
    `;

    
    // Check availability boxes
    currentUser.availability.forEach(slot => {
        const checkbox = document.querySelector(`input[name="availability"][value="${slot}"]`);
        if (checkbox) checkbox.checked = true;
    });
    
    // TODO: Pre-fill skills (more complex, skip for now)
}

function updateUserInterface() {
    if (currentUser) {
        document.getElementById('userCredits').textContent = currentUser.credits;
        document.getElementById('createProfileBtn').textContent = 'View Profile';
    }
}

// ===========================
// AI MATCHING ALGORITHM
// ===========================

function calculateMatchScore(user, currentUserSkill) {
    let score = 0;
    
    // Check if user can teach what currentUser wants to learn
    const canTeach = user.teachSkills.find(skill => 
        skill.name.toLowerCase() === currentUserSkill.name.toLowerCase()
    );
    
    if (!canTeach) return 0;
    
    // Base score for skill match
    score += 40;
    
    // Skill level match (prefer similar or slightly higher level)
    const levelPoints = {
        'beginner': 1,
        'intermediate': 2,
        'advanced': 3
    };
    
    const userLevel = levelPoints[canTeach.level] || 0;
    const desiredLevel = levelPoints[currentUserSkill.level] || 0;
    
    if (userLevel >= desiredLevel) {
        score += 30;
    } else {
        score += 10;
    }
    
    // Availability match
    if (currentUser) {
        const commonAvailability = user.availability.filter(slot => 
            currentUser.availability.includes(slot)
        );
        score += commonAvailability.length * 10;
    }
    
    // Rating bonus
    if (user.rating) {
        score += user.rating * 2;
    }
    
    return Math.min(100, Math.round(score));
}

// ===========================
// BROWSE SKILLS
// ===========================

function initializeBrowse() {
    const searchInput = document.getElementById('searchInput');
    const categoryFilter = document.getElementById('categoryFilter');
    const levelFilter = document.getElementById('levelFilter');
    const availabilityFilter = document.getElementById('availabilityFilter');
    
    searchInput.addEventListener('input', loadBrowseSkills);
    categoryFilter.addEventListener('change', loadBrowseSkills);
    levelFilter.addEventListener('change', loadBrowseSkills);
    availabilityFilter.addEventListener('change', loadBrowseSkills);
}

function loadBrowseSkills() {
    const searchQuery = document.getElementById('searchInput').value.toLowerCase();
    const categoryFilter = document.getElementById('categoryFilter').value;
    const levelFilter = document.getElementById('levelFilter').value;
    const availabilityFilter = document.getElementById('availabilityFilter').value;
    
    const container = document.getElementById('skillsList');
    
    // Get all available skills from users (except current user)
    let availableSkills = [];
    
    allUsers.forEach(user => {
        if (currentUser && user.id === currentUser.id) return;
        
        user.teachSkills.forEach(skill => {
            // Apply filters
            if (categoryFilter && skill.category !== categoryFilter) return;
            if (levelFilter && skill.level !== levelFilter) return;
            if (availabilityFilter && !user.availability.includes(availabilityFilter)) return;
            if (searchQuery && !skill.name.toLowerCase().includes(searchQuery)) return;
            
            // Calculate match score if user is logged in
            let matchScore = 0;
            if (currentUser) {
                const matchingLearnSkill = currentUser.learnSkills.find(ls => 
                    ls.name.toLowerCase() === skill.name.toLowerCase()
                );
                if (matchingLearnSkill) {
                    matchScore = calculateMatchScore(user, matchingLearnSkill);
                }
            }
            
            availableSkills.push({
                ...skill,
                user,
                matchScore
            });
        });
    });
    
    // Sort by match score
    availableSkills.sort((a, b) => b.matchScore - a.matchScore);
    
    if (availableSkills.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">🔍</div>
                <h3>No skills found</h3>
                <p>Try adjusting your filters</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = availableSkills.map(skill => `
        <div class="skill-card" onclick='showSkillDetails(${JSON.stringify(skill)})'>
            <div class="skill-card-header">
                <div class="skill-info">
                    <h3>${skill.name}</h3>
                    <div class="skill-meta">
                        <span class="skill-badge badge-level">${skill.level}</span>
                        <span class="skill-tag ${skill.category}">${skillCategories[skill.category].icon} ${skillCategories[skill.category].name}</span>
                    </div>
                </div>
                ${skill.matchScore > 0 ? `
                    <div style="text-align: center;">
                        <div class="match-score">${skill.matchScore}%</div>
                        <div class="match-label">Match</div>
                    </div>
                ` : ''}
            </div>
            
            <div class="student-info">
                <div class="student-avatar">${skill.user.name.charAt(0)}</div>
                <div>
                    <div class="student-name">${skill.user.name}</div>
                    <div class="student-year">${skill.user.year} Year${skill.user.rating ? ` • ⭐ ${skill.user.rating}` : ''}</div>
                </div>
            </div>
            
            <div style="margin-top: 12px;">
                <strong>Available:</strong> ${skill.user.availability.join(', ')}
            </div>
            
            <div class="skill-card-actions">
                <button class="btn btn-primary" onclick='sendRequest(${skill.user.id}, "${skill.name}", event)'>
                    Request Exchange
                </button>
                <button class="btn btn-secondary" onclick='viewUserProfile(${skill.user.id}, event)'>
                    View Profile
                </button>
            </div>
        </div>
    `).join('');
}

function showSkillDetails(skill) {
    const modal = document.getElementById('skillModal');
    const modalBody = document.getElementById('modalBody');
    
    modalBody.innerHTML = `
        <h2>${skill.name}</h2>
        <div style="margin: 24px 0;">
            <div class="skill-tag ${skill.category}">${skillCategories[skill.category].icon} ${skillCategories[skill.category].name}</div>
            <span class="skill-badge badge-level" style="margin-left: 8px;">${skill.level}</span>
        </div>
        
        <div class="student-info" style="margin-bottom: 24px;">
            <div class="student-avatar" style="width: 60px; height: 60px; font-size: 24px;">${skill.user.name.charAt(0)}</div>
            <div>
                <div class="student-name" style="font-size: 18px;">${skill.user.name}</div>
                <div class="student-year">${skill.user.year} Year | ${skill.user.college}</div>
                <div class="student-year">${skill.user.email} | ${skill.user.phone}</div>
                ${skill.user.rating ? `<div style="margin-top: 4px;">⭐ ${skill.user.rating} / 5.0</div>` : ''}
            </div>
        </div>
        
        ${skill.user.bio ? `<p style="margin-bottom: 16px; color: var(--text-secondary);">${skill.user.bio}</p>` : ''}
        
        <div style="margin: 16px 0;">
            <strong>Available:</strong> ${skill.user.availability.join(', ')}
        </div>
        
        ${skill.matchScore > 0 ? `
             <div style="background: var(--bg-main); padding: 16px; border-radius: 8px; margin: 16px 0;">
                <div style="display: flex; align-items: center; justify-content: space-between;">
                    <span>Match Score</span>
                    <span style="font-size: 24px; font-weight: 800; color: var(--primary);">${skill.matchScore}%</span>
                </div>
            </div>
        ` : ''}
        
        <div style="display: flex; gap: 12px; margin-top: 24px;">
            <button class="btn btn-primary btn-large" onclick='sendRequest(${skill.user.id}, "${skill.name}", event)'>
                Request Skill Exchange
            </button>
        </div>
    `;
    
    modal.classList.add('active');
}

function viewUserProfile(userId, event) {
    if (event) event.stopPropagation();
    
    const user = allUsers.find(u => u.id === userId);
    if (!user) return;
    
    const modal = document.getElementById('skillModal');
    const modalBody = document.getElementById('modalBody');
    
    modalBody.innerHTML = `
         <div style="text-align: center; margin-bottom: 24px;">
            <div class="student-avatar" style="width: 100px; height: 100px; font-size: 40px; margin: 0 auto 16px;">${user.name.charAt(0)}</div>
            <h2>${user.name}</h2>
            <p>${user.year} Year | ${user.college}</p>
            ${user.rating ? `<p>⭐ ${user.rating} / 5.0</p>` : ''}
        </div>
        
        ${user.bio ? `<p style="margin-bottom: 24px; color: var(--text-secondary); text-align: center;">${user.bio}</p>` : ''}
        
        <div style="margin-bottom: 24px;">
            <h3 style="margin-bottom: 12px;">🎯 Can Teach</h3>
            <div style="display: flex; flex-wrap: wrap; gap: 8px;">
                ${user.teachSkills.map(skill => `
                    <span class="skill-tag ${skill.category}">${skill.name} (${skill.level})</span>
                `).join('')}
            </div>
        </div>
        
        <div style="margin-bottom: 24px;">
            <h3 style="margin-bottom: 12px;">📚 Wants to Learn</h3>
            <div style="display: flex; flex-wrap: wrap; gap: 8px;">
                ${user.learnSkills.map(skill => `
                    <span class="skill-tag ${skill.category}">${skill.name} (${skill.level})</span>
                `).join('')}
            </div>
        </div>
        
        <div>
            <h3 style="margin-bottom: 12px;">🕒 Availability</h3>
            <p>${user.availability.join(', ')}</p>
        </div>
    `;
    
    modal.classList.add('active');
}

// ===========================
// REQUESTS MANAGEMENT
// ===========================

function sendRequest(recipientId, skillName, event) {
    if (event) event.stopPropagation();
    
    if (!currentUser) {
        showToast('Please create a profile first!', 'error');
        navigateToPage('profile');
        return;
    }
    
    const recipient = allUsers.find(u => u.id === recipientId);
    if (!recipient) return;
    
    // Check if request already exists
    const existingRequest = requests.find(r => 
        r.senderId === currentUser.id && 
        r.recipientId === recipientId && 
        r.skillRequested === skillName &&
        r.status === 'pending'
    );
    
    if (existingRequest) {
        showToast('You already have a pending request for this skill!', 'error');
        return;
    }
    
    const newRequest = {
        id: Date.now(),
        senderId: currentUser.id,
        senderName: currentUser.name,
        recipientId,
        recipientName: recipient.name,
        skillRequested: skillName,
        status: 'pending',
        timestamp: new Date().toISOString()
    };
    
    requests.push(newRequest);
    saveData();
    
    showToast('Request sent successfully! 🎉', 'success');
    
    // Close modal if open
    const modal = document.getElementById('skillModal');
    modal.classList.remove('active');
}

function loadRequests() {
    if (!currentUser) {
        document.getElementById('receivedRequests').innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">👤</div>
                <h3>Create a profile first</h3>
                <p>You need to create a profile to send and receive requests</p>
            </div>
        `;
        document.getElementById('sentRequests').innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">👤</div>
                <h3>Create a profile first</h3>
                <p>You need to create a profile to send and receive requests</p>
            </div>
        `;
        return;
    }
    
    // Load received requests
    const receivedRequests = requests.filter(r => r.recipientId === currentUser.id);
    const receivedContainer = document.getElementById('receivedRequests');
    
    if (receivedRequests.length === 0) {
        receivedContainer.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">📭</div>
                <h3>No requests yet</h3>
                <p>You haven't received any skill exchange requests</p>
            </div>
        `;
    } else {
        receivedContainer.innerHTML = receivedRequests.map(request => `
            <div class="request-card">
                <div class="request-header">
                    <div>
                        <h3>${request.senderName}</h3>
                        <p style="color: var(--text-secondary); margin: 4px 0;">wants to learn <strong>${request.skillRequested}</strong></p>
                        <p style="font-size: 12px; color: var(--text-muted);">${formatDate(request.timestamp)}</p>
                    </div>
                    <span class="status-badge status-${request.status}">${request.status}</span>
                </div>
                ${request.status === 'pending' ? `
                    <div class="request-actions">
                        <button class="btn btn-primary" onclick="acceptRequest(${request.id})">Accept</button>
                        <button class="btn btn-secondary" onclick="declineRequest(${request.id})">Decline</button>
                    </div>
                ` : ''}
            </div>
        `).join('');
    }
    
    // Load sent requests
    const sentRequests = requests.filter(r => r.senderId === currentUser.id);
    const sentContainer = document.getElementById('sentRequests');
    
    if (sentRequests.length === 0) {
        sentContainer.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">📤</div>
                <h3>No requests sent</h3>
                <p>Browse skills and send exchange requests!</p>
            </div>
        `;
    } else {
        sentContainer.innerHTML = sentRequests.map(request => `
            <div class="request-card">
                <div class="request-header">
                    <div>
                        <h3>To: ${request.recipientName}</h3>
                        <p style="color: var(--text-secondary); margin: 4px 0;">Skill: <strong>${request.skillRequested}</strong></p>
                        <p style="font-size: 12px; color: var(--text-muted);">${formatDate(request.timestamp)}</p>
                    </div>
                    <span class="status-badge status-${request.status}">${request.status}</span>
                </div>
            </div>
        `).join('');
    }
}

function acceptRequest(requestId) {
    const request = requests.find(r => r.id === requestId);
    if (!request) return;
    
    request.status = 'accepted';
    saveData();
    
    showToast('Request accepted! You can now coordinate the session.', 'success');
    loadRequests();
}

function declineRequest(requestId) {
    const request = requests.find(r => r.id === requestId);
    if (!request) return;
    
    request.status = 'declined';
    saveData();
    
    showToast('Request declined.', 'info');
    loadRequests();
}

// ===========================
// TABS
// ===========================

function initializeTabs() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    
    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabName = btn.getAttribute('data-tab');
            
            // Update active button
            tabButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            // Update active content
            document.querySelectorAll('.tab-content').forEach(content => {
                content.classList.remove('active');
            });
            
            const activeContent = document.getElementById(`${tabName}Requests`);
            if (activeContent) {
                activeContent.classList.add('active');
            }
        });
    });
}

// ===========================
// MODAL
// ===========================

function initializeModal() {
    const modal = document.getElementById('skillModal');
    const closeBtn = document.querySelector('.modal-close');
    
    closeBtn.addEventListener('click', () => {
        modal.classList.remove('active');
    });
    
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.remove('active');
        }
    });
}

// ===========================
// TOAST NOTIFICATIONS
// ===========================

function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideInRight 0.3s ease-out reverse';
        setTimeout(() => {
            container.removeChild(toast);
        }, 300);
    }, 3000);
}

// ===========================
// UTILITY FUNCTIONS
// ===========================

function formatDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);
    
    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins} minutes ago`;
    if (diffHours < 24) return `${diffHours} hours ago`;
    if (diffDays < 7) return `${diffDays} days ago`;
    
    return date.toLocaleDateString();
}

// ===========================
// INITIALIZATION
// ===========================

document.addEventListener('DOMContentLoaded', () => {
    initializeData();
    initializeNavigation();
    initializeProfileForm();
    initializeBrowse();
    initializeTabs();
    initializeModal();
    
    // Update stats on home page
    document.getElementById('totalStudents').textContent = allUsers.length;
    document.getElementById('totalSkills').textContent = allUsers.reduce((sum, user) => sum + user.teachSkills.length, 0);
    document.getElementById('totalSwaps').textContent = requests.filter(r => r.status === 'completed').length;
});
document.getElementById('userDocument').addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        const allowedTypes = ['image/jpeg', 'image/png', 'application/pdf'];
        if (!allowedTypes.includes(file.type)) {
            showToast('Invalid file type! Please upload a JPG, PNG, or PDF.', 'error');
            e.target.value = '';
            return;
        }
        
        if (file.size > 5 * 1024 * 1024) { // 5MB limit
            showToast('File size exceeds 5MB! Please upload a smaller file.', 'error');
            e.target.value = '';
            return;
        }
        
        showToast('Document uploaded successfully!', 'success');
    }
});
document.getElementById('profileForm').addEventListener('submit', (e) => {
    e.preventDefault();
    
    const documentInput = document.getElementById('userDocument');
    if (documentInput.files.length === 0) {
        showToast('Please upload a valid ID for verification!', 'error');
        return;
    }
        
    createUserProfile();
});
