/**
 * Visualizer.js - Handles 10x UI Enhancements: Dark Mode & Charts
 */

// Theme Management
function toggleTheme() {
    const body = document.body;
    const isDark = body.classList.toggle('dark-theme');
    localStorage.setItem('ats-theme', isDark ? 'dark' : 'light');
    
    updateThemeIcons(isDark);
}

function updateThemeIcons(isDark) {
    const lightIcon = document.querySelector('.theme-icon-light');
    const darkIcon = document.querySelector('.theme-icon-dark');
    
    if (lightIcon && darkIcon) {
        lightIcon.style.display = isDark ? 'none' : 'inline';
        darkIcon.style.display = isDark ? 'inline' : 'none';
    }
}

// Initialize theme on load
document.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('ats-theme');
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-theme');
        updateThemeIcons(true);
    }
});

// Chart.js Visualizations
const Visualizer = {
    createDistributionChart(canvasId, results) {
        const ctx = document.getElementById(canvasId).getContext('2d');
        const scores = results.map(r => r.overall_score);
        
        // Group scores into buckets
        const buckets = [0, 0, 0, 0, 0]; // 0-20, 21-40, 41-60, 61-80, 81-100
        scores.forEach(s => {
            const idx = Math.min(4, Math.floor(s / 20));
            buckets[idx]++;
        });

        return new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['0-20%', '21-40%', '41-60%', '61-80%', '81-100%'],
                datasets: [{
                    label: 'Number of Candidates',
                    data: buckets,
                    backgroundColor: 'rgba(52, 152, 219, 0.6)',
                    borderColor: 'rgba(52, 152, 219, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: { beginAtZero: true, ticks: { stepSize: 1 } }
                },
                plugins: {
                    title: { display: true, text: 'Score Distribution' }
                }
            }
        });
    },

    createSkillRadarChart(canvasId, matchedSkills, missingSkills) {
        const ctx = document.getElementById(canvasId).getContext('2d');
        const labels = [...matchedSkills, ...missingSkills].slice(0, 10);
        const data = labels.map(label => matchedSkills.includes(label) ? 100 : 20);

        return new Chart(ctx, {
            type: 'radar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Skill Proficiency',
                    data: data,
                    fill: true,
                    backgroundColor: 'rgba(46, 204, 113, 0.2)',
                    borderColor: 'rgba(46, 204, 113, 1)',
                    pointBackgroundColor: 'rgba(46, 204, 113, 1)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgba(46, 204, 113, 1)'
                }]
            },
            options: {
                elements: { line: { borderWidth: 3 } },
                scales: { r: { angleLines: { display: false }, suggestMin: 0, suggestMax: 100 } }
            }
        });
    }
};
